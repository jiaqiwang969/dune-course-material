""" Registering finite elements that we have, but FEniCS does not """

from ufl import register_element, L2


register_element("Discontinuous Gauss-Lobatto-Legendre",
                 "DGLL",
                 0,
                 L2,
                 "identity",
                 (0, None),
                 ('interval',),
                 )


register_element("Monomials",
                 "Monom",
                 0,
                 L2,
                 "identity",
                 (0, None),
                 ('interval',),
                 )


register_element("L2-Orthonormal Polynomials",
                 "OPB",
                 0,
                 L2,
                 "identity",
                 (0, None),
                 ('interval',),
                 )


register_element("Rannacher-Turek",
                 "RaTu",
                 0,
                 L2,
                 "identity",
                 (1, 1),
                 ('quadrilateral', 'hexahedron'),
                 )
