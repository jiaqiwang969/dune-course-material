from collections import defaultdict, OrderedDict
from functools import reduce
from itertools import groupby
from operator import or_

import loopy as lp
import pymbolic.primitives as prim
from dune.codegen.loopy.symbolic import FusedMultiplyAdd
from dune.codegen.loopy.vcl import VCLLoad, VCLStore
from dune.codegen.options import get_form_option
from dune.codegen.tools import get_pymbolic_basename
from loopy.kernel.data import VectorizeTag
from loopy.symbolic import WalkMapper, IdentityMapper, CombineMapper, DependencyMapper
from pytools import memoize


class UnknownLoopNesting(RuntimeError):
    pass


class CountTerms(WalkMapper):
    """
    Iterates over all expressions and counts the individual terms.
    These are stored in a map, with a corresponding counter variable.
    Static terms are skipped because they are not to be replaced later.
    """
    def __init__(self, inames, cost_estimator):
        self.cache = defaultdict(lambda: 0)
        self.ids = defaultdict(list)
        self.inames = inames
        self.active_inames = frozenset()
        self.cost_estimator = cost_estimator
        super().__init__()

    def __call__(self, expr, insnId, active_inames, *args, **kwargs):
        self.active_inames = active_inames
        ret = super().__call__(expr, insnId, *args, **kwargs)
        self.active_inames = frozenset()
        return ret

    def addToDict(self, expr, insnId):
        self.cache[expr] += self.cost_estimator(self.active_inames - self.inames[expr])

        self.ids[expr] += [insnId]

    def visit(self, expr, insnId):
        if isinstance(expr, prim.Expression):
            self.addToDict(expr, insnId)
        return True

    def map_reduction(self, expr, *args, **kwargs):
        old_active_inames = self.active_inames
        self.active_inames = frozenset()  # currently ignore reductions bc of problem if cse depends on reduction inames
        self.rec(expr.expr, *args, **kwargs)
        self.active_inames = old_active_inames

    def map_subscript(self, expr, insnId):
        pass

    def map_variable(self, expr, insnId):
        pass

    def map_constant(self, expr, insnId):
        pass

    def map_loopy_function_identifier(self, expr, insnId):
        pass

    def map_call(self, expr, insnId):
        # This whole special case if very unfortunate, but it will eventually go away
        # in the transition to kernel callables anyway.
        from dune.codegen.pdelab.argument import PDELabAccumulationFunction, CoefficientAccess
        if isinstance(expr.function, PDELabAccumulationFunction):
            self.rec(expr.parameters[-1], insnId)
        elif isinstance(expr.function, CoefficientAccess):
            pass  # deactivate cse for coefficient indices
        elif isinstance(expr.function, (VCLLoad, VCLStore)):
            pass  # deactivate cse for vcl load and store functions
        else:
            WalkMapper.map_call(self, expr, insnId)

    def map_if(self, expr, *args, **kwargs):
        if not self.visit(expr, *args, **kwargs):
            return

        # currently don't apply caching to condition
        self.rec(expr.then, *args, **kwargs)
        self.rec(expr.else_, *args, **kwargs)

        self.post_visit(expr, *args, **kwargs)


class SplitByIname(IdentityMapper):
    def __init__(self, inames):
        self.inames = dict((k, frozenset(v)) for k, v in inames.items())
        self.active_inames = tuple()

    def map_sum(self, expr, **kwargs):
        groups = tuple(tuple(g) for k, g in groupby(sorted(expr.children, key=lambda c: hash(self.inames[c])),
                                                    lambda c: self.inames[c]))
        if (len(groups) == len(expr.children)) or (len(groups) == 1):
            return super().map_sum(expr, **kwargs)
        else:
            groups = sorted(groups, key=lambda g: len(self.inames[g[0]]))
            group_inames = [self.inames[g[0]] for g in groups]
            if not all(a <= b for a, b in zip(group_inames[:-1], group_inames[1:])):
                raise UnknownLoopNesting()
            children = []
            for group in groups:
                if len(group) > 1:
                    children.append(prim.Sum(tuple(self.rec(c) for c in group)))
                else:
                    children.append(self.rec(group[0]))
            s = children[0]
            for c in children[1:]:
                s = prim.Sum((s, c))
            return s

    def map_product(self, expr, **kwargs):
        groups = tuple(tuple(g) for k, g in groupby(sorted(expr.children, key=lambda c: hash(self.inames[c])),
                                                    lambda c: self.inames[c]))
        if (len(groups) == len(expr.children)) or (len(groups) == 1):
            return super().map_product(expr, **kwargs)
        else:
            groups = sorted(groups, key=lambda g: len(self.inames[g[0]]))
            group_inames = [self.inames[g[0]] for g in groups]
            if not all(a <= b for a, b in zip(group_inames[:-1], group_inames[1:])):
                raise UnknownLoopNesting()
            children = []
            for group in groups:
                if len(group) > 1:
                    children.append(prim.Product(tuple(self.rec(c) for c in group)))
                else:
                    children.append(self.rec(group[0]))
            p = children[0]
            for c in children[1:]:
                p = prim.Product((p, c))
            return p


class DetermineInames(CombineMapper):
    def __init__(self, all_inames, temporary_inames, parent_inames):
        super().__init__()
        self.all_inames = all_inames
        self.result_cache = dict()
        self.temporary_inames = temporary_inames
        self.parent_inames = parent_inames
        self.default_inames = frozenset()

    def rec(self, expr):
        try:
            return self.result_cache[expr]
        except KeyError:
            result = super().rec(expr)
            self.result_cache[expr] = result
            return result

    def __call__(self, expr, *args, default_inames=frozenset(), **kwargs):
        self.default_inames = default_inames
        return self.rec(expr)

    def combine(self, values):
        import operator
        from functools import reduce
        return reduce(operator.or_, values, frozenset())

    def map_constant(self, expr):
        return frozenset()

    def map_variable(self, expr):
        if expr.name in self.all_inames:
            return frozenset({expr.name} | self.parent_inames.get(expr.name, set())) | self.default_inames
        elif expr.name in self.temporary_inames:
            return self.temporary_inames[expr.name] | self.default_inames
        else:
            return self.default_inames

    map_function_symbol = map_constant

    def map_loopy_function_identifier(self, expr):
        return self.default_inames

    map_tagged_variable = map_variable

    def map_foreign(self, expr):
        if isinstance(expr, (set, frozenset)):
            return self.map_list(expr)
        else:
            return super().map_foreign(expr)


class ChildExpressions(WalkMapper):
    def __init__(self, cses, filter):
        self.cses = cses
        self.toplevel_cses = set()
        self.level = 0
        self.filter = filter
        self.result_cache = defaultdict(set)

    def __call__(self, *args, **kwargs):
        self.level = 0
        super().__call__(*args, **kwargs)

    def visit(self, expr, *args, **kwargs):
        if expr in self.cses:
            self.level += 1
            if self.level == 1:
                self.toplevel_cses |= {expr}
        return True

    def post_visit(self, expr, *args, **kwargs):
        if expr in self.cses:
            self.level -= 1
            self.result_cache[expr] |= set()
            children = ()
            if isinstance(expr, (prim.Sum, prim.Product)):
                children = expr.children
            elif isinstance(expr, prim.Call):
                children = expr.parameters
            elif isinstance(expr, prim.QuotientBase):
                children = (expr.numerator, expr.denominator)
            elif isinstance(expr, FusedMultiplyAdd):
                children = (expr.mul_op1, expr.mul_op2, expr.add_op)
            for subexpr in children:
                if subexpr in self.cses and self.filter(expr, subexpr):
                    self.result_cache[expr] |= {subexpr}


class ReplaceMapper(IdentityMapper):
    """
    Creates new variables for the instructions for all terms that occur more
    than once. The new variables are returned, for replacing the original
    ones.
    """
    def __init__(self, replacement_map):
        self.replacement_map = replacement_map

    def rec(self, expr, *args, **kwargs):
        try:
            return self.replacement_map[expr]
        except KeyError:
            return IdentityMapper.rec(self, expr, *args, **kwargs)

    __call__ = rec

    # don't flatten sum or product since this would prohibit expression matching correctly
    def map_sum(self, expr, *args, **kwargs):
        return prim.Sum(tuple(self.rec(child, *args, **kwargs) for child in expr.children))

    def map_product(self, expr, *args, **kwargs):
        return prim.Product(tuple(self.rec(child, *args, **kwargs) for child in expr.children))


def invert_graph(graph):
    inverted = defaultdict(set)
    for node, children in graph.items():
        inverted[node] |= set()
        for c in children:
            inverted[c] |= {node}
    return inverted


def roots(graph):
    return list(node for node in graph if node not in reduce(or_, graph.values()))


def build_cse_graph(cses, insns, inames):
    # build a hierarchy of cses
    child_cse_mapper = ChildExpressions(cses, lambda e, se: True)
    for insn in insns:
        child_cse_mapper(insn.expression)
    contains_cses = child_cse_mapper.result_cache  # the sub expression each cse contains
    within_cses = invert_graph(contains_cses)  # all sub expressions which directly contain a cse
    toplevel_cses = child_cse_mapper.toplevel_cses

    # filter cses, which parents are also in the same loop nest
    # this should leave the c++ compiler with more opportunities to do cse within each loop level
    queue = roots(within_cses)
    filtered_contains = defaultdict(set)
    while queue:
        current = queue.pop()
        filtered_contains[current] |= set()
        keep_cse = current in toplevel_cses or any(inames[child] != inames[current] for child in within_cses[current])
        for child in within_cses[current]:
            queue.insert(0, child)
            if not keep_cse:
                filtered_contains[child] |= filtered_contains[current]
            else:
                filtered_contains[child] |= {current}
        if not keep_cse:
            del filtered_contains[current]
    filtered_within = invert_graph(filtered_contains)

    return filtered_contains, filtered_within


def precompute_cses(kernel, temp_dag, cse_to_temp, cse_ids, inames, apply_recursive=True):
    def find_dependencies(expr):
        dep_mapper = DependencyMapper()
        deps = (get_pymbolic_basename(d) for d in dep_mapper(expr))
        dependency_ids = set()
        writer_map = defaultdict(set, **kernel.writer_map())
        for dep in deps:
            if dep in kernel.temporary_variables:
                dependency_ids |= writer_map[dep]
        return frozenset(dependency_ids)

    new_insns = []
    new_temporaries = dict()
    new_ids = defaultdict(set)
    dependency_map = defaultdict(frozenset)
    replacement_map = {}

    temp_to_cse = dict((v, k) for k, v in cse_to_temp.items())
    inverted_temp_dag = invert_graph(temp_dag)
    queue = roots(inverted_temp_dag)
    visited = set()
    while queue:
        current = queue.pop()
        current_name, current_id = current
        for next_temp in inverted_temp_dag[current]:
            if next_temp not in visited:
                visited |= {next_temp}
                queue.insert(0, next_temp)

        replace = ReplaceMapper(replacement_map)
        orig_expr = temp_to_cse[current]
        new_expr = replace(orig_expr) if apply_recursive else orig_expr

        # check if the temporary needs to be vectorized
        orig_inames = inames[orig_expr]
        try:
            vec_iname = next(iname for iname in orig_inames
                             if iname in kernel.iname_to_tags and
                             any(isinstance(tag, VectorizeTag) for tag in kernel.iname_to_tags[iname]))
            shape = (kernel.get_constant_iname_length(vec_iname),)
            dim_tags = ("vec",)

            replacement_map[orig_expr] = prim.Subscript(prim.Variable(current_name), (prim.Variable(vec_iname),))
        except StopIteration:
            shape = ()
            dim_tags = ()
            replacement_map[orig_expr] = prim.Variable(current_name)

        # Create temporary variable
        new_temporaries[current_name] = lp.TemporaryVariable(current_name, dtype=lp.auto, shape=shape,
                                                             dim_tags=dim_tags, address_space=lp.AddressSpace.PRIVATE)

        predicates = frozenset()
        for insn_id in cse_ids[orig_expr]:
            new_ids[insn_id] |= {current_id}
            insn_predicates = kernel.id_to_insn[insn_id].predicates
            if insn_predicates:
                predicates = predicates | frozenset([insn_predicates])
        if len(predicates) > 1:
            predicates = frozenset({prim.LogicalOr(tuple(prim.LogicalAnd(tuple(p for p in subpredicates))
                                                         for subpredicates in predicates))})
        elif len(predicates) == 1:
            predicates, = predicates

        tagsets = tuple(kernel.id_to_insn[insn_id].tags for insn_id in cse_ids[orig_expr])
        alltags = reduce(frozenset.union, tagsets, frozenset())
        csetags = reduce(frozenset.intersection, tagsets, alltags)

        dependencies = find_dependencies(new_expr)
        for _, child_id in temp_dag[current]:
            dependencies = dependencies | frozenset({child_id})
        for p in predicates:
            dependencies = dependencies | find_dependencies(p)
        dependency_map[current_id] = dependencies
        new_insns.append(lp.Assignment(replacement_map[orig_expr], new_expr,
                                       within_inames=orig_inames, id=current_id,
                                       depends_on=dependencies, predicates=predicates,
                                       boostable=False, boostable_into=frozenset(),
                                       tags=csetags))

    return new_insns, new_ids, new_temporaries, replacement_map, dependency_map


def build_precompute_graph(kernel, contains_cses):
    name_generator = kernel.get_var_name_generator()

    cse_to_temporary = dict((cse, name_generator("temp")) for cse in contains_cses)
    cse_to_temporary = dict((cse, (name, "precompute_{}".format(name))) for cse, name in cse_to_temporary.items())

    # replace the nodes of contains_cses with a name for the temporary and an id for the new instruction
    temp_dag = dict()
    for node, children in contains_cses.items():
        temp = cse_to_temporary[node]
        temp_dag[temp] = set()
        for child in children:
            temp_dag[temp] |= {cse_to_temporary[child]}

    return temp_dag, cse_to_temporary


def insert(a: list, b: list, idx: list):
    """
    Insert the list b into a, such that an element b[i] is inserted at the index idx[i] if no other elements of
    b were inserted.
    """
    assert len(b) == len(idx)
    result = []
    i = 0
    popcount = 0

    a = list(reversed(a))
    b = list(reversed(b))
    idx = list(reversed(idx))

    while a or b:
        if b and i == idx[-1] + popcount:
            new = b.pop()
            idx.pop()
            popcount = popcount + 1
        else:
            new = a.pop()
        result.append(new)
        i = i + 1
    return result


def index_inames(kernel, insn):
    inames = frozenset()
    if isinstance(insn, (lp.Assignment, lp.CallInstruction, lp.CInstruction)):
        for assignee in insn.assignees:
            if isinstance(assignee, prim.Subscript):
                deps = lp.symbolic.DependencyMapper(composite_leaves=False)(assignee.index_tuple)
                inames = inames | frozenset(v.name for v in deps if v.name in kernel.all_inames())
    return inames


def to_dot(graph_dict):
    from graphviz import Digraph
    g = Digraph("G")
    for node, children in graph_dict.items():
        g.node(str(node))
        children = [children] if isinstance(children, str) else children
        for child in children:
            g.edge(str(node), str(child))
    return g


def build_schedule(kernel, dependency_dag, temp_inames):
    precompute_ids = set(dependency_dag.keys())

    schedule_idx = OrderedDict()
    active_inames = set()
    inames_at_idx = []
    for i, s in enumerate(kernel.schedule):
        inames_at_idx.append(active_inames.copy())
        if isinstance(s, lp.schedule.EnterLoop):
            active_inames |= {s.iname}
        elif isinstance(s, lp.schedule.LeaveLoop):
            active_inames.remove(s.iname)
        elif isinstance(s, lp.schedule.RunInstruction):
            schedule_idx[s.insn_id] = i

    def advance_to_iname_nest(start_idx, inames):
        while inames_at_idx[start_idx] != inames:
            start_idx += 1
        return start_idx

    inverted_dependency_dag = invert_graph(dependency_dag)
    queue = roots(invert_graph(dependency_dag))
    scheduled = set()
    while queue:
        current = queue.pop()
        scheduled |= {current}
        if current not in schedule_idx:
            # The new instruction should be scheduled either immediately after the last existing instruction
            # or new precomputation it depends on. By using an ordered dict, it is ensured that if the last instruction
            # it depends on is a new precomputation it gets inserted immediately after in the new schedule.
            # Additionally the new precomputation must be scheduled inside the correct loop nest, which is done in
            # `advance_to_iname_set`.
            schedule_idx[current] = advance_to_iname_nest(
                max(list(schedule_idx[dep] if dep in precompute_ids else schedule_idx[dep] + 1
                         for dep in dependency_dag[current]) or [1]),
                temp_inames[current])
        for child in inverted_dependency_dag[current]:
            # only add node to the queue if the instructions it depends on have been scheduled
            if dependency_dag[child] - scheduled == set():
                queue.insert(0, child)

    items_list = sorted([lp.schedule.RunInstruction(insn_id=id) for id in schedule_idx if id in precompute_ids],
                        key=lambda x: schedule_idx[x.insn_id])
    idx_list = sorted([idx for id, idx in schedule_idx.items() if id in precompute_ids])
    new_schedule = insert(kernel.schedule, items_list, idx_list)
    return new_schedule


def add_cse_to_kernel(kernel, keep_insn, cse_insn, precompute_insn, cse_temporaries, cse_ids, new_schedule,
                      replacement_map):
    replace = ReplaceMapper(replacement_map)

    insns = [insn.with_transformed_expressions(replace).copy(depends_on=insn.depends_on | frozenset(cse_ids[insn.id]))
             for insn in cse_insn]

    return kernel.copy(instructions=keep_insn + insns + precompute_insn,
                       temporary_variables=dict(**kernel.temporary_variables, **cse_temporaries),
                       schedule=new_schedule)


def simple_cse(kernel, keep_insns, cse_insns):
    """
    This is the fallback cse algorithm implementations. cses are only found if they appear multiple times
    within exactly one loop nest.
    """
    # count the number of occurrence of an subexpression
    count_occurrence = CountTerms(defaultdict(frozenset), lambda _: 1)
    for insn in cse_insns:
        count_occurrence(insn.expression, insn.id, frozenset())

    # returns the terms in the map that occur more than one time
    cses = set(e for e, n in count_occurrence.cache.items() if n > 1)

    if cses:
        # gather cses which do not appear within other cses
        child_cse_mapper = ChildExpressions(cses, lambda e, se: True)
        for insn in cse_insns:
            child_cse_mapper(insn.expression)

        cses = set()
        inames = dict()
        # only consider cse which appear in exactly one loop nest
        for cse in child_cse_mapper.toplevel_cses:
            cse_inames = set(kernel.id_to_insn[insn_id].within_inames for insn_id in count_occurrence.ids[cse])
            if len(cse_inames) == 1:
                inames[cse], = cse_inames
                cses |= {cse}

        if cses:
            filtered_contains = dict((e, set()) for e in cses)

            temp_dag, cse_to_temp = build_precompute_graph(kernel, filtered_contains)

            new_insns, new_ids, new_temporaries, replacement_map, dependency_map = \
                precompute_cses(kernel, temp_dag, cse_to_temp, count_occurrence.ids, inames, apply_recursive=False)

            kernel = add_cse_to_kernel(kernel, keep_insns, cse_insns, new_insns, new_temporaries, new_ids,
                                       kernel.schedule, replacement_map)

            kernel = lp.infer_unknown_types(kernel)

    return kernel


def licm_cse(kernel, keep_insns, cse_insns):
    """
    This implements cse with loop-invariant code motion. First, for each expression a minimal iname
    set is constructed. Since at this point the kernel has no loop ordering, a specific loop ordering is assumed,
    namely the outermost iname is "q". In the blockstructured case additional orderings are assumed.
    Then, sums and products are split into sums or products with the same minimal iname set.
    If during this step a sum or product contains terms with non nested minimal iname sets an exception is thrown
    and the fallback cse algorithm is used instead. The expressions are counted wrt to the size of the domain of
    instruction inames without the minimal inames.
    """
    @memoize
    def estimate_domain_size(inames):
        if len(inames) == 0:
            return 1
        else:
            domain = kernel.get_inames_domain(inames)
            # set parameterized bounds to 2 (bound is assumed to be upper bound)
            for name, (t, p) in domain.get_var_dict().items():
                if t == 1:  # t == isl.dim_type.param
                    domain = domain.fix_val(t, p, 2)
            # if the domain contains other inames, remove them first
            while inames != set(v for v, (t, _) in domain.get_var_dict().items() if t == 3):
                name, (t, p) = next(filter(lambda item: item[0] not in inames, domain.get_var_dict().items()))
                domain = domain.remove_dims(t, p, 1)
            return domain.count_val().to_python()

    kernel = lp.get_one_scheduled_kernel(lp.preprocess_kernel(kernel))

    # for each temporary variable, find the iname set in which it gets initialized.
    # these inames, without possible indexing inames for the temporary, are added
    # to the iname set of each expression containing the temporary.
    temporary_inames = defaultdict(frozenset)
    for temporary in kernel.temporary_variables:
        if temporary in kernel.writer_map():
            for insn_id in kernel.writer_map()[temporary]:
                insns = kernel.id_to_insn[insn_id]
                inames = frozenset(insns.within_inames - index_inames(kernel, insns))
                # if there are multiple inames where a temporary gets written, use all inames
                temporary_inames[temporary] = temporary_inames[temporary] | inames

    schedule = kernel.schedule
    active_inames = set()
    parent_inames = defaultdict(frozenset)
    for item in schedule:
        if isinstance(item, lp.schedule.EnterLoop):
            parent_inames[item.iname] = parent_inames[item.iname] | active_inames
            active_inames |= {item.iname}
        elif isinstance(item, lp.schedule.LeaveLoop):
            assert item.iname in active_inames
            active_inames.remove(item.iname)

    # cache the minimal iname set for each sub expression
    predicate_inames_mapper = DetermineInames(kernel.all_inames(), temporary_inames, parent_inames)
    for insn in cse_insns:
        predicate_inames_mapper(insn.predicates)
    predicate_inames = predicate_inames_mapper.result_cache

    inames_mapper = DetermineInames(kernel.all_inames(), temporary_inames, parent_inames)
    for insn in cse_insns:
        inames_mapper(insn.expression, default_inames=predicate_inames[insn.predicates])
    inames = inames_mapper.result_cache

    try:
        # split sums and products into groups of sums/products with the same iname set
        split = SplitByIname(inames)
        for insn in cse_insns:
            insn.expression = split(insn.expression)
    except UnknownLoopNesting:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning("licm_cse: licm could not nest subexpressions properly, using simple cse instead.")
        return simple_cse(kernel, keep_insns, cse_insns)

    # splitting may have changed expressions, so redo iname set caching
    for insn in cse_insns:
        inames_mapper(insn.expression)
    inames = inames_mapper.result_cache

    # count the number of occurrence of an subexpression wrt to the iname set of the current instruction
    count_occurrence = CountTerms(inames, estimate_domain_size)
    for insn in cse_insns:
        count_occurrence(insn.expression, insn.id, insn.within_inames)

    # returns the terms in the map that occur more than one time
    cses = set(e for e, n in count_occurrence.cache.items() if n > 1)
    if cses:
        filtered_contains, filtered_within = build_cse_graph(cses, cse_insns, inames)

        temp_dag, cse_to_temp = build_precompute_graph(kernel, filtered_contains)

        temp_inames = dict((v[1], inames[k]) for k, v in cse_to_temp.items())

        new_insns, new_ids, new_temporaries, replacement_map, dependency_dag =\
            precompute_cses(kernel, temp_dag, cse_to_temp, count_occurrence.ids, inames)

        new_schedule = build_schedule(kernel, dependency_dag, temp_inames)

        new_kernel = add_cse_to_kernel(kernel, keep_insns, cse_insns, new_insns, new_temporaries, new_ids,
                                       new_schedule, replacement_map)

        if lp.has_schedulable_iname_nesting(new_kernel):
            kernel = lp.infer_unknown_types(new_kernel)
        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("licm_cse: licm did not produce a schedulable kernel, using simple cse instead.")
            kernel = simple_cse(kernel, keep_insns, cse_insns)

    return kernel


def cse(kernel):
    """
    The function finds all terms in a kernel and replaces them with simple
    placeholders. First the mapper function counts all the terms and saves them
    in a map. After that the new instruction will be created and a copy of the
    kernel is returned.
    """
    if not kernel:
        return kernel

    insns_with_cse_possible = []
    insns_without_cse_possible = []
    for insn in kernel.instructions:
        if isinstance(insn, (lp.Assignment, lp.CallInstruction)):
            insns_with_cse_possible.append(insn)
        else:
            insns_without_cse_possible.append(insn)

    if get_form_option("apply_cse") == "licm":
        return licm_cse(kernel, insns_without_cse_possible, insns_with_cse_possible)
    elif get_form_option("apply_cse") == "simple":
        return simple_cse(kernel, insns_without_cse_possible, insns_with_cse_possible)
    else:
        return kernel
