from __future__ import annotations

from ..models import CodeExample, Exercise, Lesson, Level, QuizQuestion

# ---------------------------------------------------------------------------
# University of Michigan "Python Basics" aligned lessons — Beginner track
# ---------------------------------------------------------------------------

MICHIGAN_BASICS_LESSONS: list[Lesson] = [

    # ------------------------------------------------------------------
    # b21 — Indexing, Slicing & Sequence Operations
    # ------------------------------------------------------------------
    Lesson(
        id="b21",
        title="Indexing, Slicing & Sequence Operations",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "Python strings and lists are both *sequences*, which means every element "
            "lives at a numbered position called an **index**. Indices start at 0 for "
            "the first element. You access a single element with the bracket operator "
            "`[]`, e.g. `word[0]` gives the first character. Python also supports "
            "**negative indices**: `-1` always refers to the last element, `-2` to the "
            "second-to-last, and so on — no need to know the length in advance.\n\n"
            "The same `[]` syntax is used for *creating* lists (`[1, 2, 3]`) and for "
            "*indexing* into them (`my_list[0]`). Context makes this unambiguous: if `[]` "
            "appears on the right side of `=` with values inside, it's a list literal; "
            "if it follows a variable name it's indexing.\n\n"
            "The built-in `len()` function returns the number of elements in any "
            "sequence. The **slice operator** `[start:stop:step]` extracts a sub-sequence. "
            "`start` defaults to 0, `stop` defaults to `len()`, and `step` defaults to 1. "
            "For example, `s[1:4]` returns characters at indices 1, 2, and 3 (stop is "
            "exclusive). A step of `-1` reverses the sequence.\n\n"
            "You can **concatenate** two sequences of the same type with `+` and "
            "**repeat** a sequence with `*`. The `in` and `not in` operators test "
            "membership: `'cat' in 'concatenate'` is `True`."
        ),
        key_terms={
            "index": "A zero-based integer position identifying a single element in a sequence.",
            "negative index": "An index counted from the end; -1 is the last element.",
            "slice": "A sub-sequence extracted with [start:stop:step].",
            "len()": "Built-in function that returns the number of elements in a sequence.",
            "concatenation": "Joining two sequences with the + operator.",
            "membership operator": "The `in` / `not in` keywords that test whether a value appears in a sequence.",
        },
        code_examples=[
            CodeExample(
                title="Indexing strings and lists",
                code=(
                    'word = "Python"\n'
                    'print(word[0])   # P\n'
                    'print(word[-1])  # n\n'
                    'nums = [10, 20, 30, 40]\n'
                    'print(nums[2])   # 30\n'
                    'print(nums[-1])  # 40'
                ),
                explanation=(
                    "Both strings and lists use []. Negative indices count from the end."
                ),
                output=(
                    "P\n"
                    "n\n"
                    "30\n"
                    "40"
                ),
                line_notes={
                    1: "[bold]word[/bold] is assigned the string 'Python' — 6 characters, indices 0-5.",
                    2: "Index [bold]0[/bold] is the first character.",
                    3: "Index [bold]-1[/bold] is always the last element — 'n' here.",
                    4: "[bold]nums[/bold] is a list of four integers.",
                    5: "Index [bold]2[/bold] picks the third element (0-based).",
                    6: "Index [bold]-1[/bold] picks the last element, 40.",
                },
            ),
            CodeExample(
                title="Slicing, len, concatenation & membership",
                code=(
                    's = "abcdefg"\n'
                    'print(s[2:5])     # cde\n'
                    'print(s[:3])      # abc\n'
                    'print(s[::2])     # aceg\n'
                    'print(s[::-1])    # gfedcba\n'
                    'print(len(s))     # 7\n'
                    'print("abc" + "xyz")  # abcxyz\n'
                    'print("ha" * 3)       # hahaha\n'
                    'print("c" in s)       # True\n'
                    'print("z" not in s)   # True'
                ),
                explanation=(
                    "Slicing extracts sub-sequences. Omitting start/stop uses defaults. "
                    "Step=-1 reverses. + and * work on both strings and lists."
                ),
                output=(
                    "cde\n"
                    "abc\n"
                    "aceg\n"
                    "gfedcba\n"
                    "7\n"
                    "abcxyz\n"
                    "hahaha\n"
                    "True\n"
                    "True"
                ),
                line_notes={
                    2: "[bold][2:5][/bold] — indices 2, 3, 4 (stop=5 is exclusive).",
                    3: "Omitting start defaults to 0, so [:3] means [0:3].",
                    4: "Step of [bold]2[/bold] skips every other character.",
                    5: "Step of [bold]-1[/bold] iterates backwards — a clean reversal trick.",
                    6: "[bold]len()[/bold] returns 7, the number of characters.",
                },
            ),
        ],
        common_mistakes=[
            "Off-by-one with slicing: `s[1:4]` returns indices 1,2,3 — the stop is EXCLUSIVE.",
            "Confusing `[]` for list creation vs. indexing — the position in the expression is the clue.",
            "IndexError: using `s[7]` on a 7-character string — valid indices are 0-6.",
            "Using `+` to mix types, e.g. `[1,2] + (3,4)` — both sides must be the same type.",
        ],
        practice_prompts=[
            "Given `s = 'Mississippi'`, write a slice that extracts just 'ssi'.",
            "Create a list of the first 5 even numbers, then reverse it using a slice.",
            "Check whether your name is a substring of a longer string using `in`.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does `'hello'[-2]` evaluate to?",
                qtype="multiple_choice",
                correct_answer="'l'",
                options=["'e'", "'l'", "'o'", "'h'"],
                explanation="-1 is 'o', -2 is 'l'.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The slice `s[1:5]` includes the element at index 5.",
                qtype="true_false",
                correct_answer="false",
                explanation="The stop index is exclusive — s[1:5] covers indices 1,2,3,4.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which operator tests whether a value exists inside a sequence?",
                qtype="fill_blank",
                correct_answer="in",
                explanation="The `in` keyword returns True if the value is found.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b21-ex",
            title="Slice & Dice a Word",
            instructions=(
                "Given the string `word = 'fantastic'`, complete the following:\n"
                "1. Print the first 3 characters using a slice.\n"
                "2. Print the last 3 characters using a negative-index slice.\n"
                "3. Print every other character (step=2).\n"
                "4. Print `True` if the letter 'a' appears in the word."
            ),
            starter_code=(
                "word = 'fantastic'\n"
                "# 1. First 3 characters\n"
                "print(word[:3])\n"
                "# 2. Last 3 characters\n"
                "print(word[-3:])\n"
                "# 3. Every other character\n"
                "print(word[::2])\n"
                "# 4. Is 'a' in the word?\n"
                "print('a' in word)"
            ),
            expected_output="fan\ntic\nfnatc\nTrue",
            hints=[
                "For the first 3 chars, omit the start index: word[:3].",
                "For the last 3 chars, use a negative start: word[-3:].",
                "Step=2 skips every other character: word[::2].",
                "The `in` operator returns a boolean.",
            ],
            solution=(
                "word = 'fantastic'\n"
                "print(word[:3])     # fan\n"
                "print(word[-3:])    # tic\n"
                "print(word[::2])    # fnatc (indices 0,2,4,6,8 -> f,n,a,t,c)\n"
                "print('a' in word)  # True"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # ------------------------------------------------------------------
    # b22 — String & List Methods
    # ------------------------------------------------------------------
    Lesson(
        id="b22",
        title="String & List Methods",
        level=Level.BEGINNER,
        estimated_minutes=13,
        explanation=(
            "Python objects carry built-in functions called **methods** — you call them "
            "with dot notation: `object.method(arguments)`. String methods are "
            "**non-mutating**: they return a *new* string and leave the original "
            "unchanged. For example, `'hello'.upper()` returns `'HELLO'` but doesn't "
            "modify the original. Useful string methods include `.upper()`, `.lower()`, "
            "`.strip()` (removes surrounding whitespace), `.replace(old, new)`, and "
            "`.find(sub)` (returns the index of the first match, or -1 if not found).\n\n"
            "`.split(sep)` breaks a string into a list of substrings using `sep` as the "
            "delimiter; omitting `sep` splits on any whitespace. The reverse is "
            "`.join(iterable)` — called on a separator string, it glues an iterable of "
            "strings together. Both `.count(x)` and `.index(x)` work on strings *and* "
            "lists: `.count()` returns how many times `x` appears; `.index()` returns "
            "the position of the first occurrence (raises `ValueError` if absent).\n\n"
            "List methods, by contrast, **mutate in place** and return `None`. "
            "`.append(x)` adds one element to the end; `.insert(i, x)` inserts before "
            "position `i`; `.pop(i)` removes and returns the element at `i` (default "
            "last); `.remove(x)` removes the *first* occurrence of value `x`; `.sort()` "
            "sorts in place. A critical distinction: `lst.append(x)` adds `x` as a "
            "single element, while `lst + [x]` creates a *new* list without changing "
            "`lst`. You can also delete an element by index with `del lst[i]`."
        ),
        key_terms={
            "method": "A function attached to an object and called with dot notation.",
            "non-mutating": "Returns a new value without changing the original object.",
            "mutating": "Modifies the object in place; often returns None.",
            ".split() / .join()": "Inverse operations: split string → list, join list → string.",
            ".append() vs +": ".append(x) mutates in place; lst + [x] creates a new list.",
            "del": "Statement that removes an element from a list by index.",
        },
        code_examples=[
            CodeExample(
                title="Non-mutating string methods",
                code=(
                    'msg = "  Hello, World!  "\n'
                    'print(msg.strip())\n'
                    'print(msg.strip().lower())\n'
                    'print(msg.strip().replace("World", "Python"))\n'
                    'print(msg.find("World"))\n'
                    'words = msg.strip().split(", ")\n'
                    'print(words)\n'
                    'print(" | ".join(words))'
                ),
                explanation=(
                    "Methods can be chained because each returns a new string. "
                    ".find() returns the index of 'World' in the stripped string."
                ),
                output=(
                    "Hello, World!\n"
                    "hello, world!\n"
                    "Hello, Python!\n"
                    "7\n"
                    "['Hello', 'World!']\n"
                    "Hello | World!"
                ),
                line_notes={
                    1: "[bold]msg[/bold] has leading and trailing spaces — common in real data.",
                    2: "[bold].strip()[/bold] removes surrounding whitespace; original msg is unchanged.",
                    3: "Methods chain left-to-right: strip first, then lower.",
                    5: "[bold].find()[/bold] returns 7, the index of 'W' in the stripped string.",
                    6: "[bold].split(', ')[/bold] breaks on the comma-space, producing a list.",
                    7: "[bold].join()[/bold] is called on the separator, not the list.",
                },
            ),
            CodeExample(
                title="Mutating list methods vs. concatenation",
                code=(
                    'fruits = ["apple", "banana"]\n'
                    'fruits.append("cherry")\n'
                    'print(fruits)\n'
                    'new_list = fruits + ["date"]\n'
                    'print(fruits)    # unchanged!\n'
                    'print(new_list)\n'
                    'fruits.insert(1, "apricot")\n'
                    'fruits.remove("banana")\n'
                    'print(fruits)\n'
                    'del fruits[0]\n'
                    'print(fruits)'
                ),
                explanation=(
                    "append mutates in place; + creates a brand new list. "
                    "This is one of the most common sources of beginner bugs."
                ),
                output=(
                    "['apple', 'banana', 'cherry']\n"
                    "['apple', 'banana', 'cherry']\n"
                    "['apple', 'banana', 'cherry', 'date']\n"
                    "['apple', 'apricot', 'cherry']\n"
                    "['apricot', 'cherry']"
                ),
                line_notes={
                    2: "[bold].append()[/bold] mutates [bold]fruits[/bold] in place — returns None.",
                    4: "[bold]+[/bold] creates a new list stored in new_list; fruits is untouched.",
                    5: "Confirm: fruits still has 3 elements, not 4.",
                    7: "[bold].insert(1, 'apricot')[/bold] — position 1, shifting others right.",
                    8: "[bold].remove()[/bold] deletes the first occurrence of the value 'banana'.",
                    10: "[bold]del[/bold] removes by index, not by value.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting that string methods return a new string — `s.upper()` does nothing if you don't capture the result.",
            "Expecting `.append()` to return the modified list — it returns None.",
            "Using `.remove()` when you meant `del` (remove needs the value, del needs the index).",
            ".sort() modifies in place and returns None; `sorted()` returns a new list and leaves the original alone.",
        ],
        practice_prompts=[
            "Take a messy user input string with extra spaces and mixed case, and normalize it to lowercase with no surrounding spaces.",
            "Split a CSV line like `'Alice,30,Engineer'` into a list, then rejoin it with ' | ' as separator.",
            "Build a list of 5 numbers, sort it in place, then remove the largest using .pop().",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does `'hello'.upper()` do to the original string 'hello'?",
                qtype="multiple_choice",
                correct_answer="Nothing — it returns a new string 'HELLO'",
                options=[
                    "Nothing — it returns a new string 'HELLO'",
                    "Modifies 'hello' to become 'HELLO' in place",
                    "Returns None",
                    "Raises a TypeError",
                ],
                explanation="String methods are non-mutating; they always return a new string.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is the return value of `my_list.append(5)`?",
                qtype="multiple_choice",
                correct_answer="None",
                options=["None", "The updated list", "5", "True"],
                explanation=".append() mutates in place and returns None.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The `.join()` method is called on the list of strings, not on the separator string.",
                qtype="true_false",
                correct_answer="false",
                explanation="Counterintuitively, .join() is called on the separator: sep.join(list).",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b22-ex",
            title="Clean and Split a Sentence",
            instructions=(
                "Given `sentence = '  the quick BROWN fox  '`:\n"
                "1. Strip whitespace and convert to lowercase — store in `clean`.\n"
                "2. Split `clean` into a list of words — store in `words`.\n"
                "3. Append the word 'jumps' to `words`.\n"
                "4. Print the length of `words` and then print the words joined by ' - '."
            ),
            starter_code=(
                "sentence = '  the quick BROWN fox  '\n"
                "clean = sentence.strip().lower()\n"
                "words = clean.split()\n"
                "words.append('jumps')\n"
                "print(len(words))\n"
                "print(' - '.join(words))"
            ),
            expected_output="5\nthe - quick - brown - fox - jumps",
            hints=[
                "Chain .strip() and .lower() on the original string.",
                "Calling .split() with no arguments splits on any whitespace.",
                ".append() adds a single element to the end of the list.",
                "Call .join() on the separator string, passing words as the argument.",
            ],
            solution=(
                "sentence = '  the quick BROWN fox  '\n"
                "clean = sentence.strip().lower()\n"
                "words = clean.split()\n"
                "words.append('jumps')\n"
                "print(len(words))          # 5\n"
                "print(' - '.join(words))   # the - quick - brown - fox - jumps"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # ------------------------------------------------------------------
    # b23 — String Formatting: f-strings and .format()
    # ------------------------------------------------------------------
    Lesson(
        id="b23",
        title="String Formatting: f-strings and .format()",
        level=Level.BEGINNER,
        estimated_minutes=10,
        explanation=(
            "Hard-coding values into print strings quickly becomes awkward. Python "
            "provides two elegant solutions. **f-strings** (formatted string literals) "
            "are the modern approach: prefix a string with `f` or `F`, then embed any "
            "Python expression inside `{}` braces: `f'Hello, {name}!'`. The expression "
            "is evaluated at runtime and converted to a string. You can also include a "
            "**format specification** after a colon inside the braces: "
            "`f'{price:.2f}'` formats a float to two decimal places, and "
            "`f'{label:>10}'` right-aligns text in a field of width 10.\n\n"
            "The older **`str.format()` method** works similarly: you write `{}` "
            "placeholders in the template string and pass values as arguments to "
            "`.format()`. Positional references (`{0}`, `{1}`) and keyword references "
            "(`{name}`) are both supported, e.g. "
            "`'Hi {first}, you are {age}!'.format(first='Ana', age=25)`.\n\n"
            "In modern Python (3.6+), **prefer f-strings**: they are faster, more "
            "readable, and let you write the expression directly. Use `.format()` when "
            "you need to fill in a template *later* — for example, storing a template "
            "string in a variable or config file before the values are known. Converting "
            "between the two is straightforward: move the variable names inside the "
            "braces for f-strings, or move them to `.format()` arguments for the older style."
        ),
        key_terms={
            "f-string": "A string literal prefixed with f that evaluates expressions in {} at runtime.",
            "format specification": "A mini-language after the colon inside {}: controls width, precision, alignment.",
            ".format()": "A string method using {} placeholders filled positionally or by keyword.",
            ":.2f": "Format spec for floating-point with exactly 2 decimal places.",
            ":>10": "Right-align the value inside a field of width 10.",
        },
        code_examples=[
            CodeExample(
                title="f-string basics and format specs",
                code=(
                    'name = "Alice"\n'
                    'score = 95.678\n'
                    'print(f"Hello, {name}!")\n'
                    'print(f"Score: {score:.2f}")\n'
                    'print(f"Score: {score:8.2f}")\n'
                    'print(f"Name: {name:>10}")\n'
                    'print(f"2 + 2 = {2 + 2}")'
                ),
                explanation=(
                    "Any expression works inside the braces — variable, arithmetic, "
                    "or even a function call."
                ),
                output=(
                    "Hello, Alice!\n"
                    "Score: 95.68\n"
                    "Score:    95.68\n"
                    "Name:      Alice\n"
                    "2 + 2 = 4"
                ),
                line_notes={
                    3: "The [bold]f[/bold] prefix turns this into a formatted string literal.",
                    4: "[bold]:.2f[/bold] — float format, 2 decimal places; note rounding.",
                    5: "[bold]:8.2f[/bold] — total field width 8, 2 decimal places.",
                    6: "[bold]:>10[/bold] — right-align in a 10-character field.",
                    7: "Any Python [bold]expression[/bold] is valid inside {}.",
                },
            ),
            CodeExample(
                title=".format() with positional and keyword arguments",
                code=(
                    'template = "Hi {0}, you scored {1:.1f}%"\n'
                    'print(template.format("Bob", 88.5))\n'
                    'msg = "Dear {first}, your order #{num} is ready."\n'
                    'print(msg.format(first="Carol", num=4217))'
                ),
                explanation=(
                    ".format() is useful when the template is defined before the values. "
                    "The template string itself is reusable."
                ),
                output=(
                    "Hi Bob, you scored 88.5%\n"
                    "Dear Carol, your order #4217 is ready."
                ),
                line_notes={
                    1: "[bold]{0}[/bold] and [bold]{1}[/bold] are positional placeholders.",
                    2: "Values are passed positionally to [bold].format()[/bold].",
                    3: "[bold]{first}[/bold] and [bold]{num}[/bold] are keyword placeholders.",
                    4: "Keyword arguments can appear in any order.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting the `f` prefix — `'Hello, {name}'` prints literally '{name}'.",
            "Mixing up positional and keyword args in .format() without the matching placeholder style.",
            "Using .format() when f-strings are cleaner (and vice versa for reusable templates).",
        ],
        practice_prompts=[
            "Format a product report: item name (left-aligned, width 15), price (right-aligned, width 8, 2 decimals).",
            "Rewrite `'The answer is ' + str(42) + '!'` as an f-string.",
            "Create a reusable .format() template for an email greeting that takes a first name and a date.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which prefix turns a string into an f-string?",
                qtype="fill_blank",
                correct_answer="f",
                explanation="Write f'...' or F'...' to create an f-string.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What does the format spec `:.2f` control?",
                qtype="multiple_choice",
                correct_answer="Display a float with exactly 2 decimal places",
                options=[
                    "Display a float with exactly 2 decimal places",
                    "Round to 2 significant figures",
                    "Left-align in a field of width 2",
                    "Display 2 characters of a string",
                ],
                explanation="The f in :.2f stands for float; .2 sets the decimal precision.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b23-ex",
            title="Format a Receipt Line",
            instructions=(
                "Write code that prints a receipt line in this exact format:\n"
                "  `Item: Apples          Price:   $1.99`\n\n"
                "Use an f-string with format specs:\n"
                "- Item name left-aligned in a 15-character field.\n"
                "- Price formatted to 2 decimal places, preceded by '$'."
            ),
            starter_code=(
                "item = 'Apples'\n"
                "price = 1.99\n"
                "print(f'Item: {item:<15} Price: ${price:.2f}')"
            ),
            expected_output="Item: Apples          Price: $1.99",
            hints=[
                "Use :<15 for left-align in a 15-character field.",
                "Use :.2f for 2 decimal places on the price.",
                "You can put literal text like 'Item: ' and 'Price: $' outside the braces.",
            ],
            solution=(
                "item = 'Apples'\n"
                "price = 1.99\n"
                "print(f'Item: {item:<15} Price: ${price:.2f}')\n"
                "# Output: Item: Apples          Price: $1.99"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # ------------------------------------------------------------------
    # b24 — The Accumulator Pattern
    # ------------------------------------------------------------------
    Lesson(
        id="b24",
        title="The Accumulator Pattern",
        level=Level.BEGINNER,
        estimated_minutes=14,
        explanation=(
            "The **accumulator pattern** is the single most important beginner pattern "
            "in the Michigan course. The idea is simple: create a variable *before* a "
            "loop to hold a running result, then update it *inside* the loop on each "
            "iteration. After the loop, the variable holds the final answer.\n\n"
            "The pattern has three parts: (1) **Initialize** the accumulator to an "
            "appropriate starting value (0 for a sum, `[]` for a list, `''` for a string, "
            "`None` or the first element for a max). (2) **Loop** — typically `for i in "
            "range(n):` or `for item in some_list:`. (3) **Update** the accumulator — "
            "`total += i`, `result.append(...)`, `text += word`. The update step is "
            "always inside the loop.\n\n"
            "You can accumulate different things depending on the initial value and "
            "update logic: a running **sum** (`total += x`), a new **list** "
            "(`.append()`), a **string** built up character by character, a **count** "
            "(`count += 1`), or a **maximum** by combining the update with a conditional "
            "(`if x > current_max: current_max = x`).\n\n"
            "**Debugging tip:** if your accumulated result is wrong, add a `print()` "
            "*inside* the loop to see the accumulator's value after each step. Watching "
            "it evolve line-by-line almost always reveals the bug immediately."
        ),
        key_terms={
            "accumulator": "A variable initialized before a loop and updated each iteration to build up a result.",
            "range()": "Built-in that produces a sequence of integers: range(n) → 0..n-1.",
            "+=": "Shorthand for x = x + value; essential for numeric accumulators.",
            ".append()": "Adds one element to the end of a list — the list accumulator's update step.",
            "running maximum": "Accumulating the largest value seen so far using a conditional inside the loop.",
            "initialize before the loop": "The accumulator must exist and have a sensible starting value BEFORE the loop begins.",
        },
        code_examples=[
            CodeExample(
                title="Accumulating a sum, count, and maximum",
                code=(
                    "numbers = [3, 7, 2, 9, 4, 6]\n"
                    "total = 0\n"
                    "count = 0\n"
                    "current_max = numbers[0]\n"
                    "for n in numbers:\n"
                    "    total += n\n"
                    "    count += 1\n"
                    "    if n > current_max:\n"
                    "        current_max = n\n"
                    "print(f'Sum={total}, Count={count}, Max={current_max}')"
                ),
                explanation=(
                    "Three accumulators run in parallel inside one loop. "
                    "Each has its own initialization and update step."
                ),
                output="Sum=31, Count=6, Max=9",
                line_notes={
                    2: "[bold]total = 0[/bold] — sum accumulator; start at 0 (identity for addition).",
                    3: "[bold]count = 0[/bold] — count accumulator; increments once per iteration.",
                    4: "[bold]current_max[/bold] — initialize to the first element, not 0.",
                    6: "[bold]total += n[/bold] is the update step — must be inside the loop.",
                    8: "Conditional update: only replace current_max when a bigger value is found.",
                },
            ),
            CodeExample(
                title="Accumulating a list and a string",
                code=(
                    "squares = []\n"
                    "sentence = ''\n"
                    "words = ['the', 'cat', 'sat']\n"
                    "for i in range(1, 6):\n"
                    "    squares.append(i ** 2)\n"
                    "for word in words:\n"
                    "    sentence += word + ' '\n"
                    "print(squares)\n"
                    "print(sentence.strip())"
                ),
                explanation=(
                    "Use [] and '' as starting accumulators. "
                    ".append() grows the list; += grows the string."
                ),
                output=(
                    "[1, 4, 9, 16, 25]\n"
                    "the cat sat"
                ),
                line_notes={
                    1: "[bold]squares = [][/bold] — empty list is the correct starting value.",
                    2: "[bold]sentence = ''[/bold] — empty string accumulator.",
                    4: "[bold]range(1, 6)[/bold] produces 1, 2, 3, 4, 5.",
                    5: "[bold].append(i ** 2)[/bold] — compute and immediately accumulate.",
                    7: "[bold]sentence += word + ' '[/bold] — adds word plus a space each time.",
                },
            ),
        ],
        common_mistakes=[
            "Initializing the accumulator INSIDE the loop — it resets to zero every iteration!",
            "Using `=` instead of `+=` for numeric accumulation — overwrites rather than adds.",
            "Initializing a max accumulator to 0 — fails if all numbers in the list are negative.",
            "Forgetting to .append() and instead using = which replaces the list each time.",
        ],
        practice_prompts=[
            "Use the accumulator pattern to compute the product (multiplication) of all numbers in a list.",
            "Build a list of all even numbers between 1 and 50 using range() and the accumulator pattern.",
            "Find the length of the longest word in a list of strings using a max accumulator.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Where should the accumulator variable be initialized?",
                qtype="multiple_choice",
                correct_answer="Before the loop",
                options=[
                    "Before the loop",
                    "Inside the loop, at the top",
                    "After the loop",
                    "It doesn't matter",
                ],
                explanation="Initializing inside the loop resets the accumulator on every iteration.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is the correct starting value for a sum accumulator?",
                qtype="fill_blank",
                correct_answer="0",
                explanation="0 is the additive identity; adding it to any number leaves the number unchanged.",
                difficulty="easy",
            ),
            QuizQuestion(
                question=(
                    "The following code correctly accumulates a sum:\n"
                    "  total = 0\n"
                    "  for x in [1,2,3]:\n"
                    "      total = x"
                ),
                qtype="true_false",
                correct_answer="false",
                explanation="total = x overwrites; should be total += x.",
                difficulty="easy",
            ),
            QuizQuestion(
                question=(
                    "Describe what the accumulator pattern for finding the maximum "
                    "in a list does differently compared to a simple sum accumulator."
                ),
                qtype="short_answer",
                correct_answer=(
                    "A max accumulator uses a conditional inside the loop: it only "
                    "updates when the current element is greater than the stored maximum. "
                    "It is also initialized to the first element (or negative infinity), "
                    "not to 0."
                ),
                keywords=["conditional", "greater", "initialized"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b24-ex",
            title="Count Vowels with the Accumulator Pattern",
            instructions=(
                "Write a program that counts the number of vowels (a, e, i, o, u) "
                "in the string `text = 'accumulator pattern'` using the accumulator "
                "pattern. Print the count."
            ),
            starter_code=(
                "text = 'accumulator pattern'\n"
                "vowels = 'aeiou'\n"
                "count = 0\n"
                "for ch in text:\n"
                "    if ch in vowels:\n"
                "        count += 1\n"
                "print(count)"
            ),
            expected_output="7",
            hints=[
                "Initialize count = 0 before the loop.",
                "Loop over each character in text with: for ch in text:",
                "Inside the loop, check if ch is in the string 'aeiou'.",
                "If so, do count += 1.",
            ],
            solution=(
                "text = 'accumulator pattern'\n"
                "vowels = 'aeiou'\n"
                "count = 0\n"
                "for ch in text:\n"
                "    if ch in vowels:\n"
                "        count += 1\n"
                "print(count)  # 7"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # ------------------------------------------------------------------
    # b25 — Mutability, References, Aliasing & Cloning
    # ------------------------------------------------------------------
    Lesson(
        id="b25",
        title="Mutability, References, Aliasing & Cloning",
        level=Level.BEGINNER,
        estimated_minutes=13,
        explanation=(
            "In Python, every value is an **object** living in memory, and variables "
            "are **references** (pointers) to those objects — not boxes that hold values "
            "directly. Understanding this distinction is key to avoiding subtle bugs.\n\n"
            "Types fall into two camps. **Immutable** types (int, str, float, tuple, bool) "
            "cannot be changed after creation. When you 'change' a string, Python creates "
            "a new object and rebinds the variable. **Mutable** types (list, dict, set) "
            "can be modified in place. When you call `my_list.append(5)`, the same object "
            "in memory grows — any other variable pointing to it sees the change too.\n\n"
            "**Aliasing** is when two variable names refer to the same mutable object. "
            "`b = a` (where `a` is a list) does NOT copy the list — both `a` and `b` now "
            "point to the identical object. Mutating via `b` is visible through `a`. "
            "Use `a is b` to check identity (same object), and `a == b` to check equality "
            "(same contents). To **clone** (shallow-copy) a list and break the alias, use "
            "`b = a[:]`, `b = list(a)`, or `b = a.copy()`.\n\n"
            "A notorious gotcha: **don't mutate a list while iterating over it**. Removing "
            "elements inside a `for` loop shifts indices mid-loop and causes items to be "
            "skipped silently. Instead, iterate over a copy or build a new list."
        ),
        key_terms={
            "immutable": "Cannot be changed after creation (int, str, tuple). 'Changes' create new objects.",
            "mutable": "Can be modified in place (list, dict, set). Changes are visible to all references.",
            "reference": "A variable stores a reference (pointer) to an object, not the object itself.",
            "aliasing": "Two variables referring to the same mutable object — mutations are shared.",
            "is vs ==": "`is` tests identity (same object); `==` tests equality (same value).",
            "cloning": "Creating a true copy of a list: a[:], list(a), or a.copy().",
        },
        code_examples=[
            CodeExample(
                title="Aliasing vs. cloning a list",
                code=(
                    "a = [1, 2, 3]\n"
                    "b = a          # alias — same object!\n"
                    "b.append(4)\n"
                    "print(a)       # [1, 2, 3, 4] — a changed too!\n"
                    "c = a[:]       # clone — new object\n"
                    "c.append(5)\n"
                    "print(a)       # [1, 2, 3, 4] — a unchanged\n"
                    "print(b is a)  # True\n"
                    "print(c is a)  # False\n"
                    "print(c == a)  # False (different contents now)"
                ),
                explanation=(
                    "b = a does NOT copy the list. The slice [:] creates a real copy."
                ),
                output=(
                    "[1, 2, 3, 4]\n"
                    "[1, 2, 3, 4]\n"
                    "True\n"
                    "False\n"
                    "False"
                ),
                line_notes={
                    2: "[bold]b = a[/bold] — b is an alias; both names point to the same list object.",
                    3: "Mutating via b affects the shared object.",
                    4: "a reflects the change even though we never wrote a.append().",
                    5: "[bold]a[:][/bold] is a shallow clone — a new list with the same element values.",
                    8: "[bold]is[/bold] checks identity: b and a are literally the same object.",
                    9: "c is a different object — [bold]is[/bold] returns False.",
                },
            ),
            CodeExample(
                title="Immutable vs. mutable: the rebinding difference",
                code=(
                    "x = 'hello'\n"
                    "y = x\n"
                    "x = x.upper()\n"
                    "print(x)  # HELLO\n"
                    "print(y)  # hello — strings are immutable\n"
                    "lst1 = [1, 2]\n"
                    "lst2 = lst1\n"
                    "lst1[0] = 99\n"
                    "print(lst2)  # [99, 2] — shared mutation!"
                ),
                explanation=(
                    "Reassigning x with x.upper() creates a new string; y still points "
                    "to the original. But mutating lst1[0] goes through the shared object."
                ),
                output=(
                    "HELLO\n"
                    "hello\n"
                    "[99, 2]"
                ),
                line_notes={
                    3: "[bold]x.upper()[/bold] returns a NEW string; x is rebound, y is unaffected.",
                    7: "lst2 = lst1 — aliasing again; both point to [1, 2].",
                    8: "Item assignment [bold]mutates[/bold] the object; lst2 sees the change.",
                },
            ),
        ],
        common_mistakes=[
            "Writing `copy = original` for a list and thinking you have two independent lists.",
            "Using `is` to compare list contents — use `==` for value equality, `is` for identity.",
            "Removing items from a list inside a for-loop over that same list — use a copy or filter.",
            "Assuming reassigning a string variable changes it for everyone — strings are immutable, so only that variable is rebound.",
        ],
        practice_prompts=[
            "Create a list, alias it, mutate via the alias, and verify both names see the change. Then clone it and verify independence.",
            "Write a function that takes a list and returns a sorted copy WITHOUT modifying the original.",
            "Explain in your own words why `x = x + 1` works for integers even though ints are immutable.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which of the following creates a true independent copy of a list `a`?",
                qtype="multiple_choice",
                correct_answer="b = a[:]",
                options=["b = a", "b = a[:]", "b = a.append(None)", "b = str(a)"],
                explanation="a[:] is a shallow clone. b = a is an alias.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="After `b = a` (where a is a list), `b is a` evaluates to True.",
                qtype="true_false",
                correct_answer="true",
                explanation="b = a makes b an alias — both refer to the same object.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b25-ex",
            title="Spot the Alias Bug",
            instructions=(
                "The code below has a bug caused by aliasing. Fix it so that `original` "
                "is NOT modified when `working_copy` is sorted.\n\n"
                "```python\n"
                "original = [5, 3, 8, 1, 4]\n"
                "working_copy = original\n"
                "working_copy.sort()\n"
                "print('original:', original)\n"
                "print('sorted copy:', working_copy)\n"
                "```\n"
                "Expected: original should still print [5, 3, 8, 1, 4]."
            ),
            starter_code=(
                "original = [5, 3, 8, 1, 4]\n"
                "working_copy = original  # BUG: this is an alias!\n"
                "working_copy.sort()\n"
                "print('original:', original)\n"
                "print('sorted copy:', working_copy)"
            ),
            expected_output="original: [5, 3, 8, 1, 4]\nsorted copy: [1, 3, 4, 5, 8]",
            hints=[
                "The bug is on line 2: `working_copy = original` creates an alias, not a copy.",
                "Replace it with a slice clone: `working_copy = original[:]`.",
                "You could also use `working_copy = list(original)` or `original.copy()`.",
            ],
            solution=(
                "original = [5, 3, 8, 1, 4]\n"
                "working_copy = original[:]  # clone, not alias\n"
                "working_copy.sort()\n"
                "print('original:', original)      # [5, 3, 8, 1, 4]\n"
                "print('sorted copy:', working_copy) # [1, 3, 4, 5, 8]"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # ------------------------------------------------------------------
    # b26 — Objects & Instances (Turtle Graphics)
    # ------------------------------------------------------------------
    Lesson(
        id="b26",
        title="Objects & Instances (Turtle Graphics)",
        level=Level.BEGINNER,
        estimated_minutes=12,
        explanation=(
            "An **object** is a bundle of data and behaviour. Python's `turtle` module "
            "is a perfect introduction to objects because you can visualize what they do: "
            "a turtle is a cursor that moves around a canvas drawing lines. When you call "
            "`turtle.Turtle()`, Python creates a brand-new **instance** — an independent "
            "turtle with its own position, direction, color, and pen state. You can create "
            "as many instances as you like ('a herd of turtles'), and each one is "
            "completely independent: moving `alex` does not move `tess`.\n\n"
            "You interact with an instance by calling its **methods** — functions that "
            "belong to it. For example, `alex.forward(100)` moves that specific turtle "
            "forward 100 steps; `alex.left(90)` turns it left. Methods can both read and "
            "modify the object's internal state. This is the fundamental idea behind "
            "**object-oriented programming**: objects encapsulate state and expose "
            "behaviour through methods.\n\n"
            "Combining instances with a `for` loop is powerful: you can draw a square by "
            "repeating `forward` and `left` four times, or give each turtle in a list a "
            "random color using the `random` module. To use turtle graphics, import the "
            "module with `import turtle`, then create instances. Note that turtle opens a "
            "real GUI window — the examples below are illustrative code snippets; the "
            "concepts of objects, instances, and methods apply identically to every Python "
            "class you will ever write.\n\n"
            "Importing: `import turtle` gives access via `turtle.Turtle()`. You can also "
            "use `from random import randint, choice` to pull individual names into scope "
            "from the `random` module."
        ),
        key_terms={
            "object": "A bundle of data (attributes) and behaviour (methods) created from a class.",
            "instance": "One specific object created from a class — e.g. one particular Turtle.",
            "method": "A function that belongs to an object and is called with dot notation.",
            "class": "The blueprint (template) used to create instances; Turtle is a class.",
            "import": "Makes a module's contents available; `import turtle` or `from random import choice`.",
            "attribute": "Data stored inside an object, accessed with dot notation (e.g. turtle's speed).",
        },
        code_examples=[
            CodeExample(
                title="Creating instances and calling methods",
                code=(
                    "import turtle\n"
                    "\n"
                    "alex = turtle.Turtle()\n"
                    "tess = turtle.Turtle()\n"
                    "\n"
                    "alex.color('blue')\n"
                    "alex.forward(100)\n"
                    "alex.left(90)\n"
                    "alex.forward(100)\n"
                    "\n"
                    "tess.color('red')\n"
                    "tess.forward(150)\n"
                    "\n"
                    "turtle.done()"
                ),
                explanation=(
                    "NOTE: This code opens a GUI window when run. "
                    "alex and tess are independent instances — changing one does not affect the other. "
                    "This pattern of creating objects and calling methods is the foundation of OOP."
                ),
                output="(Opens a Turtle graphics window with a blue partial square and a red line.)",
                line_notes={
                    3: "[bold]turtle.Turtle()[/bold] creates one instance and binds it to [bold]alex[/bold].",
                    4: "A second independent instance — tess has its own position and color.",
                    6: "[bold].color()[/bold] sets alex's drawing color; tess is unaffected.",
                    11: "tess starts from the origin independently.",
                },
            ),
            CodeExample(
                title="Drawing a shape with a for loop and random colors",
                code=(
                    "import turtle\n"
                    "from random import choice\n"
                    "\n"
                    "colors = ['red', 'blue', 'green', 'orange']\n"
                    "t = turtle.Turtle()\n"
                    "t.speed(0)\n"
                    "\n"
                    "for side in range(4):\n"
                    "    t.color(choice(colors))\n"
                    "    t.forward(100)\n"
                    "    t.left(90)\n"
                    "\n"
                    "turtle.done()"
                ),
                explanation=(
                    "NOTE: Opens a GUI window. "
                    "Combining a for loop with method calls on one instance draws a square. "
                    "Each side gets a random color from the list."
                ),
                output="(Draws a square with 4 randomly colored sides in a Turtle window.)",
                line_notes={
                    2: "[bold]from random import choice[/bold] brings choice into scope directly.",
                    5: "[bold]turtle.Turtle()[/bold] — one instance is enough for this drawing.",
                    8: "[bold]range(4)[/bold] iterates 4 times — once per side of the square.",
                    9: "[bold]choice(colors)[/bold] picks a random element from the list.",
                    10: "[bold].forward(100)[/bold] — draw one side of length 100.",
                    11: "[bold].left(90)[/bold] — turn 90 degrees to prepare for the next side.",
                },
            ),
        ],
        common_mistakes=[
            "Calling turtle.forward(100) (module-level) instead of t.forward(100) (on your instance) — they work differently.",
            "Forgetting turtle.done() — without it the window may close immediately in some environments.",
            "Thinking two variables assigned with Turtle() share state — each call creates an independent instance.",
            "Confusing `import turtle` with `from turtle import *` — the latter pollutes the namespace.",
        ],
        practice_prompts=[
            "Create two turtle instances and draw a triangle with one and a pentagon with the other simultaneously.",
            "Use the random module to give a turtle a random starting direction before it draws.",
            "Think of another Python class you've seen (e.g. list). What are its instances? What are its methods?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does `turtle.Turtle()` return?",
                qtype="multiple_choice",
                correct_answer="A new independent turtle instance",
                options=[
                    "A new independent turtle instance",
                    "The turtle module itself",
                    "A string representing the turtle",
                    "The turtle's current position",
                ],
                explanation="Calling a class (like Turtle()) constructs and returns a new instance.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Two turtle instances created with Turtle() share the same position and state.",
                qtype="true_false",
                correct_answer="false",
                explanation="Each instance is independent — its own position, direction, and color.",
                difficulty="easy",
            ),
            QuizQuestion(
                question=(
                    "In the expression `alex.forward(100)`, what is `forward` an example of?"
                ),
                qtype="fill_blank",
                correct_answer="method",
                explanation="forward is a method — a function that belongs to the alex instance.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="b26-ex",
            title="Plan a Herd of Turtles",
            instructions=(
                "Without running turtle graphics (or in a turtle-enabled environment), "
                "write the code that would:\n"
                "1. Create a list of three turtle instances.\n"
                "2. Set their colors to 'red', 'green', and 'blue' respectively.\n"
                "3. Use a for loop to make each turtle draw a square of side 80.\n\n"
                "Focus on the OOP concepts: instance creation, method calls, and loops."
            ),
            starter_code=(
                "import turtle\n"
                "\n"
                "colors = ['red', 'green', 'blue']\n"
                "turtles = [turtle.Turtle() for _ in range(3)]\n"
                "\n"
                "for i, t in enumerate(turtles):\n"
                "    t.color(colors[i])\n"
                "\n"
                "for t in turtles:\n"
                "    for _ in range(4):\n"
                "        t.forward(80)\n"
                "        t.left(90)\n"
                "\n"
                "turtle.done()"
            ),
            expected_output="(Three squares drawn by three independent turtle instances in red, green, and blue.)",
            hints=[
                "Use a list comprehension [turtle.Turtle() for _ in range(3)] to create three instances.",
                "Loop over enumerate(turtles) to get both the index and the turtle object.",
                "The inner loop `for _ in range(4)` handles the four sides of the square.",
                "Methods like .color(), .forward(), .left() are called on each individual instance.",
            ],
            solution=(
                "import turtle\n"
                "\n"
                "colors = ['red', 'green', 'blue']\n"
                "turtles = [turtle.Turtle() for _ in range(3)]\n"
                "\n"
                "for i, t in enumerate(turtles):\n"
                "    t.color(colors[i])\n"
                "\n"
                "for t in turtles:\n"
                "    for _ in range(4):\n"
                "        t.forward(80)\n"
                "        t.left(90)\n"
                "\n"
                "turtle.done()"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # ------------------------------------------------------------------
    # b27 — Debugging & Testing: Errors and assert
    # ------------------------------------------------------------------
    Lesson(
        id="b27",
        title="Debugging & Testing: Errors and assert",
        level=Level.BEGINNER,
        estimated_minutes=11,
        explanation=(
            "Every programmer makes mistakes. The skill is in finding and fixing them "
            "quickly. Python distinguishes three kinds of errors. A **syntax error** "
            "happens before the program even runs — Python can't parse the code (e.g. a "
            "missing colon after `if`). A **runtime error** (exception) occurs during "
            "execution when something goes wrong (e.g. dividing by zero, indexing past "
            "the end of a list, calling a method on the wrong type). A **semantic error** "
            "is the sneakiest kind: the program runs without crashing, but produces the "
            "wrong result because the logic is flawed.\n\n"
            "When a runtime error occurs, Python prints a **traceback** — a stack of "
            "function calls leading to the crash, with the actual error message on the "
            "last line. Read it bottom-up: the last line names the exception type and "
            "message; the lines above show exactly which file and line number caused it. "
            "Learning to read tracebacks confidently is one of the highest-leverage "
            "debugging skills.\n\n"
            "Practice **incremental programming**: write a little, test a little. Don't "
            "write 50 lines before running. Add a few lines, run the program, inspect the "
            "output, then add more. Common beginner errors include off-by-one index "
            "mistakes, forgetting to return from a function, and accidentally shadowing a "
            "built-in name like `list = [1, 2, 3]`.\n\n"
            "The `assert` statement is a lightweight testing tool. `assert expression, "
            "'message'` checks that `expression` is truthy; if it's not, Python raises an "
            "`AssertionError` with your message. You can write simple test cases right "
            "next to your function: `assert add(2, 3) == 5, 'add(2,3) should be 5'`. "
            "This habit of writing assertions builds confidence that your code works and "
            "immediately catches regressions."
        ),
        key_terms={
            "syntax error": "Caught before execution; Python cannot parse the code (e.g. missing colon).",
            "runtime error": "An exception raised during execution (e.g. ZeroDivisionError, IndexError).",
            "semantic error": "The program runs but produces a wrong result due to a logic mistake.",
            "traceback": "Python's error report: a stack trace ending with the exception type and message.",
            "assert": "assert expr, 'msg' — raises AssertionError if expr is False; a lightweight test.",
            "incremental programming": "Build and test small pieces at a time to catch bugs early.",
        },
        code_examples=[
            CodeExample(
                title="Reading a traceback and the three error types",
                code=(
                    "# Syntax error (would prevent the file from running):\n"
                    "# if x > 0   <- missing colon; Python says SyntaxError\n"
                    "\n"
                    "# Runtime error:\n"
                    "items = [1, 2, 3]\n"
                    "# print(items[5])  # IndexError: list index out of range\n"
                    "\n"
                    "# Semantic error (no crash, wrong answer):\n"
                    "def average(nums):\n"
                    "    return sum(nums) / len(nums) + 1  # oops: +1 is wrong logic\n"
                    "\n"
                    "print(average([10, 20, 30]))  # prints 21.0 instead of 20.0"
                ),
                explanation=(
                    "All three error types demonstrated in one snippet. "
                    "Syntax and runtime errors are visible immediately; semantic errors hide."
                ),
                output="21.0",
                line_notes={
                    9: "The function definition looks fine — Python will not complain.",
                    10: "[bold]+ 1[/bold] is the semantic bug: the formula is wrong, but no exception occurs.",
                    12: "Python runs and prints 21.0 — the bug is invisible without checking expected output.",
                },
            ),
            CodeExample(
                title="Writing test cases with assert",
                code=(
                    "def add(a, b):\n"
                    "    return a + b\n"
                    "\n"
                    "def to_upper(s):\n"
                    "    return s.upper()\n"
                    "\n"
                    "assert add(2, 3) == 5, 'add(2,3) should be 5'\n"
                    "assert add(0, 0) == 0, 'add(0,0) should be 0'\n"
                    "assert add(-1, 1) == 0, 'add(-1,1) should be 0'\n"
                    "assert to_upper('hello') == 'HELLO', 'uppercase failed'\n"
                    "print('All tests passed!')"
                ),
                explanation=(
                    "If any assert fails, Python raises AssertionError immediately with your message. "
                    "Passing assertions are silent; only the final print confirms success."
                ),
                output="All tests passed!",
                line_notes={
                    7: "[bold]assert[/bold] — if add(2,3) != 5, an AssertionError is raised with the message.",
                    8: "Edge case: both inputs are zero.",
                    9: "Edge case: negative + positive.",
                    11: "Only reached if ALL assertions above passed.",
                },
            ),
        ],
        common_mistakes=[
            "Reading a traceback from the top — start from the bottom where the actual error message is.",
            "Writing a large amount of code before testing — makes bugs much harder to locate.",
            "Shadowing built-in names (e.g. `list = [1,2,3]`) — now `list()` is broken for the rest of the session.",
            "Forgetting the comma and message in assert — `assert x == y 'msg'` is a SyntaxError; use `assert x == y, 'msg'`.",
        ],
        practice_prompts=[
            "Write a `multiply(a, b)` function and add at least 4 assert test cases covering positive, negative, and zero inputs.",
            "Introduce a deliberate syntax error, a deliberate runtime error, and a deliberate semantic error in a short program, then fix each one.",
            "Given a buggy function that's supposed to return the largest element of a list but returns the sum, identify which error type it is and fix it.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which error type occurs when Python cannot parse your code before running it?",
                qtype="multiple_choice",
                correct_answer="Syntax error",
                options=["Syntax error", "Runtime error", "Semantic error", "ImportError"],
                explanation="Syntax errors prevent the program from starting — Python rejects the file.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A semantic error always causes Python to raise an exception.",
                qtype="true_false",
                correct_answer="false",
                explanation="Semantic errors are logic mistakes — the program runs but produces wrong output.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The `assert` statement raises a __________ if its condition is False.",
                qtype="fill_blank",
                correct_answer="AssertionError",
                explanation="assert expr raises AssertionError when expr evaluates to a falsy value.",
                difficulty="easy",
            ),
            QuizQuestion(
                question=(
                    "Describe the 'incremental programming' strategy and why it helps "
                    "with debugging."
                ),
                qtype="short_answer",
                correct_answer=(
                    "Incremental programming means writing a small piece of code and "
                    "testing it before writing more. It helps because when a bug appears "
                    "you know it must be in the code you just added, making it much faster "
                    "to locate and fix."
                ),
                keywords=["small", "test", "locate"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="b27-ex",
            title="Write and Test a Function with assert",
            instructions=(
                "Write a function `is_even(n)` that returns `True` if `n` is even "
                "and `False` otherwise. Then write at least 4 assert statements that "
                "test it. Make sure to test positive numbers, zero, and a negative number."
            ),
            starter_code=(
                "def is_even(n):\n"
                "    return n % 2 == 0\n"
                "\n"
                "assert is_even(4) == True,  'is_even(4) should be True'\n"
                "assert is_even(7) == False, 'is_even(7) should be False'\n"
                "assert is_even(0) == True,  'is_even(0) should be True'\n"
                "assert is_even(-2) == True, 'is_even(-2) should be True'\n"
                "print('All is_even tests passed!')"
            ),
            expected_output="All is_even tests passed!",
            hints=[
                "Use the modulo operator %: a number is even if n % 2 == 0.",
                "Your function should return a boolean expression directly, not use if/else.",
                "Test edge cases: zero is even, negative even numbers should return True.",
                "If an assert fails, Python prints an AssertionError — read the message to know which case failed.",
            ],
            solution=(
                "def is_even(n):\n"
                "    return n % 2 == 0\n"
                "\n"
                "assert is_even(4) == True,  'is_even(4) should be True'\n"
                "assert is_even(7) == False, 'is_even(7) should be False'\n"
                "assert is_even(0) == True,  'is_even(0) should be True'\n"
                "assert is_even(-2) == True, 'is_even(-2) should be True'\n"
                "print('All is_even tests passed!')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
]
