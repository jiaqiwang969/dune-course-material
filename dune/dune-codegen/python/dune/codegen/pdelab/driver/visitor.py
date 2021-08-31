from dune.codegen.generation import global_context, preamble
from dune.codegen.ufl.visitor import UFL2LoopyVisitor

import pymbolic.primitives as prim


@preamble(section="gridoperator", kernel="driver_block")
def set_lop_to_starting_time():
    from dune.codegen.pdelab.driver import get_form_ident
    from dune.codegen.pdelab.driver.gridoperator import name_localoperator
    lop = name_localoperator(get_form_ident())
    return "{}->setTime(0.0);".format(lop)


class DriverUFL2PymbolicVisitor(UFL2LoopyVisitor):
    def __init__(self):
        UFL2LoopyVisitor.__init__(self, "exterior_facet", {})

    def __call__(self, expr):
        self.preambles = []
        ret = self._call(expr, False)
        return set(self.preambles), ret

    def facet_normal(self, o):
        self.preambles.append("auto n=is.unitOuterNormal(xl);")
        return prim.Variable("n")

    def spatial_coordinate(self, o):
        self.preambles.append("auto x=is.geometry().global(xl);")
        return prim.Variable("x")

    def max_value(self, o):
        self.preambles.append("using std::max;")
        return UFL2LoopyVisitor.max_value(self, o)

    def min_value(self, o):
        self.preambles.append("using std::min;")
        return UFL2LoopyVisitor.min_value(self, o)

    def coefficient(self, o):
        if o.count() == 2:
            from dune.codegen.pdelab.driver import get_form_ident
            from dune.codegen.pdelab.driver.gridoperator import name_localoperator
            lop = name_localoperator(get_form_ident())
            set_lop_to_starting_time()
            return prim.Call(prim.Variable("{}->getTime".format(lop)), ())
        else:
            return UFL2LoopyVisitor.coefficient(self, o)


def ufl_to_code(expr, boundary=True):
    # So far, we only considered this code branch on boundaries!
    assert boundary
    from dune.codegen.pdelab.driver import get_form_ident
    with global_context(integral_type="exterior_facet", form_identifier=get_form_ident()):
        visitor = DriverUFL2PymbolicVisitor()
        from pymbolic.mapper.c_code import CCodeMapper
        ccm = CCodeMapper()
        preambles, vis_expr = visitor(expr)
        return "{} return {};".format("".join(preambles), ccm(vis_expr))
