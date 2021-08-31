// Gmsh project created on Tue Oct 23 11:21:07 2018
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 0.23};
//+
Point(2) = {0, 1, 0, 0.23};
//+
Point(3) = {1, 1, 0, 0.23};
//+
Point(4) = {1, 0, 0, 0.23};
//+
Line(1) = {1, 4};
//+
Line(2) = {4, 3};
//+
Line(3) = {3, 2};
//+
Line(4) = {2, 1};
//+
Line Loop(1) = {3, 4, 1, 2};
//+
Plane Surface(1) = {1};
//+
Recombine Surface {1};
//+
Extrude {0, 0, 1} {
  Surface{1}; Layers{5}; Recombine;
}
