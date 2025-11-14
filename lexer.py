import ply.lex as lex

# Tokens
tokens = (
    'NUMBER',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'NAME',
    'EQUALS',
    'COMMA',
    'STRING',
    'INTERPOLATION',
    'ESCREVER',
    'CONCAT',
    'COMMENT',
    'ENTRADA',
    'ALEATORIO',
    'FUNCAO',
    'FIM',
    'COLON',
    'SEMICOLON',
    'MAIOR', 
    'MENOR',
)

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUALS = r'='
t_COMMA = r','
t_CONCAT = r'\<\>'
t_COLON = r':'
t_SEMICOLON = r';'


def t_MAIOR(t):
    r'/\\'
    return t

def t_MENOR(t):
    r'\\/'
    return t

def t_FUNCAO(t):
    r'FUNCAO'
    return t

def t_FIM(t):
    r'FIM'
    return t

def t_ESCREVER(t):
    r'ESCREVER'
    return t

def t_ENTRADA(t):
    r'ENTRADA'
    return t

def t_ALEATORIO(t):
    r'ALEATORIO'
    return t

def t_INTERPOLATION(t):
    r'\"([^\\\n]|(\\.))*?\"'
    if '#{' in t.value:
        t.type = 'INTERPOLATION'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

def t_NAME(t):
    r'[a-zA-Z_À-ÿà-ÿ_][a-zA-Z_0-9À-ÿà-ÿ_?!]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_multiline_comment(t):
    r'\{\-([\s\S]*?)\-\}'
    t.lexer.lineno += t.value.count('\n')
    pass  

def t_singleline_comment(t):
    r'\-\-.*'
    pass 

t_ignore = ' \t\n'  

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
