from __future__ import annotations

from ..models import CodeExample, Exercise, Lesson, Level, QuizQuestion

ADVANCED_LESSONS: list[Lesson] = [
    # ------------------------------------------------------------------ a01
    Lesson(
        id="a01",
        title="Iterators",
        level=Level.ADVANCED,
        estimated_minutes=14,
        explanation=(
            "An iterator is any object that implements two dunder methods: "
            "__iter__, which returns the iterator itself, and __next__, which "
            "returns the next value or raises StopIteration when done. Every "
            "for-loop in Python secretly calls these two methods under the hood.\n\n"
            "An iterable is a broader concept — it only needs __iter__. Lists, "
            "tuples, dicts, and files are all iterables; calling iter() on them "
            "returns a fresh iterator each time.\n\n"
            "Building your own iterator class lets you control exactly when and "
            "how data is produced. This is valuable when the full dataset is too "
            "large to hold in memory — for example, streaming rows from a huge "
            "CSV or chunked API response — because only one item exists in memory "
            "at a time.\n\n"
            "Understanding the iterator protocol also demystifies generators, "
            "zip, enumerate, map, and every other lazy tool in Python's standard "
            "library, since they all follow the same contract."
        ),
        key_terms={
            "__iter__": "Returns the iterator object itself; required on both iterables and iterators.",
            "__next__": "Returns the next value; raises StopIteration when the sequence is exhausted.",
            "StopIteration": "Exception that signals a for-loop (or next()) to stop.",
            "Iterable": "Any object with __iter__; can produce an iterator but is not one itself.",
            "Iterator": "An object with both __iter__ and __next__; stateful cursor over a sequence.",
            "iter() / next()": "Built-in functions that call __iter__ and __next__ respectively.",
        },
        code_examples=[
            CodeExample(
                title="Manual iteration with iter() and next()",
                code="""data = [10, 20, 30]
it = iter(data)
print(next(it))
print(next(it))
print(next(it))""",
                explanation=(
                    "Calling iter() on a list returns a list_iterator. "
                    "Each next() call advances it by one position."
                ),
                output="10\n20\n30",
                line_notes={
                    1: "A plain list is an [bold]iterable[/bold] — not itself an iterator.",
                    2: "[bold]iter()[/bold] creates a stateful iterator from the list.",
                    3: "First [bold]next()[/bold] call triggers __next__ → returns 10.",
                    5: "A fourth next() here would raise [bold]StopIteration[/bold].",
                },
            ),
            CodeExample(
                title="Custom iterator class for chunked data",
                code="""class ChunkedRange:
    def __init__(self, start, stop, step=1):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value

for n in ChunkedRange(0, 6, 2):
    print(n)""",
                explanation=(
                    "ChunkedRange walks a range in configurable steps, "
                    "producing one integer per __next__ call without "
                    "materialising the full list."
                ),
                output="0\n2\n4",
                line_notes={
                    7: "__iter__ returns [bold]self[/bold] — the object is its own iterator.",
                    9: "__next__ is called automatically by the for-loop each iteration.",
                    10: "Raise [bold]StopIteration[/bold] to tell the loop there are no more values.",
                    16: "for uses __iter__ then __next__ repeatedly — no manual calls needed.",
                },
            ),
        ],
        common_mistakes=[
            "Confusing iterables (have __iter__) with iterators (have __iter__ AND __next__).",
            "Forgetting to raise StopIteration, causing an infinite loop in __next__.",
            "Trying to restart an exhausted iterator — you must call iter() again on the original iterable.",
            "Omitting 'return self' from __iter__, which breaks use inside for-loops.",
        ],
        practice_prompts=[
            "How does a for-loop differ from a while-loop at the protocol level?",
            "When would you implement a custom iterator instead of using a generator function?",
            "What happens when you call iter() on an iterator (not just an iterable)?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which exception signals the end of an iterator?",
                qtype="multiple_choice",
                correct_answer="StopIteration",
                options=["IndexError", "StopIteration", "EndOfSequence", "IteratorDone"],
                explanation="StopIteration is the standard sentinel that tells for-loops and next() to stop.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="An object is an iterator if and only if it has __next__ alone (no __iter__ needed).",
                qtype="true_false",
                correct_answer="false",
                explanation="An iterator must implement BOTH __iter__ (returning self) and __next__.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="The built-in function that creates an iterator from an iterable is called ___.",
                qtype="fill_blank",
                correct_answer="iter",
                explanation="iter(obj) calls obj.__iter__() and returns the resulting iterator.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Explain the difference between an iterable and an iterator in one sentence.",
                qtype="short_answer",
                correct_answer="An iterable has __iter__ and can produce an iterator; an iterator also has __next__ and maintains state.",
                keywords=["__iter__", "__next__"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a01-ex",
            title="Countdown Iterator",
            instructions=(
                "Implement a Countdown class that iterates from a given start "
                "value down to 1 (inclusive). Use it with a for-loop to print "
                "each value. For start=3 the output should be:\n3\n2\n1"
            ),
            starter_code=(
                "class Countdown:\n"
                "    def __init__(self, start):\n"
                "        ...\n\n"
                "    def __iter__(self):\n"
                "        ...\n\n"
                "    def __next__(self):\n"
                "        ...\n\n"
                "for n in Countdown(3):\n"
                "    print(n)"
            ),
            expected_output="3\n2\n1",
            hints=[
                "Store the current value in self.current inside __init__.",
                "__iter__ should return self.",
                "In __next__, raise StopIteration when self.current < 1.",
                "Decrement self.current after capturing the value to return.",
            ],
            solution=(
                "class Countdown:\n"
                "    def __init__(self, start):\n"
                "        self.current = start\n\n"
                "    def __iter__(self):\n"
                "        return self\n\n"
                "    def __next__(self):\n"
                "        if self.current < 1:\n"
                "            raise StopIteration\n"
                "        value = self.current\n"
                "        self.current -= 1\n"
                "        return value\n\n"
                "for n in Countdown(3):\n"
                "    print(n)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a02
    Lesson(
        id="a02",
        title="Generators",
        level=Level.ADVANCED,
        estimated_minutes=14,
        explanation=(
            "A generator is a function that produces values lazily, one at a time, "
            "using the yield keyword instead of return. When Python sees yield in a "
            "function body it automatically builds an object that satisfies the full "
            "iterator protocol — you get __iter__ and __next__ for free.\n\n"
            "Because values are produced on demand, generators are memory-efficient "
            "for large or infinite sequences. Streaming millions of log lines, "
            "generating an endless sequence of IDs, or producing all permutations of "
            "a dataset — none of these require storing the full collection in RAM.\n\n"
            "Generator expressions (parentheses instead of brackets) give you the "
            "same laziness in a one-liner: (x**2 for x in range(10)) builds nothing "
            "until iterated. They compose well with sum(), max(), and other built-ins "
            "that accept any iterable.\n\n"
            "yield from lets one generator delegate to a sub-generator or any "
            "iterable, forwarding values transparently. This keeps generator pipelines "
            "clean and readable when chaining transformations."
        ),
        key_terms={
            "yield": "Pauses a generator function and emits a value; resumes on the next next() call.",
            "Generator function": "A function containing yield; calling it returns a generator object.",
            "Generator expression": "Lazy comprehension syntax using () instead of [].",
            "Lazy evaluation": "Computing values only when they are actually needed.",
            "yield from": "Delegates iteration to a sub-generator or iterable.",
            "send()": "Resumes a generator and injects a value as the result of the yield expression.",
        },
        code_examples=[
            CodeExample(
                title="A countdown generator",
                code="""def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)""",
                explanation="Each loop iteration resumes the generator after yield.",
                output="3\n2\n1",
                line_notes={
                    1: "Define a normal function — [bold]yield[/bold] inside makes it a generator.",
                    3: "[bold]yield n[/bold] emits a value and pauses the function here.",
                    4: "On the next request, execution resumes and decrements n.",
                    6: "Looping over the generator drives it to completion.",
                },
            ),
            CodeExample(
                title="Generator pipeline for data processing",
                code="""def read_rows(data):
    for row in data:
        yield row.strip()

def filter_nonempty(rows):
    for row in rows:
        if row:
            yield row

def parse_floats(rows):
    for row in rows:
        yield float(row)

raw = ["1.2\\n", "\\n", "3.4\\n", "5.6\\n"]
pipeline = parse_floats(filter_nonempty(read_rows(raw)))
print(list(pipeline))""",
                explanation=(
                    "Three generators are chained. No intermediate list is built; "
                    "each row flows through the pipeline one at a time."
                ),
                output="[1.2, 3.4, 5.6]",
                line_notes={
                    1: "First stage: strip whitespace from each raw string.",
                    5: "Second stage: skip empty strings (blanks after stripping).",
                    10: "Third stage: convert remaining strings to float.",
                    15: "Compose stages by wrapping — nothing runs until list() consumes pipeline.",
                },
            ),
            CodeExample(
                title="Generator expression for memory-efficient aggregation",
                code="""prices = [10.5, 22.0, 8.75, 31.0, 15.25]
total = sum(p * 1.08 for p in prices if p > 10)
print(round(total, 2))""",
                explanation=(
                    "The generator expression filters and transforms without "
                    "building an intermediate list."
                ),
                output="83.97",
                line_notes={
                    2: "Parentheses (not brackets) make this a [bold]generator expression[/bold].",
                },
            ),
        ],
        common_mistakes=[
            "Expecting a generator to restart — once exhausted, it's done; create a new one.",
            "Calling list() on an infinite generator and hanging the program.",
            "Mistaking a generator expression (lazy) for a list comprehension (eager).",
            "Forgetting that a generator function returns a generator object when called — the body does not run yet.",
        ],
        practice_prompts=[
            "When would a generator save memory compared to building a list?",
            "How would you write a generator that endlessly cycles through a list of labels?",
            "What is the difference between yield and yield from?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which keyword turns a function into a generator?",
                qtype="fill_blank",
                correct_answer="yield",
                explanation="yield emits values lazily and pauses the function.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="A generator can be iterated many times after exhaustion.",
                qtype="true_false",
                correct_answer="false",
                explanation="Once exhausted you must create a new generator object.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What does a generator expression use instead of square brackets?",
                qtype="multiple_choice",
                correct_answer="Parentheses ()",
                options=["Curly braces {}", "Parentheses ()", "Angle brackets <>", "Square brackets []"],
                explanation="(x for x in ...) is a generator expression; [x for x in ...] is a list comprehension.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Describe one scenario where a generator is more appropriate than a list.",
                qtype="short_answer",
                correct_answer="When the sequence is very large or infinite and you only need to iterate once.",
                keywords=["memory", "large"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a02-ex",
            title="Infinite IDs",
            instructions=(
                "Write a generator gen_ids() that yields 1, 2, 3, ... forever. "
                "Print the first three values using next()."
            ),
            starter_code=(
                "def gen_ids():\n"
                "    ...\n\n"
                "g = gen_ids()\n"
                "print(next(g), next(g), next(g))"
            ),
            expected_output="1 2 3",
            hints=[
                "Use a while True loop inside the generator.",
                "yield an incrementing counter variable.",
                "Initialise the counter to 1 before the loop.",
            ],
            solution=(
                "def gen_ids():\n"
                "    i = 1\n"
                "    while True:\n"
                "        yield i\n"
                "        i += 1\n\n"
                "g = gen_ids()\n"
                "print(next(g), next(g), next(g))"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a03
    Lesson(
        id="a03",
        title="Decorators",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation=(
            "A decorator is a callable that takes a function and returns a new "
            "function with added behaviour. The @ syntax is pure syntactic sugar: "
            "@my_decorator above def f() is identical to f = my_decorator(f). "
            "Because functions are first-class objects in Python, this pattern is "
            "completely idiomatic.\n\n"
            "The standard decorator body creates a wrapper function with *args and "
            "**kwargs so it can wrap any callable, calls the original function inside, "
            "and returns the result. Using functools.wraps on the wrapper preserves "
            "the original function's __name__ and __doc__, which matters for "
            "debugging, documentation generation, and testing.\n\n"
            "Decorators with arguments require an extra layer: a factory function "
            "that receives the arguments and returns the actual decorator. This "
            "three-level nesting — factory → decorator → wrapper — is a common "
            "pattern for retries, rate-limiting, logging, and caching.\n\n"
            "Class-based decorators implement __call__ instead of nesting functions, "
            "which can be cleaner when the decorator needs to maintain state across "
            "calls, such as counting invocations or caching results."
        ),
        key_terms={
            "@syntax": "Syntactic sugar: @dec before def f is equivalent to f = dec(f).",
            "Higher-order function": "A function that takes or returns another function.",
            "Wrapper function": "The inner function inside a decorator that adds behaviour around the original.",
            "functools.wraps": "Copies __name__, __doc__, and other metadata from the wrapped function.",
            "Decorator factory": "A function that accepts arguments and returns a decorator.",
            "Closure": "A wrapper that captures variables from the enclosing decorator scope.",
        },
        code_examples=[
            CodeExample(
                title="A timing decorator",
                code="""import time
import functools

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timeit
def slow_sum(n):
    return sum(range(n))

print(slow_sum(1_000_000))""",
                explanation=(
                    "timeit wraps any function, measures wall time, and prints "
                    "it before returning the original result."
                ),
                output="slow_sum took 0.0312s\n499999500000",
                line_notes={
                    4: "Decorator receives [bold]func[/bold] — the function being wrapped.",
                    5: "[bold]@functools.wraps(func)[/bold] copies metadata so wrapper looks like func.",
                    6: "wrapper accepts *args/**kwargs to wrap [bold]any[/bold] function signature.",
                    8: "Call the original function and capture its return value.",
                    11: "Return wrapper — this replaces func in the caller's namespace.",
                    13: "@ applies the decorator: slow_sum = timeit(slow_sum).",
                },
            ),
            CodeExample(
                title="Decorator factory with arguments",
                code="""import functools

def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")""",
                explanation=(
                    "repeat(times=3) is a factory — it returns a decorator. "
                    "The extra nesting is the cost of parameterising a decorator."
                ),
                output="Hello, Alice!\nHello, Alice!\nHello, Alice!",
                line_notes={
                    2: "Factory layer: receives the decorator's argument ([bold]times[/bold]).",
                    3: "Decorator layer: receives the function to wrap.",
                    5: "Wrapper layer: runs at call time, loops [bold]times[/bold] times.",
                    13: "@repeat(times=3) calls the factory first, then applies the returned decorator.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting functools.wraps, which causes the wrapper to shadow the original function's name.",
            "Calling the decorator when applying it — @timeit() (with parens) requires a factory; @timeit (no parens) does not.",
            "Not returning result from wrapper, making every decorated function return None.",
            "Building stateful decorators without realising closures share state across all calls.",
        ],
        practice_prompts=[
            "How would you write a decorator that retries a function up to N times on exception?",
            "What is the difference between @dec and @dec() when applied to a function?",
            "How could you use a class instead of nested functions to implement a caching decorator?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="@my_decorator above def f() is equivalent to which statement?",
                qtype="multiple_choice",
                correct_answer="f = my_decorator(f)",
                options=["f = my_decorator(f)", "my_decorator = f(my_decorator)", "f.decorator = my_decorator", "f(my_decorator)"],
                explanation="The @ syntax is pure syntactic sugar for reassigning the name to the decorated result.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="functools.wraps is necessary for a decorator to work at all.",
                qtype="true_false",
                correct_answer="false",
                explanation="functools.wraps is optional but strongly recommended — it preserves metadata like __name__ and __doc__.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="To make a decorator accept arguments, you need an extra outer function called a decorator ___.",
                qtype="fill_blank",
                correct_answer="factory",
                explanation="A decorator factory accepts the arguments and returns the actual decorator function.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What does *args, **kwargs in a wrapper function accomplish?",
                qtype="short_answer",
                correct_answer="It allows the wrapper to accept and forward any positional and keyword arguments, making the decorator work with any function signature.",
                keywords=["any", "arguments"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a03-ex",
            title="Call Counter Decorator",
            instructions=(
                "Write a decorator count_calls that tracks how many times a function "
                "has been called. Store the count on the wrapper as wrapper.calls. "
                "After decorating add(a, b) and calling it twice, print wrapper.calls."
            ),
            starter_code=(
                "import functools\n\n"
                "def count_calls(func):\n"
                "    ...\n\n"
                "@count_calls\n"
                "def add(a, b):\n"
                "    return a + b\n\n"
                "add(1, 2)\n"
                "add(3, 4)\n"
                "print(add.calls)"
            ),
            expected_output="2",
            hints=[
                "Initialise wrapper.calls = 0 inside the decorator (after defining wrapper).",
                "Increment wrapper.calls by 1 inside the wrapper body each call.",
                "Use @functools.wraps(func) on the wrapper.",
                "Return wrapper at the end of count_calls.",
            ],
            solution=(
                "import functools\n\n"
                "def count_calls(func):\n"
                "    @functools.wraps(func)\n"
                "    def wrapper(*args, **kwargs):\n"
                "        wrapper.calls += 1\n"
                "        return func(*args, **kwargs)\n"
                "    wrapper.calls = 0\n"
                "    return wrapper\n\n"
                "@count_calls\n"
                "def add(a, b):\n"
                "    return a + b\n\n"
                "add(1, 2)\n"
                "add(3, 4)\n"
                "print(add.calls)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a04
    Lesson(
        id="a04",
        title="Context Managers",
        level=Level.ADVANCED,
        estimated_minutes=14,
        explanation=(
            "A context manager is an object that defines setup and teardown logic "
            "for a block of code, expressed with the with statement. Python guarantees "
            "that the teardown runs even if an exception occurs inside the block — "
            "making it the idiomatic way to manage resources like files, database "
            "connections, and locks.\n\n"
            "Any class that implements __enter__ (setup, returns the resource) and "
            "__exit__ (teardown, receives exception info) is a context manager. "
            "__exit__ receives three arguments — exc_type, exc_val, tb — and can "
            "suppress the exception by returning True, or let it propagate by "
            "returning False (or None).\n\n"
            "The contextlib.contextmanager decorator is the shortcut: write a "
            "generator that yields once; everything before yield is __enter__, "
            "everything after is __exit__. This is usually cleaner than writing a "
            "class for simple cases.\n\n"
            "Common real-world uses include timing a block, temporarily changing "
            "working directories, opening database transactions, and mocking objects "
            "in tests. Getting comfortable with context managers makes your resource "
            "handling both safer and more readable."
        ),
        key_terms={
            "with statement": "Runs a block inside a context manager, guaranteeing cleanup.",
            "__enter__": "Called on entering the with block; return value bound to the 'as' variable.",
            "__exit__": "Called on exiting the block; receives exception info; return True to suppress.",
            "contextlib.contextmanager": "Decorator that turns a generator function into a context manager.",
            "Resource management": "Ensuring resources (files, locks, connections) are released after use.",
            "Exception suppression": "Returning True from __exit__ prevents the exception from propagating.",
        },
        code_examples=[
            CodeExample(
                title="Class-based context manager",
                code="""class ManagedFile:
    def __init__(self, path, mode="r"):
        self.path = path
        self.mode = mode

    def __enter__(self):
        self.file = open(self.path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, tb):
        self.file.close()
        return False

with ManagedFile("data.csv") as f:
    header = f.readline()""",
                explanation=(
                    "ManagedFile ensures the file is closed even if readline() raises. "
                    "Returning False lets any exception propagate normally."
                ),
                output="",
                line_notes={
                    6: "__enter__ opens the file and [bold]returns[/bold] it — bound to 'f' in the with clause.",
                    10: "__exit__ always closes the file regardless of whether an exception occurred.",
                    11: "Returning [bold]False[/bold] (or None) lets exceptions propagate; True would suppress them.",
                },
            ),
            CodeExample(
                title="contextmanager decorator shortcut",
                code="""from contextlib import contextmanager
import time

@contextmanager
def timer(label):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.4f}s")

with timer("list comprehension"):
    result = [x**2 for x in range(100_000)]""",
                explanation=(
                    "Everything before yield is __enter__; everything after is "
                    "__exit__. Much less boilerplate than a class."
                ),
                output="list comprehension: 0.0089s",
                line_notes={
                    4: "@contextmanager turns this generator into a context manager.",
                    6: "Code before [bold]yield[/bold] runs on entry — equivalent to __enter__.",
                    7: "[bold]yield[/bold] hands control to the with block; no value needed here.",
                    8: "Code after yield runs on exit — equivalent to __exit__.",
                },
            ),
        ],
        common_mistakes=[
            "Opening a file without a with statement and forgetting to call .close().",
            "Returning True from __exit__ unintentionally, silently swallowing exceptions.",
            "Yielding more than once inside a @contextmanager function — only one yield is allowed.",
            "Not handling exceptions inside @contextmanager with try/finally, so cleanup is skipped on error.",
        ],
        practice_prompts=[
            "How would you write a context manager that temporarily changes the current working directory?",
            "When would you choose a class-based context manager over @contextmanager?",
            "How does the with statement improve over try/finally for resource cleanup?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which dunder method is called when entering a with block?",
                qtype="fill_blank",
                correct_answer="__enter__",
                explanation="__enter__ runs setup and its return value is bound to the 'as' variable.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Returning True from __exit__ suppresses any exception raised in the with block.",
                qtype="true_false",
                correct_answer="true",
                explanation="True tells Python the exception has been handled; False (default) lets it propagate.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which module provides the @contextmanager decorator?",
                qtype="multiple_choice",
                correct_answer="contextlib",
                options=["functools", "contextlib", "itertools", "collections"],
                explanation="contextlib.contextmanager turns a one-yield generator into a context manager.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What happens if a @contextmanager generator does not use try/finally and an exception occurs in the with block?",
                qtype="short_answer",
                correct_answer="The code after yield (cleanup) is skipped unless wrapped in try/finally.",
                keywords=["cleanup", "skipped"],
                difficulty="hard",
            ),
        ],
        mini_exercise=Exercise(
            id="a04-ex",
            title="Suppress-error Context Manager",
            instructions=(
                "Use @contextmanager to write suppress_errors() that catches any "
                "exception inside its block and prints 'Error suppressed: <message>'. "
                "Demonstrate it by dividing by zero inside a with block."
            ),
            starter_code=(
                "from contextlib import contextmanager\n\n"
                "@contextmanager\n"
                "def suppress_errors():\n"
                "    ...\n\n"
                "with suppress_errors():\n"
                "    print(1 / 0)"
            ),
            expected_output="Error suppressed: division by zero",
            hints=[
                "Use try/yield/except inside the generator.",
                "Catch Exception as e and print the message.",
                "Do not re-raise the exception — the generator should finish normally.",
            ],
            solution=(
                "from contextlib import contextmanager\n\n"
                "@contextmanager\n"
                "def suppress_errors():\n"
                "    try:\n"
                "        yield\n"
                "    except Exception as e:\n"
                "        print(f'Error suppressed: {e}')\n\n"
                "with suppress_errors():\n"
                "    print(1 / 0)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a05
    Lesson(
        id="a05",
        title="Regular Expressions",
        level=Level.ADVANCED,
        estimated_minutes=20,
        explanation=(
            "Regular expressions (regex) are a concise language for describing "
            "text patterns. Python's re module compiles a pattern string into a "
            "finite automaton that can search, match, split, and substitute text "
            "extremely fast — far faster than hand-written loops for complex patterns.\n\n"
            "Key functions: re.match() anchors at the start; re.search() finds the "
            "first match anywhere; re.findall() returns a list of all non-overlapping "
            "matches; re.sub() replaces matches; re.split() splits on a pattern. "
            "Always use raw strings (r'...') for patterns so backslashes are not "
            "consumed by Python's string parser before reaching the regex engine.\n\n"
            "In data science, regex is indispensable for cleaning messy text: "
            "extracting numeric fields from free-form strings, normalising date "
            "formats, removing HTML tags, and validating structured data like "
            "email addresses or ISBNs before loading into a DataFrame.\n\n"
            "Compiled patterns (re.compile()) avoid re-parsing the pattern on every "
            "call — important inside loops that process millions of rows. Named "
            "groups (?P<name>...) make extraction code self-documenting and produce "
            "clean dictionaries via .groupdict()."
        ),
        key_terms={
            "Pattern": "A string written in regex syntax that describes a text shape to match.",
            "raw string": "r'...' prefix — backslashes are literal, not escape sequences.",
            "re.compile()": "Pre-compiles a pattern into a reusable Pattern object for efficiency.",
            "Group": "Parentheses () capture a sub-match; named groups use (?P<name>...).",
            "re.findall()": "Returns a list of all non-overlapping matches in a string.",
            "re.sub()": "Replaces every match of a pattern with a replacement string or function.",
        },
        code_examples=[
            CodeExample(
                title="Extracting numbers from messy text",
                code="""import re

text = "Temperature: 36.6C, Pressure: 1013.25hPa, Humidity: 78%"
pattern = re.compile(r'(\\d+\\.?\\d*)')
numbers = pattern.findall(text)
print(numbers)""",
                explanation=(
                    "A compiled pattern extracts every numeric token. "
                    "This is typical data-cleaning work before parsing into floats."
                ),
                output="['36.6', '1013.25', '78']",
                line_notes={
                    3: "Sensor reading with mixed units — common in IoT and scientific datasets.",
                    4: r"r'\d+\.?\d*' matches integers or decimals; compile() avoids re-parsing in loops.",
                    5: "findall returns a [bold]list of strings[/bold] — convert with float() as needed.",
                },
            ),
            CodeExample(
                title="Named groups for structured log parsing",
                code="""import re

log = "2024-03-15 14:32:07 ERROR Database connection timeout"
pattern = re.compile(
    r'(?P<date>\\d{4}-\\d{2}-\\d{2}) '
    r'(?P<time>\\d{2}:\\d{2}:\\d{2}) '
    r'(?P<level>\\w+) '
    r'(?P<message>.+)'
)
m = pattern.match(log)
if m:
    print(m.groupdict())""",
                explanation=(
                    "Named groups turn a regex match into a clean dictionary, "
                    "ready to be loaded into a DataFrame row or a dataclass."
                ),
                output="{'date': '2024-03-15', 'time': '14:32:07', 'level': 'ERROR', 'message': 'Database connection timeout'}",
                line_notes={
                    4: "Compile once; reuse for every log line in a file with millions of rows.",
                    5: r"(?P<date>...) captures into a named group — readable and self-documenting.",
                    10: "match() anchors at the start of the string.",
                    11: "[bold]groupdict()[/bold] returns {name: value} for all named groups.",
                },
            ),
            CodeExample(
                title="Cleaning text with re.sub()",
                code="""import re

html = "<p>Average <b>price</b>: $12.50 per kg</p>"
clean = re.sub(r'<[^>]+>', '', html)
print(clean)""",
                explanation="re.sub() removes all HTML tags, leaving only the text content.",
                output="Average price: $12.50 per kg",
                line_notes={
                    3: "Raw HTML — common output from web scraping or report exports.",
                    4: r"<[^>]+> matches an opening < then one-or-more non-> chars then >.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting the r'' prefix — '\\d' is the two-character string backslash-d, not a digit class.",
            "Using re.match() when you need re.search() — match() only checks the start of the string.",
            "Not compiling patterns used inside loops, causing unnecessary re-parsing on every iteration.",
            "Writing greedy patterns (.*) when lazy (.*?) is needed, capturing too much text.",
        ],
        practice_prompts=[
            "How would you use re.sub() to normalise all date formats (DD/MM/YYYY, YYYY-MM-DD) to ISO 8601?",
            "What named groups would you use to parse a CSV-style row with quoted fields?",
            "When should you prefer str.split() over re.split()?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which re function returns ALL non-overlapping matches as a list?",
                qtype="multiple_choice",
                correct_answer="re.findall()",
                options=["re.match()", "re.search()", "re.findall()", "re.fullmatch()"],
                explanation="re.findall() scans the entire string and returns a list of all matches.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="re.match() searches for a match anywhere in the string.",
                qtype="true_false",
                correct_answer="false",
                explanation="re.match() anchors at the START of the string; use re.search() for anywhere.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="The prefix ___ on a string literal prevents Python from interpreting backslashes as escape sequences.",
                qtype="fill_blank",
                correct_answer="r",
                explanation="r'\\d' is a raw string containing backslash-d; without r it would be a non-printable character.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What syntax creates a named capture group called 'year' in a regex pattern?",
                qtype="fill_blank",
                correct_answer="(?P<year>",
                explanation="(?P<year>\\d{4}) captures four digits into a group named 'year'.",
                difficulty="hard",
            ),
        ],
        mini_exercise=Exercise(
            id="a05-ex",
            title="Email Extractor",
            instructions=(
                "Write a function extract_emails(text) that returns a list of all "
                "email addresses found in text using re.findall(). Test it on the "
                "sample string provided."
            ),
            starter_code=(
                "import re\n\n"
                "def extract_emails(text):\n"
                "    ...\n\n"
                "sample = 'Contact alice@example.com or bob.smith@data.org for help.'\n"
                "print(extract_emails(sample))"
            ),
            expected_output="['alice@example.com', 'bob.smith@data.org']",
            hints=[
                r"A simple pattern: r'[\w.+-]+@[\w-]+\.[a-zA-Z]+'",
                "Use re.findall() with the pattern and text.",
                "Return the list directly.",
            ],
            solution=(
                "import re\n\n"
                "def extract_emails(text):\n"
                r"    return re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]+', text)"
                "\n\n"
                "sample = 'Contact alice@example.com or bob.smith@data.org for help.'\n"
                "print(extract_emails(sample))"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a06
    Lesson(
        id="a06",
        title="Async and Await",
        level=Level.ADVANCED,
        estimated_minutes=20,
        explanation=(
            "Asynchronous programming lets a single thread handle many tasks at "
            "once by suspending a coroutine while it waits for I/O — a network "
            "request, a file read, a database query — and resuming it when the "
            "result is ready. Python's asyncio library provides the event loop "
            "that schedules these coroutines.\n\n"
            "async def creates a coroutine function; calling it returns a coroutine "
            "object that does not run until awaited or scheduled. await suspends "
            "the current coroutine and yields control to the event loop, which can "
            "run other coroutines in the meantime. This is cooperative concurrency: "
            "coroutines voluntarily yield, so they must always await I/O-bound calls.\n\n"
            "asyncio.gather() runs multiple coroutines concurrently and collects "
            "their results. Fetching ten URLs concurrently with gather() can be "
            "10x faster than fetching them sequentially, without threads. This makes "
            "async the right tool for data pipelines that call many APIs or read "
            "from many files simultaneously.\n\n"
            "The key mental model: async/await is NOT about parallelism (using "
            "multiple CPU cores). It is about concurrency — efficiently interleaving "
            "tasks that spend most of their time waiting. For CPU-bound work, use "
            "multiprocessing or concurrent.futures instead."
        ),
        key_terms={
            "Coroutine": "A function defined with async def; suspended at each await, resumed by the event loop.",
            "Event loop": "The scheduler that drives coroutines, switching between them at await points.",
            "await": "Suspends the current coroutine and gives control back to the event loop.",
            "asyncio.gather()": "Runs multiple coroutines concurrently and returns their results as a list.",
            "async for / async with": "Async versions of for-loops and context managers for async iterables/CMs.",
            "Concurrency vs parallelism": "Concurrency interleaves tasks on one thread; parallelism runs them on multiple CPUs.",
        },
        code_examples=[
            CodeExample(
                title="Basic coroutine and event loop",
                code="""import asyncio

async def greet(name, delay):
    await asyncio.sleep(delay)
    print(f"Hello, {name}!")

async def main():
    await asyncio.gather(
        greet("Alice", 1),
        greet("Bob", 0.5),
    )

asyncio.run(main())""",
                explanation=(
                    "Both greets run concurrently. Bob (0.5 s) finishes before "
                    "Alice (1 s) even though Alice was scheduled first."
                ),
                output="Hello, Bob!\nHello, Alice!",
                line_notes={
                    3: "[bold]async def[/bold] makes greet a coroutine function.",
                    4: "[bold]await asyncio.sleep()[/bold] suspends greet, freeing the event loop.",
                    8: "[bold]asyncio.gather()[/bold] schedules both coroutines concurrently.",
                    12: "[bold]asyncio.run()[/bold] creates an event loop, runs main(), then closes it.",
                },
            ),
            CodeExample(
                title="Concurrent HTTP requests with httpx",
                code="""import asyncio
import httpx

URLS = [
    "https://httpbin.org/get?n=1",
    "https://httpbin.org/get?n=2",
    "https://httpbin.org/get?n=3",
]

async def fetch(client, url):
    resp = await client.get(url)
    return resp.status_code

async def main():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[fetch(client, url) for url in URLS]
        )
    print(results)

asyncio.run(main())""",
                explanation=(
                    "Three HTTP requests run concurrently through a single shared "
                    "client. async with manages the client lifecycle safely."
                ),
                output="[200, 200, 200]",
                line_notes={
                    10: "fetch is a coroutine — it [bold]awaits[/bold] the HTTP response.",
                    14: "[bold]async with[/bold] is the async version of with — ensures client.aclose() is called.",
                    15: "gather fans out all fetch coroutines simultaneously.",
                    16: "List unpacking (*[...]) spreads the coroutine list as positional arguments.",
                },
            ),
        ],
        common_mistakes=[
            "Calling an async function without await — you get a coroutine object, not the result.",
            "Using time.sleep() instead of await asyncio.sleep() — blocks the entire event loop.",
            "Running asyncio.run() inside a running event loop (e.g., Jupyter) — use await directly instead.",
            "Thinking async speeds up CPU-bound code — it only helps I/O-bound tasks.",
        ],
        practice_prompts=[
            "How does asyncio.gather() differ from running coroutines sequentially with await?",
            "When would you choose threading over asyncio for concurrency?",
            "How would you limit concurrency to N simultaneous requests using asyncio.Semaphore?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does await do inside a coroutine?",
                qtype="multiple_choice",
                correct_answer="Suspends the coroutine and yields control to the event loop",
                options=[
                    "Suspends the coroutine and yields control to the event loop",
                    "Blocks the entire thread until the awaited call finishes",
                    "Creates a new thread for the awaited task",
                    "Returns None immediately without waiting",
                ],
                explanation="await suspends just the current coroutine; the event loop can run other coroutines while it waits.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="async/await is suitable for speeding up CPU-bound computations.",
                qtype="true_false",
                correct_answer="false",
                explanation="async/await is designed for I/O-bound concurrency. CPU-bound work needs multiprocessing.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="The function used to run a top-level coroutine from synchronous code is asyncio.___().",
                qtype="fill_blank",
                correct_answer="run",
                explanation="asyncio.run(coro) creates an event loop, runs the coroutine, and closes the loop.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which asyncio function runs multiple coroutines concurrently and collects all results?",
                qtype="multiple_choice",
                correct_answer="asyncio.gather()",
                options=["asyncio.run()", "asyncio.gather()", "asyncio.wait()", "asyncio.shield()"],
                explanation="asyncio.gather() schedules all provided coroutines concurrently and returns a list of results.",
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="a06-ex",
            title="Concurrent Delays",
            instructions=(
                "Write an async function run_tasks() that uses asyncio.gather() to "
                "run three coroutines concurrently: task(1, 0.3), task(2, 0.1), "
                "task(3, 0.2). Each task should sleep for its delay then print "
                "'Task N done'. The output order should reflect the shortest delay "
                "finishing first."
            ),
            starter_code=(
                "import asyncio\n\n"
                "async def task(n, delay):\n"
                "    ...\n\n"
                "async def run_tasks():\n"
                "    ...\n\n"
                "asyncio.run(run_tasks())"
            ),
            expected_output="Task 2 done\nTask 3 done\nTask 1 done",
            hints=[
                "Inside task(), use await asyncio.sleep(delay) then print.",
                "Inside run_tasks(), call asyncio.gather() with all three task() calls.",
                "Pass task(1, 0.3), task(2, 0.1), task(3, 0.2) as arguments to gather().",
            ],
            solution=(
                "import asyncio\n\n"
                "async def task(n, delay):\n"
                "    await asyncio.sleep(delay)\n"
                "    print(f'Task {n} done')\n\n"
                "async def run_tasks():\n"
                "    await asyncio.gather(\n"
                "        task(1, 0.3),\n"
                "        task(2, 0.1),\n"
                "        task(3, 0.2),\n"
                "    )\n\n"
                "asyncio.run(run_tasks())"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a07
    Lesson(
        id="a07",
        title="Calling APIs with requests / httpx",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation=(
            "The requests library is the most popular way to make HTTP calls in "
            "Python. A single requests.get(url) returns a Response object with "
            ".status_code, .json(), .text, and .headers. Always check the status "
            "code — or call response.raise_for_status() — before consuming the body, "
            "so network errors are caught immediately rather than silently corrupted.\n\n"
            "For production code and anything async, httpx is the modern alternative. "
            "It has an almost identical synchronous API but also provides an "
            "AsyncClient for concurrent requests. Both libraries support sessions "
            "(persistent connections, shared headers, automatic cookie handling) and "
            "timeout configuration — always set timeouts to avoid hanging forever.\n\n"
            "Authentication, pagination, and rate limiting are the three patterns "
            "you will encounter most. Bearer tokens go in the Authorization header; "
            "API keys often go in a query parameter or custom header. Paginated APIs "
            "typically return a next_page URL or cursor; loop until you get None.\n\n"
            "For data science work, APIs are the primary source of real-time data — "
            "financial prices, weather, census data, social media. The usual pipeline "
            "is: fetch JSON → normalise with json_normalize or pd.DataFrame → clean "
            "→ analyse. Always cache responses during development to avoid hitting "
            "rate limits while iterating on your analysis."
        ),
        key_terms={
            "requests.get()": "Sends an HTTP GET and returns a Response object.",
            "raise_for_status()": "Raises HTTPError for 4xx/5xx responses; no-op for 2xx.",
            "Session": "A requests.Session reuses a TCP connection and shares headers/cookies.",
            "Timeout": "Maximum seconds to wait for a connection or response — always set this.",
            "httpx.AsyncClient": "Async HTTP client compatible with asyncio for concurrent requests.",
            "Pagination": "Pattern where large API responses are split across multiple pages.",
        },
        code_examples=[
            CodeExample(
                title="Basic GET request and JSON parsing",
                code="""import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.71,
    "longitude": -74.01,
    "current_weather": True,
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()
data = response.json()
print(data["current_weather"]["temperature"])""",
                explanation=(
                    "Fetch current weather for New York. params are URL-encoded "
                    "automatically; raise_for_status() guards against HTTP errors."
                ),
                output="18.4",
                line_notes={
                    3: "Separate base URL from query parameters for readability and encoding safety.",
                    10: "Always pass [bold]timeout[/bold] — without it, a hanging server hangs your program.",
                    11: "[bold]raise_for_status()[/bold] converts 4xx/5xx into a Python exception immediately.",
                    12: ".json() parses the response body as JSON into a Python dict.",
                },
            ),
            CodeExample(
                title="Session with authentication and pagination",
                code="""import requests

BASE = "https://api.example.com"

session = requests.Session()
session.headers.update({
    "Authorization": "Bearer MY_TOKEN",
    "Accept": "application/json",
})

results = []
page = 1
while True:
    resp = session.get(f"{BASE}/records", params={"page": page}, timeout=10)
    resp.raise_for_status()
    payload = resp.json()
    results.extend(payload["data"])
    if not payload.get("next_page"):
        break
    page += 1

print(f"Fetched {len(results)} records")""",
                explanation=(
                    "A Session persists the Authorization header across requests. "
                    "The while loop fetches every page until next_page is absent."
                ),
                output="Fetched 250 records",
                line_notes={
                    5: "[bold]Session[/bold] reuses the TCP connection and shares headers for all requests.",
                    6: "Set auth header once — every request in this session sends it automatically.",
                    12: "Pagination loop — page until the API signals there are no more results.",
                    17: "Safely check next_page with .get() to avoid KeyError if field is absent.",
                },
            ),
        ],
        common_mistakes=[
            "Not setting a timeout — a slow server hangs the program indefinitely.",
            "Not calling raise_for_status(), silently processing error responses as if they were data.",
            "Constructing query strings with string formatting — use the params= argument instead.",
            "Creating a new requests.Session() inside a loop — sessions should be created once and reused.",
        ],
        practice_prompts=[
            "How would you add exponential backoff retry logic to a requests call?",
            "What is the advantage of httpx over requests for an async data pipeline?",
            "How would you cache API responses to disk during exploratory data analysis?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which method raises an exception automatically for 4xx and 5xx responses?",
                qtype="fill_blank",
                correct_answer="raise_for_status",
                explanation="response.raise_for_status() raises requests.HTTPError for any non-2xx status.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Creating a new requests.Session per request is more efficient than reusing one.",
                qtype="true_false",
                correct_answer="false",
                explanation="Sessions reuse TCP connections and share settings; creating one per request wastes resources.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which requests.get() parameter should you ALWAYS set to avoid hanging indefinitely?",
                qtype="multiple_choice",
                correct_answer="timeout",
                options=["headers", "timeout", "verify", "stream"],
                explanation="Without timeout, a slow or unresponsive server will block your program forever.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is one advantage of httpx over requests for a data pipeline that calls many APIs?",
                qtype="short_answer",
                correct_answer="httpx provides an AsyncClient that works with asyncio, enabling concurrent requests without threads.",
                keywords=["async", "concurrent"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a07-ex",
            title="Fetch a Public JSON API",
            instructions=(
                "Use requests to fetch https://jsonplaceholder.typicode.com/todos/1 "
                "and print the title and completed fields from the JSON response. "
                "Use raise_for_status() and a timeout of 10 seconds."
            ),
            starter_code=(
                "import requests\n\n"
                "url = 'https://jsonplaceholder.typicode.com/todos/1'\n"
                "# fetch and print title and completed"
            ),
            expected_output="delectus aut autem\nFalse",
            hints=[
                "Call requests.get(url, timeout=10).",
                "Call .raise_for_status() on the response.",
                "Call .json() to get a dict, then access ['title'] and ['completed'].",
            ],
            solution=(
                "import requests\n\n"
                "url = 'https://jsonplaceholder.typicode.com/todos/1'\n"
                "resp = requests.get(url, timeout=10)\n"
                "resp.raise_for_status()\n"
                "data = resp.json()\n"
                "print(data['title'])\n"
                "print(data['completed'])"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a08
    Lesson(
        id="a08",
        title="Web Scraping Basics",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation=(
            "Web scraping is the process of programmatically extracting data from "
            "HTML pages. The typical Python stack is requests to download the HTML "
            "and BeautifulSoup4 to parse and navigate it. BeautifulSoup represents "
            "the page as a tree of Tag objects that you can search with CSS selectors "
            "or by tag name and attributes.\n\n"
            "Always inspect the page in a browser's DevTools before writing code — "
            "right-click the element you want, choose 'Inspect', and note the tag "
            "name, class, and id. soup.select('div.price') uses CSS selectors; "
            "soup.find('h1') finds the first matching tag; .find_all() returns a list. "
            "Use .get_text(strip=True) to get clean text without HTML entities.\n\n"
            "Ethical scraping means respecting robots.txt, adding delays between "
            "requests, identifying your bot in the User-Agent header, and not "
            "hammering servers. Many sites block requests without a browser-like "
            "User-Agent. For JavaScript-rendered pages, BeautifulSoup sees only the "
            "raw HTML — you need Playwright or Selenium to run the JS first.\n\n"
            "For data science, scraping is often the only way to collect datasets "
            "that do not have a public API — product prices, news headlines, sports "
            "stats. The output is usually a list of dicts, which loads directly into "
            "a pandas DataFrame with pd.DataFrame(records)."
        ),
        key_terms={
            "BeautifulSoup": "HTML/XML parser that turns raw markup into a navigable tree of Tag objects.",
            "soup.select()": "CSS-selector-based search; returns a list of matching Tag objects.",
            "soup.find()": "Returns the first matching tag by name, class, id, or other attributes.",
            "get_text()": "Extracts all text content from a Tag, optionally stripping whitespace.",
            "robots.txt": "A file at /robots.txt that declares which paths scrapers should not access.",
            "User-Agent": "HTTP header identifying the client; set it politely when scraping.",
        },
        code_examples=[
            CodeExample(
                title="Scraping a table of data",
                code="""import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
headers = {"User-Agent": "Mozilla/5.0 (educational scraper)"}

resp = requests.get(url, headers=headers, timeout=15)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

table = soup.select_one("table.wikitable")
rows = table.find_all("tr")[1:]
records = []
for row in rows:
    cells = row.find_all(["td", "th"])
    if len(cells) >= 2:
        records.append({
            "country": cells[0].get_text(strip=True),
            "gdp": cells[1].get_text(strip=True),
        })

print(records[:2])""",
                explanation=(
                    "Downloads a Wikipedia table and parses each row into a dict. "
                    "records loads directly into pd.DataFrame(records)."
                ),
                output="[{'country': 'World', 'gdp': '109,529,214'}, {'country': 'United States', 'gdp': '28,781,083'}]",
                line_notes={
                    4: "Identify the URL in DevTools Network tab — copy the actual page URL.",
                    5: "Set a polite [bold]User-Agent[/bold]; many servers reject Python's default.",
                    9: "html.parser is built-in; lxml is faster for large pages.",
                    11: "CSS selector — [bold]table.wikitable[/bold] matches a <table class='wikitable'>.",
                    17: "[bold]get_text(strip=True)[/bold] removes surrounding whitespace and HTML entities.",
                },
            ),
            CodeExample(
                title="Scraping with CSS selectors",
                code=(
                    'from bs4 import BeautifulSoup\n\n'
                    'html = \'<ul class="prices">'
                    '<li class="item"><span class="name">Apples</span>'
                    '<span class="price">$1.20</span></li>'
                    '<li class="item"><span class="name">Bananas</span>'
                    '<span class="price">$0.50</span></li>'
                    '</ul>\'\n'
                    'soup = BeautifulSoup(html, "html.parser")\n'
                    'for item in soup.select("li.item"):\n'
                    '    name = item.select_one("span.name").get_text()\n'
                    '    price = item.select_one("span.price").get_text()\n'
                    '    print(f"{name}: {price}")'
                ),
                explanation=(
                    "CSS selectors make navigating nested HTML concise. "
                    "select_one() returns one tag; select() returns a list."
                ),
                output="Apples: $1.20\nBananas: $0.50",
                line_notes={
                    5: "[bold]select()[/bold] returns all matching tags — iterate over them.",
                    6: "[bold]select_one()[/bold] returns the first match within the parent tag.",
                },
            ),
        ],
        common_mistakes=[
            "Not setting a User-Agent header — many sites return 403 or a CAPTCHA page.",
            "Calling .get_text() on None when a tag is missing — always guard with 'if tag:'.",
            "Scraping sites that render content with JavaScript — BeautifulSoup only sees static HTML.",
            "Not adding delays between requests, triggering rate limits or IP bans.",
        ],
        practice_prompts=[
            "How would you convert a list of scraped dicts into a pandas DataFrame?",
            "What would you do if a site requires JavaScript to render the data you need?",
            "How do you check robots.txt before writing a scraper?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which BeautifulSoup method uses CSS selectors to find elements?",
                qtype="multiple_choice",
                correct_answer="soup.select()",
                options=["soup.find()", "soup.select()", "soup.query()", "soup.css()"],
                explanation="soup.select('div.price') uses CSS selector syntax to find all matching elements.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="BeautifulSoup can execute JavaScript to render dynamic pages.",
                qtype="true_false",
                correct_answer="false",
                explanation="BeautifulSoup only parses static HTML. Playwright or Selenium is needed for JS-rendered pages.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The Tag method that returns only the text content (no HTML) is .get____().",
                qtype="fill_blank",
                correct_answer="text",
                explanation=".get_text() strips all tags and returns the inner text content.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Why should you add time.sleep() between scraping requests?",
                qtype="short_answer",
                correct_answer="To avoid overloading the server, triggering rate limits, or getting your IP banned.",
                keywords=["rate", "server"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a08-ex",
            title="Parse a Price List",
            instructions=(
                "Given the HTML string below, use BeautifulSoup to extract a list of "
                "(product, price) tuples and print them. Do not make any HTTP requests."
            ),
            starter_code=(
                "from bs4 import BeautifulSoup\n\n"
                "html = '''\n"
                "<ul>\n"
                "  <li><b>Widget</b> - $9.99</li>\n"
                "  <li><b>Gadget</b> - $24.50</li>\n"
                "  <li><b>Doohickey</b> - $4.75</li>\n"
                "</ul>\n"
                "'''\n\n"
                "soup = BeautifulSoup(html, 'html.parser')\n"
                "# extract and print each product and price"
            ),
            expected_output="Widget - $9.99\nGadget - $24.50\nDoohickey - $4.75",
            hints=[
                "Use soup.find_all('li') to get each list item.",
                "Use .get_text(strip=True) on each <li> to get the full text.",
                "Or find the <b> tag for the name and extract remaining text separately.",
            ],
            solution=(
                "from bs4 import BeautifulSoup\n\n"
                "html = '''\n"
                "<ul>\n"
                "  <li><b>Widget</b> - $9.99</li>\n"
                "  <li><b>Gadget</b> - $24.50</li>\n"
                "  <li><b>Doohickey</b> - $4.75</li>\n"
                "</ul>\n"
                "'''\n\n"
                "soup = BeautifulSoup(html, 'html.parser')\n"
                "for li in soup.find_all('li'):\n"
                "    print(li.get_text(strip=True))"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a09
    Lesson(
        id="a09",
        title="SQLite",
        level=Level.ADVANCED,
        estimated_minutes=20,
        explanation=(
            "SQLite is a serverless, file-based relational database built into "
            "Python's standard library via the sqlite3 module. Because there is no "
            "server to configure, it is the ideal database for local scripts, "
            "prototyping, data analysis pipelines, and embedded applications — a "
            "single .db file contains the entire database.\n\n"
            "The workflow is always: connect → get a cursor → execute SQL → commit "
            "(for writes) → close. Python's sqlite3 supports parameterised queries "
            "with ? placeholders, which prevent SQL injection and handle type "
            "conversions automatically. Never use f-strings or % formatting to "
            "interpolate user data into SQL.\n\n"
            "For data science, SQLite bridges raw files and pandas elegantly. "
            "pd.read_sql_query(sql, con) runs a SELECT and returns a DataFrame "
            "directly. df.to_sql(table, con, if_exists='replace') dumps a DataFrame "
            "into a table. This makes SQLite a lightweight data store for cleaned "
            "datasets, intermediate results, and experiment logs.\n\n"
            "The with connection: pattern (connection as context manager) auto-commits "
            "on success and auto-rolls back on exception, keeping your data consistent "
            "without manual commit/rollback calls."
        ),
        key_terms={
            "sqlite3.connect()": "Opens (or creates) a .db file and returns a Connection object.",
            "Cursor": "Object used to execute SQL statements and retrieve results.",
            "Parameterised query": "SQL with ? placeholders; values passed separately to prevent injection.",
            "commit()": "Persists pending write operations (INSERT/UPDATE/DELETE) to the file.",
            "fetchall()": "Returns all rows from the last SELECT as a list of tuples.",
            "pd.read_sql_query()": "Runs SQL against a sqlite3 connection and returns a pandas DataFrame.",
        },
        code_examples=[
            CodeExample(
                title="Create, insert, and query a table",
                code=(
                    'import sqlite3\n\n'
                    'con = sqlite3.connect("sensors.db")\n'
                    'cur = con.cursor()\n\n'
                    'cur.execute(\n'
                    '    "CREATE TABLE IF NOT EXISTS readings (\n'
                    '        id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                    '        sensor TEXT NOT NULL,\n'
                    '        value REAL NOT NULL,\n'
                    '        ts TEXT NOT NULL\n'
                    '    )"\n'
                    ')\n\n'
                    'rows = [\n'
                    '    ("temp_01", 22.4, "2024-03-15 08:00"),\n'
                    '    ("temp_01", 23.1, "2024-03-15 09:00"),\n'
                    '    ("temp_02", 19.8, "2024-03-15 08:00"),\n'
                    ']\n'
                    'cur.executemany(\n'
                    '    "INSERT INTO readings (sensor, value, ts) VALUES (?, ?, ?)",\n'
                    '    rows,\n'
                    ')\n'
                    'con.commit()\n\n'
                    'cur.execute("SELECT sensor, AVG(value) FROM readings GROUP BY sensor")\n'
                    'for row in cur.fetchall():\n'
                    '    print(row)\n\n'
                    'con.close()'
                ),
                explanation=(
                    "Creates a sensor readings table, bulk-inserts rows with "
                    "executemany, and runs a GROUP BY aggregation."
                ),
                output="('temp_01', 22.75)\n('temp_02', 19.8)",
                line_notes={
                    3: "Pass ':memory:' instead of a filename for a temporary in-memory database.",
                    6: "Always use [bold]CREATE TABLE IF NOT EXISTS[/bold] to make scripts idempotent.",
                    20: "executemany is faster than looping execute() for bulk inserts.",
                    21: "[bold]?[/bold] placeholders: sqlite3 escapes values safely — never use f-strings here.",
                    24: "[bold]con.commit()[/bold] flushes writes to disk; without it changes are lost.",
                },
            ),
            CodeExample(
                title="SQLite with pandas for data analysis",
                code="""import sqlite3
import pandas as pd

con = sqlite3.connect("sensors.db")

df = pd.read_sql_query(
    "SELECT sensor, value, ts FROM readings ORDER BY ts",
    con,
)
print(df.head())

summary = df.groupby("sensor")["value"].describe()
print(summary)

con.close()""",
                explanation=(
                    "pd.read_sql_query pulls a SQLite table straight into a "
                    "DataFrame — no manual fetchall or column mapping needed."
                ),
                output="  sensor  value                ts\n0  temp_01   22.4  2024-03-15 08:00\n...",
                line_notes={
                    5: "[bold]pd.read_sql_query()[/bold] runs SQL and maps results to a DataFrame automatically.",
                    11: "Once in pandas, all DataFrame operations (groupby, merge, plot) are available.",
                },
            ),
        ],
        common_mistakes=[
            "Using f-strings or % formatting to put user input into SQL — always use ? placeholders.",
            "Forgetting con.commit() after INSERT/UPDATE/DELETE — changes disappear when the connection closes.",
            "Not closing the connection — leaves file locks that can block other processes.",
            "Calling cur.fetchall() after executemany (which is a write, not a SELECT) — raises an error.",
        ],
        practice_prompts=[
            "How would you store ML experiment results (params + metrics) in SQLite for comparison?",
            "When would you prefer SQLite over a CSV file for storing intermediate analysis data?",
            "How would you use df.to_sql() to load a cleaned pandas DataFrame into SQLite?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which placeholder character does sqlite3 use for parameterised queries?",
                qtype="fill_blank",
                correct_answer="?",
                explanation="cur.execute('SELECT * FROM t WHERE id = ?', (42,)) safely passes the value.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Changes made with INSERT are saved immediately without calling commit().",
                qtype="true_false",
                correct_answer="false",
                explanation="sqlite3 uses transactions; commit() is required to persist writes to disk.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which pandas function runs a SQL query against a sqlite3 connection and returns a DataFrame?",
                qtype="multiple_choice",
                correct_answer="pd.read_sql_query()",
                options=["pd.read_csv()", "pd.read_sql_query()", "pd.from_sql()", "pd.query()"],
                explanation="pd.read_sql_query(sql, con) is the standard bridge between SQLite and pandas.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What filename do you pass to sqlite3.connect() for an in-memory database that disappears when closed?",
                qtype="fill_blank",
                correct_answer=":memory:",
                explanation="sqlite3.connect(':memory:') creates a temporary database entirely in RAM.",
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a09-ex",
            title="In-Memory Student Database",
            instructions=(
                "Using an in-memory SQLite database, create a table 'students' with "
                "columns name (TEXT) and grade (REAL). Insert three rows of your choice. "
                "Query and print the name and grade of all students with grade >= 85, "
                "ordered by grade descending."
            ),
            starter_code=(
                "import sqlite3\n\n"
                "con = sqlite3.connect(':memory:')\n"
                "cur = con.cursor()\n"
                "# create table, insert rows, query and print"
            ),
            expected_output="Alice 95.0\nBob 88.0",
            hints=[
                "CREATE TABLE students (name TEXT, grade REAL);",
                "Use executemany with ? placeholders to insert rows.",
                "SELECT name, grade FROM students WHERE grade >= 85 ORDER BY grade DESC",
                "Loop over cur.fetchall() and print each row.",
            ],
            solution=(
                "import sqlite3\n\n"
                "con = sqlite3.connect(':memory:')\n"
                "cur = con.cursor()\n"
                "cur.execute('CREATE TABLE students (name TEXT, grade REAL)')\n"
                "cur.executemany('INSERT INTO students VALUES (?, ?)', [\n"
                "    ('Alice', 95.0), ('Bob', 88.0), ('Carol', 72.0)\n"
                "])\n"
                "con.commit()\n"
                "cur.execute(\n"
                "    'SELECT name, grade FROM students WHERE grade >= 85 ORDER BY grade DESC'\n"
                ")\n"
                "for name, grade in cur.fetchall():\n"
                "    print(name, grade)\n"
                "con.close()"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a10
    Lesson(
        id="a10",
        title="ORMs Overview",
        level=Level.ADVANCED,
        estimated_minutes=16,
        explanation=(
            "An Object-Relational Mapper (ORM) lets you interact with a relational "
            "database using Python classes instead of raw SQL. Each class maps to a "
            "table, each instance maps to a row, and attribute access replaces SELECT "
            "statements. This improves code readability, reduces boilerplate, and "
            "makes swapping database backends (SQLite → PostgreSQL) a one-line change.\n\n"
            "SQLAlchemy is the standard Python ORM, offering two APIs: the Core "
            "(SQL expression language close to raw SQL) and the ORM layer (declarative "
            "models with relationships). SQLModel, built on top of SQLAlchemy and "
            "Pydantic, is the modern FastAPI-friendly option. Django's built-in ORM "
            "is the default for Django web projects.\n\n"
            "The main ORM concepts are: Model (class = table), Session (unit of work "
            "that tracks changes), Query (chainable filter/order/limit), and "
            "Relationship (foreign-key navigation via attributes). ORMs handle "
            "connection pooling, parameterisation, and migrations (via Alembic).\n\n"
            "ORMs are not always the right tool. Complex analytical queries, "
            "bulk inserts of millions of rows, and window functions are often cleaner "
            "and faster in raw SQL or pandas. Use the ORM for CRUD operations and "
            "domain logic; fall back to pd.read_sql_query() for analytics."
        ),
        key_terms={
            "ORM": "Object-Relational Mapper — maps Python classes to database tables.",
            "Model": "A Python class that represents a database table; each attribute is a column.",
            "Session": "The ORM's unit-of-work; tracks new/changed/deleted objects and flushes to DB.",
            "Query": "Chainable API for building SELECT statements: filter(), order_by(), limit().",
            "Relationship": "ORM attribute that navigates a foreign-key link (e.g. user.orders).",
            "Migration": "Versioned schema change script; managed by Alembic for SQLAlchemy.",
        },
        code_examples=[
            CodeExample(
                title="SQLAlchemy ORM: define and query",
                code="""from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    sensor = Column(String, nullable=False)
    value = Column(Float, nullable=False)

engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([
        Measurement(sensor="temp_01", value=22.4),
        Measurement(sensor="temp_01", value=23.1),
    ])
    session.commit()

    results = session.query(Measurement).filter(
        Measurement.value > 22.0
    ).all()
    for m in results:
        print(m.sensor, m.value)""",
                explanation=(
                    "Defines a table as a class, creates the schema, inserts rows "
                    "via Python objects, and queries with a Pythonic filter."
                ),
                output="temp_01 22.4\ntemp_01 23.1",
                line_notes={
                    4: "[bold]DeclarativeBase[/bold] is the modern SQLAlchemy 2.x base class.",
                    7: "The class name becomes the Python handle; __tablename__ is the DB table name.",
                    12: "[bold]create_engine()[/bold] sets the connection string — swap 'sqlite:///:memory:' for a real URL.",
                    14: "[bold]create_all()[/bold] issues CREATE TABLE IF NOT EXISTS for all mapped models.",
                    16: "Session as context manager auto-commits on success, rolls back on exception.",
                    21: "filter() generates a WHERE clause; .all() executes and returns a list.",
                },
            ),
            CodeExample(
                title="SQLModel: modern Pydantic-friendly ORM",
                code="""from sqlmodel import Field, SQLModel, create_engine, Session, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    power_level: float

engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Hero(name="Rogue", power_level=8.5))
    session.commit()

    stmt = select(Hero).where(Hero.power_level > 7)
    heroes = session.exec(stmt).all()
    for h in heroes:
        print(h.name, h.power_level)""",
                explanation=(
                    "SQLModel combines SQLAlchemy with Pydantic — models validate "
                    "data on assignment and integrate naturally with FastAPI."
                ),
                output="Rogue 8.5",
                line_notes={
                    3: "[bold]table=True[/bold] tells SQLModel this class maps to a database table.",
                    4: "Pydantic-style type annotations — SQLModel infers column types automatically.",
                    14: "select() returns a type-safe statement; session.exec() runs it.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting session.commit() — changes are queued in memory until committed.",
            "Loading entire related collections accidentally (N+1 query problem) — use joinedload() for relationships.",
            "Using the ORM for bulk analytical queries — raw SQL or pd.read_sql_query is often faster.",
            "Mixing SQLAlchemy 1.x and 2.x patterns — they have different Session and query APIs.",
        ],
        practice_prompts=[
            "When would you choose raw sqlite3 over an ORM for a data science project?",
            "How does Alembic help manage schema changes over the lifetime of a project?",
            "What is the N+1 query problem and how does joinedload() solve it?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="In SQLAlchemy, which object tracks changes to model instances and flushes them to the database?",
                qtype="multiple_choice",
                correct_answer="Session",
                options=["Engine", "Session", "Connection", "Query"],
                explanation="The Session is the ORM's unit-of-work; it tracks new, dirty, and deleted objects.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="An ORM is always faster than raw SQL for data analytics workloads.",
                qtype="true_false",
                correct_answer="false",
                explanation="ORMs add overhead and abstraction; complex analytical queries are often faster in raw SQL or pandas.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="The process of versioning and applying database schema changes is called ___.",
                qtype="fill_blank",
                correct_answer="migration",
                explanation="Alembic is the standard migration tool for SQLAlchemy projects.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What does the table=True argument do in SQLModel?",
                qtype="short_answer",
                correct_answer="It tells SQLModel that the class should map to a real database table, not just be a data-validation model.",
                keywords=["table", "database"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a10-ex",
            title="ORM Book Table",
            instructions=(
                "Using SQLAlchemy (or SQLModel), define a Book model with fields "
                "id (primary key), title (str), and pages (int). Create an in-memory "
                "SQLite database, insert two books, and query all books with more than "
                "200 pages, printing their titles."
            ),
            starter_code=(
                "from sqlalchemy import create_engine, Column, Integer, String\n"
                "from sqlalchemy.orm import DeclarativeBase, Session\n\n"
                "class Base(DeclarativeBase):\n"
                "    pass\n\n"
                "# define Book model here\n\n"
                "engine = create_engine('sqlite:///:memory:')\n"
                "Base.metadata.create_all(engine)\n"
                "# insert books and query"
            ),
            expected_output="Clean Code",
            hints=[
                "Add __tablename__ = 'books' to the Book class.",
                "Use Column(Integer, primary_key=True) for id.",
                "Insert Book(title='Clean Code', pages=431) and Book(title='Haiku', pages=80).",
                "Filter with .filter(Book.pages > 200).all()",
            ],
            solution=(
                "from sqlalchemy import create_engine, Column, Integer, String\n"
                "from sqlalchemy.orm import DeclarativeBase, Session\n\n"
                "class Base(DeclarativeBase):\n"
                "    pass\n\n"
                "class Book(Base):\n"
                "    __tablename__ = 'books'\n"
                "    id = Column(Integer, primary_key=True)\n"
                "    title = Column(String, nullable=False)\n"
                "    pages = Column(Integer, nullable=False)\n\n"
                "engine = create_engine('sqlite:///:memory:')\n"
                "Base.metadata.create_all(engine)\n\n"
                "with Session(engine) as session:\n"
                "    session.add_all([\n"
                "        Book(title='Clean Code', pages=431),\n"
                "        Book(title='Haiku', pages=80),\n"
                "    ])\n"
                "    session.commit()\n"
                "    for b in session.query(Book).filter(Book.pages > 200).all():\n"
                "        print(b.title)"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a11
    Lesson(
        id="a11",
        title="CLI Apps with Typer",
        level=Level.ADVANCED,
        estimated_minutes=16,
        explanation=(
            "Typer is a library for building command-line interfaces from Python "
            "type annotations. You define commands as plain functions, annotate "
            "parameters with Python types, and Typer automatically generates argument "
            "parsing, help text, error messages, and shell completion — no argparse "
            "boilerplate required.\n\n"
            "A Typer app is created with app = typer.Typer(). Functions decorated "
            "with @app.command() become subcommands. Parameters with no default become "
            "required positional arguments; parameters with defaults become optional "
            "flags. Annotating with typer.Option() or typer.Argument() gives you "
            "control over the flag name, help string, and validation.\n\n"
            "Rich integration (typer installs rich automatically) gives you "
            "coloured output, tables, progress bars, and styled error messages with "
            "no extra setup. typer.echo() is the simple printer; print() and Rich's "
            "Console work equally well.\n\n"
            "For data science and automation scripts, Typer turns a single Python "
            "file into a polished tool that non-programmers can use. Wrapping a "
            "pandas pipeline as a CLI app — with arguments for input file, output "
            "file, and filter threshold — makes it composable with shell pipelines "
            "and schedulable by cron or Airflow."
        ),
        key_terms={
            "typer.Typer()": "Creates the CLI application object; add commands with @app.command().",
            "@app.command()": "Decorator that registers a function as a CLI subcommand.",
            "typer.Option()": "Marks a parameter as a named flag (--name) with optional default and help.",
            "typer.Argument()": "Marks a parameter as a positional argument.",
            "app()": "Entry point; call this in __main__ to run the CLI.",
            "typer.echo()": "Print to stdout; supports ANSI colours via the fg parameter.",
        },
        code_examples=[
            CodeExample(
                title="Simple Typer CLI app",
                code="""import typer

app = typer.Typer()

@app.command()
def greet(
    name: str,
    times: int = typer.Option(1, help="How many times to greet"),
):
    for _ in range(times):
        typer.echo(f"Hello, {name}!")

if __name__ == "__main__":
    app()""",
                explanation=(
                    "name is a required positional argument; --times is an optional "
                    "flag. Running 'python app.py Alice --times 2' prints twice."
                ),
                output="Hello, Alice!\nHello, Alice!",
                line_notes={
                    2: "Typer infers argument types and help text from Python annotations.",
                    5: "@app.command() registers greet as the default command.",
                    7: "Type annotation [bold]str[/bold] → required positional arg; Typer validates automatically.",
                    8: "[bold]typer.Option()[/bold] makes this a named flag with a default value.",
                    13: "app() parses sys.argv and dispatches to the correct command.",
                },
            ),
            CodeExample(
                title="Multi-command data pipeline CLI",
                code="""import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def clean(
    input: Path = typer.Argument(..., help="Input CSV path"),
    output: Path = typer.Option("cleaned.csv", help="Output CSV path"),
):
    typer.echo(f"Cleaning {input} -> {output}")

@app.command()
def summarise(
    input: Path = typer.Argument(...),
    column: str = typer.Option("value", help="Column to summarise"),
):
    typer.echo(f"Summarising column '{column}' in {input}")

if __name__ == "__main__":
    app()""",
                explanation=(
                    "Two subcommands: 'python pipeline.py clean data.csv' and "
                    "'python pipeline.py summarise data.csv --column price'."
                ),
                output="Cleaning data.csv -> cleaned.csv",
                line_notes={
                    8: "[bold]...[/bold] as the default means the argument is required (no default).",
                    9: "Path type gives automatic existence checking with typer.Option(exists=True).",
                    12: "Each @app.command() function becomes a separate subcommand.",
                },
            ),
        ],
        common_mistakes=[
            "Forgetting if __name__ == '__main__': app() — the CLI never starts without it.",
            "Using mutable defaults in typer.Option() — use None and handle inside the function.",
            "Confusing typer.Argument (positional) with typer.Option (flag) syntax.",
            "Not testing with --help first — Typer generates comprehensive help text automatically.",
        ],
        practice_prompts=[
            "How would you add a --verbose flag that enables debug logging when set?",
            "How would you wrap a pandas data-cleaning script as a Typer CLI?",
            "What is the difference between typer.Argument() and typer.Option()?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which decorator registers a function as a Typer subcommand?",
                qtype="fill_blank",
                correct_answer="@app.command()",
                explanation="@app.command() tells Typer to expose the decorated function as a CLI command.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In Typer, a function parameter with no default value becomes a required positional argument.",
                qtype="true_false",
                correct_answer="true",
                explanation="Typer infers required positional args from unannotated or non-defaulted parameters.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which typer helper creates a named flag like --output rather than a positional argument?",
                qtype="multiple_choice",
                correct_answer="typer.Option()",
                options=["typer.Argument()", "typer.Option()", "typer.Flag()", "typer.Param()"],
                explanation="typer.Option() generates --flag-name style CLI parameters; typer.Argument() is positional.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What single line at the bottom of a Typer script actually starts the CLI application?",
                qtype="short_answer",
                correct_answer="app() inside an if __name__ == '__main__': block.",
                keywords=["app()", "__main__"],
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="a11-ex",
            title="Word Count CLI",
            instructions=(
                "Write a Typer CLI app with a single command count_words that takes "
                "a required positional argument text (str) and prints the number of "
                "words. Running it with 'Hello world foo' should print 3."
            ),
            starter_code=(
                "import typer\n\n"
                "app = typer.Typer()\n\n"
                "@app.command()\n"
                "def count_words(text: str):\n"
                "    ...\n\n"
                "if __name__ == '__main__':\n"
                "    app()"
            ),
            expected_output="3",
            hints=[
                "Use len(text.split()) to count words.",
                "Print the count with typer.echo() or print().",
            ],
            solution=(
                "import typer\n\n"
                "app = typer.Typer()\n\n"
                "@app.command()\n"
                "def count_words(text: str):\n"
                "    typer.echo(len(text.split()))\n\n"
                "if __name__ == '__main__':\n"
                "    app()"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a12
    Lesson(
        id="a12",
        title="Packaging Python Projects",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation=(
            "Packaging turns your script or library into something that can be "
            "installed with pip and imported by other projects. The modern toolchain "
            "is driven by pyproject.toml — a single config file that replaces the "
            "old setup.py and setup.cfg. Build backends like Hatchling, Flit, and "
            "setuptools read pyproject.toml to produce wheel and sdist archives.\n\n"
            "The minimum pyproject.toml needs [project] metadata (name, version, "
            "dependencies) and a [build-system] section naming the backend. Add a "
            "src/ layout: put your package under src/your_package/ and mark it as "
            "the package root. This prevents the local directory from accidentally "
            "shadowing an installed copy during testing.\n\n"
            "pip install -e . installs your package in editable mode — changes to "
            "source files are reflected immediately without reinstalling. This is the "
            "standard development workflow. When ready to publish, build with "
            "'python -m build' (produces dist/*.whl and dist/*.tar.gz), then upload "
            "with twine upload dist/*.\n\n"
            "Virtual environments isolate each project's dependencies. Always create "
            "one with python -m venv .venv and activate it before pip installing. "
            "Lock files (pip-tools, Poetry, uv) pin exact versions for reproducible "
            "environments — critical for data science where library version mismatches "
            "break analyses."
        ),
        key_terms={
            "pyproject.toml": "The modern single-file project config: metadata, dependencies, build backend.",
            "Build backend": "Tool (Hatchling, setuptools, Flit) that turns source into wheel/sdist.",
            "Wheel (.whl)": "Pre-built distribution archive; fastest to install.",
            "Editable install": "pip install -e . — source changes apply without reinstalling.",
            "Virtual environment": "Isolated Python install per project; created with python -m venv.",
            "twine": "Tool for securely uploading distributions to PyPI.",
        },
        code_examples=[
            CodeExample(
                title="Minimal pyproject.toml",
                code="""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myanalysis"
version = "0.1.0"
description = "Data analysis utilities"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.0",
    "matplotlib>=3.7",
    "httpx>=0.27",
]

[project.scripts]
myanalysis = "myanalysis.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["src/myanalysis"]""",
                explanation=(
                    "A complete pyproject.toml for a data-science utility package "
                    "with a CLI entry point. Place this file at the project root."
                ),
                output="",
                line_notes={
                    1: "[build-system] tells pip which backend to use when building the package.",
                    5: "[project] is the PEP 621 metadata table — required for PyPI publishing.",
                    10: "List runtime dependencies here; pip installs them automatically.",
                    16: "[project.scripts] creates a console command: 'myanalysis' runs cli.app().",
                    19: "src/ layout: the actual package lives under src/myanalysis/__init__.py.",
                },
            ),
            CodeExample(
                title="Recommended src/ directory layout",
                code="""myanalysis/
├── pyproject.toml
├── README.md
├── src/
│   └── myanalysis/
│       ├── __init__.py
│       ├── cli.py
│       └── utils.py
└── tests/
    └── test_utils.py""",
                explanation=(
                    "The src/ layout prevents the local package from being imported "
                    "before it is installed, catching missing-dependency bugs early."
                ),
                output="",
                line_notes={
                    1: "Project root — pyproject.toml lives here alongside README.md.",
                    4: "src/ prefix isolates the installable package from top-level scripts.",
                    5: "The importable package name matches [project] name in pyproject.toml.",
                    9: "tests/ lives outside src/ so test helpers are not shipped in the package.",
                },
            ),
        ],
        common_mistakes=[
            "Putting the package directly at the project root — the local directory shadows the installed version in tests.",
            "Forgetting to activate the virtual environment before pip install.",
            "Hardcoding absolute version pins (==) in install_requires — use >= to allow compatible upgrades.",
            "Not incrementing the version before publishing to PyPI — overwriting a published version fails.",
        ],
        practice_prompts=[
            "What is the difference between a wheel and a source distribution?",
            "How would you add an optional 'dev' dependency group for pytest and ruff?",
            "Why is the src/ layout recommended over a flat layout?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="The modern Python project configuration file is called ___.",
                qtype="fill_blank",
                correct_answer="pyproject.toml",
                explanation="pyproject.toml (PEP 517/518/621) replaces setup.py and setup.cfg.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="pip install -e . installs a package in editable mode so source changes apply immediately.",
                qtype="true_false",
                correct_answer="true",
                explanation="Editable mode (-e) symlinks the source directory so changes are reflected without reinstalling.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which tool is used to upload a built distribution to PyPI?",
                qtype="multiple_choice",
                correct_answer="twine",
                options=["pip", "twine", "build", "hatch"],
                explanation="twine upload dist/* securely uploads wheel and sdist archives to PyPI.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What is one advantage of the src/ layout over a flat project layout?",
                qtype="short_answer",
                correct_answer="It prevents the local uninstalled package from being accidentally imported during testing, catching missing-dependency bugs.",
                keywords=["import", "test"],
                difficulty="hard",
            ),
        ],
        mini_exercise=Exercise(
            id="a12-ex",
            title="Write a pyproject.toml",
            instructions=(
                "Write a minimal pyproject.toml for a package called 'datasummary' "
                "version 0.2.0 that depends on pandas>=2.0. Use hatchling as the "
                "build backend and set the wheel package path to src/datasummary. "
                "Print the file contents to verify."
            ),
            starter_code=(
                "content = '''\n"
                "# fill in the pyproject.toml content here\n"
                "'''\n"
                "print(content.strip())"
            ),
            expected_output=(
                "[build-system]\n"
                "requires = [\"hatchling\"]\n"
                "build-backend = \"hatchling.build\"\n\n"
                "[project]\n"
                "name = \"datasummary\"\n"
                "version = \"0.2.0\"\n"
                "dependencies = [\"pandas>=2.0\"]\n\n"
                "[tool.hatch.build.targets.wheel]\n"
                "packages = [\"src/datasummary\"]"
            ),
            hints=[
                "Start with [build-system] then [project].",
                "dependencies is a TOML array: [\"pandas>=2.0\"]",
                "The wheel section is under [tool.hatch.build.targets.wheel].",
            ],
            solution=(
                "content = '''\n"
                "[build-system]\n"
                "requires = [\"hatchling\"]\n"
                "build-backend = \"hatchling.build\"\n\n"
                "[project]\n"
                "name = \"datasummary\"\n"
                "version = \"0.2.0\"\n"
                "dependencies = [\"pandas>=2.0\"]\n\n"
                "[tool.hatch.build.targets.wheel]\n"
                "packages = [\"src/datasummary\"]\n"
                "'''\n"
                "print(content.strip())"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a13
    Lesson(
        id="a13",
        title="Environment Variables",
        level=Level.ADVANCED,
        estimated_minutes=12,
        explanation=(
            "Environment variables are key-value pairs set in the shell that running "
            "processes can read. They are the standard way to supply secrets (API "
            "keys, database passwords), configuration (debug mode, log level), and "
            "environment-specific values (staging vs production URLs) to a Python "
            "program without hardcoding them in source code.\n\n"
            "os.environ is a dict-like object that maps variable names to values. "
            "os.environ['KEY'] raises KeyError if the variable is absent; "
            "os.environ.get('KEY', default) is safer. os.getenv() is an alias for "
            ".get(). Always validate that required variables are present at startup — "
            "fail fast with a clear error rather than crashing deep in the pipeline.\n\n"
            "The python-dotenv library loads a .env file into os.environ at startup. "
            "This is the standard development workflow: keep secrets in .env (never "
            "commit it — add to .gitignore), load with load_dotenv(), and read with "
            "os.getenv(). In production, set variables directly in the shell, "
            "systemd unit file, Docker environment, or CI/CD secrets — no .env file.\n\n"
            "For data science projects, environment variables hold database URLs, "
            "cloud storage credentials, model API keys, and path overrides. A "
            "config.py module that reads all variables once at import time is cleaner "
            "than scattering os.getenv() calls throughout the codebase."
        ),
        key_terms={
            "os.environ": "Dict-like object of the current process's environment variables.",
            "os.getenv()": "Returns the value of an env var, or a default if it is absent.",
            ".env file": "Plain-text file of KEY=VALUE pairs loaded by python-dotenv in development.",
            "load_dotenv()": "Function from python-dotenv that reads .env into os.environ.",
            ".gitignore": "Git file listing paths that should never be committed — always include .env.",
            "Secret": "A sensitive value (password, API key) that must never be hardcoded in source.",
        },
        code_examples=[
            CodeExample(
                title="Reading env vars safely",
                code="""import os

api_key = os.getenv("OPENWEATHER_API_KEY")
if api_key is None:
    raise EnvironmentError(
        "OPENWEATHER_API_KEY is not set. "
        "Export it or add it to .env"
    )

db_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
debug = os.getenv("DEBUG", "false").lower() == "true"

print(f"DB: {db_url}, debug={debug}")""",
                explanation=(
                    "Required secrets fail fast with a clear message. Optional "
                    "settings have sensible defaults."
                ),
                output="DB: sqlite:///local.db, debug=False",
                line_notes={
                    3: "[bold]os.getenv()[/bold] returns None (not KeyError) when the variable is absent.",
                    4: "Fail fast at startup — better than a cryptic error inside the pipeline.",
                    10: "Provide a default for optional config so the program works without .env.",
                    11: "Env var values are always strings — convert to bool/int as needed.",
                },
            ),
            CodeExample(
                title="Loading a .env file with python-dotenv",
                code="""from dotenv import load_dotenv
import os

load_dotenv()

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
data_dir = os.getenv("DATA_DIR", "/tmp/data")

print(f"data_dir={data_dir}")""",
                explanation=(
                    "load_dotenv() reads .env from the current directory (or a "
                    "specified path) and populates os.environ. Call it once, early."
                ),
                output="data_dir=/tmp/data",
                line_notes={
                    3: "[bold]load_dotenv()[/bold] is a no-op if .env is absent — safe in production.",
                    5: "After load_dotenv, os.getenv works exactly as if variables were exported in the shell.",
                },
            ),
        ],
        common_mistakes=[
            "Committing .env to git — secrets leak to anyone with repo access; always add .env to .gitignore.",
            "Using os.environ['KEY'] instead of os.getenv() — raises KeyError in environments where the variable is absent.",
            "Hardcoding fallback secrets in code — the default should be None or a non-sensitive placeholder.",
            "Setting environment variables inside the Python process with os.environ — changes only affect the current process and its children, not the parent shell.",
        ],
        practice_prompts=[
            "How would you validate that all required environment variables are set at application startup?",
            "What is the difference between exporting a variable in the shell vs loading it with load_dotenv()?",
            "How would you handle a .env file for local dev vs Kubernetes secrets in production?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which function from os reads an env var and returns None (not an exception) if absent?",
                qtype="fill_blank",
                correct_answer="os.getenv",
                explanation="os.getenv('KEY') returns None if KEY is not set; os.environ['KEY'] raises KeyError.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="It is safe to commit a .env file to a public GitHub repository.",
                qtype="true_false",
                correct_answer="false",
                explanation=".env files contain secrets; they must be listed in .gitignore and never committed.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What library provides the load_dotenv() function?",
                qtype="multiple_choice",
                correct_answer="python-dotenv",
                options=["dotenv-python", "python-dotenv", "envparse", "config"],
                explanation="Install with: pip install python-dotenv; import with: from dotenv import load_dotenv",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Why should required API keys fail immediately at startup rather than deeper in the code?",
                qtype="short_answer",
                correct_answer="Failing fast at startup gives a clear error message pinpointing the missing config, rather than a cryptic error deep in the call stack after partial work.",
                keywords=["startup", "clear"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a13-ex",
            title="Config Validator",
            instructions=(
                "Write a function check_env(required_keys) that takes a list of "
                "environment variable names. For each key, print 'OK: KEY' if set, "
                "or 'MISSING: KEY' if not. Test with ['HOME', 'NONEXISTENT_XYZ']."
            ),
            starter_code=(
                "import os\n\n"
                "def check_env(required_keys):\n"
                "    ...\n\n"
                "check_env(['HOME', 'NONEXISTENT_XYZ'])"
            ),
            expected_output="OK: HOME\nMISSING: NONEXISTENT_XYZ",
            hints=[
                "Loop over required_keys.",
                "Use os.getenv(key) — check if it is None.",
                "Print 'OK: KEY' or 'MISSING: KEY' accordingly.",
            ],
            solution=(
                "import os\n\n"
                "def check_env(required_keys):\n"
                "    for key in required_keys:\n"
                "        if os.getenv(key) is not None:\n"
                "            print(f'OK: {key}')\n"
                "        else:\n"
                "            print(f'MISSING: {key}')\n\n"
                "check_env(['HOME', 'NONEXISTENT_XYZ'])"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a14
    Lesson(
        id="a14",
        title="Config Files",
        level=Level.ADVANCED,
        estimated_minutes=14,
        explanation=(
            "Config files externalise settings that change between deployments or "
            "users — database URLs, feature flags, model hyperparameters — without "
            "requiring code changes. Python's standard library provides configparser "
            "for .ini-style files and the tomllib module (Python 3.11+) for reading "
            "TOML. Third-party options include PyYAML for .yaml and pydantic-settings "
            "for structured, type-validated configuration.\n\n"
            "INI files (configparser) are simple key-value pairs grouped in sections. "
            "TOML is the modern preference: it is type-aware (integers, booleans, and "
            "arrays are distinct from strings), readable, and already familiar from "
            "pyproject.toml. YAML is expressive but error-prone — significant "
            "whitespace and surprising implicit type coercions catch many developers.\n\n"
            "A clean pattern is a single config.py that reads the chosen format at "
            "import time and exposes typed attributes. Application code imports from "
            "config, not from os.environ or raw file reads scattered everywhere. "
            "Combine environment variables (secrets) with config files (non-secret "
            "settings) using a merge strategy: env vars override file values.\n\n"
            "For data science and ML projects, config files are standard for "
            "hyperparameters, data paths, and experiment settings. Version-controlling "
            "a config file gives you a reproducible record of every experiment run."
        ),
        key_terms={
            "configparser": "Standard-library module for reading/writing .ini-style config files.",
            "TOML": "Tom's Obvious Minimal Language — typed config format used by pyproject.toml.",
            "tomllib": "Built-in TOML reader (Python 3.11+); read-only, open file in binary mode.",
            "YAML": "Human-readable format popular in DevOps; requires PyYAML (pip install pyyaml).",
            "Config hierarchy": "Pattern where env vars override file config which overrides defaults.",
            "pydantic-settings": "Library that reads env vars and config files into validated Pydantic models.",
        },
        code_examples=[
            CodeExample(
                title="Reading an INI config with configparser",
                code="""import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

db_host = config.get("database", "host", fallback="localhost")
db_port = config.getint("database", "port", fallback=5432)
debug = config.getboolean("app", "debug", fallback=False)

print(f"DB: {db_host}:{db_port}, debug={debug}")""",
                explanation=(
                    "configparser reads a .ini file with [section] headers. "
                    "Type-aware getters (getint, getboolean) avoid manual casting."
                ),
                output="DB: localhost:5432, debug=False",
                line_notes={
                    3: "[bold]ConfigParser()[/bold] creates a parser; read() loads one or more files.",
                    6: "fallback= avoids KeyError when the key or section is missing.",
                    7: "getint() and getboolean() convert strings to the right Python types.",
                },
            ),
            CodeExample(
                title="Reading TOML config (Python 3.11+)",
                code="""import tomllib

with open("config.toml", "rb") as f:
    cfg = tomllib.load(f)

model = cfg["training"]["model"]
lr = cfg["training"]["learning_rate"]
epochs = cfg["training"]["epochs"]

print(f"Training {model} for {epochs} epochs at lr={lr}")""",
                explanation=(
                    "TOML values are already typed — no string-to-int conversions. "
                    "Open in binary mode ('rb') as required by tomllib."
                ),
                output="Training resnet50 for 10 epochs at lr=0.001",
                line_notes={
                    3: "tomllib requires [bold]binary mode[/bold] ('rb') — it handles encoding internally.",
                    4: "[bold]tomllib.load()[/bold] returns a plain Python dict.",
                    6: "TOML types map directly: strings, floats, ints — no manual conversion needed.",
                },
            ),
        ],
        common_mistakes=[
            "Opening a TOML file in text mode ('r') — tomllib requires binary mode ('rb').",
            "Using YAML for config files and getting bitten by implicit type coercions (e.g., 'yes' → True).",
            "Putting secrets (passwords, API keys) in config files that get committed to git.",
            "Reading the config file inside a function called many times — read once at module import.",
        ],
        practice_prompts=[
            "How would you merge a TOML config file with environment variable overrides?",
            "What are the pros and cons of YAML vs TOML for an ML experiment config?",
            "How would you validate a config file's types and required fields at startup?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="tomllib.load() requires the file to be opened in which mode?",
                qtype="multiple_choice",
                correct_answer="Binary ('rb')",
                options=["Text ('r')", "Binary ('rb')", "Append ('a')", "Write ('w')"],
                explanation="tomllib handles encoding internally and requires binary mode 'rb'.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="configparser.getint() converts a string value from the config file to a Python integer.",
                qtype="true_false",
                correct_answer="true",
                explanation="Type-specific getters (getint, getfloat, getboolean) handle the conversion for you.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The built-in Python 3.11+ module for reading TOML files is called ___.",
                qtype="fill_blank",
                correct_answer="tomllib",
                explanation="tomllib was added to the standard library in Python 3.11 (PEP 680).",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Why should secrets like passwords NOT be stored in config files committed to git?",
                qtype="short_answer",
                correct_answer="Anyone with access to the repository can read the secrets; use environment variables or a secrets manager instead.",
                keywords=["secret", "git"],
                difficulty="easy",
            ),
        ],
        mini_exercise=Exercise(
            id="a14-ex",
            title="INI Config Reader",
            instructions=(
                "Write a function load_db_config(path) that uses configparser to read "
                "a .ini file and return a dict with keys host, port (int), and name. "
                "Use fallbacks of 'localhost', 5432, and 'mydb'. Print the result."
            ),
            starter_code=(
                "import configparser\n\n"
                "def load_db_config(path):\n"
                "    config = configparser.ConfigParser()\n"
                "    config.read(path)\n"
                "    ...\n\n"
                "print(load_db_config('nonexistent.ini'))"
            ),
            expected_output="{'host': 'localhost', 'port': 5432, 'name': 'mydb'}",
            hints=[
                "Use config.get('database', 'host', fallback='localhost').",
                "Use config.getint('database', 'port', fallback=5432).",
                "Return a dict with the three keys.",
            ],
            solution=(
                "import configparser\n\n"
                "def load_db_config(path):\n"
                "    config = configparser.ConfigParser()\n"
                "    config.read(path)\n"
                "    return {\n"
                "        'host': config.get('database', 'host', fallback='localhost'),\n"
                "        'port': config.getint('database', 'port', fallback=5432),\n"
                "        'name': config.get('database', 'name', fallback='mydb'),\n"
                "    }\n\n"
                "print(load_db_config('nonexistent.ini'))"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a15
    Lesson(
        id="a15",
        title="Automation Scripts",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation=(
            "Automation scripts use Python to handle repetitive tasks: renaming "
            "batches of files, processing every CSV in a directory, sending "
            "scheduled reports, watching a folder for new data. The standard tools "
            "are pathlib for file system work, subprocess for running shell commands, "
            "shutil for copying and archiving, and schedule or cron for time-based "
            "execution.\n\n"
            "pathlib.Path is the modern, object-oriented replacement for os.path. "
            "Path.glob() and Path.rglob() match files by pattern; .read_text() and "
            ".write_text() handle I/O; .rename(), .unlink(), and .mkdir() manage "
            "the file system. All operations are cross-platform without manual "
            "os.sep handling.\n\n"
            "subprocess.run() executes external commands and captures their output. "
            "Always pass a list of strings (not a shell string), set check=True to "
            "raise on non-zero exit codes, and capture output with "
            "capture_output=True, text=True. Use shell=True only when you genuinely "
            "need shell features — it introduces injection risks.\n\n"
            "For data science automation, common patterns include: daily download of "
            "fresh data from an API, batch conversion of data formats, automatic "
            "generation of summary reports, and archiving processed files. A "
            "well-written automation script should be idempotent — safe to run twice "
            "— and log what it does so failures are diagnosable."
        ),
        key_terms={
            "pathlib.Path": "Cross-platform object-oriented file system path — the modern os.path replacement.",
            "Path.glob()": "Yields paths matching a shell-style wildcard pattern (e.g. '*.csv').",
            "subprocess.run()": "Runs an external command; returns CompletedProcess with returncode and output.",
            "shutil": "Standard-library module for file copying, moving, and archiving operations.",
            "Idempotent": "A script that produces the same result whether run once or many times.",
            "schedule": "Third-party library for running functions on a time interval inside a Python process.",
        },
        code_examples=[
            CodeExample(
                title="Batch rename files with pathlib",
                code="""from pathlib import Path

data_dir = Path("data/raw")
for csv_file in data_dir.glob("report_*.csv"):
    new_name = csv_file.stem.replace("report_", "processed_") + csv_file.suffix
    dest = csv_file.with_name(new_name)
    csv_file.rename(dest)
    print(f"Renamed: {csv_file.name} -> {dest.name}")""",
                explanation=(
                    "glob() selects matching files; stem and suffix decompose the name; "
                    "rename() moves the file in place."
                ),
                output="Renamed: report_jan.csv -> processed_jan.csv\nRenamed: report_feb.csv -> processed_feb.csv",
                line_notes={
                    3: "[bold]Path()[/bold] creates a path object — works identically on Windows, macOS, Linux.",
                    4: "glob('*.csv') yields only files matching the shell pattern in that directory.",
                    5: ".stem is the filename without extension; .suffix is the extension including the dot.",
                    7: "[bold]rename()[/bold] moves the file — use shutil.copy2() to copy instead.",
                },
            ),
            CodeExample(
                title="Running a shell command with subprocess",
                code="""import subprocess
from pathlib import Path

input_file = Path("data.csv")
output_file = Path("data.parquet")

result = subprocess.run(
    ["python3", "-c",
     f"import pandas as pd; pd.read_csv('{input_file}').to_parquet('{output_file}')"],
    capture_output=True,
    text=True,
    check=True,
)
print("Converted successfully")
print(result.stdout)""",
                explanation=(
                    "subprocess.run() with check=True raises CalledProcessError on "
                    "failure. capture_output=True captures stdout and stderr."
                ),
                output="Converted successfully\n",
                line_notes={
                    7: "Pass a [bold]list of strings[/bold], not a shell string — avoids injection.",
                    10: "capture_output=True collects stdout and stderr instead of printing to the terminal.",
                    11: "text=True decodes output as UTF-8 strings; default is bytes.",
                    12: "[bold]check=True[/bold] raises CalledProcessError if the command exits non-zero.",
                },
            ),
        ],
        common_mistakes=[
            "Using os.path instead of pathlib.Path — pathlib is more readable and fully cross-platform.",
            "Passing a shell string to subprocess.run() without shell=True — it won't be parsed correctly.",
            "Forgetting check=True and silently ignoring a failed subprocess call.",
            "Writing scripts that fail if run twice — always check if the output already exists first.",
        ],
        practice_prompts=[
            "How would you write a script that archives all CSV files older than 30 days into a zip file?",
            "How would you make a data-download script idempotent — skipping files already downloaded?",
            "When would you use pathlib.rglob() instead of glob()?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which pathlib method yields files matching a wildcard pattern like '*.csv'?",
                qtype="fill_blank",
                correct_answer="glob",
                explanation="Path.glob('*.csv') yields all CSV files in the directory.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="subprocess.run() with shell=True is the safest way to run external commands.",
                qtype="true_false",
                correct_answer="false",
                explanation="shell=True introduces injection risks; pass a list of strings without shell=True instead.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which subprocess.run() parameter raises an exception automatically on non-zero exit codes?",
                qtype="multiple_choice",
                correct_answer="check=True",
                options=["capture_output=True", "check=True", "text=True", "timeout=30"],
                explanation="check=True raises CalledProcessError if the command returns a non-zero exit code.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What does it mean for an automation script to be idempotent?",
                qtype="short_answer",
                correct_answer="It produces the same result whether run once or multiple times, without duplicate work or errors on re-runs.",
                keywords=["same", "multiple"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a15-ex",
            title="List Python Files",
            instructions=(
                "Write a function list_py_files(directory) that uses pathlib to "
                "return a sorted list of all .py filenames (name only, not full path) "
                "found directly inside the given directory. Test with Path('.')."
            ),
            starter_code=(
                "from pathlib import Path\n\n"
                "def list_py_files(directory):\n"
                "    ...\n\n"
                "files = list_py_files(Path('.'))\n"
                "for f in files:\n"
                "    print(f)"
            ),
            expected_output="(varies by directory — should print .py filenames sorted alphabetically)",
            hints=[
                "Use Path(directory).glob('*.py') to find .py files.",
                "Use .name to get just the filename (not the full path).",
                "Wrap in sorted() to sort alphabetically.",
                "Return a list: return sorted(p.name for p in Path(directory).glob('*.py'))",
            ],
            solution=(
                "from pathlib import Path\n\n"
                "def list_py_files(directory):\n"
                "    return sorted(p.name for p in Path(directory).glob('*.py'))\n\n"
                "files = list_py_files(Path('.'))\n"
                "for f in files:\n"
                "    print(f)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a16
    Lesson(
        id="a16",
        title="Basic Data Analysis with pandas",
        level=Level.ADVANCED,
        estimated_minutes=25,
        explanation=(
            "pandas is the foundational library for tabular data in Python. A "
            "DataFrame is a two-dimensional table with labelled columns; a Series is "
            "a single labelled column. Together they provide SQL-like operations — "
            "filter, group, join, pivot — plus I/O for CSV, Parquet, Excel, JSON, "
            "and SQL databases.\n\n"
            "The core mental model: operations on DataFrames produce new DataFrames "
            "rather than mutating in place (by default). Chain operations for "
            "readable pipelines: df.dropna().query('price > 0').groupby('category')."
            "mean(). Use vectorised operations (df['col'] * 2) instead of Python "
            "loops — pandas delegates to NumPy C code, which is orders of magnitude "
            "faster.\n\n"
            "Common data-cleaning steps before any analysis: handle missing values "
            "with .fillna() or .dropna(); convert dtypes with .astype(); parse dates "
            "with pd.to_datetime(); rename columns with .rename(); deduplicate with "
            ".drop_duplicates(). Always inspect with .info(), .describe(), and "
            ".head() before diving into analysis.\n\n"
            "For a Master's in Data Science, pandas fluency is non-negotiable. "
            "Groupby aggregations, merge/join, pivot tables, rolling windows, and "
            "apply/lambda transforms are all exam and interview fundamentals. "
            "Understanding when to switch from pandas to polars (large data) or "
            "PySpark (distributed) is equally important."
        ),
        key_terms={
            "DataFrame": "Two-dimensional labelled table — the central pandas data structure.",
            "Series": "One-dimensional labelled array; a single DataFrame column is a Series.",
            "groupby()": "Splits data into groups by one or more columns, then aggregates.",
            "merge()": "Joins two DataFrames on a key column — analogous to SQL JOIN.",
            "vectorised operation": "Applying arithmetic/functions to an entire column at once via NumPy.",
            "pd.to_datetime()": "Parses string or numeric columns into a DatetimeSeries.",
        },
        code_examples=[
            CodeExample(
                title="Load, inspect, and clean a dataset",
                code="""import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"])
print(df.shape)
print(df.dtypes)
print(df.head(3))

df = df.dropna(subset=["revenue"])
df = df[df["revenue"] > 0]
df["month"] = df["date"].dt.to_period("M")
print(df.describe())""",
                explanation=(
                    "Standard data-loading sequence: read → inspect shape and dtypes "
                    "→ remove nulls and invalid rows → engineer features."
                ),
                output="(1200, 5)\ndate       datetime64[ns]\nrevenue       float64\n...",
                line_notes={
                    3: "[bold]parse_dates=[/bold] automatically converts the 'date' column to datetime.",
                    4: "shape returns (rows, columns) — always check this first to confirm the load.",
                    8: "dropna with subset= removes only rows where 'revenue' is NaN.",
                    10: ".dt accessor unlocks datetime properties — to_period('M') groups by month.",
                },
            ),
            CodeExample(
                title="Groupby aggregation and pivot",
                code="""import pandas as pd

data = {
    "category": ["A", "B", "A", "B", "A"],
    "month":    ["Jan", "Jan", "Feb", "Feb", "Jan"],
    "sales":    [100, 200, 150, 250, 120],
}
df = pd.DataFrame(data)

summary = (
    df.groupby(["category", "month"])["sales"]
    .agg(["sum", "mean", "count"])
    .reset_index()
)
print(summary)

pivot = df.pivot_table(
    values="sales", index="category", columns="month", aggfunc="sum"
)
print(pivot)""",
                explanation=(
                    "groupby + agg produces a multi-stat summary. pivot_table "
                    "reshapes it into a category × month matrix — a common "
                    "analysis output for dashboards and reports."
                ),
                output="  category month  sum   mean  count\n0        A   Feb  150  150.0      1\n...",
                line_notes={
                    10: "Chain groupby → agg → reset_index for a clean flat summary table.",
                    11: "agg(['sum','mean','count']) computes multiple statistics in one pass.",
                    16: "pivot_table is the pandas equivalent of a spreadsheet pivot — reshapes aggregated data.",
                },
            ),
            CodeExample(
                title="Merging DataFrames",
                code="""import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3],
    "product_id": [101, 102, 101],
    "qty": [2, 1, 3],
})
products = pd.DataFrame({
    "product_id": [101, 102],
    "name": ["Widget", "Gadget"],
    "price": [9.99, 24.50],
})

result = orders.merge(products, on="product_id", how="left")
result["total"] = result["qty"] * result["price"]
print(result[["order_id", "name", "total"]])""",
                explanation=(
                    "left join keeps all orders even if the product is missing. "
                    "Vectorised multiplication computes totals without a loop."
                ),
                output="   order_id    name  total\n0         1  Widget  19.98\n1         2  Gadget  24.50\n2         3  Widget  29.97",
                line_notes={
                    13: "[bold]merge()[/bold] joins on 'product_id'; how='left' keeps all rows from orders.",
                    14: "Vectorised: multiplies entire columns at once — no Python loop needed.",
                    15: "Select only the columns needed for the final output.",
                },
            ),
        ],
        common_mistakes=[
            "Using iterrows() to loop over a DataFrame — always prefer vectorised operations or apply().",
            "Modifying a slice of a DataFrame and getting SettingWithCopyWarning — use .loc[] or .copy().",
            "Not resetting the index after groupby + reset_index, leaving a MultiIndex that confuses later operations.",
            "Forgetting that pd.read_csv() reads all numeric-looking columns as floats — check dtypes immediately.",
        ],
        practice_prompts=[
            "How would you calculate a 7-day rolling average of daily sales using pandas?",
            "What is the difference between merge() and concat() in pandas?",
            "How would you detect and handle outliers in a numeric column programmatically?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which pandas method removes rows where specified columns contain NaN values?",
                qtype="fill_blank",
                correct_answer="dropna",
                explanation="df.dropna(subset=['col']) removes rows where 'col' is NaN.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Iterating over a DataFrame with iterrows() is the recommended way to apply a function to each row.",
                qtype="true_false",
                correct_answer="false",
                explanation="iterrows() is very slow; use vectorised operations, apply(), or numpy functions instead.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which pandas function joins two DataFrames on a common column, like a SQL JOIN?",
                qtype="multiple_choice",
                correct_answer="merge()",
                options=["concat()", "merge()", "join()", "append()"],
                explanation="df.merge(other, on='key') performs an inner join by default; use how= to change join type.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Explain the difference between df.groupby('col').mean() and df.pivot_table().",
                qtype="short_answer",
                correct_answer="groupby returns a flat aggregated Series/DataFrame; pivot_table reshapes the result into a 2D matrix with one variable on rows and another on columns.",
                keywords=["pivot", "reshape"],
                difficulty="hard",
            ),
        ],
        mini_exercise=Exercise(
            id="a16-ex",
            title="Sales Summary",
            instructions=(
                "Given the sales DataFrame below, compute the total revenue per "
                "region using groupby and print the result sorted by revenue descending."
            ),
            starter_code=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({\n"
                "    'region': ['North', 'South', 'North', 'East', 'South'],\n"
                "    'revenue': [1200, 800, 950, 1100, 700],\n"
                "})\n\n"
                "# compute total revenue per region, sorted descending"
            ),
            expected_output="region\nNorth    2150\nEast     1100\nSouth    1500\ndtype: int64",
            hints=[
                "Use df.groupby('region')['revenue'].sum()",
                "Chain .sort_values(ascending=False) to sort.",
                "print() the result directly.",
            ],
            solution=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({\n"
                "    'region': ['North', 'South', 'North', 'East', 'South'],\n"
                "    'revenue': [1200, 800, 950, 1100, 700],\n"
                "})\n\n"
                "result = df.groupby('region')['revenue'].sum().sort_values(ascending=False)\n"
                "print(result)"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a17
    Lesson(
        id="a17",
        title="Basic Plotting with matplotlib",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation=(
            "matplotlib is the foundational plotting library in Python's data science "
            "stack. Most other visualization libraries (seaborn, pandas .plot(), "
            "plotly's static export) either wrap matplotlib or mimic its API. "
            "Understanding matplotlib's object model unlocks precise control over "
            "every chart element.\n\n"
            "The two interfaces: pyplot (plt.*) is the stateful MATLAB-style API "
            "convenient for quick exploratory plots. The object-oriented interface "
            "uses explicit Figure and Axes objects — preferred for production code "
            "because it is explicit and composable. fig, ax = plt.subplots() is the "
            "standard OO entry point.\n\n"
            "An Axes object represents one subplot. You call ax.plot(), ax.bar(), "
            "ax.scatter(), ax.hist() etc. on it, then customise with ax.set_title(), "
            "ax.set_xlabel(), ax.set_ylabel(), ax.legend(), and ax.grid(). Multiple "
            "subplots share a Figure: fig, axes = plt.subplots(1, 2) gives two axes.\n\n"
            "For data science, the most important chart types are: line plots for "
            "time series, scatter plots for correlation, histograms and KDE for "
            "distributions, and bar charts for categorical comparisons. seaborn "
            "builds higher-level statistical plots (boxplot, heatmap, pairplot) on "
            "top of matplotlib and integrates directly with pandas DataFrames."
        ),
        key_terms={
            "Figure": "The top-level container — the entire canvas; created by plt.figure() or plt.subplots().",
            "Axes": "A single plot area within a Figure; the object you call plot/bar/scatter on.",
            "plt.subplots()": "Creates a Figure and one or more Axes; returns (fig, ax) or (fig, axes).",
            "ax.set_()": "Family of methods to set title, labels, limits, and ticks on an Axes.",
            "plt.savefig()": "Saves the current Figure to a file; supports PNG, PDF, SVG.",
            "seaborn": "High-level statistical visualization library built on matplotlib.",
        },
        code_examples=[
            CodeExample(
                title="Line plot of a time series",
                code="""import matplotlib.pyplot as plt
import pandas as pd

dates = pd.date_range("2024-01", periods=12, freq="ME")
sales = [120, 135, 128, 145, 160, 175, 168, 182, 195, 210, 225, 240]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(dates, sales, marker="o", linewidth=2, color="steelblue", label="Monthly Sales")
ax.set_title("Monthly Sales 2024", fontsize=14)
ax.set_xlabel("Month")
ax.set_ylabel("Units Sold")
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("sales_trend.png", dpi=150)
plt.show()""",
                explanation=(
                    "Object-oriented interface: fig and ax are explicit. "
                    "tight_layout() prevents label clipping; savefig() before show()."
                ),
                output="(saves sales_trend.png)",
                line_notes={
                    7: "[bold]plt.subplots()[/bold] returns (Figure, Axes) — always unpack both.",
                    8: "marker='o' adds data point markers; all style kwargs are optional.",
                    12: "alpha=0.3 makes the gridlines subtle — doesn't compete with the data.",
                    14: "[bold]tight_layout()[/bold] auto-adjusts spacing to prevent label overlap.",
                    15: "Call savefig [bold]before[/bold] show() — show() clears the figure.",
                },
            ),
            CodeExample(
                title="Subplots: histogram and scatter side by side",
                code="""import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
x = rng.normal(0, 1, 300)
y = 2 * x + rng.normal(0, 0.5, 300)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.hist(x, bins=20, color="coral", edgecolor="white")
ax1.set_title("Distribution of X")
ax1.set_xlabel("Value")
ax1.set_ylabel("Frequency")

ax2.scatter(x, y, alpha=0.4, s=20, color="steelblue")
ax2.set_title("X vs Y")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")

plt.tight_layout()
plt.savefig("analysis.png", dpi=150)""",
                explanation=(
                    "plt.subplots(1, 2) creates one row of two axes. "
                    "Unpack into separate variables for clear code."
                ),
                output="(saves analysis.png)",
                line_notes={
                    8: "subplots(1, 2) returns a Figure and an array of 2 Axes — unpack directly.",
                    10: "bins= controls histogram granularity; edgecolor separates bars visually.",
                    14: "alpha=0.4 helps visualise overplotted points in a dense scatter.",
                },
            ),
        ],
        common_mistakes=[
            "Calling plt.show() before plt.savefig() — show() clears the figure, saving a blank image.",
            "Using the pyplot stateful API (plt.plot()) inside functions that may be called multiple times — use OO interface instead.",
            "Forgetting plt.tight_layout() — axis labels often overlap with adjacent subplots.",
            "Not setting dpi when saving — default is 72, which looks blurry when embedded in documents.",
        ],
        practice_prompts=[
            "How would you plot two lines on the same Axes with a legend distinguishing them?",
            "When would you use seaborn instead of raw matplotlib for a data science report?",
            "How do you set axis limits to zoom in on a specific data range?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which matplotlib function creates a Figure and one or more Axes simultaneously?",
                qtype="fill_blank",
                correct_answer="plt.subplots",
                explanation="fig, ax = plt.subplots() is the standard OO entry point for matplotlib.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="plt.savefig() should be called after plt.show() to save the figure.",
                qtype="true_false",
                correct_answer="false",
                explanation="plt.show() clears the figure; always call savefig() BEFORE show().",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which Axes method adds a title to a single subplot?",
                qtype="multiple_choice",
                correct_answer="ax.set_title()",
                options=["ax.title()", "ax.set_title()", "plt.title()", "ax.add_title()"],
                explanation="ax.set_title('My Title') sets the title on the specific Axes object.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="What is the difference between the pyplot stateful API and the object-oriented API in matplotlib?",
                qtype="short_answer",
                correct_answer="The pyplot API (plt.*) implicitly tracks the 'current' figure/axes; the OO API uses explicit fig and ax objects, which is clearer in functions and multi-subplot code.",
                keywords=["explicit", "ax"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a17-ex",
            title="Bar Chart of Category Counts",
            instructions=(
                "Create a bar chart showing the count of each category in the list "
                "below. Use the OO interface (fig, ax = plt.subplots()), set a title "
                "and axis labels, and save to 'categories.png'."
            ),
            starter_code=(
                "import matplotlib.pyplot as plt\n"
                "from collections import Counter\n\n"
                "data = ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'C', 'B', 'A']\n"
                "counts = Counter(data)\n\n"
                "# create bar chart with fig, ax interface"
            ),
            expected_output="(saves categories.png with bars for A=4, B=3, C=3)",
            hints=[
                "Use fig, ax = plt.subplots()",
                "ax.bar(counts.keys(), counts.values())",
                "Set title and axis labels with ax.set_title(), ax.set_xlabel(), ax.set_ylabel()",
                "Call plt.savefig('categories.png') then plt.show()",
            ],
            solution=(
                "import matplotlib.pyplot as plt\n"
                "from collections import Counter\n\n"
                "data = ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'C', 'B', 'A']\n"
                "counts = Counter(data)\n\n"
                "fig, ax = plt.subplots()\n"
                "ax.bar(counts.keys(), counts.values(), color='steelblue')\n"
                "ax.set_title('Category Counts')\n"
                "ax.set_xlabel('Category')\n"
                "ax.set_ylabel('Count')\n"
                "plt.tight_layout()\n"
                "plt.savefig('categories.png', dpi=150)\n"
                "plt.show()"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a18
    Lesson(
        id="a18",
        title="Software Architecture Basics",
        level=Level.ADVANCED,
        estimated_minutes=20,
        explanation=(
            "Software architecture is the set of high-level decisions that shape how "
            "a system is structured: which components exist, how they communicate, "
            "and what their responsibilities are. Good architecture is not about "
            "following a trendy pattern — it is about making the system easy to "
            "understand, test, extend, and maintain over time.\n\n"
            "Separation of concerns is the foundational principle: each module or "
            "class should have one clear job. Three-layer architecture — presentation "
            "(UI/CLI), business logic (domain rules), persistence (database/files) — "
            "is the classic expression. Code that mixes database queries with "
            "rendering logic is hard to test and hard to change independently.\n\n"
            "Design patterns are named solutions to recurring problems. The most "
            "important for Python developers are: Repository (abstracts data access), "
            "Service (encapsulates a business operation), Factory (creates objects "
            "without exposing instantiation logic), and Observer (notifies listeners "
            "of state changes). Patterns are vocabulary — not mandatory templates.\n\n"
            "For data science systems, think about the data pipeline architecture "
            "separately: ingestion (fetch/scrape) → storage (SQLite/S3) → processing "
            "(pandas/Spark) → modelling (scikit-learn) → serving (API/CLI). Keeping "
            "each stage as an independent, testable unit makes the whole pipeline "
            "reproducible and debuggable."
        ),
        key_terms={
            "Separation of concerns": "Each module/class has one clearly defined responsibility.",
            "Three-layer architecture": "Presentation, business logic, and persistence as separate layers.",
            "Dependency injection": "Providing dependencies (DB, API client) to a class rather than creating them inside it.",
            "Repository pattern": "An abstraction layer over data access that hides storage details from business logic.",
            "Coupling": "The degree to which two modules depend on each other; low coupling is desirable.",
            "Cohesion": "How closely related the responsibilities within a single module are; high cohesion is desirable.",
        },
        code_examples=[
            CodeExample(
                title="Three-layer separation",
                code="""# persistence layer
class SensorRepo:
    def __init__(self, connection):
        self.con = connection

    def get_recent(self, limit=100):
        cur = self.con.execute(
            "SELECT sensor, value, ts FROM readings ORDER BY ts DESC LIMIT ?",
            (limit,)
        )
        return cur.fetchall()

# business logic layer
class SensorService:
    def __init__(self, repo: SensorRepo):
        self.repo = repo

    def average_by_sensor(self):
        rows = self.repo.get_recent()
        from collections import defaultdict
        totals, counts = defaultdict(float), defaultdict(int)
        for sensor, value, _ in rows:
            totals[sensor] += value
            counts[sensor] += 1
        return {s: totals[s] / counts[s] for s in totals}

# presentation layer
def print_averages(service: SensorService):
    for sensor, avg in service.average_by_sensor().items():
        print(f"{sensor}: {avg:.2f}")""",
                explanation=(
                    "Three classes, three responsibilities. SensorService does not "
                    "know how data is stored; SensorRepo does not know how results "
                    "are displayed. Each layer is independently testable."
                ),
                output="temp_01: 22.75\ntemp_02: 19.80",
                line_notes={
                    2: "Repository hides all SQL — swap it for a file reader or HTTP client without touching service logic.",
                    13: "SensorService receives its dependency (repo) — [bold]dependency injection[/bold].",
                    14: "Typed hint makes the dependency explicit and IDE-friendly.",
                    24: "Presentation layer only knows about the service interface — not the DB.",
                },
            ),
            CodeExample(
                title="Factory function for flexible object creation",
                code="""def create_storage(backend: str, **kwargs):
    if backend == "sqlite":
        import sqlite3
        return sqlite3.connect(kwargs.get("path", ":memory:"))
    elif backend == "csv":
        from pathlib import Path
        return Path(kwargs.get("path", "data.csv"))
    else:
        raise ValueError(f"Unknown backend: {backend}")

db = create_storage("sqlite", path="sensors.db")
print(type(db))""",
                explanation=(
                    "The factory pattern encapsulates object creation logic. "
                    "Callers request a 'sqlite' or 'csv' backend without knowing "
                    "the import or constructor details."
                ),
                output="<class 'sqlite3.Connection'>",
                line_notes={
                    1: "Factory function: takes a name/config, returns a concrete object.",
                    8: "Raising ValueError for unknown backends fails fast with a clear message.",
                    10: "Caller code is decoupled from the concrete type — swap 'sqlite' for 'csv' freely.",
                },
            ),
        ],
        common_mistakes=[
            "Putting database calls directly in request handlers or CLI commands — mixing persistence with presentation.",
            "Over-engineering: applying complex patterns (Abstract Factory, Mediator) to a 50-line script.",
            "Hardcoding dependencies inside classes instead of injecting them — makes unit testing impossible.",
            "Ignoring architecture until the codebase is too large to refactor — add structure as soon as you have two layers.",
        ],
        practice_prompts=[
            "How would you restructure a 500-line analytics script into a layered architecture?",
            "What is the difference between low coupling and high cohesion, and why do you want both?",
            "How does dependency injection make a class easier to unit test?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which architectural principle states that each class or module should have one clearly defined job?",
                qtype="multiple_choice",
                correct_answer="Separation of concerns",
                options=["DRY (Don't Repeat Yourself)", "Separation of concerns", "YAGNI", "Open/Closed Principle"],
                explanation="Separation of concerns splits a system into distinct sections, each addressing one aspect.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Dependency injection means creating dependencies (DB connections, API clients) inside the class that uses them.",
                qtype="true_false",
                correct_answer="false",
                explanation="Dependency injection means PROVIDING dependencies from outside the class, not creating them internally.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="An abstraction layer over data access that hides storage details from business logic is called the ___ pattern.",
                qtype="fill_blank",
                correct_answer="Repository",
                explanation="The Repository pattern keeps storage technology details out of business logic.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Why is low coupling between modules desirable in a software system?",
                qtype="short_answer",
                correct_answer="Low coupling means modules can be changed, tested, or replaced independently without cascading changes throughout the codebase.",
                keywords=["independent", "change"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a18-ex",
            title="Inject the Dependency",
            instructions=(
                "Refactor the DataLoader class below so that it accepts a 'fetcher' "
                "callable as a constructor argument instead of hardcoding requests.get. "
                "Write a fake_fetcher for testing that returns a fixed dict, and show "
                "that DataLoader works with the fake."
            ),
            starter_code=(
                "# Original (tightly coupled):\n"
                "# class DataLoader:\n"
                "#     def load(self, url):\n"
                "#         import requests\n"
                "#         return requests.get(url).json()\n\n"
                "class DataLoader:\n"
                "    def __init__(self, fetcher):\n"
                "        ...\n\n"
                "    def load(self, url):\n"
                "        ...\n\n"
                "def fake_fetcher(url):\n"
                "    return {'status': 'ok', 'url': url}\n\n"
                "loader = DataLoader(fake_fetcher)\n"
                "print(loader.load('https://example.com'))"
            ),
            expected_output="{'status': 'ok', 'url': 'https://example.com'}",
            hints=[
                "Store the fetcher in self.fetcher inside __init__.",
                "In load(), call self.fetcher(url) and return the result.",
            ],
            solution=(
                "class DataLoader:\n"
                "    def __init__(self, fetcher):\n"
                "        self.fetcher = fetcher\n\n"
                "    def load(self, url):\n"
                "        return self.fetcher(url)\n\n"
                "def fake_fetcher(url):\n"
                "    return {'status': 'ok', 'url': url}\n\n"
                "loader = DataLoader(fake_fetcher)\n"
                "print(loader.load('https://example.com'))"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    # ------------------------------------------------------------------ a19
    Lesson(
        id="a19",
        title="Clean Code Principles",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation=(
            "Clean code is code that is easy to read, understand, and change. "
            "It is not about perfect abstraction or minimal line count — it is about "
            "communicating intent clearly to the next reader (often your future self). "
            "Most of the principles in Robert Martin's 'Clean Code' apply directly "
            "to Python: meaningful names, small focused functions, and no surprises.\n\n"
            "Meaningful names are the highest-leverage clean-code practice. A good "
            "name answers what a variable holds, what a function does, and why. "
            "Avoid single-letter variables outside of mathematical loops; avoid "
            "abbreviations that are not universally known; avoid generic names like "
            "data, result, or temp. Rename freely — modern IDEs make it instant.\n\n"
            "Functions should do one thing. If a function's name contains 'and', it "
            "probably does two things. Keep functions short (roughly 10–20 lines), "
            "avoid deeply nested conditionals, and use guard clauses (early return) "
            "to flatten nesting. Magic numbers and strings belong in named constants "
            "at the top of the module, not embedded in logic.\n\n"
            "Pythonic code follows PEP 8 and PEP 20 (import this). Use list "
            "comprehensions instead of map/filter, prefer explicit over implicit, "
            "and write code that is easy to test. Tools like ruff (linting + "
            "formatting) and mypy (type checking) enforce these standards "
            "automatically — run them in CI so code quality is a team baseline, "
            "not an individual habit."
        ),
        key_terms={
            "PEP 8": "Python's official style guide: naming, indentation, line length, imports.",
            "Guard clause": "An early return/raise at the top of a function that handles edge cases, flattening nested ifs.",
            "Magic number": "A bare numeric or string literal in logic code; should be a named constant.",
            "Single responsibility": "A function or class should have exactly one reason to change.",
            "DRY": "Don't Repeat Yourself — extract duplicated logic into a shared function or constant.",
            "ruff": "Fast Python linter and formatter that enforces PEP 8 and catches common errors.",
        },
        code_examples=[
            CodeExample(
                title="Before and after: meaningful names and guard clauses",
                code="""# BEFORE: unclear names, deep nesting
def proc(d, t):
    r = []
    for x in d:
        if x > 0:
            if x < t:
                r.append(x * 1.1)
    return r

# AFTER: clear names, guard clauses, constant
TAX_RATE = 1.1

def apply_tax_to_valid_prices(prices, price_cap):
    taxed = []
    for price in prices:
        if price <= 0:
            continue
        if price >= price_cap:
            continue
        taxed.append(price * TAX_RATE)
    return taxed

print(apply_tax_to_valid_prices([10, -5, 200, 50], price_cap=100))""",
                explanation=(
                    "Guard clauses (early continue) eliminate nesting. "
                    "TAX_RATE is a named constant, not a magic number. "
                    "The function name explains exactly what it does."
                ),
                output="[11.0, 55.00000000000001]",
                line_notes={
                    2: "proc, d, t, x, r — none of these names convey any meaning.",
                    11: "Named constant at module level — one place to update the tax rate.",
                    13: "Function name is a full sentence describing the transformation.",
                    15: "Guard clause: skip invalid prices early rather than nesting the happy path.",
                },
            ),
            CodeExample(
                title="DRY: extract duplicated logic",
                code="""# BEFORE: duplicated validation
def save_user(name, email):
    if not name or len(name) < 2:
        raise ValueError("Invalid name")
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    print(f"Saving user: {name}, {email}")

def update_user(name, email):
    if not name or len(name) < 2:
        raise ValueError("Invalid name")
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    print(f"Updating user: {name}, {email}")

# AFTER: single validation function
def _validate_user_inputs(name, email):
    if not name or len(name) < 2:
        raise ValueError("Invalid name")
    if not email or "@" not in email:
        raise ValueError("Invalid email")

def save_user(name, email):
    _validate_user_inputs(name, email)
    print(f"Saving user: {name}, {email}")

def update_user(name, email):
    _validate_user_inputs(name, email)
    print(f"Updating user: {name}, {email}")

save_user("Alice", "alice@example.com")""",
                explanation=(
                    "Duplicated validation is extracted into one place. "
                    "Bug fixes and rule changes now only need to happen once."
                ),
                output="Saving user: Alice, alice@example.com",
                line_notes={
                    2: "BEFORE: validation duplicated in every function that needs it.",
                    16: "AFTER: extract to a private helper (leading underscore = internal use).",
                    22: "save_user is now 2 lines — easy to read, easy to test.",
                },
            ),
        ],
        common_mistakes=[
            "Commenting what the code does instead of why — good names make 'what' comments redundant.",
            "Writing one giant function because 'it's all related' — split on the responsibility boundary.",
            "Leaving magic numbers (0.1, 86400, 'admin') embedded in logic — always name them.",
            "Skipping linting because 'it's just style' — automated formatting removes entire categories of code review debates.",
        ],
        practice_prompts=[
            "Look at a function you wrote recently — does its name tell you exactly what it does without reading the body?",
            "Find a place in your code where the same logic appears twice and refactor it into a shared helper.",
            "How would you configure ruff as a pre-commit hook to enforce style automatically?",
        ],
        quiz_questions=[
            QuizQuestion(
                question="A 'guard clause' is an early ___ or raise at the top of a function that handles edge cases.",
                qtype="fill_blank",
                correct_answer="return",
                explanation="Guard clauses handle the exceptional/edge cases first with early returns, keeping the happy path flat.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Adding comments that describe what each line of code does is a hallmark of clean code.",
                qtype="true_false",
                correct_answer="false",
                explanation="Clean code is self-documenting through good names. What-comments mean the names are not clear enough.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="The principle 'Don't Repeat Yourself' is abbreviated as ___.",
                qtype="fill_blank",
                correct_answer="DRY",
                explanation="DRY: every piece of knowledge should have a single, authoritative representation.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which of these is a fast Python linter and formatter that enforces PEP 8?",
                qtype="multiple_choice",
                correct_answer="ruff",
                options=["pylint", "ruff", "black", "flake8"],
                explanation="ruff is a modern Rust-based linter + formatter that replaces pylint, flake8, and isort together.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What makes a function name 'clean' according to the single responsibility principle?",
                qtype="short_answer",
                correct_answer="It describes exactly one action the function performs, without 'and' joining two responsibilities, and can be read without looking at the function body.",
                keywords=["one", "action"],
                difficulty="medium",
            ),
        ],
        mini_exercise=Exercise(
            id="a19-ex",
            title="Refactor for Clarity",
            instructions=(
                "Refactor the function below to use a meaningful name, replace the "
                "magic numbers with named constants, and use a guard clause to remove "
                "nesting. The function filters a list of scores, discarding those "
                "outside the range [60, 100], and adds a 5-point bonus."
            ),
            starter_code=(
                "def f(lst):\n"
                "    r = []\n"
                "    for x in lst:\n"
                "        if x >= 60:\n"
                "            if x <= 100:\n"
                "                r.append(x + 5)\n"
                "    return r\n\n"
                "print(f([55, 70, 95, 105, 80]))"
            ),
            expected_output="[75, 100, 85]",
            hints=[
                "Name the constants: MIN_PASSING_SCORE = 60, MAX_SCORE = 100, BONUS = 5",
                "Name the function: apply_bonus_to_passing_scores(scores)",
                "Use 'if score < MIN_PASSING_SCORE: continue' as a guard clause.",
                "Add a second guard for score > MAX_SCORE.",
            ],
            solution=(
                "MIN_PASSING_SCORE = 60\n"
                "MAX_SCORE = 100\n"
                "BONUS = 5\n\n"
                "def apply_bonus_to_passing_scores(scores):\n"
                "    adjusted = []\n"
                "    for score in scores:\n"
                "        if score < MIN_PASSING_SCORE:\n"
                "            continue\n"
                "        if score > MAX_SCORE:\n"
                "            continue\n"
                "        adjusted.append(score + BONUS)\n"
                "    return adjusted\n\n"
                "print(apply_bonus_to_passing_scores([55, 70, 95, 105, 80]))"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
]
