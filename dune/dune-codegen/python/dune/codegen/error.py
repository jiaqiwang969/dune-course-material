""" Some error classes for dune-codegen """


class CodegenError(Exception):
    pass


class CodegenUFLError(CodegenError):
    pass


class CodegenCodegenError(CodegenError):
    pass


class CodegenLoopyError(CodegenError):
    pass


class CodegenVectorizationError(CodegenCodegenError):
    pass


class CodegenAutotuneError(CodegenVectorizationError):
    pass


class CodegenUnsupportedFiniteElementError(CodegenUFLError):
    pass
