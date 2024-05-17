from file_reader import read_model_input
from main import call_simplex

if __name__=="__main__":
    
    print("#" * 35 + " EXEMPLO 1 " + "#" * 34)
    data = read_model_input("exemplos/exemplo_1.txt")
    problem_type, c, A, operators, b = data
    call_simplex(problem_type, c, A, operators, b)    
    print("#" * 80 + "\n\n")

    print("#" * 35 + " EXEMPLO 2 " + "#" * 34)
    data =read_model_input("exemplos/exemplo_2_infactivel.txt")
    problem_type, c, A, operators, b = data
    call_simplex(problem_type, c, A, operators, b)    
    print("#" * 80 + "\n\n")

    print("#" * 35 + " EXEMPLO 3 " + "#" * 34)
    data =read_model_input("exemplos/exemplo_3_ilimitada.txt")
    problem_type, c, A, operators, b = data
    call_simplex(problem_type, c, A, operators, b)    
    print("#" * 80 + "\n\n")

    print("#" * 35 + " EXEMPLO 4 " + "#" * 34)
    data =read_model_input("exemplos/exemplo_4.txt")
    problem_type, c, A, operators, b = data
    call_simplex(problem_type, c, A, operators, b)    
    print("#" * 80 + "\n\n")

    print("#" * 35 + " EXEMPLO 5 " + "#" * 34)
    data =read_model_input("exemplos/exemplo_5.txt")
    problem_type, c, A, operators, b = data
    call_simplex(problem_type, c, A, operators, b)
    print("#" * 80 + "\n\n")
    