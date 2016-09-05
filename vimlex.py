import ply.lex as lex
from ply.lex import TOKEN

# Declare the state
states = (
   ('operatorpending','exclusive'),
   ('textobjpending','exclusive'),
)

tokens = (
   'REG',
   'NUMBER',
   'META',
   'CHAR',
   'OPERATOR',
   'MOTION',
   'TEXTOBJMOD',
   'TEXTOBJ',
   'PASTE',
)

# Regular expression rules for simple tokens
operator = r'[dyc]'
number  = r'[1-9]\d*'
motion = r'[hjklwWeEbB\[\]{}()]|t.|f.|F.|T.'
text_obj = r'[wWps{}()"`\[\]]'
text_obj_mod = r'a|i'
t_ANY_MOTION = motion
t_META  = r'<.+>'
t_REG  = r'"[a-zA-Z0-9"]'
t_PASTE = r'P|p'

@TOKEN(operator)
def t_operatorpending_OPERATOR(t):
    t.lexer.begin('INITIAL')
    return t

@TOKEN(text_obj)
def t_textobjpending_TEXTOBJ(t):
    t.lexer.begin('INITIAL')
    return t

@TOKEN(text_obj_mod)
def t_operatorpending_TEXTOBJMOD(t):
    t.lexer.begin('textobjpending')
    return t

@TOKEN(number)
def t_operatorpending_NUMBER(t):
    return t

@TOKEN(motion)
def t_operatorpending_MOTION(t):
    t.lexer.begin('INITIAL')
    return t

@TOKEN(operator)
def t_OPERATOR(t):
    t.lexer.begin('operatorpending')
    return t

@TOKEN(number)
def t_NUMBER(t):
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
t_textobjpending_ignore  = ' \t'
t_operatorpending_ignore  = ' \t'

# Error handling rule
def t_textobjpending_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_operatorpending_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    # Build the lexer
    lexer = lex.lex()
    # Test it out
    data = '''
    12d51w<ESC>
    daw"0p
    12d51w<ESC>
    p""
    di{
    w3w4w
    dd
    yy
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)

