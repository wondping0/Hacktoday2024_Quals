import numpy as np

bound1 = 1295911241295070912759062510927419182371092570912740917209471290749986192846891264891628946189264982
bound2 = 9124789812750912709571902562640812649812640812640126508126408612084612856193641021290712049605126091
bound3 = 5275097124129650129640129471209719207491206751249012709217590109128390127490172599471092650192750500

def matrix_exponentiation(A, power, mod):
    result = np.identity(len(A), dtype=int)
    base = A.copy()
    
    while power:
        if power % 2:
            result = np.dot(result, base) % mod
        base = np.dot(base, base) % mod
        power //= 2
    
    return result

def eq1_eval(n, bound1, bound2):
    mod = bound1 * bound2
    
    # Matriks representasi untuk mengakomodasi jumlah deret dan suku konstan
    A = np.array([[1, 1, 0],
                  [0, 1, 1],
                  [0, 0, 1]], dtype=int)
    
    # Vektor awal
    F = np.array([0, 0, 2], dtype=int)
    
    # Hitung eksponensial matriks
    if n == 0:
        return F[0] % mod
    result_matrix = matrix_exponentiation(A, n, mod)
    
    # Hasil akhir
    result = np.dot(result_matrix, F) % mod
    
    return result[0]


def eq1(x):
    return x + 2
def eq2(x):
    return 3 * x**2 + x + 5
def eq3(x):
    return 69 * x**4 + 420 * (x + 69)**2 + 420 * x

def eq1_evals(n):
    ret = 0
    for x in range(1, n + 1):
        ret += eq1(x)
    return ret % (bound1 * bound2)


print(eq1_eval(100, bound1, bound2))
print(eq1_evals(100))
