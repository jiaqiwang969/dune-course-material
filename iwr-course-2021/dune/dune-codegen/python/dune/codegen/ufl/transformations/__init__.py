"""Infrastructure for printing trees of UFL expressions."""


class UFLTransformationWrapper(object):
    def __init__(self, func, **kwargs):
        # Store the decorated function
        self.func = func
        self.counter = 0

        # Extract the name of the transformation from the given kwargs
        assert "name" in kwargs
        self.name = kwargs.pop("name")
        self.printBefore = kwargs.pop("printBefore", True)
        self.extractExpressionListFromResult = kwargs.pop("extraction_lambda", lambda e: [e])

    def write_trafo(self, expr, before):
        # Skip this if we explicitly disabled it
        if before and not self.printBefore:
            return

        # Write out a dot file
        from dune.codegen.options import get_form_option
        if get_form_option("print_transformations"):
            import os
            dir = get_form_option("print_transformations_dir")

            for i, exprtowrite in enumerate(expr):
                filename = "trafo_{}_{}_{}{}.dot".format(self.name, str(self.counter).zfill(4), "in" if before else "out", "_{}".format(i) if len(expr) > 1 else "")
                filename = os.path.join(dir, filename)
                with open(filename, 'w') as out:
                    from ufl.formatting.ufl2dot import ufl2dot
                    out.write(str(ufl2dot(exprtowrite)[0]))

            if not before:
                self.counter = self.counter + 1

    def __call__(self, expr, *args, **kwargs):
        # We assume that the first argument to any transformation is the expression
        from ufl.classes import Expr
        assert isinstance(expr, Expr)

        # Maybe output the input expression!
        self.write_trafo([expr], True)

        # Call the original function
        ret = self.func(expr, *args, **kwargs)

        # We do also assume that the transformation returns an ufl expression or a list there of
        ret_for_print = self.extractExpressionListFromResult(ret)
        assert isinstance(ret_for_print, list) and all(isinstance(e, Expr) for e in ret_for_print)

        # Maybe output the returned expression
        self.write_trafo(ret_for_print, False)

        # return the result
        return ret


def ufl_transformation(_positional_arg=None, **kwargs):
    """ A decorator for ufl transformations. It allows us to output the
    result if needed. """
    assert not _positional_arg
    return lambda f: UFLTransformationWrapper(f, **kwargs)


@ufl_transformation(name="print", printBefore=False)
def print_expression(e):
    return e


def transform_integral(integral, trafo):
    from ufl import Integral
    assert isinstance(integral, Integral)
    assert isinstance(trafo, UFLTransformationWrapper)

    return integral.reconstruct(integrand=trafo(integral.integrand()))


def transform_form(form, trafo):
    from ufl import Form
    assert isinstance(form, Form)
    assert isinstance(trafo, UFLTransformationWrapper)

    return Form([transform_integral(i, trafo) for i in form.integrals()])
