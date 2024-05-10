import json
from sympy import *

class Newtons:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)

        self.func_str = config['f(x)']
        if config['Iteration'] == 0:
            self.xi = config['xi']
        else:
            self.xi = config['xi+1']
        self.eps = config['Eps']
        self.Rest = config['Rest']
        self.Method = config['Method']
        self.criteria = config['Stop_Criteria']

        x = symbols('x')
        self.func_expr = eval(self.func_str)
        self.f_val = self.func_expr.subs('x', self.xi).evalf()
        self.f_prime = self.find_derivative(self.func_expr)
        self.f_sec_prime = self.find_derivative(self.func_expr)
        self.tangent = self.find_tanget()

    def find_derivative(self, func_expr):
        x = symbols('x')  
        func_prime = diff(func_expr, x)
        return func_prime
    
    def find_tanget(self):
        x = symbols('x')  
        tanget = self.f_prime.subs('x', self.xi).evalf()*(x-self.xi)+ self.func_expr.subs('x', self.xi).evalf()
        return tanget
    
    def Iteration(self):
        x = self.xi
        f_prime_val = self.f_prime.subs('x', x).evalf()
        self.xi = x - self.f_val / f_prime_val
        if abs(x-self.xi)<self.eps:
            self.criteria = True

    def update_config(self):
        with open('config.json', "r") as f:
            config = json.load(f)

        if config['Iteration'] == 0: 
            config['dx'] = str(self.f_prime)
            config['d2x'] = str(self.f_sec_prime)
        config['tangent'] = str(self.tangent)
        config['xi'] = config['xi+1']
        config['xi+1'] = float(self.xi)
        config['f(xi)'] = float(self.f_val)
        config['f(xi+1)'] = float(self.func_expr.subs('x', self.xi).evalf())
        config['Rest'] = self.Rest
        config['Iteration'] += 1
        config['Stop_Criteria'] = self.criteria

        print("incredible")
        with open('config.json', "w") as f:
            json.dump(config, f)

def root_search():
    methods = {
        "Newtons": Newtons,
    }
    with open('config.json', "r") as f:
        config = json.load(f)

    Num_method = methods[config['Method']]()
    Num_method.Iteration()
    Num_method.update_config()
    
root_search()