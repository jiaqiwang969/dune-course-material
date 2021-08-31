""" Autotuning for sum factorization kernels """

import os
import re
import subprocess
import filelock
import hashlib
import logging
import json
from operator import mul
import pkg_resources
from six.moves import reduce
import textwrap
import time

import loopy as lp
from pytools import product
from cgen import ArrayOf, AlignedAttribute, Initializer

from dune.codegen.generation import cache_restoring, delete_cache_items
from dune.codegen.loopy.target import DuneTarget, type_floatingpoint
from dune.codegen.sumfact.realization import realize_sumfact_kernel_function
from dune.codegen.options import get_option, option_context
from dune.codegen.error import CodegenAutotuneError


def get_cmake_cache_entry(entry):
    for line in open(os.path.join(get_option("project_basedir"), "CMakeCache.txt"), "r"):
        match = re.match("{}:[INTERNAL|FILEPATH|BOOL|STRING|PATH|UNINITIALIZED|STATIC]+=(.*)".format(entry), line)
        if match:
            return match.groups()[0]


def get_dune_codegen_dir():
    if get_cmake_cache_entry("CMAKE_PROJECT_NAME") == "dune-codegen":
        return get_option("project_basedir")
    else:
        return get_cmake_cache_entry("dune-codegen_DIR")


def compiler_invocation(name, filename):
    # Determine the CMake Generator in use
    gen = get_cmake_cache_entry("CMAKE_GENERATOR")
    assert(gen == "Unix Makefiles")

    # Find compiler path
    compiler = get_cmake_cache_entry("CMAKE_CXX_COMPILER")
    compile_flags = [compiler]

    # Parse compiler flags
    for line in open(os.path.join(get_dune_codegen_dir(), "python", "CMakeFiles", "_autotune_target.dir", "flags.make"), "r"):
        match = re.match("([^=]*)=(.*)", line)
        if match:
            compile_flags.extend(match.groups()[1].split())

    # Add the source file
    compile_flags.append(filename)

    # Parse linker flags
    for line in open(os.path.join(get_dune_codegen_dir(), "python", "CMakeFiles", "_autotune_target.dir", "link.txt"), "r"):
        match = re.match(".*_autotune_target (.*)", line)
        if match:
            for flag in match.groups()[0].split():
                if flag.startswith("-") or os.path.isabs(flag):
                    compile_flags.append(flag)
                else:
                    compile_flags.append(os.path.join(get_dune_codegen_dir(), "python", flag))

    # Set an output name
    compile_flags.append("-o")
    compile_flags.append(name)

    return compile_flags


def write_global_data(sf, filename):
    opcounting = get_option("opcounter")
    with open(filename, "a") as f:
        # Get kernel
        from dune.codegen.pdelab.localoperator import extract_kernel_from_cache
        knl = realize_sumfact_kernel_function(sf)
        constructor_knl = extract_kernel_from_cache("operator", "constructor_kernel", None, wrap_in_cgen=False, add_timings=False)
        constructor_knl = constructor_knl.copy(target=DuneTarget(declare_temporaries=False))
        constructor_knl = lp.get_one_scheduled_kernel(constructor_knl)

        target = DuneTarget()
        from loopy.codegen import CodeGenerationState
        codegen_state = CodeGenerationState(kernel=constructor_knl,
                                            implemented_data_info=None,
                                            implemented_domain=None,
                                            implemented_predicates=frozenset(),
                                            seen_dtypes=frozenset(),
                                            seen_functions=frozenset(),
                                            seen_atomic_dtypes=frozenset(),
                                            var_subst_map={},
                                            allow_complex=False,
                                            is_generating_device_code=True,
                                            )

        for decl in target.get_device_ast_builder().get_temporary_decls(codegen_state, 0):
            f.write("{}\n".format(next(iter(decl.generate()))))


def write_setup_code(sf, filename, define_thetas=True):
    with open(filename, "a") as f:
        # Setup a polynomial object (normally done in the LocalOperator members)
        from dune.codegen.loopy.target import type_floatingpoint
        real = type_floatingpoint()
        f.write("  using RF = {};\n".format(real))
        f.write("  using DF = {};\n".format(real))

        from dune.codegen.sumfact.tabulation import name_polynomials
        degs = tuple(m.basis_size - 1 for m in sf.matrix_sequence_quadrature_permuted)
        for deg in set(degs):
            f.write("  Dune::QkStuff::EquidistantLagrangePolynomials<DF, RF, {}> {};\n".format(deg, name_polynomials(deg)))

        # Get kernel
        from dune.codegen.pdelab.localoperator import extract_kernel_from_cache
        knl = realize_sumfact_kernel_function(sf)
        constructor_knl = extract_kernel_from_cache("operator", "constructor_kernel", None, wrap_in_cgen=False, add_timings=False)
        constructor_knl = constructor_knl.copy(target=DuneTarget(declare_temporaries=False))
        constructor_knl = lp.get_one_scheduled_kernel(constructor_knl)

        # Allocate buffers
        alignment = get_option("max_vector_width") // 8
        size = max(product(m.quadrature_size for m in sf.matrix_sequence_quadrature_permuted) * sf.vector_width,
                   product(m.basis_size for m in sf.matrix_sequence_quadrature_permuted) * sf.vector_width)
        size = int(size * (get_option("precision_bits") / 8))
        f.writelines(["  char buffer0[{}] __attribute__ ((aligned ({})));\n".format(size, alignment),
                      "  char buffer1[{}] __attribute__ ((aligned ({})));\n".format(size, alignment),
                      ])

        # Setup fastdg inputs
        for arg in sf.interface.signature_args:
            if "jacobian" in arg:
                f.write("{} = 0;\n".format(arg))
            else:
                size = sf.interface.fastdg_interface_object_size
                f.write("  RF {}[{}] __attribute__ ((aligned ({})));\n".format(arg.split()[-1], size, alignment))

        # Write stuff into the input buffer
        f.writelines(["  {0} *input = ({0} *)buffer0;\n".format(real),
                      "  {0} *output = ({0} *)buffer{1};\n".format(real, sf.length % 2),
                      "  for(int i=0; i<{}; ++i)\n".format(size / (get_option("precision_bits") / 8)),
                      "    input[i] = ({})(i+1);\n".format(real),
                      ])

        target = DuneTarget()
        from loopy.codegen import CodeGenerationState
        codegen_state = CodeGenerationState(kernel=constructor_knl,
                                            implemented_data_info=None,
                                            implemented_domain=None,
                                            implemented_predicates=frozenset(),
                                            seen_dtypes=frozenset(),
                                            seen_functions=frozenset(),
                                            seen_atomic_dtypes=frozenset(),
                                            var_subst_map={},
                                            allow_complex=False,
                                            is_generating_device_code=True,
                                            )

        if define_thetas:
            for decl in target.get_device_ast_builder().get_temporary_decls(codegen_state, 0):
                f.write("  {}\n".format(next(iter(decl.generate()))))

        for _, line in constructor_knl.preambles:
            if "gfsu" not in line:
                f.write("  {}\n".format(line))

        # Add setup code for theta matrices. We add some lines not necessary,
        # but it would be more work to remove them than keeping them.
        for line in lp.generate_body(constructor_knl).split("\n")[1:-1]:
            if "gfsu" not in line and "meshwidth" not in line and "geometry" not in line:
                f.write("  {}\n".format(line))

        # INtroduces a variable that makes sure that the kernel cannot be optimized away
        f.writelines(["  {} accum;\n".format(real),
                      "  std::mt19937 rng;\n",
                      "  rng.seed(42);\n",
                      "  std::uniform_int_distribution<> dis(0, {});\n".format(size / (get_option("precision_bits") / 8)),
                      ])


def generate_standalone_code_google_benchmark(sf, filename):
    delete_cache_items("kernel_default")

    # Turn off opcounting
    with option_context(opcounter=False):
        # Extract sum factorization kernel
        from dune.codegen.pdelab.localoperator import extract_kernel_from_cache
        knl = realize_sumfact_kernel_function(sf)

        # Add the implementation of the kernel.
        # TODO: This can probably done in a safer way?
        first_line = knl.member.lines[0]
        arguments = first_line[first_line.find("(") + 1:first_line.find(")")]

        with open(filename, "w") as f:
            f.writelines(["// {}".format(first_line),
                          "\n",
                          "#include \"config.h\"\n",
                          "#include \"benchmark/benchmark.h\"\n",
                          "#include<dune/pdelab/finiteelementmap/qkdg.hh>\n",
                          "#include<dune/codegen/common/vectorclass.hh>\n",
                          "#include<dune/codegen/sumfact/onedquadrature.hh>\n",
                          "#include<dune/codegen/sumfact/horizontaladd.hh>\n",
                          "#include<random>\n",
                          "#include<fstream>\n",
                          "#include<iostream>\n",
                          "\n"
                          ])

        write_global_data(sf, filename)

        with open(filename, "a") as f:
            arguments = ', '.join(sf.interface.signature_args)
            if len(arguments) > 0:
                arguments = ', ' + arguments
            arguments = 'const char* buffer0, const char* buffer1' + arguments
            f.write("void sumfact_kernel({})\n".format(arguments))
            for line in knl.member.lines[1:]:
                f.write("{}\n".format(line))

            f.write("\n\n")
            f.write("static void BM_sumfact_kernel(benchmark::State& state){\n")

        write_setup_code(sf, filename, define_thetas=False)

        additional_arguments = [i.split()[-1] for i in sf.interface.signature_args]
        additional_arguments = ', '.join(additional_arguments)
        if len(additional_arguments) > 0:
            additional_arguments = ', ' + additional_arguments
        with open(filename, "a") as f:
            f.writelines(["  for (auto _ : state){\n",
                          "    sumfact_kernel(buffer0, buffer1{});\n".format(additional_arguments),
                          "  }\n",
                          "}\n",
                          "BENCHMARK(BM_sumfact_kernel);\n",
                          "\n",
                          "BENCHMARK_MAIN();"
                          ])


def generate_standalone_code(sf, filename):
    delete_cache_items("kernel_default")

    # Turn off opcounting
    with option_context(opcounter=False):
        # Extract sum factorization kernel
        from dune.codegen.pdelab.localoperator import extract_kernel_from_cache
        knl = realize_sumfact_kernel_function(sf)
        first_line = knl.member.lines[0]

        with open(filename, "w") as f:
            f.writelines(["// {}".format(first_line),
                          "\n",
                          "#include \"config.h\"\n",
                          "#include<dune/pdelab/finiteelementmap/qkdg.hh>\n",
                          "#include<dune/codegen/common/tsc.hh>\n",
                          "#include<dune/codegen/common/vectorclass.hh>\n",
                          "#include<dune/codegen/sumfact/onedquadrature.hh>\n",
                          "#include<dune/codegen/sumfact/horizontaladd.hh>\n",
                          "#include<random>\n",
                          "#include<fstream>\n",
                          "#include<iostream>\n",
                          "\n"
                          ])

            f.writelines(["int main(int argc, char** argv)\n",
                          "{\n",
                          ])

        write_setup_code(sf, filename)

        # Write measurement
        with open(filename, "a") as f:
            # Start a TSC timer
            f.writelines(["  auto start = Dune::PDELab::TSC::start();\n",
                          ])

            # Add the implementation of the kernel.
            repeats = int(1e9 / sf.operations)
            f.write("  for(int i=0; i<{}; ++i)\n".format(repeats))
            f.write("  {\n")
            for line in knl.member.lines[1:]:
                f.write("    {}\n".format(line))
            f.write("  }\n")

            # Stop the TSC timer and write the result to a file
            f.writelines(["  auto stop = Dune::PDELab::TSC::stop();\n",
                          "  std::ofstream file;\n",
                          "  file.open(argv[1]);\n",
                          "  file << Dune::PDELab::TSC::elapsed(start, stop) / {} << std::endl;\n".format(str(float(repeats))),
                          "  file.close();\n",
                          "  accum += output[dis(rng)];\n",
                          "  std::cout << accum;\n",
                          "}\n",
                          ])


def generate_standalone_kernel_code(kernel, signature, filename, transformations=None):
    # Turn off opcounting
    with option_context(opcounter=False):
        # Remove opcounter from signature
        p = re.compile('OpCounter::OpCounter<([^>]*)>')
        assert len(signature) == 1
        sig = signature[0]
        sig = p.sub(r'\1', sig)
        assert 'OpCounter' not in signature

        # Which transformations were applied
        codegen_transformations = ''
        if transformations:
            codegen_transformations = ''
            for trafo in transformations:
                codegen_transformations += '// {}\n'.format(trafo)

        template = 'kernel_benchmark_template1.cc.in'
        use_datasets = True

        # Old benchmark template
        # template = 'kernel_benchmark_template0.cc.in'
        # use_datasets = False

        template_filename = pkg_resources.resource_filename(__name__, template)
        with open(template_filename, 'r') as f:
            benchmark = f.read()

        # Find function arguments and global arguments
        arguments = sig[sig.find('(') + 1:sig.find(')')].split(',')
        arguments = [a.split(' ')[-1] for a in arguments]
        global_args = [a for a in kernel.args if a.name not in arguments]
        buffer_arguments = [a for a in arguments if a.startswith('buff')]
        input_arguments = [a for a in arguments if a not in buffer_arguments]

        # Declare global arguments
        codegen_declare_global_arguments = ''
        target = DuneTarget()
        for g in global_args:
            decl_info = g.decl_info(target, True, g.dtype)
            for idi in decl_info:
                ast_builder = target.get_device_ast_builder()
                arg_decl = lp.target.c.POD(ast_builder, idi.dtype, idi.name)
                arg_decl = ArrayOf(arg_decl, reduce(mul, g.shape))
                arg_decl = AlignedAttribute(g.dtype.itemsize * g.vector_size(target), arg_decl)
                codegen_declare_global_arguments += '{}\n'.format(arg_decl)
        codegen_declare_global_arguments = textwrap.indent(codegen_declare_global_arguments, '  ')

        # Helper function for argument initialization
        def _initialize_arg(arg):
            if isinstance(arg, lp.ValueArg):
                return []
            real = type_floatingpoint()
            size = reduce(mul, arg.shape)
            fill_name = arg.name + '_fill'
            lines = ['  {}* {} = (double *) {};'.format(real, fill_name, arg.name),
                     '  for (std::size_t i=0; i<{}; ++i){{'.format(size),
                     '    {}[i] = unif(re);'.format(fill_name),
                     '  }']
            return lines

        # Initialize global arguments
        codegen_initialize_global_arguments = ''
        for arg in global_args:
            lines = _initialize_arg(arg)
            codegen_initialize_global_arguments += '\n'.join(lines) + '\n'
        codegen_initialize_global_arguments = textwrap.indent(codegen_initialize_global_arguments, '  ')

        codegen_initialize_input = ''

        # Function we want to benchmark
        codegen_benchmark_function = ''
        codegen_benchmark_function += sig[0:sig.find(')') + 1]
        codegen_benchmark_function += lp.generate_body(kernel)
        codegen_benchmark_function = textwrap.indent(codegen_benchmark_function, '  ')

        # Declare function arguments
        codegen_declare_arguments = []
        codegen_declare_input = []
        function_arguments = [a for a in kernel.args if a.name in arguments]
        for arg in function_arguments:
            if 'buffer' in arg.name:
                byte_size = reduce(mul, arg.shape) * 8
                codegen_declare_arguments.append('  char {}[{}] __attribute__ ((aligned ({})));\n'.format(arg.name,
                                                                                                          byte_size,
                                                                                                          arg.alignment),)
            elif isinstance(arg, lp.ValueArg):
                assert 'jacobian_offset' in arg.name
                decl = arg.get_arg_decl(ast_builder)
                decl = Initializer(decl, 'unif_int(re)')
                codegen_declare_arguments.append(('  {}\n'.format(decl)))
            else:
                assert 'fastdg' in arg.name
                size = reduce(mul, arg.shape)
                min_stride = min([tag.stride for tag in arg.dim_tags])
                size *= min_stride
                alignment = arg.dtype.itemsize
                real = type_floatingpoint()
                if use_datasets:
                    codegen_declare_input.append(('{} {}[datasets][{}] __attribute__ ((aligned ({})));\n'.format(real,
                                                                                                                 arg.name,
                                                                                                                 size,
                                                                                                                 alignment)))
                else:
                    codegen_declare_input.append(('{} {}[{}] __attribute__ ((aligned ({})));\n'.format(real,
                                                                                                       arg.name,
                                                                                                       size,
                                                                                                       alignment)))

        codegen_declare_arguments = ''.join(codegen_declare_arguments)
        codegen_declare_arguments = textwrap.indent(codegen_declare_arguments, '  ')
        codegen_declare_input = ''.join(codegen_declare_input)
        codegen_declare_input = textwrap.indent(codegen_declare_input, '  ')

        # Initialize function arguments
        codegen_initialize_arguments = ''
        codegen_initialize_input = ''
        for arg in function_arguments:
            if 'fastdg' in arg.name:
                if use_datasets:
                    lines = _initialize_arg(arg)
                    lines = ['  ' + a for a in lines]
                    lines = [a.replace(arg.name + ';', arg.name + '[i];') for a in lines]
                    lines.insert(0, 'for(std::size_t i=0; i<datasets; ++i){')
                    lines.append('}')
                    codegen_initialize_input += '\n'.join(lines) + '\n'
                else:
                    lines = _initialize_arg(arg)
                    codegen_initialize_arguments += '\n'.join(lines) + '\n'
            else:
                lines = _initialize_arg(arg)
                codegen_initialize_arguments += '\n'.join(lines) + '\n'
        codegen_initialize_arguments = textwrap.indent(codegen_initialize_arguments, '  ')
        codegen_initialize_input = textwrap.indent(codegen_initialize_input, '  ')

        # Call the benchmark function
        if use_datasets:
            arguments_with_datasets = arguments.copy()
            arguments_with_datasets = [a if 'fastdg' not in a else a + '[i]' for a in arguments]
            codegen_call_benchmark_function = 'for (std::size_t i=0; i<datasets; ++i){\n'
            codegen_call_benchmark_function += '  ' + kernel.name + '({})'.format(','.join(arguments_with_datasets)) + ';\n'
            for arg in input_arguments:
                codegen_call_benchmark_function += 'benchmark::DoNotOptimize({}[i][0]);\n'.format(arg)
            codegen_call_benchmark_function += '}'
        else:
            codegen_call_benchmark_function = kernel.name + '({})'.format(','.join(arguments)) + ';\n'
        codegen_call_benchmark_function = textwrap.indent(codegen_call_benchmark_function, '    ')

        # Replace placeholders in benchmark template
        benchmark = benchmark.replace('${CODEGEN_TRANSFORMATIONS}', codegen_transformations)
        benchmark = benchmark.replace('${CODEGEN_DECLARE_GLOBAL_ARGUMENTS}', codegen_declare_global_arguments)
        benchmark = benchmark.replace('${CODEGEN_DECLARE_INPUT}', codegen_declare_input)
        benchmark = benchmark.replace('${CODEGEN_INITIALIZE_GLOBAL_ARGUMENTS}', codegen_initialize_global_arguments)
        benchmark = benchmark.replace('${CODEGEN_INITIALIZE_INPUT}', codegen_initialize_input)
        benchmark = benchmark.replace('${CODEGEN_BENCHMARK_FUNCTION}', codegen_benchmark_function)
        benchmark = benchmark.replace('${CODEGEN_DECLARE_ARGUMENTS}', codegen_declare_arguments)
        benchmark = benchmark.replace('${CODEGEN_INITIALIZE_ARGUMENTS}', codegen_initialize_arguments)
        benchmark = benchmark.replace('${CODEGEN_CALL_BENCHMARK_FUNCTION}', codegen_call_benchmark_function)

        # Write benchmark source file
        with open(filename, 'w') as f:
            f.writelines(benchmark)


def autotune_realization(sf=None, kernel=None, signature=None, transformations=None):
    """Generate an microbenchmark, compile run and return time

    Parameters
    ----------
    sf: SumfactKernel or VectorizedSumfactKernel
    kernel: loopy.kernel.LoopKernel
    signature: str
    transformation: list of str
        Will be used to distinguish between autotune targets
    """
    if sf is None:
        assert kernel is not None
        assert signature is not None
    else:
        assert kernel is None
        assert signature is None

    logger = logging.getLogger(__name__)

    # Make sure that the benchmark directory exists
    dir = os.path.join(get_option("project_basedir"), "autotune-benchmarks")
    if not os.path.exists(dir):
        os.mkdir(dir)

    if sf is None:
        basename = "autotune_sumfact_{}".format(kernel.name)
    else:
        basename = "autotune_sumfact_{}".format(sf.function_name)
    if transformations:
        for trafo in transformations:
            basename = '{}_{}'.format(basename, trafo)
    basename = hashlib.sha256(basename.encode()).hexdigest()

    filename = os.path.join(dir, "{}.cc".format(basename))
    logname = os.path.join(dir, "{}.log".format(basename))
    lock = os.path.join(dir, "{}.lock".format(basename))
    executable = os.path.join(dir, basename)

    # Generate and compile a benchmark program
    #
    # Note: cache restoring is only necessary when generating from SumfactKernel
    with cache_restoring():
        with filelock.FileLock(lock):
            if not os.path.isfile(logname):
                logger.debug('Generate autotune target in file {}'.format(filename))

                if sf is None:
                    generate_standalone_kernel_code(kernel, signature, filename, transformations)
                elif get_option("autotune_google_benchmark"):
                    generate_standalone_code_google_benchmark(sf, filename)
                else:
                    generate_standalone_code(sf, filename)

                call = []
                wrapper = get_cmake_cache_entry("DUNE_CODEGEN_BENCHMARK_COMPILATION_WRAPPER")
                if wrapper:
                    call.append(wrapper)

                call.extend(compiler_invocation(executable, filename))
                devnull = open(os.devnull, 'w')
                os.environ['DUNE_CODEGEN_THREADS'] = '1'
                ret = subprocess.call(call, stdout=devnull, stderr=subprocess.STDOUT)
                if ret != 0:
                    raise CodegenAutotuneError("Compilation of autotune executable failed. Invocation: {}".format(" ".join(call)))

                # File system synchronization!
                while not os.path.exists(executable):
                    time.sleep(0.01)

                # Check whether the user specified an execution wrapper
                call = []
                wrapper = get_cmake_cache_entry("DUNE_CODEGEN_BENCHMARK_EXECUTION_WRAPPER")
                if wrapper:
                    call.append(wrapper)

                # Run the benchmark program
                call.append(executable)
                if get_option("autotune_google_benchmark"):
                    call.append("--benchmark_out={}".format(logname))
                    call.append("--benchmark_repetitions=5")
                    # call.append("--benchmark_out_format=csv")
                else:
                    call.append(logname)
                ret = subprocess.call(call, stdout=devnull, stderr=subprocess.STDOUT)
                if ret != 0:
                    raise CodegenAutotuneError("Execution of autotune benchmark failed. Invocation: {}".format(" ".join(call)))

                # File system synchronization!
                while not os.path.exists(logname):
                    time.sleep(0.01)

            # Extract the result form the log file
            if get_option("autotune_google_benchmark"):
                import json
                with open(logname) as json_file:
                    try:
                        data = json.load(json_file)
                        minimal_time = 1e80
                        for b in data['benchmarks']:
                            if b['name'].endswith('_mean') or b['name'].endswith('_median') or b['name'].endswith('_stddev'):
                                pass
                            else:
                                if b['cpu_time'] < minimal_time:
                                    minimal_time = b['cpu_time']
                        assert minimal_time < 1e80
                        return minimal_time
                    except Exception as e:
                        print("Error while loading file {}".format(logname))
                        raise e
            else:
                return float(next(iter(open(logname, "r")))) / 1000000
