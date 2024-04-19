import sympy as sp

def normalize_dict(dict):
    """Generates a modified dictionary for the coefficients of the characteristic eqn
    in the form: s**4  s**3  s**2  s**1  s**0"""
    modified_dict = {}
    while dict:
        item = dict.popitem()
        if item[0] == 1:
            modified_dict["s**0"] = item[1]
        elif str(item[0]) == 's':
            modified_dict["s**1"] = item[1]
        else:
            modified_dict[str(item[0])] = item[1]
    return modified_dict

# check the powers of the polynomial
def check_powers(powers):
    """Check whether all the powers exist or not
    NB: If the zero-th power doesn't exist it can't determine the result
    and needs further routh calculations."""
    # getting the p_list of powers
    p_list = []
    for pow in powers:
        p_list.append(int(pow[-1]))
    # checking the existance of all powers in the p_list
    if len(p_list) == max(p_list) + 1:
        return True
    if 0 not in p_list and len(p_list) == max(p_list):
        return True
    return False

# check the signs of the coefficients
def check_signs(coeffs):
    """Checks whether the characterstic coeffiecients have the same sign or nor"""
    negative = 0
    positive = 0
    # checking the sign of the coefficients
    for coeff in coeffs:
        if int(coeff) < 0:
            negative += 1
            if positive:
                return False
        elif int(coeff) > 0:
            positive += 1
            if negative:
                return False
    return True

# construct the routh array
def construct_routh_array(dict):
    """Initializes the Routh Array with the first 2 coefficienst Rows"""
    sorted_keys=sorted(dict.keys(),reverse=True)
    n = len(sorted_keys)
    m = n//2 + n%2
    x=0
    routh_array = [[0 for i in range(m)] for j in range(n)]
    
    for i in range(0, n, 2):
        routh_array[0][x] = dict.get(sorted_keys[i])
        x+=1
    x=0
    for i in range(1, n, 2):
        routh_array[1][x] = dict.get(sorted_keys[i])
        x+=1
        
    return routh_array

def fill_routh_array(matrix):
    """Calculates the routh array for a given coeffiecients matrix
    Exceptions:
        case 0 row: handled if the auxilliary equation is even-ordered
        case 0 in the first column: handled using 1e-10 instead of 0
    Returns:
        matrix: The new Routh Array
        state: state identifying whether there is an exception."""
    n = len(matrix)
    state = 1
    for i in range(2, n):
        for j in range(0, len(matrix[0])-1):
            try:
                if matrix[i-1][0] == 0:
                    raise ZeroDivisionError
                matrix[i][j] = (matrix[i-1][0]*matrix[i-2][j+1] - matrix[i-2][0]*matrix[i-1][j+1]) / matrix[i-1][0]
            except ZeroDivisionError:
                row = True
                for j in range(0, len(matrix[0]) - 1):
                    if matrix[i-1][j] != 0:
                        row = False
                if row:
                    state = -1
                    pow = n - (i - 2) - 1
                    if pow % 2 == 0:
                        for j in range(0, len(matrix[0])-1):
                            if pow >= 0:
                                matrix[i-1][j] = pow * matrix[i-2][j]
                                pow -= 2
                            matrix[i][j] = (matrix[i-1][0]*matrix[i-2][j+1] - matrix[i-2][0]*matrix[i-1][j+1]) / matrix[i-1][0]
                    else:
                        raise Exception("System can't be tested for stability: Odd-Ordered Auxiliary Equation")
                else:
                    state = 0
                    matrix[i-1][0] = 1e-10
                    for j in range(0, len(matrix[0]) - 1):
                        matrix[i][j] = (matrix[i-1][0]*matrix[i-2][j+1] - matrix[i-2][0]*matrix[i-1][j+1]) / matrix[i-1][0]
                    
    return matrix, state

def check_stability(matrix):
    """Checks whether the system is stable after conducting the Routh Array"""
    n = len(matrix)
    sign_change = 0
    pos = True
    for i in range(0, n):
        if matrix[i][0] > 0 and not pos:
            pos = True
            sign_change += 1
        elif matrix[i][0] < 0 and pos:
            pos = False
            sign_change += 1
    return sign_change        


def parse_sympy_equation():
    """Parse the input string into a sympy expression and 
    return the symbols used in the expression.
    Returns:
        parsed_expression: sympy expression
        symbols_dict: dictionary of symbols used in the expression
    """
    expression_str = input("Enter the Characteristic Equation in the form a*s**n + b*s**n-1 ... c*s**2 + d*s**1 + e(*s**0)\n")

    try:
        parsed_expression = sp.sympify(expression_str)

        symbols_used = parsed_expression.free_symbols
        symbols_dict = {str(symbol): symbol for symbol in symbols_used}

        return parsed_expression, symbols_dict

    except Exception as e:
        print("Error:", e)
        return None, None
    

def main():
    parsed_expression =  None
    while(not parsed_expression):
        parsed_expression, symbols_dict = parse_sympy_equation()
        if(not parsed_expression):
            print("Please enter a valid expression.")

    s = sp.symbols('s')
    substituted_expression = parsed_expression.subs(symbols_dict)
    print(sp.latex(substituted_expression))
    dict = substituted_expression.as_coefficients_dict()
    new_dict = normalize_dict(dict)
    # checking the powers and signs
    if not check_powers(new_dict.keys()):
        print("System is Unstable: Missing powers of s.")
        return
    if not check_signs(new_dict.values()):
        print("System is Unstable: Coefficients alternate signs.")
        print("Finding the number of roots.")
        print("________________________________________")

    matrix = construct_routh_array(new_dict)
    routh_matrix, state = fill_routh_array(matrix)
    stability = check_stability(routh_matrix)
    if(state == -1):
        print("System has a zero row in the Routh array ... Checking for Marginal Stability.")
    elif(state == 0):
        print("System has a zero division error in the Routh array.")
    else:
        print("System has no zero division error in the Routh array.")
    print("Final Matrix: ", routh_matrix)
    
    if(stability == 0):
        print("Stability Check: System is Stable.")
    else:
        print("Stability Check: System is Unstable and has {} roots in the positive side of the S-plane.".format(stability))

if __name__ == "__main__":
    main()