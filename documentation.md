## 1. Overview

This mini compiler parses, compiles, and executes a tiny subset of Python-like code:

- **Integer arithmetic**  
- **Variables & assignment**  
- **Unary operators** (`+`, `–`)  
- **Binary operators** (`+`, `–`, `*`, `/`)  
- **Parentheses** for grouping  
- **Semicolon-terminated statements**  
- **Automatic printing** of each expression’s result  
- **No support for comments, floats, strings, control flow, functions, etc.**

---

## 2. Lexical Elements

| Token Type   | Description                          | Example           |
|--------------|--------------------------------------|-------------------|
| `INTEGER`    | Sequence of digits → an integer      | `123`, `0`, `42`  |
| `IDENTIFIER` | Letter or underscore, then alphanum  | `x`, `_foo`, `var1` |
| `PLUS`       | Plus operator                        | `+`               |
| `MINUS`      | Minus operator                       | `-`               |
| `MUL`        | Multiplication operator              | `*`               |
| `DIV`        | Division operator                    | `/`               |
| `LPAREN`     | Left parenthesis                     | `(`               |
| `RPAREN`     | Right parenthesis                    | `)`               |
| `ASSIGN`     | Assignment operator                  | `=`               |
| `SEMI`       | Statement terminator                 | `;`               |
| `EOF`        | End of input                         | —                 |

Whitespace (spaces, tabs, newlines) is ignored between tokens.

---

## 3. Grammar

```
program           ::= statement_list EOF

statement_list    ::= statement (';' statement)*

statement         ::= assignment_statement
                    | expr

assignment_statement
                  ::= IDENTIFIER '=' expr

expr              ::= term (( '+' | '–' ) term)*

term              ::= factor (( '*' | '/' ) factor)*

factor            ::= ('+' | '–') factor
                    | INTEGER
                    | IDENTIFIER
                    | '(' expr ')'
```

- **Semicolons** (`;`) separate statements; the final statement may optionally end without a trailing semicolon.
- **Lookahead** on `IDENTIFIER`+`=` distinguishes assignments from variable references in expressions.

---

## 4. Variables & Assignment

- Assign with `=`:  
  ```  
  x = 5;  
  my_var = x + 3;  
  ```
- Variables must be assigned before use; otherwise you get an “Undefined variable” error.

---

## 5. Expressions

- **Binary arithmetic**:  
  ```  
  2 + 3  
  10 - 4  
  7 * 8  
  20 / 5  
  ```
- **Unary plus/minus** (only on factors):  
  ```  
  -5  
  +x  
  ```
- **Grouping** with parentheses:  
  ```  
  (2 + 3) * 4  
  -(a - (b + 1))  
  ```

---

## 6. Statement Execution & Output

- Each **expression statement** (i.e. not an assignment) automatically prints its value.  
- Assignments do **not** print unless you refer to the variable in a later expression.

**Example:**

```text
a = 5;
b = 10;
a + b;          ➔ 15
a * b;          ➔ 50
c = a * (b+2);
c - 3;          ➔ 57
```

---

## 7. Error Handling

- **Syntax errors** (e.g. unexpected token, missing `;`, mismatched `(`) raise “Invalid syntax” or “Unexpected token” messages.
- **Lexical errors** (invalid characters) raise “Invalid character.”
- **Runtime errors** (e.g. division by zero, undefined variable) raise descriptive exceptions.

---

## 8. Limitations & Extensions

- **No support** for:
  - Floating-point numbers  
  - Strings or other data types  
  - Comments  
  - Control flow (`if`, `while`, etc.)  
  - Functions or scopes  
- To extend, you’d need to:
  1. Add new token types (e.g. `FLOAT`, `STRING`, keywords).  
  2. Enhance the parser with new grammar rules.  
  3. Update the AST, code generator, and VM to handle new constructs.

---

## 9. Using the Streamlit Interface

1. **Enter** your program in the text area (semicolon-separated).  
2. **Click** **Run Program**.  
3. **View** output under **Program Output**.
