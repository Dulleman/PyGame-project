def f_of_x(x, a, b, c, d):
    
    return a * x**3 + b * x**2 + c * x + d

def f_less_than_0(a, b, c, d):
    
    l = -1 

    if a > 0:

        while f_of_x(l, a, b, c, d) >= 0:
            l = l - 1
    else:

        while f_of_x(l, a, b, c, d) <= 0:
            l = l - 1

    return l

def f_bigger_than_0(a, b, c, d):

    r = 1 

    if a > 0:
        
        while f_of_x(r, a, b, c, d) <= 0:
            r = r + 1
    else:

        while f_of_x(r, a, b, c, d) >= 0:
            r = r + 1

    return r

def bisection_method(a, b, c, d, tolerance=0.001):

    a_val = f_less_than_0(a, b, c, d)
    b_val = f_bigger_than_0(a, b, c, d)

    while True:
        
        c_val = (a_val + b_val) / 2
        f_of_c = f_of_x(c_val, a, b, c, d)

        if abs(f_of_c) <= tolerance:
            
            return c_val

        f_a = f_of_x(a_val, a, b, c, d) 

        if f_a * f_of_c < 0:
            
            b_val = c_val
            
        else:
            
            a_val = c_val

def main():

    try:
        a = float(input("Enter a: "))
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))
        d = float(input("Enter d: "))
        
        answer = bisection_method(a, b, c, d)
        print(f"f(x) = 0, within the tolerance is x = {answer}")

    except ValueError:
        print("Invalid input")

main()
