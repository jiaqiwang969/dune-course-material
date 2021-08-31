from dune.codegen.loopy.symbolic import identity_map_fused_multiply_add
from dune.codegen.loopy.target import dtype_floatingpoint
from loopy.symbolic import IdentityMapperMixin
from pymbolic.mapper.constant_folder import CommutativeConstantFoldingMapper
from pymbolic.mapper.constant_converter import ConstantToNumpyConversionMapper


class ConstantFoldingMapper(CommutativeConstantFoldingMapper, IdentityMapperMixin):
    map_fused_multiply_add = identity_map_fused_multiply_add


class ConstantConverterMapper(ConstantToNumpyConversionMapper, IdentityMapperMixin):
    map_fused_multiply_add = identity_map_fused_multiply_add


def apply_constant_folding(kernel):
    constant_folding_mapper = ConstantFoldingMapper()
    constant_converter_mapper = ConstantConverterMapper(dtype_floatingpoint())
    new_insns = []
    for insn in kernel.instructions:
        new_insns.append(insn.with_transformed_expressions(
            lambda expr: constant_folding_mapper(constant_converter_mapper(expr)))
        )
    return kernel.copy(instructions=new_insns)
