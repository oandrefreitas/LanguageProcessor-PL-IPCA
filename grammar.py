import ply.yacc as yacc
from lexer import tokens
import random

# Classe para armazenar funções
class Function:
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __repr__(self):
        return f"Function(params={self.params}, body={self.body})"

    def call(self, args):
        local_vars = dict(zip(self.params, args))
        return execute_function(self.body, local_vars)

variables = {}
functions = {}

precedence = (
    ('right', 'UMINUS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'CONCAT'),
    ('left', 'MAIOR', 'MENOR') 
)

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement_list statement SEMICOLON
                      | statement SEMICOLON'''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : assignment
                 | write_statement
                 | function_definition
                 | function_call'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : NAME EQUALS expression
                  | NAME EQUALS ENTRADA LPAREN RPAREN
                  | NAME EQUALS ALEATORIO LPAREN expression RPAREN
                  | NAME EQUALS function_call'''
    if len(p) == 4:
        result = eval_expression(p[3])
        variables[p[1]] = result
        p[0] = ('assign', p[1], result)
    elif p[3] == 'ENTRADA':
        user_input = input("Digite um valor: ")
        variables[p[1]] = int(user_input)
        p[0] = ('assign', p[1], user_input)
    elif p[3] == 'ALEATORIO':
        count = eval_expression(p[5])
        random_value = random.randint(0, count)
        variables[p[1]] = random_value
        p[0] = ('assign', p[1], random_value)

def p_write_statement(p):
    '''write_statement : ESCREVER LPAREN expression RPAREN'''
    result = eval_expression(p[3])
    p[0] = ('write', result)
    print(str(result))  # Converte o resultado para string e imprime

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression MAIOR expression
                  | expression MENOR expression'''
    p[0] = ('binop', p[1], p[3], p[2])

def p_expression_concat(p):
    '''expression : expression CONCAT expression'''
    left = eval_expression(p[1])
    right = eval_expression(p[3])
    p[0] = str(left) + str(right)

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1]

def p_expression_interpolation(p):
    '''expression : INTERPOLATION'''
    base_string = p[1]
    interpolated_string = base_string
    while '#{' in interpolated_string:
        start = interpolated_string.index('#{')
        end = interpolated_string.index('}', start)
        var_name = interpolated_string[start+2:end]
        interpolated_string = interpolated_string[:start] + str(variables.get(var_name, '')) + interpolated_string[end+1:]
    p[0] = interpolated_string

def p_expression_variable(p):
    '''expression : NAME'''
    p[0] = variables.get(p[1], 0)

def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = -eval_expression(p[2])

def p_expression_list(p):
    '''expression : LBRACKET elements RBRACKET'''
    p[0] = [eval_expression(elem) for elem in p[2]]

def p_elements(p):
    '''elements : elements COMMA expression
                | expression
                | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_function_definition(p):
    '''function_definition : FUNCAO NAME LPAREN parameters RPAREN COLON statement_list FIM'''
    functions[p[2]] = Function(p[4], p[7])
    p[0] = ('function_definition', p[2], p[4], p[7])

def p_parameters(p):
    '''parameters : NAME COMMA parameters
                  | NAME
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []

def p_function_call(p):
    '''function_call : NAME LPAREN arguments RPAREN'''
    function_name = p[1]
    args = [eval_expression(arg) for arg in p[3]]
    if function_name in functions:
        function = functions[function_name]
        p[0] = function.call(args)
    else:
        print(f"Erro: função {function_name} não definida")
        p[0] = None

def p_arguments(p):
    '''arguments : expression COMMA arguments
                 | expression
                 | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []

def execute_function(body, local_vars):
    global variables
    old_vars = variables.copy()
    variables.update(local_vars)
    result = None
    try:
        if isinstance(body, list):  # Verifica se o corpo é uma lista de instruções
            for statement in body:
                if isinstance(statement, tuple) and statement[0] == 'assign':
                    variables[statement[1]] = eval_expression(statement[2])
                    result = variables[statement[1]]
                else:
                    result = eval_expression(statement)
        else:  # Caso contrário, avalia o corpo diretamente
            result = eval_expression(body)
    finally:
        variables = old_vars
    return result

def eval_expression(expression):
    if isinstance(expression, tuple):
        if expression[0] == 'binop':
            left = eval_expression(expression[1])
            right = eval_expression(expression[2])
            if expression[3] == '+':
                return left + right
            elif expression[3] == '-':
                return left - right
            elif expression[3] == '*':
                return left * right
            elif expression[3] == '/':
                return left / right
            elif expression[3] == '/\\':
                return left > right
            elif expression[3] == '\\/':
                return left < right
        elif expression[0] == 'concat':
            left = eval_expression(expression[1])
            right = eval_expression(expression[2])
            return str(left) + str(right)
        elif expression[0] == 'variable':
            return variables.get(expression[1], 0)
        elif expression[0] == 'list':
            return [eval_expression(elem) for elem in expression[1]]
        elif expression[0] == 'call':
            function_name = expression[1]
            args = [eval_expression(arg) for arg in expression[2]]
            if function_name in functions:
                function = functions[function_name]
                return function.call(args)
            else:
                print(f"Erro: função {function_name} não definida")
                return None
    elif isinstance(expression, str):
        return variables.get(expression, expression)
    return expression

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno} e coluna {p.lexpos}")
    else:
        print("Erro de sintaxe no final da entrada")

parser = yacc.yacc()

def parse_input(data):
    try:
        return parser.parse(data)
    except Exception as e:
        print(f"Erro ao analisar o programa: {str(e)}")
