import numpy

class Simplex:

    def __init__(self):
        # Solution status
        self.optimal = None
        self.infeasible = None
        self.unlimited = None
        self.degenerated = None

        # Solution variables values
        self.solution = None

        # Basic Matrix
        self.B = None
        # Basic variables values
        self.xb = None
        # Basic variables related costs
        self.cb = None
        # Non-basic matrix
        self.N = None
        self.objective = None
        # Constants vector
        self.b = None
        # Number of iterations
        self.it = 0

        # Mapping of basic matrix columns
        self.B_A_indices = None
        # Mapping of non-basic matrix columns
        self.N_A_indices = None


    def simplex_phase_one(self):
        # Initialize artificial matrix as an mxm identity matrix
        artificial_matrix = []
        for i in range(len(self.A)):
            artificial_matrix.append(
                numpy.array([
                    0 if j != i else 1 
                    for j in range(len(self.A))
                ])
            )

        # Define basic matrix as artificial matrix
        self.B = numpy.array(artificial_matrix)
        # Define non-basic matrix as input A matrix
        self.N = numpy.copy(self.A)
        
        # Map the column indices of basic and non-basic matrix
        # Artificial columns indices starts at n+1
        self.B_A_indices = [i+len(self.N.T) for i in range(len(self.B.T))]
        self.N_A_indices = [i for i in range(len(self.N.T))]

        # Define cb as 1, since they are the artificial variables costs
        self.cb = numpy.array([1.0] * len(artificial_matrix))
        # Define cn as 0, since they are the original variables costs
        self.cn = numpy.array([0.0] * len(self.A[0]))

        # Since B is an identity, the solution is b
        self.xb = numpy.copy(self.b)

        # Calculate objective
        self.objective = numpy.sum(numpy.matmul(self.cb.T, self.xb))

        # Solve artificial problem
        self.simplex_phase_two()

        # Search for the indices of the artificial variables  on basic matrix
        artificial_vars_in_solution = numpy.where([
            i >= len(self.A.T) 
            for i in self.B_A_indices
        ])[0]

        # If there is any artificial variable in the solution
        # the problem is infeasible
        if (len(artificial_vars_in_solution) > 0):
            self.optimal = False
            self.unlimited = False
            self.infeasible = True
            return


    def simplex_phase_two(self):
        
        # print("Matriz basica:")
        # print(self.B)
        # print("Vetor de custos básicos:")
        # print(self.cb)
        # print("Mapa de indices das colunas básicas:")
        # print(self.B_A_indices)
        # print("Matriz não basica:")
        # print(self.N)
        # print("Vetor de custos não básicos:")
        # print(self.cn)
        # print("Mapa de indices das colunas não básicas:")
        # print(self.N_A_indices)
        # print("Valor F.O.:")
        # print(self.objective)

        self.it = 0
        while True:
            # print("*********************************************************")
            B_inv = numpy.linalg.inv(self.B)
            # New solution
            self.xb = numpy.matmul(B_inv, self.b)
            
            # print(Valor variáveis básicas:)
            # print(self.xb)

            # Simplex multiplier vector
            simplex_multipliers_T = (numpy.matmul(self.cb.T, B_inv))
            
            # reduced costs vector (improvement of each non-basic variable)
            cn_new = numpy.array([
                self.cn[j] - numpy.matmul(simplex_multipliers_T, self.N.T[j]) 
                for j in range(len(self.N.T))
            ])

            # Best improvement value
            cn_k = numpy.min(cn_new)
            
            # Position of the best improvement 
            # (same position of the variable that will go to the base)
            in_var = numpy.argmin(cn_new)

            # If cn_k >= 0 (if best improvement is >= 0), 
            # then optimal was found
            if (cn_k >= 0):
                self.optimal = True
                self.infeasible = False
                self.unlimited = False
                return
            
            # Otherwise, calculate simplex direction
            simplex_direction = numpy.matmul(B_inv, self.N.T[in_var])
            if (all(simplex_direction <= 0)):
                self.optimal = False
                self.infeasible = False
                self.unlimited = True
                return
            
            # Steps sizes calculation (epslon)
            indices_decreasing_steps = numpy.where(simplex_direction > 0)[0]
            possible_step_sizes = numpy.array([
                self.xb[i] / simplex_direction[i] 
                for i in indices_decreasing_steps
            ])

            # Simplex step size (minimun)
            step_size = numpy.min(possible_step_sizes)
            out_var = indices_decreasing_steps[
                numpy.argmin(possible_step_sizes)
            ]
            
            # Basic and Non-Basic columns swap
            col_N = numpy.copy(self.N.T[in_var])
            col_B = numpy.copy(self.B.T[out_var])
            
            self.B[:, out_var] = col_N
            self.N[:, in_var] = col_B

            # Basic and Non-Basic costs update
            out_cost = self.cb[out_var]
            in_cost = self.cn[in_var]

            self.cn[in_var] = out_cost
            self.cb[out_var] = in_cost

            # Basic and Non-Basic mapping update
            column_N = self.N_A_indices[in_var]
            column_B = self.B_A_indices[out_var]
            self.N_A_indices[in_var] = column_B
            self.B_A_indices[out_var] = column_N

            # Objective Function update
            self.objective += (cn_k * step_size)

            # print(
            #     "entra coluna " + str(column_N) + 
            #     ", sai coluna " + str(column_B)
            # )
           
            # print("Matriz basica:")
            # print(self.B)
            # print("Vetor de custos básicos:")
            # print(self.cb)
            # print("Mapa de indices das colunas básicas:")
            # print(self.B_A_indices)
            # print("Matriz não basica:")
            # print(self.N)
            # print("Vetor de custos não básicos:")
            # print(self.cn)
            # print("Mapa de indices das colunas não básicas:")
            # print(self.N_A_indices)
            # print("Valor F.O.:")
            # print(self.objective)

            self.it += 1


    # Input -> Standard Form
    # min transpose(c) * x 
    # s.a.: A*x = b
    def optimize(self, A_matrix, b_list, c_list):
        # Make a numpy array from inputs
        self.A = numpy.array(A_matrix)
        self.b = numpy.array(b_list)
        self.c = numpy.array(c_list)
        
        # If there is a negative value in b,
        # make it positive by multiplying its line
        # (this is needed for simplex phase 1)
        negative_b_positions = numpy.where(self.b < 0)
        for i in negative_b_positions:
            self.A[i] = self.A[i] * (-1)
            self.b[i] = self.b[i] * (-1)        

        # Call simplex phase 1 to find a starting basic matrix
        self.simplex_phase_one()

        # If the problem was found infeasible, stops
        if (self.infeasible):
            return False
        
        # Reset Non-Basic matrix and costs
        self.N = numpy.zeros(shape=(len(self.A), len(self.A.T)-len(self.A)))
        self.cn = numpy.zeros(len(self.A.T)-len(self.A))

        # Get the A columns indices that should be on Non-Basic matrix
        self.N_A_indices = numpy.delete(
            self.N_A_indices, numpy.where([
                i >= len(self.A.T) 
                for i in self.N_A_indices
            ])
        )

        # Assign Non-Basic matrix columns
        k = 0
        for i in self.N_A_indices:
            self.N[:, k] = numpy.copy(self.A.T[i])
            self.cn[k] = numpy.copy(self.c[i])
            k += 1
        
        # Assign the Basic matrix columns
        k = 0
        for i in self.B_A_indices:
            self.B[:, k] = numpy.copy(self.A.T[i])
            self.cb[k] = numpy.copy(self.c[i])
            k += 1

        # Calculate Objective Value
        self.objective = numpy.matmul(self.cb.T, self.xb)
        
        # Verify degeneracy
        self.degenerated = (any(self.xb == 0))

        # Solve the problem
        self.simplex_phase_two()

        # If the solution is unlimited, stops
        if (self.unlimited):
            return False

        # Make the solution variables vector
        self.solution = []
        self.solution = numpy.zeros(len(self.A.T))
        for i in range(len(self.xb)):
            if (self.xb[i] == 0):
                self.degenerated = True
            self.solution[self.B_A_indices[i]] = self.xb[i]
        

    def print_solution(self):
        # If optimal value is None, the algorithm was not executed
        if (self.optimal is None):
            print("O Simplex ainda não foi executado.")
            print("Utilize a função 'optimize'.")
            return
        
        # Otherwise, if optimal, prints the solution 
        # and indicates if it is degenerated
        if (self.optimal):
            text = "Solução ótima encontrada."
            if (self.degenerated):
                text += " A solução é degenerada."
            print(text)
            for i, value in enumerate(self.solution):
                print(
                    "X_" + str(i) + 
                    " = " + 
                    str(numpy.round(value, decimals=6))
                )
            print(numpy.round(self.objective, decimals=6))
            return
    
        # If the problem is infeasible it is printed
        if (self.infeasible):
            print("Solução infactível")
            return
        
        # If the problem is unlimited it is printed
        if (self.unlimited):
            print("Solução com função objetivo ilimitada.")
            return

