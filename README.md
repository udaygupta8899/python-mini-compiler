# Python Mini Compiler/Interpreter

Welcome to **Python Mini Compiler/Interpreter**! This project is an educational mini compiler/interpreter for a subset of Python-like syntax. It demonstrates the fundamental stages of language processing, including lexical analysis, parsing, code generation, and execution via a simple virtual machine.

## Features

- **Lexical Analysis:** Tokenizes input into identifiers, integers, operators, etc.
- **Parsing & AST:** Builds an Abstract Syntax Tree (AST) for arithmetic expressions, variable assignments, and more.
- **Code Generation:** Converts the AST into bytecode-like instructions.
- **Virtual Machine:** Executes the generated instructions using a stack-based approach.
- **Streamlit UI:** Provides an interactive web interface with a custom background, heading, and icon for a modern look.

## Getting Started

### Prerequisites

Ensure you have [Python 3](https://www.python.org/) installed. You will also need to install [Streamlit](https://streamlit.io/).

To install Streamlit, run:

```bash
pip install streamlit
```

### Running the App

1. Clone or download the repository.
2. Navigate to the project directory.
3. Run the Streamlit app using:

   ```bash
   streamlit run streamlit_app.py
   ```

4. Your browser should automatically open to the app interface. If not, follow the local URL provided in the terminal.

### Using the Compiler/Interpreter

- **Input:**  
  Enter your program code into the provided text area. For example:
  ```plaintext
  a = 5;
  b = 10;
  a + b;
  a * b;
  c = a * (b + 2);
  c - 3;
  ```
- **Execution:**  
  Click the **Run Program** button. The app will compile and execute your code, displaying the output below the text area.

## Project Structure

- `streamlit_app.py`: Main Streamlit application that integrates the mini compiler/interpreter.
- `README.md`: This documentation file.

The code is structured into several components:
- **Lexer:** Responsible for tokenizing the input string.
- **Parser & AST:** Parses tokens into an AST.
- **Code Generator:** Transforms the AST into bytecode-like instructions.
- **Virtual Machine:** Executes instructions using a stack-based environment.
- **Streamlit Interface:** Provides an interactive UI for code input and output display.

## Customization

The project includes custom CSS injected into the Streamlit app to enhance the UI:
- **Page Title & Icon:** Set using `st.set_page_config` (e.g., "Python Mini Compiler/Interpreter" with a rocket icon).
- **Background & Styling:** Custom gradients, fonts, and button styles are defined in the embedded CSS.

## Future Enhancements

- Add support for more language features such as conditionals, loops, and functions.
- Enhance error handling and debugging outputs.
- Optimize the code generation phase.
- Extend the user interface with more advanced styling and interactive features.

## License

This project is provided for educational purposes. Feel free to modify and expand upon it for your own learning and development.

---
