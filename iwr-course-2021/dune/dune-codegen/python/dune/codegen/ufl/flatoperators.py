""" A module that treats the problem of binary ufl operators """


def get_operands(expr, operator=None):
    """ Get the operators of the flattened operation in the expression """
    # If no operator is specified, it is the root of the expression
    if not operator:
        operator = type(expr)

    # We assume all operators to be binary
    assert len(expr.ufl_operands) == 2

    result = []
    for op in expr.ufl_operands:
        if isinstance(op, operator):
            result.extend(get_operands(op, operator))
        else:
            result.append(op)

    return result


def construct_binary_operator(operands, operator):
    if len(operands) == 1:
        return operands[0]
    if len(operands) == 2:
        return operator(operands[0], operands[1])
    else:
        mid = len(operands) // 2 + 1
        return operator(construct_binary_operator(operands[:mid], operator), construct_binary_operator(operands[mid:len(operands)], operator))
