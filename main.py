from Simplex import Simplex

def call_simplex(A, b, c):
    model = Simplex()
    model.optimize(A, b, c)
    model.print_solution()



if __name__=="__main__":
    print("########")
    # Infeasible
    A = [
        [0, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 0],
        [5, 1, 0, 0, 0, 1]
    ]
    b = [-1, -1, -1, -1]
    c = [-1, -3, 0, 0, 0, 0]

    call_simplex(A, b, c)

    print("########")

    # Unlimited
    A = [
        [1, -1, 1, 0],
        [-1, 1, 0, 1]
    ]
    b = [4, 4]
    c = [-1, -1, 0, 0]

    call_simplex(A, b, c)
    
    print("########")

    # Multiple Optimal
    A = [
        [1, 1, 1, 0, 0],
        [1, -1, 0, 1, 0],
        [-1, 1, 0, 0, 1]
    ]
    b = [6, 4, 4]
    c = [-1, -1, 0, 0, 0]

    call_simplex(A, b, c)

    print("########")

    # Optimal
    A = [
        [-3, 1, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [1, 2, 0, 0, 1, 0],
        [3, 1, 0, 0, 0, 1]
    ]
    b = [2, 3, 9, 18]
    c = [-1, -1, 0, 0, 0, 0]

    call_simplex(A, b, c)