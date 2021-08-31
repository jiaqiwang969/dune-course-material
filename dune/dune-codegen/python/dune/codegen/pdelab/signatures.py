""" Signatures for PDELab local opreator assembly functions """
from dune.codegen.generation import get_global_context_value
from dune.codegen.ufl.modified_terminals import Restriction
from dune.codegen.pdelab.geometry import (name_geometry_wrapper,
                                          type_geometry_wrapper,
                                          )
from dune.codegen.pdelab.argument import (name_accumulation_variable,
                                          type_accumulation_variable,
                                          name_coefficientcontainer,
                                          type_coefficientcontainer,
                                          name_applycontainer,
                                          type_linearizationpointcontainer,
                                          )
from dune.codegen.pdelab.spaces import (name_testfunctionspace,
                                        type_testfunctionspace,
                                        name_trialfunctionspace,
                                        type_trialfunctionspace,
                                        )


def ufl_measure_to_pdelab_measure(which):
    return {'cell': 'Volume',
            'exterior_facet': 'Boundary',
            'interior_facet': 'Skeleton',
            }.get(which)


def assembler_routine_name():
    from dune.codegen.generation import get_global_context_value
    integral_type = get_global_context_value("integral_type")
    form_type = get_global_context_value("form_type")

    part1 = {"residual": "alpha"}.get(form_type, form_type)
    part2 = ufl_measure_to_pdelab_measure(integral_type).lower()

    return "{}_{}".format(part1, part2)


def kernel_name():
    arn = assembler_routine_name()
    facedir_s = get_global_context_value("facedir_s", None)
    facedir_n = get_global_context_value("facedir_n", None)
    facemod_s = get_global_context_value("facemod_s", None)
    facemod_n = get_global_context_value("facemod_n", None)
    suffix = "{}{}{}{}".format("_facedirs{}".format(facedir_s) if facedir_s is not None else "",
                               "_facedirn{}".format(facedir_n) if facedir_n is not None else "",
                               "_facemods{}".format(facemod_s) if facemod_s is not None else "",
                               "_facemodn{}".format(facemod_n) if facemod_n is not None else "",
                               )

    return "{}{}".format(arn, suffix)


def assembly_routine_signature():
    integral_type = get_global_context_value("integral_type")
    form_type = get_global_context_value("form_type")

    templates, args = {('residual', 'cell'): (alpha_volume_templates, alpha_volume_args),
                       ('residual', 'exterior_facet'): (alpha_boundary_templates, alpha_boundary_args),
                       ('residual', 'interior_facet'): (alpha_skeleton_templates, alpha_skeleton_args),
                       ('jacobian', 'cell'): (jacobian_volume_templates, jacobian_volume_args),
                       ('jacobian', 'exterior_facet'): (jacobian_boundary_templates, jacobian_boundary_args),
                       ('jacobian', 'interior_facet'): (jacobian_skeleton_templates, jacobian_skeleton_args),
                       }.get((form_type, integral_type), (None, None))

    if templates is None:
        # Check if form is linear
        from dune.codegen.pdelab.driver import is_linear
        linear = is_linear()

        templates, args = {('jacobian_apply', 'cell', True): (jacobian_apply_volume_templates, jacobian_apply_volume_args),
                           ('jacobian_apply', 'exterior_facet', True): (jacobian_apply_boundary_templates, jacobian_apply_boundary_args),
                           ('jacobian_apply', 'interior_facet', True): (jacobian_apply_skeleton_templates, jacobian_apply_skeleton_args),
                           ('jacobian_apply', 'cell', False): (nonlinear_jacobian_apply_volume_templates, nonlinear_jacobian_apply_volume_args),
                           ('jacobian_apply', 'exterior_facet', False): (nonlinear_jacobian_apply_boundary_templates, nonlinear_jacobian_apply_boundary_args),
                           ('jacobian_apply', 'interior_facet', False): (nonlinear_jacobian_apply_skeleton_templates, nonlinear_jacobian_apply_skeleton_args),
                           }.get((form_type, integral_type, linear), None)

    return construct_signature(templates(), args(), kernel_name())


def assembly_routine_args():
    integral_type = get_global_context_value("integral_type")
    form_type = get_global_context_value("form_type")

    args = {('residual', 'cell'): alpha_volume_args,
            ('residual', 'exterior_facet'): alpha_boundary_args,
            ('residual', 'interior_facet'): alpha_skeleton_args,
            ('jacobian', 'cell'): jacobian_volume_args,
            ('jacobian', 'exterior_facet'): jacobian_boundary_args,
            ('jacobian', 'interior_facet'): jacobian_skeleton_args,
            }.get((form_type, integral_type), None)

    if args is None:
        # Check if form is linear
        from dune.codegen.pdelab.driver import is_linear
        linear = is_linear()

        args = {('jacobian_apply', 'cell', True): jacobian_apply_volume_args,
                ('jacobian_apply', 'exterior_facet', True): jacobian_apply_boundary_args,
                ('jacobian_apply', 'interior_facet', True): jacobian_apply_skeleton_args,
                ('jacobian_apply', 'cell', False): nonlinear_jacobian_apply_volume_args,
                ('jacobian_apply', 'exterior_facet', False): nonlinear_jacobian_apply_boundary_args,
                ('jacobian_apply', 'interior_facet', False): nonlinear_jacobian_apply_skeleton_args,
                }.get((form_type, integral_type, linear), None)

    return args()


def construct_signature(types, args, name):
    templates = "template<{}>".format(", ".join("typename {}".format(t) for t in set(types)))
    func = "void {}({}) const".format(name, ", ".join("{}{}& {}".format("const " if c else "", t, a) for t, (c, a) in zip(types, args)))
    return [templates, func]


def alpha_volume_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, avt)


def alpha_volume_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.NONE)
    lfsv = name_testfunctionspace(Restriction.NONE)
    cc = name_coefficientcontainer(Restriction.NONE)
    av = name_accumulation_variable((Restriction.NONE,))
    return ((True, geo), (True, lfsu), (True, cc), (True, lfsv), (False, av))


def alpha_boundary_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, avt)


def alpha_boundary_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.POSITIVE)
    lfsv = name_testfunctionspace(Restriction.POSITIVE)
    cc = name_coefficientcontainer(Restriction.POSITIVE)
    av = name_accumulation_variable((Restriction.POSITIVE,))
    return ((True, geo), (True, lfsu), (True, cc), (True, lfsv), (False, av))


def alpha_skeleton_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, lfsut, cct, lfsvt, avt, avt)


def alpha_skeleton_args():
    geo = name_geometry_wrapper()
    lfsu_s = name_trialfunctionspace(Restriction.POSITIVE)
    lfsu_n = name_trialfunctionspace(Restriction.NEGATIVE)
    lfsv_s = name_testfunctionspace(Restriction.POSITIVE)
    lfsv_n = name_testfunctionspace(Restriction.NEGATIVE)
    cc_s = name_coefficientcontainer(Restriction.POSITIVE)
    cc_n = name_coefficientcontainer(Restriction.NEGATIVE)
    av_s = name_accumulation_variable((Restriction.POSITIVE,))
    av_n = name_accumulation_variable((Restriction.NEGATIVE,))
    return ((True, geo), (True, lfsu_s), (True, cc_s), (True, lfsv_s), (True, lfsu_n), (True, cc_n), (True, lfsv_n), (False, av_s), (False, av_n))


def jacobian_volume_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, avt)


def jacobian_volume_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.NONE)
    lfsv = name_testfunctionspace(Restriction.NONE)
    cc = name_coefficientcontainer(Restriction.NONE)
    av = name_accumulation_variable((Restriction.NONE, Restriction.NONE))
    return ((True, geo), (True, lfsu), (True, cc), (True, lfsv), (False, av))


def jacobian_boundary_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, avt)


def jacobian_boundary_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.POSITIVE)
    lfsv = name_testfunctionspace(Restriction.POSITIVE)
    cc = name_coefficientcontainer(Restriction.POSITIVE)
    av = name_accumulation_variable((Restriction.POSITIVE, Restriction.POSITIVE))
    return ((True, geo), (True, lfsu), (True, cc), (True, lfsv), (False, av))


def jacobian_skeleton_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, lfsut, cct, lfsvt, avt, avt, avt, avt)


def jacobian_skeleton_args():
    geo = name_geometry_wrapper()
    lfsu_s = name_trialfunctionspace(Restriction.POSITIVE)
    lfsu_n = name_trialfunctionspace(Restriction.NEGATIVE)
    lfsv_s = name_testfunctionspace(Restriction.POSITIVE)
    lfsv_n = name_testfunctionspace(Restriction.NEGATIVE)
    cc_s = name_coefficientcontainer(Restriction.POSITIVE)
    cc_n = name_coefficientcontainer(Restriction.NEGATIVE)
    av_ss = name_accumulation_variable((Restriction.POSITIVE, Restriction.POSITIVE))
    av_sn = name_accumulation_variable((Restriction.POSITIVE, Restriction.NEGATIVE))
    av_ns = name_accumulation_variable((Restriction.NEGATIVE, Restriction.POSITIVE))
    av_nn = name_accumulation_variable((Restriction.NEGATIVE, Restriction.NEGATIVE))
    return ((True, geo), (True, lfsu_s), (True, cc_s), (True, lfsv_s), (True, lfsu_n), (True, cc_n), (True, lfsv_n), (False, av_ss), (False, av_sn), (False, av_ns), (False, av_nn))


def jacobian_apply_volume_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, avt)


def jacobian_apply_volume_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.NONE)
    lfsv = name_testfunctionspace(Restriction.NONE)
    ac = name_applycontainer(Restriction.NONE)
    av = name_accumulation_variable((Restriction.NONE,))
    return ((True, geo), (True, lfsu), (True, ac), (True, lfsv), (False, av))


def jacobian_apply_boundary_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, avt)


def jacobian_apply_boundary_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.POSITIVE)
    lfsv = name_testfunctionspace(Restriction.POSITIVE)
    ac = name_applycontainer(Restriction.POSITIVE)
    av = name_accumulation_variable((Restriction.POSITIVE,))
    return ((True, geo), (True, lfsu), (True, ac), (True, lfsv), (False, av))


def jacobian_apply_skeleton_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lfsvt, lfsut, cct, lfsvt, avt, avt)


def jacobian_apply_skeleton_args():
    geo = name_geometry_wrapper()
    lfsu_s = name_trialfunctionspace(Restriction.POSITIVE)
    lfsu_n = name_trialfunctionspace(Restriction.NEGATIVE)
    lfsv_s = name_testfunctionspace(Restriction.POSITIVE)
    lfsv_n = name_testfunctionspace(Restriction.NEGATIVE)
    ac_s = name_applycontainer(Restriction.POSITIVE)
    ac_n = name_applycontainer(Restriction.NEGATIVE)
    av_s = name_accumulation_variable((Restriction.POSITIVE,))
    av_n = name_accumulation_variable((Restriction.NEGATIVE,))
    return ((True, geo), (True, lfsu_s), (True, ac_s), (True, lfsv_s), (True, lfsu_n), (True, ac_n), (True, lfsv_n), (False, av_s), (False, av_n))


def nonlinear_jacobian_apply_volume_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    lpt = type_linearizationpointcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lpt, lfsvt, avt)


def nonlinear_jacobian_apply_volume_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.NONE)
    lfsv = name_testfunctionspace(Restriction.NONE)
    cc = name_coefficientcontainer(Restriction.NONE)
    ac = name_applycontainer(Restriction.NONE)
    av = name_accumulation_variable((Restriction.NONE,))
    return ((True, geo), (True, lfsu), (True, cc), (True, ac), (True, lfsv), (False, av))


def nonlinear_jacobian_apply_boundary_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    lpt = type_linearizationpointcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lpt, lfsvt, avt)


def nonlinear_jacobian_apply_boundary_args():
    geo = name_geometry_wrapper()
    lfsu = name_trialfunctionspace(Restriction.POSITIVE)
    lfsv = name_testfunctionspace(Restriction.POSITIVE)
    cc = name_coefficientcontainer(Restriction.POSITIVE)
    ac = name_applycontainer(Restriction.POSITIVE)
    av = name_accumulation_variable((Restriction.POSITIVE,))
    return ((True, geo), (True, lfsu), (True, cc), (True, ac), (True, lfsv), (False, av))


def nonlinear_jacobian_apply_skeleton_templates():
    geot = type_geometry_wrapper()
    lfsut = type_trialfunctionspace()
    lfsvt = type_testfunctionspace()
    cct = type_coefficientcontainer()
    lpt = type_linearizationpointcontainer()
    avt = type_accumulation_variable()
    return (geot, lfsut, cct, lpt, lfsvt, lfsut, cct, lpt, lfsvt, avt, avt)


def nonlinear_jacobian_apply_skeleton_args():
    geo = name_geometry_wrapper()
    lfsu_s = name_trialfunctionspace(Restriction.POSITIVE)
    lfsu_n = name_trialfunctionspace(Restriction.NEGATIVE)
    lfsv_s = name_testfunctionspace(Restriction.POSITIVE)
    lfsv_n = name_testfunctionspace(Restriction.NEGATIVE)
    cc_s = name_coefficientcontainer(Restriction.POSITIVE)
    cc_n = name_coefficientcontainer(Restriction.NEGATIVE)
    ac_s = name_applycontainer(Restriction.POSITIVE)
    ac_n = name_applycontainer(Restriction.NEGATIVE)
    av_s = name_accumulation_variable((Restriction.POSITIVE,))
    av_n = name_accumulation_variable((Restriction.NEGATIVE,))
    return ((True, geo), (True, lfsu_s), (True, cc_s), (True, ac_s), (True, lfsv_s), (True, lfsu_n), (True, cc_n), (True, ac_n), (True, lfsv_n), (False, av_s), (False, av_n))
