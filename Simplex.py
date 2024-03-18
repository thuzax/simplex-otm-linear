import numpy

class Simplex:

    def __init__(self):
        self.optimal = None
        self.infeasible = None
        self.fo_infinity = None
        self.solution = None

        self.B = None
        self.xb = None
        self.N = None
        self.xn = None
        self.cb = None
        self.xn = None
        self.b = None
        self.objective = None
        self.it = 0

        self.B_A_indices = None
        self.N_A_indices = None

    def simplex_phase_one(self):

        append_matrix = []
        for i in range(len(self.A)):
            append_matrix.append(numpy.array([0 if j != i else 1 for j in range(len(self.A))]))

        self.B = numpy.array(append_matrix)
        self.N = numpy.copy(self.A)
        
        self.N_A_indices = [i for i in range(len(self.N.T))]
        self.B_A_indices = [i+len(self.N.T) for i in range(len(self.B.T))]

        self.artificial_costs = numpy.array([1.0]*len(append_matrix))
        self.xb = self.b[:len(append_matrix)]
        self.xn = numpy.array([0] * len(self.A[0]))

        self.cb = numpy.array([1.0] * len(append_matrix))
        self.cn = numpy.array([1.0] * len(self.A[0]))

        self.objective = numpy.matmul(self.cb.T, self.xb)

        self.simplex_phase_two()


    def simplex_phase_two(self):
        self.it = 0
        while True:
            B_inv = numpy.linalg.inv(self.B)
            # New solution
            self.xb = numpy.matmul(B_inv, self.b)
            self.xn = numpy.zeros(shape=len(self.N.T))

            # Simplex multiplier vector
            simplex_multipliers_T = (numpy.matmul(self.cb.T, B_inv))

            # reduced costs vector (improvement of each non-basic variable)
            cn_new = numpy.array([
                self.cn[j] - numpy.matmul(simplex_multipliers_T, self.N.T[j]) 
                for j in range(len(self.N.T))
            ])

            # Best improvement value
            cn_k = numpy.min(cn_new)
            # Position of the best improvement (same position of the variable that will go to the base)
            in_var = numpy.argmin(cn_new)

            # If cn_k >= 0 (if best improvement is >= 0), then optimal was found
            if (cn_k >= 0):
                self.optimal = True
                self.infeasible = False
                self.fo_infinity = False
                return
            
            # Otherwise, calculate simplex direction
            simplex_direction = numpy.matmul(B_inv, self.N.T[in_var])
            if (all(simplex_direction <= 0)):
                self.optimal = False
                self.infeasible = False
                self.fo_infinity = True
                return
            
            indices_decreasing_steps = numpy.where(simplex_direction > 0)[0]
            possible_step_sizes = numpy.array([self.xb[i] / simplex_direction[i] for i in indices_decreasing_steps])
            step_size = numpy.min(possible_step_sizes)
            out_var = indices_decreasing_steps[numpy.argmin(possible_step_sizes)]
            
            col_N = numpy.copy(self.N.T[in_var])
            col_B = numpy.copy(self.B.T[out_var])
            
            # print(B)
            # print(N)
            # print(cn_new)
            # print(in_var)
            # print(out_var)

            self.B[:, out_var] = col_N
            self.N[:, in_var] = col_B

            out_cost = self.cb[out_var]
            in_cost = self.cn[in_var]

            self.cn[in_var] = out_cost
            self.cb[out_var] = in_cost

            column_N = self.N_A_indices[in_var]
            column_B = self.B_A_indices[out_var]
            self.N_A_indices[in_var] = column_B
            self.B_A_indices[out_var] = column_N

            self.objective += (cn_k * step_size)
            self.it += 1


    # Input -> Standard Form
    # min transpose(c) * x 
    # s.a.: A*x = b
    def optimize(self, A_matrix, b_list, c_list):
        self.A = numpy.array(A_matrix)
        self.b = numpy.array(b_list)
        self.c = numpy.array(c_list)
        negative_b_positions = numpy.where(self.b < 0)
        for i in negative_b_positions:
            self.A[i] = self.A[i] * (-1)
            self.b[i] = self.b[i] * (-1)
        
        self.simplex_phase_one()

        print(self.N_A_indices)

        self.xn = numpy.zeros(len(self.A.T)-len(self.A))
        self.N = numpy.zeros(shape=(len(self.A), len(self.A.T)-len(self.A)))
        self.cn = numpy.zeros(len(self.A.T)-len(self.A))

        self.N_A_indices = numpy.delete(self.N_A_indices, numpy.where([i >= len(self.A.T) for i in self.N_A_indices]))
        
        k = 0
        for i in self.N_A_indices:
            self.N[:, k] = numpy.copy(self.A.T[i])
            self.cn[k] = numpy.copy(self.c[i])
            k += 1
        
        k = 0
        for i in self.B_A_indices:
            self.B[:, k] = numpy.copy(self.A.T[i])
            self.cb[k] = numpy.copy(self.c[i])
            k += 1

        print("--")
        print(self.cb.T, self.xb)
        self.objective = numpy.matmul(self.cb.T, self.xb)


        print(self.xb)
        print(self.xn)
        print(self.B)
        print(self.N)
        print(self.cb)
        print(self.cn)
        print(self.objective)

        print("--")

        self.simplex_phase_two()

        print(self.B)
        print(self.N)
        print(self.xb)
        print(self.xn)
        print(self.objective)



