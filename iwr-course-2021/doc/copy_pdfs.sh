#!/bin/bash

# Run this from the course root directory if you have build the course material with LATEX
# like: ./dpc/copy_pdfs.sh

cp $(find ./release-build/dune-pdelab-tutorials -name "*.pdf") doc

pushd doc
mv c++_doc_c++_refresher_tex_source.pdf c++_refresher.pdf
mv c++_exercise_doc_exercise_cpp1_tex_source.pdf c++_exercise.pdf
mv c++_slides_c++slides_tex_source.pdf c++_slides.pdf
mv gridinterface_exercise_doc_exercise_grid1_tex_source.pdf gridinterface_exercise.pdf
mv gridinterface_slides_slidesgrid_tex_source.pdf gridinterface_slides.pdf
mv overview_abstractions_tex_source.pdf overview_abstractions.pdf
mv overview_exercise-workflow_tex_source.pdf overview_exercise.pdf
mv overview_overview_tex_source.pdf overview.pdf
mv tutorial00_doc_tutorial00_tex_source.pdf tutorial00.pdf
mv tutorial00_exercise_doc_exercise00_tex_source.pdf tutorial00_exercise.pdf
mv tutorial00_slides_slides00_tex_source.pdf tutorial00_slides.pdf
mv tutorial01_doc_tutorial01_tex_source.pdf tutorial01.pdf
mv tutorial01_exercise_doc_exercise01_tex_source.pdf tutorial01_exercise.pdf
mv tutorial01_slides_slides01_tex_source.pdf tutorial01_slides.pdf
mv tutorial02_doc_tutorial02_tex_source.pdf tutorial02.pdf
mv tutorial02_slides_slides02_tex_source.pdf tutorial02_slides.pdf
mv tutorial03_doc_tutorial03_tex_source.pdf tutorial03.pdf
mv tutorial03_exercise_doc_exercise03_tex_source.pdf tutorial03_exercise.pdf
mv tutorial03_slides_slides03_tex_source.pdf tutorial03_slides.pdf
mv tutorial04_doc_tutorial04_tex_source.pdf tutorial04.pdf
mv tutorial04_exercise_doc_exercise04_tex_source.pdf tutorial04_exercise.pdf
mv tutorial04_slides_slides04_tex_source.pdf tutorial04_slides.pdf
mv tutorial05_doc_tutorial05_tex_source.pdf tutorial05.pdf
mv tutorial05_exercise_doc_exercise05_tex_source.pdf tutorial05_exercise.pdf
mv tutorial05_slides_slides05_tex_source.pdf tutorial05_slides.pdf
mv tutorial06_doc_tutorial06_tex_source.pdf tutorial06.pdf
mv tutorial06_exercise_doc_exercise06_tex_source.pdf tutorial06_exercise.pdf
mv tutorial06_slides_slides06_tex_source.pdf tutorial06_slides.pdf
mv tutorial07_doc_tutorial07_tex_source.pdf tutorial07.pdf
mv tutorial07_slides_slides07_tex_source.pdf tutorial07_slides.pdf
mv tutorial08_doc_tutorial08_tex_source.pdf tutorial08.pdf
mv tutorial09_exercise_doc_exercise09_tex_source.pdf tutorial09_exercise.pdf
mv tutorial09_slides_slides09_tex_source.pdf tutorial09_slides.pdf
mv workflow_exercise_doc_exercise_workflow_tex_source.pdf workflow_exercise.pdf
popd

git add doc/*.pdf
git commit -m "Update PDFs in doc"
