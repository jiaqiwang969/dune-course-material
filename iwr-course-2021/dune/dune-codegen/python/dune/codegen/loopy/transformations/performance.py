from dune.codegen.options import get_form_option
from dune.codegen.sumfact.transformations import sumfact_performance_transformations


def performance_transformations(kernel, signature):
    if get_form_option("sumfact"):
        kernel = sumfact_performance_transformations(kernel, signature)
    return kernel
