import ply
import ply.lex as lex

tokens = (
    'U8', 'U16', 'U32','BYTE',
    'ID','NUMBER',
    'EQUALS', 'COLON',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'
)

# Tokens
t_COLON = r':'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'


def t_NUMBER(t):
    r'0[xX][0-9a-fA-F]+|\d+'
    try:
        if t.value.startswith("0x") or t.value.startswith("0X"):
            t.value = int(t.value,16)
        else:
            t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


reserved = {
    'u8': 'U8',
    'u16': 'U16',
    'u32': 'U32',
    'byte': 'BYTE'
    }

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Build the lexer


lexer = lex.lex()


def test_lex_token():
    str_value = "u8:STC=0x4e u8:CMD u8:SEQ u16:DID u32:Length  byte[Length]:Data  u8:CS u8:END=0x5f"
    lexer.input(str_value)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)



