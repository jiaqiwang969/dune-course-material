import sys

sys.path.append('/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/scripts')

extensions = ['sphinx_cmake_dune']

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "classic"
html_theme_options = {
    "rightsidebar": "true",
    "relbarbgcolor": "#eeeeee",
    "relbartextcolor": "#353B44",
    "relbarlinkcolor": "#353B44",
    "headbgcolor": "white",
    "headtextcolor": "#353B44",
    "linkcolor": "#337AB7",
    "visitedlinkcolor": "#337AB7",
    "textcolor": "#353B44",
    "footerbgcolor": "white",
    "footertextcolor": "#353B44",
    "codebgcolor": "#eeeeee",
}

html_sidebars = {'**': []}
html_title = ""
