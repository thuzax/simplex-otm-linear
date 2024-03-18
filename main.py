from Simplex import Simplex

if __name__=="__main__":
    A = [
        [1, 1, 1, 0, 0],
        [1, -1, 0, 1, 0],
        [-1, 1, 0, 0, 1]
    ]
    b = [6, 4, 4]
    c = [-1, -2, 0, 0, 0]

    m = Simplex()
    m.optimize(A, b, c)