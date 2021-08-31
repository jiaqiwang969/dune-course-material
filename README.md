# dune-course-material


这是[DUNE的课程](https://heibox.uni-heidelberg.de/d/1860f3cd05d84a20b3b1/)的一部分，是专门从虚拟机从抽离出来的。


目的: 为了让其能够适应于不同的编译环境, 帮助避坑。

测试通过环境：

✅ubuntu-18.04

✅apple m1-arm64

其他环境(比如windows)安装的问题，未考虑到的
如果遇到问题，请及时反馈： 
上传issues或联系QQ 3390579731

额外可选安装包：superlu(for 案例09)，latex、LatexMk（for doc）

以下暂未测试：
 * dune-python
 * Inkscape, converts SVG images, <www.inkscape.org>
   To generate the documentation with LaTeX
 * TBB, Threading Building Blocks library
   Parallel programming on multi-core processors
 * Vc, C++ Vectorization library, <https://github.com/VcDevel/Vc>
   For use of SIMD instructions
 * Alberta
 * Psurface
 * AmiraMesh
 * ParMETIS
 * ZLIB
 * SIONlib
 * DLMalloc
 * PTScotch
 * ZOLTAN
 * METIS
 * PETSc
 * Eigen3

修复(改进)的一些问题：
- 打包操作：tar -zcvf iwr-course-2021.tar.gz iwr-course-2021
- 额外安装：sudo apt install libsuperlu-dev/brew install superlu  ---> in order to use:  Dune::PDELab::ISTLBackend_SEQ_SuperLU in tuturial09
- 文档生成条件：install Latex for new-made doc
- codegen-m1: change tsc file: rdtsc-->chrono 
- 为生成tutorial09-pdf: brew install pygments 
- latex文档：\usepackage{scrpage2}--》\usepackage{scrlayer-scrpage}



