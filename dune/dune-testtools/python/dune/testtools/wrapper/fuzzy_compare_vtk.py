""" A module for fuzzy comparing VTK files.

This module provides methods to compare two VTK files. Applicable
for all VTK style formats like VTK files. Fuzzy compares numbers by
using absolute and/or relative difference comparison.

"""
from __future__ import absolute_import
import argparse
import xml.etree.ElementTree as ET
from operator import attrgetter, itemgetter
import sys
from six.moves import range
from six.moves import zip

from xml.etree.ElementTree import XMLParser, TreeBuilder
import struct
import base64
import re


class VTKTreeBuilder(TreeBuilder):
    """
    Sublass of TreeBuilder that decodes ASCII or base64-encoded VTK DataArrays.
    When the end-tag of a base64-encoded DataArray is encountered, the XML string
    is decoded and unpacked according to its data type and the VTK specification.
    Only strips whitespace for ASCII-encoded VTK.
    VTK specification found at http://www.vtk.org/Wiki/VTK_XML_Formats
    """

    # Buffer codes from https://docs.python.org/2/library/struct.html
    buffers = {"Int8": "b", "UInt8": "B", "Int16": "h", "UInt16": "H",
               "Int32": "i", "UInt32": "I", "Int64": "q", "UInt64": "Q",
               "Float32": "f", "Float64": "d"}
    byteorders = {"LittleEndian": "<", "BigEndian": ">"}

    def start(self, tag, attrib):
        self.elem = super(VTKTreeBuilder, self).start(tag, attrib)
        self.array_data = ""
        if tag == "VTKFile":
            try:
                self.split_header = attrib["version"] == "0.1"
            except KeyError:
                raise ValueError("Missing version attribute in VTKFile tag")
            try:
                self.byteorder = self.byteorders[attrib["byte_order"]]
            except KeyError:
                raise ValueError("Unknown byteorder {}".format(attrib["byte_order"]))
            try:
                self.header_type = self.buffers[attrib["header_type"]]
            except KeyError:  # default header in older VTK versions is UInt32
                self.header_type = "I"
        elif tag == "DataArray":
            if not attrib["format"] in ("binary", "ascii"):
                raise ValueError("VTK data format must be ascii or binary (base64). Got: {}".format(attrib["format"]))
        return self.elem

    def data(self, data):
        """
        Just record the data instead of writing it immediately. All data in VTK
        files is contained in DataArray tags, so no need to record anything if
        we are not currently in a DataArray.
        """
        if self.elem.tag == "DataArray":
            self.array_data += data

    def end(self, tag):
        """
        Detect the end-tag of a DataArray.
        """
        if tag != "DataArray":
            return super(VTKTreeBuilder, self).end(tag)

        # remove trailing whitespace
        self.array_data = re.sub(r"\s+", " ", "".join(self.array_data).strip())

        if self.elem.attrib["format"] == "binary":
            cbuf = self.buffers[self.elem.attrib["type"]]
            data = "".join(self.array_data)
            # binary encoded VTK files start with an integer giving the number of bytes to follow
            data_len = struct.unpack_from(self.byteorder + self.header_type, base64.b64decode(data))[0]
            if self.split_header:  # vtk version 0.1, encoding header and content separately
                header_size = len(base64.b64encode(struct.pack(self.byteorder + self.header_type, 0)))
                data_content = base64.b64decode(data[header_size:])
                byte_string = self.byteorder + cbuf * int(data_len / struct.calcsize(cbuf))
                data_unpacked = struct.unpack(byte_string, data_content)
            else:  # vtk version 1.0, encoding header and content together
                data_content = base64.b64decode(data)
                byte_string = self.byteorder + self.header_type + cbuf * int(data_len / struct.calcsize(cbuf))
                data_unpacked = struct.unpack(byte_string, data_content)[1:]
            assert data_len == len(data_unpacked) * struct.calcsize(cbuf)
            self.array_data = " ".join([str(v) for v in data_unpacked]).strip()

        # write data to element
        super(VTKTreeBuilder, self).data(self.array_data)
        return super(VTKTreeBuilder, self).end(tag)


# fuzzy compare VTK tree from VTK strings
def compare_vtk(vtk1, vtk2, absolute=1.2e-7, relative=1e-2, zeroValueThreshold={}, verbose=True):
    """ Take two vtk files and fuzzy compare them. Returns an exit key as return value.

    :param vtk1: The filename of the vtk files to compare
    :type vtk1: string
    :param vtk2: The filename of the vtk files to compare
    :type vtk2: string

    :param absolute: The epsilon used for comparing numbers with an absolute criterion
    :type absolute: float

    :param relative: The epsilon used for comparing numbers with an relative criterion
    :type relative: float

    :param zeroValueThreshold: A dictionary of parameter value pairs that set the threshold under
                               which a number is treated as zero for a certain parameter. Use this parameter if
                               you have to avoid comparisons of very small numbers for a certain parameter.
    :type zeroValueThreshold: dict

    :param verbose: If the script should produce informative output. Enabled by default as the details
                    give the tester a lot more information on why tests fail.
    :type verbose: bool
    """

    # construct element tree from vtk file
    root1 = ET.parse(vtk1, parser=XMLParser(target=VTKTreeBuilder())).getroot()
    root2 = ET.parse(vtk2, parser=XMLParser(target=VTKTreeBuilder())).getroot()

    # sort the vtk file in case nodes appear in different positions
    # e.g. because of minor changes in the output code
    sortedroot1 = sort_vtk(root1)
    sortedroot2 = sort_vtk(root2)

    if verbose:
        print("Comparing {} and {}".format(vtk1, vtk2))
        print("...with a maximum relative error of {} and a maximum absolute error of {}*p_max, where p_max is highest absolute parameter value.".format(relative, absolute))

    # sort the vtk file so that the comparison is independent of the
    # index numbering (coming e.g. from different grid managers)
    sortedroot1, sortedroot2 = sort_vtk_by_coordinates(sortedroot1, sortedroot2, verbose)

    # do the fuzzy compare
    if is_fuzzy_equal_node(sortedroot1, sortedroot2, absolute, relative, zeroValueThreshold, verbose):
        return 0
    else:
        return 1


# fuzzy compare of VTK nodes
def is_fuzzy_equal_node(node1, node2, absolute, relative, zeroValueThreshold, verbose):

    is_equal = True
    for node1child, node2child in zip(node1.iter(), node2.iter()):
        if node1.tag != node2.tag:
            if verbose:
                print('The name of the node differs in: {} and {}'.format(node1.tag, node2.tag))
                is_equal = False
            else:
                return False

        if len(list(node1.iter())) != len(list(node2.iter())):
            if verbose:
                print('Number of children differs in node: {}'.format(node1.tag))
                is_equal = False
            else:
                return False
        if node1child.text or node2child.text:
            if "NumberOfComponents" in node1child.attrib:
                    numComp = int(node1child.attrib["NumberOfComponents"])
            else:
                    numComp = 1
            if not is_fuzzy_equal_text(node1child.text, node2child.text,
                                       node1child.attrib["Name"],
                                       numComp,
                                       absolute, relative, zeroValueThreshold, verbose):
                if node1child.attrib["Name"] == node2child.attrib["Name"]:
                    if verbose:
                        print('Data differs in parameter: {}'.format(node1child.attrib["Name"]))
                        is_equal = False
                    else:
                        return False
                else:
                    if verbose:
                        print('Comparing different parameters: {} and {}'.format(node1child.attrib["Name"], node2child.attrib["Name"]))
                        is_equal = False
                    else:
                        return False
    return is_equal


# fuzzy compare of text (in the xml sense) consisting of whitespace separated numbers
def is_fuzzy_equal_text(text1, text2, parameter, numComp, absolute, relative, zeroValueThreshold, verbose):
    list1 = text1.split()
    list2 = text2.split()
    # difference only in whitespace?
    if (list1 == list2):
        return True
    # compare number by number
    is_equal = True

    # first split the list into compononents
    lists1 = []
    lists2 = []
    parameters = []
    for i in range(0, numComp):
        lists1.append(list1[i::numComp])
        lists2.append(list2[i::numComp])
        if numComp > 1:
            parameters.append("{}_{}".format(parameter, i))
            # if zero threshold was set for all components one component inherits it from the parameter
            if parameter in zeroValueThreshold:
                zeroValueThreshold["{}_{}".format(parameter, i)] = zeroValueThreshold[parameter]
        else:
            parameters.append(parameter)

    for list1, list2, parameter in zip(lists1, lists2, parameters):
        # for verbose output
        max_relative_difference = 0.0
        message = ''

        # see inspiration, explanations in
        # https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/
        # get the order of magnitude of the parameter by calculating the max
        floatList1 = [float(i) for i in list1]
        floatList2 = [float(i) for i in list2]

        # manipulate the data set for the sake of sensible comparison
        # if the parameter is listed in the zeroThreshold dictionary replace all float under threshold with zero.
        # only replace them with zero if the parameters in both lists are under the threshold. Otherwise we
        # compare a non-zero value with 0 later.
        if parameter in zeroValueThreshold:
            floatList1 = [0.0 if abs(i) < float(zeroValueThreshold[parameter]) and abs(j) < float(zeroValueThreshold[parameter])
                          else i for i, j in zip(floatList1, floatList2)]
            floatList2 = [0.0 if abs(i) < float(zeroValueThreshold[parameter]) and abs(j) < float(zeroValueThreshold[parameter])
                          else j for i, j in zip(floatList1, floatList2)]

        absFloatList1 = [abs(i) for i in floatList1]
        absFloatList2 = [abs(i) for i in floatList2]

        magnitude = max(max(absFloatList1), max(absFloatList2))
        minimal = min(min(absFloatList1), min(absFloatList2))

        for number1, number2 in zip(floatList1, floatList2):
            diff = abs(number1 - number2)
            largernumber = max(abs(number1), abs(number2))

            # If the absolute criterion is satisfied we consider the numbers equal...
            # scale the absolute tolerance with the magnitude of the parameter
            if diff <= absolute * magnitude:
                continue

            # ...if not check the relative criterion
            if diff <= largernumber * relative:
                continue
            else:
                # the numbers are not equal
                if verbose:
                    is_equal = False
                    if largernumber != 0.0:
                        if diff / largernumber > max_relative_difference:
                            message = 'Difference is too large between: {} and {}'.format(number1, number2)
                            max_relative_difference = diff / largernumber
                else:
                    return False

        if verbose and max_relative_difference != 0.0:
            print(message)
            print('Maximum relative difference for parameter {}: {:.2%}'.format(parameter, max_relative_difference))
            print('Info: The highest absolute value of {} is {} and the smallest {}.'.format(parameter, magnitude, minimal))
            if parameter in zeroValueThreshold:
                print('For parameter {} a zero value threshold of {} was given.'.format(parameter, zeroValueThreshold[parameter]))

    return is_equal


def sort_by_name(elem):
    name = elem.get('Name')
    if name:
        try:
            return str(name)
        except ValueError:
            return ''
    return ''


# sorts attributes of an item and returns a sorted item
def sort_attributes(item, sorteditem):
    attrkeys = sorted(item.keys())
    for key in attrkeys:
        sorteditem.set(key, item.get(key))


def sort_elements(items, newroot):
    items = sorted(items, key=sort_by_name)
    items = sorted(items, key=attrgetter('tag'))

    # Once sorted, we sort each of the items
    for item in items:
        # Create a new item to represent the sorted version
        # of the next item, and copy the tag name and contents
        newitem = ET.Element(item.tag)
        if item.text and item.text.isspace() is False:
            newitem.text = item.text

        # Copy the attributes (sorted by key) to the new item
        sort_attributes(item, newitem)

        # Copy the children of item (sorted) to the new item
        sort_elements(list(item), newitem)

        # Append this sorted item to the sorted root
        newroot.append(newitem)


# has to sort all Cell and Point Data after the attribute "Name"!
def sort_vtk(root):
    if(root.tag != "VTKFile"):
        print('Format is not a VTKFile. Sorting will most likely fail!')
    # create a new root for the sorted tree
    newroot = ET.Element(root.tag)
    # create the sorted copy
    # (after the idea of Dale Lane's xmldiff.py)
    sort_attributes(root, newroot)
    sort_elements(list(root), newroot)
    # return the sorted element tree
    return newroot


# sorts the data by point coordinates so that it is independent of index numbering
def sort_vtk_by_coordinates(root1, root2, verbose):
    if not is_fuzzy_equal_node(root1.find(".//Points/DataArray"), root2.find(".//Points/DataArray"), absolute=1e-2, relative=1.5e-7, zeroValueThreshold=dict(), verbose=False):
        if verbose:
            print("Sorting vtu by coordinates...")
        for root in [root1, root2]:
            # parse all DataArrays in a dictionary
            pointDataArrays = []
            cellDataArrays = []
            dataArrays = {}
            numberOfComponents = {}
            for dataArray in root.findall(".//PointData/DataArray"):
                pointDataArrays.append(dataArray.attrib["Name"])
            for dataArray in root.findall(".//CellData/DataArray"):
                cellDataArrays.append(dataArray.attrib["Name"])
            for dataArray in root.findall(".//DataArray"):
                dataArrays[dataArray.attrib["Name"]] = dataArray.text
                if "NumberOfComponents" in dataArray.attrib:
                    numberOfComponents[dataArray.attrib["Name"]] = int(dataArray.attrib["NumberOfComponents"])
                else:
                    numberOfComponents[dataArray.attrib["Name"]] = 1

            vertexArray = []
            coords = dataArrays["Coordinates"].split()
            # group the coordinates into coordinate tuples
            dim = numberOfComponents["Coordinates"]
            for i in range(len(coords) // dim):
                vertexArray.append([float(c) for c in coords[i * dim: i * dim + dim]])

            # obtain a vertex index map
            vMap = []
            for idx, coords in enumerate(vertexArray):
                vMap.append((idx, coords))
            sortedVMap = sorted(vMap, key=itemgetter(1))
            vertexIndexMap = {}
            for idxNew, idxOld in enumerate(sortedVMap):
                vertexIndexMap[idxOld[0]] = idxNew

            # group the cells into vertex index tuples
            cellArray = []
            offsets = dataArrays["offsets"].split()
            connectivity = dataArrays["connectivity"].split()
            vertexCounter = 0
            for cellIdx, offset in enumerate(offsets):
                cellArray.append([])
                for v in range(vertexCounter, int(offset)):
                    cellArray[cellIdx].append(int(connectivity[v]))
                vertexCounter += int(offset)

            # replace all vertex indices in the cellArray by the new indices
            for cellIdx, cell in enumerate(cellArray):
                for i, vertexIndex in enumerate(cell):
                    cell[i] = vertexIndexMap[vertexIndex]
                # sort the connectivity array
                # for the comparison we don't care about the local order of the vertices
                # in the connectivity array. As different grid manager might produce different
                # local orderings, i.e. flipped or permuted versions of the same element, we
                # just sort them in ascending order here to make them easy to compare
                cellArray[cellIdx] = sorted(cell)

            # sort all data arrays
            for name, text in list(dataArrays.items()):
                # split the text
                items = text.split()
                # convert if vector
                num = numberOfComponents[name]
                newitems = []
                for i in range(len(items) // num):
                    newitems.append([i for i in items[i * num: i * num + num]])
                items = newitems
                # sort the items: we have either vertex or cell data
                if name in pointDataArrays:
                    sortedItems = [j for (i, j) in sorted(zip(vertexArray, items), key=itemgetter(0))]
                elif name in cellDataArrays or name == "types":
                    sortedItems = [j for (i, j) in sorted(zip(cellArray, items), key=itemgetter(0))]
                elif name == "offsets":
                    sortedItems = []
                    counter = 0
                    for cell in sorted(cellArray):
                        counter += len(cell)
                        sortedItems.append([str(counter)])
                elif name == "Coordinates":
                    sortedItems = sorted(vertexArray)
                elif name == "connectivity":
                    sortedItems = sorted(cellArray)

                # convert the sorted arrays to a xml text
                dataArrays[name] = ""
                for i in sortedItems:
                    for j in i:
                        dataArrays[name] += str(j) + " "

            # do the replacement in the actual elements
            for dataArray in root.findall(".//DataArray"):
                dataArray.text = dataArrays[dataArray.attrib["Name"]]

    return (root1, root2)
