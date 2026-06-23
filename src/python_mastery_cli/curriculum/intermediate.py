from __future__ import annotations

from ..models import CodeExample, Exercise, Lesson, Level, QuizQuestion

INTERMEDIATE_LESSONS: list[Lesson] = [
    # -------------------------------------------------------------------------
    # i01 — List Comprehensions
    # -------------------------------------------------------------------------
    Lesson(
        id="i01",
        title="List Comprehensions",
        level=Level.INTERMEDIATE,
        estimated_minutes=12,
        explanation=(
            "List comprehensions are a concise, readable way to build new lists by "
            "applying an expression to every item in an iterable — often on a single "
            "line where a `for` loop would take three or four. They were inspired by "
            "set-builder notation in mathematics and have become one of the most "
            "recognisable Python idioms.\n\n"
            "The basic form is `[expression for item in iterable]`. You can add an "
            "optional filter with `if condition` at the end: only items for which the "
            "condition is `True` will be processed. This replaces the combination of a "
            "`for` loop plus an `if` statement inside it, keeping your intent right on "
            "the surface.\n\n"
            "List comprehensions are not just syntactic sugar — CPython executes them "
            "slightly faster than an equivalent `for` loop with `.append()` because the "
            "entire comprehension is compiled to a dedicated opcode. For large data "
            "processing tasks the performance difference can be meaningful, though "
            "readability should still be your primary guide.\n\n"
            "Nested comprehensions (a comprehension inside another) are possible and "
            "useful for flattening 2-D structures, but more than one level of nesting "
            "usually hurts readability. When the logic grows complex enough that you "
            "need comments to explain it, a plain `for` loop is almost always the "
            "better choice."
        ),
        key_terms={
            "list comprehension": "A compact `[expr for x in iterable]` syntax that builds a list.",
            "iterable": "Any object Python can loop over — list, tuple, string, range, etc.",
            "expression": "The value placed in the new list for each element.",
            "filter clause": "An optional `if condition` that skips unwanted elements.",
            "nested comprehension": "A comprehension whose iterable is itself a comprehension.",
            "readability": "How easily a human can understand code at a glance.",
        },
        code_examples=[
            CodeExample(
                title="Basic list comprehension",
                code=(
                    "numbers = [1, 2, 3, 4, 5]\n"
                    "squares = [n ** 2 for n in numbers]\n"
                    "print(squares)"
                ),
                explanation="Square every number without a manual loop.",
                output="[1, 4, 9, 16, 25]",
                line_notes={
                    1: "Source list we want to transform.",
                    2: "Comprehension: for each n, compute n**2 and collect the results.",
                    3: "Print the new list — the original is unchanged.",
                },
            ),
            CodeExample(
                title="Comprehension with filter",
                code=(
                    "words = ['apple', 'banana', 'cherry', 'date', 'elderberry']\n"
                    "long_words = [w.upper() for w in words if len(w) > 5]\n"
                    "print(long_words)"
                ),
                explanation="Keep only words longer than 5 characters, then uppercase them.",
                output="['BANANA', 'CHERRY', 'ELDERBERRY']",
                line_notes={
                    1: "A list of fruit names of varying lengths.",
                    2: "The `if len(w) > 5` guard runs before the expression; only passing words are uppercased.",
                    3: "Print the filtered, transformed list.",
                },
            ),
            CodeExample(
                title="Flattening a 2-D list",
                code=(
                    "matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n"
                    "flat = [cell for row in matrix for cell in row]\n"
                    "print(flat)"
                ),
                explanation="Two `for` clauses flatten a list of lists into a single list.",
                output="[1, 2, 3, 4, 5, 6, 7, 8, 9]",
                line_notes={
                    1: "A 3×3 matrix stored as a list of lists.",
                    2: "Outer loop iterates rows; inner loop iterates cells within each row.",
                    3: "All nine integers appear in reading order.",
                },
            ),
        ],
        common_mistakes=[
            "Putting the `if` clause before the `for` clause — the filter always goes at the end.",
            "Using a comprehension when the logic is complex enough to need nested `if/else` chains; a loop is clearer.",
            "Confusing `[x for x in range(5)]` (list) with `(x for x in range(5))` (generator — not stored in memory).",
            "Modifying the original list while iterating over it inside a comprehension.",
        ],
        practice_prompts=[
            "Write a comprehension that produces a list of all even numbers between 1 and 50.",
            "Given a list of strings, build a new list containing only those that start with a vowel.",
            "Flatten the 2-D list `[[1,2],[3,4],[5,6]]` using a nested comprehension.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What is the output of `[x * 2 for x in range(4)]`?",
                qtype="multiple_choice",
                correct_answer="[0, 2, 4, 6]",
                options=["[0, 2, 4, 6]", "[2, 4, 6, 8]", "[1, 2, 3, 4]", "[0, 1, 2, 3]"],
                explanation="`range(4)` yields 0,1,2,3; each is doubled.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="List comprehensions are always faster than equivalent for-loops.",
                qtype="true_false",
                correct_answer="false",
                explanation="They are often faster but readability should guide the choice; complex logic in a comprehension can be slower and harder to maintain.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="In `[x for x in items if x > 0]`, which clause runs first for each element — the expression or the filter?",
                qtype="multiple_choice",
                correct_answer="The filter",
                options=["The expression", "The filter", "They run simultaneously", "It depends on the Python version"],
                explanation="Python evaluates the `if` guard before computing the expression, so non-matching items are never processed.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Complete the comprehension to get a list of lengths: `lengths = [___ for w in words]`",
                qtype="fill_blank",
                correct_answer="len(w)",
                explanation="`len(w)` is the expression that turns each word into its character count.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i01-ex",
            title="Temperature Converter",
            instructions=(
                "You have a list of temperatures in Celsius:\n"
                "  temps_c = [0, 20, 37, 100]\n\n"
                "Use a single list comprehension to convert them all to Fahrenheit.\n"
                "Formula: F = C * 9/5 + 32\n"
                "Print the resulting list."
            ),
            starter_code=(
                "temps_c = [0, 20, 37, 100]\n"
                "# Your comprehension here\n"
                "temps_f = []\n"
                "print(temps_f)"
            ),
            expected_output="[32.0, 68.0, 98.6, 212.0]",
            hints=[
                "Replace `[]` with `[expr for c in temps_c]`.",
                "The expression is `c * 9/5 + 32`.",
                "Division with `/` in Python 3 always returns a float.",
            ],
            solution=(
                "temps_c = [0, 20, 37, 100]\n"
                "temps_f = [c * 9/5 + 32 for c in temps_c]\n"
                "print(temps_f)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i02 — Dictionary Comprehensions
    # -------------------------------------------------------------------------
    Lesson(
        id="i02",
        title="Dictionary Comprehensions",
        level=Level.INTERMEDIATE,
        estimated_minutes=10,
        explanation=(
            "Dictionary comprehensions extend the same compact syntax to building "
            "`dict` objects. Instead of square brackets you use curly braces, and "
            "instead of a single expression you write a `key: value` pair: "
            "`{key_expr: val_expr for item in iterable}`. Like list comprehensions, "
            "an optional `if` clause filters out unwanted items.\n\n"
            "A common use-case is inverting a dictionary — swapping keys and values — "
            "which would require a loop and several lines in older code but collapses "
            "to `{v: k for k, v in original.items()}`. Another frequent pattern is "
            "building a lookup table from a list: `{item.id: item for item in records}`.\n\n"
            "Set comprehensions use the same curly-brace syntax but with a single "
            "expression instead of a `key: value` pair: `{x for x in items}`. This "
            "produces a `set`, not a `dict`. An empty `{}` always creates a dict; use "
            "`set()` for an empty set.\n\n"
            "When iterating over a dictionary use `.items()` to get both key and value, "
            "`.keys()` for keys only, or `.values()` for values only. These return "
            "view objects that reflect live changes to the dictionary."
        ),
        key_terms={
            "dictionary comprehension": "A `{k: v for ...}` expression that builds a dict.",
            "set comprehension": "A `{expr for ...}` expression that builds a set.",
            ".items()": "Returns (key, value) pairs from a dict as a view object.",
            "inversion": "Swapping keys and values to create a reverse-lookup dict.",
            "lookup table": "A dict used to retrieve values by a key in O(1) time.",
            "view object": "A live, read-only window into a dict's keys, values, or items.",
        },
        code_examples=[
            CodeExample(
                title="Basic dictionary comprehension",
                code=(
                    "fruits = ['apple', 'banana', 'cherry']\n"
                    "lengths = {fruit: len(fruit) for fruit in fruits}\n"
                    "print(lengths)"
                ),
                explanation="Map each fruit name to its character count.",
                output="{'apple': 5, 'banana': 6, 'cherry': 6}",
                line_notes={
                    1: "Source list of fruit names.",
                    2: "For each fruit, key = fruit name, value = number of characters.",
                    3: "Print the resulting dictionary.",
                },
            ),
            CodeExample(
                title="Inverting a dictionary",
                code=(
                    "codes = {'a': 1, 'b': 2, 'c': 3}\n"
                    "inverted = {v: k for k, v in codes.items()}\n"
                    "print(inverted)"
                ),
                explanation="Swap keys and values so you can look up a letter by its code number.",
                output="{1: 'a', 2: 'b', 3: 'c'}",
                line_notes={
                    1: "Original mapping from letter to number.",
                    2: "`.items()` gives (key, value) tuples; we unpack as k, v and swap them.",
                    3: "The inverted dict maps numbers back to letters.",
                },
            ),
            CodeExample(
                title="Filtered dictionary comprehension",
                code=(
                    "scores = {'Alice': 88, 'Bob': 55, 'Carol': 92, 'Dave': 61}\n"
                    "passing = {name: score for name, score in scores.items() if score >= 70}\n"
                    "print(passing)"
                ),
                explanation="Keep only students who scored 70 or above.",
                output="{'Alice': 88, 'Carol': 92}",
                line_notes={
                    1: "A dict of student names mapped to their scores.",
                    2: "The `if score >= 70` filter excludes Bob and Dave.",
                    3: "Print only the passing students.",
                },
            ),
        ],
        common_mistakes=[
            "Writing `{x for x in items}` expecting a dict — this produces a set, not a dict.",
            "Using `{}` to create an empty set — `{}` always creates an empty dict; use `set()` instead.",
            "Inverting a dict with duplicate values: the last key wins, silently dropping earlier ones.",
            "Forgetting `.items()` and iterating over just keys when you need both key and value.",
        ],
        practice_prompts=[
            "Given `names = ['alice', 'bob', 'carol']`, build a dict mapping each name to its uppercase version.",
            "Filter the dict `{'x': 10, 'y': -3, 'z': 7}` to keep only positive values.",
            "Build a set comprehension that contains the first letter of each word in a sentence.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does `{v: k for k, v in d.items()}` do?",
                qtype="multiple_choice",
                correct_answer="Inverts the dictionary (swaps keys and values)",
                options=[
                    "Inverts the dictionary (swaps keys and values)",
                    "Returns a list of (value, key) tuples",
                    "Creates a set of all values",
                    "Sorts the dictionary by value",
                ],
                explanation="By unpacking `.items()` as k, v and writing `v: k`, the new dict maps old values to old keys.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="`{}` creates an empty set in Python.",
                qtype="true_false",
                correct_answer="false",
                explanation="`{}` creates an empty dict. Use `set()` for an empty set.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which method returns (key, value) pairs from a dictionary?",
                qtype="fill_blank",
                correct_answer=".items()",
                explanation="`.items()` returns a view of (key, value) tuples.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="When two keys would map to the same value in a dict inversion, what happens?",
                qtype="multiple_choice",
                correct_answer="The last key processed wins; earlier entries are silently overwritten",
                options=[
                    "The last key processed wins; earlier entries are silently overwritten",
                    "Python raises a KeyError",
                    "Both values are stored in a list",
                    "The first key processed wins",
                ],
                explanation="Dictionaries cannot have duplicate keys; later assignments overwrite earlier ones.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i02-ex",
            title="Word Frequency Table",
            instructions=(
                "Given the list of words below, build a dictionary that maps each "
                "unique word to the number of times it appears in the list.\n\n"
                "  words = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat']\n\n"
                "Expected output: {'cat': 3, 'dog': 2, 'bird': 1}\n\n"
                "Hint: you may use a comprehension together with the `.count()` method, "
                "or explore `set()` to get unique words first."
            ),
            starter_code=(
                "words = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat']\n"
                "# Build frequency dict here\n"
                "freq = {}\n"
                "print(freq)"
            ),
            expected_output="{'cat': 3, 'dog': 2, 'bird': 1}",
            hints=[
                "Use `set(words)` to get the unique words.",
                "For each unique word `w`, `words.count(w)` gives its frequency.",
                "Combine: `{w: words.count(w) for w in set(words)}`.",
                "Dict ordering follows insertion order in Python 3.7+, so the output order may differ — that is fine.",
            ],
            solution=(
                "words = ['cat', 'dog', 'cat', 'bird', 'dog', 'cat']\n"
                "freq = {w: words.count(w) for w in set(words)}\n"
                "print(freq)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i03 — Lambda Functions
    # -------------------------------------------------------------------------
    Lesson(
        id="i03",
        title="Lambda Functions",
        level=Level.INTERMEDIATE,
        estimated_minutes=10,
        explanation=(
            "A lambda is a small anonymous function defined with the `lambda` keyword "
            "instead of `def`. Its syntax is `lambda parameters: expression` — the "
            "expression is implicitly returned, so no `return` statement is needed or "
            "allowed. Lambdas are single-expression functions; any logic that requires "
            "statements (assignments, loops, `if/else` blocks) must live in a regular `def`.\n\n"
            "The canonical use for lambdas is as short, throw-away callables passed to "
            "higher-order functions such as `sorted()`, `min()`, `max()`, or the "
            "`key` argument of list's `.sort()` method. Writing a full `def` for a "
            "one-liner key function would be verbose; a lambda keeps the intent "
            "co-located with the call.\n\n"
            "Lambdas can capture variables from their enclosing scope — this is called "
            "a closure. However, Python captures the *variable*, not its value at "
            "definition time, which causes the classic 'late binding' gotcha inside "
            "loops: all lambdas end up seeing the loop variable's final value unless "
            "you use a default argument (`lambda x=x: x`) to snapshot it.\n\n"
            "Despite their convenience, lambdas are easily misused. PEP 8 explicitly "
            "discourages assigning a lambda to a variable (`f = lambda x: x + 1`) "
            "because a `def` gives the function a proper name that shows up in "
            "tracebacks and profiling output. Use lambdas inline; name your functions "
            "with `def`."
        ),
        key_terms={
            "lambda": "An anonymous, single-expression function defined with the `lambda` keyword.",
            "anonymous function": "A function without a name, typically used once and inline.",
            "higher-order function": "A function that accepts other functions as arguments.",
            "closure": "A function that captures variables from the surrounding scope.",
            "late binding": "Closures look up variable values at call time, not at definition time.",
            "key function": "A callable passed to `sorted()`/`.sort()` to determine sort order.",
        },
        code_examples=[
            CodeExample(
                title="Lambda basics",
                code=(
                    "double = lambda x: x * 2\n"
                    "print(double(5))\n"
                    "\n"
                    "add = lambda a, b: a + b\n"
                    "print(add(3, 4))"
                ),
                explanation="Simple lambdas assigned to variables — legal but discouraged by PEP 8; prefer `def` for named functions.",
                output="10\n7",
                line_notes={
                    1: "Lambda with one parameter; multiplies by 2.",
                    2: "Call it like any function.",
                    4: "Lambda with two parameters; returns their sum.",
                    5: "Call with positional arguments.",
                },
            ),
            CodeExample(
                title="Lambda as a sort key",
                code=(
                    "people = [\n"
                    "    {'name': 'Alice', 'age': 30},\n"
                    "    {'name': 'Bob', 'age': 25},\n"
                    "    {'name': 'Carol', 'age': 35},\n"
                    "]\n"
                    "by_age = sorted(people, key=lambda p: p['age'])\n"
                    "for person in by_age:\n"
                    "    print(person['name'], person['age'])"
                ),
                explanation="Sort a list of dicts by the 'age' key using a lambda as the key function.",
                output="Bob 25\nAlice 30\nCarol 35",
                line_notes={
                    1: "List of dicts, each with a name and age.",
                    6: "Pass a lambda as the `key` argument; it extracts the age for comparison.",
                    7: "Iterate the sorted result.",
                    8: "Print each person's name and age in ascending age order.",
                },
            ),
            CodeExample(
                title="Late-binding gotcha in a loop",
                code=(
                    "funcs = [lambda: i for i in range(3)]\n"
                    "print([f() for f in funcs])\n"
                    "\n"
                    "fixed = [lambda i=i: i for i in range(3)]\n"
                    "print([f() for f in fixed])"
                ),
                explanation="Without a default argument, all lambdas share the same `i`; the default-argument trick snapshots the value.",
                output="[2, 2, 2]\n[0, 1, 2]",
                line_notes={
                    1: "Three lambdas, each closing over `i` — but `i` is the same variable.",
                    2: "By the time we call them, the loop is done and `i == 2`.",
                    4: "`i=i` creates a local copy of `i` at definition time, fixing the binding.",
                    5: "Now each lambda remembers its own snapshot of `i`.",
                },
            ),
        ],
        common_mistakes=[
            "Assigning a lambda to a variable name — use `def` instead so the function has a real name in tracebacks.",
            "Trying to include statements (assignments, print, loops) inside a lambda — only a single expression is allowed.",
            "Assuming lambdas capture values at creation time — they capture the variable, so mutable closures can surprise you.",
            "Using a complex lambda where a comprehension or named function would be clearer.",
        ],
        practice_prompts=[
            "Sort the list `['banana', 'apple', 'cherry', 'fig']` by string length using a lambda.",
            "Write a lambda that returns `True` if a number is odd.",
            "Fix the late-binding bug: `multipliers = [lambda x: x * n for n in range(1, 4)]`.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which keyword defines a lambda function?",
                qtype="fill_blank",
                correct_answer="lambda",
                explanation="The `lambda` keyword introduces an anonymous, single-expression function.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A lambda function can contain `for` loops.",
                qtype="true_false",
                correct_answer="false",
                explanation="Lambdas are restricted to a single expression; statements like loops are not allowed.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is the output of `(lambda x, y: x ** y)(2, 3)`?",
                qtype="multiple_choice",
                correct_answer="8",
                options=["6", "8", "9", "23"],
                explanation="2 raised to the power 3 is 8.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="PEP 8 discourages assigning a lambda to a variable name because:",
                qtype="multiple_choice",
                correct_answer="A `def` gives the function a proper name visible in tracebacks",
                options=[
                    "A `def` gives the function a proper name visible in tracebacks",
                    "Lambdas run slower than def functions",
                    "Variable assignment makes the lambda immutable",
                    "Lambdas cannot be passed as arguments after assignment",
                ],
                explanation="Named functions show up in error tracebacks and profiler output, making debugging much easier.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i03-ex",
            title="Custom Sort with Lambda",
            instructions=(
                "You have a list of tuples representing (name, score) pairs:\n\n"
                "  students = [('Alice', 88), ('Bob', 95), ('Carol', 72), ('Dave', 95)]\n\n"
                "Sort the list so that:\n"
                "  1. Students with higher scores come first.\n"
                "  2. Students with equal scores are sorted alphabetically by name.\n\n"
                "Use a single `sorted()` call with a lambda key. Print the result."
            ),
            starter_code=(
                "students = [('Alice', 88), ('Bob', 95), ('Carol', 72), ('Dave', 95)]\n"
                "# Sort: highest score first, then alphabetically by name\n"
                "result = sorted(students)\n"
                "print(result)"
            ),
            expected_output="[('Bob', 95), ('Dave', 95), ('Alice', 88), ('Carol', 72)]",
            hints=[
                "The `key` argument to `sorted()` receives a lambda that returns a tuple.",
                "To reverse a numeric sort without `reverse=True`, negate the number: `-score`.",
                "A tuple key `(-score, name)` sorts by descending score then ascending name.",
                "`lambda s: (-s[1], s[0])` extracts `(-score, name)` from each tuple `s`.",
            ],
            solution=(
                "students = [('Alice', 88), ('Bob', 95), ('Carol', 72), ('Dave', 95)]\n"
                "result = sorted(students, key=lambda s: (-s[1], s[0]))\n"
                "print(result)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i04 — Map, Filter, and Reduce
    # -------------------------------------------------------------------------
    Lesson(
        id="i04",
        title="Map, Filter, and Reduce",
        level=Level.INTERMEDIATE,
        estimated_minutes=12,
        explanation=(
            "`map()`, `filter()`, and `reduce()` are the three classic higher-order "
            "functions of functional programming. Python provides `map` and `filter` as "
            "built-ins; `reduce` lives in the `functools` module because Guido van Rossum "
            "felt it was less essential — if you need a running total, `sum()` is clearer.\n\n"
            "`map(function, iterable)` applies `function` to every element and returns a "
            "lazy iterator of the results. You usually wrap the result in `list()` to "
            "materialise it. `filter(function, iterable)` returns only elements for which "
            "`function` returns a truthy value; passing `None` as the function keeps all "
            "truthy elements.\n\n"
            "`functools.reduce(function, iterable, initializer)` applies a two-argument "
            "function cumulatively: it takes the first two elements, applies the function, "
            "then applies the function to the result and the next element, and so on until "
            "a single value remains. It is the general form of operations like `sum()`, "
            "`max()`, and `min()`.\n\n"
            "In modern Python, list comprehensions and generator expressions cover most of "
            "what `map` and `filter` do, and are generally preferred for readability. Still, "
            "knowing these functions is important because they appear in existing code and "
            "frameworks, and `reduce` has no direct comprehension equivalent."
        ),
        key_terms={
            "map()": "Applies a function to every element of an iterable, returning a lazy iterator.",
            "filter()": "Returns elements for which a predicate function is truthy.",
            "reduce()": "Cumulatively applies a two-argument function to collapse an iterable to one value.",
            "lazy iterator": "An object that computes values on demand rather than storing them all at once.",
            "predicate": "A function that returns True or False, used for filtering.",
            "functools": "Standard-library module containing higher-order function utilities.",
        },
        code_examples=[
            CodeExample(
                title="map() — transform every element",
                code=(
                    "from functools import reduce\n"
                    "\n"
                    "nums = [1, 2, 3, 4, 5]\n"
                    "doubled = list(map(lambda x: x * 2, nums))\n"
                    "print(doubled)"
                ),
                explanation="Double every number. `map` returns a lazy iterator so we wrap it in `list()`.",
                output="[2, 4, 6, 8, 10]",
                line_notes={
                    1: "Import reduce for later examples (shown here for context).",
                    3: "Source list of integers.",
                    4: "`map` applies the lambda to each element; `list()` materialises the iterator.",
                    5: "Print the doubled values.",
                },
            ),
            CodeExample(
                title="filter() — keep matching elements",
                code=(
                    "nums = [1, 2, 3, 4, 5, 6, 7, 8]\n"
                    "evens = list(filter(lambda x: x % 2 == 0, nums))\n"
                    "print(evens)"
                ),
                explanation="Keep only even numbers from the list.",
                output="[2, 4, 6, 8]",
                line_notes={
                    1: "List of integers 1 through 8.",
                    2: "The lambda returns True for even numbers; filter keeps those elements.",
                    3: "Print the filtered list.",
                },
            ),
            CodeExample(
                title="reduce() — collapse to a single value",
                code=(
                    "from functools import reduce\n"
                    "\n"
                    "nums = [1, 2, 3, 4, 5]\n"
                    "product = reduce(lambda acc, x: acc * x, nums)\n"
                    "print(product)"
                ),
                explanation="Multiply all numbers together: 1*2=2, 2*3=6, 6*4=24, 24*5=120.",
                output="120",
                line_notes={
                    1: "reduce lives in functools — import it explicitly.",
                    3: "The list we want to fold into a single product.",
                    4: "`acc` accumulates the running total; `x` is the next element.",
                    5: "Print the final product: 120.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting that `map()` and `filter()` return lazy iterators, not lists — wrap with `list()` to inspect.",
            "Importing `reduce` from the wrong place — it moved to `functools` in Python 3.",
            "Using `reduce` for simple aggregations (`sum`, `max`) instead of the dedicated built-in.",
            "Passing a function that accepts the wrong number of arguments to `reduce` — it always calls `f(acc, x)`.",
        ],
        practice_prompts=[
            "Use `map()` to convert a list of strings to their integer equivalents.",
            "Use `filter()` to remove empty strings from a list.",
            "Use `reduce()` to find the maximum value in a list without using `max()`.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Where does `reduce` live in Python 3?",
                qtype="multiple_choice",
                correct_answer="functools.reduce",
                options=["builtins.reduce", "functools.reduce", "itertools.reduce", "operator.reduce"],
                explanation="`reduce` was moved from builtins to `functools` in Python 3.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="`map()` returns a list in Python 3.",
                qtype="true_false",
                correct_answer="false",
                explanation="`map()` returns a lazy map object (iterator). Wrap it in `list()` to get a list.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What does `list(filter(None, [0, 1, '', 'hi', False, True]))` return?",
                qtype="multiple_choice",
                correct_answer="[1, 'hi', True]",
                options=["[0, 1, '', 'hi', False, True]", "[1, 'hi', True]", "[0, '', False]", "[]"],
                explanation="Passing `None` as the function keeps only truthy elements; 0, '', and False are falsy.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What is `reduce(lambda a, b: a + b, [1, 2, 3, 4])`?",
                qtype="fill_blank",
                correct_answer="10",
                explanation="1+2=3, 3+3=6, 6+4=10.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i04-ex",
            title="Pipeline with map and filter",
            instructions=(
                "Given a list of strings representing numbers (some invalid):\n\n"
                "  raw = ['3', '7', 'abc', '12', '', '5']\n\n"
                "1. Use `filter()` to keep only strings that are purely numeric "
                "   (hint: str.isdigit()).\n"
                "2. Use `map()` to convert the filtered strings to integers.\n"
                "3. Print the resulting list.\n\n"
                "Expected output: [3, 7, 12, 5]"
            ),
            starter_code=(
                "raw = ['3', '7', 'abc', '12', '', '5']\n"
                "# Step 1: filter to keep only digit strings\n"
                "# Step 2: map to int\n"
                "result = []\n"
                "print(result)"
            ),
            expected_output="[3, 7, 12, 5]",
            hints=[
                "Use `str.isdigit` (without parentheses) as the predicate for `filter()`.",
                "Use `int` (the type itself) as the function for `map()`.",
                "Chain them: `list(map(int, filter(str.isdigit, raw)))`.",
                "Remember both `map` and `filter` return iterators; wrap the outer one in `list()`.",
            ],
            solution=(
                "raw = ['3', '7', 'abc', '12', '', '5']\n"
                "result = list(map(int, filter(str.isdigit, raw)))\n"
                "print(result)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i05 — Working with Paths (pathlib)
    # -------------------------------------------------------------------------
    Lesson(
        id="i05",
        title="Working with Paths (pathlib)",
        level=Level.INTERMEDIATE,
        estimated_minutes=14,
        explanation=(
            "Before `pathlib` (added in Python 3.4), filesystem paths were plain strings "
            "manipulated with `os.path` functions — `os.path.join()`, `os.path.exists()`, "
            "`os.path.basename()`, and so on. The `pathlib` module replaced this with an "
            "object-oriented API: a `Path` object knows how to join, split, query, read, "
            "and write itself. Code that used to span multiple `os.path` calls now reads "
            "as natural attribute access.\n\n"
            "The central class is `pathlib.Path`. On Windows it instantiates as a "
            "`WindowsPath`; on macOS/Linux as a `PosixPath`. You almost never import "
            "these subclasses directly — just `from pathlib import Path`. You can construct "
            "a path from a string or from `Path.cwd()` (current directory) and "
            "`Path.home()` (home directory).\n\n"
            "The `/` operator is overloaded on `Path` objects to mean 'join': "
            "`Path('/tmp') / 'data' / 'file.txt'` produces `Path('/tmp/data/file.txt')`. "
            "This replaces `os.path.join()` entirely. Key properties include `.name` "
            "(final component), `.stem` (name without suffix), `.suffix` (extension), "
            "`.parent` (containing directory), and `.parts` (all components as a tuple).\n\n"
            "To iterate a directory, `.iterdir()` yields children as `Path` objects. "
            "`.glob(pattern)` accepts shell-style wildcards, and `.rglob(pattern)` "
            "recurses into sub-directories. Querying methods include `.exists()`, "
            "`.is_file()`, `.is_dir()`, and `.stat()`. Creating directories is "
            "`.mkdir(parents=True, exist_ok=True)`; writing text is simply "
            "`.write_text('hello')` and reading is `.read_text()`."
        ),
        key_terms={
            "Path": "The main pathlib class representing a filesystem path.",
            "/ operator": "Overloaded on Path to join path components instead of os.path.join().",
            ".glob()": "Yields Path objects matching a shell-style wildcard pattern.",
            ".rglob()": "Like glob() but searches all subdirectories recursively.",
            ".stem": "The filename without its suffix (extension).",
            ".suffix": "The file extension including the dot, e.g. '.txt'.",
        },
        code_examples=[
            CodeExample(
                title="Path basics",
                code=(
                    "from pathlib import Path\n"
                    "\n"
                    "p = Path('/tmp/data/report.txt')\n"
                    "print(p.name)\n"
                    "print(p.stem)\n"
                    "print(p.suffix)\n"
                    "print(p.parent)"
                ),
                explanation="Inspect the components of a path using attributes instead of string slicing.",
                output="/tmp/data/report.txt\nreport\n.txt\n/tmp/data",
                line_notes={
                    1: "Import Path — the only class you normally need from pathlib.",
                    3: "Construct a Path from a string (not a real file; just for demonstration).",
                    4: "`.name` is the final component: 'report.txt'.",
                    5: "`.stem` strips the suffix: 'report'.",
                    6: "`.suffix` is the extension including the dot: '.txt'.",
                    7: "`.parent` is the containing directory as another Path object.",
                },
            ),
            CodeExample(
                title="Joining paths with /",
                code=(
                    "from pathlib import Path\n"
                    "\n"
                    "base = Path.home()\n"
                    "config = base / '.config' / 'myapp' / 'settings.json'\n"
                    "print(config)"
                ),
                explanation="Use the `/` operator to build paths — much cleaner than `os.path.join()`.",
                output="~/.config/myapp/settings.json",
                line_notes={
                    1: "Import Path.",
                    3: "`Path.home()` returns the current user's home directory.",
                    4: "Each `/` call joins one more component — fully cross-platform.",
                    5: "Print the assembled path.",
                },
            ),
            CodeExample(
                title="Reading and writing files",
                code=(
                    "from pathlib import Path\n"
                    "\n"
                    "p = Path('/tmp/hello.txt')\n"
                    "p.write_text('Hello, pathlib!')\n"
                    "content = p.read_text()\n"
                    "print(content)\n"
                    "p.unlink()"
                ),
                explanation="Write and read a file using Path's built-in methods, then delete it.",
                output="Hello, pathlib!",
                line_notes={
                    1: "Import Path.",
                    3: "Define the path (the file may not exist yet).",
                    4: "`.write_text()` creates the file and writes the string in one call.",
                    5: "`.read_text()` returns the entire file contents as a string.",
                    6: "Print what we just read back.",
                    7: "`.unlink()` deletes the file.",
                },
            ),
        ],
        common_mistakes=[
            "Mixing `Path` objects with raw strings in `os.path` functions — use pathlib consistently.",
            "Forgetting that `.iterdir()` yields files *and* directories; use `.is_file()` to filter.",
            "Using `p / '/absolute/path'` — a leading `/` in the right operand resets the path, discarding everything before it.",
            "Not passing `exist_ok=True` to `.mkdir()`, which raises `FileExistsError` if the directory already exists.",
        ],
        practice_prompts=[
            "Use `Path.cwd()` and the `/` operator to build a path to a file called `output.txt` in the current directory.",
            "List all `.py` files in a directory using `.glob('*.py')`.",
            "Check whether a path exists and whether it is a file or a directory.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="How do you join two path components with pathlib?",
                qtype="multiple_choice",
                correct_answer="Use the / operator between two Path objects or a Path and a string",
                options=[
                    "Use the / operator between two Path objects or a Path and a string",
                    "Call Path.join(a, b)",
                    "Use os.path.join() with the Path objects",
                    "Concatenate strings with +",
                ],
                explanation="Pathlib overloads `/` for path joining, replacing `os.path.join()`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="`.stem` returns the filename including its extension.",
                qtype="true_false",
                correct_answer="false",
                explanation="`.stem` returns the filename *without* its extension. `.name` includes the extension.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which method reads the entire contents of a text file as a string?",
                qtype="fill_blank",
                correct_answer=".read_text()",
                explanation="`Path.read_text()` opens, reads, and closes the file in one call.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What does `Path('/a/b') / '/c/d'` evaluate to?",
                qtype="multiple_choice",
                correct_answer="Path('/c/d')",
                options=["Path('/a/b/c/d')", "Path('/c/d')", "Path('/a/b//c/d')", "TypeError"],
                explanation="An absolute path on the right-hand side of `/` replaces everything before it.",
                difficulty="hard",
            ),
        ],
        mini_exercise=Exercise(
            id="i05-ex",
            title="Directory Lister",
            instructions=(
                "Write a script that lists all files (not directories) in the current "
                "working directory and prints each filename (just the name, not the full "
                "path) along with its size in bytes.\n\n"
                "Use `Path.cwd()`, `.iterdir()`, `.is_file()`, `.name`, and `.stat().st_size`.\n\n"
                "Output format (one line per file):\n"
                "  filename.ext: 1234 bytes"
            ),
            starter_code=(
                "from pathlib import Path\n"
                "\n"
                "cwd = Path.cwd()\n"
                "for item in cwd.iterdir():\n"
                "    # Check if it's a file, then print name and size\n"
                "    pass"
            ),
            expected_output="(varies by directory contents)",
            hints=[
                "Use `item.is_file()` to skip directories.",
                "`.name` gives the filename without the directory path.",
                "`.stat().st_size` returns the file size in bytes.",
                "f-string: `f'{item.name}: {item.stat().st_size} bytes'`",
            ],
            solution=(
                "from pathlib import Path\n"
                "\n"
                "cwd = Path.cwd()\n"
                "for item in sorted(cwd.iterdir()):\n"
                "    if item.is_file():\n"
                "        print(f'{item.name}: {item.stat().st_size} bytes')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i06 — Working with JSON
    # -------------------------------------------------------------------------
    Lesson(
        id="i06",
        title="Working with JSON",
        level=Level.INTERMEDIATE,
        estimated_minutes=12,
        explanation=(
            "JSON (JavaScript Object Notation) is the dominant data interchange format "
            "on the web. It maps cleanly onto Python's built-in types: JSON objects become "
            "dicts, arrays become lists, strings stay strings, numbers become `int` or "
            "`float`, `true`/`false` become `True`/`False`, and `null` becomes `None`. "
            "Python's standard-library `json` module handles encoding (Python → JSON text) "
            "and decoding (JSON text → Python) with no third-party dependencies.\n\n"
            "The four core functions are `json.dumps()` (dict to string), `json.loads()` "
            "(string to dict), `json.dump()` (dict to file), and `json.load()` (file to "
            "dict). The 's' suffix stands for 'string'. `dumps` accepts optional "
            "`indent` and `sort_keys` arguments that make output human-readable — useful "
            "for logging and config files.\n\n"
            "By default the `json` module can only serialise Python's built-in types. "
            "Custom objects like `datetime` or dataclasses raise `TypeError`. You can "
            "extend serialisation by writing a custom `default` function (or `JSONEncoder` "
            "subclass) that converts unknown types to a serialisable form. Deserialisation "
            "can be customised with the `object_hook` parameter of `loads`/`load`.\n\n"
            "Common pitfalls include assuming JSON preserves integer keys (they become "
            "strings), expecting ordered output without `sort_keys=True` (ordering is "
            "insertion-order since Python 3.7 but JSON spec does not guarantee it), and "
            "confusing `json.dumps()` with `str()` — a dict printed with `str()` uses "
            "Python syntax (single quotes, `True`/`False`) not valid JSON."
        ),
        key_terms={
            "json.dumps()": "Serialises a Python object to a JSON-formatted string.",
            "json.loads()": "Deserialises a JSON string into a Python object.",
            "json.dump()": "Writes a Python object as JSON to a file-like object.",
            "json.load()": "Reads JSON from a file-like object and returns a Python object.",
            "serialisation": "Converting a Python object to a transmittable/storable format.",
            "indent": "A `dumps()` argument that pretty-prints JSON with the given indentation level.",
        },
        code_examples=[
            CodeExample(
                title="Encoding and decoding JSON strings",
                code=(
                    "import json\n"
                    "\n"
                    "data = {'name': 'Alice', 'age': 30, 'active': True}\n"
                    "json_str = json.dumps(data, indent=2)\n"
                    "print(json_str)\n"
                    "\n"
                    "back = json.loads(json_str)\n"
                    "print(back['name'])"
                ),
                explanation="Round-trip a dict through JSON: encode to string then decode back.",
                output='{\n  "name": "Alice",\n  "age": 30,\n  "active": true\n}\nAlice',
                line_notes={
                    1: "Import the standard-library json module.",
                    3: "A Python dict with mixed value types.",
                    4: "`dumps` with `indent=2` produces pretty-printed JSON; True becomes true.",
                    5: "Print the JSON string.",
                    7: "`loads` parses the JSON string back into a Python dict.",
                    8: "Access a key — we get 'Alice' back.",
                },
            ),
            CodeExample(
                title="Reading and writing JSON files",
                code=(
                    "import json\n"
                    "from pathlib import Path\n"
                    "\n"
                    "config = {'theme': 'dark', 'font_size': 14}\n"
                    "path = Path('/tmp/config.json')\n"
                    "\n"
                    "with path.open('w') as fh:\n"
                    "    json.dump(config, fh, indent=2)\n"
                    "\n"
                    "with path.open() as fh:\n"
                    "    loaded = json.load(fh)\n"
                    "\n"
                    "print(loaded)"
                ),
                explanation="Write a config dict to a JSON file then read it back.",
                output="{'theme': 'dark', 'font_size': 14}",
                line_notes={
                    1: "Import json.",
                    2: "Import Path for clean file handling.",
                    4: "Dict to persist as JSON.",
                    5: "Path to the output file.",
                    7: "Open in write mode; use a context manager to ensure the file is closed.",
                    8: "`json.dump` writes directly to the file object.",
                    10: "Open in read mode (default).",
                    11: "`json.load` reads from the file object.",
                    13: "Print the loaded dict.",
                },
            ),
        ],
        common_mistakes=[
            "Using `str(data)` instead of `json.dumps(data)` — `str()` uses Python syntax which is not valid JSON.",
            "Expecting integer keys to survive a round-trip — JSON only supports string keys; `{1: 'a'}` becomes `{'1': 'a'}` after loads.",
            "Forgetting `indent` when writing a config file — the result is one unreadable line.",
            "Trying to serialise a `datetime` directly — it is not JSON-serialisable; convert to `.isoformat()` string first.",
        ],
        practice_prompts=[
            "Serialise a list of dicts to a JSON string and print it with indentation.",
            "Load a JSON string `'{\"x\": 1, \"y\": 2}'` and add the two values together.",
            "Write a function that saves any serialisable object to a `.json` file.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which function converts a Python dict to a JSON string?",
                qtype="multiple_choice",
                correct_answer="json.dumps()",
                options=["json.dump()", "json.dumps()", "json.encode()", "json.stringify()"],
                explanation="`json.dumps()` serialises to a string; `json.dump()` writes to a file.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="JSON supports integer keys in objects.",
                qtype="true_false",
                correct_answer="false",
                explanation="JSON object keys must be strings. Python's `json.dumps({1: 'a'})` converts the key to '1'.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What Python value does JSON `null` map to?",
                qtype="fill_blank",
                correct_answer="None",
                explanation="JSON `null` deserialises to Python `None`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What `json.dumps()` argument controls pretty-printing indentation?",
                qtype="fill_blank",
                correct_answer="indent",
                explanation="Pass `indent=2` (or any integer) to get human-readable multi-line output.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i06-ex",
            title="JSON Config Manager",
            instructions=(
                "Write two functions:\n\n"
                "  save_config(path, config_dict)  — writes config_dict as indented JSON\n"
                "  load_config(path)               — reads and returns the dict\n\n"
                "Then demonstrate them:\n"
                "  1. Save `{'debug': False, 'max_retries': 3, 'timeout': 30}` to `/tmp/app_config.json`\n"
                "  2. Load it back and print the `max_retries` value.\n\n"
                "Expected output: 3"
            ),
            starter_code=(
                "import json\n"
                "from pathlib import Path\n"
                "\n"
                "def save_config(path, config_dict):\n"
                "    pass\n"
                "\n"
                "def load_config(path):\n"
                "    pass\n"
                "\n"
                "cfg = {'debug': False, 'max_retries': 3, 'timeout': 30}\n"
                "save_config('/tmp/app_config.json', cfg)\n"
                "loaded = load_config('/tmp/app_config.json')\n"
                "print(loaded['max_retries'])"
            ),
            expected_output="3",
            hints=[
                "In `save_config`, open the path in write mode with `Path(path).open('w')`.",
                "Use `json.dump(config_dict, fh, indent=2)` inside the with block.",
                "In `load_config`, open in read mode and return `json.load(fh)`.",
            ],
            solution=(
                "import json\n"
                "from pathlib import Path\n"
                "\n"
                "def save_config(path, config_dict):\n"
                "    with Path(path).open('w') as fh:\n"
                "        json.dump(config_dict, fh, indent=2)\n"
                "\n"
                "def load_config(path):\n"
                "    with Path(path).open() as fh:\n"
                "        return json.load(fh)\n"
                "\n"
                "cfg = {'debug': False, 'max_retries': 3, 'timeout': 30}\n"
                "save_config('/tmp/app_config.json', cfg)\n"
                "loaded = load_config('/tmp/app_config.json')\n"
                "print(loaded['max_retries'])"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i07 — Working with CSV
    # -------------------------------------------------------------------------
    Lesson(
        id="i07",
        title="Working with CSV",
        level=Level.INTERMEDIATE,
        estimated_minutes=13,
        explanation=(
            "CSV (Comma-Separated Values) is the lowest-common-denominator format for "
            "tabular data — every spreadsheet application can export and import it, and "
            "it is human-readable in a plain text editor. Python's built-in `csv` module "
            "handles the many edge cases that make 'split on commas' brittle: quoted "
            "fields, embedded commas, embedded newlines, and varying dialects like "
            "tab-separated or semicolon-separated files.\n\n"
            "The two reader classes are `csv.reader` (returns rows as lists of strings) "
            "and `csv.DictReader` (returns rows as `OrderedDict`/dict using the first row "
            "as header keys). `DictReader` is almost always preferable because column "
            "names are clearer than integer indices, and the code stays correct if columns "
            "are reordered.\n\n"
            "Writing uses `csv.writer` (takes lists) or `csv.DictWriter` (takes dicts). "
            "Always open CSV files with `newline=''` in Python 3 — the `csv` module "
            "handles newlines internally, and omitting this argument causes double newlines "
            "on Windows. Also specify `encoding='utf-8-sig'` when the file will be "
            "opened in Excel, which expects a BOM for UTF-8.\n\n"
            "For heavy data processing, `pandas` is more powerful than the `csv` module, "
            "but learning the standard-library approach first gives you a solid mental "
            "model of what higher-level tools are doing underneath."
        ),
        key_terms={
            "csv.reader": "Reads CSV rows as lists of strings.",
            "csv.DictReader": "Reads CSV rows as dicts keyed by header names.",
            "csv.writer": "Writes lists as CSV rows.",
            "csv.DictWriter": "Writes dicts as CSV rows using a specified fieldnames list.",
            "dialect": "A named set of formatting parameters (delimiter, quotechar, etc.).",
            "newline=''": "Required when opening a CSV file in Python 3 to prevent double newlines.",
        },
        code_examples=[
            CodeExample(
                title="Reading a CSV with DictReader",
                code=(
                    "import csv\n"
                    "import io\n"
                    "\n"
                    "sample = 'name,age,city\\nAlice,30,NY\\nBob,25,LA\\n'\n"
                    "reader = csv.DictReader(io.StringIO(sample))\n"
                    "for row in reader:\n"
                    "    print(row['name'], row['age'])"
                ),
                explanation="Parse an in-memory CSV string using DictReader for named field access.",
                output="Alice 30\nBob 25",
                line_notes={
                    1: "Import the csv module.",
                    2: "io.StringIO lets us treat a string as a file-like object.",
                    4: "A two-row CSV string with a header line.",
                    5: "DictReader wraps the file-like object; it uses the first row as keys.",
                    6: "Iterate rows; each row is a dict.",
                    7: "Access fields by name — much safer than indices.",
                },
            ),
            CodeExample(
                title="Writing a CSV with DictWriter",
                code=(
                    "import csv\n"
                    "from pathlib import Path\n"
                    "\n"
                    "rows = [\n"
                    "    {'name': 'Alice', 'score': 92},\n"
                    "    {'name': 'Bob', 'score': 85},\n"
                    "]\n"
                    "path = Path('/tmp/scores.csv')\n"
                    "with path.open('w', newline='', encoding='utf-8') as fh:\n"
                    "    writer = csv.DictWriter(fh, fieldnames=['name', 'score'])\n"
                    "    writer.writeheader()\n"
                    "    writer.writerows(rows)"
                ),
                explanation="Write a list of dicts to a CSV file including a header row.",
                output="(creates /tmp/scores.csv with header and two data rows)",
                line_notes={
                    1: "Import csv.",
                    2: "Import Path for cleaner file handling.",
                    4: "List of dicts — our data source.",
                    8: "Target file path.",
                    9: "Open with `newline=''` to let the csv module manage line endings.",
                    10: "DictWriter needs the fieldnames list to determine column order.",
                    11: "Write the header row using the fieldnames list.",
                    12: "Write all data rows in one call.",
                },
            ),
        ],
        common_mistakes=[
            "Omitting `newline=''` when opening the file — causes blank lines between rows on Windows.",
            "Using `csv.reader` when column names are more meaningful than indices — prefer `DictReader`.",
            "Assuming all values are the correct type — CSV only stores strings; convert explicitly (e.g. `int(row['age'])`).",
            "Not calling `writeheader()` with DictWriter — the output file will lack a header row.",
        ],
        practice_prompts=[
            "Read a CSV of products (name, price, quantity) and print the total inventory value.",
            "Write a function that takes a list of dicts and a filename, and saves them as CSV.",
            "Filter a CSV to keep only rows where a numeric column exceeds a threshold.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which csv reader returns rows as dicts instead of lists?",
                qtype="multiple_choice",
                correct_answer="csv.DictReader",
                options=["csv.reader", "csv.DictReader", "csv.dictreader", "csv.NamedReader"],
                explanation="`csv.DictReader` uses the header row as keys, returning each row as a dict.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="You should open CSV files in Python 3 with `newline=''`.",
                qtype="true_false",
                correct_answer="true",
                explanation="Without `newline=''`, the universal newline translation in Python's text mode interferes with the csv module's own newline handling, causing extra blank lines on Windows.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="After reading a row with `csv.reader`, what Python type are all the cell values?",
                qtype="fill_blank",
                correct_answer="str",
                explanation="The csv module never converts types — every cell comes back as a string.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which DictWriter method writes the header row?",
                qtype="multiple_choice",
                correct_answer="writeheader()",
                options=["write_header()", "writeheader()", "header()", "writefieldnames()"],
                explanation="`writer.writeheader()` writes the fieldnames as the first row.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i07-ex",
            title="CSV Grade Averager",
            instructions=(
                "Given this in-memory CSV data:\n\n"
                "  name,math,english,science\n"
                "  Alice,90,85,92\n"
                "  Bob,78,88,80\n"
                "  Carol,95,91,97\n\n"
                "Use `csv.DictReader` to compute each student's average score "
                "across the three subjects and print:\n"
                "  Alice: 89.0\n"
                "  Bob: 82.0\n"
                "  Carol: 94.33"
            ),
            starter_code=(
                "import csv\n"
                "import io\n"
                "\n"
                "data = 'name,math,english,science\\nAlice,90,85,92\\nBob,78,88,80\\nCarol,95,91,97\\n'\n"
                "\n"
                "reader = csv.DictReader(io.StringIO(data))\n"
                "for row in reader:\n"
                "    # Compute average and print\n"
                "    pass"
            ),
            expected_output="Alice: 89.0\nBob: 82.0\nCarol: 94.33",
            hints=[
                "Convert each score to int: `int(row['math'])`.",
                "Average = (math + english + science) / 3.",
                "Use `round(avg, 2)` to match the expected output.",
                "f-string: `f\"{row['name']}: {round(avg, 2)}\"`",
            ],
            solution=(
                "import csv\n"
                "import io\n"
                "\n"
                "data = 'name,math,english,science\\nAlice,90,85,92\\nBob,78,88,80\\nCarol,95,91,97\\n'\n"
                "\n"
                "reader = csv.DictReader(io.StringIO(data))\n"
                "for row in reader:\n"
                "    avg = (int(row['math']) + int(row['english']) + int(row['science'])) / 3\n"
                "    print(f\"{row['name']}: {round(avg, 2)}\")"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i08 — Virtual Environments
    # -------------------------------------------------------------------------
    Lesson(
        id="i08",
        title="Virtual Environments",
        level=Level.INTERMEDIATE,
        estimated_minutes=12,
        explanation=(
            "A virtual environment is an isolated Python installation — a self-contained "
            "directory containing a Python interpreter and its own set of installed "
            "packages, completely separate from the system Python. When you activate one, "
            "the `python` and `pip` commands in your shell point to that isolated copy "
            "rather than the global installation. This means two projects can depend on "
            "different versions of the same library without conflict.\n\n"
            "Python ships with the `venv` module (standard since 3.3) to create virtual "
            "environments: `python -m venv .venv` creates one in a `.venv` directory. "
            "Activation differs by OS: on macOS/Linux you `source .venv/bin/activate`; "
            "on Windows you run `.venv\\Scripts\\activate`. Your shell prompt changes to "
            "show the active environment. Deactivating runs the `deactivate` command.\n\n"
            "Each project should have its own virtual environment and a `requirements.txt` "
            "(or `pyproject.toml`) that records its dependencies. `pip freeze > requirements.txt` "
            "captures the current environment; `pip install -r requirements.txt` recreates "
            "it on another machine or CI server. Committing the environment directory "
            "itself to git is an anti-pattern — commit only the requirements file.\n\n"
            "Modern tooling like `poetry`, `pipenv`, `hatch`, and `uv` automate virtual "
            "environment creation and dependency management on top of the same underlying "
            "mechanism. Understanding `venv` directly makes these tools easier to reason "
            "about."
        ),
        key_terms={
            "virtual environment": "An isolated Python installation with its own packages.",
            "venv": "The standard-library module used to create virtual environments.",
            "activate": "A shell script that points `python`/`pip` at the venv instead of the system Python.",
            "deactivate": "Restores the shell to the system Python.",
            "requirements.txt": "A plain-text list of package names and versions for reproducing an environment.",
            "pip freeze": "Outputs all installed packages and their exact versions.",
        },
        code_examples=[
            CodeExample(
                title="Creating and activating a virtual environment",
                code=(
                    "# In your terminal (not a Python script)\n"
                    "\n"
                    "# Create the virtual environment\n"
                    "python -m venv .venv\n"
                    "\n"
                    "# Activate (macOS / Linux)\n"
                    "source .venv/bin/activate\n"
                    "\n"
                    "# Activate (Windows)\n"
                    ".venv\\Scripts\\activate\n"
                    "\n"
                    "# Confirm which Python is active\n"
                    "which python"
                ),
                explanation="Shell commands to create and activate a virtual environment.",
                output="# Prompt changes to (.venv)\n# which python -> /path/to/.venv/bin/python",
                line_notes={
                    1: "These are shell commands, not Python code.",
                    4: "`python -m venv .venv` creates a hidden `.venv` directory in the current folder.",
                    7: "Source (not execute) the activate script on macOS/Linux.",
                    10: "Windows uses a backslash path and .bat extension.",
                    13: "Verify the active Python is inside `.venv`.",
                },
            ),
            CodeExample(
                title="Managing dependencies",
                code=(
                    "# Install a package into the active venv\n"
                    "pip install requests\n"
                    "\n"
                    "# Freeze current packages to a file\n"
                    "pip freeze > requirements.txt\n"
                    "\n"
                    "# Recreate the environment from requirements.txt\n"
                    "pip install -r requirements.txt\n"
                    "\n"
                    "# Deactivate when done\n"
                    "deactivate"
                ),
                explanation="Standard workflow for capturing and restoring dependencies.",
                output="# requirements.txt will contain: requests==2.x.x (and its deps)",
                line_notes={
                    2: "Install into the active venv only — global Python is unaffected.",
                    5: "Capture exact versions of everything installed right now.",
                    8: "Anyone can run this command to get the exact same packages.",
                    11: "Restores the shell to the system Python.",
                },
            ),
        ],
        common_mistakes=[
            "Committing the `.venv` directory to git — it's large, OS-specific, and easily regenerated from requirements.txt.",
            "Running `pip install` before activating the environment — packages go to the wrong Python.",
            "Forgetting to add `.venv/` to `.gitignore`.",
            "Using `pip freeze` in an environment that has development-only tools installed — consider separate dev and prod requirements files.",
        ],
        practice_prompts=[
            "Create a virtual environment for a new project, activate it, install `requests`, and freeze the dependencies.",
            "Write a `.gitignore` entry that excludes common virtual environment directories.",
            "Explain the difference between `pip install package` and `pip install -r requirements.txt`.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What command creates a virtual environment in a directory called `.venv`?",
                qtype="fill_blank",
                correct_answer="python -m venv .venv",
                explanation="The `-m venv` flag runs the venv module as a script; `.venv` is the target directory name.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="You should commit the `.venv` directory to git so teammates can share your environment.",
                qtype="true_false",
                correct_answer="false",
                explanation="Commit only `requirements.txt` (or `pyproject.toml`). The `.venv` directory is OS-specific and large.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What command deactivates the currently active virtual environment?",
                qtype="multiple_choice",
                correct_answer="deactivate",
                options=["deactivate", "venv stop", "source deactivate", "exit"],
                explanation="The `deactivate` shell function is added to your shell by the activate script.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which command saves all currently installed packages and versions to a file?",
                qtype="multiple_choice",
                correct_answer="pip freeze > requirements.txt",
                options=[
                    "pip freeze > requirements.txt",
                    "pip save requirements.txt",
                    "pip export > requirements.txt",
                    "pip list > requirements.txt",
                ],
                explanation="`pip freeze` outputs `package==version` lines that `pip install -r` can consume.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i08-ex",
            title="Virtual Environment Setup Checklist",
            instructions=(
                "This exercise is a guided terminal walkthrough — there is no Python script to run.\n\n"
                "Complete the following steps in order:\n"
                "  1. Navigate to a new empty directory (e.g. `mkdir ~/venv-practice && cd ~/venv-practice`).\n"
                "  2. Create a virtual environment: `python -m venv .venv`\n"
                "  3. Activate it (macOS/Linux: `source .venv/bin/activate`).\n"
                "  4. Verify: `which python` should show the `.venv` path.\n"
                "  5. Install a package: `pip install httpx`\n"
                "  6. Freeze: `pip freeze > requirements.txt` — open `requirements.txt` and check its contents.\n"
                "  7. Deactivate: `deactivate`\n\n"
                "Write down the path printed by `which python` in step 4."
            ),
            starter_code="# No Python code needed — run the shell commands described above.",
            expected_output="(path ends with .venv/bin/python)",
            hints=[
                "On Windows, use `.venv\\Scripts\\activate` instead of `source .venv/bin/activate`.",
                "On Windows, use `where python` instead of `which python`.",
                "If `python -m venv` fails, try `python3 -m venv` on macOS/Linux.",
                "The requirements.txt should contain `httpx==<version>` and its dependencies.",
            ],
            solution=(
                "# Terminal session (macOS/Linux):\n"
                "# mkdir ~/venv-practice && cd ~/venv-practice\n"
                "# python -m venv .venv\n"
                "# source .venv/bin/activate\n"
                "# which python   # -> ~/venv-practice/.venv/bin/python\n"
                "# pip install httpx\n"
                "# pip freeze > requirements.txt\n"
                "# cat requirements.txt\n"
                "# deactivate"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i09 — Pip and Packages
    # -------------------------------------------------------------------------
    Lesson(
        id="i09",
        title="Pip and Packages",
        level=Level.INTERMEDIATE,
        estimated_minutes=11,
        explanation=(
            "`pip` is Python's package installer. It downloads packages from the Python "
            "Package Index (PyPI — pypi.org), resolves their dependencies, and installs "
            "everything into the active Python environment. Nearly every Python library "
            "you will ever use is distributed through PyPI; learning `pip` well means "
            "having immediate access to tens of thousands of battle-tested tools.\n\n"
            "The essential commands are `pip install <package>`, `pip uninstall <package>`, "
            "`pip list` (show installed packages), `pip show <package>` (metadata for one "
            "package), `pip install --upgrade <package>` (update to latest), and "
            "`pip install <package>==<version>` (pin a specific version). Always run `pip` "
            "inside an activated virtual environment to avoid polluting your global Python.\n\n"
            "PyPI packages use `setuptools` or the modern `flit`/`hatchling` build backends "
            "and are distributed as wheels (`.whl`) — pre-built binary archives — or as "
            "source distributions (`.tar.gz`). `pip` prefers wheels because they install "
            "without compilation. When no wheel is available, `pip` compiles from source, "
            "which requires a C compiler for packages with C extensions.\n\n"
            "For serious projects, consider `pyproject.toml` (PEP 518/660) as the "
            "modern replacement for `setup.py`. Tools like `poetry`, `hatch`, and `uv` "
            "build on top of `pip` and `pyproject.toml` to provide lock files, dependency "
            "groups, and faster resolution. But every one of them ultimately calls `pip` "
            "or the same underlying install machinery."
        ),
        key_terms={
            "pip": "Python's standard package installer; downloads from PyPI.",
            "PyPI": "Python Package Index — the central repository at pypi.org.",
            "wheel": "A pre-built binary package format; installs faster than source distributions.",
            "requirements.txt": "A file listing packages (with optional version pins) for reproducible installs.",
            "version pinning": "Specifying an exact version (`==`) to ensure reproducibility.",
            "dependency": "A package required by another package to function correctly.",
        },
        code_examples=[
            CodeExample(
                title="Common pip commands",
                code=(
                    "# Install the latest version of a package\n"
                    "pip install requests\n"
                    "\n"
                    "# Install a specific version\n"
                    "pip install requests==2.31.0\n"
                    "\n"
                    "# Upgrade an installed package\n"
                    "pip install --upgrade requests\n"
                    "\n"
                    "# List all installed packages\n"
                    "pip list\n"
                    "\n"
                    "# Show details for one package\n"
                    "pip show requests"
                ),
                explanation="The most-used pip commands for day-to-day package management.",
                output="# pip list shows a table of name + version\n# pip show shows metadata: name, version, location, requires",
                line_notes={
                    2: "Installs the newest available version from PyPI.",
                    5: "Pins to an exact version — useful for reproducibility.",
                    8: "Upgrades to the latest version, even if already installed.",
                    11: "Prints a table of all installed packages and their versions.",
                    14: "Prints metadata: version, author, home page, and dependencies.",
                },
            ),
            CodeExample(
                title="Installing from requirements.txt",
                code=(
                    "# requirements.txt contents:\n"
                    "# requests==2.31.0\n"
                    "# rich>=13.0,<14.0\n"
                    "# httpx\n"
                    "\n"
                    "# Install everything listed:\n"
                    "pip install -r requirements.txt\n"
                    "\n"
                    "# Uninstall a package:\n"
                    "pip uninstall requests -y"
                ),
                explanation="Install all project dependencies in one command using a requirements file.",
                output="# Installs requests, rich (>=13,<14), and latest httpx",
                line_notes={
                    1: "Each line names a package; version specifiers are optional.",
                    2: "Exact pin with `==`.",
                    3: "Range pin with `>=` and `<` — compatible minor versions.",
                    4: "No pin — installs the latest available version.",
                    7: "`-r` means 'from requirements file'.",
                    10: "`-y` skips the confirmation prompt.",
                },
            ),
        ],
        common_mistakes=[
            "Running `pip install` without an active virtual environment — packages end up in the global Python, causing version conflicts across projects.",
            "Pinning every dependency to an exact version in a library (not an application) — users will get conflicts; use ranges for libraries.",
            "Forgetting to update `requirements.txt` after installing new packages — teammates get an incomplete environment.",
            "Confusing `pip list` (all packages) with `pip freeze` (all packages in pip-install format).",
        ],
        practice_prompts=[
            "Install the `rich` library, then write a small script that uses `rich.print` to print coloured text.",
            "Create a `requirements.txt` that pins `requests` to version 2.31.0 and allows any version of `httpx`.",
            "Use `pip show` to find out what packages `requests` depends on.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does `pip install requests==2.28.0` do?",
                qtype="multiple_choice",
                correct_answer="Installs exactly version 2.28.0 of requests",
                options=[
                    "Installs the latest version of requests",
                    "Installs exactly version 2.28.0 of requests",
                    "Installs any version >= 2.28.0",
                    "Installs version 2.28.0 only if nothing newer is available",
                ],
                explanation="`==` is the exact-version specifier in pip.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="`pip freeze` and `pip list` produce identical output.",
                qtype="true_false",
                correct_answer="false",
                explanation="`pip list` shows a human-readable table; `pip freeze` outputs `name==version` lines suitable for `requirements.txt`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is PyPI?",
                qtype="short_answer",
                correct_answer="The Python Package Index — the public repository at pypi.org where Python packages are published and downloaded by pip.",
                keywords=["Python Package Index", "pypi.org", "repository", "packages"],
                explanation="PyPI hosts over 500,000 packages and is pip's default source.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which pip flag installs all packages listed in a file?",
                qtype="fill_blank",
                correct_answer="-r",
                explanation="`pip install -r requirements.txt` reads and installs every package in the file.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i09-ex",
            title="Dependency Inspector",
            instructions=(
                "In your terminal (with a virtual environment active):\n\n"
                "1. Install the `httpx` package: `pip install httpx`\n"
                "2. Run `pip show httpx` and note its 'Requires' field.\n"
                "3. Write a short Python script that imports `httpx` and prints its version.\n\n"
                "Expected output: something like `0.27.0`"
            ),
            starter_code=(
                "import httpx\n"
                "\n"
                "# Print the version of httpx\n"
                "print()"
            ),
            expected_output="0.27.0  # (actual version may differ)",
            hints=[
                "Most packages expose their version as `package.__version__`.",
                "Try `print(httpx.__version__)`.",
                "If `__version__` doesn't exist, try `importlib.metadata.version('httpx')`.",
            ],
            solution=(
                "import httpx\n"
                "\n"
                "print(httpx.__version__)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i10 — Object-Oriented Programming
    # -------------------------------------------------------------------------
    Lesson(
        id="i10",
        title="Object-Oriented Programming",
        level=Level.INTERMEDIATE,
        estimated_minutes=15,
        explanation=(
            "Object-Oriented Programming (OOP) is a paradigm that organises code around "
            "*objects* — bundles of related data (attributes) and behaviour (methods). "
            "Instead of writing functions that operate on raw data structures, you define "
            "classes that model real-world or conceptual entities, and those classes know "
            "how to manage their own state and expose operations that make sense for them.\n\n"
            "The four core principles of OOP are encapsulation (hiding internal state "
            "behind a clean interface), abstraction (exposing only what callers need to "
            "know), inheritance (a subclass reuses and extends a parent class), and "
            "polymorphism (different classes responding to the same method call in their "
            "own way). Python supports all four, though it takes a pragmatic rather than "
            "strict approach — nothing is truly private, and duck typing often matters "
            "more than class hierarchies.\n\n"
            "Python is a multi-paradigm language. You do not have to use OOP. Simple "
            "scripts and data pipelines are often clearest as procedural code or "
            "comprehensions. OOP shines when you have entities with state that changes "
            "over time, when you want to bundle related operations together, when you need "
            "to model a domain closely (games, GUIs, simulations), or when building "
            "libraries with clean public APIs.\n\n"
            "A class is the *blueprint*; an object (or instance) is a concrete thing "
            "built from that blueprint. You can create as many instances of a class as "
            "you like, and each carries its own independent copy of the instance "
            "attributes. Methods are functions defined inside the class that automatically "
            "receive the instance as their first argument, by convention named `self`."
        ),
        key_terms={
            "OOP": "Object-Oriented Programming — organising code around objects with data and behaviour.",
            "class": "A blueprint that defines the attributes and methods of a type of object.",
            "object / instance": "A concrete realisation of a class, with its own attribute values.",
            "encapsulation": "Bundling data and the methods that operate on it into one unit.",
            "inheritance": "A subclass that receives all attributes and methods of its parent class.",
            "polymorphism": "Different classes implementing the same interface in different ways.",
        },
        code_examples=[
            CodeExample(
                title="OOP vs procedural style",
                code=(
                    "# Procedural approach\n"
                    "def area_rect(w, h):\n"
                    "    return w * h\n"
                    "\n"
                    "# OOP approach\n"
                    "class Rectangle:\n"
                    "    def __init__(self, width, height):\n"
                    "        self.width = width\n"
                    "        self.height = height\n"
                    "\n"
                    "    def area(self):\n"
                    "        return self.width * self.height\n"
                    "\n"
                    "r = Rectangle(4, 5)\n"
                    "print(r.area())"
                ),
                explanation="Both compute area, but the OOP version bundles the data with the operation.",
                output="20",
                line_notes={
                    1: "Procedural: data (w, h) passed as arguments — no persistent state.",
                    2: "A standalone function with no memory between calls.",
                    6: "OOP: define a class as the blueprint.",
                    7: "`__init__` is called automatically when an instance is created.",
                    8: "`self.width` stores width on *this* instance, not globally.",
                    11: "An instance method — `self` is the Rectangle it's called on.",
                    14: "Create an instance: `__init__` receives width=4, height=5.",
                    15: "Call the method on the instance; `self` is `r` inside `area()`.",
                },
            ),
            CodeExample(
                title="Inheritance and polymorphism",
                code=(
                    "class Shape:\n"
                    "    def area(self):\n"
                    "        raise NotImplementedError\n"
                    "\n"
                    "class Circle(Shape):\n"
                    "    def __init__(self, radius):\n"
                    "        self.radius = radius\n"
                    "    def area(self):\n"
                    "        return 3.14159 * self.radius ** 2\n"
                    "\n"
                    "class Square(Shape):\n"
                    "    def __init__(self, side):\n"
                    "        self.side = side\n"
                    "    def area(self):\n"
                    "        return self.side ** 2\n"
                    "\n"
                    "shapes = [Circle(5), Square(4)]\n"
                    "for s in shapes:\n"
                    "    print(round(s.area(), 2))"
                ),
                explanation="Both Circle and Square inherit from Shape and provide their own `area()` — polymorphism.",
                output="78.54\n16",
                line_notes={
                    1: "Base class defines the interface but not the implementation.",
                    2: "`area()` raises NotImplementedError to signal subclasses must override it.",
                    5: "`Circle(Shape)` means Circle inherits from Shape.",
                    8: "Circle overrides `area()` with its own formula.",
                    11: "Square also inherits from Shape and overrides `area()`.",
                    17: "A mixed list of shapes — both are `Shape` subclasses.",
                    18: "Same `s.area()` call works on any Shape — polymorphism in action.",
                },
            ),
        ],
        common_mistakes=[
            "Overusing OOP — not every script needs classes; functional or procedural code is often simpler.",
            "Confusing the class itself with an instance — `Rectangle.area()` needs an instance; `r.area()` is correct.",
            "Forgetting `self` as the first parameter of every instance method.",
            "Thinking Python's single underscore `_attr` makes an attribute truly private — it's a convention only.",
        ],
        practice_prompts=[
            "Model a `BankAccount` class with `deposit()`, `withdraw()`, and `balance` attributes.",
            "Create a `Vehicle` base class with `make`, `model`, and `speed_up()`, then subclass `Car` and `Truck`.",
            "Explain when you would choose OOP over a plain function in a new project.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which OOP principle bundles data and the methods that operate on it together?",
                qtype="multiple_choice",
                correct_answer="Encapsulation",
                options=["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"],
                explanation="Encapsulation groups related state and behaviour into one class, hiding implementation details.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In Python, a class attribute prefixed with `__` (double underscore) is completely inaccessible from outside the class.",
                qtype="true_false",
                correct_answer="false",
                explanation="Python uses name-mangling (`_ClassName__attr`) rather than true access control — it can still be accessed, just with a different name.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What is the term for when different classes implement the same method name in different ways?",
                qtype="fill_blank",
                correct_answer="polymorphism",
                explanation="Polymorphism lets you call `s.area()` on any Shape regardless of its concrete subclass.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A class is to an object as a _____ is to a house.",
                qtype="multiple_choice",
                correct_answer="blueprint",
                options=["blueprint", "room", "key", "window"],
                explanation="A class defines the structure; instances (objects) are the concrete things built from it.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i10-ex",
            title="Temperature class",
            instructions=(
                "Create a `Temperature` class that:\n"
                "  - Stores a value in Celsius (`__init__(self, celsius)`).\n"
                "  - Has a method `to_fahrenheit()` returning C * 9/5 + 32.\n"
                "  - Has a method `to_kelvin()` returning C + 273.15.\n"
                "  - Has a `__str__` method returning `'X°C'` (e.g. `'100°C'`).\n\n"
                "Then:\n"
                "  t = Temperature(100)\n"
                "  print(t)               # 100°C\n"
                "  print(t.to_fahrenheit())  # 212.0\n"
                "  print(t.to_kelvin())      # 373.15"
            ),
            starter_code=(
                "class Temperature:\n"
                "    def __init__(self, celsius):\n"
                "        pass\n"
                "\n"
                "    def to_fahrenheit(self):\n"
                "        pass\n"
                "\n"
                "    def to_kelvin(self):\n"
                "        pass\n"
                "\n"
                "    def __str__(self):\n"
                "        pass\n"
                "\n"
                "t = Temperature(100)\n"
                "print(t)\n"
                "print(t.to_fahrenheit())\n"
                "print(t.to_kelvin())"
            ),
            expected_output="100°C\n212.0\n373.15",
            hints=[
                "Store celsius: `self.celsius = celsius`.",
                "Fahrenheit formula: `self.celsius * 9/5 + 32`.",
                "Kelvin formula: `self.celsius + 273.15`.",
                "`__str__` should return `f'{self.celsius}°C'`.",
            ],
            solution=(
                "class Temperature:\n"
                "    def __init__(self, celsius):\n"
                "        self.celsius = celsius\n"
                "\n"
                "    def to_fahrenheit(self):\n"
                "        return self.celsius * 9/5 + 32\n"
                "\n"
                "    def to_kelvin(self):\n"
                "        return self.celsius + 273.15\n"
                "\n"
                "    def __str__(self):\n"
                "        return f'{self.celsius}°C'\n"
                "\n"
                "t = Temperature(100)\n"
                "print(t)\n"
                "print(t.to_fahrenheit())\n"
                "print(t.to_kelvin())"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i11 — Classes
    # -------------------------------------------------------------------------
    Lesson(
        id="i11",
        title="Classes",
        level=Level.INTERMEDIATE,
        estimated_minutes=16,
        explanation=(
            "A class definition begins with the `class` keyword, a name (by convention "
            "CapWords), and an optional base class in parentheses. The body contains "
            "method definitions and, optionally, class-level attributes. The special "
            "method `__init__` is the *initialiser* — it runs automatically each time "
            "you create a new instance and is where you set up the instance's initial state.\n\n"
            "Instance attributes belong to one specific object and are set via "
            "`self.name = value` inside `__init__` (or any method). Class attributes "
            "are shared across all instances and live directly on the class. When Python "
            "looks up `obj.attr`, it first checks the instance's `__dict__`, then "
            "the class's `__dict__`. This means an instance attribute *shadows* a "
            "class attribute of the same name without destroying it.\n\n"
            "Python's *dunder* (double-underscore) methods let classes integrate with "
            "built-in syntax. `__str__` controls what `str()` and `print()` show; "
            "`__repr__` provides an unambiguous developer representation; `__len__` "
            "makes `len(obj)` work; `__eq__` defines `==`; `__lt__` enables sorting. "
            "You implement only the dunders relevant to your class's role.\n\n"
            "Class methods (decorated with `@classmethod`) receive the class as their "
            "first argument (`cls`) rather than an instance; they are often used as "
            "alternative constructors. Static methods (`@staticmethod`) receive neither "
            "class nor instance — they are plain functions logically grouped inside a "
            "class. Properties (`@property`) let you compute attribute values on access, "
            "making them appear to callers as plain attributes rather than method calls."
        ),
        key_terms={
            "__init__": "The initialiser method — runs automatically when a new instance is created.",
            "instance attribute": "Data stored on a specific object via `self.name = value`.",
            "class attribute": "Data shared by all instances, defined at class body level.",
            "dunder method": "A method with double-underscore prefix/suffix that hooks into Python syntax.",
            "@classmethod": "A method receiving `cls` (the class) as its first argument.",
            "@property": "A decorator that makes a method callable as an attribute.",
        },
        code_examples=[
            CodeExample(
                title="Instance vs class attributes",
                code=(
                    "class Dog:\n"
                    "    species = 'Canis lupus familiaris'  # class attribute\n"
                    "\n"
                    "    def __init__(self, name, age):\n"
                    "        self.name = name   # instance attribute\n"
                    "        self.age = age     # instance attribute\n"
                    "\n"
                    "d1 = Dog('Rex', 3)\n"
                    "d2 = Dog('Bella', 5)\n"
                    "print(d1.species)\n"
                    "print(d1.name, d2.name)"
                ),
                explanation="Both dogs share `species`; each has its own `name` and `age`.",
                output="Canis lupus familiaris\nRex Bella",
                line_notes={
                    1: "Class definition begins with `class`.",
                    2: "Class attribute — one value shared by all Dog instances.",
                    4: "`__init__` receives the new instance as `self` plus the caller's arguments.",
                    5: "Instance attribute — unique to each Dog object.",
                    8: "Create the first Dog instance.",
                    9: "Create the second Dog instance.",
                    10: "Both `d1.species` and `d2.species` return the same class attribute.",
                    11: "Instance attributes are independent per object.",
                },
            ),
            CodeExample(
                title="Dunder methods and properties",
                code=(
                    "class Circle:\n"
                    "    PI = 3.14159\n"
                    "\n"
                    "    def __init__(self, radius):\n"
                    "        self.radius = radius\n"
                    "\n"
                    "    @property\n"
                    "    def area(self):\n"
                    "        return self.PI * self.radius ** 2\n"
                    "\n"
                    "    def __repr__(self):\n"
                    "        return f'Circle(radius={self.radius})'\n"
                    "\n"
                    "    def __eq__(self, other):\n"
                    "        return self.radius == other.radius\n"
                    "\n"
                    "c = Circle(5)\n"
                    "print(c.area)\n"
                    "print(repr(c))\n"
                    "print(c == Circle(5))"
                ),
                explanation="Properties, repr, and equality comparison using dunder methods.",
                output="78.53975\nCircle(radius=5)\nTrue",
                line_notes={
                    1: "Class definition.",
                    2: "Class-level constant — shared by all circles.",
                    4: "Initialiser stores the radius.",
                    7: "`@property` makes `area` accessible as `c.area` without parentheses.",
                    8: "The property method computes area on demand.",
                    11: "`__repr__` gives the developer-facing string representation.",
                    14: "`__eq__` defines what `==` means for two Circle objects.",
                    17: "Create a Circle with radius 5.",
                    18: "Access the property — no parentheses needed.",
                    19: "`repr(c)` calls `__repr__`.",
                    20: "Compares two circles with equal radii.",
                },
            ),
            CodeExample(
                title="Class method as alternative constructor",
                code=(
                    "class Date:\n"
                    "    def __init__(self, year, month, day):\n"
                    "        self.year = year\n"
                    "        self.month = month\n"
                    "        self.day = day\n"
                    "\n"
                    "    @classmethod\n"
                    "    def from_string(cls, s):\n"
                    "        year, month, day = map(int, s.split('-'))\n"
                    "        return cls(year, month, day)\n"
                    "\n"
                    "    def __str__(self):\n"
                    "        return f'{self.year}-{self.month:02d}-{self.day:02d}'\n"
                    "\n"
                    "d = Date.from_string('2024-06-15')\n"
                    "print(d)"
                ),
                explanation="A class method parses a string and constructs a Date — an alternative constructor pattern.",
                output="2024-06-15",
                line_notes={
                    1: "Date class with year, month, day attributes.",
                    7: "`@classmethod` decorator — the method receives `cls`, not an instance.",
                    8: "`cls` is the Date class (or a subclass if inherited).",
                    9: "Parse the ISO string by splitting on `-` and converting to int.",
                    10: "Delegate to the normal `__init__` via `cls(...)` — works with subclasses too.",
                    12: "`__str__` formats with zero-padding for month and day.",
                    15: "Call the class method on the class itself, not an instance.",
                    16: "Print triggers `__str__`.",
                },
            ),
        ],
        common_mistakes=[
            "Defining a class attribute when you mean an instance attribute — mutable class attributes (lists, dicts) are shared and mutate together across all instances.",
            "Forgetting `self.` when reading an instance attribute inside a method — Python will look for a local variable instead.",
            "Using `__repr__` and `__str__` interchangeably — `__repr__` should be unambiguous and ideally eval-able; `__str__` is for humans.",
            "Defining a `@property` but forgetting a setter — trying to assign `obj.attr = val` raises `AttributeError`.",
        ],
        practice_prompts=[
            "Add a `__len__` method to a `Playlist` class that returns the number of songs.",
            "Write a `Person` class with a `@property` for `full_name` computed from `first` and `last`.",
            "Create an alternative constructor `from_celsius` for a Temperature class that accepts Celsius and stores Kelvin internally.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What is a class attribute?",
                qtype="multiple_choice",
                correct_answer="A value defined in the class body and shared by all instances",
                options=[
                    "A value defined in the class body and shared by all instances",
                    "A value set with self.name = value inside __init__",
                    "A method decorated with @classmethod",
                    "An attribute that cannot be changed after creation",
                ],
                explanation="Class attributes live on the class itself; all instances see the same value unless they shadow it with an instance attribute.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="`__str__` and `__repr__` always return the same string.",
                qtype="true_false",
                correct_answer="false",
                explanation="`__str__` is for human-readable output; `__repr__` should be an unambiguous developer representation, ideally showing how to recreate the object.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which decorator makes a method callable as an attribute (without parentheses)?",
                qtype="fill_blank",
                correct_answer="@property",
                explanation="`@property` turns a method into a descriptor accessed as `obj.name` rather than `obj.name()`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A mutable class attribute (like a list) is shared across all instances. What can go wrong?",
                qtype="multiple_choice",
                correct_answer="Appending to it via one instance also changes it for all other instances",
                options=[
                    "Appending to it via one instance also changes it for all other instances",
                    "Python raises a TypeError when you try to mutate it",
                    "The list is automatically copied for each new instance",
                    "Nothing — class attributes are read-only",
                ],
                explanation="All instances reference the same list object; mutation through any one of them affects all.",
                difficulty="hard",
            ),
        ],
        mini_exercise=Exercise(
            id="i11-ex",
            title="Stack Implementation",
            instructions=(
                "Implement a `Stack` class with:\n"
                "  - `push(item)` — add item to the top.\n"
                "  - `pop()` — remove and return the top item; raise `IndexError` if empty.\n"
                "  - `peek()` — return the top item without removing it.\n"
                "  - `is_empty()` — return True if the stack has no items.\n"
                "  - `__len__()` — return the number of items.\n"
                "  - `__repr__()` — return `Stack([...])` showing the items.\n\n"
                "Demonstrate:\n"
                "  s = Stack()\n"
                "  s.push(1); s.push(2); s.push(3)\n"
                "  print(len(s))    # 3\n"
                "  print(s.pop())   # 3\n"
                "  print(s.peek())  # 2\n"
                "  print(repr(s))   # Stack([1, 2])"
            ),
            starter_code=(
                "class Stack:\n"
                "    def __init__(self):\n"
                "        self._items = []\n"
                "\n"
                "    def push(self, item):\n"
                "        pass\n"
                "\n"
                "    def pop(self):\n"
                "        pass\n"
                "\n"
                "    def peek(self):\n"
                "        pass\n"
                "\n"
                "    def is_empty(self):\n"
                "        pass\n"
                "\n"
                "    def __len__(self):\n"
                "        pass\n"
                "\n"
                "    def __repr__(self):\n"
                "        pass\n"
                "\n"
                "s = Stack()\n"
                "s.push(1); s.push(2); s.push(3)\n"
                "print(len(s))\n"
                "print(s.pop())\n"
                "print(s.peek())\n"
                "print(repr(s))"
            ),
            expected_output="3\n3\n2\nStack([1, 2])",
            hints=[
                "`push` appends to `self._items`.",
                "`pop` should check `is_empty()` first, then return `self._items.pop()`.",
                "`peek` returns `self._items[-1]`.",
                "`__len__` returns `len(self._items)`.",
            ],
            solution=(
                "class Stack:\n"
                "    def __init__(self):\n"
                "        self._items = []\n"
                "\n"
                "    def push(self, item):\n"
                "        self._items.append(item)\n"
                "\n"
                "    def pop(self):\n"
                "        if self.is_empty():\n"
                "            raise IndexError('pop from empty stack')\n"
                "        return self._items.pop()\n"
                "\n"
                "    def peek(self):\n"
                "        if self.is_empty():\n"
                "            raise IndexError('peek at empty stack')\n"
                "        return self._items[-1]\n"
                "\n"
                "    def is_empty(self):\n"
                "        return len(self._items) == 0\n"
                "\n"
                "    def __len__(self):\n"
                "        return len(self._items)\n"
                "\n"
                "    def __repr__(self):\n"
                "        return f'Stack({self._items})'\n"
                "\n"
                "s = Stack()\n"
                "s.push(1); s.push(2); s.push(3)\n"
                "print(len(s))\n"
                "print(s.pop())\n"
                "print(s.peek())\n"
                "print(repr(s))"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i12 — Instances
    # -------------------------------------------------------------------------
    Lesson(
        id="i12",
        title="Instances",
        level=Level.INTERMEDIATE,
        estimated_minutes=13,
        explanation=(
            "Every time you call a class like a function — `Dog('Rex', 3)` — Python "
            "creates a brand-new instance of that class. Under the hood, Python calls "
            "`Dog.__new__(Dog)` to allocate the object, then calls `Dog.__init__(instance, 'Rex', 3)` "
            "to initialise it. You almost never need to override `__new__` directly; "
            "`__init__` is the right place for almost all setup work.\n\n"
            "Each instance has its own `__dict__` — a dictionary of instance attributes. "
            "When you write `self.name = 'Rex'`, you are inserting `'name': 'Rex'` into "
            "that dict. `vars(obj)` returns the instance dict, which is useful for "
            "introspection and debugging. Since attribute lookup walks up the inheritance "
            "chain, an instance inherits all class and parent-class attributes while "
            "keeping its own independent data.\n\n"
            "Python provides several built-in tools for working with instances: "
            "`isinstance(obj, ClassName)` checks whether an object is an instance of a "
            "class (or a subclass); `issubclass(Child, Parent)` checks the class "
            "hierarchy. `type(obj)` returns the exact class — it is stricter than "
            "`isinstance` and does not account for inheritance. `hasattr(obj, 'name')` "
            "and `getattr(obj, 'name', default)` let you probe and fetch attributes "
            "dynamically.\n\n"
            "Object identity (is two names pointing to the same object in memory) vs "
            "equality (do two objects have the same value) is a common source of bugs. "
            "The `is` operator checks identity — two equal objects can still be different "
            "objects. `==` checks value equality using `__eq__`. Mutable default arguments "
            "in `__init__` are the classic Python gotcha: never write "
            "`def __init__(self, items=[])` — every instance will share the *same* list."
        ),
        key_terms={
            "instance": "A single concrete object created from a class blueprint.",
            "__dict__": "The per-instance dictionary that stores all instance attributes.",
            "isinstance()": "Returns True if obj is an instance of a class or any subclass.",
            "identity (is)": "Whether two names reference the exact same object in memory.",
            "equality (==)": "Whether two objects are considered equal by their __eq__ method.",
            "mutable default argument": "A common bug: using `[]` or `{}` as a default in def causes sharing across calls.",
        },
        code_examples=[
            CodeExample(
                title="Instance creation and __dict__",
                code=(
                    "class Point:\n"
                    "    def __init__(self, x, y):\n"
                    "        self.x = x\n"
                    "        self.y = y\n"
                    "\n"
                    "p1 = Point(1, 2)\n"
                    "p2 = Point(1, 2)\n"
                    "print(vars(p1))\n"
                    "print(p1 is p2)\n"
                    "print(p1.x == p2.x)"
                ),
                explanation="Two equal-value Points are different objects in memory.",
                output="{'x': 1, 'y': 2}\nFalse\nTrue",
                line_notes={
                    1: "Define Point with x and y attributes.",
                    6: "Create first instance.",
                    7: "Create second instance — same values, different object.",
                    8: "`vars()` returns the instance's `__dict__`.",
                    9: "`is` checks identity — they are different objects, so False.",
                    10: "`==` compares values — both x attributes are 1, so True.",
                },
            ),
            CodeExample(
                title="isinstance and type checking",
                code=(
                    "class Animal:\n"
                    "    pass\n"
                    "\n"
                    "class Dog(Animal):\n"
                    "    pass\n"
                    "\n"
                    "rex = Dog()\n"
                    "print(isinstance(rex, Dog))\n"
                    "print(isinstance(rex, Animal))\n"
                    "print(type(rex) is Dog)\n"
                    "print(type(rex) is Animal)"
                ),
                explanation="`isinstance` respects inheritance; `type(...) is` is exact.",
                output="True\nTrue\nTrue\nFalse",
                line_notes={
                    1: "Base class Animal.",
                    4: "Dog inherits from Animal.",
                    7: "Create a Dog instance.",
                    8: "`isinstance(rex, Dog)` — True, rex is a Dog.",
                    9: "`isinstance(rex, Animal)` — True, Dog is a subclass of Animal.",
                    10: "`type(rex) is Dog` — True, the exact class is Dog.",
                    11: "`type(rex) is Animal` — False, Animal is not the exact class.",
                },
            ),
            CodeExample(
                title="Mutable default argument gotcha",
                code=(
                    "class Bag:\n"
                    "    def __init__(self, items=[]):  # BUG: shared list!\n"
                    "        self.items = items\n"
                    "\n"
                    "b1 = Bag()\n"
                    "b2 = Bag()\n"
                    "b1.items.append('apple')\n"
                    "print(b2.items)"
                ),
                explanation="Both b1 and b2 share the same default list — appending to b1 affects b2.",
                output="['apple']",
                line_notes={
                    1: "Bag class.",
                    2: "Using `[]` as a default is a bug — the list is created once and shared.",
                    5: "b1 created without arguments — gets the shared list.",
                    6: "b2 also gets the same shared list.",
                    7: "Mutate b1's items list.",
                    8: "b2 sees the mutation — they reference the same list object!",
                },
            ),
        ],
        common_mistakes=[
            "Using a mutable default argument in `__init__` — use `None` and create a fresh list/dict inside the method body.",
            "Using `==` when you mean `is` (or vice versa) — `None` checks should always use `is None`.",
            "Using `type(obj) == ClassName` instead of `isinstance(obj, ClassName)` — `type` breaks polymorphism.",
            "Assuming two instances with identical attribute values are the same object — `==` is equality, `is` is identity.",
        ],
        practice_prompts=[
            "Fix the mutable default argument bug by using `None` as the default and initialising to `[]` inside `__init__`.",
            "Write code that creates three `Car` instances and verifies each has its own `mileage` attribute.",
            "Use `isinstance()` to write a function that accepts either an `int` or a `float` but rejects strings.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does `vars(obj)` return?",
                qtype="multiple_choice",
                correct_answer="The instance's __dict__ containing its instance attributes",
                options=[
                    "The instance's __dict__ containing its instance attributes",
                    "A list of all method names on the object",
                    "The class the object belongs to",
                    "A string representation of the object",
                ],
                explanation="`vars(obj)` returns `obj.__dict__` — the mapping of attribute names to values for that instance.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="`isinstance(obj, Parent)` returns True even if obj is an instance of a subclass of Parent.",
                qtype="true_false",
                correct_answer="true",
                explanation="`isinstance` walks the class hierarchy; subclass instances pass the parent-class check.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is the correct way to check if a variable holds `None`?",
                qtype="multiple_choice",
                correct_answer="x is None",
                options=["x == None", "x is None", "x === None", "isinstance(x, None)"],
                explanation="`is None` checks identity — there is only one `None` object; `== None` works but is less Pythonic and can be fooled by `__eq__`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Why is `def __init__(self, tags=[])` a bug?",
                qtype="short_answer",
                correct_answer="The default list [] is created once when the function is defined and shared across all instances that use the default, so mutating it in one instance affects all others.",
                keywords=["shared", "default", "created once", "mutation", "all instances"],
                explanation="Use `None` as the default and `self.tags = tags if tags is not None else []` in the body.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i12-ex",
            title="Counter with Fixed Default",
            instructions=(
                "The buggy `Counter` class below shares a single history list across all "
                "instances. Fix it so each instance gets its own independent history.\n\n"
                "Then verify the fix:\n"
                "  c1 = Counter()\n"
                "  c2 = Counter()\n"
                "  c1.increment()\n"
                "  c1.increment()\n"
                "  print(c1.count)    # 2\n"
                "  print(c2.count)    # 0\n"
                "  print(c1.history)  # [1, 2]\n"
                "  print(c2.history)  # []"
            ),
            starter_code=(
                "class Counter:\n"
                "    def __init__(self, history=[]):  # BUG!\n"
                "        self.count = 0\n"
                "        self.history = history\n"
                "\n"
                "    def increment(self):\n"
                "        self.count += 1\n"
                "        self.history.append(self.count)\n"
                "\n"
                "c1 = Counter()\n"
                "c2 = Counter()\n"
                "c1.increment()\n"
                "c1.increment()\n"
                "print(c1.count)\n"
                "print(c2.count)\n"
                "print(c1.history)\n"
                "print(c2.history)"
            ),
            expected_output="2\n0\n[1, 2]\n[]",
            hints=[
                "Change the default argument from `history=[]` to `history=None`.",
                "Inside `__init__`, add: `self.history = history if history is not None else []`.",
                "This creates a new list for each instance that doesn't pass a `history` argument.",
            ],
            solution=(
                "class Counter:\n"
                "    def __init__(self, history=None):\n"
                "        self.count = 0\n"
                "        self.history = history if history is not None else []\n"
                "\n"
                "    def increment(self):\n"
                "        self.count += 1\n"
                "        self.history.append(self.count)\n"
                "\n"
                "c1 = Counter()\n"
                "c2 = Counter()\n"
                "c1.increment()\n"
                "c1.increment()\n"
                "print(c1.count)\n"
                "print(c2.count)\n"
                "print(c1.history)\n"
                "print(c2.history)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i13 — Attributes (instance vs class; __dict__; property)
    # -------------------------------------------------------------------------
    Lesson(
        id="i13",
        title="Attributes",
        level=Level.INTERMEDIATE,
        estimated_minutes=14,
        explanation=(
            "Attributes are the data that lives on a class or its instances. Python "
            "distinguishes two kinds: *class attributes* are defined directly in the "
            "class body and are shared by every instance; *instance attributes* are "
            "created by assigning to `self.name` and belong exclusively to one object. "
            "When Python resolves `obj.attr`, it first searches the instance's own "
            "`__dict__`, then the class's `__dict__`, then parent classes in MRO order.\n\n"
            "Each instance carries a `__dict__` — a plain Python dictionary of its "
            "instance attributes. You can inspect it with `vars(obj)` or `obj.__dict__`. "
            "This transparency is powerful for debugging: you can print an object's "
            "entire state in one call. Dynamic attribute assignment (`obj.new_attr = val`) "
            "works at any time, not just in `__init__`.\n\n"
            "The `@property` decorator lets you expose a method as if it were a plain "
            "attribute. Callers write `account.balance` without parentheses, but behind "
            "the scenes Python calls the getter function you defined. Paired with a "
            "`@name.setter`, you can validate values on assignment. This is how Python "
            "achieves encapsulation without Java-style explicit getters and setters.\n\n"
            "For the BankAccount domain used throughout lessons i13-i19: `bank_name` is "
            "a class attribute shared by all accounts at the same bank; `owner` and "
            "`balance` are instance attributes unique to each account."
        ),
        key_terms={
            "class attribute": "A value defined in the class body; shared by all instances.",
            "instance attribute": "A value stored on a specific object via `self.name = value`.",
            "__dict__": "The per-instance (or per-class) dict that holds attribute name/value pairs.",
            "@property": "Decorator that exposes a method as a read-only attribute.",
            "@name.setter": "Decorator that allows validated assignment to a property.",
            "attribute lookup": "The MRO chain Python walks to find obj.attr: instance → class → parents.",
        },
        code_examples=[
            CodeExample(
                title="Instance vs class attributes in BankAccount",
                code=(
                    "class BankAccount:\n"
                    "    bank_name = 'PyBank'  # class attribute\n"
                    "\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner      # instance attribute\n"
                    "        self.balance = balance  # instance attribute\n"
                    "\n"
                    "a1 = BankAccount('Alice', 500)\n"
                    "a2 = BankAccount('Bob')\n"
                    "print(a1.bank_name, a2.bank_name)\n"
                    "print(vars(a1))"
                ),
                explanation="bank_name is shared; owner and balance are per-instance.",
                output="PyBank PyBank\n{'owner': 'Alice', 'balance': 500}",
                line_notes={
                    1: "Class definition — BankAccount is the blueprint.",
                    2: "Class attribute: one value for ALL BankAccount instances.",
                    4: "`__init__` initialises each new instance.",
                    5: "Instance attribute — unique to this account.",
                    6: "Another instance attribute; default value is 0.0.",
                    8: "Create Alice's account with 500 initial balance.",
                    9: "Bob's account uses the default balance of 0.0.",
                    10: "Both accounts access the same class attribute.",
                    11: "`vars()` shows only instance attributes, not class attributes.",
                },
            ),
            CodeExample(
                title="Property for validated balance",
                code=(
                    "class BankAccount:\n"
                    "    bank_name = 'PyBank'\n"
                    "\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = balance\n"
                    "\n"
                    "    @property\n"
                    "    def balance(self):\n"
                    "        return self._balance\n"
                    "\n"
                    "    @balance.setter\n"
                    "    def balance(self, amount):\n"
                    "        if amount < 0:\n"
                    "            raise ValueError('Balance cannot be negative')\n"
                    "        self._balance = amount\n"
                    "\n"
                    "a = BankAccount('Alice', 100)\n"
                    "print(a.balance)\n"
                    "a.balance = 200\n"
                    "print(a.balance)"
                ),
                explanation="Use _balance internally; expose balance via property with validation.",
                output="100\n200",
                line_notes={
                    6: "Store internally with underscore convention — 'private by convention'.",
                    8: "@property turns this method into a readable attribute.",
                    12: "@balance.setter intercepts `a.balance = value` assignments.",
                    14: "Reject negative balances before they corrupt state.",
                    20: "Assignment triggers the setter, not a direct dict write.",
                },
            ),
            CodeExample(
                title="Shadowing a class attribute",
                code=(
                    "class BankAccount:\n"
                    "    bank_name = 'PyBank'\n"
                    "\n"
                    "a = BankAccount.__new__(BankAccount)\n"
                    "a.bank_name = 'LocalBank'\n"
                    "print(a.bank_name)\n"
                    "print(BankAccount.bank_name)"
                ),
                explanation="Setting bank_name on the instance shadows (not overwrites) the class attribute.",
                output="LocalBank\nPyBank",
                line_notes={
                    4: "__new__ creates a bare instance without calling __init__.",
                    5: "Assign to the instance — creates an instance attribute that shadows the class one.",
                    6: "Instance lookup finds the instance attribute first.",
                    7: "The class attribute is still unchanged.",
                },
            ),
        ],
        common_mistakes=[
            "Using a mutable class attribute (list or dict) and mutating it via an instance — all instances are affected.",
            "Forgetting the underscore prefix for private-by-convention attributes paired with a @property.",
            "Accessing `obj.__dict__` expecting to see class attributes — `__dict__` only shows instance attributes.",
            "Defining the setter before the getter — Python looks up the property by name; getter must come first.",
        ],
        practice_prompts=[
            "Add a class attribute `interest_rate = 0.03` to BankAccount and a property that computes monthly interest as balance * interest_rate / 12.",
            "Write a BankAccount property `display_name` that returns 'owner @ bank_name'.",
            "Inspect `vars()` of two different BankAccount instances to confirm they have independent attribute dicts.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="A class attribute defined in the class body is shared by all instances.",
                qtype="true_false",
                correct_answer="true",
                explanation="Class attributes live on the class object itself; every instance that hasn't shadowed it sees the same value.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which built-in returns the instance's attribute dictionary?",
                qtype="multiple_choice",
                correct_answer="vars(obj)",
                options=["dir(obj)", "vars(obj)", "type(obj)", "attrs(obj)"],
                explanation="`vars(obj)` returns `obj.__dict__` — the dict of instance attributes.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What decorator turns a method into a readable attribute (no parentheses on access)?",
                qtype="fill_blank",
                correct_answer="@property",
                explanation="`@property` makes the method callable as `obj.name` without `()`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="If an instance and its class both have an attribute with the same name, which one does Python use?",
                qtype="multiple_choice",
                correct_answer="The instance attribute shadows the class attribute",
                options=[
                    "The instance attribute shadows the class attribute",
                    "The class attribute always wins",
                    "Python raises AttributeError",
                    "The last one assigned wins regardless",
                ],
                explanation="Python checks instance __dict__ first, so the instance attribute takes precedence.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="The `@balance.setter` decorator lets you validate values when assigning to a property.",
                qtype="true_false",
                correct_answer="true",
                explanation="The setter intercepts `obj.balance = value`, allowing you to raise an error or transform the value before storing.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i13-ex",
            title="BankAccount Attributes",
            instructions=(
                "Create a BankAccount class with:\n"
                "  - Class attribute `bank_name = 'PyBank'`\n"
                "  - Instance attributes `owner` and `_balance` (set via __init__)\n"
                "  - A `balance` property that returns `_balance`\n"
                "  - A `balance` setter that raises ValueError if amount < 0\n\n"
                "Then run:\n"
                "  a = BankAccount('Alice', 1000)\n"
                "  print(a.bank_name)   # PyBank\n"
                "  print(a.balance)     # 1000\n"
                "  print(vars(a))       # shows owner and _balance"
            ),
            starter_code=(
                "class BankAccount:\n"
                "    bank_name = 'PyBank'\n"
                "\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = balance\n"
                "\n"
                "    # Add property here\n"
                "\n"
                "a = BankAccount('Alice', 1000)\n"
                "print(a.bank_name)\n"
                "print(a.balance)\n"
                "print(vars(a))"
            ),
            expected_output="PyBank\n1000\n{'owner': 'Alice', '_balance': 1000}",
            hints=[
                "Add `@property` above a `def balance(self):` method that returns `self._balance`.",
                "Add `@balance.setter` above a `def balance(self, amount):` method.",
                "In the setter, check `if amount < 0: raise ValueError(...)`.",
            ],
            solution=(
                "class BankAccount:\n"
                "    bank_name = 'PyBank'\n"
                "\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = balance\n"
                "\n"
                "    @property\n"
                "    def balance(self):\n"
                "        return self._balance\n"
                "\n"
                "    @balance.setter\n"
                "    def balance(self, amount):\n"
                "        if amount < 0:\n"
                "            raise ValueError('Balance cannot be negative')\n"
                "        self._balance = amount\n"
                "\n"
                "a = BankAccount('Alice', 1000)\n"
                "print(a.bank_name)\n"
                "print(a.balance)\n"
                "print(vars(a))"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i14 — Methods (instance, class, static)
    # -------------------------------------------------------------------------
    Lesson(
        id="i14",
        title="Methods",
        level=Level.INTERMEDIATE,
        estimated_minutes=13,
        explanation=(
            "A method is a function defined inside a class body. Python provides three "
            "flavours, each with a different first argument and different use cases. "
            "Understanding which to use keeps your class interface clean and correct.\n\n"
            "*Instance methods* receive `self` (the object) as their first argument. "
            "They can read and write instance attributes and call other instance methods. "
            "These are the most common and cover the majority of class behaviour — "
            "`deposit()` and `withdraw()` on BankAccount are instance methods.\n\n"
            "*Class methods*, decorated with `@classmethod`, receive `cls` (the class "
            "itself) as their first argument instead of an instance. They cannot access "
            "instance data. The canonical use is an alternative constructor: "
            "`BankAccount.from_dict({'owner': 'Alice', 'balance': 200})` reads from a "
            "dictionary and returns a new BankAccount. Using `cls(...)` instead of "
            "`BankAccount(...)` means the method works correctly in subclasses.\n\n"
            "*Static methods*, decorated with `@staticmethod`, receive neither `self` "
            "nor `cls`. They are plain functions that happen to be logically grouped "
            "inside the class. `validate_amount(amount)` — which just checks that a "
            "number is positive — belongs on BankAccount conceptually but doesn't need "
            "access to any instance or class state, making it a perfect static method."
        ),
        key_terms={
            "instance method": "A method receiving `self`; can access and modify instance state.",
            "class method": "A method decorated with @classmethod; receives `cls`, used for alternative constructors.",
            "static method": "A method decorated with @staticmethod; receives neither self nor cls.",
            "@classmethod": "Decorator that passes the class as the first argument.",
            "@staticmethod": "Decorator that removes the automatic first argument entirely.",
            "alternative constructor": "A class method that creates an instance from a different input format.",
        },
        code_examples=[
            CodeExample(
                title="All three method types on BankAccount",
                code=(
                    "class BankAccount:\n"
                    "    bank_name = 'PyBank'\n"
                    "\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def deposit(self, amount):        # instance method\n"
                    "        self._balance += amount\n"
                    "\n"
                    "    @classmethod\n"
                    "    def from_dict(cls, data):         # class method\n"
                    "        return cls(data['owner'], data.get('balance', 0))\n"
                    "\n"
                    "    @staticmethod\n"
                    "    def validate_amount(amount):      # static method\n"
                    "        return isinstance(amount, (int, float)) and amount > 0\n"
                    "\n"
                    "a = BankAccount.from_dict({'owner': 'Alice', 'balance': 500})\n"
                    "print(BankAccount.validate_amount(100))\n"
                    "a.deposit(50)\n"
                    "print(a._balance)"
                ),
                explanation="deposit is instance, from_dict is classmethod constructor, validate_amount is static.",
                output="True\n550.0",
                line_notes={
                    8: "Instance method — `self` gives access to this account's data.",
                    11: "@classmethod decorator makes the next method receive `cls`.",
                    12: "`cls` is the class; calling `cls(...)` works for subclasses too.",
                    15: "@staticmethod — no self or cls; pure utility function.",
                    19: "Call the classmethod on the class, not an instance.",
                    20: "Static methods can be called on the class or an instance.",
                },
            ),
            CodeExample(
                title="Why cls beats hard-coding the class name",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    @classmethod\n"
                    "    def from_dict(cls, data):\n"
                    "        return cls(data['owner'], data['balance'])\n"
                    "\n"
                    "class SavingsAccount(BankAccount):\n"
                    "    pass\n"
                    "\n"
                    "data = {'owner': 'Bob', 'balance': 200}\n"
                    "s = SavingsAccount.from_dict(data)\n"
                    "print(type(s).__name__)"
                ),
                explanation="Because we used cls, from_dict on SavingsAccount creates a SavingsAccount, not a BankAccount.",
                output="SavingsAccount",
                line_notes={
                    8: "`cls` is SavingsAccount when called via SavingsAccount.from_dict.",
                    14: "Calling the inherited classmethod on the subclass.",
                    15: "Returns 'SavingsAccount' — correct polymorphic behaviour.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting `self` as the first parameter of an instance method — Python won't automatically pass the instance.",
            "Using a classmethod when you need instance state — classmethods cannot access `self`.",
            "Using a staticmethod when the logic should vary per-subclass — a classmethod with `cls` is more flexible.",
            "Calling an instance method on the class: `BankAccount.deposit(50)` fails because there's no instance.",
        ],
        practice_prompts=[
            "Add a `withdraw(amount)` instance method to BankAccount that reduces balance (raise ValueError if insufficient funds).",
            "Add a `from_csv_row(cls, row_string)` classmethod that parses 'Alice,500' into a BankAccount.",
            "Add a `is_valid_owner(name)` staticmethod that returns True if name is a non-empty string.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which decorator makes a method receive the class as its first argument?",
                qtype="fill_blank",
                correct_answer="@classmethod",
                explanation="`@classmethod` passes `cls` (the class) as the first argument instead of an instance.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A static method can access instance attributes via self.",
                qtype="true_false",
                correct_answer="false",
                explanation="Static methods receive neither `self` nor `cls`; they have no access to instance or class state.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Why use `cls(...)` instead of `ClassName(...)` in a classmethod?",
                qtype="multiple_choice",
                correct_answer="So the method works correctly when called on a subclass",
                options=[
                    "So the method works correctly when called on a subclass",
                    "cls is faster to type than the class name",
                    "cls avoids importing the class",
                    "There is no difference",
                ],
                explanation="When a subclass calls the inherited classmethod, `cls` is the subclass, so `cls(...)` creates an instance of the right type.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which method type is best for a utility function that belongs conceptually to a class but needs no instance or class data?",
                qtype="multiple_choice",
                correct_answer="static method",
                options=["instance method", "class method", "static method", "property"],
                explanation="Static methods group related utilities in the class namespace without requiring self or cls.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i14-ex",
            title="BankAccount Methods",
            instructions=(
                "Extend BankAccount with three methods:\n"
                "  1. deposit(amount) — instance method; adds amount to _balance\n"
                "  2. from_dict(data) — classmethod; creates account from a dict\n"
                "  3. validate_amount(amount) — staticmethod; returns True if amount > 0\n\n"
                "Run:\n"
                "  a = BankAccount.from_dict({'owner': 'Alice', 'balance': 300})\n"
                "  a.deposit(100)\n"
                "  print(a._balance)                        # 400.0\n"
                "  print(BankAccount.validate_amount(-5))   # False"
            ),
            starter_code=(
                "class BankAccount:\n"
                "    bank_name = 'PyBank'\n"
                "\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    # Add deposit, from_dict, validate_amount here\n"
                "\n"
                "a = BankAccount.from_dict({'owner': 'Alice', 'balance': 300})\n"
                "a.deposit(100)\n"
                "print(a._balance)\n"
                "print(BankAccount.validate_amount(-5))"
            ),
            expected_output="400.0\nFalse",
            hints=[
                "deposit: `self._balance += amount`",
                "from_dict: decorated with @classmethod, returns cls(data['owner'], data.get('balance', 0))",
                "validate_amount: decorated with @staticmethod, returns `amount > 0`",
            ],
            solution=(
                "class BankAccount:\n"
                "    bank_name = 'PyBank'\n"
                "\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        self._balance += amount\n"
                "\n"
                "    @classmethod\n"
                "    def from_dict(cls, data):\n"
                "        return cls(data['owner'], data.get('balance', 0))\n"
                "\n"
                "    @staticmethod\n"
                "    def validate_amount(amount):\n"
                "        return amount > 0\n"
                "\n"
                "a = BankAccount.from_dict({'owner': 'Alice', 'balance': 300})\n"
                "a.deposit(100)\n"
                "print(a._balance)\n"
                "print(BankAccount.validate_amount(-5))"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i15 — The self Parameter
    # -------------------------------------------------------------------------
    Lesson(
        id="i15",
        title="The self Parameter",
        level=Level.INTERMEDIATE,
        estimated_minutes=10,
        explanation=(
            "`self` is the conventional name for the first parameter of every instance "
            "method in Python. When you call `account.deposit(100)`, Python automatically "
            "passes the object `account` as the first argument to `deposit`. Inside the "
            "method, that object is available as `self`. The name `self` is not a keyword "
            "— you could write `this` or `me` and Python would not complain — but "
            "deviating from `self` is a strong convention violation that will confuse "
            "every reader of your code.\n\n"
            "The mechanism is straightforward: `account.deposit(100)` is exactly "
            "equivalent to `BankAccount.deposit(account, 100)`. The dot-call syntax is "
            "syntactic sugar that inserts the object as the first positional argument. "
            "This is why a method defined as `def deposit(self, amount)` is called with "
            "only one argument from the outside — Python supplies `self` automatically.\n\n"
            "Common confusion arises when a beginner forgets `self.` when accessing an "
            "instance attribute inside a method. Writing `balance += amount` creates a "
            "local variable `balance` that vanishes when the method returns; "
            "`self._balance += amount` modifies the object's persistent attribute. "
            "Similarly, calling another method from inside the class requires "
            "`self.other_method()` — just `other_method()` looks for a global function.\n\n"
            "In class methods, `cls` plays the analogous role for the class itself. "
            "In static methods, there is no automatic first argument at all."
        ),
        key_terms={
            "self": "The conventional name for the first parameter of an instance method; refers to the calling instance.",
            "implicit passing": "Python automatically passes the instance as the first argument when you call obj.method().",
            "bound method": "A method that has already captured its instance; `account.deposit` is a bound method.",
            "unbound call": "Calling a method via the class: `BankAccount.deposit(account, 100)`.",
            "local variable": "A variable inside a function that disappears on return — distinct from `self.attr`.",
        },
        code_examples=[
            CodeExample(
                title="self is the instance",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def deposit(self, amount):\n"
                    "        self._balance += amount\n"
                    "        return self  # enables chaining\n"
                    "\n"
                    "a = BankAccount('Alice', 100)\n"
                    "BankAccount.deposit(a, 50)   # explicit self\n"
                    "a.deposit(50)                # implicit self\n"
                    "print(a._balance)"
                ),
                explanation="Both calls are identical; dot-notation just inserts the instance automatically.",
                output="200.0",
                line_notes={
                    6: "self refers to whatever instance deposit is called on.",
                    7: "self._balance is the instance attribute — persistent across calls.",
                    8: "Returning self enables method chaining.",
                    11: "Explicit form: pass the instance as the first argument.",
                    12: "Implicit form: Python passes `a` for you.",
                },
            ),
            CodeExample(
                title="Forgetting self. is a classic bug",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def bad_deposit(self, amount):\n"
                    "        balance = self._balance + amount  # local var!\n"
                    "        # self._balance never updated\n"
                    "\n"
                    "    def good_deposit(self, amount):\n"
                    "        self._balance += amount\n"
                    "\n"
                    "a = BankAccount('Alice', 100)\n"
                    "a.bad_deposit(50)\n"
                    "print(a._balance)\n"
                    "a.good_deposit(50)\n"
                    "print(a._balance)"
                ),
                explanation="bad_deposit creates a throwaway local; good_deposit updates the instance attribute.",
                output="100.0\n150.0",
                line_notes={
                    7: "Creates a LOCAL variable `balance` — gone when the method returns.",
                    11: "self._balance persists on the object after the method returns.",
                    14: "No effect on the account balance.",
                    16: "Correctly increments the persistent attribute.",
                },
            ),
        ],
        common_mistakes=[
            "Omitting `self` as the first parameter: `def deposit(amount)` — Python passes the instance as `amount`, causing a TypeError.",
            "Writing `balance += amount` instead of `self._balance += amount` — creates a local variable that vanishes.",
            "Calling a sibling method without `self.`: `validate()` instead of `self.validate()`.",
            "Thinking `self` is a keyword — it is just a strong convention; any name works but only `self` is Pythonic.",
        ],
        practice_prompts=[
            "Write a withdraw(amount) method and call it both the explicit (BankAccount.withdraw(a, x)) and implicit (a.withdraw(x)) ways.",
            "Add a summary() method that returns 'owner: X, balance: Y' using self attributes.",
            "Create two BankAccount instances and confirm that modifying one's balance does not affect the other.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="`self` is a Python keyword that must be used as the first parameter name.",
                qtype="true_false",
                correct_answer="false",
                explanation="`self` is a naming convention only. Python accepts any name, but using anything other than `self` violates PEP 8.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is the explicit form of `account.deposit(100)`?",
                qtype="multiple_choice",
                correct_answer="BankAccount.deposit(account, 100)",
                options=[
                    "BankAccount.deposit(account, 100)",
                    "deposit(account, 100)",
                    "account.deposit(self, 100)",
                    "BankAccount.deposit(100)",
                ],
                explanation="Python translates dot-notation into passing the instance as the first positional argument.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Inside a method, writing `balance = 0` instead of `self.balance = 0` creates a ___.",
                qtype="fill_blank",
                correct_answer="local variable",
                explanation="Without `self.`, the assignment creates a local variable that disappears when the method returns.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="How do you call another instance method from inside a method?",
                qtype="multiple_choice",
                correct_answer="self.other_method()",
                options=["other_method()", "self.other_method()", "cls.other_method()", "super().other_method()"],
                explanation="`self.other_method()` routes through the instance; bare `other_method()` looks for a global function.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i15-ex",
            title="Method Chaining with self",
            instructions=(
                "Add deposit and withdraw methods to BankAccount that each return self.\n"
                "This enables chaining:\n\n"
                "  a = BankAccount('Alice', 100)\n"
                "  a.deposit(200).deposit(50).withdraw(75)\n"
                "  print(a._balance)  # 275.0"
            ),
            starter_code=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        pass  # add to balance, return self\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        pass  # subtract from balance, return self\n"
                "\n"
                "a = BankAccount('Alice', 100)\n"
                "a.deposit(200).deposit(50).withdraw(75)\n"
                "print(a._balance)"
            ),
            expected_output="275.0",
            hints=[
                "At the end of deposit: `return self`",
                "At the end of withdraw: `return self`",
                "Chaining works because each call returns the same object.",
            ],
            solution=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        self._balance += amount\n"
                "        return self\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        self._balance -= amount\n"
                "        return self\n"
                "\n"
                "a = BankAccount('Alice', 100)\n"
                "a.deposit(200).deposit(50).withdraw(75)\n"
                "print(a._balance)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i16 — The __init__ Constructor
    # -------------------------------------------------------------------------
    Lesson(
        id="i16",
        title="The __init__ Constructor",
        level=Level.INTERMEDIATE,
        estimated_minutes=13,
        explanation=(
            "`__init__` is the *initialiser* method — it runs automatically immediately "
            "after Python creates a new instance with `__new__`. Its job is to put the "
            "object into a valid, usable initial state by setting instance attributes. "
            "Every value you assign to `self.attr` in `__init__` becomes available on "
            "the object for its entire lifetime.\n\n"
            "Like any function, `__init__` can have default argument values. "
            "`def __init__(self, owner, balance=0.0)` makes `balance` optional — callers "
            "can write `BankAccount('Alice')` and the account starts at zero. Default "
            "values should be immutable (numbers, strings, None, tuples); never use a "
            "mutable default like `[]` or `{}` because it is shared across all calls.\n\n"
            "When a subclass defines its own `__init__`, it should call "
            "`super().__init__(...)` to ensure the parent class sets up its attributes "
            "first. Without this call, the parent's attributes are never created and any "
            "parent method that accesses them will raise `AttributeError`. `super()` "
            "returns a proxy that delegates to the next class in the MRO, making it "
            "robust in multiple-inheritance hierarchies.\n\n"
            "If a class doesn't define `__init__`, Python falls back to `object.__init__`, "
            "which accepts only `self` and sets no attributes. Defining `__init__` is "
            "optional for classes that carry no state — though such classes are unusual."
        ),
        key_terms={
            "__init__": "The initialiser called right after object creation; sets up instance state.",
            "default argument": "A parameter with a fallback value used when the caller omits it.",
            "super().__init__()": "Calls the parent class's __init__ to initialise inherited attributes.",
            "MRO": "Method Resolution Order — the chain Python follows when looking up methods.",
            "__new__": "The allocator called before __init__; rarely overridden directly.",
        },
        code_examples=[
            CodeExample(
                title="BankAccount __init__ with defaults",
                code=(
                    "class BankAccount:\n"
                    "    bank_name = 'PyBank'\n"
                    "\n"
                    "    def __init__(self, owner, balance=0.0, currency='USD'):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "        self.currency = currency\n"
                    "\n"
                    "a1 = BankAccount('Alice', 500)\n"
                    "a2 = BankAccount('Bob', 200, 'EUR')\n"
                    "print(a1.currency, a1._balance)\n"
                    "print(a2.currency, a2._balance)"
                ),
                explanation="balance and currency have defaults; currency can be overridden.",
                output="USD 500.0\nEUR 200.0",
                line_notes={
                    4: "Two optional parameters with default values.",
                    6: "`float()` ensures balance is always a float, even if an int is passed.",
                    9: "Alice uses default currency 'USD'.",
                    10: "Bob overrides currency to 'EUR'.",
                },
            ),
            CodeExample(
                title="Calling super().__init__ in a subclass",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "class SavingsAccount(BankAccount):\n"
                    "    def __init__(self, owner, balance=0.0, rate=0.03):\n"
                    "        super().__init__(owner, balance)\n"
                    "        self.rate = rate\n"
                    "\n"
                    "s = SavingsAccount('Carol', 1000, rate=0.05)\n"
                    "print(s.owner, s._balance, s.rate)"
                ),
                explanation="super().__init__ sets up owner and _balance; then SavingsAccount adds rate.",
                output="Carol 1000.0 0.05",
                line_notes={
                    7: "SavingsAccount adds its own parameter `rate`.",
                    8: "Delegate owner and balance setup to the parent class.",
                    9: "Add the subclass-specific attribute after super().__init__ runs.",
                    11: "Create a SavingsAccount with all three attributes properly set.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting `super().__init__()` in a subclass — parent attributes never get created.",
            "Using a mutable default like `transactions=[]` in __init__ — all instances share the same list.",
            "Doing heavy work (file I/O, network calls) in __init__ — constructors should be fast; use factory methods instead.",
            "Returning a value from __init__ — Python ignores any return value except None, and some linters raise a warning.",
        ],
        practice_prompts=[
            "Add a `transactions` attribute (initialised to a new empty list) to BankAccount's __init__.",
            "Create a CheckingAccount subclass that calls super().__init__ and adds an `overdraft_limit` attribute.",
            "Write a BankAccount.__init__ that raises ValueError if owner is not a string or balance is negative.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What is the purpose of `super().__init__()` in a subclass?",
                qtype="multiple_choice",
                correct_answer="To call the parent class's __init__ so inherited attributes are set up",
                options=[
                    "To call the parent class's __init__ so inherited attributes are set up",
                    "To create a new instance of the parent class",
                    "To skip the parent class initialisation",
                    "To call __new__ on the parent class",
                ],
                explanation="Without `super().__init__()`, the parent's attributes are never assigned, causing AttributeError when parent methods try to access them.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="`__init__` is the method Python calls to allocate memory for a new object.",
                qtype="true_false",
                correct_answer="false",
                explanation="Memory allocation is done by `__new__`; `__init__` only *initialises* the already-created object.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What default value should you use for a list parameter in __init__ to avoid shared state?",
                qtype="multiple_choice",
                correct_answer="None",
                options=["[]", "None", "list()", "()"],
                explanation="Use `None` as the default, then assign `self.attr = attr if attr is not None else []` inside the body.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="If a class does not define __init__, what happens when you create an instance?",
                qtype="multiple_choice",
                correct_answer="Python uses object.__init__, which accepts only self and sets no attributes",
                options=[
                    "Python uses object.__init__, which accepts only self and sets no attributes",
                    "Python raises TypeError",
                    "Python calls __new__ but not __init__",
                    "Python looks for a __setup__ method instead",
                ],
                explanation="Every class implicitly inherits from `object`, which provides a no-op `__init__`.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i16-ex",
            title="SavingsAccount Constructor",
            instructions=(
                "Create a SavingsAccount that inherits from BankAccount.\n"
                "SavingsAccount.__init__ should accept owner, balance=0.0, and rate=0.03.\n"
                "It must call super().__init__ then set self.rate.\n\n"
                "  s = SavingsAccount('Dave', 2000, rate=0.04)\n"
                "  print(s.owner)     # Dave\n"
                "  print(s._balance)  # 2000.0\n"
                "  print(s.rate)      # 0.04"
            ),
            starter_code=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "class SavingsAccount(BankAccount):\n"
                "    def __init__(self, owner, balance=0.0, rate=0.03):\n"
                "        pass  # call super and set rate\n"
                "\n"
                "s = SavingsAccount('Dave', 2000, rate=0.04)\n"
                "print(s.owner)\n"
                "print(s._balance)\n"
                "print(s.rate)"
            ),
            expected_output="Dave\n2000.0\n0.04",
            hints=[
                "Call `super().__init__(owner, balance)` first.",
                "Then set `self.rate = rate`.",
            ],
            solution=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "class SavingsAccount(BankAccount):\n"
                "    def __init__(self, owner, balance=0.0, rate=0.03):\n"
                "        super().__init__(owner, balance)\n"
                "        self.rate = rate\n"
                "\n"
                "s = SavingsAccount('Dave', 2000, rate=0.04)\n"
                "print(s.owner)\n"
                "print(s._balance)\n"
                "print(s.rate)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i17 — Inheritance
    # -------------------------------------------------------------------------
    Lesson(
        id="i17",
        title="Inheritance",
        level=Level.INTERMEDIATE,
        estimated_minutes=15,
        explanation=(
            "Inheritance lets a *subclass* automatically acquire all the attributes and "
            "methods of its *parent* (or *base*) class, then add or override behaviour. "
            "You declare it by putting the parent in parentheses: "
            "`class SavingsAccount(BankAccount)`. Every instance of SavingsAccount is "
            "also a BankAccount — `isinstance(s, BankAccount)` returns `True`.\n\n"
            "The subclass can *override* any method by redefining it with the same name. "
            "SavingsAccount might override `withdraw` to deduct a small fee before each "
            "withdrawal — the parent's logic is no longer called unless the override "
            "explicitly invokes it with `super().withdraw(amount)`. Calling super is "
            "important whenever you want to extend rather than replace parent behaviour.\n\n"
            "Python's `super()` function returns a proxy that delegates method calls to "
            "the next class in the Method Resolution Order (MRO). For simple single "
            "inheritance `super()` is equivalent to 'call the parent', but in multiple "
            "inheritance its cooperative behaviour ensures each class in the chain is "
            "called exactly once. Always call `super()` without arguments in Python 3 — "
            "the two-argument form `super(ClassName, self)` is only needed in Python 2.\n\n"
            "Use inheritance for genuine *is-a* relationships. If SavingsAccount *is a* "
            "BankAccount, inheritance is appropriate. If it merely *uses* a BankAccount, "
            "prefer composition (covered in i18). Deep inheritance chains (more than 2-3 "
            "levels) are usually a sign that the design should be refactored."
        ),
        key_terms={
            "subclass": "A class that inherits from a parent class.",
            "parent / base class": "The class being inherited from.",
            "override": "Redefining a method in the subclass to replace the parent's version.",
            "super()": "A proxy that delegates to the next class in the MRO.",
            "MRO": "Method Resolution Order — the linearised list of classes Python searches for a method.",
            "is-a relationship": "The semantic criterion for inheritance: a Dog is an Animal.",
        },
        code_examples=[
            CodeExample(
                title="SavingsAccount overrides withdraw",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def deposit(self, amount):\n"
                    "        self._balance += amount\n"
                    "\n"
                    "    def withdraw(self, amount):\n"
                    "        if amount > self._balance:\n"
                    "            raise ValueError('Insufficient funds')\n"
                    "        self._balance -= amount\n"
                    "\n"
                    "class SavingsAccount(BankAccount):\n"
                    "    FEE = 2.0\n"
                    "\n"
                    "    def withdraw(self, amount):\n"
                    "        super().withdraw(amount + self.FEE)\n"
                    "\n"
                    "s = SavingsAccount('Carol', 500)\n"
                    "s.withdraw(100)\n"
                    "print(s._balance)"
                ),
                explanation="SavingsAccount charges a $2 fee on each withdrawal by calling super().withdraw with the adjusted amount.",
                output="398.0",
                line_notes={
                    14: "SavingsAccount inherits all of BankAccount's methods automatically.",
                    15: "Class attribute — shared fee for all savings accounts.",
                    17: "Override withdraw to add fee logic.",
                    18: "Delegate to parent with fee added; parent handles the balance check.",
                    21: "100 + 2 fee = 102 deducted; 500 - 102 = 398.",
                },
            ),
            CodeExample(
                title="Checking the MRO",
                code=(
                    "class BankAccount:\n"
                    "    pass\n"
                    "\n"
                    "class SavingsAccount(BankAccount):\n"
                    "    pass\n"
                    "\n"
                    "print(SavingsAccount.__mro__)"
                ),
                explanation="__mro__ shows the order Python searches for methods.",
                output="(<class 'SavingsAccount'>, <class 'BankAccount'>, <class 'object'>)",
                line_notes={
                    7: "MRO: SavingsAccount → BankAccount → object (every class inherits from object).",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting `super().__init__()` in the subclass — parent attributes are never created.",
            "Calling `super()` with two arguments in Python 3 — use the no-argument form `super()`.",
            "Using inheritance for has-a relationships — prefer composition when the subclass only uses the parent, not is the parent.",
            "Overriding a method without calling super() when you intended to extend (not replace) the parent's logic.",
        ],
        practice_prompts=[
            "Create a CheckingAccount subclass that inherits from BankAccount and overrides withdraw to allow a small overdraft (e.g., -$100).",
            "Print `SavingsAccount.__mro__` and explain what each class in the chain provides.",
            "Write a Premium SavingsAccount that inherits from SavingsAccount but has no fee.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does `super().withdraw(amount)` do inside SavingsAccount?",
                qtype="multiple_choice",
                correct_answer="Calls BankAccount.withdraw on the current instance",
                options=[
                    "Calls BankAccount.withdraw on the current instance",
                    "Creates a new BankAccount and calls withdraw on it",
                    "Skips the withdraw call entirely",
                    "Calls object.withdraw",
                ],
                explanation="`super()` in SavingsAccount delegates to BankAccount (the next in MRO), passing `self` automatically.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="`isinstance(savings_obj, BankAccount)` returns False because SavingsAccount is a different class.",
                qtype="true_false",
                correct_answer="false",
                explanation="`isinstance` returns True for instances of the class AND any of its subclasses.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is the Python 3 syntax for calling super without arguments?",
                qtype="fill_blank",
                correct_answer="super()",
                explanation="In Python 3, `super()` with no arguments automatically captures the enclosing class and instance.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="When should you prefer composition over inheritance?",
                qtype="multiple_choice",
                correct_answer="When the relationship is has-a rather than is-a",
                options=[
                    "When the relationship is has-a rather than is-a",
                    "When performance is critical",
                    "When you need more than two methods",
                    "When the parent class is abstract",
                ],
                explanation="Inheritance models 'is-a'; composition models 'has-a'. Using inheritance for has-a creates tight coupling.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i17-ex",
            title="SavingsAccount with Fee",
            instructions=(
                "Build on the BankAccount class to create SavingsAccount.\n"
                "SavingsAccount should:\n"
                "  - inherit from BankAccount\n"
                "  - have a class attribute FEE = 1.50\n"
                "  - override withdraw(amount) to add FEE to the amount before calling super().withdraw\n\n"
                "  s = SavingsAccount('Eve', 300)\n"
                "  s.withdraw(50)\n"
                "  print(s._balance)  # 248.5  (300 - 50 - 1.50)"
            ),
            starter_code=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        if amount > self._balance:\n"
                "            raise ValueError('Insufficient funds')\n"
                "        self._balance -= amount\n"
                "\n"
                "class SavingsAccount(BankAccount):\n"
                "    FEE = 1.50\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        pass  # call super with amount + FEE\n"
                "\n"
                "s = SavingsAccount('Eve', 300)\n"
                "s.withdraw(50)\n"
                "print(s._balance)"
            ),
            expected_output="248.5",
            hints=[
                "Call `super().withdraw(amount + self.FEE)`",
                "The parent's withdraw handles balance validation and deduction.",
            ],
            solution=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        if amount > self._balance:\n"
                "            raise ValueError('Insufficient funds')\n"
                "        self._balance -= amount\n"
                "\n"
                "class SavingsAccount(BankAccount):\n"
                "    FEE = 1.50\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        super().withdraw(amount + self.FEE)\n"
                "\n"
                "s = SavingsAccount('Eve', 300)\n"
                "s.withdraw(50)\n"
                "print(s._balance)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i18 — Composition
    # -------------------------------------------------------------------------
    Lesson(
        id="i18",
        title="Composition",
        level=Level.INTERMEDIATE,
        estimated_minutes=13,
        explanation=(
            "Composition means building complex objects by assembling simpler objects "
            "as attributes — the *has-a* relationship. A `Bank` *has* a list of "
            "`BankAccount` objects; a `Car` *has* an `Engine`. Compare this with "
            "inheritance, which models *is-a*: a `SavingsAccount` *is a* `BankAccount`. "
            "Many OOP authorities (notably the Gang of Four) advise 'favour composition "
            "over inheritance' because composed systems are easier to change without "
            "ripple effects.\n\n"
            "In Python, composition is just an attribute that holds another object. "
            "A `Bank` class might store `self.accounts = []` and expose `add_account`, "
            "`remove_account`, and `total_deposits` methods. The Bank doesn't inherit "
            "from BankAccount — it uses BankAccount instances. This means you can "
            "freely swap the account type without touching the Bank class.\n\n"
            "The key design question is: 'If I change the inner class, how many "
            "callers break?' With composition, the outer class is insulated by its "
            "method interface. With deep inheritance, changes propagate through the "
            "hierarchy. Composition also avoids the fragile-base-class problem, where "
            "a change to the parent silently breaks a subclass.\n\n"
            "A practical rule of thumb: start with composition, add inheritance only "
            "when the subtype relationship is genuinely obvious and stable. Mixed "
            "approaches work well — a SavingsAccount can inherit from BankAccount "
            "(is-a) while Bank holds accounts by composition (has-a)."
        ),
        key_terms={
            "composition": "Building objects by including other objects as attributes (has-a).",
            "has-a": "A relationship where one class contains or uses instances of another.",
            "is-a": "A relationship where one class is a specialisation of another (inheritance).",
            "delegation": "The composed object calling methods on its inner objects to get work done.",
            "coupling": "How tightly two classes depend on each other; loose coupling is preferred.",
        },
        code_examples=[
            CodeExample(
                title="Bank has-a list of BankAccounts",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "class Bank:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n"
                    "        self.accounts = []\n"
                    "\n"
                    "    def add_account(self, account):\n"
                    "        self.accounts.append(account)\n"
                    "\n"
                    "    def total_deposits(self):\n"
                    "        return sum(a._balance for a in self.accounts)\n"
                    "\n"
                    "bank = Bank('PyBank')\n"
                    "bank.add_account(BankAccount('Alice', 500))\n"
                    "bank.add_account(BankAccount('Bob', 300))\n"
                    "print(bank.total_deposits())"
                ),
                explanation="Bank uses BankAccount objects but does not inherit from them.",
                output="800.0",
                line_notes={
                    6: "Bank does NOT inherit from BankAccount — pure composition.",
                    9: "The list of accounts is created fresh for each Bank instance.",
                    11: "Delegate storage to the accounts list.",
                    14: "Iterate over composed accounts — Bank calls methods on them.",
                    20: "500 + 300 = 800.",
                },
            ),
            CodeExample(
                title="Composition vs inheritance decision",
                code=(
                    "# Has-a: use composition\n"
                    "class Address:\n"
                    "    def __init__(self, city, country):\n"
                    "        self.city = city\n"
                    "        self.country = country\n"
                    "\n"
                    "class Person:\n"
                    "    def __init__(self, name, city, country):\n"
                    "        self.name = name\n"
                    "        self.address = Address(city, country)  # has-a\n"
                    "\n"
                    "p = Person('Alice', 'London', 'UK')\n"
                    "print(p.address.city)"
                ),
                explanation="Person has an Address (composition), not is an Address (which would be wrong).",
                output="London",
                line_notes={
                    10: "Embed an Address instance — composition: Person has-a Address.",
                    13: "Access the composed object's attributes via chained dot notation.",
                },
            ),
        ],
        common_mistakes=[
            "Using inheritance when composition is more appropriate — check whether is-a or has-a better describes the relationship.",
            "Exposing the inner composed object directly, creating tight coupling — prefer methods on the outer class that delegate.",
            "Forgetting to initialise the composed list/object in __init__ — it won't exist for the first method call.",
            "Mutating a shared composed object across instances — ensure each instance gets its own copy if they should be independent.",
        ],
        practice_prompts=[
            "Add a `find_account(owner)` method to Bank that returns the matching BankAccount or None.",
            "Add a `richest_account()` method to Bank that returns the account with the highest balance.",
            "Model a Library class that has-a list of Book objects with methods to add, remove, and search by title.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="A Bank holds a list of BankAccount objects. This relationship is called:",
                qtype="multiple_choice",
                correct_answer="composition (has-a)",
                options=["composition (has-a)", "inheritance (is-a)", "polymorphism", "encapsulation"],
                explanation="Bank does not inherit from BankAccount; it contains BankAccount instances — that is composition.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="'Favour composition over inheritance' means you should never use inheritance.",
                qtype="true_false",
                correct_answer="false",
                explanation="The advice means to default to composition and reach for inheritance only when the is-a relationship is clear and stable.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is delegation in the context of composition?",
                qtype="multiple_choice",
                correct_answer="The outer class calling methods on its inner composed objects",
                options=[
                    "The outer class calling methods on its inner composed objects",
                    "A subclass calling super() to use parent methods",
                    "Passing a function as an argument",
                    "Inheriting all methods without overriding",
                ],
                explanation="Delegation means the outer class forwards work to its composed inner objects rather than doing everything itself.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What is the main advantage of composition over deep inheritance hierarchies?",
                qtype="short_answer",
                correct_answer="Composition creates looser coupling — you can change the inner class without breaking the outer class, avoiding the fragile-base-class problem.",
                keywords=["coupling", "change", "fragile", "independent", "flexible"],
                explanation="Composed objects communicate through method interfaces, so internal changes stay hidden.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i18-ex",
            title="Bank with Composed Accounts",
            instructions=(
                "Complete the Bank class so it:\n"
                "  - stores accounts in self.accounts (list)\n"
                "  - has add_account(account) method\n"
                "  - has total_deposits() method\n"
                "  - has richest_owner() method returning the owner name with the highest balance\n\n"
                "  bank = Bank('PyBank')\n"
                "  bank.add_account(BankAccount('Alice', 500))\n"
                "  bank.add_account(BankAccount('Bob', 900))\n"
                "  print(bank.total_deposits())   # 1400.0\n"
                "  print(bank.richest_owner())    # Bob"
            ),
            starter_code=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "class Bank:\n"
                "    def __init__(self, name):\n"
                "        self.name = name\n"
                "        self.accounts = []\n"
                "\n"
                "    def add_account(self, account):\n"
                "        pass\n"
                "\n"
                "    def total_deposits(self):\n"
                "        pass\n"
                "\n"
                "    def richest_owner(self):\n"
                "        pass\n"
                "\n"
                "bank = Bank('PyBank')\n"
                "bank.add_account(BankAccount('Alice', 500))\n"
                "bank.add_account(BankAccount('Bob', 900))\n"
                "print(bank.total_deposits())\n"
                "print(bank.richest_owner())"
            ),
            expected_output="1400.0\nBob",
            hints=[
                "add_account: `self.accounts.append(account)`",
                "total_deposits: `sum(a._balance for a in self.accounts)`",
                "richest_owner: `max(self.accounts, key=lambda a: a._balance).owner`",
            ],
            solution=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "class Bank:\n"
                "    def __init__(self, name):\n"
                "        self.name = name\n"
                "        self.accounts = []\n"
                "\n"
                "    def add_account(self, account):\n"
                "        self.accounts.append(account)\n"
                "\n"
                "    def total_deposits(self):\n"
                "        return sum(a._balance for a in self.accounts)\n"
                "\n"
                "    def richest_owner(self):\n"
                "        return max(self.accounts, key=lambda a: a._balance).owner\n"
                "\n"
                "bank = Bank('PyBank')\n"
                "bank.add_account(BankAccount('Alice', 500))\n"
                "bank.add_account(BankAccount('Bob', 900))\n"
                "print(bank.total_deposits())\n"
                "print(bank.richest_owner())"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i19 — Dunder (Magic) Methods
    # -------------------------------------------------------------------------
    Lesson(
        id="i19",
        title="Dunder (Magic) Methods",
        level=Level.INTERMEDIATE,
        estimated_minutes=15,
        explanation=(
            "Dunder methods — named for their double-underscore prefix and suffix "
            "(e.g. `__str__`) — are the hooks Python uses to integrate your class with "
            "built-in syntax and functions. Implementing them lets instances behave "
            "naturally with `print()`, `len()`, `==`, `+`, `<`, iteration, context "
            "managers, and more. The Python data model is built entirely on dunders.\n\n"
            "`__str__` is called by `str(obj)` and `print(obj)`; it should return a "
            "human-friendly string. `__repr__` is called by `repr(obj)` and by the "
            "interactive REPL; it should be unambiguous, ideally returning a string "
            "that could recreate the object. If only one is defined, `__str__` falls "
            "back to `__repr__` when needed.\n\n"
            "`__len__` lets `len(obj)` work. `__eq__` defines `==`; by default, "
            "two objects are equal only if they are the same object in memory. Once "
            "you define `__eq__`, Python automatically makes the class unhashable (sets "
            "and dict keys stop working) unless you also define `__hash__`. "
            "`__lt__`, `__le__`, `__gt__`, `__ge__` enable comparisons and sorting; "
            "the `@functools.total_ordering` decorator can generate the missing "
            "comparison methods from just `__eq__` and one of the ordering methods.\n\n"
            "`__add__` defines `a + b`; similarly `__sub__`, `__mul__`, etc. define "
            "arithmetic. Returning `NotImplemented` (not raising) tells Python to try "
            "the reflected operation on the other operand."
        ),
        key_terms={
            "__str__": "Called by str() and print(); returns a human-readable string.",
            "__repr__": "Called by repr(); returns an unambiguous developer representation.",
            "__eq__": "Defines the == operator between two objects.",
            "__len__": "Enables len(obj); must return a non-negative integer.",
            "__add__": "Defines obj + other; return NotImplemented if the operation is unsupported.",
            "__hash__": "Required for objects to be used in sets/dicts; auto-disabled when __eq__ is defined.",
        },
        code_examples=[
            CodeExample(
                title="__str__, __repr__, __eq__ on BankAccount",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def __str__(self):\n"
                    "        return f'{self.owner}: ${self._balance:.2f}'\n"
                    "\n"
                    "    def __repr__(self):\n"
                    "        return f'BankAccount({self.owner!r}, {self._balance})'\n"
                    "\n"
                    "    def __eq__(self, other):\n"
                    "        if not isinstance(other, BankAccount):\n"
                    "            return NotImplemented\n"
                    "        return self.owner == other.owner\n"
                    "\n"
                    "a = BankAccount('Alice', 250)\n"
                    "print(str(a))\n"
                    "print(repr(a))\n"
                    "print(a == BankAccount('Alice', 999))"
                ),
                explanation="__str__ is for humans; __repr__ is for developers; __eq__ compares by owner name.",
                output="Alice: $250.00\nBankAccount('Alice', 250.0)\nTrue",
                line_notes={
                    6: "__str__: human-readable format with 2 decimal places.",
                    9: "__repr__: developer format using !r to quote the owner string.",
                    12: "__eq__: return NotImplemented for unknown types so Python can try the other operand.",
                    15: "Two accounts are equal if they have the same owner.",
                    20: "True because both have owner 'Alice', even though balances differ.",
                },
            ),
            CodeExample(
                title="__add__ to merge two accounts",
                code=(
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self.owner = owner\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def __add__(self, other):\n"
                    "        combined = self._balance + other._balance\n"
                    "        return BankAccount(self.owner, combined)\n"
                    "\n"
                    "a = BankAccount('Alice', 200)\n"
                    "b = BankAccount('Alice', 300)\n"
                    "merged = a + b\n"
                    "print(merged._balance)"
                ),
                explanation="a + b creates a new account with the combined balance.",
                output="500.0",
                line_notes={
                    6: "__add__ is called when + is used between two BankAccounts.",
                    7: "Sum the two balances.",
                    8: "Return a new BankAccount — don't mutate either operand.",
                    12: "`a + b` invokes `a.__add__(b)`.",
                },
            ),
        ],
        common_mistakes=[
            "Defining __eq__ but forgetting __hash__ — the object becomes unhashable and can't be stored in sets or used as dict keys.",
            "Returning a string from __len__ — it must return a non-negative integer.",
            "Raising TypeError instead of returning NotImplemented in __add__ — NotImplemented lets Python try the reflected method.",
            "Confusing __str__ and __repr__ — __str__ is for end-users; __repr__ is for developers and debugging.",
        ],
        practice_prompts=[
            "Add __lt__ to BankAccount so accounts can be sorted by balance with sorted().",
            "Add __len__ to Bank (from i18) returning the number of accounts.",
            "Implement __repr__ such that eval(repr(account)) recreates an equivalent BankAccount.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which dunder method is called by `print(obj)`?",
                qtype="multiple_choice",
                correct_answer="__str__",
                options=["__repr__", "__str__", "__print__", "__format__"],
                explanation="`print()` calls `str(obj)`, which in turn calls `obj.__str__()`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Defining __eq__ automatically disables __hash__, making the object unusable as a dict key.",
                qtype="true_false",
                correct_answer="true",
                explanation="Python sets __hash__ to None when __eq__ is defined, because mutable-equality objects shouldn't be hashable by default.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What should __add__ return when it doesn't know how to add the other operand?",
                qtype="fill_blank",
                correct_answer="NotImplemented",
                explanation="Returning NotImplemented (not raising) tells Python to try the reflected operation `other.__radd__(self)`.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which decorator generates missing comparison methods from __eq__ and one ordering method?",
                qtype="multiple_choice",
                correct_answer="@functools.total_ordering",
                options=[
                    "@functools.total_ordering",
                    "@functools.compare",
                    "@classmethod",
                    "@dataclass(order=True)",
                ],
                explanation="`@functools.total_ordering` fills in the missing __lt__, __le__, __gt__, __ge__ from the ones you provide.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i19-ex",
            title="Full BankAccount Dunder Suite",
            instructions=(
                "Add __str__, __repr__, and __eq__ to BankAccount.\n"
                "  __str__: 'Alice: $500.00'\n"
                "  __repr__: \"BankAccount('Alice', 500.0)\"\n"
                "  __eq__: True if both owner and balance match\n\n"
                "  a = BankAccount('Alice', 500)\n"
                "  print(str(a))\n"
                "  print(repr(a))\n"
                "  print(a == BankAccount('Alice', 500))\n"
                "  print(a == BankAccount('Alice', 999))"
            ),
            starter_code=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def __str__(self):\n"
                "        pass\n"
                "\n"
                "    def __repr__(self):\n"
                "        pass\n"
                "\n"
                "    def __eq__(self, other):\n"
                "        pass\n"
                "\n"
                "a = BankAccount('Alice', 500)\n"
                "print(str(a))\n"
                "print(repr(a))\n"
                "print(a == BankAccount('Alice', 500))\n"
                "print(a == BankAccount('Alice', 999))"
            ),
            expected_output="Alice: $500.00\nBankAccount('Alice', 500.0)\nTrue\nFalse",
            hints=[
                "__str__: f'{self.owner}: ${self._balance:.2f}'",
                "__repr__: f\"BankAccount({self.owner!r}, {self._balance})\"",
                "__eq__: check owner AND _balance both match.",
            ],
            solution=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def __str__(self):\n"
                "        return f'{self.owner}: ${self._balance:.2f}'\n"
                "\n"
                "    def __repr__(self):\n"
                "        return f'BankAccount({self.owner!r}, {self._balance})'\n"
                "\n"
                "    def __eq__(self, other):\n"
                "        if not isinstance(other, BankAccount):\n"
                "            return NotImplemented\n"
                "        return self.owner == other.owner and self._balance == other._balance\n"
                "\n"
                "a = BankAccount('Alice', 500)\n"
                "print(str(a))\n"
                "print(repr(a))\n"
                "print(a == BankAccount('Alice', 500))\n"
                "print(a == BankAccount('Alice', 999))"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i20 — Type Hints
    # -------------------------------------------------------------------------
    Lesson(
        id="i20",
        title="Type Hints",
        level=Level.INTERMEDIATE,
        estimated_minutes=12,
        explanation=(
            "Type hints (PEP 484, Python 3.5+) let you annotate variables, function "
            "parameters, and return values with their expected types. Python itself "
            "ignores them at runtime — they are documentation that tools like mypy, "
            "pyright, and IDEs use to catch type errors before you run your code. "
            "Even without a type checker, hints make code dramatically easier to read "
            "and understand.\n\n"
            "Basic annotations use built-in types directly: `name: str`, `count: int`, "
            "`price: float`, `active: bool`. For collections, Python 3.9+ lets you "
            "write `list[str]`, `dict[str, int]`, `tuple[int, ...]` directly. For "
            "older code you import these from `typing`: `List[str]`, `Dict[str, int]`. "
            "The `from __future__ import annotations` import makes all annotations "
            "lazy strings, which avoids forward-reference errors and is recommended "
            "for new code.\n\n"
            "`Optional[X]` (equivalent to `X | None`) marks a value that may be None. "
            "`Union[X, Y]` (or `X | Y` in Python 3.10+) allows multiple types. "
            "`Any` opts out of type checking for that value. For function return types, "
            "`-> None` is explicit; omitting the annotation is ambiguous and some "
            "checkers flag it. For callables, use `Callable[[ArgType], ReturnType]`.\n\n"
            "Type hints do not slow down your program — at runtime `__annotations__` "
            "is just a dictionary and the type objects themselves are never evaluated "
            "unless you call `typing.get_type_hints()`."
        ),
        key_terms={
            "type hint": "An annotation that documents the expected type of a variable or parameter.",
            "Optional[X]": "Shorthand for `X | None`; the value may be X or None.",
            "Union[X, Y]": "A value that may be type X or type Y.",
            "list[T]": "A list whose elements are all of type T (Python 3.9+ native syntax).",
            "-> ReturnType": "Annotates the return type of a function.",
            "mypy": "The most popular static type checker for Python.",
        },
        code_examples=[
            CodeExample(
                title="Annotating a function",
                code=(
                    "from __future__ import annotations\n"
                    "\n"
                    "def greet(name: str, times: int = 1) -> str:\n"
                    "    return (f'Hello, {name}! ' * times).strip()\n"
                    "\n"
                    "def add_numbers(a: int | float, b: int | float) -> float:\n"
                    "    return float(a + b)\n"
                    "\n"
                    "print(greet('Alice', 2))\n"
                    "print(add_numbers(3, 4.5))"
                ),
                explanation="Annotate parameters and return types for documentation and static analysis.",
                output="Hello, Alice! Hello, Alice!\n7.5",
                line_notes={
                    1: "`from __future__ import annotations` makes all hints lazy strings (recommended).",
                    3: "name is str, times defaults to int 1, returns str.",
                    6: "Union using `|` syntax (Python 3.10+); accepts int or float for both args.",
                    9: "Runtime behaviour is unchanged — hints are documentation only.",
                },
            ),
            CodeExample(
                title="Annotating a class",
                code=(
                    "from __future__ import annotations\n"
                    "from typing import Optional\n"
                    "\n"
                    "class BankAccount:\n"
                    "    bank_name: str = 'PyBank'\n"
                    "\n"
                    "    def __init__(self, owner: str, balance: float = 0.0) -> None:\n"
                    "        self.owner: str = owner\n"
                    "        self._balance: float = balance\n"
                    "\n"
                    "    def deposit(self, amount: float) -> None:\n"
                    "        self._balance += amount\n"
                    "\n"
                    "    def find_owner(self, name: str) -> Optional[str]:\n"
                    "        return self.owner if self.owner == name else None\n"
                    "\n"
                    "a = BankAccount('Alice', 100.0)\n"
                    "print(a.find_owner('Bob'))"
                ),
                explanation="Annotate class attributes, __init__ params, and method signatures.",
                output="None",
                line_notes={
                    5: "Class-level attribute annotation with default value.",
                    7: "__init__ returns None (it's always None).",
                    14: "Optional[str] means this method returns str or None.",
                },
            ),
        ],
        common_mistakes=[
            "Using `list` without subscript in Python 3.8 — write `List[str]` from `typing` or upgrade to 3.9+.",
            "Confusing `Optional[str]` with `Union[str, None]` — they are identical; `Optional` is shorthand.",
            "Thinking type hints are enforced at runtime — Python ignores them; use mypy/pyright for enforcement.",
            "Annotating `-> None` is unnecessary only in __init__; for all other methods the annotation adds clarity.",
        ],
        practice_prompts=[
            "Add type hints to all BankAccount methods from the previous lessons.",
            "Write a function `find_max(values: list[int]) -> Optional[int]` that returns None for an empty list.",
            "Annotate a function that takes a Union[str, int] parameter and returns str.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Type hints are checked and enforced by Python at runtime.",
                qtype="true_false",
                correct_answer="false",
                explanation="Python ignores type hints at runtime. External tools like mypy perform static type checking.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What does `Optional[str]` mean?",
                qtype="multiple_choice",
                correct_answer="The value is either a str or None",
                options=[
                    "The value is either a str or None",
                    "The annotation is optional and can be omitted",
                    "The function parameter is keyword-only",
                    "The value is a string with optional length",
                ],
                explanation="`Optional[X]` is shorthand for `Union[X, None]`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In Python 3.10+, what is the shorthand for Union[int, str]?",
                qtype="fill_blank",
                correct_answer="int | str",
                explanation="The `|` syntax for unions was introduced in Python 3.10, replacing `Union[int, str]`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What import makes type hints lazy strings, avoiding forward-reference errors?",
                qtype="fill_blank",
                correct_answer="from __future__ import annotations",
                explanation="This postpones evaluation of all annotations, so you can reference classes before they are defined.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i20-ex",
            title="Typed BankAccount",
            instructions=(
                "Add type hints to the BankAccount class:\n"
                "  - Class attribute bank_name: str\n"
                "  - __init__(self, owner: str, balance: float = 0.0) -> None\n"
                "  - deposit(self, amount: float) -> None\n"
                "  - get_summary(self) -> str (returns 'owner: X, balance: Y')\n\n"
                "  a = BankAccount('Alice', 500.0)\n"
                "  a.deposit(100.0)\n"
                "  print(a.get_summary())"
            ),
            starter_code=(
                "from __future__ import annotations\n"
                "\n"
                "class BankAccount:\n"
                "    bank_name: str = 'PyBank'\n"
                "\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        self._balance += amount\n"
                "\n"
                "    def get_summary(self):\n"
                "        return f'owner: {self.owner}, balance: {self._balance}'\n"
                "\n"
                "a = BankAccount('Alice', 500.0)\n"
                "a.deposit(100.0)\n"
                "print(a.get_summary())"
            ),
            expected_output="owner: Alice, balance: 600.0",
            hints=[
                "Add `: str` after each str param, `: float` after each float param.",
                "Add `-> None` to __init__ and deposit.",
                "Add `-> str` to get_summary.",
            ],
            solution=(
                "from __future__ import annotations\n"
                "\n"
                "class BankAccount:\n"
                "    bank_name: str = 'PyBank'\n"
                "\n"
                "    def __init__(self, owner: str, balance: float = 0.0) -> None:\n"
                "        self.owner: str = owner\n"
                "        self._balance: float = float(balance)\n"
                "\n"
                "    def deposit(self, amount: float) -> None:\n"
                "        self._balance += amount\n"
                "\n"
                "    def get_summary(self) -> str:\n"
                "        return f'owner: {self.owner}, balance: {self._balance}'\n"
                "\n"
                "a = BankAccount('Alice', 500.0)\n"
                "a.deposit(100.0)\n"
                "print(a.get_summary())"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i21 — Dataclasses
    # -------------------------------------------------------------------------
    Lesson(
        id="i21",
        title="Dataclasses",
        level=Level.INTERMEDIATE,
        estimated_minutes=13,
        explanation=(
            "The `@dataclass` decorator (Python 3.7+, `from dataclasses import dataclass`) "
            "automatically generates `__init__`, `__repr__`, and `__eq__` from the class's "
            "field annotations. A class that would take 30 lines of boilerplate collapses "
            "to 5 annotated attributes. Dataclasses are ideal for any object whose primary "
            "purpose is to carry structured data — DTOs, configuration objects, records.\n\n"
            "By default, a dataclass is mutable. Pass `frozen=True` to make it immutable "
            "(and hashable): `@dataclass(frozen=True)`. Pass `order=True` to auto-generate "
            "`__lt__`, `__le__`, `__gt__`, `__ge__` based on field order, enabling "
            "direct use with `sorted()`. The `eq=True` default generates `__eq__`; "
            "combining `eq=True` and `frozen=True` also generates `__hash__`.\n\n"
            "For fields with complex defaults, use `field()` from `dataclasses`. Never "
            "write `items: list = []` — this raises `ValueError` because dataclass "
            "detects the mutable default. Instead, use `field(default_factory=list)`. "
            "The `__post_init__` method, if defined, runs right after the generated "
            "`__init__`, letting you validate or compute derived attributes.\n\n"
            "Dataclasses work naturally with type hints and compose well with inheritance. "
            "A subclass dataclass inherits parent fields; its own fields come after the "
            "parent's in the generated `__init__`. Be careful: if a parent field has a "
            "default, all child fields must also have defaults."
        ),
        key_terms={
            "@dataclass": "Decorator that auto-generates __init__, __repr__, and __eq__ from field annotations.",
            "field()": "Helper for configuring a dataclass field, especially with default_factory.",
            "default_factory": "A callable passed to field() that produces a new default value per instance.",
            "__post_init__": "Hook method called at the end of the generated __init__ for validation/derived fields.",
            "frozen=True": "Makes the dataclass immutable and hashable.",
            "order=True": "Auto-generates comparison methods so instances can be sorted.",
        },
        code_examples=[
            CodeExample(
                title="Basic dataclass",
                code=(
                    "from dataclasses import dataclass\n"
                    "\n"
                    "@dataclass\n"
                    "class Point:\n"
                    "    x: float\n"
                    "    y: float\n"
                    "\n"
                    "p1 = Point(1.0, 2.0)\n"
                    "p2 = Point(1.0, 2.0)\n"
                    "print(p1)\n"
                    "print(p1 == p2)"
                ),
                explanation="@dataclass generates __init__, __repr__, and __eq__ automatically.",
                output="Point(x=1.0, y=2.0)\nTrue",
                line_notes={
                    3: "@dataclass triggers code generation — no manual __init__ needed.",
                    5: "Annotated fields become __init__ parameters in order.",
                    10: "__repr__ is auto-generated: Point(x=1.0, y=2.0).",
                    11: "__eq__ compares all fields: both x and y match, so True.",
                },
            ),
            CodeExample(
                title="field() and __post_init__",
                code=(
                    "from dataclasses import dataclass, field\n"
                    "\n"
                    "@dataclass\n"
                    "class BankAccount:\n"
                    "    owner: str\n"
                    "    balance: float = 0.0\n"
                    "    transactions: list = field(default_factory=list)\n"
                    "\n"
                    "    def __post_init__(self):\n"
                    "        if self.balance < 0:\n"
                    "            raise ValueError('Balance cannot be negative')\n"
                    "\n"
                    "a = BankAccount('Alice', 500)\n"
                    "print(a)\n"
                    "print(a.transactions)"
                ),
                explanation="field(default_factory=list) creates a fresh list per instance; __post_init__ validates.",
                output="BankAccount(owner='Alice', balance=500, transactions=[])\n[]",
                line_notes={
                    7: "default_factory=list creates a NEW list for each instance — no shared mutable default.",
                    9: "__post_init__ runs after __init__; use it for validation.",
                    10: "Raise if balance is negative — catches bad input at construction time.",
                    14: "The generated __repr__ includes all fields.",
                },
            ),
        ],
        common_mistakes=[
            "Writing `items: list = []` in a dataclass — raises ValueError; use `field(default_factory=list)`.",
            "Expecting `frozen=True` to deep-freeze nested mutable objects — it only prevents attribute reassignment.",
            "Defining __init__ manually in a dataclass — the decorator overwrites it unless you pass `init=False`.",
            "Mixing fields with and without defaults in the wrong order — fields with defaults must come after those without.",
        ],
        practice_prompts=[
            "Create a frozen, ordered dataclass `Product` with name, price, and stock fields.",
            "Add a __post_init__ that validates price > 0.",
            "Create a dataclass `Order` that has a field `items: list[str]` using default_factory.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which argument to @dataclass makes instances immutable?",
                qtype="fill_blank",
                correct_answer="frozen=True",
                explanation="`@dataclass(frozen=True)` prevents attribute assignment after creation and generates __hash__.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Why should you use `field(default_factory=list)` instead of `items: list = []`?",
                qtype="multiple_choice",
                correct_answer="To create a fresh list for each instance instead of sharing one list",
                options=[
                    "To create a fresh list for each instance instead of sharing one list",
                    "Because list is not a valid type annotation",
                    "To make the field read-only",
                    "Because @dataclass requires field() for all defaults",
                ],
                explanation="Mutable defaults like `[]` are shared; `default_factory=list` calls `list()` for each new instance.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which method runs after the generated __init__ for validation?",
                qtype="fill_blank",
                correct_answer="__post_init__",
                explanation="`__post_init__` is called at the end of the auto-generated `__init__`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A dataclass with @dataclass(order=True) can be used directly with sorted().",
                qtype="true_false",
                correct_answer="true",
                explanation="`order=True` generates __lt__, __le__, __gt__, __ge__ based on field order, enabling sorting.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="i21-ex",
            title="Product Dataclass",
            instructions=(
                "Create a @dataclass Product with:\n"
                "  name: str\n"
                "  price: float\n"
                "  tags: list (empty list by default, use field)\n\n"
                "Add __post_init__ that raises ValueError if price <= 0.\n\n"
                "  p = Product('Widget', 9.99, tags=['sale', 'new'])\n"
                "  print(p)\n"
                "  print(p.tags)"
            ),
            starter_code=(
                "from dataclasses import dataclass, field\n"
                "\n"
                "@dataclass\n"
                "class Product:\n"
                "    name: str\n"
                "    price: float\n"
                "    tags: list = field(default_factory=list)\n"
                "\n"
                "    def __post_init__(self):\n"
                "        pass  # validate price\n"
                "\n"
                "p = Product('Widget', 9.99, tags=['sale', 'new'])\n"
                "print(p)\n"
                "print(p.tags)"
            ),
            expected_output="Product(name='Widget', price=9.99, tags=['sale', 'new'])\n['sale', 'new']",
            hints=[
                "In __post_init__: `if self.price <= 0: raise ValueError('Price must be positive')`",
                "The generated __repr__ prints all fields automatically.",
            ],
            solution=(
                "from dataclasses import dataclass, field\n"
                "\n"
                "@dataclass\n"
                "class Product:\n"
                "    name: str\n"
                "    price: float\n"
                "    tags: list = field(default_factory=list)\n"
                "\n"
                "    def __post_init__(self):\n"
                "        if self.price <= 0:\n"
                "            raise ValueError('Price must be positive')\n"
                "\n"
                "p = Product('Widget', 9.99, tags=['sale', 'new'])\n"
                "print(p)\n"
                "print(p.tags)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i22 — Debugging
    # -------------------------------------------------------------------------
    Lesson(
        id="i22",
        title="Debugging",
        level=Level.INTERMEDIATE,
        estimated_minutes=14,
        explanation=(
            "Debugging is the process of finding and fixing incorrect behaviour in your "
            "program. Every programmer spends a significant portion of their time "
            "debugging, so developing good debugging instincts is as important as "
            "writing code in the first place.\n\n"
            "The simplest technique is *print debugging*: inserting `print()` statements "
            "at key points to inspect variable values and confirm control flow. It is "
            "immediately available, requires no setup, and works everywhere. The main "
            "drawback is that you have to remember to remove the prints before shipping. "
            "A slightly more robust alternative is `logging` (covered in i23), which "
            "lets you leave debug statements in the code and control verbosity via "
            "configuration.\n\n"
            "Python ships with `pdb` — the Python Debugger. The easiest way to drop into "
            "it is `breakpoint()` (Python 3.7+), which pauses execution and opens an "
            "interactive prompt. From there you can step line by line (`n`), step into "
            "functions (`s`), continue to the next breakpoint (`c`), inspect variables "
            "by typing their name, and quit with `q`. IDEs like VS Code and PyCharm wrap "
            "pdb in a graphical interface — set a breakpoint by clicking the gutter.\n\n"
            "Common runtime errors to recognise: `NameError` — a variable name doesn't "
            "exist; `TypeError` — wrong type passed to an operation or function; "
            "`AttributeError` — accessing an attribute or method that doesn't exist on "
            "an object; `IndexError` — list index out of range; `KeyError` — dict key "
            "not found; `ValueError` — right type but wrong value. Reading the full "
            "traceback from top to bottom — especially the *last* line, which gives "
            "the error type and message — is the first step in any debugging session."
        ),
        key_terms={
            "breakpoint()": "Pauses execution and opens the pdb interactive debugger (Python 3.7+).",
            "pdb": "Python Debugger — the built-in interactive step-through debugger.",
            "traceback": "The stack of function calls shown when an exception is raised.",
            "NameError": "Raised when a variable or function name is not defined.",
            "AttributeError": "Raised when an attribute or method does not exist on an object.",
            "TypeError": "Raised when an operation is applied to an object of the wrong type.",
        },
        code_examples=[
            CodeExample(
                title="Print debugging",
                code=(
                    "def compute_average(numbers):\n"
                    "    print(f'DEBUG: numbers={numbers}')\n"
                    "    total = sum(numbers)\n"
                    "    print(f'DEBUG: total={total}, count={len(numbers)}')\n"
                    "    return total / len(numbers)\n"
                    "\n"
                    "result = compute_average([10, 20, 30])\n"
                    "print(result)"
                ),
                explanation="Strategic print statements reveal intermediate values to trace the computation.",
                output="DEBUG: numbers=[10, 20, 30]\nDEBUG: total=60, count=3\n20.0",
                line_notes={
                    2: "Print the input immediately to confirm it arrived correctly.",
                    4: "Print intermediate values before the final computation.",
                    5: "The actual logic — now we can see exactly what goes into it.",
                },
            ),
            CodeExample(
                title="Common error messages",
                code=(
                    "# NameError\n"
                    "try:\n"
                    "    print(undefined_var)\n"
                    "except NameError as e:\n"
                    "    print(f'NameError: {e}')\n"
                    "\n"
                    "# AttributeError\n"
                    "try:\n"
                    "    x = 42\n"
                    "    x.append(1)\n"
                    "except AttributeError as e:\n"
                    "    print(f'AttributeError: {e}')\n"
                    "\n"
                    "# KeyError\n"
                    "try:\n"
                    "    d = {'a': 1}\n"
                    "    print(d['b'])\n"
                    "except KeyError as e:\n"
                    "    print(f'KeyError: {e}')"
                ),
                explanation="Recognise these three common errors and understand what each means.",
                output="NameError: name 'undefined_var' is not defined\nAttributeError: 'int' object has no attribute 'append'\nKeyError: 'b'",
                line_notes={
                    3: "NameError: 'undefined_var' was never assigned.",
                    10: "AttributeError: int has no append method — int is not a list.",
                    17: "KeyError: key 'b' does not exist in the dict.",
                },
            ),
            CodeExample(
                title="Using breakpoint()",
                code=(
                    "def find_bug(data):\n"
                    "    result = []\n"
                    "    for item in data:\n"
                    "        breakpoint()  # pause here in pdb\n"
                    "        result.append(item * 2)\n"
                    "    return result\n"
                    "\n"
                    "# In real use, remove breakpoint() before shipping\n"
                    "# pdb commands: n=next, s=step, c=continue, q=quit"
                ),
                explanation="breakpoint() drops you into pdb at line 4; type variable names to inspect them.",
                output="(pdb interactive session — remove before shipping)",
                line_notes={
                    4: "Execution pauses here; type `item` or `result` in the pdb prompt to inspect.",
                    9: "Remove all breakpoint() calls before committing code.",
                },
            ),
        ],
        common_mistakes=[
            "Reading only the last line of a traceback — the full call stack shows where the error originated.",
            "Leaving `print` or `breakpoint()` debug statements in production code.",
            "Catching all exceptions with bare `except:` — this hides bugs; catch specific exceptions.",
            "Assuming the error is on the line number reported — the traceback points to where the error *surfaced*, not always where it was *caused*.",
        ],
        practice_prompts=[
            "Add strategic print statements to debug a function that calculates compound interest and returns wrong results.",
            "Use `breakpoint()` to step through a loop and inspect a variable that becomes None unexpectedly.",
            "Given a traceback, identify the root cause and the line that caused it.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which built-in drops you into the Python debugger at runtime?",
                qtype="fill_blank",
                correct_answer="breakpoint()",
                explanation="`breakpoint()` was added in Python 3.7 as a clean replacement for `import pdb; pdb.set_trace()`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What does AttributeError mean?",
                qtype="multiple_choice",
                correct_answer="An attribute or method was accessed that does not exist on the object",
                options=[
                    "An attribute or method was accessed that does not exist on the object",
                    "A variable name was used before being assigned",
                    "A list index was out of range",
                    "A function received an argument of the wrong type",
                ],
                explanation="AttributeError: `'int' object has no attribute 'append'` — you tried to call append on an int.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="You should always use bare `except:` to catch every possible error so your program never crashes.",
                qtype="true_false",
                correct_answer="false",
                explanation="Bare `except:` catches even SystemExit and KeyboardInterrupt, masking genuine bugs. Always catch specific exception types.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In pdb, which single-letter command continues execution until the next breakpoint?",
                qtype="fill_blank",
                correct_answer="c",
                explanation="`c` (continue) resumes execution; `n` steps to the next line; `s` steps into a function call; `q` quits.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i22-ex",
            title="Debug the Broken Function",
            instructions=(
                "The function below has two bugs. Use print statements to find them.\n\n"
                "Bug 1: It crashes with an error on some inputs.\n"
                "Bug 2: Even when it doesn't crash, the result is wrong.\n\n"
                "Fix both bugs so the output is 'Average: 25.0'."
            ),
            starter_code=(
                "def average(numbers):\n"
                "    total = 0\n"
                "    for n in numbers:\n"
                "        total = total + n\n"
                "    return total / len(numbers)\n"
                "\n"
                "data = [10, 20, 30, 40]\n"
                "# Bug: data gets modified — find why average is wrong\n"
                "data.pop()  # simulated bug: removes last element\n"
                "result = average(data)\n"
                "print(f'Average: {result}')"
            ),
            expected_output="Average: 25.0",
            hints=[
                "Add `print(f'DEBUG data before average: {data}')` before calling average().",
                "The pop() call removes the last element — remove it to fix the data.",
                "With data = [10, 20, 30, 40], average should be (10+20+30+40)/4 = 25.0.",
            ],
            solution=(
                "def average(numbers):\n"
                "    total = 0\n"
                "    for n in numbers:\n"
                "        total = total + n\n"
                "    return total / len(numbers)\n"
                "\n"
                "data = [10, 20, 30, 40]\n"
                "result = average(data)  # removed data.pop() bug\n"
                "print(f'Average: {result}')"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i23 — Logging
    # -------------------------------------------------------------------------
    Lesson(
        id="i23",
        title="Logging",
        level=Level.INTERMEDIATE,
        estimated_minutes=13,
        explanation=(
            "The `logging` module is Python's built-in answer to 'I need more than "
            "print statements'. Unlike print, logged messages carry a severity level, "
            "a timestamp, the source module, and can be routed to multiple destinations "
            "(console, file, network) simultaneously — all configurable without changing "
            "application code. This makes logging production-ready where print is not.\n\n"
            "The five standard levels in ascending severity are `DEBUG`, `INFO`, "
            "`WARNING`, `ERROR`, and `CRITICAL`. The default level is `WARNING`, so "
            "DEBUG and INFO messages are suppressed unless you configure otherwise. "
            "Call `logging.basicConfig(level=logging.DEBUG)` at the start of your "
            "script to enable all levels. In production, you would typically set the "
            "level to `INFO` or `WARNING`.\n\n"
            "For anything beyond basic scripts, create a named *logger* with "
            "`logging.getLogger(__name__)`. Using `__name__` as the logger name means "
            "the module path appears in each log line, making it easy to trace where "
            "a message came from. Loggers form a hierarchy (dotted names); a child "
            "logger propagates messages to its parent unless propagation is disabled.\n\n"
            "*Handlers* define where log output goes: `StreamHandler` writes to the "
            "console, `FileHandler` writes to a file. *Formatters* control the layout "
            "of each line. A common production formatter is "
            "`'%(asctime)s %(levelname)s %(name)s: %(message)s'`. You attach handlers "
            "to loggers and set a formatter on each handler."
        ),
        key_terms={
            "logger": "A named logging channel created with logging.getLogger().",
            "handler": "Defines where log messages go (console, file, network).",
            "formatter": "Controls the layout (timestamp, level, message) of each log line.",
            "level": "Severity threshold; messages below the level are suppressed.",
            "basicConfig()": "One-call setup for simple logging to the console.",
            "propagation": "A child logger's messages bubble up to parent loggers by default.",
        },
        code_examples=[
            CodeExample(
                title="Basic logging setup",
                code=(
                    "import logging\n"
                    "\n"
                    "logging.basicConfig(\n"
                    "    level=logging.DEBUG,\n"
                    "    format='%(levelname)s: %(message)s'\n"
                    ")\n"
                    "\n"
                    "logging.debug('Starting computation')\n"
                    "logging.info('Processing 42 records')\n"
                    "logging.warning('Disk space below 10%')\n"
                    "logging.error('Failed to connect to database')"
                ),
                explanation="basicConfig configures the root logger; all four messages appear because level=DEBUG.",
                output="DEBUG: Starting computation\nINFO: Processing 42 records\nWARNING: Disk space below 10%\nERROR: Failed to connect to database",
                line_notes={
                    3: "basicConfig sets up the root logger — call once, at startup.",
                    4: "DEBUG is the lowest level; everything at DEBUG and above will be shown.",
                    5: "Custom format: just level + message for brevity.",
                    8: "DEBUG: fine-grained diagnostic info.",
                    9: "INFO: normal operational messages.",
                    10: "WARNING: something unexpected but not fatal.",
                    11: "ERROR: a serious problem that needs attention.",
                },
            ),
            CodeExample(
                title="Named logger with file handler",
                code=(
                    "import logging\n"
                    "\n"
                    "logger = logging.getLogger('bank')\n"
                    "logger.setLevel(logging.DEBUG)\n"
                    "\n"
                    "handler = logging.FileHandler('/tmp/bank.log')\n"
                    "formatter = logging.Formatter(\n"
                    "    '%(asctime)s %(levelname)s: %(message)s'\n"
                    ")\n"
                    "handler.setFormatter(formatter)\n"
                    "logger.addHandler(handler)\n"
                    "\n"
                    "logger.info('Account created for Alice')\n"
                    "logger.warning('Low balance: Alice $5.00')"
                ),
                explanation="Named logger writes to a file with timestamps.",
                output="(written to /tmp/bank.log with timestamps)",
                line_notes={
                    3: "Create a named logger — `__name__` is the convention in modules.",
                    5: "FileHandler routes output to a log file.",
                    7: "Formatter specifies the layout of each log line.",
                    10: "Attach the formatter to the handler.",
                    11: "Attach the handler to the logger.",
                    13: "Log an informational message.",
                },
            ),
        ],
        common_mistakes=[
            "Using print() in library code — libraries should use logging so applications can control verbosity.",
            "Calling basicConfig() multiple times — only the first call takes effect; later calls are ignored.",
            "Logging sensitive data (passwords, tokens) — log messages may persist in files; scrub secrets.",
            "Not using `__name__` as the logger name — hardcoded names make it hard to filter by module.",
        ],
        practice_prompts=[
            "Add logging to a BankAccount class: log INFO on deposit, WARNING when balance drops below $10.",
            "Configure a logger that writes DEBUG+ to a file and WARNING+ to the console simultaneously.",
            "Replace all print() calls in a script with equivalent logging calls at appropriate levels.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What is the default logging level (messages below this level are suppressed)?",
                qtype="multiple_choice",
                correct_answer="WARNING",
                options=["DEBUG", "INFO", "WARNING", "ERROR"],
                explanation="The root logger's default level is WARNING, so DEBUG and INFO messages are hidden unless you change it.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="logging.basicConfig() can be called multiple times to update the configuration.",
                qtype="true_false",
                correct_answer="false",
                explanation="basicConfig() has no effect if the root logger already has handlers. It should be called once at startup.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What is the conventional argument to pass to logging.getLogger() inside a module?",
                qtype="fill_blank",
                correct_answer="__name__",
                explanation="`__name__` evaluates to the module's fully-qualified name, making log lines easy to trace.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What does a Handler do in the logging system?",
                qtype="multiple_choice",
                correct_answer="Determines where log messages are sent (console, file, etc.)",
                options=[
                    "Determines where log messages are sent (console, file, etc.)",
                    "Formats the timestamp of each message",
                    "Filters messages by level",
                    "Creates a new logger instance",
                ],
                explanation="Handlers route messages to destinations; Formatters control layout; Filters restrict which messages pass.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i23-ex",
            title="Logging BankAccount Events",
            instructions=(
                "Set up a logger named 'bank' at DEBUG level.\n"
                "Add logging to a simple BankAccount class:\n"
                "  - deposit: log INFO 'Deposited X; new balance Y'\n"
                "  - withdraw: log INFO 'Withdrew X; new balance Y'\n"
                "  - withdraw when balance < 50: also log WARNING 'Low balance: Y'\n\n"
                "  a = BankAccount('Alice', 100)\n"
                "  a.deposit(50)\n"
                "  a.withdraw(130)"
            ),
            starter_code=(
                "import logging\n"
                "\n"
                "logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')\n"
                "logger = logging.getLogger('bank')\n"
                "\n"
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        self._balance += amount\n"
                "        # log INFO here\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        self._balance -= amount\n"
                "        # log INFO here\n"
                "        # log WARNING if balance < 50\n"
                "\n"
                "a = BankAccount('Alice', 100)\n"
                "a.deposit(50)\n"
                "a.withdraw(130)"
            ),
            expected_output="INFO: Deposited 50; new balance 150.0\nINFO: Withdrew 130; new balance 20.0\nWARNING: Low balance: 20.0",
            hints=[
                "After deposit: `logger.info(f'Deposited {amount}; new balance {self._balance}')`",
                "After withdraw: similar info log, then `if self._balance < 50: logger.warning(...)`",
            ],
            solution=(
                "import logging\n"
                "\n"
                "logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')\n"
                "logger = logging.getLogger('bank')\n"
                "\n"
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self.owner = owner\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        self._balance += amount\n"
                "        logger.info(f'Deposited {amount}; new balance {self._balance}')\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        self._balance -= amount\n"
                "        logger.info(f'Withdrew {amount}; new balance {self._balance}')\n"
                "        if self._balance < 50:\n"
                "            logger.warning(f'Low balance: {self._balance}')\n"
                "\n"
                "a = BankAccount('Alice', 100)\n"
                "a.deposit(50)\n"
                "a.withdraw(130)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),

    # -------------------------------------------------------------------------
    # i24 — Testing with pytest
    # -------------------------------------------------------------------------
    Lesson(
        id="i24",
        title="Testing with pytest",
        level=Level.INTERMEDIATE,
        estimated_minutes=16,
        explanation=(
            "Automated tests are executable specifications — they tell you both what "
            "your code is supposed to do and whether it actually does it. Without tests, "
            "every change risks silently breaking existing behaviour. With a good test "
            "suite, you can refactor confidently and catch regressions immediately.\n\n"
            "pytest is the most popular Python testing framework. Install it with "
            "`pip install pytest`, then run `pytest` from the project root. pytest "
            "automatically discovers any file named `test_*.py` or `*_test.py` and runs "
            "any function whose name starts with `test_`. Tests pass if they complete "
            "without raising an exception; they fail if any `assert` is False or an "
            "unexpected exception is raised. pytest's error messages are significantly "
            "more readable than the standard library's `unittest`.\n\n"
            "The core tool is the plain `assert` statement: "
            "`assert result == expected, 'optional message'`. pytest rewrites assert "
            "to show the actual vs expected values on failure. For expected exceptions, "
            "use `pytest.raises(ExceptionType)` as a context manager — the test passes "
            "only if the wrapped code raises that exception.\n\n"
            "*Fixtures* are reusable setup functions decorated with `@pytest.fixture`. "
            "A test receives a fixture by declaring it as a parameter. This avoids "
            "repeating setup code across tests. *Parametrize* (`@pytest.mark.parametrize`) "
            "runs a single test function with multiple input/output pairs, concisely "
            "covering many cases without duplicating test code."
        ),
        key_terms={
            "pytest": "A powerful, widely-used Python testing framework installed with pip.",
            "assert": "Statement that raises AssertionError if the condition is False.",
            "pytest.raises()": "Context manager that asserts a specific exception is raised.",
            "fixture": "A reusable setup function decorated with @pytest.fixture.",
            "@pytest.mark.parametrize": "Runs a test with multiple sets of inputs automatically.",
            "test discovery": "pytest's automatic search for test files and test functions.",
        },
        code_examples=[
            CodeExample(
                title="Basic test functions",
                code=(
                    "# test_bank.py\n"
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def deposit(self, amount):\n"
                    "        self._balance += amount\n"
                    "\n"
                    "def test_deposit_increases_balance():\n"
                    "    account = BankAccount('Alice', 100)\n"
                    "    account.deposit(50)\n"
                    "    assert account._balance == 150.0\n"
                    "\n"
                    "def test_initial_balance_defaults_to_zero():\n"
                    "    account = BankAccount('Bob')\n"
                    "    assert account._balance == 0.0"
                ),
                explanation="Two test functions; pytest discovers them by the test_ prefix and runs both.",
                output="# Run with: pytest test_bank.py\n# . .  (2 passed)",
                line_notes={
                    1: "File must be named test_*.py for pytest to discover it.",
                    9: "Test function names must start with test_.",
                    12: "Plain assert — pytest rewrites this to show actual vs expected on failure.",
                    14: "Each test function is independent; pytest creates a fresh call for each.",
                },
            ),
            CodeExample(
                title="pytest.raises and fixture",
                code=(
                    "import pytest\n"
                    "\n"
                    "class BankAccount:\n"
                    "    def __init__(self, owner, balance=0.0):\n"
                    "        self._balance = float(balance)\n"
                    "\n"
                    "    def withdraw(self, amount):\n"
                    "        if amount > self._balance:\n"
                    "            raise ValueError('Insufficient funds')\n"
                    "        self._balance -= amount\n"
                    "\n"
                    "@pytest.fixture\n"
                    "def account():\n"
                    "    return BankAccount('Alice', 200)\n"
                    "\n"
                    "def test_withdraw_raises_on_overdraft(account):\n"
                    "    with pytest.raises(ValueError):\n"
                    "        account.withdraw(999)\n"
                    "\n"
                    "def test_withdraw_succeeds(account):\n"
                    "    account.withdraw(50)\n"
                    "    assert account._balance == 150.0"
                ),
                explanation="A fixture supplies a fresh BankAccount to each test; pytest.raises asserts the exception.",
                output="# . .  (2 passed)",
                line_notes={
                    12: "@pytest.fixture marks this function as reusable test setup.",
                    13: "The fixture creates and returns a fresh account each time.",
                    16: "Declare fixture as parameter — pytest injects it automatically.",
                    17: "pytest.raises asserts that ValueError is raised inside the block.",
                    20: "Second test gets its own fresh account from the fixture.",
                },
            ),
            CodeExample(
                title="Parametrize for multiple inputs",
                code=(
                    "import pytest\n"
                    "\n"
                    "def is_even(n):\n"
                    "    return n % 2 == 0\n"
                    "\n"
                    "@pytest.mark.parametrize('n,expected', [\n"
                    "    (2, True),\n"
                    "    (3, False),\n"
                    "    (0, True),\n"
                    "    (-4, True),\n"
                    "])\n"
                    "def test_is_even(n, expected):\n"
                    "    assert is_even(n) == expected"
                ),
                explanation="One test function runs four times with different n and expected values.",
                output="# . . . .  (4 passed)",
                line_notes={
                    6: "@pytest.mark.parametrize takes the param names and a list of value tuples.",
                    12: "pytest calls this function once per tuple, substituting n and expected.",
                    13: "Single assert covers all four test cases.",
                },
            ),
        ],
        common_mistakes=[
            "Naming test files without the `test_` prefix — pytest won't discover them.",
            "Writing assert in tests without pytest — the built-in assert gives poor error messages; pytest rewrites it.",
            "Using a single mega-test that checks many things — one assert per test makes failures easier to diagnose.",
            "Not testing edge cases (empty input, zero, None) — boundary conditions are where most bugs hide.",
        ],
        practice_prompts=[
            "Write tests for a SavingsAccount.withdraw that charges a fee: test the balance change and test that ValueError is raised for insufficient funds.",
            "Use @pytest.mark.parametrize to test a function that categorises bank account balances as 'low', 'medium', or 'high'.",
            "Write a fixture that creates a Bank with three BankAccounts and use it in two different tests.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="How does pytest discover test functions automatically?",
                qtype="multiple_choice",
                correct_answer="It looks for files named test_*.py and functions named test_*",
                options=[
                    "It looks for files named test_*.py and functions named test_*",
                    "It runs all .py files in the project",
                    "You must register tests in a config file",
                    "It looks for functions decorated with @test",
                ],
                explanation="pytest's default discovery: files matching `test_*.py` or `*_test.py`, and functions starting with `test_`.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A pytest test passes if it completes without raising an exception.",
                qtype="true_false",
                correct_answer="true",
                explanation="Tests fail on AssertionError or any unexpected exception; they pass if they run to completion cleanly.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which pytest tool runs a single test function with multiple sets of inputs?",
                qtype="fill_blank",
                correct_answer="@pytest.mark.parametrize",
                explanation="`@pytest.mark.parametrize` generates multiple test cases from a list of argument tuples.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is a pytest fixture used for?",
                qtype="multiple_choice",
                correct_answer="Reusable setup code that is injected into test functions as parameters",
                options=[
                    "Reusable setup code that is injected into test functions as parameters",
                    "A way to skip a test under certain conditions",
                    "A decorator that marks a test as expected to fail",
                    "A tool to measure code coverage",
                ],
                explanation="Fixtures encapsulate setup (and optional teardown) and are injected by pytest when a test declares them as parameters.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="How do you assert that a function raises ValueError?",
                qtype="multiple_choice",
                correct_answer="with pytest.raises(ValueError): call_the_function()",
                options=[
                    "with pytest.raises(ValueError): call_the_function()",
                    "assert raises(ValueError)",
                    "try/except ValueError: pass",
                    "@pytest.expect(ValueError)",
                ],
                explanation="`pytest.raises()` is a context manager; the test passes only if the wrapped code raises the specified exception.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="i24-ex",
            title="Test the BankAccount",
            instructions=(
                "Write three pytest test functions for a BankAccount class:\n"
                "  1. test_deposit — deposits 100 into a 200-balance account, asserts 300\n"
                "  2. test_withdraw — withdraws 50 from 200, asserts 150\n"
                "  3. test_withdraw_raises — asserts ValueError when withdrawing more than balance\n\n"
                "Use a @pytest.fixture named `account` that returns BankAccount('Test', 200)."
            ),
            starter_code=(
                "import pytest\n"
                "\n"
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        self._balance += amount\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        if amount > self._balance:\n"
                "            raise ValueError('Insufficient funds')\n"
                "        self._balance -= amount\n"
                "\n"
                "@pytest.fixture\n"
                "def account():\n"
                "    return BankAccount('Test', 200)\n"
                "\n"
                "def test_deposit(account):\n"
                "    pass\n"
                "\n"
                "def test_withdraw(account):\n"
                "    pass\n"
                "\n"
                "def test_withdraw_raises(account):\n"
                "    pass"
            ),
            expected_output="# 3 passed",
            hints=[
                "test_deposit: account.deposit(100); assert account._balance == 300.0",
                "test_withdraw: account.withdraw(50); assert account._balance == 150.0",
                "test_withdraw_raises: `with pytest.raises(ValueError): account.withdraw(999)`",
            ],
            solution=(
                "import pytest\n"
                "\n"
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0.0):\n"
                "        self._balance = float(balance)\n"
                "\n"
                "    def deposit(self, amount):\n"
                "        self._balance += amount\n"
                "\n"
                "    def withdraw(self, amount):\n"
                "        if amount > self._balance:\n"
                "            raise ValueError('Insufficient funds')\n"
                "        self._balance -= amount\n"
                "\n"
                "@pytest.fixture\n"
                "def account():\n"
                "    return BankAccount('Test', 200)\n"
                "\n"
                "def test_deposit(account):\n"
                "    account.deposit(100)\n"
                "    assert account._balance == 300.0\n"
                "\n"
                "def test_withdraw(account):\n"
                "    account.withdraw(50)\n"
                "    assert account._balance == 150.0\n"
                "\n"
                "def test_withdraw_raises(account):\n"
                "    with pytest.raises(ValueError):\n"
                "        account.withdraw(999)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
]
