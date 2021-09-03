\documentclass[ignorenonframetext,11pt]{scrartcl}
\usepackage{beamerarticle}
\usepackage{scrlayer-scrpage}
\pagestyle{scrheadings}

\usepackage{graphicx}
\graphicspath{{../slides/figures/}}

\usepackage{hyperref}
\usepackage{listings}
\lstset{language=C++, basicstyle=\small\ttfamily,
  keywordstyle=\bfseries, tabsize=4, stringstyle=\ttfamily,morekeywords={decltype},
  commentstyle=\itshape, extendedchars=true, escapeinside={/*@}{@*/},inputpath=../slides/src_samples}
\def\inline{\lstinline[basicstyle=\ttfamily]}

\input{../slides/c++slides_content}
