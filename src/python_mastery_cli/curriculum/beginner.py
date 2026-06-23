from __future__ import annotations

from ..models import CodeExample, Exercise, Lesson, Level, QuizQuestion

BEGINNER_LESSONS: list[Lesson] = [
    Lesson(
        id="b01",
        title="What Python Is",
        level=Level.BEGINNER,
        estimated_minutes=8,
        explanation=(
            "Python is a high-level, general-purpose programming language created by Guido van Rossum "
            "and first released in 1991. It is designed to be readable — the code often looks almost like "
            "plain English — which makes it a popular first language for new programmers and a powerful "
            "tool for experienced ones alike.\n\n"
            "When you run a Python program, an interpreter reads your source file line by line and "
            "executes each instruction immediately. This is different from compiled languages like C, "
            "where code must be translated into machine code before it can run.\n\n"
            "Python is used everywhere: web development (Instagram, Pinterest), data science and AI "
            "(TensorFlow, pandas), automation, scripting, game development, and more. Learning Python "
            "gives you access to one of the largest communities and ecosystems of libraries in the world."
        ),
        key_terms={
            "Interpreter": "The program that reads your Python source code and executes it line by line.",
            "Syntax": "The grammar rules that determine whether code is valid Python.",
            "Source code": "The human-readable text you write and save in a .py file.",
            "High-level language": "A language that hides low-level machine details, making it easier to write.",
            "Library": "A collection of pre-written Python code you can reuse in your own programs.",
        },
        code_examples=[
            CodeExample(
                title="Your first Python program",
                code='print("Hello, world!")',
                explanation="The classic first program — it tells Python to display a line of text on screen.",
                output="Hello, world!",
                line_notes={
                    1: "[bold]print()[/bold] is a built-in function that outputs text. The text in quotes is called a [bold]string[/bold].",
                },
            ),
            CodeExample(
                title="Python as a calculator",
                code=(
                    "print(2 + 3)\n"
                    "print(10 / 4)\n"
                    "print(2 ** 8)"
                ),
                explanation="Python can evaluate arithmetic expressions directly.",
                output="5\n2.5\n256",
                line_notes={
                    1: "Adds 2 and 3, then prints the result.",
                    2: "Divides 10 by 4 — note the decimal result.",
                    3: "[bold]**[/bold] is the exponentiation operator: 2 to the power of 8.",
                },
            ),
        ],
        common_mistakes=[
            'Forgetting quotes around text: print(Hello) raises a NameError. Use print("Hello").',
            "Capitalising Print — Python is case-sensitive; the function is print, not Print.",
            "Mixing up running Python 2 vs Python 3 — this course targets Python 3.",
        ],
        practice_prompts=[
            "In your own words, what does the Python interpreter do when you run a script?",
            "Why might a readable, English-like syntax matter when you are just starting to code?",
            "Name two real-world applications or companies that use Python.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Python code is executed by a ____.",
                qtype="fill_blank",
                correct_answer="interpreter",
                explanation="The CPython interpreter reads and runs your code line by line.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which built-in function displays text on the screen?",
                qtype="multiple_choice",
                options=["echo()", "print()", "show()", "log()"],
                correct_answer="print()",
                explanation="print() is Python's standard output function.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Python is case-sensitive, so 'print' and 'Print' are different.",
                qtype="true_false",
                correct_answer="true",
                explanation="Python distinguishes upper and lower case everywhere, including function names.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b01-ex",
            title="Print a greeting",
            instructions="Write a program that prints exactly: Hello, Python!",
            starter_code='# Replace the ellipsis with the correct text\nprint("...")',
            expected_output="Hello, Python!",
            hints=[
                "Use the print() function.",
                "Put the exact text inside double quotes.",
                'The text must be: Hello, Python! (capital H, comma, space, exclamation mark)',
            ],
            solution='print("Hello, Python!")',
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b02",
        title="Installing and Running Python",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Before you can write Python programs, you need the Python interpreter installed on your "
            "computer. Visit python.org and download the latest Python 3 release for your operating "
            "system. During installation on Windows, tick the box that says 'Add Python to PATH' — "
            "this lets you run python from any terminal.\n\n"
            "Once installed, open a terminal (Command Prompt on Windows, Terminal on macOS/Linux) and "
            "type python3 --version (or python --version on Windows). You should see something like "
            "Python 3.12.0. If you do, Python is ready.\n\n"
            "You can run Python in two ways: interactively in the REPL (type python3 and press Enter "
            "to start a live prompt where each line executes immediately), or by saving code in a .py "
            "file and running it with python3 myfile.py. For real projects, the file approach is standard."
        ),
        key_terms={
            "REPL": "Read-Eval-Print Loop — an interactive Python prompt where you type code and see results immediately.",
            "PATH": "A system variable that tells your OS where to find executable programs like python3.",
            "Terminal": "A text-based interface for running commands on your computer.",
            ".py file": "A plain-text file containing Python source code, identified by the .py extension.",
            "pip": "Python's package installer — use it to add third-party libraries.",
        },
        code_examples=[
            CodeExample(
                title="Checking your Python version",
                code="# Run this in your terminal, NOT in Python itself\n# python3 --version",
                explanation="Before writing code, confirm which Python version is installed.",
                output="Python 3.12.0",
                line_notes={
                    1: "Lines starting with [bold]#[/bold] are comments — Python ignores them.",
                    2: "This shell command prints the installed Python version.",
                },
            ),
            CodeExample(
                title="Running a script from the terminal",
                code=(
                    '# Save this as hello.py, then run: python3 hello.py\n'
                    'print("Hello from a file!")'
                ),
                explanation="A .py file is just a text file. You run it by passing its name to python3.",
                output="Hello from a file!",
                line_notes={
                    1: "A comment explaining how to run this file — not executed by Python.",
                    2: "This is the only line Python actually runs.",
                },
            ),
        ],
        common_mistakes=[
            "On Windows, typing python3 may not work — try python instead.",
            "Forgetting to add Python to PATH during installation means the terminal can't find it.",
            "Saving your file as hello.txt instead of hello.py — Python expects the .py extension.",
            "Running python2 by accident — always check the version before starting.",
        ],
        practice_prompts=[
            "What is the difference between the REPL and running a .py file?",
            "Why does PATH matter for running Python from the terminal?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What flag shows the installed Python version in the terminal?",
                qtype="multiple_choice",
                options=["--version", "--info", "--check", "--release"],
                correct_answer="--version",
                explanation="python3 --version prints the version string.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The Python REPL executes code one line at a time interactively.",
                qtype="true_false",
                correct_answer="true",
                explanation="REPL stands for Read-Eval-Print Loop — each line is run as you press Enter.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What file extension do Python source files use?",
                qtype="fill_blank",
                correct_answer=".py",
                explanation="Python files are saved with the .py extension.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b02-ex",
            title="Verify your installation",
            instructions=(
                "Open your terminal and run: python3 --version\n"
                "Then create a file named greet.py containing a single print statement "
                "that outputs: Python is ready!\n"
                "Run it with: python3 greet.py"
            ),
            starter_code='# greet.py\nprint("...")',
            expected_output="Python is ready!",
            hints=[
                "Make sure Python 3 is installed before creating the file.",
                'Change the ... to the exact text: Python is ready!',
                "Run the file from the same directory where you saved it.",
            ],
            solution='print("Python is ready!")',
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b03",
        title="Variables",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "A variable is a named container that holds a value. Instead of writing the same number or "
            "text repeatedly, you store it once in a variable and refer to it by name. In Python you "
            "create a variable simply by assigning a value: name = 'Alice'. There is no need to declare "
            "the type first.\n\n"
            "Variable names must start with a letter or underscore, can contain letters, digits, and "
            "underscores, and are case-sensitive (age and Age are different variables). By convention, "
            "Python programmers use snake_case for multi-word names: first_name, total_price.\n\n"
            "Variables can be reassigned at any time — their value can even change type, though doing "
            "so carelessly leads to confusing bugs. Think of a variable as a sticky label you attach to "
            "a value; you can move the label to a different value whenever you like."
        ),
        key_terms={
            "Variable": "A named reference to a value stored in memory.",
            "Assignment": "Binding a name to a value using the = operator.",
            "snake_case": "The naming convention of using lowercase words separated by underscores.",
            "Reassignment": "Giving a variable a new value after it was already created.",
            "Identifier": "The name you give a variable, function, or other object.",
        },
        code_examples=[
            CodeExample(
                title="Creating and using variables",
                code=(
                    "name = 'Alice'\n"
                    "age = 30\n"
                    "print(name)\n"
                    "print(age)"
                ),
                explanation="Variables store a value under a name you choose.",
                output="Alice\n30",
                line_notes={
                    1: "Creates a variable [bold]name[/bold] and assigns the string 'Alice' to it.",
                    2: "Creates a variable [bold]age[/bold] and assigns the integer 30.",
                    3: "Reads the value stored in [bold]name[/bold] and prints it.",
                    4: "Reads the value stored in [bold]age[/bold] and prints it.",
                },
            ),
            CodeExample(
                title="Reassigning a variable",
                code=(
                    "score = 0\n"
                    "print(score)\n"
                    "score = 10\n"
                    "print(score)"
                ),
                explanation="A variable's value can be updated as many times as you like.",
                output="0\n10",
                line_notes={
                    1: "score starts at 0.",
                    3: "score is now reassigned to 10; the old value 0 is gone.",
                },
            ),
            CodeExample(
                title="Multiple assignment in one line",
                code="x, y, z = 1, 2, 3\nprint(x, y, z)",
                explanation="Python lets you assign several variables at once by separating them with commas.",
                output="1 2 3",
                line_notes={
                    1: "Unpacks three values into three variables simultaneously.",
                    2: "print() can accept multiple arguments separated by commas.",
                },
            ),
        ],
        common_mistakes=[
            "Using a variable before assigning it — Python raises NameError: name 'x' is not defined.",
            "Starting a variable name with a digit (1score is invalid); names must begin with a letter or underscore.",
            "Using spaces in names — Python requires underscores: total_price not total price.",
            "Confusing = (assignment) with == (equality check).",
        ],
        practice_prompts=[
            "Why is it useful to store a value in a variable rather than repeating the literal value?",
            "What would happen if you tried to print a variable that you had not yet assigned?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which of the following is a valid Python variable name?",
                qtype="multiple_choice",
                options=["2fast", "first_name", "first-name", "first name"],
                correct_answer="first_name",
                explanation="Variable names can only contain letters, digits, and underscores, and must not start with a digit.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In Python, x = 5 is called an ____.",
                qtype="fill_blank",
                correct_answer="assignment",
                explanation="The = operator assigns a value to a variable name.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Python variables must be declared with a type before use.",
                qtype="true_false",
                correct_answer="false",
                explanation="Python uses dynamic typing — you just assign a value and the type is inferred.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b03-ex",
            title="Store and print your info",
            instructions=(
                "Create three variables: name (your name as a string), age (your age as an integer), "
                "and city (your city as a string). Then print all three on separate lines."
            ),
            starter_code=(
                "name = ...\n"
                "age = ...\n"
                "city = ...\n"
                "print(name)\n"
                "print(age)\n"
                "print(city)"
            ),
            expected_output="Alice\n30\nNew York",
            hints=[
                "Strings go in quotes; integers do not.",
                "Replace each ... with a real value.",
                "Make sure your print statements use the variable name, not a literal string.",
            ],
            solution=(
                'name = "Alice"\n'
                "age = 30\n"
                'city = "New York"\n'
                "print(name)\n"
                "print(age)\n"
                "print(city)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b04",
        title="Data Types",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Every value in Python has a type that describes what kind of data it is and what you can do "
            "with it. The four most common built-in types you will meet right away are: int (whole numbers), "
            "float (decimal numbers), str (text), and bool (True or False).\n\n"
            "Python figures out the type of a value automatically — this is called dynamic typing. You can "
            "always check the type of any value with the built-in type() function. Understanding types "
            "matters because certain operations only work on certain types (you can multiply two numbers, "
            "but multiplying two strings raises an error).\n\n"
            "You can also convert between types using int(), float(), str(), and bool(). This is called "
            "type casting. For example, int('42') converts the string '42' to the integer 42."
        ),
        key_terms={
            "int": "Integer — a whole number with no decimal point, e.g. 7 or -3.",
            "float": "Floating-point number — a number with a decimal point, e.g. 3.14.",
            "str": "String — a sequence of characters enclosed in quotes, e.g. 'hello'.",
            "bool": "Boolean — either True or False.",
            "type()": "Built-in function that returns the type of any value.",
            "Type casting": "Converting a value from one type to another using int(), float(), str(), etc.",
        },
        code_examples=[
            CodeExample(
                title="The four basic types",
                code=(
                    "print(type(42))\n"
                    "print(type(3.14))\n"
                    "print(type('hello'))\n"
                    "print(type(True))"
                ),
                explanation="type() reveals the built-in type of any value.",
                output=(
                    "<class 'int'>\n"
                    "<class 'float'>\n"
                    "<class 'str'>\n"
                    "<class 'bool'>"
                ),
                line_notes={
                    1: "42 is an [bold]int[/bold] — a whole number.",
                    2: "3.14 is a [bold]float[/bold] — a number with a decimal part.",
                    3: "'hello' is a [bold]str[/bold] — text in quotes.",
                    4: "True is a [bold]bool[/bold] — one of exactly two values: True or False.",
                },
            ),
            CodeExample(
                title="Type casting",
                code=(
                    "x = '99'\n"
                    "print(type(x))\n"
                    "x = int(x)\n"
                    "print(type(x))\n"
                    "print(x + 1)"
                ),
                explanation="Converting a string to an int lets you do arithmetic on it.",
                output="<class 'str'>\n<class 'int'>\n100",
                line_notes={
                    1: "x is a string — note the quotes around 99.",
                    3: "[bold]int()[/bold] converts the string '99' into the integer 99.",
                    5: "Now x is an integer, so arithmetic works.",
                },
            ),
        ],
        common_mistakes=[
            "Confusing '42' (a string) with 42 (an integer) — you cannot do math on a string.",
            'Calling int() on a non-numeric string like int("hello") — this raises ValueError.',
            "Forgetting that True and False are capitalised in Python (not true or false).",
            "Mixing up float division (/) and integer division (//) — 7/2 is 3.5, but 7//2 is 3.",
        ],
        practice_prompts=[
            "What happens if you try to add an int and a string? Try it in the REPL.",
            "When would you need to cast a string to an int in a real program?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What type does Python assign to the value 3.14?",
                qtype="multiple_choice",
                options=["int", "float", "str", "double"],
                correct_answer="float",
                explanation="Any number with a decimal point is a float.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The built-in function to check a value's type is ____().",
                qtype="fill_blank",
                correct_answer="type",
                explanation="type(value) returns the type object for that value.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In Python, True and False are values of type bool.",
                qtype="true_false",
                correct_answer="true",
                explanation="bool is a distinct built-in type with exactly two values: True and False.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which function converts the string '7' to an integer?",
                qtype="multiple_choice",
                options=["str(7)", "int('7')", "float('7')", "num('7')"],
                correct_answer="int('7')",
                explanation="int() converts a compatible string or float to an integer.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b04-ex",
            title="Identify and convert types",
            instructions=(
                "Create a variable called value and assign it the string '2024'. "
                "Print its type, then convert it to an integer and print the result of adding 1 to it."
            ),
            starter_code=(
                "value = '2024'\n"
                "print(type(value))\n"
                "number = ...\n"
                "print(number + 1)"
            ),
            expected_output="<class 'str'>\n2025",
            hints=[
                "Use type() to check the current type.",
                "Use int() to convert the string to an integer.",
                "Once it is an integer, + 1 will work.",
            ],
            solution=(
                "value = '2024'\n"
                "print(type(value))\n"
                "number = int(value)\n"
                "print(number + 1)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b05",
        title="Strings",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "A string is a sequence of characters — letters, digits, spaces, punctuation — enclosed in "
            "single quotes ('...') or double quotes (\"...\"). Multi-line strings use triple quotes "
            "('''...''' or \"\"\"...\"\"\"). Strings are one of the most commonly used types in Python.\n\n"
            "Python provides a rich set of string operations. You can join strings with + (concatenation), "
            "repeat them with *, find their length with len(), and access individual characters with "
            "indexing (s[0] gives the first character). Strings also have many built-in methods like "
            ".upper(), .lower(), .strip(), .replace(), and .split().\n\n"
            "The most modern way to embed variable values inside strings is an f-string: prefix the "
            "opening quote with f and put expressions in curly braces. For example, f'Hello, {name}!' "
            "automatically fills in the value of name. F-strings are readable, concise, and fast."
        ),
        key_terms={
            "String": "An immutable sequence of characters enclosed in quotes.",
            "Concatenation": "Joining two strings with the + operator.",
            "f-string": "A formatted string literal where {expression} is replaced by its value at runtime.",
            "Indexing": "Accessing a single character by its position, starting at 0.",
            "len()": "Built-in function that returns the number of characters in a string.",
            "Method": "A function that belongs to an object and is called with dot notation, e.g. s.upper().",
        },
        code_examples=[
            CodeExample(
                title="Basic string operations",
                code=(
                    "greeting = 'Hello'\n"
                    "name = 'World'\n"
                    "message = greeting + ', ' + name + '!'\n"
                    "print(message)\n"
                    "print(len(message))\n"
                    "print(message[0])"
                ),
                explanation="Strings can be concatenated with + and measured with len().",
                output="Hello, World!\n13\nH",
                line_notes={
                    3: "[bold]+[/bold] joins the strings together. Note the extra ', ' string for the comma and space.",
                    5: "[bold]len()[/bold] counts every character including spaces and punctuation.",
                    6: "[bold]message[0][/bold] — indexing starts at 0, so this is the very first character.",
                },
            ),
            CodeExample(
                title="F-strings and string methods",
                code=(
                    "name = 'alice'\n"
                    "age = 25\n"
                    "print(f'Name: {name.capitalize()}, Age: {age}')\n"
                    "print(name.upper())\n"
                    "print('  hello  '.strip())"
                ),
                explanation="F-strings embed expressions directly. Methods transform string values.",
                output="Name: Alice, Age: 25\nALICE\nhello",
                line_notes={
                    3: "The [bold]f'...'[/bold] prefix makes this an f-string; [bold]{name.capitalize()}[/bold] capitalises the first letter.",
                    4: "[bold].upper()[/bold] returns a new string with all letters uppercased.",
                    5: "[bold].strip()[/bold] removes leading and trailing whitespace.",
                },
            ),
        ],
        common_mistakes=[
            "Mixing quote styles: starting with ' and ending with \" causes a SyntaxError.",
            'Forgetting to convert non-strings before concatenation: "Age: " + 25 raises TypeError.',
            "Thinking strings are mutable — they are not. s[0] = 'X' raises TypeError.",
            "Off-by-one errors with indexing: the last character is at index len(s) - 1, not len(s).",
        ],
        practice_prompts=[
            "What is the difference between concatenation and an f-string? Which do you prefer and why?",
            "If a string has 5 characters, what index does the last character have?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="How do you start an f-string in Python?",
                qtype="multiple_choice",
                options=["s'...'", "f'...'", "format'...'", "fmt'...'"],
                correct_answer="f'...'",
                explanation="An f-string is created by prefixing the opening quote with the letter f.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="String indexing in Python starts at ____.",
                qtype="fill_blank",
                correct_answer="0",
                explanation="The first character of any sequence in Python is at index 0.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Python strings can be modified in place (e.g. s[0] = 'X').",
                qtype="true_false",
                correct_answer="false",
                explanation="Strings are immutable — you must create a new string to make changes.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b05-ex",
            title="Build a formatted greeting",
            instructions=(
                "Create variables first_name and last_name. Use an f-string to print: "
                "Hello, <first_name> <last_name>! You have 3 new messages.\n"
                "Also print the full name in uppercase on the next line."
            ),
            starter_code=(
                "first_name = 'Jane'\n"
                "last_name = 'Doe'\n"
                "# Use an f-string here\n"
                "print(...)\n"
                "full_name = first_name + ' ' + last_name\n"
                "print(full_name....())"
            ),
            expected_output="Hello, Jane Doe! You have 3 new messages.\nJANE DOE",
            hints=[
                "Use f'...' and embed {first_name} and {last_name} in the string.",
                "Concatenate first_name + ' ' + last_name to build the full name.",
                "Call .upper() on the full name string.",
            ],
            solution=(
                "first_name = 'Jane'\n"
                "last_name = 'Doe'\n"
                "print(f'Hello, {first_name} {last_name}! You have 3 new messages.')\n"
                "full_name = first_name + ' ' + last_name\n"
                "print(full_name.upper())"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b06",
        title="Numbers",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Python has two primary numeric types: int for whole numbers (42, -7, 0) and float for "
            "numbers with a decimal component (3.14, -0.5, 1.0). For most everyday arithmetic Python "
            "handles them automatically, converting between the two when needed.\n\n"
            "The arithmetic operators are: + (add), - (subtract), * (multiply), / (true divide — "
            "always returns a float), // (floor divide — rounds down to an int), % (modulo — the "
            "remainder), and ** (exponentiation). The order of operations follows standard mathematics: "
            "parentheses first, then exponents, multiplication/division, then addition/subtraction.\n\n"
            "Python also provides the math module for more advanced operations like square roots, "
            "trigonometry, and logarithms. Import it with import math and use functions like "
            "math.sqrt(16) or constants like math.pi."
        ),
        key_terms={
            "int": "A whole number with no fractional part.",
            "float": "A number that includes a decimal point.",
            "Floor division (//)": "Divides and rounds the result down to the nearest integer.",
            "Modulo (%)": "Returns the remainder after division (e.g. 10 % 3 is 1).",
            "Exponentiation (**)": "Raises a number to a power (e.g. 2 ** 10 is 1024).",
        },
        code_examples=[
            CodeExample(
                title="Arithmetic operators",
                code=(
                    "print(7 + 2)\n"
                    "print(7 - 2)\n"
                    "print(7 * 2)\n"
                    "print(7 / 2)\n"
                    "print(7 // 2)\n"
                    "print(7 % 2)\n"
                    "print(7 ** 2)"
                ),
                explanation="All seven arithmetic operators in one example.",
                output="9\n5\n14\n3.5\n3\n1\n49",
                line_notes={
                    4: "[bold]/[/bold] always returns a float, even when the result is a whole number.",
                    5: "[bold]//[/bold] floor division — drops any fraction, so 7 // 2 = 3.",
                    6: "[bold]%[/bold] modulo — gives the remainder: 7 = 3*2 + 1, so remainder is 1.",
                    7: "[bold]**[/bold] exponentiation: 7 squared = 49.",
                },
            ),
            CodeExample(
                title="Using the math module",
                code=(
                    "import math\n"
                    "print(math.sqrt(144))\n"
                    "print(math.pi)\n"
                    "print(math.floor(4.9))"
                ),
                explanation="The math module extends Python's built-in arithmetic.",
                output="12.0\n3.141592653589793\n4",
                line_notes={
                    1: "[bold]import math[/bold] loads the standard library math module.",
                    2: "[bold]math.sqrt()[/bold] returns the square root as a float.",
                    4: "[bold]math.floor()[/bold] rounds down — same as // but works on any float.",
                },
            ),
        ],
        common_mistakes=[
            "Expecting 7/2 to equal 3 — in Python 3, / always gives a float (3.5). Use // for integer division.",
            "Forgetting operator precedence: 2 + 3 * 4 is 14, not 20. Use parentheses to be explicit.",
            "Integer overflow is not an issue in Python — ints can be arbitrarily large.",
            "Floating-point imprecision: 0.1 + 0.2 is not exactly 0.3 due to IEEE 754 representation.",
        ],
        practice_prompts=[
            "What is the difference between / and // in Python? Give an example.",
            "When would the modulo operator % be useful in a real program?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does 9 % 4 evaluate to?",
                qtype="multiple_choice",
                options=["2", "1", "3", "0"],
                correct_answer="1",
                explanation="9 divided by 4 is 2 remainder 1, so 9 % 4 = 1.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In Python 3, the / operator always returns a ____.",
                qtype="fill_blank",
                correct_answer="float",
                explanation="True division (/) always produces a float, even for 4/2 = 2.0.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="2 ** 10 evaluates to 1024.",
                qtype="true_false",
                correct_answer="true",
                explanation="** is the exponentiation operator: 2 to the power 10 = 1024.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b06-ex",
            title="Temperature converter",
            instructions=(
                "Write a program that converts 100 degrees Celsius to Fahrenheit.\n"
                "Formula: fahrenheit = (celsius * 9/5) + 32\n"
                "Print the result as: 100°C is 212.0°F"
            ),
            starter_code=(
                "celsius = 100\n"
                "fahrenheit = ...\n"
                "print(f'{celsius}°C is {fahrenheit}°F')"
            ),
            expected_output="100°C is 212.0°F",
            hints=[
                "Apply the formula: (celsius * 9/5) + 32",
                "The / operator returns a float, so the result will be 212.0.",
                "Use an f-string to embed the variables in the output.",
            ],
            solution=(
                "celsius = 100\n"
                "fahrenheit = (celsius * 9/5) + 32\n"
                "print(f'{celsius}°C is {fahrenheit}°F')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b07",
        title="Booleans",
        level=Level.BEGINNER,
        estimated_minutes=8,
        explanation=(
            "A boolean is a value that is either True or False. Booleans are the foundation of all "
            "decision-making in programs — every if-statement, while-loop, and conditional expression "
            "ultimately tests a boolean value.\n\n"
            "You create booleans through comparison operators: == (equal), != (not equal), < (less than), "
            "> (greater than), <= (less than or equal), >= (greater than or equal). These comparisons "
            "always return True or False. You combine booleans with the logical operators and, or, and not.\n\n"
            "Python also has a concept of 'truthiness': many non-boolean values behave as True or False "
            "in a boolean context. Empty containers ([], '', {}, 0, None) are falsy; everything else is "
            "truthy. This lets you write concise checks like if name: instead of if name != ''."
        ),
        key_terms={
            "bool": "The boolean type — either True or False.",
            "Comparison operator": "An operator that compares two values and returns True or False.",
            "Logical operator": "and, or, not — combine or negate boolean values.",
            "Truthy": "A non-boolean value that Python treats as True in a boolean context.",
            "Falsy": "A non-boolean value that Python treats as False (e.g. 0, '', None, []).",
        },
        code_examples=[
            CodeExample(
                title="Comparison and logical operators",
                code=(
                    "print(5 > 3)\n"
                    "print(5 == 5)\n"
                    "print(5 != 3)\n"
                    "print(True and False)\n"
                    "print(True or False)\n"
                    "print(not True)"
                ),
                explanation="Comparisons return booleans; and/or/not combine them.",
                output="True\nTrue\nTrue\nFalse\nTrue\nFalse",
                line_notes={
                    1: "[bold]>[/bold] greater-than comparison returns True because 5 is greater than 3.",
                    2: "[bold]==[/bold] equality check — do NOT confuse with = (assignment).",
                    4: "[bold]and[/bold] returns True only if BOTH sides are True.",
                    5: "[bold]or[/bold] returns True if AT LEAST ONE side is True.",
                    6: "[bold]not[/bold] flips the boolean: not True → False.",
                },
            ),
            CodeExample(
                title="Truthiness in practice",
                code=(
                    "name = ''\n"
                    "if name:\n"
                    "    print('Name provided')\n"
                    "else:\n"
                    "    print('No name given')"
                ),
                explanation="An empty string is falsy, so the else branch runs.",
                output="No name given",
                line_notes={
                    1: "An empty string is [bold]falsy[/bold] — Python treats it as False.",
                    2: "This if-check works because Python converts name to bool automatically.",
                },
            ),
        ],
        common_mistakes=[
            "Writing if x == True: instead of the more idiomatic if x:.",
            "Confusing = (assignment) with == (comparison) inside conditions.",
            "Assuming and returns True/False — it returns one of its operands (e.g. 1 and 2 returns 2).",
            "Forgetting that 0, 0.0, '', [], {}, and None are all falsy.",
        ],
        practice_prompts=[
            "Give three examples of falsy values in Python and explain why each one makes sense.",
            "What is the difference between and and or in a boolean expression?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which of the following values is falsy in Python?",
                qtype="multiple_choice",
                options=["1", "True", "0", "'False'"],
                correct_answer="0",
                explanation="The integer 0 is falsy. The string 'False' is truthy because it is non-empty.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="True and False evaluates to ____.",
                qtype="fill_blank",
                correct_answer="False",
                explanation="and requires both operands to be True; since False is present, the result is False.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="not False evaluates to True.",
                qtype="true_false",
                correct_answer="true",
                explanation="not flips the boolean value: not False → True.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b07-ex",
            title="Boolean expressions",
            instructions=(
                "Without running the code first, predict the output of each print statement. "
                "Then run it and check your predictions.\n"
                "The four lines should print: True, False, True, False"
            ),
            starter_code=(
                "print(10 > 5)\n"
                "print(10 == 5)\n"
                "print(10 > 5 and 3 < 7)\n"
                "print(10 > 5 and 3 > 7)"
            ),
            expected_output="True\nFalse\nTrue\nFalse",
            hints=[
                "10 > 5 is True, 10 == 5 is False.",
                "and requires BOTH sides to be True.",
                "3 < 7 is True, 3 > 7 is False.",
            ],
            solution=(
                "print(10 > 5)\n"
                "print(10 == 5)\n"
                "print(10 > 5 and 3 < 7)\n"
                "print(10 > 5 and 3 > 7)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b08",
        title="Operators",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Operators are special symbols that perform operations on values. You have already met "
            "arithmetic operators (+, -, *, /) and comparison operators (==, !=, <, >). Python has "
            "several more categories worth knowing.\n\n"
            "Assignment operators let you update a variable in a shorthand way: x += 3 is the same as "
            "x = x + 3. There are versions for all arithmetic operations: -=, *=, /=, //=, %=, **=. "
            "These are read as 'add and assign', 'subtract and assign', etc.\n\n"
            "Membership operators (in, not in) test whether a value exists inside a container. Identity "
            "operators (is, is not) test whether two names refer to the exact same object in memory — "
            "use == for value equality and is only for checking against None. Operator precedence "
            "determines evaluation order; when in doubt, use parentheses to make your intent explicit."
        ),
        key_terms={
            "Augmented assignment": "Shorthand like += that updates and reassigns a variable in one step.",
            "Membership operator": "in and not in — test whether an item is inside a container.",
            "Identity operator": "is and is not — test whether two names point to the same object.",
            "Operator precedence": "The order in which operators are evaluated (PEMDAS/BODMAS).",
            "Unary operator": "An operator that acts on a single operand, e.g. -x or not x.",
        },
        code_examples=[
            CodeExample(
                title="Augmented assignment operators",
                code=(
                    "count = 0\n"
                    "count += 1\n"
                    "print(count)\n"
                    "count *= 10\n"
                    "print(count)"
                ),
                explanation="Augmented assignments update a variable in place with less typing.",
                output="1\n10",
                line_notes={
                    2: "[bold]+=[/bold] adds 1 to count and stores the result back in count.",
                    4: "[bold]*=[/bold] multiplies count by 10 and stores the result.",
                },
            ),
            CodeExample(
                title="Membership and identity operators",
                code=(
                    "fruits = ['apple', 'banana', 'cherry']\n"
                    "print('banana' in fruits)\n"
                    "print('grape' not in fruits)\n"
                    "x = None\n"
                    "print(x is None)"
                ),
                explanation="in tests membership; is tests identity (best reserved for None checks).",
                output="True\nTrue\nTrue",
                line_notes={
                    2: "[bold]in[/bold] checks whether 'banana' exists in the list.",
                    3: "[bold]not in[/bold] checks that 'grape' is absent.",
                    5: "[bold]is None[/bold] is the idiomatic way to check for None — prefer it over == None.",
                },
            ),
        ],
        common_mistakes=[
            "Using = inside a condition (if x = 5:) instead of ==.",
            "Confusing == (value equality) with is (identity) — two equal strings may not be the same object.",
            "Forgetting that is checks identity, not equality: [1,2] is [1,2] is False even though they are equal.",
            "Ignoring operator precedence: not x == y is parsed as not (x == y), which may not be what you intended.",
        ],
        practice_prompts=[
            "What is the difference between x == y and x is y? When should you use each?",
            "Rewrite score = score + 5 using an augmented assignment operator.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does x += 3 mean?",
                qtype="multiple_choice",
                options=["x = 3", "x = x + 3", "x > 3", "x == x + 3"],
                correct_answer="x = x + 3",
                explanation="+= is augmented assignment: add the right side to x and store the result.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The correct way to check if a variable is None is x ____ None.",
                qtype="fill_blank",
                correct_answer="is",
                explanation="Use 'is' for identity checks against None, not ==.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="'cat' in 'concatenate' evaluates to True.",
                qtype="true_false",
                correct_answer="true",
                explanation="The in operator works on strings too, checking for substrings.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b08-ex",
            title="Score tracker",
            instructions=(
                "Start with score = 0. Use augmented assignment to:\n"
                "1. Add 10 points\n"
                "2. Multiply the score by 3\n"
                "3. Subtract 5 points\n"
                "Print the final score."
            ),
            starter_code=(
                "score = 0\n"
                "score ...\n"
                "score ...\n"
                "score ...\n"
                "print(score)"
            ),
            expected_output="25",
            hints=[
                "Use += 10 to add 10.",
                "Use *= 3 to multiply by 3.",
                "Use -= 5 to subtract 5.",
                "0 + 10 = 10, 10 * 3 = 30, 30 - 5 = 25.",
            ],
            solution=(
                "score = 0\n"
                "score += 10\n"
                "score *= 3\n"
                "score -= 5\n"
                "print(score)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b09",
        title="Input and Output",
        level=Level.BEGINNER,
        estimated_minutes=8,
        explanation=(
            "Programs become much more useful when they can communicate with the user. In Python, "
            "print() handles output and input() handles input. You have used print() already; input() "
            "is just as simple — it pauses the program, shows an optional prompt, waits for the user "
            "to type something and press Enter, then returns what they typed as a string.\n\n"
            "Because input() always returns a string, you often need to convert the result before using "
            "it in arithmetic. If you ask for a number, wrap the call in int() or float(): "
            "age = int(input('Enter your age: ')). Forgetting this conversion is one of the most common "
            "beginner mistakes.\n\n"
            "print() accepts multiple arguments separated by commas, adds a space between them, and ends "
            "with a newline by default. You can change the separator with sep= and the line ending with "
            "end=. For example, print('a', 'b', sep='-') prints a-b."
        ),
        key_terms={
            "input()": "Built-in function that reads a line of text from the user and returns it as a string.",
            "print()": "Built-in function that writes values to standard output.",
            "Prompt": "The optional message passed to input() that tells the user what to type.",
            "Standard input": "The default source for user input — usually the keyboard.",
            "sep": "The print() keyword argument that sets the separator between values (default: space).",
        },
        code_examples=[
            CodeExample(
                title="Getting user input",
                code=(
                    "name = input('What is your name? ')\n"
                    "print(f'Hello, {name}!')"
                ),
                explanation="input() reads a line of text and stores it in name.",
                output="What is your name? Alice\nHello, Alice!",
                line_notes={
                    1: "[bold]input()[/bold] shows the prompt, waits for the user, then returns what they typed as a string.",
                    2: "The f-string embeds the user's input into the greeting.",
                },
            ),
            CodeExample(
                title="Converting input to a number",
                code=(
                    "year_str = input('Enter the current year: ')\n"
                    "year = int(year_str)\n"
                    "birth_year = year - 30\n"
                    "print(f'Thirty years ago it was {birth_year}.')"
                ),
                explanation="input() always returns a string; convert before doing arithmetic.",
                output="Enter the current year: 2024\nThirty years ago it was 1994.",
                line_notes={
                    1: "input() returns a string — '2024', not 2024.",
                    2: "[bold]int()[/bold] converts the string to an integer so arithmetic works.",
                    3: "Now year is an int, so subtraction is valid.",
                },
            ),
        ],
        common_mistakes=[
            "Trying to do math on input() without converting: input() + 1 raises TypeError.",
            "Forgetting the space at the end of the prompt string — 'Enter name:' looks cramped.",
            "Using print to 'return' a value from a function (those are different things).",
            "Not handling invalid input — int('hello') raises ValueError if the user types text.",
        ],
        practice_prompts=[
            "Why does input() always return a string, even when the user types a number?",
            "How would you ask a user for a floating-point number and convert it properly?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What type does input() always return?",
                qtype="multiple_choice",
                options=["int", "float", "str", "bool"],
                correct_answer="str",
                explanation="input() returns a string regardless of what the user types.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="To read a number from the user, you should wrap input() in ____().",
                qtype="fill_blank",
                correct_answer="int",
                explanation="int(input(...)) converts the string returned by input() to an integer.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="print('a', 'b', sep='-') outputs a-b.",
                qtype="true_false",
                correct_answer="true",
                explanation="The sep keyword argument replaces the default space separator.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b09-ex",
            title="Simple greeting app",
            instructions=(
                "Ask the user for their name and age. Then print:\n"
                "Hello, <name>! In 10 years you will be <age+10>."
            ),
            starter_code=(
                "name = input('Your name: ')\n"
                "age = ...(input('Your age: '))\n"
                "print(f'Hello, {name}! In 10 years you will be {age + 10}.')"
            ),
            expected_output="Hello, Alice! In 10 years you will be 40.",
            hints=[
                "input() returns a string, so convert age with int().",
                "Use an f-string and embed age + 10 inside the braces.",
            ],
            solution=(
                "name = input('Your name: ')\n"
                "age = int(input('Your age: '))\n"
                "print(f'Hello, {name}! In 10 years you will be {age + 10}.')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b10",
        title="Lists",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "A list is an ordered, mutable collection of items enclosed in square brackets: "
            "[1, 2, 3] or ['apple', 'banana']. Lists can hold any type of value — even a mix of types "
            "— and can grow or shrink after creation. They are one of the most used data structures in Python.\n\n"
            "You access items by their zero-based index: fruits[0] is the first item. Negative indices "
            "count from the end: fruits[-1] is the last item. Slicing with fruits[1:3] returns a new list "
            "containing items at indices 1 and 2 (the end index is exclusive).\n\n"
            "Common list methods include .append(item) to add to the end, .remove(item) to delete the "
            "first match, .pop(index) to remove and return an item, .sort() to sort in place, and "
            ".len() — actually len(my_list) as a built-in — to get the count. Lists are everywhere in "
            "Python programs: storing rows of data, queuing tasks, collecting user responses, and more."
        ),
        key_terms={
            "List": "An ordered, mutable sequence of items defined with square brackets.",
            "Index": "The integer position of an item in a list, starting at 0.",
            "Slice": "A portion of a list extracted with the [start:end] syntax.",
            "append()": "List method that adds one item to the end.",
            "Mutable": "Can be changed after creation — unlike strings or tuples.",
        },
        code_examples=[
            CodeExample(
                title="Creating and accessing lists",
                code=(
                    "colors = ['red', 'green', 'blue']\n"
                    "print(colors[0])\n"
                    "print(colors[-1])\n"
                    "print(colors[0:2])\n"
                    "print(len(colors))"
                ),
                explanation="Indexing and slicing let you reach any subset of a list.",
                output="red\nblue\n['red', 'green']\n3",
                line_notes={
                    2: "Index [bold]0[/bold] is the first item.",
                    3: "Index [bold]-1[/bold] is the last item — handy when you don't know the length.",
                    4: "[bold][0:2][/bold] slices from index 0 up to (but not including) index 2.",
                    5: "[bold]len()[/bold] returns the total number of items.",
                },
            ),
            CodeExample(
                title="Modifying a list",
                code=(
                    "nums = [3, 1, 4, 1, 5]\n"
                    "nums.append(9)\n"
                    "nums.remove(1)\n"
                    "nums.sort()\n"
                    "print(nums)"
                ),
                explanation="Lists are mutable — you can add, remove, and reorder items.",
                output="[1, 3, 4, 5, 9]",
                line_notes={
                    2: "[bold].append()[/bold] adds 9 to the end of nums.",
                    3: "[bold].remove(1)[/bold] deletes only the FIRST occurrence of 1.",
                    4: "[bold].sort()[/bold] sorts in place (ascending by default).",
                },
            ),
        ],
        common_mistakes=[
            "IndexError: forgetting that a list of 3 items has indices 0, 1, 2 — index 3 is out of range.",
            "Confusing .append([1,2]) (adds a nested list) with .extend([1,2]) (adds individual items).",
            "Sorting a list that mixes types (e.g. [1, 'a']) — Python 3 raises TypeError.",
            "Forgetting that slice end is exclusive: my_list[0:3] gives items at indices 0, 1, 2.",
        ],
        practice_prompts=[
            "What is the difference between list[2] and list[2:4]?",
            "If you need to keep items in insertion order and be able to change them, which Python type would you use?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What index does the last item of a list always have?",
                qtype="multiple_choice",
                options=["len(list)", "len(list) - 1", "-0", "last"],
                correct_answer="len(list) - 1",
                explanation="Indices start at 0, so a list with n items has indices 0 through n-1. You can also use -1.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The list method that adds an item to the end is ____().",
                qtype="fill_blank",
                correct_answer="append",
                explanation="list.append(item) adds a single item to the end of the list.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Lists in Python are immutable and cannot be changed after creation.",
                qtype="true_false",
                correct_answer="false",
                explanation="Lists are mutable — you can add, remove, and change items freely.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b10-ex",
            title="Shopping list manager",
            instructions=(
                "Start with shopping = ['milk', 'eggs']. "
                "Append 'bread', remove 'eggs', then print the sorted list."
            ),
            starter_code=(
                "shopping = ['milk', 'eggs']\n"
                "# Add 'bread'\n"
                "...\n"
                "# Remove 'eggs'\n"
                "...\n"
                "shopping.sort()\n"
                "print(shopping)"
            ),
            expected_output="['bread', 'milk']",
            hints=[
                "Use shopping.append('bread') to add bread.",
                "Use shopping.remove('eggs') to remove eggs.",
                ".sort() modifies the list in place.",
            ],
            solution=(
                "shopping = ['milk', 'eggs']\n"
                "shopping.append('bread')\n"
                "shopping.remove('eggs')\n"
                "shopping.sort()\n"
                "print(shopping)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b11",
        title="Tuples",
        level=Level.BEGINNER,
        estimated_minutes=8,
        explanation=(
            "A tuple is like a list but immutable — once created, its items cannot be changed, added, "
            "or removed. Tuples are written with parentheses: (1, 2, 3) or just 1, 2, 3 (parentheses "
            "are often optional). A single-item tuple needs a trailing comma: (42,).\n\n"
            "Because tuples are immutable, Python can make them faster and more memory-efficient than "
            "lists. Use a tuple when the collection represents a fixed group of values that should not "
            "change — like a point (x, y), RGB colour (255, 128, 0), or a database row.\n\n"
            "You can unpack a tuple into separate variables: x, y = (3, 7) assigns 3 to x and 7 to y. "
            "This is called tuple unpacking and works for any sequence. Functions often return multiple "
            "values as tuples, and unpacking is the clean way to receive them."
        ),
        key_terms={
            "Tuple": "An ordered, immutable sequence defined with parentheses.",
            "Immutable": "Cannot be changed after creation.",
            "Tuple unpacking": "Assigning the items of a tuple to separate variables in one statement.",
            "Trailing comma": "The comma after a single item that makes it a tuple: (42,).",
        },
        code_examples=[
            CodeExample(
                title="Creating and using tuples",
                code=(
                    "point = (3, 7)\n"
                    "print(point[0])\n"
                    "print(len(point))\n"
                    "x, y = point\n"
                    "print(f'x={x}, y={y}')"
                ),
                explanation="Tuples support indexing and len(), and can be unpacked.",
                output="3\n2\nx=3, y=7",
                line_notes={
                    1: "A tuple is created with parentheses. Indexing works just like lists.",
                    4: "[bold]Tuple unpacking[/bold] — assigns 3 to x and 7 to y in one line.",
                },
            ),
            CodeExample(
                title="Tuple immutability",
                code=(
                    "rgb = (255, 128, 0)\n"
                    "# rgb[0] = 100  # This would raise TypeError\n"
                    "print(rgb)"
                ),
                explanation="Attempting to change a tuple item raises a TypeError.",
                output="(255, 128, 0)",
                line_notes={
                    2: "This line is commented out because [bold]tuples are immutable[/bold] — assignment would fail.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting the trailing comma for single-item tuples: (42) is just 42 (an int), not a tuple.",
            "Trying to modify a tuple element — this raises TypeError.",
            "Treating tuples and lists as interchangeable — choose based on mutability needs.",
        ],
        practice_prompts=[
            "When would you choose a tuple over a list to store data?",
            "What does tuple unpacking look like, and why is it convenient?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which of the following correctly creates a single-element tuple?",
                qtype="multiple_choice",
                options=["(42)", "(42,)", "[42]", "{42}"],
                correct_answer="(42,)",
                explanation="A trailing comma is required for a single-element tuple; (42) is just the integer 42.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Tuples are ____, meaning they cannot be changed after creation.",
                qtype="fill_blank",
                correct_answer="immutable",
                explanation="Immutability is the key distinguishing feature of tuples versus lists.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="You can unpack a tuple's values into separate variables.",
                qtype="true_false",
                correct_answer="true",
                explanation="x, y = (3, 7) assigns 3 to x and 7 to y in one statement.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b11-ex",
            title="Coordinate unpacking",
            instructions=(
                "Given the tuple location = (40.7128, -74.0060) (latitude, longitude of New York), "
                "unpack it into lat and lon, then print: Lat: 40.7128, Lon: -74.006"
            ),
            starter_code=(
                "location = (40.7128, -74.0060)\n"
                "lat, lon = ...\n"
                "print(f'Lat: {lat}, Lon: {lon}')"
            ),
            expected_output="Lat: 40.7128, Lon: -74.006",
            hints=[
                "Use lat, lon = location to unpack.",
                "The f-string handles the formatting automatically.",
            ],
            solution=(
                "location = (40.7128, -74.0060)\n"
                "lat, lon = location\n"
                "print(f'Lat: {lat}, Lon: {lon}')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b12",
        title="Dictionaries",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "A dictionary (dict) stores key-value pairs. Instead of using an integer index to look up "
            "items, you use meaningful keys. A dict is defined with curly braces: "
            "{'name': 'Alice', 'age': 30}. Keys are usually strings or numbers; values can be anything.\n\n"
            "Access a value with dict[key], update it with dict[key] = new_value, and add a new pair "
            "the same way. Delete a key with del dict[key] or dict.pop(key). Check whether a key exists "
            "with 'key' in dict. Iterate over keys with for key in dict, over values with "
            "dict.values(), and over pairs with dict.items().\n\n"
            "Dictionaries are the go-to structure whenever you need to look something up by name rather "
            "than position: configuration settings, word frequencies, user profiles, JSON data from an "
            "API. As of Python 3.7, dictionaries maintain insertion order."
        ),
        key_terms={
            "Dictionary": "A mutable mapping of unique keys to values, defined with curly braces.",
            "Key": "The identifier used to look up a value in a dict — must be hashable (e.g. string, int).",
            "Value": "The data associated with a key in a dict.",
            "Key-value pair": "One entry in a dictionary: a key and its associated value.",
            ".items()": "Dict method that returns key-value pairs as tuples for iteration.",
            ".get()": "Dict method that returns a value for a key, or a default if the key is absent.",
        },
        code_examples=[
            CodeExample(
                title="Creating and accessing a dict",
                code=(
                    "person = {'name': 'Bob', 'age': 28, 'city': 'London'}\n"
                    "print(person['name'])\n"
                    "print(person.get('country', 'Unknown'))\n"
                    "person['age'] = 29\n"
                    "print(person['age'])"
                ),
                explanation="Dicts are accessed by key; .get() avoids KeyError for missing keys.",
                output="Bob\nUnknown\n29",
                line_notes={
                    2: "Access a value with [bold]dict[key][/bold] — raises KeyError if key is absent.",
                    3: "[bold].get(key, default)[/bold] returns 'Unknown' instead of raising an error.",
                    4: "Assigning to an existing key updates its value.",
                },
            ),
            CodeExample(
                title="Iterating a dictionary",
                code=(
                    "scores = {'Alice': 95, 'Bob': 82, 'Carol': 90}\n"
                    "for name, score in scores.items():\n"
                    "    print(f'{name}: {score}')"
                ),
                explanation=".items() lets you loop over key-value pairs together.",
                output="Alice: 95\nBob: 82\nCarol: 90",
                line_notes={
                    2: "[bold].items()[/bold] returns each key-value pair as a tuple; we unpack into name and score.",
                },
            ),
        ],
        common_mistakes=[
            "Using dict[missing_key] — raises KeyError. Use .get() when the key might not exist.",
            "Using mutable types (lists) as keys — dict keys must be hashable; use tuples instead.",
            "Forgetting that dict.keys(), dict.values(), dict.items() return view objects, not lists.",
            "Confusing {} (empty dict) with set() (empty set) — both use curly braces.",
        ],
        practice_prompts=[
            "When would you use a dictionary instead of a list to store data?",
            "What is the difference between dict[key] and dict.get(key)?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which method safely retrieves a value without raising a KeyError if the key is missing?",
                qtype="multiple_choice",
                options=["dict[key]", "dict.get(key)", "dict.fetch(key)", "dict.find(key)"],
                correct_answer="dict.get(key)",
                explanation=".get() returns None (or a provided default) when the key is absent.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="To iterate over key-value pairs of a dict, use dict.____().",
                qtype="fill_blank",
                correct_answer="items",
                explanation="dict.items() returns (key, value) tuples you can unpack in a for loop.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Dictionary keys must be unique — duplicate keys are not allowed.",
                qtype="true_false",
                correct_answer="true",
                explanation="If you assign to a duplicate key, it overwrites the previous value.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b12-ex",
            title="Word frequency counter",
            instructions=(
                "Given the list words = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat'], "
                "build a dictionary that maps each word to how many times it appears, "
                "then print each word and its count."
            ),
            starter_code=(
                "words = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat']\n"
                "freq = {}\n"
                "for word in words:\n"
                "    freq[word] = freq.get(word, 0) + 1\n"
                "for word, count in freq.items():\n"
                "    print(f'{word}: {count}')"
            ),
            expected_output="cat: 3\ndog: 2\nbird: 1",
            hints=[
                "Use .get(word, 0) to return 0 if the word hasn't been seen yet.",
                "Add 1 to the existing count each iteration.",
                "Iterate over freq.items() to print each pair.",
            ],
            solution=(
                "words = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat']\n"
                "freq = {}\n"
                "for word in words:\n"
                "    freq[word] = freq.get(word, 0) + 1\n"
                "for word, count in freq.items():\n"
                "    print(f'{word}: {count}')"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b13",
        title="Sets",
        level=Level.BEGINNER,
        estimated_minutes=8,
        explanation=(
            "A set is an unordered collection of unique items. It is created with curly braces "
            "{1, 2, 3} or the set() constructor. Because sets enforce uniqueness, they automatically "
            "remove duplicates — set([1, 2, 2, 3]) gives {1, 2, 3}.\n\n"
            "Sets are fast at membership testing (x in my_set is very quick, even for huge sets) "
            "because they use a hash table internally. They also support standard mathematical set "
            "operations: union (|), intersection (&), difference (-), and symmetric difference (^).\n\n"
            "Sets are unordered, so you cannot index them (my_set[0] raises TypeError). Use a set "
            "when you care about uniqueness or need fast membership tests, but do not need to access "
            "items by position."
        ),
        key_terms={
            "Set": "An unordered collection of unique, hashable items.",
            "Union (|)": "Combines two sets, keeping all items from both.",
            "Intersection (&)": "Returns only items that appear in both sets.",
            "Difference (-)": "Returns items in the first set that are not in the second.",
            "Hashable": "An object that has a consistent hash value — required to be stored in a set.",
        },
        code_examples=[
            CodeExample(
                title="Creating sets and removing duplicates",
                code=(
                    "tags = {'python', 'code', 'python', 'learn'}\n"
                    "print(tags)\n"
                    "tags.add('fun')\n"
                    "tags.discard('code')\n"
                    "print('python' in tags)"
                ),
                explanation="Sets deduplicate automatically and support fast membership tests.",
                output="{'python', 'code', 'learn'}\nTrue",
                line_notes={
                    1: "The duplicate 'python' is silently dropped — sets only store unique items.",
                    3: "[bold].add()[/bold] inserts a new item (does nothing if it already exists).",
                    4: "[bold].discard()[/bold] removes an item without raising an error if absent (unlike .remove()).",
                    5: "[bold]in[/bold] with a set is very fast — O(1) on average.",
                },
            ),
            CodeExample(
                title="Set operations",
                code=(
                    "a = {1, 2, 3, 4}\n"
                    "b = {3, 4, 5, 6}\n"
                    "print(a | b)\n"
                    "print(a & b)\n"
                    "print(a - b)"
                ),
                explanation="Set operators mirror mathematical Venn diagram operations.",
                output="{1, 2, 3, 4, 5, 6}\n{3, 4}\n{1, 2}",
                line_notes={
                    3: "[bold]|[/bold] union — all items from both sets.",
                    4: "[bold]&[/bold] intersection — only items in BOTH sets.",
                    5: "[bold]-[/bold] difference — items in a but NOT in b.",
                },
            ),
        ],
        common_mistakes=[
            "Trying to index a set: my_set[0] raises TypeError — sets are unordered.",
            "Creating an empty set with {} — that creates an empty dict. Use set() instead.",
            "Storing mutable items (like lists) in a set — they must be hashable; use tuples.",
        ],
        practice_prompts=[
            "When would removing duplicates from a list be useful? How would you use a set to do it?",
            "What is the difference between .remove() and .discard() on a set?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does set([1, 2, 2, 3, 3]) produce?",
                qtype="multiple_choice",
                options=["{1, 2, 2, 3, 3}", "{1, 2, 3}", "[1, 2, 3]", "(1, 2, 3)"],
                correct_answer="{1, 2, 3}",
                explanation="Sets automatically deduplicate — only unique values are kept.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="To create an empty set you use ____().",
                qtype="fill_blank",
                correct_answer="set",
                explanation="{} creates an empty dict, not an empty set. Use set() for an empty set.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Sets in Python maintain insertion order.",
                qtype="true_false",
                correct_answer="false",
                explanation="Sets are unordered — the iteration order is not guaranteed.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b13-ex",
            title="Find unique visitors",
            instructions=(
                "Given visitors = ['alice', 'bob', 'alice', 'carol', 'bob', 'alice'], "
                "find the number of unique visitors and print it."
            ),
            starter_code=(
                "visitors = ['alice', 'bob', 'alice', 'carol', 'bob', 'alice']\n"
                "unique = ...\n"
                "print(f'Unique visitors: {len(unique)}')"
            ),
            expected_output="Unique visitors: 3",
            hints=[
                "Convert the list to a set to remove duplicates.",
                "Use len() on the resulting set.",
            ],
            solution=(
                "visitors = ['alice', 'bob', 'alice', 'carol', 'bob', 'alice']\n"
                "unique = set(visitors)\n"
                "print(f'Unique visitors: {len(unique)}')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b14",
        title="Conditionals",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Conditionals let your program make decisions. The if statement checks a condition; if it "
            "is True, Python runs the indented block below it. You can add an elif (else-if) for "
            "additional conditions, and an else for the fallback case. Only the first matching branch runs.\n\n"
            "Python uses indentation (consistently 4 spaces by convention) to define blocks — there "
            "are no curly braces. Getting indentation wrong is one of the most common syntax errors "
            "for new programmers. An IndentationError means a block is not indented correctly.\n\n"
            "For simple two-branch decisions, Python has a one-line ternary expression: "
            "value = 'yes' if condition else 'no'. This is handy for assigning a variable based on a "
            "condition without a full if/else block, but do not overuse it — clarity beats brevity."
        ),
        key_terms={
            "if": "Keyword that starts a conditional block, executed only when the condition is True.",
            "elif": "Short for 'else if' — checks a second condition when the previous ones were False.",
            "else": "The fallback block that runs when no preceding if/elif condition was True.",
            "Indentation": "The leading whitespace (4 spaces) that defines a code block in Python.",
            "Ternary expression": "A one-line if/else: value = x if condition else y.",
        },
        code_examples=[
            CodeExample(
                title="if, elif, else",
                code=(
                    "score = 75\n"
                    "if score >= 90:\n"
                    "    print('Grade: A')\n"
                    "elif score >= 70:\n"
                    "    print('Grade: B')\n"
                    "elif score >= 50:\n"
                    "    print('Grade: C')\n"
                    "else:\n"
                    "    print('Grade: F')"
                ),
                explanation="Multiple conditions are checked in order; the first True branch runs.",
                output="Grade: B",
                line_notes={
                    2: "Python checks this first — 75 >= 90 is False, so skip this block.",
                    4: "75 >= 70 is True — this block runs.",
                    8: "The [bold]else[/bold] block only runs if ALL conditions above were False.",
                },
            ),
            CodeExample(
                title="Ternary expression",
                code=(
                    "age = 20\n"
                    "status = 'adult' if age >= 18 else 'minor'\n"
                    "print(status)"
                ),
                explanation="A ternary assigns one of two values based on a condition.",
                output="adult",
                line_notes={
                    2: "Read as: 'adult' if the condition is True, otherwise 'minor'.",
                },
            ),
        ],
        common_mistakes=[
            "Using = instead of == in a condition: if x = 5: is a SyntaxError.",
            "Inconsistent indentation — mixing tabs and spaces causes IndentationError.",
            "Forgetting the colon (:) at the end of if, elif, or else lines.",
            "Writing unnecessary else after a return in a function — the else is redundant.",
        ],
        practice_prompts=[
            "What happens if you write multiple if statements instead of elif? Is the result the same?",
            "When is the ternary expression more readable than a full if/else block?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="In Python, code blocks are defined by ____.",
                qtype="multiple_choice",
                options=["curly braces {}", "parentheses ()", "indentation", "the colon :"],
                correct_answer="indentation",
                explanation="Python uses consistent indentation (4 spaces) to delimit blocks instead of braces.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The keyword ____ is used for a second condition in a chain.",
                qtype="fill_blank",
                correct_answer="elif",
                explanation="elif means 'else if' — it checks a new condition only when earlier ones were False.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="If the if condition is True, the elif and else blocks are still evaluated.",
                qtype="true_false",
                correct_answer="false",
                explanation="Once a True branch is found, Python skips all remaining elif and else blocks.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b14-ex",
            title="FizzBuzz (single number)",
            instructions=(
                "Given number = 15, print 'FizzBuzz' if it is divisible by both 3 and 5, "
                "'Fizz' if only by 3, 'Buzz' if only by 5, otherwise print the number itself."
            ),
            starter_code=(
                "number = 15\n"
                "if ...:\n"
                "    print('FizzBuzz')\n"
                "elif ...:\n"
                "    print('Fizz')\n"
                "elif ...:\n"
                "    print('Buzz')\n"
                "else:\n"
                "    print(number)"
            ),
            expected_output="FizzBuzz",
            hints=[
                "Use % to check divisibility: number % 3 == 0.",
                "Check divisibility by both 3 AND 5 first using and.",
                "Order matters — check the combined condition before the individual ones.",
            ],
            solution=(
                "number = 15\n"
                "if number % 3 == 0 and number % 5 == 0:\n"
                "    print('FizzBuzz')\n"
                "elif number % 3 == 0:\n"
                "    print('Fizz')\n"
                "elif number % 5 == 0:\n"
                "    print('Buzz')\n"
                "else:\n"
                "    print(number)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b15",
        title="Loops",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "Loops let you repeat code without copying and pasting it. Python has two kinds of loops. "
            "A for loop iterates over a sequence — a list, string, range, or any other iterable — "
            "running its body once for each item. A while loop keeps running as long as a condition "
            "is True, and stops when the condition becomes False.\n\n"
            "range(n) generates integers from 0 up to (but not including) n, making it the standard "
            "way to repeat something n times. range(start, stop, step) gives you more control. "
            "The built-in enumerate(iterable) pairs each item with its index, so you can loop over "
            "both at once: for i, item in enumerate(my_list).\n\n"
            "Two control keywords change loop flow: break exits the loop immediately, and continue "
            "skips the rest of the current iteration and moves to the next one. Use them sparingly — "
            "clear loop conditions are usually easier to read."
        ),
        key_terms={
            "for loop": "Iterates over each item in a sequence, executing the body once per item.",
            "while loop": "Repeats a block as long as a given condition remains True.",
            "range()": "Generates a sequence of integers, commonly used with for loops.",
            "break": "Exits the enclosing loop immediately.",
            "continue": "Skips the remainder of the current iteration and proceeds to the next.",
            "enumerate()": "Returns (index, value) pairs when iterating, so you have both at once.",
        },
        code_examples=[
            CodeExample(
                title="for loop with range and enumerate",
                code=(
                    "fruits = ['apple', 'banana', 'cherry']\n"
                    "for i, fruit in enumerate(fruits):\n"
                    "    print(f'{i}: {fruit}')"
                ),
                explanation="enumerate gives both the index and the value in each iteration.",
                output="0: apple\n1: banana\n2: cherry",
                line_notes={
                    2: "[bold]enumerate(fruits)[/bold] yields (0, 'apple'), (1, 'banana'), (2, 'cherry').",
                    3: "f-string embeds both [bold]i[/bold] (index) and [bold]fruit[/bold] (value).",
                },
            ),
            CodeExample(
                title="while loop with break",
                code=(
                    "count = 1\n"
                    "while count <= 5:\n"
                    "    print(count)\n"
                    "    count += 1"
                ),
                explanation="The while loop runs as long as count <= 5.",
                output="1\n2\n3\n4\n5",
                line_notes={
                    2: "The condition is checked [bold]before[/bold] each iteration.",
                    4: "[bold]count += 1[/bold] is essential — forgetting it creates an infinite loop!",
                },
            ),
        ],
        common_mistakes=[
            "Infinite while loop: forgetting to update the variable the condition depends on.",
            "Modifying a list while iterating over it — this can skip items or cause errors.",
            "Using range(len(my_list)) when enumerate(my_list) is clearer and more Pythonic.",
            "Off-by-one with range: range(5) gives 0–4, not 1–5.",
        ],
        practice_prompts=[
            "When would you use a while loop instead of a for loop?",
            "What would happen if you forgot count += 1 inside a while loop?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does range(3) produce?",
                qtype="multiple_choice",
                options=["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "(0, 1, 2)"],
                correct_answer="[0, 1, 2]",
                explanation="range(n) starts at 0 and goes up to (but not including) n.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The ____ keyword exits a loop immediately.",
                qtype="fill_blank",
                correct_answer="break",
                explanation="break stops the loop and continues execution after the loop body.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="continue skips the rest of the current iteration and moves to the next one.",
                qtype="true_false",
                correct_answer="true",
                explanation="continue does not exit the loop — it just jumps to the next iteration.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What built-in function gives you both the index and value when looping over a list?",
                qtype="short_answer",
                correct_answer="enumerate",
                keywords=["enumerate"],
                explanation="enumerate(iterable) yields (index, value) pairs.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b15-ex",
            title="Sum of squares",
            instructions=(
                "Use a for loop and range() to compute the sum of squares from 1 to 5 "
                "(1² + 2² + 3² + 4² + 5²) and print the result."
            ),
            starter_code=(
                "total = 0\n"
                "for n in range(1, 6):\n"
                "    total += ...\n"
                "print(total)"
            ),
            expected_output="55",
            hints=[
                "range(1, 6) gives 1, 2, 3, 4, 5.",
                "Use n ** 2 to square each number.",
                "1 + 4 + 9 + 16 + 25 = 55.",
            ],
            solution=(
                "total = 0\n"
                "for n in range(1, 6):\n"
                "    total += n ** 2\n"
                "print(total)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b16",
        title="Functions",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "A function is a reusable block of code with a name. You define it once with def and call "
            "it as many times as you need. Functions help you organise code, avoid repetition, and "
            "make programs easier to test and maintain.\n\n"
            "A function can accept input through parameters (the names listed in the def line) and "
            "return output with the return statement. If no return is written, the function returns "
            "None. Parameters can have default values: def greet(name, greeting='Hello') allows the "
            "caller to omit greeting and it defaults to 'Hello'.\n\n"
            "Good functions do one thing, have a clear name that describes what they do, and are "
            "short enough to read in a glance. A docstring — a string on the first line of the "
            "function body — documents what the function does and is shown by help()."
        ),
        key_terms={
            "def": "Keyword that starts a function definition.",
            "Parameter": "A variable name listed in the function definition that receives a value when called.",
            "Argument": "The actual value passed to a function when calling it.",
            "return": "Sends a value back to the caller and exits the function.",
            "Docstring": "A string literal on the first line of a function body that documents its purpose.",
            "Default parameter": "A parameter with a preset value used when no argument is provided.",
        },
        code_examples=[
            CodeExample(
                title="Defining and calling a function",
                code=(
                    "def greet(name, greeting='Hello'):\n"
                    '    """Return a personalised greeting."""\n'
                    "    return f'{greeting}, {name}!'\n"
                    "\n"
                    "print(greet('Alice'))\n"
                    "print(greet('Bob', 'Hi'))"
                ),
                explanation="A function with a default parameter and a docstring.",
                output="Hello, Alice!\nHi, Bob!",
                line_notes={
                    1: "[bold]def[/bold] starts the definition. [bold]greeting='Hello'[/bold] is a default parameter.",
                    2: "The [bold]docstring[/bold] describes what the function does — shown by help().",
                    3: "[bold]return[/bold] sends the f-string value back to whoever called the function.",
                    5: "Called with one argument — greeting uses its default value 'Hello'.",
                    6: "Called with two arguments — greeting becomes 'Hi'.",
                },
            ),
            CodeExample(
                title="Function that returns multiple values",
                code=(
                    "def min_max(numbers):\n"
                    "    return min(numbers), max(numbers)\n"
                    "\n"
                    "low, high = min_max([4, 1, 9, 2, 7])\n"
                    "print(f'Min: {low}, Max: {high}')"
                ),
                explanation="Functions can return a tuple; unpack it into separate variables.",
                output="Min: 1, Max: 9",
                line_notes={
                    2: "Returning two values implicitly creates a tuple.",
                    4: "Tuple unpacking assigns both return values in one line.",
                },
            ),
        ],
        common_mistakes=[
            "Calling a function before defining it — Python raises NameError.",
            "Forgetting return — the function returns None silently, which is hard to debug.",
            "Using a mutable default argument like def f(lst=[]) — the default list is shared across all calls.",
            "Confusing parameters (in the def) with arguments (the values you pass when calling).",
        ],
        practice_prompts=[
            "What is the difference between a parameter and an argument?",
            "Why is it dangerous to use a mutable object (like a list) as a default parameter?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What keyword is used to send a value back from a function?",
                qtype="multiple_choice",
                options=["send", "yield", "return", "output"],
                correct_answer="return",
                explanation="return exits the function and passes a value back to the caller.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="If a function has no return statement, it returns ____.",
                qtype="fill_blank",
                correct_answer="None",
                explanation="Python implicitly returns None when a function reaches the end without a return.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A function can return more than one value.",
                qtype="true_false",
                correct_answer="true",
                explanation="Returning multiple values creates a tuple: return a, b is equivalent to return (a, b).",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b16-ex",
            title="Area calculator function",
            instructions=(
                "Write a function called rectangle_area(width, height) that returns the area "
                "(width * height). Then call it with width=5 and height=3 and print the result."
            ),
            starter_code=(
                "def rectangle_area(width, height):\n"
                "    ...\n"
                "\n"
                "area = rectangle_area(5, 3)\n"
                "print(area)"
            ),
            expected_output="15",
            hints=[
                "Use return inside the function body.",
                "return width * height will do it.",
                "Call the function with the two arguments and store the result.",
            ],
            solution=(
                "def rectangle_area(width, height):\n"
                "    return width * height\n"
                "\n"
                "area = rectangle_area(5, 3)\n"
                "print(area)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b17",
        title="Scope",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Scope determines where in your program a variable can be accessed. Python uses the LEGB "
            "rule: it looks up a name in Local scope first, then the Enclosing scope (for nested "
            "functions), then Global scope, then Built-ins. A variable created inside a function is "
            "local — it only exists for the duration of that call.\n\n"
            "A global variable is defined at the top level of a module, outside any function. "
            "Functions can read global variables freely, but to reassign one from inside a function "
            "you must declare it with the global keyword. Without global, the assignment creates a "
            "new local variable that shadows the global one — a common source of subtle bugs.\n\n"
            "The cleanest approach is to pass values in as arguments and return results — this makes "
            "dependencies explicit and avoids relying on global state. Reserve global variables for "
            "true constants (like MAX_SIZE = 100) that never change."
        ),
        key_terms={
            "Scope": "The region of code where a variable name is visible and accessible.",
            "Local variable": "A variable created inside a function — only visible within that function.",
            "Global variable": "A variable defined at the module level, outside any function.",
            "LEGB rule": "The order Python searches for a name: Local, Enclosing, Global, Built-in.",
            "global keyword": "Declares that an assignment inside a function refers to the global variable.",
            "Shadowing": "Defining a local variable with the same name as a global, hiding the global.",
        },
        code_examples=[
            CodeExample(
                title="Local vs global scope",
                code=(
                    "message = 'Hello from global'\n"
                    "\n"
                    "def show():\n"
                    "    message = 'Hello from local'\n"
                    "    print(message)\n"
                    "\n"
                    "show()\n"
                    "print(message)"
                ),
                explanation="The function creates its own local message — it does not change the global one.",
                output="Hello from local\nHello from global",
                line_notes={
                    1: "This is the [bold]global[/bold] message variable.",
                    4: "A new [bold]local[/bold] message is created inside show() — shadows the global.",
                    8: "The global message is unchanged after the function call.",
                },
            ),
            CodeExample(
                title="Using the global keyword",
                code=(
                    "counter = 0\n"
                    "\n"
                    "def increment():\n"
                    "    global counter\n"
                    "    counter += 1\n"
                    "\n"
                    "increment()\n"
                    "increment()\n"
                    "print(counter)"
                ),
                explanation="global lets the function modify the module-level counter.",
                output="2",
                line_notes={
                    4: "[bold]global counter[/bold] tells Python to use the module-level variable, not create a local one.",
                    5: "Now += modifies the global counter.",
                },
            ),
        ],
        common_mistakes=[
            "Expecting a local variable to persist between function calls — it is recreated each time.",
            "Forgetting global inside a function and getting UnboundLocalError when trying to use +=.",
            "Overusing global variables — makes code harder to test and understand.",
            "Shadowing built-ins: naming a variable list or len hides the built-in.",
        ],
        practice_prompts=[
            "What is the LEGB rule and why does it matter when looking up a variable name?",
            "Why is passing values via arguments generally better than using global variables?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does LEGB stand for?",
                qtype="short_answer",
                correct_answer="Local, Enclosing, Global, Built-in",
                keywords=["local", "enclosing", "global", "built-in"],
                explanation="LEGB is the order Python searches for a name when resolving it.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="A variable created inside a function is ____ — it cannot be accessed outside.",
                qtype="fill_blank",
                correct_answer="local",
                explanation="Local variables are created when the function runs and discarded when it returns.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A function can read a global variable without the global keyword.",
                qtype="true_false",
                correct_answer="true",
                explanation="Reading is fine; only reassigning a global inside a function requires the global keyword.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b17-ex",
            title="Scope experiment",
            instructions=(
                "Predict what this code prints, then run it to confirm:\n"
                "x = 'global'\n"
                "def f():\n"
                "    x = 'local'\n"
                "    print(x)\n"
                "f()\n"
                "print(x)"
            ),
            starter_code=(
                "x = 'global'\n"
                "def f():\n"
                "    x = 'local'\n"
                "    print(x)\n"
                "f()\n"
                "print(x)"
            ),
            expected_output="local\nglobal",
            hints=[
                "The x inside f() is a new local variable — it does not overwrite the global x.",
                "After f() returns, the global x is still 'global'.",
            ],
            solution=(
                "x = 'global'\n"
                "def f():\n"
                "    x = 'local'\n"
                "    print(x)\n"
                "f()\n"
                "print(x)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b18",
        title="Errors and Exceptions",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Errors in Python come in two flavours. Syntax errors are detected before your program "
            "runs — Python cannot even parse the file because the grammar rules are broken "
            "(e.g. a missing colon). Runtime errors (exceptions) happen while the program is running "
            "when something unexpected occurs, such as dividing by zero or accessing a missing key.\n\n"
            "You handle exceptions with a try/except block. Code that might fail goes in try; if an "
            "exception is raised, Python jumps to except and runs that block instead of crashing. "
            "You can catch specific exception types (except ValueError) or all exceptions (except "
            "Exception) — be specific when you can. An optional else block runs when no exception "
            "occurs, and finally always runs (great for cleanup like closing files).\n\n"
            "You can also raise exceptions yourself with raise ValueError('message'), which is useful "
            "when your code detects an invalid state. Custom messages make debugging much faster."
        ),
        key_terms={
            "Exception": "An error raised at runtime that interrupts normal program flow.",
            "try": "Marks the block of code to attempt — if an exception occurs, control moves to except.",
            "except": "Catches and handles a specific exception type.",
            "finally": "A block that always runs after try/except, regardless of whether an error occurred.",
            "raise": "Manually triggers an exception with a given type and message.",
            "ValueError": "Raised when a function receives an argument of the right type but wrong value.",
        },
        code_examples=[
            CodeExample(
                title="Basic try/except",
                code=(
                    "try:\n"
                    "    number = int(input('Enter a number: '))\n"
                    "    print(f'You entered {number}')\n"
                    "except ValueError:\n"
                    "    print('That is not a valid number!')"
                ),
                explanation="If the user types text instead of a number, ValueError is caught instead of crashing.",
                output="Enter a number: hello\nThat is not a valid number!",
                line_notes={
                    1: "[bold]try[/bold] wraps the code that might raise an exception.",
                    4: "[bold]except ValueError[/bold] catches only ValueErrors — other exceptions still propagate.",
                },
            ),
            CodeExample(
                title="try/except/else/finally",
                code=(
                    "try:\n"
                    "    result = 10 / 2\n"
                    "except ZeroDivisionError:\n"
                    "    print('Cannot divide by zero')\n"
                    "else:\n"
                    "    print(f'Result: {result}')\n"
                    "finally:\n"
                    "    print('Done')"
                ),
                explanation="else runs on success; finally always runs.",
                output="Result: 5.0\nDone",
                line_notes={
                    5: "[bold]else[/bold] only executes when NO exception was raised in try.",
                    7: "[bold]finally[/bold] always executes — for cleanup like closing a file or connection.",
                },
            ),
        ],
        common_mistakes=[
            "Bare except: — this catches everything including KeyboardInterrupt; always name the exception.",
            "Swallowing exceptions silently with an empty except block, hiding real bugs.",
            "Handling exceptions too broadly — a broad except Exception can mask unexpected errors.",
            "Not reading the traceback — the error type and line number tell you exactly what went wrong.",
        ],
        practice_prompts=[
            "What is the difference between a syntax error and a runtime exception?",
            "Why should you catch specific exception types rather than using a bare except?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which block always executes regardless of whether an exception was raised?",
                qtype="multiple_choice",
                options=["try", "except", "else", "finally"],
                correct_answer="finally",
                explanation="finally runs whether or not an exception occurred — useful for cleanup.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="To manually trigger an exception, use the ____ keyword.",
                qtype="fill_blank",
                correct_answer="raise",
                explanation="raise ExceptionType('message') triggers an exception from your own code.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The else block in a try/except runs when no exception occurs.",
                qtype="true_false",
                correct_answer="true",
                explanation="else executes only when the try block completes without raising any exception.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b18-ex",
            title="Safe division",
            instructions=(
                "Write a function safe_divide(a, b) that returns a / b. "
                "If b is 0, catch the ZeroDivisionError and return None. "
                "Test it with safe_divide(10, 2) and safe_divide(5, 0)."
            ),
            starter_code=(
                "def safe_divide(a, b):\n"
                "    try:\n"
                "        ...\n"
                "    except ZeroDivisionError:\n"
                "        ...\n"
                "\n"
                "print(safe_divide(10, 2))\n"
                "print(safe_divide(5, 0))"
            ),
            expected_output="5.0\nNone",
            hints=[
                "Put the division inside the try block.",
                "Use return a / b in the try block.",
                "Use return None in the except block.",
            ],
            solution=(
                "def safe_divide(a, b):\n"
                "    try:\n"
                "        return a / b\n"
                "    except ZeroDivisionError:\n"
                "        return None\n"
                "\n"
                "print(safe_divide(10, 2))\n"
                "print(safe_divide(5, 0))"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b19",
        title="Imports and Modules",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "A module is a Python file containing code — functions, classes, and variables — that you "
            "can reuse in other files. Python ships with a large standard library of modules covering "
            "maths, dates, files, networking, and much more. You load a module with the import "
            "statement.\n\n"
            "There are three common import forms. import math gives you access to everything via math.sqrt. "
            "from math import sqrt lets you call sqrt directly without the prefix. "
            "from math import sqrt as sq lets you rename it. The first form is usually best for clarity "
            "because the module name documents where the function came from.\n\n"
            "You can also install third-party packages (not in the standard library) using pip: "
            "pip install requests. Once installed they are imported exactly the same way. "
            "Organising your own code into multiple .py files and importing between them works the "
            "same way — Python finds modules in the same directory or in directories listed in sys.path."
        ),
        key_terms={
            "Module": "A .py file that contains reusable Python code.",
            "import": "Keyword that loads a module so its contents become available.",
            "Standard library": "The collection of modules bundled with Python (math, os, json, etc.).",
            "Package": "A directory of modules with an __init__.py file.",
            "pip": "The Python package installer for third-party libraries.",
            "Alias": "A shorter name for an imported module or name, created with as.",
        },
        code_examples=[
            CodeExample(
                title="Three ways to import",
                code=(
                    "import math\n"
                    "print(math.pi)\n"
                    "\n"
                    "from math import sqrt\n"
                    "print(sqrt(25))\n"
                    "\n"
                    "from math import factorial as fact\n"
                    "print(fact(5))"
                ),
                explanation="Three import styles — full module, specific name, and aliased name.",
                output="3.141592653589793\n5.0\n120",
                line_notes={
                    1: "[bold]import math[/bold] loads the entire module; access names with math.<name>.",
                    4: "[bold]from math import sqrt[/bold] brings sqrt into the local namespace directly.",
                    7: "[bold]as fact[/bold] creates an alias — now you call fact() instead of factorial().",
                },
            ),
            CodeExample(
                title="Useful standard library modules",
                code=(
                    "import random\n"
                    "import datetime\n"
                    "\n"
                    "print(random.randint(1, 6))\n"
                    "print(datetime.date.today())"
                ),
                explanation="random and datetime are two commonly used standard library modules.",
                output="4\n2024-01-15",
                line_notes={
                    4: "[bold]random.randint(1, 6)[/bold] returns a random integer between 1 and 6 inclusive.",
                    5: "[bold]datetime.date.today()[/bold] returns today's date.",
                },
            ),
        ],
        common_mistakes=[
            "Naming your own file the same as a standard library module (e.g. math.py) — your file shadows the library.",
            "Using from module import * — this pollutes the namespace and makes it unclear where names come from.",
            "Trying to import a third-party package before installing it with pip.",
            "Circular imports — two modules importing each other — can cause ImportError.",
        ],
        practice_prompts=[
            "What is the difference between import math and from math import sqrt?",
            "Why might naming a file random.py cause problems in your project?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which import style gives you direct access to sqrt without a module prefix?",
                qtype="multiple_choice",
                options=["import math", "from math import sqrt", "import sqrt from math", "require('math')"],
                correct_answer="from math import sqrt",
                explanation="from module import name brings the name into the local scope directly.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The tool used to install third-party Python packages is ____.",
                qtype="fill_blank",
                correct_answer="pip",
                explanation="pip install <package> downloads and installs packages from PyPI.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="You can use the as keyword to give an imported name an alias.",
                qtype="true_false",
                correct_answer="true",
                explanation="import numpy as np is the classic example — np is shorter to type.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b19-ex",
            title="Random number guessing setup",
            instructions=(
                "Import the random module. Use random.randint(1, 10) to generate a secret number "
                "and print: Secret number chosen between 1 and 10."
            ),
            starter_code=(
                "import ...\n"
                "secret = random.randint(1, 10)\n"
                "print('Secret number chosen between 1 and 10.')"
            ),
            expected_output="Secret number chosen between 1 and 10.",
            hints=[
                "Replace ... with the module name: random.",
                "The print output is fixed — it does not print the secret itself.",
            ],
            solution=(
                "import random\n"
                "secret = random.randint(1, 10)\n"
                "print('Secret number chosen between 1 and 10.')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="b20",
        title="Reading and Writing Files",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "Files let your program store data that persists beyond a single run. Python's built-in "
            "open() function opens a file and returns a file object. You pass the file path and a "
            "mode: 'r' to read, 'w' to write (creates or overwrites), 'a' to append, and 'b' added "
            "to any mode for binary files.\n\n"
            "The safest way to work with files is the with statement — it automatically closes the "
            "file when the block ends, even if an error occurs. Inside the with block, call "
            ".read() for the entire contents, .readline() for one line, or .readlines() for a list "
            "of lines. To write, call .write(text). Remember to include newline characters (\\n) "
            "yourself when writing multiple lines.\n\n"
            "Common pitfalls: forgetting to close files (solved by with), writing a string when you "
            "meant bytes, and using relative paths that break when you run the script from a different "
            "directory. For structured data, the json and csv standard library modules make reading "
            "and writing those formats straightforward."
        ),
        key_terms={
            "open()": "Built-in function that opens a file and returns a file object.",
            "File mode": "The second argument to open(): 'r' (read), 'w' (write), 'a' (append).",
            "with statement": "A context manager that ensures the file is closed when the block exits.",
            ".read()": "File method that reads the entire file content as a single string.",
            ".write()": "File method that writes a string to the file.",
            ".readlines()": "File method that returns a list of lines including newline characters.",
        },
        code_examples=[
            CodeExample(
                title="Writing to a file",
                code=(
                    "with open('notes.txt', 'w') as f:\n"
                    "    f.write('First line\\n')\n"
                    "    f.write('Second line\\n')\n"
                    "print('File written.')"
                ),
                explanation="The with block opens, writes, and automatically closes the file.",
                output="File written.",
                line_notes={
                    1: "[bold]open('notes.txt', 'w')[/bold] — 'w' mode creates the file (or overwrites it). [bold]as f[/bold] names the file object.",
                    2: "[bold]\\n[/bold] is a newline character — without it all text runs together on one line.",
                    4: "The file is already closed once the with block ends.",
                },
            ),
            CodeExample(
                title="Reading from a file",
                code=(
                    "with open('notes.txt', 'r') as f:\n"
                    "    for line in f:\n"
                    "        print(line.strip())"
                ),
                explanation="Iterating over the file object yields one line at a time.",
                output="First line\nSecond line",
                line_notes={
                    1: "[bold]'r'[/bold] mode opens for reading — raises FileNotFoundError if the file does not exist.",
                    2: "Iterating over a file object is memory-efficient — it reads one line at a time.",
                    3: "[bold].strip()[/bold] removes the trailing newline character from each line.",
                },
            ),
        ],
        common_mistakes=[
            "Opening a file in 'w' mode when you meant 'a' — 'w' erases all existing content.",
            "Forgetting to add \\n when writing lines — all content merges into one long line.",
            "Not using with — if the program crashes before .close(), changes may not be saved.",
            "Using a relative path like open('data.txt') when the file is in a different directory.",
        ],
        practice_prompts=[
            "Why is the with statement preferred over manually calling f.close()?",
            "What is the difference between 'w' mode and 'a' mode when opening a file?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which file mode would you use to add content without deleting existing data?",
                qtype="multiple_choice",
                options=["'r'", "'w'", "'a'", "'x'"],
                correct_answer="'a'",
                explanation="'a' (append) mode opens the file and writes at the end, preserving existing content.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The ____ statement ensures a file is closed automatically after use.",
                qtype="fill_blank",
                correct_answer="with",
                explanation="The with context manager calls __exit__ when the block ends, which closes the file.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Opening a file in 'w' mode will overwrite all existing file content.",
                qtype="true_false",
                correct_answer="true",
                explanation="'w' mode truncates (empties) the file before writing. Use 'a' to append instead.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What file method reads the entire file as one string?",
                qtype="short_answer",
                correct_answer=".read()",
                keywords=["read"],
                explanation="f.read() returns all content as a single string.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b20-ex",
            title="Write and read a log file",
            instructions=(
                "1. Write three lines to a file called log.txt: 'Start', 'Processing', 'Done'.\n"
                "2. Read the file back and print each line (stripped of whitespace)."
            ),
            starter_code=(
                "# Step 1: write\n"
                "with open('log.txt', 'w') as f:\n"
                "    f.write(...)\n"
                "    f.write(...)\n"
                "    f.write(...)\n"
                "\n"
                "# Step 2: read\n"
                "with open('log.txt', 'r') as f:\n"
                "    for line in f:\n"
                "        print(line.strip())"
            ),
            expected_output="Start\nProcessing\nDone",
            hints=[
                "Use f.write('Start\\n') — don't forget the newline.",
                "Do the same for 'Processing\\n' and 'Done\\n'.",
                "The read loop with .strip() removes the newline when printing.",
            ],
            solution=(
                "with open('log.txt', 'w') as f:\n"
                "    f.write('Start\\n')\n"
                "    f.write('Processing\\n')\n"
                "    f.write('Done\\n')\n"
                "\n"
                "with open('log.txt', 'r') as f:\n"
                "    for line in f:\n"
                "        print(line.strip())"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
]
