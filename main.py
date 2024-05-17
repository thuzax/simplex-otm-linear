from Simplex import Simplex
from standard_form_conversor import convert_to_standard_form

def call_simplex(A, b, c, operators):
    standard_A, standard_c = convert_to_standard_form(A, operators, c)
    model = Simplex()
    model.optimize(standard_A, b, standard_c)
    model.print_solution()



if __name__=="__main__":

    print("########")
    # Infeasible
    A = [
        [0, 1],
        [1, 1],
        [1, 0],
        [5, 1]
    ]
    operators = ["<", ">", "<", "<"]
    b = [-1, -1, -1, -1]
    c = [-1, -3]

    call_simplex(A, b, c, operators)

    print("########")

    # Unlimited
    A = [
        [1, -1],
        [-1, 1]
    ]
    operators = ["<", "<"]
    b = [4, 4]
    c = [-1, -1]

    call_simplex(A, b, c, operators)
    
    print("########")

    # Multiple Optimal
    A = [
        [1, 1],
        [1, -1],
        [-1, 1]
    ]

    operators = ["<", "<", "<"]

    b = [6, 4, 4]
    c = [-1, -1]

    call_simplex(A, b, c, operators)

    print("########")

    # Optimal
    # A = [
    #     [-3, 1, 1, 0, 0, 0],
    #     [0, 1, 0, 1, 0, 0],
    #     [1, 2, 0, 0, 1, 0],
    #     [3, 1, 0, 0, 0, 1]
    # ]
    A = [
        [-3, 1],
        [0, 1],
        [1, 2],
        [3, 1]
    ]
    operators = ["<", "<", "<", "<"]
    b = [2, 3, 9, 18]
    c = [-1, -1, 0, 0, 0, 0]

    call_simplex(A, b, c, operators)
