""" Sum factorization vectorization """

from __future__ import division

import logging

from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.loopy.vcl import get_vcl_type_size
from dune.codegen.sumfact.symbolic import SumfactKernel, VectorizedSumfactKernel
from dune.codegen.generation import (generator_factory,
                                     get_counted_variable,
                                     get_global_context_value,
                                     retrieve_cache_items,
                                     )
from dune.codegen.sumfact.tabulation import (quadrature_points_per_direction,
                                             set_quadrature_points,
                                             )
from dune.codegen.error import CodegenVectorizationError
from dune.codegen.options import get_form_option, get_option, form_option_context
from dune.codegen.tools import add_to_frozendict, round_to_multiple, list_diff

from pymbolic.mapper.flop_counter import FlopCounter
from pytools import product
from frozendict import frozendict
import math


@generator_factory(item_tags=("vecinfo", "dryrundata"), cache_key_generator=lambda o, n: o)
def _cache_vectorization_info(old, new):
    if get_form_option("vectorization_not_fully_vectorized_error"):
        if not isinstance(new, VectorizedSumfactKernel):
            raise CodegenVectorizationError("Did not fully vectorize!")
    if new is None:
        raise CodegenVectorizationError("Vectorization info for sum factorization kernel was not gathered correctly!")
    return new


_collect_sumfact_nodes = generator_factory(item_tags=("sumfactnodes", "dryrundata"), context_tags="kernel", no_deco=True)


def attach_vectorization_info(sf):
    assert isinstance(sf, SumfactKernel)
    if get_global_context_value("dry_run"):
        return _collect_sumfact_nodes(sf)
    else:
        return _cache_vectorization_info(sf, None)


def costmodel(sf):
    # Penalize vertical vectorization and scalar execution
    verticality = sf.vertical_width
    if isinstance(sf, SumfactKernel):
        verticality = get_vcl_type_size(dtype_floatingpoint())
    vertical_penalty = 1 + 0.5 * math.log(verticality, 2)

    memory_penalty = 1.0
    if isinstance(sf, VectorizedSumfactKernel):
        memory_penalty = 1.0 + 0.25 * math.log(len(set(k.interface for k in sf.kernels)), 2)

    # Return total operations
    return sf.operations * vertical_penalty * memory_penalty


def explicit_costfunction(sf):
    # Read the explicitly set values for horizontal and vertical vectorization
    width = get_vcl_type_size(dtype_floatingpoint())
    horizontal = get_form_option("vectorization_horizontal")
    if horizontal is None:
        horizontal = width
    vertical = get_form_option("vectorization_vertical")
    if vertical is None:
        vertical = 1
    horizontal = int(horizontal)
    vertical = int(vertical)

    if sf.horizontal_width == horizontal and sf.vertical_width == vertical:
        # Penalize position mapping
        return sf.operations
    else:
        return 1000000000000


def target_costfunction(sf):
    # The cost of a kernel is given by the difference to the desired target cost.
    # Pitfall: The target cost needs to be weighed to account for this being called
    # on subsets and not on a full vectorization strategy!
    _, all_sf, _ = filter_active_inactive_sumfacts()
    total = len(all_sf)
    target = float(get_form_option("vectorization_target"))
    realcost = costmodel(sf)
    ratio = sf.horizontal_width / total
    return abs(realcost - ratio * target)


def accumulate_for_strategy(strategy, func, reduce=lambda x, y: x + y, start=0):
    """ Accumulate a quantity over a given vectorization strategy """
    accum = start

    # Make sure to count each implementation exactly once
    keys = set(sf.cache_key for sf in strategy.values())
    for sf in strategy.values():
        if sf.cache_key in keys:
            accum = reduce(accum, func(sf))
            keys.discard(sf.cache_key)

    return accum


def strategy_cost(strat_tuple):
    qp, strategy = strat_tuple

    # Choose the correct cost function
    s = get_form_option("vectorization_strategy")
    if s == "model":
        func = costmodel
    elif s == "explicit":
        func = explicit_costfunction
    elif s == "target":
        func = target_costfunction
    elif s == "autotune":
        from dune.codegen.sumfact.autotune import autotune_realization
        func = autotune_realization
    else:
        raise NotImplementedError("Vectorization strategy '{}' unknown!".format(s))

    keys = set(sf.cache_key for sf in strategy.values())
    set_quadrature_points(qp)

    return accumulate_for_strategy(strategy, lambda sf: float(func(sf)))


class PrimitiveApproximateOpcounter(FlopCounter):
    def map_sumfact_kernel(self, expr):
        return 0

    def map_tagged_variable(self, expr):
        return self.map_variable(expr)

    def map_loopy_function_identifier(self, expr):
        if hasattr(expr, "operations"):
            return expr.operations()

        raise NotImplementedError("The class {} should implement a symbolic flopcounter.".format(type(expr)))


@generator_factory(item_tags=("opcounts",), context_tags="kernel")
def store_operation_count(expr, count):
    return count


def count_quadrature_point_operations(expr):
    counter = PrimitiveApproximateOpcounter()
    store_operation_count(expr, counter(expr))


def quadrature_penalized_strategy_cost(strat_tuple):
    """ Implements a penalization of the cost function that accounts for
    the increase in flops that occur in the quadrature loop. This needs to
    somehow get a guess of how much work is done in the quadrature loop relative
    to the sum factorization kernels.
    """
    qp, strategy = strat_tuple

    # Evaluate the original cost function. This result will be scaled by this function.
    cost = strategy_cost(strat_tuple)
    if cost is 0:
        return 0

    # Get the total number of Flops done in sum factorization kernels
    sf_flops = accumulate_for_strategy(strategy, lambda sf: sf.operations)

    # Get the minimal possible number of quadrature points and the actual quadrature points
    num_qp_new = product(qp)
    set_quadrature_points(None)
    num_qp_old = product(quadrature_points_per_direction())
    set_quadrature_points(qp)

    # Determine the number of floating point operations per quadrature point.
    # This flop counting is a very crude approximation, but that is totally sufficient here.
    ops_per_qp = sum(i for i in retrieve_cache_items("opcounts"))

    # Do the actual scaling.
    return float((sf_flops + ops_per_qp * num_qp_new) / (sf_flops + ops_per_qp * num_qp_old)) * cost


def fixedqp_strategy_costfunction(qp):
    def _cost(strategy):
        return strategy_cost((qp, strategy))

    return _cost


def stringify_vectorization_strategy(strategy):
    result = []
    qp, strategy = strategy

    result.append("Printing potential vectorization strategy:")
    result.append("Quadrature point tuple: {}".format(qp))

    # Look for all realizations in the strategy and iterate over them
    cache_keys = frozenset(v.cache_key for v in strategy.values())
    for ck in cache_keys:
        # Filter all the kernels that are realized by this and print
        for key in strategy:
            if strategy[key].cache_key == ck:
                result.append("{}:".format(key))

        # Find one representative to print
        for val in strategy.values():
            if val.cache_key == ck:
                result.append("    {}".format(val))
                break

    return result


def short_stringify_vectorization_strategy(strategy):
    """ A short string decribing the vectorization strategy. This is used
    in costmodel validation plots to describe what a data point does
    """
    qp, strategy = strategy

    def _short(k):
        if isinstance(k, VectorizedSumfactKernel):
            return str(k.horizontal_width)
        else:
            return "scalar"

    stage1 = []
    stage3 = []
    keys = set(sf.cache_key for sf in strategy.values())
    for kernel in strategy.values():
        if kernel.cache_key in keys:
            keys.discard(kernel.cache_key)
            if kernel.stage == 1:
                stage1.append(_short(kernel))
            if kernel.stage == 3:
                stage3.append(_short(kernel))

    return "m0={};S1:{};S3:{}".format(qp[0], "|".join(stage1), "|".join(stage3))


def filter_active_inactive_sumfacts():
    # Retrieve all sum factorization kernels for stage 1 and 3
    from dune.codegen.generation import retrieve_cache_items
    all_sumfacts = [i for i in retrieve_cache_items("kernel_default and sumfactnodes")]

    # Stage 1 sum factorizations that were actually used
    basis_sumfacts = [i for i in retrieve_cache_items('kernel_default and basis_sf_kernels')]

    # This means we can have sum factorizations that will not get used
    inactive_sumfacts = [i for i in all_sumfacts if i.stage == 1 and i not in basis_sumfacts]

    # All sum factorization kernels that get used
    active_sumfacts = [i for i in all_sumfacts if i.stage == 3 or i in basis_sumfacts]

    return all_sumfacts, active_sumfacts, inactive_sumfacts


def decide_vectorization_strategy():
    """ Decide how to vectorize!
    Note that the vectorization of the quadrature loop is independent of this,
    as it is implemented through a post-processing (== loopy transformation) step.
    """
    logger = logging.getLogger(__name__)

    all_sumfacts, active_sumfacts, inactive_sumfacts = filter_active_inactive_sumfacts()

    # If no vectorization is needed, abort now
    if get_form_option("vectorization_strategy") == "none" or (get_global_context_value("form_type") == "jacobian" and not get_form_option("vectorization_jacobians")) or not get_form_option("sumfact"):
        for sf in all_sumfacts:
            _cache_vectorization_info(sf, sf.copy(buffer=get_counted_variable("buffer")))
        return

    logger.debug("decide_vectorization_strategy: Found {} active sum factorization nodes"
                 .format(len(active_sumfacts)))

    #
    # Find the best vectorization strategy by using a costmodel
    #
    # Note that this optimization procedure uses a hierarchic approach to bypass
    # the problems of unfavorable complexity of the set of all possible vectorization
    # opportunities. Optimizations are performed at different levels (you find these
    # levels in the function names implementing them), where optimal solutions at a
    # higher level are combined into lower level solutions or optima of optimal solutions
    # at higher level are calculated:
    # * Level 1: Finding an optimal quadrature tuple (by finding optimum of level 2 optima)
    # * Level 2: Split by parallelizability and combine optima into optimal solution
    # * Level 3: Optimize number of different inputs to consider
    # * Level 4: Optimize horizontal/vertical/hybrid strategy
    width = get_vcl_type_size(dtype_floatingpoint())
    qp, sfdict = level1_optimal_vectorization_strategy(active_sumfacts, width)

    set_quadrature_points(qp)
    logger.debug("decide_vectorization_strategy: Decided for the following strategy:" +
                 "\n  " +
                 "\n  ".join(stringify_vectorization_strategy((qp, sfdict))))

    # We map inactive sum factorization kernels to 0
    sfdict = add_to_frozendict(sfdict, {sf: 0 for sf in inactive_sumfacts})

    # Register the results
    for sf in all_sumfacts:
        _cache_vectorization_info(sf, sfdict[sf])


def level1_optimal_vectorization_strategy(sumfacts, width):
    # Gather a list of possible quadrature point tuples
    quad_points = [quadrature_points_per_direction()]
    if get_form_option("vectorization_allow_quadrature_changes"):
        sf = next(iter(sumfacts))
        depth = 1
        while depth <= width:
            i = 0 if sf.matrix_sequence_quadrature_permuted[0].face is None else 1
            quad = list(quadrature_points_per_direction())
            quad[i] = round_to_multiple(quad[i], depth)
            quad_points.append(tuple(quad))
            depth = depth * 2
        quad_points = list(set(quad_points))

    # Find the minimum cost strategy between all the quadrature point tuples
    optimal_strategies = {qp: level2_optimal_vectorization_strategy(sumfacts, width, qp) for qp in quad_points}

    # If we are using the 'target' strategy, we might want to log some information.
    if get_form_option("vectorization_strategy") == "target":
        # Print the achieved cost and the target cost on the screen
        with form_option_context(vectorization_strategy="model"):
            target = float(get_form_option("vectorization_target"))
            qp = min(optimal_strategies, key=lambda qp: abs(strategy_cost((qp, optimal_strategies[qp])) - target))
            cost = strategy_cost((qp, optimal_strategies[qp]))

            print("The target cost was:   {}".format(target))
            print("The achieved cost was: {}".format(cost))
            optimum = level1_optimal_vectorization_strategy(sumfacts, width)
            print("The optimal cost would be: {}".format(strategy_cost(optimum)))
            print("The score in 'target' logic was: {}".format(strategy_cost((qp, optimal_strategies[qp]))))

        # Print the employed vectorization strategy into a file
        suffix = ""
        if get_global_context_value("integral_type") == "interior_facet":
            suffix = "_dir{}_mod{}".format(get_global_context_value("facedir_s"),
                                           get_global_context_value("facemod_s"))
        filename = "targetstrat_{}{}.log".format(int(float(get_form_option("vectorization_target"))), suffix)
        with open(filename, 'w') as f:
            f.write("\n".join(stringify_vectorization_strategy((qp, optimal_strategies[qp]))))

        # Write an entry into a csvfile which connects the given measuring identifier with a cost
        from dune.testtools.parametertree.parser import parse_ini_file
        inifile = parse_ini_file(get_option("ini_file"))
        identifier = inifile["identifier"]

        # TODO: Depending on the number of samples, we might need a file lock here.
        with open("mapping.csv", 'a') as f:
            f.write(" ".join((identifier, str(cost), short_stringify_vectorization_strategy((qp, optimal_strategies[qp])))) + "\n")
    else:
        qp = min(optimal_strategies, key=lambda qp: quadrature_penalized_strategy_cost((qp, optimal_strategies[qp])))

    return qp, optimal_strategies[qp]


def level2_optimal_vectorization_strategy(sumfacts, width, qp):
    # Find the sets of simultaneously realizable kernels
    keys = frozenset(sf.parallel_key for sf in sumfacts)

    # Find minimums for each of these sets
    sfdict = frozendict()

    for key in keys:
        key_sumfacts = frozenset(sf for sf in sumfacts if sf.parallel_key == key)

        # Minimize over all the opportunities for the subset given by the current key
        key_strategy = min(level2_optimal_vectorization_strategy_generator(key_sumfacts, width, qp),
                           key=fixedqp_strategy_costfunction(qp))
        sfdict = add_to_frozendict(sfdict, key_strategy)

    return sfdict


def level2_optimal_vectorization_strategy_generator(sumfacts, width, qp):
    for opp in _level2_optimal_vectorization_strategy_generator(sumfacts, width, qp):
        # Add non-vectorized implementation information to all kernels that are not present in
        # the optimal strategy
        yield add_to_frozendict(opp,
                                {sf: sf.copy(buffer=get_counted_variable("buffer")) for sf in sumfacts if sf not in opp})


def _level2_optimal_vectorization_strategy_generator(sumfacts, width, qp, already=frozendict()):
    if len(sumfacts) == 0:
        yield already
        return

    # We store the information whether a vectorization opportunity has been yielded from this
    # generator to yield an incomplete strategy if not (which is then completed with unvectorized
    # kernel implementations)
    yielded = False

    # Find the number of input coefficients we can work on
    keys = frozenset(sf.inout_key for sf in sumfacts)

    inoutkey_sumfacts = [tuple(sorted(filter(lambda sf: sf.inout_key == key, sumfacts))) for key in sorted(keys)]

    for parallel in (1, 2):
        if parallel > len(keys):
            continue

        horizontal = 1
        while horizontal <= width // parallel:
            combo = sum((inoutkey_sumfacts[part][:horizontal] for part in range(parallel)), ())

            vecdict = get_vectorization_dict(combo, width // (horizontal * parallel), horizontal * parallel, qp)
            horizontal *= 2

            if vecdict is None:
                # This particular choice was rejected for some reason.
                # Possible reasons:
                # * the quadrature point tuple not being suitable
                #   for this vectorization strategy
                # * there are not enough horizontal kernels
                continue

            # Go into recursion to also vectorize all kernels not in this combo
            for opp in _level2_optimal_vectorization_strategy_generator(list_diff(sumfacts, combo),
                                                                        width,
                                                                        qp,
                                                                        add_to_frozendict(already, vecdict),
                                                                        ):
                yielded = True
                yield opp

    # If we did not yield on this recursion level, yield what we got so far
    if not yielded:
        yield already


def get_vectorization_dict(sumfacts, vertical, horizontal, qp):
    # Discard opportunities that do not contain enough horizontal kernels
    if len(sumfacts) not in (horizontal, horizontal * vertical - 1):
        return None

    # Enhance the list of sumfact nodes by adding vertical splittings
    kernels = []
    for sf in sumfacts:
        # No slicing needed in the pure horizontal case
        if vertical == 1:
            kernels.append(sf)
            continue

        # Determine the slicing direction
        slice_direction = 0 if sf.matrix_sequence_quadrature_permuted[0].face is None else 1
        if qp[slice_direction] % vertical != 0:
            return None

        # Split the basis tabulation matrices
        oldtab = sf.matrix_sequence_quadrature_permuted[slice_direction]
        for i in range(vertical):
            seq = list(sf.matrix_sequence_quadrature_permuted)
            seq[slice_direction] = oldtab.copy(slice_size=vertical,
                                               slice_index=i)

            # Create new sf kernel with new interface
            kwargs = sf.interface.get_keyword_arguments()
            kwargs.update({'matrix_sequence': tuple(seq)})
            newinterface = type(sf.interface)(**kwargs)
            kernels.append(sf.copy(matrix_sequence=tuple(seq), interface=newinterface))

    # Join the new kernels into a sum factorization node
    buffer = get_counted_variable("joined_buffer")
    return {sf: VectorizedSumfactKernel(kernels=tuple(kernels),
                                        horizontal_width=horizontal,
                                        vertical_width=vertical,
                                        buffer=buffer,
                                        ) for sf in sumfacts}
