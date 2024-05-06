import json
import sympy
import string

class NewtonMethod:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)

        self.func_str = config['Func']
        self.xi = config['Xi']
        self.eps = config['Eps']
        self.Rest = config['Rest']
        self.Method = config['Method']
        self.criteria = config['Stop_Criteria']

        x = sympy.symbols('x')
        self.func_expr = eval(self.func_str)
        self.f_val = self.Function(self.xi)

    def Function(self, x):
        return self.func_expr.subs('x', x).evalf()
    
    def find_derivative(self):
        x = sympy.symbols('x')  
        f_expr = eval(self.func_str)  
        f_prime = sympy.diff(f_expr, x)
        return f_prime
  
    def Iteration(self):
        x = self.xi
        f_prime = self.find_derivative()
        f_prime_val = f_prime.subs('x', x).evalf()
        self.xi = x - self.f_val / f_prime_val
        if abs(x-self.xi)<self.eps:
            self.criteria = True

    def update_config(self):
        with open('config.json', "r") as f:
            config = json.load(f)

        config['Xi'] = float(self.xi)
        config['Value'] = float(self.f_val)
        config['Rest'] = self.Rest
        config['Iteration'] += 1
        config['Stop_Criteria'] = self.criteria

        print("incredible")
        with open('config.json', "w") as f:
            json.dump(config, f)

def upload_value_derivative():
    with open('config.json', "r") as f:
        config = json.load(f)

    x = sympy.symbols('x')
    f_expr = eval(config['Func'])  
    f_value = f_expr.subs('x', x).evalf()
    f_prime = sympy.diff(f_expr, x)
    

    config['Value'] = f_value
    config['Derivative'] = f_prime
    
    with open('config.json', "w") as f:
        json.dump(config, f)

def test():
    N = NewtonMethod()
    N.Iteration()
    N.update_config()

test()
