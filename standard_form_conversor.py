from import_or_install_package import install_package
from import_or_install_package import verify_package_installed
if verify_package_installed("numpy"):
    import numpy
else:
    install_package("numpy")
    import numpy

def convert_to_min(problem_type, c):
    if (problem_type.upper() == "MAX"):
        return (numpy.array(c) * -1).tolist()
    return c

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


