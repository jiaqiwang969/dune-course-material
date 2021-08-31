""" Preprocessing algorithms for UFL forms """

from dune.codegen.generation import run_hook, ReturnArg
import ufl.classes as uc
import ufl.algorithms.apply_function_pullbacks as afp
import ufl.algorithms.apply_algebra_lowering as aal
import ufl.algorithms.apply_derivatives as ad

from dune.codegen.options import get_form_option

from pytools import memoize


class FunctionPullbackApplier(afp.FunctionPullbackApplier):
    def argument(self, o):
        return afp.apply_single_function_pullbacks(o)

    def coefficient(self, o):
        if o.count() == 2:
            # In the case of count() == 2 this coefficient represents the time
            return o
        else:
            # Note: This monkey patch was done when we still needed to avoid
            # doing function pullbacks for coefficients with count()>2. This
            # whole path could be deleted.
            return afp.apply_single_function_pullbacks(o)


# Monkey patch the pullback applier from UFL
afp.FunctionPullbackApplier = FunctionPullbackApplier


@memoize
def preprocess_form(form):
    from ufl.algorithms import compute_form_data
    formdata = compute_form_data(form,
                                 do_apply_function_pullbacks=True,
                                 do_apply_geometry_lowering=True,
                                 do_apply_integral_scaling=True,
                                 preserve_geometry_types=(uc.CellVolume,
                                                          uc.FacetArea,
                                                          uc.FacetJacobianDeterminant,
                                                          uc.FacetNormal,
                                                          uc.JacobianDeterminant,
                                                          uc.JacobianInverse,
                                                          ),
                                 do_estimate_degrees=not get_form_option("quadrature_order"),
                                 )

    formdata.preprocessed_form = apply_default_transformations(formdata.preprocessed_form)

    # Run preprocessing from custom user code
    formdata.preprocessed_form = run_hook(name="preprocess",
                                          args=(ReturnArg(formdata.preprocessed_form),))

    return formdata


def apply_default_transformations(form):
    #
    # This is the list of transformations we unconditionally apply to
    # all forms we want to generate code for.
    #
    from dune.codegen.ufl.transformations import transform_form
    from dune.codegen.ufl.transformations.indexpushdown import pushdown_indexed

    form = transform_form(form, pushdown_indexed)

    return form


# Monkey patch UFL, such that we invert matrices in C++ instead of Python.
# The latter only works for very small matrices. If this causes a problem at
# some point, we should guard this monkey patch with an option.

aal.LowerCompoundAlgebra.inverse = lambda s, o, A: s.reuse_if_untouched(o, A)
ad.GenericDerivativeRuleset.inverse = lambda s, o, A: -uc.Dot(uc.Dot(o, A), o)
