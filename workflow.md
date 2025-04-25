## 1. Streamlit Page Initialization

1. **`st.set_page_config`**  
   - Sets the browser tab title to “My Custom Mini Compiler.”  
   - Applies the 🚀 icon and wide-layout for more horizontal space.

2. **Inject Custom CSS**  
   - A `<style>` block overrides default Streamlit styles:  
     - Gradient background, monospace code textarea, neon-green buttons, etc.

3. **Render UI Components**  
   - **Title & Intro** (`st.title`, `st.markdown`)  
   - **Program Input** (`st.text_area`) with a default sample program.  
   - **Run Button** (`st.button("Run Program")`).

---

## 2. User Interaction

- When you click **Run Program**, Streamlit reruns the script top-to-bottom, sees `if st.button("Run Program")` evaluate to `True`, and enters that block.

---

## 3. Capturing & Redirecting Output

1. **`run_program_and_capture_output(program_text)`** is called with the raw text you entered.
2. **Stdout Swap**  
   - `sys.stdout` is temporarily replaced with an `io.StringIO()` buffer so that all `print()` calls in the VM get captured as a string rather than sent to the real console.

---

## 4. Compile & Run Pipeline

Inside `compile_and_run(program_text)`:

### a) Lexical Analysis (Lexer)
- **Input**: raw string, e.g.  
  ```  
  a = 5;  
  b = a * 2;  
  b + 3;  
  ```
- **Process**:  
  - `advance()`, `skip_whitespace()` to step through characters.  
  - Recognizes tokens: `IDENTIFIER(a)`, `ASSIGN(=)`, `INTEGER(5)`, `SEMI(;)`, etc.
- **Output**: a stream of `Token(type, value)` objects ending in `EOF`.

### b) Syntax Analysis (Parser → AST)
- **Lookahead**: holds both `current_token` and `next_token` so it can distinguish `x = …` vs. `x + …`.
- **Grammar Rules**:
  1. **`statement_list`** splits on semicolons into a `Compound` node.
  2. **`assignment_statement`** builds an `Assign(Var, Expr)` node.
  3. **`expr`**, **`term`**, **`factor`** recursively build `BinOp`, `UnaryOp`, `Num`, and `Var` nodes.
- **Output**: a tree of AST nodes representing the entire program.

### c) Code Generation (AST → Bytecode-like Instructions)
- A **`CodeGenerator`** walks the AST:
  - For each `Num`: emits `LOAD_CONST value`.
  - For `Var`: emits `LOAD_VAR name`.
  - For `BinOp`: first generate left/right, then `BINARY_ADD`/`SUB`/etc.
  - For `Assign`: generate right side, then `STORE_VAR name`.
  - After each top-level statement, emit `PRINT_ITEM` so expression results get printed.
- **Output**: a linear list of instructions, e.g.  
  ```
  LOAD_CONST 5
  STORE_VAR a
  LOAD_VAR a
  LOAD_CONST 2
  BINARY_MUL
  PRINT_ITEM
  ...
  ```

### d) Virtual Machine Execution
- **`VirtualMachine`** steps through instructions with:
  - A **stack** for intermediate values.  
  - An **environment dict** (`env`) mapping variable names to values.
- **Instruction Loop**:
  1. **`LOAD_CONST`** pushes a literal.
  2. **`LOAD_VAR`** looks up `env[name]`.
  3. **`BINARY_*`** pop two values, compute, push result.
  4. **`STORE_VAR`** pops result and writes it to `env`.
  5. **`UNARY_NEG`** negates the top of stack.
  6. **`PRINT_ITEM`** pops and `print()`s the value (captured by our redirect).

---

## 5. Restoring Output & Display

1. **Stdout Reset**  
   - After `vm.run()`, the captured text (e.g.  
     ```
     10
     7
     13
     ```
     ) is retrieved via `.getvalue()` and `sys.stdout` is restored.
2. **Streamlit Display**  
   - `st.subheader("Program Output:")`  
   - `st.text(output)` shows the captured lines in the app.

---

## 6. Error Handling

- **Lexer**: invalid chars → raises “Invalid character.”  
- **Parser**: unexpected tokens or missing semicolons/parentheses → “Invalid syntax” or “Unexpected token.”  
- **VM**:  
  - Undefined variable → “Undefined variable ‘x’.”  
  - Division by zero → Python’s `ZeroDivisionError`.

---

### Summary Flowchart (Textual)

```
[User enters code] 
         ↓
[Run Program button clicked]
         ↓
[run_program_and_capture_output()]
         ↓
[compile_and_run()]
    → Lexer → Token stream
    → Parser → AST
    → CodeGenerator → Instruction list
    → VirtualMachine → Printed results
         ↓
[Capture & return printed results]
         ↓
[Streamlit displays output]
```
