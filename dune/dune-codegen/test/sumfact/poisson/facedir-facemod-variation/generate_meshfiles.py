"""This program can be used to generate the 36 msh files. It is not integrated
into the build system and needs to be called by hand.

"""

c0_0 = [2,1,7,8,5,4,10,11]
c0_1 = [1,2,5,4,7,8,11,10]
c0_2 = [2,5,4,1,8,11,10,7]
c0_3 = [1,7,8,2,4,10,11,5]
c0_4 = [2,8,11,5,1,7,10,4]
c0_5 = [1,4,10,7,2,5,11,8]

c1_0 = [2,3,6,5,8,9,12,11]
c1_1 = [3,2,8,9,6,5,11,12]
c1_2 = [2,8,9,3,5,11,12,6]
c1_3 = [3,6,5,2,9,12,11,8]
c1_4 = [2,5,11,8,3,6,12,9]
c1_5 = [3,9,12,6,2,8,11,5]

c0s = [c0_0, c0_1, c0_2, c0_3, c0_4, c0_5]
c1s = [c1_0, c1_1, c1_2, c1_3, c1_4, c1_5]

begin_structured = """$MeshFormat
2.0 0 8
$EndMeshFormat
$Nodes
12
1 0 0 0
2 1 0 0
3 2 0 0
4 0 1 0
5 1 1 0
6 2 1 0
7 0 0 1
8 1 0 1
9 2 0 1
10 0 1 1
11 1 1 1
12 2 1 1
$EndNodes
$Elements
2
"""

begin_affine = """$MeshFormat
2.0 0 8
$EndMeshFormat
$Nodes
12
1 0.5 0 0
2 1 1 1
3 1.5 2 2
4 0 1 0
5 0.5 2 1
6 1 3 2
7 0 -1 1
8 0.5 0 2
9 1 1 3
10 -0.5 0 1
11 0 1 2
12 0.5 2 3
$EndNodes
$Elements
2
"""

begin_unstructured = """$MeshFormat
2.0 0 8
$EndMeshFormat
$Nodes
12
1 -0.5 0 -1
2 1.2 1.1 1.1
3 1.5 2 1.5
4 -0.5 1.5 -0.5
5 0.5 2 1
6 1 3 2
7 0 -1 1.5
8 0.4 -0.1 1.8
9 1 1 3
10 -0.7 0.2 1.2
11 0.1 1.3 2.2
12 0.5 2.2 3.5
$EndNodes
$Elements
2
"""


end = """
$EndElements
"""


def generate_files(name, begin):
    from itertools import product
    for i, c in enumerate(product(c0s, c1s)):
        with open('{}_{}.msh'.format(name, str(i).zfill(2)), 'w+') as f:
            f.write(begin)
            f.write('1 5 0')
            for a in c[0]:
                f.write(' {}'.format(a))
            f.write('\n')
            f.write('2 5 0')
            for a in c[1]:
                f.write(' {}'.format(a))

            f.write(end)


# generate_files("grid_structure", begin_structured)
# generate_files("grid_affine", begin_affine)
generate_files("grid_unstructured", begin_unstructured)
