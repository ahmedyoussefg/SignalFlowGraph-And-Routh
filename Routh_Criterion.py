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
    # getting the list of powers
    list = []
    for pow in powers:
        list.append(int(pow[-1]))
    # checking the existance of all powers in the list
    if len(list) == max(list) + 1:
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
            if positive > 0:
                return False
        elif int(coeff) > 0:
            positive += 1
            if negative > 0:
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
    for i in range(2, n):
        for j in range(0, len(matrix[0])-1):
            matrix[i][j] = (matrix[i-1][0]*matrix[i-2][j+1] - matrix[i-2][0]*matrix[i-1][j+1]) / matrix[i-1][0]
    
    return matrix
     
def main():
    x = sp.symbols('s')
    # sample input
    e= sp.sympify("3*s**2 + 1*s**4 + 2*s**3 + 4*s + 5")
    print(e)  
    dict = e.as_coefficients_dict()
    new_dict = normalize_dict(dict)
    
    # checking the powers and signs
    if not check_powers(new_dict.keys()):
        print("Error: Missing powers")
        return
    if not check_signs(new_dict.values()):
        print("Error: Sign change in coefficients")
        return
    
    matrix = construct_routh_array(new_dict)
    print(matrix)
    print(fill_routh_array(matrix))
    
      
if __name__ == "__main__":
    main()

