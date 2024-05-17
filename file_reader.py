
def read_model_input(file_name):
    with open(file_name, "r") as input_file:
        text = input_file.read()

    lines = text.splitlines()
    
    problem_type = lines[0].strip().split()[0]
    n = int(lines[1].strip())
    m = int(lines[2].strip())
    
    c = [float(cost) for cost in lines[3].strip().split()]

    A = [
        [
            float(a)
            for a in lines[i].strip().split()
        ]
        for i in range(4, m+4)
    ]

    operators = [op for op in lines[m+4].strip().split()]

    b = [float(resource) for resource in lines[m+5].strip().split()]
    
    return (problem_type, c, A, operators, b)