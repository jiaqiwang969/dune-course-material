from dune.codegen.error import CodegenCodegenError

from cgen import Generable, Block


class AccessModifier:
    PRIVATE = 1
    PUBLIC = 2
    PROTECTED = 3


def access_modifier_string(am):
    if am == AccessModifier.PRIVATE:
        return "private"
    if am == AccessModifier.PUBLIC:
        return "public"
    if am == AccessModifier.PROTECTED:
        return "protected"
    raise CodegenCodegenError("Unknown access modifier in class generation")


class BaseClass(Generable):
    def __init__(self, name, inheritance=AccessModifier.PUBLIC, construction=[]):
        self.name = name
        self.inheritance = inheritance
        self.construction = construction

        assert isinstance(name, str)
        for param in construction:
            assert isinstance(param, str)

    def generate(self):
        yield self.name


class ClassMember(Generable):
    def __init__(self, member, access=AccessModifier.PUBLIC, name=""):
        self.member = member
        self.access = access
        self.name = name

        if isinstance(member, str):
            from cgen import Line
            self.member = Line(member)
        else:
            from collections import Iterable
            assert all(isinstance(m, str) for m in self.member)

            from cgen import LiteralLines
            self.member = LiteralLines("\n" + "\n".join(self.member))

    def generate(self):
        yield "\n\n"
        yield "{}:\n".format(access_modifier_string(self.access))

        if isinstance(self.member, Generable):
            for line in self.member.generate():
                yield line + '\n'
        else:
            for generable in self.member:
                for line in generable.generate():
                    yield line + '\n'


class Class(Generable):
    """ Generator for a templated class """
    def __init__(self, name, base_classes=[], members=[], tparam_decls=[]):
        self.name = name
        self.base_classes = base_classes
        self.members = members
        self.tparam_decls = tparam_decls

        for bc in base_classes:
            assert isinstance(bc, BaseClass)
        for mem in members:
            assert isinstance(mem, Generable)

    def generate(self):
        # define the class header
        from cgen import Value
        decl = Value('class', self.name)

        if self.tparam_decls:
            yield 'template<'
            yield ', '.join('typename {}'.format(t) for t in self.tparam_decls)
            yield '>\n'

        # Yield the definition
        for line in decl.generate(with_semicolon=False):
            yield line

        yield '\n'

        # add base class inheritance
        if self.base_classes:
            yield "    : {} {}".format(access_modifier_string(self.base_classes[0].inheritance), self.base_classes[0].name)

            for bc in self.base_classes[1:]:
                yield ",\n"
                yield "      {} {}".format(access_modifier_string(bc.inheritance), bc.name)
            yield '\n'

        # Now yield the entire block
        block = Block(contents=self.members)

        # Yield the block
        for line in block.generate():
            yield line
        yield ";\n"
