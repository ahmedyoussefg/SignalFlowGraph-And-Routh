import sympy as sp

""" standardize the dictionary in form of powers of s
    s**4  s**3  s**2  s**1  s**0 """
def normalize_dict(dict):
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

""" finding determinant of the matrix 
    not handeling the zero division error or all zero row ..(simple case) """
def fill_routh_array(matrix):
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

def main():
    x = sp.symbols('s')
    # sample input
    e= sp.sympify("48*s**2 + 24*s**3 - 25*s + 2*s**4 + 1*s**5 -50")
    print(sp.latex(e))
    dict = e.as_coefficients_dict()
    new_dict = normalize_dict(dict)
    # checking the powers and signs
    if not check_powers(new_dict.keys()):
        print("System is Unstable: Missing powers of s.")
        print("Finding the number of roots.")
        print("________________________________________")
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
        print("System is Stable.")
    else:
        print("System is Unstable and has {} roots in the positive side of the S-plane.".format(stability))

if __name__ == "__main__":
    main()

