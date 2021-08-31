import loopy as lp
import numpy as np
import pymbolic.primitives as prim
from dune.codegen.blockstructured.tools import sub_element_inames

from loopy.match import Tagged, Id, Writes, Reads, And, Or, Iname, All, Not
from islpy import BasicSet

from dune.codegen.generation import get_global_context_value
from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.loopy.temporary import DuneTemporaryVariable
from dune.codegen.loopy.symbolic import substitute, InplaceCallInstruction
from dune.codegen.loopy.vcl import get_vcl_type_size, VCLPermute, VCLLoad, VCLStore
from dune.codegen.options import get_form_option
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.tools import get_pymbolic_basename


def add_vcl_temporaries(knl, vcl_size):
    vector_alias = [a for a in knl.arg_dict if a.endswith('alias')]

    # add new temporaries for vectors
    # hope one read insn doesn't have two different reads from the same temporary
    new_vec_temporaries = dict()
    new_insns = []
    init_iname = 'init_vec{}'.format(vcl_size)
    from islpy import BasicSet
    init_domain = BasicSet("{{ [{0}] : 0<={0}<{1} }}".format(init_iname, get_vcl_type_size(dtype_floatingpoint())))

    silenced_warnings = []

    for alias in vector_alias:
        vector_name = alias.replace('alias', 'vec{}'.format(vcl_size))
        new_vec_temporaries[vector_name] = DuneTemporaryVariable(vector_name, dtype=np.float64,
                                                                 shape=(vcl_size,), managed=True,
                                                                 scope=lp.temp_var_scope.PRIVATE, dim_tags=('vec',))
        # silence warning such that loopy won't complain
        silenced_warnings.append("read_no_write({})".format(vector_name))

    from loopy.kernel.data import VectorizeTag
    return knl.copy(instructions=knl.instructions + new_insns, domains=knl.domains + [init_domain],
                    temporary_variables=dict(**knl.temporary_variables, **new_vec_temporaries),
                    iname_to_tags=dict(**knl.iname_to_tags, **{init_iname: frozenset({VectorizeTag()})}),
                    silenced_warnings=knl.silenced_warnings + silenced_warnings)


def add_vcl_accum_insns(knl, inner_iname, outer_iname, vcl_size, level):
    nptype = dtype_floatingpoint()

    accum_insns = lp.find_instructions(knl, And((Tagged('accum'), Iname(inner_iname))))
    accum_ids = [insn.id for insn in accum_insns]

    new_insns = []
    vng = knl.get_var_name_generator()
    idg = knl.get_instruction_id_generator()
    new_vec_temporaries = dict()
    for insn in knl.instructions:
        # somehow CInstructions are not hashable....
        if isinstance(insn, lp.MultiAssignmentBase) and insn.id in accum_ids:
            # write accum expr as "r = expr + r"
            expr_without_r = prim.Sum(tuple(e for e in insn.expression.children if not e == insn.assignee))

            inames_micro = set((i for i in insn.within_inames if i.startswith('micro')))
            iname_ix = next((i for i in inames_micro if '_x' in i))  # TODO use TaggedIname when available

            # need inames for head and tail handling a priori
            from loopy.match import Not, All
            replace_head_inames = dict()
            replace_tail_inames = dict()
            for iname in inames_micro - frozenset({iname_ix}):
                head = iname + '_head'
                tail = iname + '_tail'
                replace_head_inames[iname] = prim.Variable(head)
                replace_tail_inames[iname] = prim.Variable(tail)
                knl = lp.duplicate_inames(knl, iname, Not(All()), suffix='_tail')
                knl = lp.duplicate_inames(knl, iname, Not(All()), suffix='_head')
            inames_head = frozenset((var.name for var in replace_head_inames.values()))
            inames_tail = frozenset((var.name for var in replace_tail_inames.values()))

            # declare a[iy] and b
            identifier_left = vng('left_node_vec{}'.format(vcl_size))
            identifier_right = vng('right_node_vec{}'.format(vcl_size))
            new_vec_temporaries[identifier_left] = DuneTemporaryVariable(identifier_left, dtype=np.float64,
                                                                         shape=(2,) * (world_dimension() - 1) +
                                                                               (vcl_size,),
                                                                         managed=True, scope=lp.temp_var_scope.PRIVATE,
                                                                         dim_tags=('f',) * (world_dimension() - 1) +
                                                                                  ('vec',))
            new_vec_temporaries[identifier_right] = DuneTemporaryVariable(identifier_right, dtype=np.float64,
                                                                          shape=(vcl_size,), managed=True,
                                                                          scope=lp.temp_var_scope.PRIVATE, dim_tags=('vec',))

            var_left = prim.Subscript(prim.Variable(identifier_left),
                                      tuple(prim.Variable(i) for i in sorted(inames_micro - frozenset({iname_ix}))) +
                                      (prim.Variable(inner_iname),))
            var_right = prim.Subscript(prim.Variable(identifier_right), (prim.Variable(inner_iname),))

            # initialize a before outer loop
            id_init_a = idg('insn_init_' + identifier_left)
            new_insns.append(lp.Assignment(assignee=substitute(var_left, replace_head_inames),
                                           expression=0,
                                           id=id_init_a,
                                           within_inames=(insn.within_inames - frozenset({outer_iname}) -
                                                          inames_micro) | inames_head,
                                           tags=frozenset({'head_vec{}'.format(vcl_size),
                                                           'vectorized_{}'.format(level)})))

            # compute a and b
            expr_right = substitute(expr_without_r, {iname_ix: 1})
            expr_left = prim.Sum((substitute(expr_without_r, {iname_ix: 0}), var_left))

            id_set_left = idg('{}_{}'.format(insn.id, identifier_left))
            id_set_right = idg('{}_{}'.format(insn.id, identifier_right))
            new_insns.append(lp.Assignment(assignee=var_right,
                                           expression=expr_right,
                                           id=id_set_right,
                                           depends_on=insn.depends_on,
                                           within_inames=insn.within_inames - frozenset({iname_ix}),
                                           tags=frozenset({'vectorized_{}'.format(level)})))
            new_insns.append(lp.Assignment(assignee=var_left,
                                           expression=expr_left,
                                           id=id_set_left,
                                           depends_on=insn.depends_on | frozenset({id_init_a}),
                                           within_inames=insn.within_inames - frozenset({iname_ix}),
                                           tags=frozenset({'vectorized_{}'.format(level)})))

            # r+=a[iy]
            id_accum = idg('{}_mod_accum'.format(insn.id))
            expr_accum = prim.Sum((var_left,
                                   prim.Call(VCLPermute(nptype, vcl_size, (-1,) + tuple(range(vcl_size - 1))),
                                             (var_right,)),
                                   substitute(insn.assignee, {iname_ix: 0})))
            new_insns.append(lp.Assignment(assignee=substitute(insn.assignee, {iname_ix: 0}),
                                           expression=expr_accum,
                                           id=id_accum,
                                           depends_on=insn.depends_on | frozenset({id_set_left,
                                                                                   id_init_a, id_set_right}),
                                           within_inames=insn.within_inames - frozenset({iname_ix}),
                                           tags=frozenset({'accum_vec{}'.format(vcl_size),
                                                           'vectorized_{}'.format(level)})))
            # a[iy] = permute
            id_permute = idg('{}_permute'.format(insn.id))
            expr_permute = prim.Call(VCLPermute(nptype, vcl_size, (vcl_size - 1,) + (-1,) * (vcl_size - 1)),
                                     (var_right,))
            new_insns.append(lp.Assignment(assignee=var_left,
                                           expression=expr_permute,
                                           id=id_permute,
                                           depends_on=insn.depends_on | frozenset({id_set_left, id_init_a, id_set_right,
                                                                                   id_accum}),
                                           within_inames=insn.within_inames - frozenset({iname_ix}),
                                           tags=frozenset({'vectorized_{}'.format(level)})
                                           ))

            # tail handling, uses tail alias
            id_accum_tail = idg('{}_accum_tail'.format(insn.id))
            subst_map = {inner_iname: vcl_size - 1, outer_iname: get_form_option("number_of_blocks") // vcl_size - 1,
                         iname_ix: 1, insn.assignee_name: prim.Variable(insn.assignee_name + '_tail'),
                         **replace_tail_inames}
            assignee_tail = substitute(insn.assignee, subst_map)
            expr_tail = prim.Sum((substitute(var_left, {inner_iname: 0, **replace_tail_inames}), assignee_tail))

            write_to_tail_ids = tuple(i.id for i in lp.find_instructions(knl,
                                                                         Writes(get_pymbolic_basename(assignee_tail))))

            new_insns.append(lp.Assignment(assignee=assignee_tail,
                                           expression=expr_tail,
                                           id=id_accum_tail,
                                           depends_on=(frozenset({id_accum, id_permute, id_set_left, id_init_a}) |
                                                       frozenset(write_to_tail_ids)),
                                           within_inames=(insn.within_inames - frozenset({inner_iname, outer_iname}) -
                                                          inames_micro) | inames_tail,
                                           tags=frozenset({'tail_vec{}'.format(vcl_size),
                                                           'vectorized_{}'.format(level)})))
        else:
            if insn.id.endswith('tail') and insn.id.replace('_tail', '') in accum_ids:
                accum_id = insn.id.replace('_tail', '')
                new_insns.append(insn.copy(depends_on=insn.depends_on | frozenset({accum_id + '_accum_tail'})))
            else:
                new_insns.append(insn)

    return knl.copy(instructions=new_insns,
                    temporary_variables=dict(**knl.temporary_variables, **new_vec_temporaries))


def add_vcl_access(knl, inner_iname, vcl_size, level=0):
    accum_insns = set((insn.id for insn in lp.find_instructions(knl, And((Tagged('accum*'),
                                                                          Iname(inner_iname))))))
    read_insns = set((insn.id for insn in lp.find_instructions(knl, And((Reads('*alias'), Iname(inner_iname))))))
    vectorized_insns = accum_insns | read_insns

    alias_suffix = 'alias'
    vector_sufix = 'vec{}'.format(vcl_size)

    from loopy.symbolic import CombineMapper
    from loopy.symbolic import IdentityMapper

    class AliasIndexCollector(CombineMapper, IdentityMapper):
        def __init__(self):
            self.found_alias = False

        def combine(self, values):
            return sum(values, tuple())

        def map_constant(self, expr):
            if self.found_alias:
                return (expr,)
            else:
                return tuple()

        map_variable = map_constant
        map_function_symbol = map_constant
        map_loopy_function_identifier = map_constant

        def map_subscript(self, expr):
            if expr.aggregate.name.endswith(alias_suffix):
                self.found_alias = True
                indices = self.combine((self.rec(index) for index in expr.index_tuple))
                self.found_alias = False
                return expr.aggregate, indices
            else:
                return tuple()

    # add load instructions if the vector is read, based on the read instruction
    # TODO brauche mehrere vectoren, falls in einer insn von einem alias mit unterschiedlichen idx gelesen wird
    # muss dafür eigentlich nur den namen des vectors anpassen
    idg = knl.get_instruction_id_generator()
    aic = AliasIndexCollector()
    load_insns = []
    read_dependencies = dict()
    vectorized_insn_to_vector_names = dict()
    for id in read_insns:
        insn = knl.id_to_insn[id]

        alias, index = aic(insn.expression)
        name_alias = alias.name
        name_vec = name_alias.replace(alias_suffix, vector_sufix)
        vectorized_insn_to_vector_names[id] = (name_alias, name_vec)

        # compute index without vec iname
        strides = tuple(tag.stride for tag in knl.arg_dict[name_alias].dim_tags)
        flat_index = prim.Sum(tuple(prim.Product((i, s)) for i, s in zip(index, strides)
                                    if not (isinstance(i, prim.Variable) and i.name == inner_iname)))

        # find write insns
        write_ids = frozenset(i.id for i in lp.find_instructions(knl, Or((Writes(name_vec), Writes(name_vec)))))

        # add load instruction
        load_id = idg('insn_' + name_vec + '_load')
        call_load = prim.Call(VCLLoad(name_vec), (prim.Sum((prim.Variable(name_alias), flat_index)),))
        load_insns.append(InplaceCallInstruction(inplace_assignees=(prim.Subscript(prim.Variable(name_vec),
                                                                                   (prim.Variable(inner_iname),)),),
                                                 expression=call_load,
                                                 id=load_id, within_inames=insn.within_inames | insn.reduction_inames(),
                                                 depends_on=insn.depends_on | write_ids,
                                                 depends_on_is_final=True,
                                                 tags=frozenset({'vectorized_{}'.format(level)})))
        read_dependencies.setdefault(id, set())
        read_dependencies[id].add(load_id)

    # add store instructions if the vector is written, based on the write instruction
    store_insns = []
    for id in accum_insns:
        insn = knl.id_to_insn[id]

        alias, index = aic(insn.expression)
        name_alias = alias.name
        name_vec = name_alias.replace(alias_suffix, vector_sufix)
        vectorized_insn_to_vector_names[id] = (name_alias, name_vec)

        # flat index without vec iname
        strides = tuple(tag.stride for tag in knl.arg_dict[name_alias].dim_tags)
        flat_index = prim.Sum(tuple(prim.Product((i, s)) for i, s in zip(index, strides)
                                    if not (isinstance(i, prim.Variable) and i.name == inner_iname)))

        # find write insns
        write_ids = frozenset(i.id for i in lp.find_instructions(knl, Or((Writes(name_vec), Writes(name_vec)))))

        # add store instruction
        store_id = idg('insn_' + name_vec + '_store')
        call_store = prim.Call(VCLStore(name_vec), (prim.Sum((prim.Variable(name_alias), flat_index)),))
        store_insns.append(InplaceCallInstruction(inplace_assignees=(prim.Variable(name_alias),), expression=call_store,
                                                  id=store_id, within_inames=insn.within_inames,
                                                  depends_on=(insn.depends_on | frozenset({id}) | read_dependencies[id] |
                                                              write_ids),
                                                  depends_on_is_final=True,
                                                  tags=frozenset({'vectorized_{}'.format(level)})))

    # replace alias with vcl vector, except for accumulation assignee
    vector_alias = [a for a in knl.arg_dict if a.endswith(alias_suffix)]
    dim = world_dimension()
    dim_names = ["x", "y", "z"] + [str(i) for i in range(4, dim + 1)]
    # remove CInstructions since loopy extract expects to get only assignments
    knl_with_subst_insns = knl.copy(instructions=[insn for insn in lp.find_instructions(knl, Iname(inner_iname))
                                                  if not isinstance(insn, lp.CInstruction)])
    for alias in vector_alias:
        # Rename lhs which would match the substitution rule since loopy doesn't want substitutions as lhs
        new_insns = []
        for insn in knl_with_subst_insns.instructions:
            if isinstance(insn, lp.Assignment) and isinstance(insn.assignee, prim.Subscript):
                if insn.assignee.aggregate.name == alias:
                    new_insns.append(insn.copy(assignee=prim.Subscript(prim.Variable('dummy_' + alias),
                                                                       insn.assignee.index_tuple)))
                else:
                    new_insns.append(insn)
            else:
                new_insns.append(insn)
        knl_with_subst_insns = knl_with_subst_insns.copy(instructions=new_insns)

        # substitution rule for alias[[ex_o]*l,ex_inner, ey, ix, iy] -> vec[ex_inner]
        parameters = ','.join(['ex_o{}'.format(l) for l in range(level + 1)]) + \
                     ',v_i,' + \
                     ','.join(['e' + d for d in dim_names[1:dim]]) + \
                     ',ix,' + \
                     ','.join(['i' + d for d in dim_names[1:dim]])
        knl_with_subst_insns = lp.extract_subst(knl_with_subst_insns,
                                                alias + '_subst', '{}[{}]'.format(alias, parameters),
                                                parameters=parameters)
        new_subst = knl_with_subst_insns.substitutions.copy()
        rule = new_subst[alias + '_subst']
        rule.expression = prim.Subscript(prim.Variable(alias.replace(alias_suffix, vector_sufix)),
                                         (prim.Variable('v_i'),))
        knl_with_subst_insns = knl_with_subst_insns.copy(substitutions=new_subst)

    knl_with_subst_insns = lp.expand_subst(knl_with_subst_insns, Iname(inner_iname))
    knl = knl.copy(instructions=knl_with_subst_insns.instructions + [insn for insn in knl.instructions
                                                                     if insn.id not in knl_with_subst_insns.id_to_insn])

    # add store and load dependencies and set right accumulation assignee
    new_insns = []
    for insn in knl.instructions:
        if insn.id not in vectorized_insns:
            new_insns.append(insn)
        else:
            # find write insns
            name_alias, name_vec = vectorized_insn_to_vector_names[insn.id]
            write_ids = frozenset(i.id for i in lp.find_instructions(knl, Or((Writes(name_vec), Writes(name_vec)))))
            if insn.id in accum_insns:
                assignee_alias = insn.assignee
                try:
                    assignee_vec = next((expr for expr in insn.expression.children
                                         if isinstance(expr, prim.Subscript) and
                                         expr.aggregate.name.replace(vector_sufix, alias_suffix) ==
                                         assignee_alias.aggregate.name.replace('dummy_', '')))
                except StopIteration:
                    from dune.codegen.error import CodegenVectorizationError
                    raise CodegenVectorizationError
                new_insns.append(insn.copy(assignee=assignee_vec,
                                           depends_on=(insn.depends_on | read_dependencies[insn.id] |
                                                       write_ids),
                                           depends_on_is_final=True,
                                           tags=insn.tags | frozenset({'vectorized_{}'.format(level)})))
            else:
                new_insns.append(insn.copy(depends_on=(insn.depends_on | read_dependencies[insn.id] |
                                                       write_ids),
                                           depends_on_is_final=True,
                                           tags=insn.tags | frozenset({'vectorized_{}'.format(level)})))

    return knl.copy(instructions=new_insns + load_insns + store_insns)


def find_accumulation_inames(knl):
    inames = set()
    for insn in knl.instructions:
        if any((n.startswith('r_') and n.endswith('alias') for n in insn.write_dependency_names())):
            inames |= insn.within_inames

    inames = set((i for i in inames if i.startswith('micro') and not i.endswith('_x')))

    return inames


def add_iname_array(knl, iname):
    insns_with_macro_points = lp.find_instructions(knl, Tagged(iname))

    if insns_with_macro_points:
        new_iname = knl.get_var_name_generator()("init_iname_array_{}".format(iname))

        new_dom = BasicSet('{{ [{0}] : 0<={0}<{1} }}'.format(new_iname, get_form_option('number_of_blocks')))

        array_name = iname + '_arr'

        new_temporaries = dict()
        new_temporaries[array_name] = DuneTemporaryVariable(array_name, managed=True,
                                                            shape=(get_form_option('number_of_blocks'),),
                                                            scope=lp.temp_var_scope.PRIVATE, dtype=np.float64,
                                                            base_storage=array_name + '_buff',
                                                            _base_storage_access_may_be_aliasing=True)

        replacemap = dict()
        replacemap[iname] = prim.Subscript(prim.Variable(array_name), (prim.Variable(iname),))

        new_insns = [lp.Assignment(assignee=prim.Subscript(prim.Variable(array_name), (prim.Variable(new_iname),)),
                                   expression=prim.Variable(new_iname),
                                   id='init_{}_buffer'.format(array_name), tags=frozenset({"iname_array"}),
                                   within_inames=frozenset({new_iname}), within_inames_is_final=True)]

        for insn in knl.instructions:
            if insn in insns_with_macro_points:
                transformed_insn = insn.with_transformed_expressions(lambda expr: substitute(expr, replacemap))
                new_insns.append(transformed_insn.copy(
                    depends_on=frozenset({'init_{}_buffer'.format(array_name)}) | insn.depends_on))
            else:
                new_insns.append(insn)

        knl = knl.copy(instructions=new_insns, domains=knl.domains + [new_dom],
                       temporary_variables=dict(**knl.temporary_variables, **new_temporaries))

    return knl


def add_vcl_iname_array(knl, iname, vec_iname, vcl_size, level):
    insns_with_macro_points = lp.find_instructions(knl, And((Tagged(iname), Iname(vec_iname))))

    if insns_with_macro_points:
        iname_array = iname + '_arr'
        vector_name = iname + '_vec{}'.format(vcl_size)

        new_temporaries = {vector_name: DuneTemporaryVariable(vector_name, managed=True,
                                                              shape=(get_form_option('number_of_blocks'),),
                                                              scope=lp.temp_var_scope.PRIVATE, dtype=np.float64,
                                                              base_storage=iname_array + '_buff',
                                                              _base_storage_access_may_be_aliasing=True)}
        silenced_warning = ["read_no_write({})".format(vector_name)]

        replacemap = {iname_array: prim.Variable(vector_name)}

        new_insns = []
        for insn in knl.instructions:
            if insn in insns_with_macro_points:
                transformed_insn = insn.with_transformed_expressions(lambda expr: substitute(expr, replacemap))
                new_insns.append(transformed_insn.copy(
                    depends_on=frozenset({'init_{}_buffer'.format(iname_array)}) | insn.depends_on,
                    tags=insn.tags | frozenset({'vectorized_{}'.format(level)})))
            else:
                new_insns.append(insn)

        knl = knl.copy(instructions=new_insns,
                       temporary_variables=dict(**knl.temporary_variables, **new_temporaries),
                       silenced_warnings=knl.silenced_warnings + silenced_warning)

        knl = lp.split_array_axis(knl, (vector_name,), 0, vcl_size)
        knl = lp.tag_array_axes(knl, (vector_name,), ('c', 'vec'))

    return knl


def realize_tail(knl, inner_iname, outer_iname, outer_bound, tail_iname, vcl_size, level):
    tail_size = get_form_option('number_of_blocks') % vcl_size
    new_dom = BasicSet("{{ [{0}] : 0<={0}<{1} }}".format(tail_iname, tail_size))

    insns_to_duplicate = lp.find_instructions(knl, Iname(inner_iname))
    ids_to_duplicate = tuple((insn.id for insn in insns_to_duplicate))

    subst_map = dict([(outer_iname, outer_bound // vcl_size),
                      (inner_iname, prim.Variable(tail_iname))])

    temporaries_to_duplicate = dict()
    for insn in insns_to_duplicate:
        if isinstance(insn, lp.Assignment):
            assignee = insn.assignee
            name = get_pymbolic_basename(assignee)
            if name in knl.temporary_variables:
                new_name = name + '_tail'
                temporaries_to_duplicate[new_name] = knl.temporary_variables[name].copy(name=new_name)
                subst_map[name] = prim.Variable(new_name)

    new_insns = []
    for insn in insns_to_duplicate:
        new_insn = insn.with_transformed_expressions(lambda e: substitute(e, subst_map))
        new_depends_on = frozenset((insn_id + '_tail' if insn_id in ids_to_duplicate else insn_id
                                    for insn_id in insn.depends_on))
        new_within_inames = frozenset((iname + '_tail' if iname == inner_iname else iname
                                       for iname in insn.within_inames)) - frozenset({outer_iname})
        new_insns.append(new_insn.copy(id=insn.id + '_tail', depends_on=new_depends_on,
                                       within_inames=new_within_inames,
                                       tags=insn.tags | frozenset({'tail_{}'.format(level)})))

    knl = knl.copy(domains=knl.domains + [new_dom], instructions=knl.instructions + new_insns,
                   temporary_variables=dict(**knl.temporary_variables, **temporaries_to_duplicate))

    common_inames = knl.all_inames()
    for insn in new_insns:
        common_inames = common_inames & (insn.within_inames | insn.reduction_inames())

    if get_form_option('vectorization_blockstructured_tail_ordering') == 'blocked':
        # TODO need to be more clever to get the right inames
        macro_inames = frozenset((iname + '_0' * level) for iname in sub_element_inames())
        common_inames = common_inames - macro_inames

    additional_inames_to_duplicate = frozenset()
    for insn in new_insns:
        insn_inames = insn.within_inames | insn.reduction_inames()
        additional_inames_to_duplicate = additional_inames_to_duplicate | (insn_inames - common_inames)

    knl = lp.duplicate_inames(knl, tuple(additional_inames_to_duplicate),
                              Or(tuple((Id(insn.id) for insn in new_insns))))

    return lp.make_reduction_inames_unique(knl)


def do_vectorization(knl, orig_iname, vec_iname, iname_bound, vcl_size, level=0):
    inner_iname = vec_iname + '_inner'
    outer_iname = vec_iname + '_outer'

    tail_size = iname_bound % vcl_size
    if get_form_option('vectorization_blockstructured_tail'):
        tail_vcl_size = vcl_size
        while tail_vcl_size > tail_size:
            tail_vcl_size = tail_vcl_size // 2
        vectorize_tail = tail_vcl_size > 1
    else:
        vectorize_tail = False

    # manually add tail, since split_iname with slabs tries to vectorize the tail
    if tail_size > 0:
        # fake suitable loop bound
        vectorizable_bound = (iname_bound // vcl_size) * vcl_size
        from loopy.kernel.tools import DomainChanger
        domch = DomainChanger(knl, (vec_iname,))
        knl = knl.copy(domains=domch.get_domains_with(
            BasicSet('{{ [{0}]: 0<={0}<{1} }}'.format(vec_iname, vectorizable_bound))))

        knl = lp.split_iname(knl, vec_iname, vcl_size, outer_iname=outer_iname, inner_iname=inner_iname)

        tail_iname = vec_iname + '_inner' + '_tail'
        knl = realize_tail(knl, inner_iname, outer_iname, iname_bound, tail_iname, vcl_size, level)
    else:
        knl = lp.split_iname(knl, vec_iname, vcl_size)

    knl = lp.tag_inames(knl, [(inner_iname, 'vec')])

    array_alias = [a for a in knl.arg_dict.keys() if a.endswith('alias') or a.endswith('tail')]
    knl = lp.split_array_axis(knl, array_alias, level, vcl_size)

    knl = add_vcl_temporaries(knl, vcl_size)
    knl = add_vcl_iname_array(knl, orig_iname, inner_iname, vcl_size, level)
    knl = add_vcl_accum_insns(knl, inner_iname, outer_iname, vcl_size, level)
    knl = add_vcl_access(knl, inner_iname, vcl_size, level)

    if tail_size > 0:
        knl = lp.add_dependency(knl, And((Tagged('tail_{}'.format(level)), Not(Tagged('head*')))),
                                Tagged('vectorized_{}'.format(level)))
        if vectorize_tail:
            knl = do_vectorization(knl, orig_iname, tail_iname, tail_size, tail_vcl_size, level + 1)

    return knl


def vectorize_micro_elements(knl):
    vec_iname = "subel_x"
    orig_iname = vec_iname
    if vec_iname in knl.all_inames() and get_global_context_value('integral_type') == 'cell':
        vcl_size = get_vcl_type_size(np.float64)
        knl = add_iname_array(knl, vec_iname)

        knl = do_vectorization(knl, orig_iname, orig_iname, get_form_option('number_of_blocks'), vcl_size)
    return knl
