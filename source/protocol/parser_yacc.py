import ply
import ply.yacc as yacc
import protocol.parser_lex as lex_module
from protocol.parser_lex import tokens
import ply.lex as lex

lexer = lex.lex(module=lex_module)

#Parsing rules
precedence = (
    # ('left', 'PLUS', 'MINUS'),
    # ('left', 'TIMES', 'DIVIDE'),
    # ('right', 'UMINUS'),
)


def p_expression_unit(t):
    'expression : type COLON ID'
    t[0] = t[2]

def p_expression_unit_const(t):
    'expression : type COLON ID EQUALS NUMBER'
    t[0] = t[2]


def p_expression_type(t):
    '''
    type : U8
         | U16
         | U32
    '''
    try:
        t[0] = ("int fixed", t)
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_expression_byte_fixed(t):
    '''
    type : BYTE LBRACKET  NUMBER  RBRACKET
    '''
    try:
        t[0] = ("byte fixed", t)
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_expression_byte_variable(t):
    '''
    type : BYTE LBRACKET ID  RBRACKET
    '''
    try:
        t[0] = ("byte variable", t)
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()

def parse_protocol_bytes(str_values):
    parser.parse(str_values)




