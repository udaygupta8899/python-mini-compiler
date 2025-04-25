import streamlit as st
import sys
import io

st.set_page_config(
    page_title="My Custom Mini Compiler",
    page_icon=":rocket:",
    layout="wide"
)

##############################
# Mini Compiler Code
##############################

# Token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ASSIGN, IDENTIFIER, SEMI, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'ASSIGN', 'IDENTIFIER', 'SEMI', 'EOF'
)

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0  # position in text
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        """Advance the 'pos' pointer and update the current_char variable."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def identifier(self):
        """Handle identifiers: variable names and keywords."""
        result = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()
        return Token(IDENTIFIER, result)

    def integer(self):
        """Return a (multidigit) integer consumed from input."""
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(INTEGER, int(result))

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)."""
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier()

            if self.current_char.isdigit():
                return self.integer()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            self.error()

        return Token(EOF, None)

##############################
# Parser and AST
##############################

# AST node classes
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = op
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = op
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left   # Var
        self.token = op    # '=' token
        self.right = right

class Compound(AST):
    """Represents a sequence of statements."""
    def __init__(self):
        self.children = []

class NoOp(AST):
    pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # Initialize both current and next tokens
        self.current_token = self.lexer.get_next_token()
        self.next_token = self.lexer.get_next_token()

    def error(self, msg="Invalid syntax"):
        raise Exception(msg)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            # Advance the tokens: current becomes next, and fetch a new next token
            self.current_token = self.next_token
            self.next_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token {token_type} but got {self.current_token.type}")

    def factor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | IDENTIFIER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type in (PLUS, MINUS):
            self.eat(token.type)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == IDENTIFIER:
            self.eat(IDENTIFIER)
            return Var(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            self.error("Unexpected token in factor")

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def assignment_statement(self):
        """assignment_statement : IDENTIFIER ASSIGN expr"""
        left = Var(self.current_token)
        self.eat(IDENTIFIER)
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left, op, right)

    def statement(self):
        """
        statement : assignment_statement
                  | expr
        """
        # Use the lookahead token to decide if it's an assignment.
        if self.current_token.type == IDENTIFIER and self.next_token.type == ASSIGN:
            return self.assignment_statement()
        else:
            return self.expr()

    def statement_list(self):
        """statement_list : statement (';' statement)*"""
        node = Compound()
        stmt = self.statement()
        node.children.append(stmt)
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            if self.current_token.type == EOF:
                break
            node.children.append(self.statement())
        return node

    def parse(self):
        node = self.statement_list()
        if self.current_token.type != EOF:
            self.error("Unexpected token after statement list")
        return node

##############################
# Code Generation
##############################

# Define opcodes for our simple VM
LOAD_CONST   = 'LOAD_CONST'
LOAD_VAR     = 'LOAD_VAR'
STORE_VAR    = 'STORE_VAR'
BINARY_ADD   = 'BINARY_ADD'
BINARY_SUB   = 'BINARY_SUB'
BINARY_MUL   = 'BINARY_MUL'
BINARY_DIV   = 'BINARY_DIV'
UNARY_NEG    = 'UNARY_NEG'
PRINT_ITEM   = 'PRINT_ITEM'

class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate(self, node):
        """Traverse the AST and generate instructions."""
        if isinstance(node, Compound):
            for child in node.children:
                self.generate(child)
                # By default, print result of expression statements
                self.instructions.append((PRINT_ITEM, None))
        elif isinstance(node, Assign):
            self.generate(node.right)
            # The result of right-hand side is now on the stack; store it in the variable
            self.instructions.append((STORE_VAR, node.left.value))
        elif isinstance(node, BinOp):
            self.generate(node.left)
            self.generate(node.right)
            if node.op.type == PLUS:
                self.instructions.append((BINARY_ADD, None))
            elif node.op.type == MINUS:
                self.instructions.append((BINARY_SUB, None))
            elif node.op.type == MUL:
                self.instructions.append((BINARY_MUL, None))
            elif node.op.type == DIV:
                self.instructions.append((BINARY_DIV, None))
        elif isinstance(node, UnaryOp):
            self.generate(node.expr)
            if node.op.type == MINUS:
                self.instructions.append((UNARY_NEG, None))
            # If PLUS, do nothing
        elif isinstance(node, Num):
            self.instructions.append((LOAD_CONST, node.value))
        elif isinstance(node, Var):
            self.instructions.append((LOAD_VAR, node.value))
        else:
            raise Exception("Unknown AST node")
        return self.instructions

##############################
# Virtual Machine
##############################

class VirtualMachine:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.env = {}  # variable environment

    def run(self):
        for inst, arg in self.instructions:
            if inst == LOAD_CONST:
                self.stack.append(arg)
            elif inst == LOAD_VAR:
                if arg in self.env:
                    self.stack.append(self.env[arg])
                else:
                    raise Exception(f"Undefined variable '{arg}'")
            elif inst == STORE_VAR:
                value = self.stack.pop()
                self.env[arg] = value
            elif inst == BINARY_ADD:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left + right)
            elif inst == BINARY_SUB:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left - right)
            elif inst == BINARY_MUL:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left * right)
            elif inst == BINARY_DIV:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left / right)
            elif inst == UNARY_NEG:
                value = self.stack.pop()
                self.stack.append(-value)
            elif inst == PRINT_ITEM:
                # For simplicity, print the top of the stack
                if self.stack:
                    value = self.stack.pop()
                    print(value)
            else:
                raise Exception(f"Unknown instruction {inst}")

##############################
# Main Compiler Driver
##############################

def compile_and_run(program_text):
    # Lexical analysis
    lexer = Lexer(program_text)
    # Parsing
    parser = Parser(lexer)
    ast = parser.parse()
    # Code Generation
    codegen = CodeGenerator()
    instructions = codegen.generate(ast)
    # Execute the instructions
    vm = VirtualMachine(instructions)
    vm.run()

##############################
# Streamlit App Interface
##############################

def run_program_and_capture_output(program_text):
    # Capture the output produced by compile_and_run
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        compile_and_run(program_text)
        output = sys.stdout.getvalue()
    except Exception as e:
        output = f"Error: {e}"
    finally:
        sys.stdout = old_stdout
    return output

# Inject custom CSS for styling with a custom background and new heading style
custom_css = """
<style>
/* Overall page background using a new gradient */
body {
    background: linear-gradient(135deg, #ff7e5f, #feb47b);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #fff;
}

/* Custom heading style */
h1 {
    font-size: 3.5em;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5em;
}

/* Container styling for the app */
.reportview-container .main .block-container {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 2em;
    border-radius: 10px;
}

/* Text area styling */
textarea {
    background-color: #222;
    color: #0f0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 1em;
    border: 2px solid #0f0;
    border-radius: 5px;
}

/* Button styling */
div.stButton > button {
    background-color: #0f0;
    color: #000;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    padding: 0.8em 2em;
    font-size: 1em;
    cursor: pointer;
}
div.stButton > button:hover {
    background-color: #cff;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# UI Components
st.title("Python Mini Compiler/Interpreter")
st.markdown("""
Welcome to **Python Mini Compiler/Interpreter**!  
This web app implements a mini compiler/interpreter for a subset of Python-like syntax.  
Enter your program in the text area below and click **Run Program** to see the output.
""")

program_text = st.text_area(
    "Enter your program here:",
    value="""a = 5;
b = 10;
a + b;
a * b;
c = a * (b + 2);
c - 3;""",
    height=300
)

if st.button("Run Program"):
    output = run_program_and_capture_output(program_text)
    st.subheader("Program Output:")
    st.text(output)
