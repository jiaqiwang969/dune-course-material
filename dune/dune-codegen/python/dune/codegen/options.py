""" Manage the command line options to the form compiler executable """

from argparse import ArgumentParser
from os.path import abspath
from pytools import ImmutableRecord, memoize
import cerberus
import yaml
import pkg_resources
from six.moves import configparser
from six import StringIO
from contextlib import contextmanager

from dune.codegen.error import CodegenError


class CodegenOptionsValidator(cerberus.Validator):
    # A validator that accepts the helpstr field in the scheme
    def _validate_helpstr(self, helpstr, field, value):
        """ Describe the option

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        return True


def _load_scheme(identifier):
    assert identifier in ["global", "form", "driverblock"]
    resource_package = __name__
    if identifier == "global":
        resource_path = 'options_global.yaml'
    elif identifier == "form":
        resource_path = 'options_form.yaml'
    else:
        assert identifier == "driverblock"
        resource_path = 'options_driverblock.yaml'
    yaml_stream = pkg_resources.resource_string(resource_package, resource_path)
    try:
        scheme = yaml.safe_load(yaml_stream)
    except Exception as e:
        raise e
    return scheme


class CodegenGlobalOptionsArray(ImmutableRecord):
    """ A collection of form compiler arguments """
    def __init__(self, **kwargs):
        # Set the default values from the yaml scheme as defaults
        scheme = _load_scheme("global")
        opts = {k: v['default'] for k, v in scheme.items()}
        opts.update(**kwargs)
        ImmutableRecord.__init__(self, **opts)


class CodegenFormOptionsArray(ImmutableRecord):
    """ A collection of form-specific form compiler arguments """
    def __init__(self, **kwargs):
        # Set the default values from the yaml scheme as defaults
        scheme = _load_scheme("form")
        opts = {k: v['default'] for k, v in scheme.items()}
        opts.update(**kwargs)
        ImmutableRecord.__init__(self, **opts)


class CodegenDriverBlockOptionsArray(ImmutableRecord):
    """ A collection of form-specific form compiler arguments """
    def __init__(self, **kwargs):
        # Set the default values from the yaml scheme as defaults
        scheme = _load_scheme("driverblock")
        opts = {k: v['default'] for k, v in scheme.items()}
        opts.update(**kwargs)
        ImmutableRecord.__init__(self, **opts)


# Until more sophisticated logic is needed, we keep the actual option data in this module
_global_options = CodegenGlobalOptionsArray()
_form_options = {}
_driverblock_options = {}


def show_options():
    def print_options(identifier):
        scheme = _load_scheme(identifier)
        for k, v in scheme.items():
            print("{}\n    {}".format(k, v['helpstr']))

    print("This is a summary of options available for the code generation process:\n")
    print("The following options can be given in the [formcompiler] section:")
    print_options("global")

    print("\nThefollowing options can be given in a form-specific subsection of [formcompiler]:")
    print_options("form")

    print("\nThefollowing options can be given in a driverblock subsection [formcompiler.driverblock.name]:")
    print_options("driverblock")


def process_global_options(opt):
    """ Make sure that the options have been fully processed """
    opt = expand_architecture_options(opt)

    if opt.overlapping:
        opt = opt.copy(parallel=True)

    return opt


def process_form_options(opt, form):
    if opt.sumfact:
        opt = opt.copy(unroll_dimension_loops=True,
                       quadrature_mixins="sumfact",
                       basis_mixins="sumfact",
                       accumulation_mixins="sumfact",
                       )

    if opt.blockstructured:
        opt = opt.copy(accumulation_mixins="blockstructured",
                       quadrature_mixins="blockstructured",
                       basis_mixins="blockstructured"
                       )

    if opt.control:
        opt = opt.copy(accumulation_mixins="control")

    if opt.numerical_jacobian:
        opt = opt.copy(generate_jacobians=False, generate_jacobian_apply=False)

    if opt.form is None:
        opt = opt.copy(form=form)

    if opt.classname is None:
        opt = opt.copy(classname="{}Operator".format(form))

    if opt.filename is None:
        opt = opt.copy(filename="{}_{}_file.hh".format(get_option("target_name"), opt.classname))

    if opt.block_preconditioner_pointdiagonal:
        opt = opt.copy(generate_jacobians=False,
                       basis_mixins="sumfact_pointdiagonal",
                       accumulation_mixins="sumfact_pointdiagonal",
                       )

    if opt.block_preconditioner_diagonal or opt.block_preconditioner_offdiagonal:
        assert opt.numerical_jacobian is False
        opt = opt.copy(generate_residuals=False,
                       generate_jacobians=True,
                       matrix_free=True,
                       )

    if opt.matrix_free:
        opt = opt.copy(generate_jacobian_apply=True)

    return opt


def process_driverblock_options(opt, driverblock):
    # Some preprocessing in case of no driver block section
    if driverblock == "default_driver_block":
        opt = opt.copy(classname="DriverBlock")
        opt = opt.copy(filename="{}_driverblock.hh".format(get_option("target_name")))
        operators = [i.strip() for i in get_option("operators").split(",")]

        # Note: In the case of hand written drivers we might have the default
        # driver block and multiple operators.
        if len(operators) == 2 and "mass" in operators:
            opt = opt.copy(temporal_form="mass")
            operators.remove("mass")
            opt = opt.copy(spatial_form=operators[0])
        elif len(operators) == 1:
            opt = opt.copy(spatial_form=operators[0])

    if opt.classname is None:
        opt = opt.copy(classname="DriverBlock{}".format(driverblock.capitalize()))

    if opt.filename is None:
        opt = opt.copy(filename="{}_{}_driverblock.hh".format(get_option("target_name"), opt.classname))

    return opt


def expand_architecture_options(opt):
    if opt.architecture == "haswell":
        return opt.copy(max_vector_width=256)
    elif opt.architecture == "knl":
        return opt.copy(max_vector_width=512)
    elif opt.architecture == "skylake":
        return opt.copy(max_vector_width=512)
    else:
        raise NotImplementedError("Architecture {} not known!".format(opt.architecture))


def initialize_options():
    """ Initialize the options from the command line """
    global _global_options
    _global_options = update_options_from_commandline(_global_options)
    _global_options = update_options_from_inifile(_global_options)
    _global_options = process_global_options(_global_options)
    for form in _form_options:
        _form_options[form] = process_form_options(_form_options[form], form)
    for db in _driverblock_options:
        _driverblock_options[db] = process_driverblock_options(_driverblock_options[db], db)

    # Validate global options
    scheme_global = _load_scheme("global")
    validator_global = CodegenOptionsValidator(scheme_global, require_all=True)
    opt_dict = _global_options.__dict__
    if not validator_global.validate({k: v for k, v in opt_dict.items() if not k.startswith("_")}):
        raise RuntimeError("Global options validation failed: {}".format(validator_global.errors))

    # Validate form options
    scheme_form = _load_scheme("form")
    validator_form = CodegenOptionsValidator(scheme_form, require_all=True)
    for form in [i.strip() for i in _global_options.operators.split(",")]:
        opt_dict = _form_options[form].__dict__
        if not validator_form.validate({k: v for k, v in opt_dict.items() if not k.startswith("_")}):
            raise RuntimeError("Form options validation failed: {}".format(validator_form.errors))

    # Validate driverblock options
    scheme_driverblock = _load_scheme("driverblock")
    validator = CodegenOptionsValidator(scheme_driverblock, require_all=True)
    for driverblock in [i.strip() for i in _global_options.driver_blocks.split(",")]:
        if not validator.validate({k: v for k, v in _driverblock_options[driverblock].__dict__.items() if not k.startswith("_")}):
            raise RuntimeError("Driverblock options validation failed: {}".format(validator.errors))


def _scheme_type_to_type(scheme_type):
    assert isinstance(scheme_type, str)
    if scheme_type == 'string':
        return str
    if scheme_type == 'boolean':
        return bool
    if scheme_type == 'integer':
        return int
    if scheme_type == 'float':
        return float


def _transform_type(scheme_type, a):
    if scheme_type == 'boolean':
        return bool(int(a))
    else:
        return _scheme_type_to_type(scheme_type)(a)


def update_options_from_commandline(opt):
    """ Return an options array object with updated values from the commandline """
    assert isinstance(opt, CodegenGlobalOptionsArray)
    parser = ArgumentParser(description="Compile UFL files to PDELab C++ code",
                            epilog="Please report bugs to dominic.kempf@iwr.uni-heidelberg.de",
                            )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    # Load global options scheme
    scheme = _load_scheme("global")

    # Add all options that have a helpstr to the command line parser
    for k, v in scheme.items():
        if v['helpstr'] is not None:
            cmdopt = "--{}".format(k.replace('_', '-'))
            parser.add_argument(cmdopt, help=v['helpstr'], type=_scheme_type_to_type(v['type']))
    parsedargs = {k: v for k, v in vars(parser.parse_args()).items() if v is not None}
    return opt.copy(**parsedargs)


def update_options_from_inifile(opt):
    """ Return an options array object with updated values from an inifile """
    if opt.ini_file:
        config = configparser.ConfigParser()

        # Read ini file
        try:
            config.read(opt.ini_file)
        except configparser.MissingSectionHeaderError:
            # Config parser doesn't like ini files where without section. For
            # this case we introduce a [root] section on top.
            ini_str = '[root]\n' + open(opt.ini_file, 'r').read()
            ini_fp = StringIO(ini_str)
            config = configparser.RawConfigParser()
            config.readfp(ini_fp)

        # Parse global options
        scheme = _load_scheme("global")
        options = {}
        if config.has_section('formcompiler'):
            options = dict(config.items('formcompiler'))
        for k, v in options.items():
            if k not in scheme:
                raise CodegenError("You try to set the global option '{}' in your ini file. This is unknown to dune-codegen.".format(k))
            options[k] = _transform_type(scheme[k]['type'], v)
        opt = opt.copy(**options)

        # Parse form options
        scheme = _load_scheme("form")
        for form in [i.strip() for i in opt.operators.split(",")]:
            section = 'formcompiler.{}'.format(form)
            options = {}
            if config.has_section(section):
                options = dict(config.items('formcompiler.{}'.format(form)))
                for k, v in options.items():
                    if k not in scheme:
                        raise CodegenError("You try to set the form option '{}' in the subsection '[formcompiler.{}]' of your ini file. This is unknown to dune-codegen.".format(k, form))
                    options[k] = _transform_type(scheme[k]['type'], v)
            _form_options[form] = CodegenFormOptionsArray(**options)

        # Parse driverblock options
        scheme = _load_scheme("driverblock")
        for db in [i.strip() for i in opt.driver_blocks.split(",")]:
            section = 'formcompiler.driverblock.{}'.format(db)
            options = {}
            if config.has_section(section):
                options = dict(config.items('formcompiler.driverblock.{}'.format(db)))
                for k, v in options.items():
                    if k not in scheme:
                        raise CodegenError("You try to set the driverblock option '{}' in the subsection '[formcompiler.driverblock.{}]' of your ini file. This is unknown to dune-codegen.".format(k, db))
                    options[k] = _transform_type(scheme[k]['type'], v)
            _driverblock_options[db] = CodegenDriverBlockOptionsArray(**options)

    return opt


def set_option(key, value):
    """Add the key value pair to the options.

    If the key is already in the options dictionary its value will be
    overwritten.  Form compiler arguments will always be set before
    any other options.
    """
    global _global_options
    _global_options = _global_options.copy(**{key: value})


def set_form_option(key, value, form=None):
    if form is None:
        from dune.codegen.generation import get_global_context_value
        form = get_global_context_value("form_identifier", 0)
    if isinstance(form, int):
        form = get_option("operators").split(",")[form].strip()
    _form_options[form] = _form_options[form].copy(**{key: value})


def get_option(key):
    return getattr(_global_options, key)


def get_form_ident():
    # First check if the form is set through global context
    from dune.codegen.generation import get_global_context_value
    form = get_global_context_value("form_identifier")
    if form:
        return form

    driver_block = get_option("driver_block_to_build")

    def _default_form():
        idents = [i.strip() for i in get_option("operators").split(",")]
        if len(idents) == 2:
            idents.remove("mass")
        assert(len(idents) == 1)
        return idents[0]

    if driver_block is None:
        # If no driver block is specified there should be one form if the
        # problem is stationary or two forms where one form is called mass for
        # the instationary case
        return _default_form()
    else:
        # If we generate driver blocks there a two cases:
        #
        # 1. The driver block specifies the forms
        #
        # 2. There are no forms specified in the driver block. This means the
        # default from above should apply and there should only be one driver
        # block.
        form = get_driverblock_option("spatial_form")
        if form is None:
            return _default_form()
        else:
            return form


def get_mass_form_ident():
    driver_block = get_option("driver_block_to_build")

    def _default_form():
        idents = [i.strip() for i in get_option("operators").split(",")]
        if len(idents) == 2 and "mass" in idents:
            return "mass"
        else:
            return None

    if driver_block is None:
        return _default_form()
    else:
        form = get_driverblock_option("temporal_form")
        if form is None:
            return _default_form()
        else:
            return form


def get_form_option(key, form=None):
    if form is None:
        form = get_form_ident()
    return getattr(_form_options[form], key)


def get_driverblock_option(key, driverblock=None):
    if driverblock is None:
        driverblock = get_option("driver_block_to_build")

    # This means that this function was called during driver generation. This
    # means there should exactly one driver block specified in the options
    # (possibly with default values everywhere)
    if driverblock is None:
        driver_blocks = [i.strip() for i in get_option("driver_blocks").split(",")]
        assert len(driver_blocks) == 1
        driverblock = driver_blocks[0]
    if isinstance(driverblock, int):
        driverblock = get_option("driver_blocks").split(",")[driverblock].strip()
    return getattr(_driverblock_options[driverblock], key)


@contextmanager
def option_context(conditional=True, **opts):
    """ A context manager that sets a given option and restores it on exit. """
    # Backup old values and set to new ones
    if conditional:
        backup = {}
        for k, v in opts.items():
            backup[k] = get_option(k)
            set_option(k, v)

    yield

    if conditional:
        # Restore old values
        for k in opts.keys():
            set_option(k, backup[k])


@contextmanager
def form_option_context(conditional=True, **opts):
    """ A context manager that sets a given form option and restores it on exit """
    if conditional:
        form = opts.pop("form", None)

        # Backup old values and set to new ones
        backup = {}
        for k, v in opts.items():
            backup[k] = get_form_option(k, form=form)
            set_form_option(k, v, form=form)

    yield

    # Restore old values
    if conditional:
        for k in opts.keys():
            set_form_option(k, backup[k], form=form)
