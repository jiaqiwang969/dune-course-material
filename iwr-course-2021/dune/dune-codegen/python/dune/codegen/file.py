""" Manages the generation of C++ header files """

from cgen import Generable, Include

from dune.codegen.generation import retrieve_cache_items


def generate_file(filename, tag, content, headerguard=True):
    """Write a file from the generation cache.

    Arguments:
    ----------
    filename: str
        The filename to write the generated code to.
    tag: str
        The tag, that all entries related to this file in the cache have.
    content: list
        A list of Generables to put into the file.

    Keyword Arguments:
    ------------------
    headerguard: bool
        Whether a double inclusion protection header should be added to the file.
        The name of the macro is mangled from the absolute path. Defaults to True.
    """
    with open(filename, 'w') as f:
        # Add a double inclusion protection header
        if headerguard:
            macro = filename.upper().replace("/", "_").replace(".", "_").replace("-", "_")
            f.write("#ifndef {0}\n#define {0}\n\n".format(macro))

        # Add pre include lines from the cache
        for define in retrieve_cache_items('{} and pre_include'.format(tag)):
            for line in define:
                f.write(line)
            f.write('\n')
        f.write('\n')

        # Add the includes from the cache
        for inc in retrieve_cache_items('{} and include'.format(tag)):
            assert isinstance(inc, Include)
            for line in inc.generate():
                f.write(line)
            f.write('\n')
        f.write('\n')

        # Add post include lines direclty after includes
        for define in retrieve_cache_items('{} and post_include'.format(tag)):
            for line in define:
                f.write(line)
            f.write('\n')

        f.write('\n\n')

        # Add main content
        for c in content:
            assert isinstance(c, Generable)
            for line in c.generate():
                f.write(line)
            f.write('\n\n')

        # Add end of file code
        for eof in retrieve_cache_items('{} and end_of_file'.format(tag)):
            for line in eof:
                f.write(line)

        # Close headerguard
        if headerguard:
            f.write("\n\n#endif //{}\n".format(macro))
