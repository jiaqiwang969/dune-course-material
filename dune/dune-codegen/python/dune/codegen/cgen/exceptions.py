""" Add Try/Catch blocks to cgen """

from cgen import Block, Generable, Value


class CatchBlock(Generable):
    def __init__(self, exc_decl, catch_block):
        assert isinstance(exc_decl, Value)
        self.exc_decl = exc_decl
        assert isinstance(catch_block, Block)
        self.catch_block = catch_block

    def generate(self):
        yield "catch ({})\n".format("".join(self.exc_decl.generate(with_semicolon=False)))
        for item in self.catch_block.generate():
            yield item
        yield "\n"


class TryCatchBlock(Generable):
    def __init__(self, try_block, catch_blocks):
        # Store the try block
        assert isinstance(try_block, Block)
        self.try_block = try_block

        assert all(isinstance(b, CatchBlock) for b in catch_blocks)
        self.catch_blocks = catch_blocks

    def generate(self):
        # Yield the try block
        yield "\n"
        yield "try\n"
        for item in self.try_block.generate():
            yield item
        yield "\n"

        # and now yield all the catch blocks
        for catch_block in self.catch_blocks:
            for item in catch_block.generate():
                yield item
