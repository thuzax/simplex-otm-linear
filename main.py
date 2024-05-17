import sys
from Simplex import Simplex
from standard_form_conversor import convert_to_standard_form, convert_to_min
from file_reader import read_model_input

def call_simplex(problem_type, c, A, operators, b):
    min_c = convert_to_min(problem_type, c)
    standard_A, standard_c = convert_to_standard_form(A, operators, min_c)
    model = Simplex()
    model.optimize(standard_A, b, standard_c)
    model.print_solution()


def execute_from_file():
    if (len(sys.argv) < 2):
        print("Arquivo contendo o modelo de entrada não informado")
        print("Leia o README.md para mais informações")
        exit(0)

    problem_type, c, A, operators, b = read_model_input(sys.argv[1])
    call_simplex(problem_type, c, A, operators, b)


if __name__=="__main__":
    execute_from_file()
    exit(0)
