# dune-course-material


这是DUNE的课程的一部分，是专门从虚拟机从抽离出来的。
https://heibox.uni-heidelberg.de/d/1860f3cd05d84a20b3b1/

目的:为了让其能够适应于不同的编译环境。

测试通过环境：
✅ubuntu-18.04
✅apple m1-arm64

其他环境(比如windows)安装的问题，未考虑到的
如果遇到问题，请及时反馈： 
上传issues或联系QQ 3390579731


修复(改进)的一些问题：
- 打包操作：tar -zcvf iwr-course-2021.tar.gz iwr-course-2021
- 额外安装包：sudo apt install libsuperlu-dev/brew install superlu  ---> in order to use:  Dune::PDELab::ISTLBackend_SEQ_SuperLU in tuturial09
- 文档生成条件：install Latex for new-made doc
- codegen-m1: change tsc file: rdtsc-->chrono
- 为生成tutorial09-pdf: brew install pygments 
- latex文档：\usepackage{scrpage2}--》\usepackage{scrlayer-scrpage}



