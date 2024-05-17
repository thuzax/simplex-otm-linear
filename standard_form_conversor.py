import numpy


def get_slack_sign(operator):
    if (operator == "<" or operator == "<="):
        return 1
    elif(operator == ">" or operator == ">="):
        return -1
    else:
        return 0

def convert_to_standard_form(A, operators, c):
    new_A = numpy.copy(A)
    new_c = numpy.copy(c).tolist()
    for pos, operator in enumerate(operators):
        multiplier = get_slack_sign(operator)
        if (multiplier == 0):
            continue
        new_column = numpy.zeros((numpy.size(new_A, axis=0),1))
        new_column[pos, 0] = multiplier
        new_A = numpy.append(new_A, new_column, axis=1)
        new_c.append(0)
    
    return new_A, new_c


