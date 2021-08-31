from dune.codegen.ufl.modified_terminals import Restriction


def restricted_name(name, restriction):
    """Adapt name according to the restictrion

    Some remarks:

    - UFL defines the jump the following: jump(v) = v('+') - v('-').

    - The corresponding outer normal vector is n =
      FacetNormal(cell)('+'). The user needs to make the right choice
      in the UFL file.

    - In the literature this convention is sometimes swapped. In order
      to be consistent with UFL we choose ('+') as self and ('-') as
      neighbor and choose the outer unit normal vector accordingly.

    """
    if restriction == Restriction.NONE:
        return name
    if restriction == Restriction.POSITIVE:
        return name + '_s'
    if restriction == Restriction.NEGATIVE:
        return name + '_n'
