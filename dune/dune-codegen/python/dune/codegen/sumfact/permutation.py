""" Permute sum factorization kernels """

import itertools

from dune.codegen.options import get_option
from dune.codegen.sumfact.tabulation import quadrature_points_per_direction
from dune.codegen.ufl.modified_terminals import Restriction


def sumfact_permutation_heuristic(permutations, stage):
    """Heuristic to choose a permutation

    - Stage 1: Pick the permutation where in permutations[1:] most
      elements are ordered by size
    - Stage 3: Pick the permutation where in permutations[:-1] most
      elements are ordered by size
    """
    def cost(perm, stage):
        cost = 0
        for i in range(0, len(perm) - 2):
            if stage == 1:
                if perm[i + 1] > perm[i + 2]:
                    cost += 1
            if stage == 3:
                if perm[0] > perm[i + 1]:
                    cost += 1
        return cost

    perm = min(permutations, key=lambda i: cost(i, stage))
    return perm


def flop_cost(matrix_sequence):
    """Computational cost of sumfactorization with this matrix_sequence
    """
    cost = 0
    for l in range(len(matrix_sequence)):
        cost_m = 1
        cost_n = 1
        for i in range(l + 1):
            cost_m *= matrix_sequence[i].rows
        for i in range(l, len(matrix_sequence)):
            cost_n *= matrix_sequence[i].cols
        cost += cost_m * cost_n
    # The factor of 2 indicates FMA
    return 2 * cost


def sumfact_cost_permutation_strategy(matrix_sequence, stage):
    """Choose permutation of the matrix sequence based on computational cost

    Note: If there are multiple permutations with the same cost a
    heuristic is used to pick one.
    """
    # Combine permutation and matrix_sequence
    perm = [i for i, _ in enumerate(matrix_sequence)]
    perm_matrix_sequence = zip(perm, matrix_sequence)

    # Find cost for all possible permutations of the matrix_sequence
    perm_cost = []
    for permutation in itertools.permutations(perm_matrix_sequence):
        perm, series = zip(*permutation)
        cost = flop_cost(series)
        perm_cost.append((perm, cost))

    # Find minimal cost and all permutations with that cost
    _, costs = zip(*perm_cost)
    minimal_cost = min(costs)
    minimal_cost_permutations = [p[0] for p in perm_cost if p[1] == minimal_cost]

    # Use heuristic to pick one of the minimal cost permutations
    perm = sumfact_permutation_heuristic(minimal_cost_permutations, stage)
    return perm


def permute_forward(t, perm):
    """Forward permute t according to perm (not inplace)

    Example:
    t = ('a', 'b', 'c')
    perm = (1, 2, 0)
    -> ('b', 'c', 'a')
    """
    tmp = []
    for pos in perm:
        tmp.append(t[pos])
    return tuple(tmp)


def permute_backward(t, perm):
    """Backward permute t according to perm (not inplace)

    Inverse of permute_forward(t, perm).

    Example:
    t = ('a', 'b', 'c')
    perm = (1, 2, 0)
    -> ('c', 'a', 'b')
    """
    tmp = [None] * len(t)
    for i, pos in enumerate(perm):
        tmp[pos] = t[i]
    return tuple(tmp)


def sumfact_quadrature_permutation_strategy(dim, restriction):
    """Return order of direction for the quadrature points for stage 2

    On intersection we need to make sure to go through the quadrature points of
    self and neighbor in the same order. We do this by making the grid edge
    consistent and complying to a convention of the directions depending on the
    dimension, restriction, facedir and facemod.

    In order to derive those conventions you need to draw the cells with edge
    orientation and see how to match the intersections.
    """
    # Use a simpler convention for structured grids. In this case we can always
    # go through the directions in the normal order. The same is true for 2D
    # and sum factorization on volumes.
    if (not get_option('grid_unstructured')) or dim == 2 or restriction == Restriction.NONE:
        return tuple(range(dim))
    else:
        # Draw a cube with edge orientations. We always do the normal direction
        # first. The first case for facedir=0, facemod=0 was chosen that way,
        # all others can be derived by rotating the cube and matching edge
        # directions.
        def _order_on_self(restriction):
            from dune.codegen.sumfact.accumulation import SumfactAccumulationMixin
            facedir = SumfactAccumulationMixin.get_facedir(None, restriction)
            facemod = SumfactAccumulationMixin.get_facemod(None, restriction)

            quadrature_order = {
                (0, 0): (0, 1, 2),
                (0, 1): (0, 2, 1),
                (1, 0): (1, 2, 0),
                (1, 1): (1, 0, 2),
                (2, 0): (2, 0, 1),
                (2, 1): (2, 1, 0),
            }

            return quadrature_order[(facedir, facemod)]

        # On neighbor we also do the normal direction first. The other two can
        # be derived by putting a second edge oriented cube besides the first
        # one. Then rotate and match edge directions.
        if restriction == Restriction.POSITIVE:
            return _order_on_self(restriction)
        else:
            # Still do normal direction first. The other two directions need to
            # be done in reverse order to go through the quadrature points in
            # the same order as on self (draw cubes!).
            assert restriction == Restriction.NEGATIVE
            l = list(_order_on_self(restriction))
            return (l[0], l[2], l[1])
