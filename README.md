# dune-course-material


这是[DUNE的课程](https://heibox.uni-heidelberg.de/d/1860f3cd05d84a20b3b1/)的一部分，是专门从虚拟机中抽离出来的。


目的: 为了让其能够适应于不同的编译环境, 帮助避坑。

运行`./install.sh`进行安装

测试通过环境：

✅ubuntu-18.04

✅apple m1-arm64

其他环境(比如windows)安装的问题，未考虑到的
如果遇到问题，请及时反馈： 
上传issues或联系QQ 3390579731

额外可选安装包：pygments、superlu(for 案例09)，latex、LatexMk（for doc）

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
- codegen-m1: change tsc file: rdtsc-->chrono 
- latex文档：\usepackage{scrpage2}--》\usepackage{scrlayer-scrpage}



