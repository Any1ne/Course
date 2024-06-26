import json
from sympy import *
import csv

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
        self.number_iteration = config['Number of Iteration']
        self.iteration = config['Iteration']+1

        x = symbols('x')
        self.func_expr = sympify(self.func_str)
        self.fxi = self.func_expr.subs('x', self.xi).evalf()
        self.f_prime = self.find_derivative(self.func_expr)
        self.f_sec_prime = self.find_derivative(self.f_prime)
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
        if not self.criteria:
            x = self.xi
            f_prime_val = self.f_prime.subs('x', self.xi).evalf()
            if f_prime_val !=0:
                self.xi_1 = x - self.fxi / f_prime_val
            else:
                self.xi_1 = x

            self.fxi_1 = self.func_expr.subs('x', self.xi_1).evalf()


            if abs(self.fxi-self.fxi_1)<self.eps or self.iteration >= self.number_iteration:
                self.criteria = True
            elif not self.fxi_1.is_real:
                self.criteria = True
                self.fxi_1 = 0

    def update_config(self):
        with open('config.json', "r") as f:
            config = json.load(f)

        if self.iteration == 1: 
            config['dx'] = str(self.f_prime)
            config['d2x'] = str(self.f_sec_prime)
            config['f(xi)'] = float(self.fxi)
            config['f(x0)'] = float(self.fxi)
        else:
            config['xi-1'] = float(self.xi)
            config['f(xi-1)'] = config['f(xi)']   
            config['xi'] = config['xi+1']
            config['f(xi)'] = config['f(xi+1)']

        config['xi+1'] = float(self.xi_1)
        config['tangent'] = str(self.tangent)
        
        config['f(xi+1)'] = float(self.fxi_1)
        
        config['Rest'] = self.Rest
        config['Iteration'] = self.iteration
        config['Stop_Criteria'] = self.criteria

        with open('config.json', "w") as f:
            json.dump(config, f, indent=4)

        with open('result.csv', 'a', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the data row
            if self.iteration == 1:
                writer.writerow([config['xi'], config['f(xi)']])
            writer.writerow([config['xi+1'], config['f(xi+1)']])
            
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