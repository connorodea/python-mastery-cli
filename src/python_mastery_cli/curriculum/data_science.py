from __future__ import annotations

from ..models import CodeExample, Exercise, Lesson, Level, QuizQuestion

DATA_SCIENCE_LESSONS: list[Lesson] = [
    Lesson(
        id="a20",
        title="NumPy Arrays and Vectorization",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation="""NumPy is the foundation of the entire Python data-science stack. pandas,
scikit-learn, and most deep-learning libraries all store their numbers in NumPy
arrays under the hood. The core object is the ``ndarray``: a fixed-size,
homogeneous (single-dtype) block of memory. Because every element shares the same
type and the data is packed contiguously, NumPy can hand whole arrays off to fast,
pre-compiled C loops instead of interpreting one Python object at a time.

That last point is what "vectorization" means. Writing ``a + b`` on two arrays adds
every pair of elements in a tight C loop — no Python-level ``for`` loop, no per-element
boxing/unboxing. For numeric work this is often 10-100x faster than the equivalent
Python loop, and it reads more like the math you are trying to express. The rule of
thumb in data science is: if you find yourself writing a Python loop over array
elements, there is almost always a vectorized NumPy expression that is both faster
and clearer.

NumPy also gives you *broadcasting* (operating on arrays of different but compatible
shapes without copying data), *boolean masks* (selecting elements with a condition),
and *axis-aware aggregations* (``sum``/``mean``/``std`` that collapse along a chosen
dimension). Together these let you describe a transformation of an entire dataset as
one expression. Learn the array, the dtype, and the shape first — everything else in
pandas builds directly on them.""",
        key_terms={
            "ndarray": "NumPy's core N-dimensional array: fixed size, single dtype, contiguous memory.",
            "dtype": "The data type of every element in an array, e.g. int64 or float64.",
            "shape": "A tuple giving the size of the array along each axis, e.g. (3, 4).",
            "vectorization": "Applying an operation to a whole array in compiled C code instead of a Python loop.",
            "broadcasting": "Rules that let NumPy combine arrays of compatible-but-different shapes without copying.",
            "axis": "The dimension an aggregation collapses; axis=0 walks down columns, axis=1 across rows.",
        },
        code_examples=[
            CodeExample(
                title="Vectorized arithmetic beats a Python loop",
                code="""
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])
print(a + b)
print(a * 2)
print(a.dtype, a.shape)
""",
                explanation="One expression adds all four pairs in compiled code — no Python loop needed.",
                output="[11 22 33 44]\n[2 4 6 8]\nint64 (4,)",
                line_notes={
                    1: "Import NumPy with the universal alias np.",
                    3: "np.array turns a Python list into a homogeneous ndarray.",
                    5: "Element-wise addition: a[i] + b[i] for every i, in C.",
                    6: "Scalar 2 is broadcast against every element of a.",
                    7: "Every array carries a dtype and a shape tuple.",
                },
            ),
            CodeExample(
                title="Boolean masks and axis-aware aggregation",
                code="""
import numpy as np

grades = np.array([[85, 90, 78],
                   [60, 72, 88]])
print(grades.mean())          # mean of all 6 values
print(grades.mean(axis=0))    # column means (per subject)
print(grades.mean(axis=1))    # row means (per student)
passing = grades[grades >= 80]
print(passing)
""",
                explanation="axis= chooses which dimension to collapse; a boolean mask selects elements.",
                output="78.83333333333333\n[72.5 81.  83. ]\n[84.33333333 73.33333333]\n[85 90 88]",
            ),
        ],
        common_mistakes=[
            "Looping element-by-element in Python when a vectorized expression would be faster and clearer.",
            "Forgetting that NumPy arrays are homogeneous — mixing types silently upcasts everything (e.g. ints become floats or objects).",
            "Confusing axis=0 (down the rows, per column) with axis=1 (across the columns, per row).",
            "Assuming a slice is a copy — NumPy slices are views, so writing into them mutates the original array.",
        ],
        practice_prompts=[
            "Create a 1D array of 10 numbers and compute its mean, std, min, and max without any loops.",
            "Build a 3x4 array and take both the per-row and per-column sums using the axis argument.",
            "Given an array of temperatures, use a boolean mask to select only the values above the average.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Why is a vectorized NumPy expression typically much faster than a Python for-loop over the same data?",
                qtype="multiple_choice",
                correct_answer="The operation runs in pre-compiled C over contiguous, single-dtype memory instead of the Python interpreter",
                options=[
                    "NumPy secretly uses multiple threads for every operation",
                    "The operation runs in pre-compiled C over contiguous, single-dtype memory instead of the Python interpreter",
                    "Python loops are disabled when NumPy is imported",
                    "Vectorized code uses less memory so it always runs faster",
                ],
                explanation="Homogeneous, contiguous arrays let NumPy push the whole loop into compiled C, avoiding per-element interpreter overhead.",
                difficulty="medium",
                keywords=[],
            ),
            QuizQuestion(
                question="A NumPy ndarray can hold elements of different data types (e.g. ints and strings) in the same array.",
                qtype="true_false",
                correct_answer="false",
                explanation="ndarrays are homogeneous: every element shares one dtype. Mixing types forces an upcast (often to object).",
                difficulty="easy",
            ),
            QuizQuestion(
                question="To get the mean of each COLUMN of a 2D array, call .mean(axis=___).",
                qtype="fill_blank",
                correct_answer="0",
                explanation="axis=0 collapses the row dimension, leaving one mean per column.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="What is broadcasting in NumPy, in one sentence?",
                qtype="short_answer",
                correct_answer="A set of rules that lets NumPy operate on arrays of different but compatible shapes without copying data.",
                explanation="Broadcasting stretches a smaller array across a larger one virtually, so a scalar or row can combine with a full matrix.",
                difficulty="medium",
                keywords=["shape", "without"],
            ),
        ],
        mini_exercise=Exercise(
            id="a20-ex",
            title="Vectorize a price calculation",
            instructions=(
                "You are given a NumPy array of item prices. Apply an 8% sales tax to every "
                "price using a single vectorized expression (no loops), then print the total "
                "of all the tax-inclusive prices. Round the total to 2 decimals."
            ),
            starter_code=(
                "import numpy as np\n\n"
                "prices = np.array([10.0, 25.0, 4.5, 100.0])\n"
                "# TODO: add 8% tax to every price (vectorized), then sum and round to 2 dp\n"
            ),
            expected_output="150.66",
            hints=[
                "Multiply the whole array by 1.08 in one expression — broadcasting handles every element.",
                "Use .sum() to total the array.",
                "round(value, 2) rounds the final scalar to two decimals.",
            ],
            solution=(
                "import numpy as np\n\n"
                "prices = np.array([10.0, 25.0, 4.5, 100.0])\n"
                "with_tax = prices * 1.08\n"
                "print(round(with_tax.sum(), 2))\n"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="a21",
        title="pandas: Series and DataFrames",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation="""If NumPy gives you fast arrays of raw numbers, pandas gives you *labeled* tabular
data — the spreadsheet-shaped objects that almost all real analysis happens on. There
are two core types. A ``Series`` is a one-dimensional array with an attached index
(labels for each value), like a single column. A ``DataFrame`` is a two-dimensional
table: a collection of Series that all share the same row index, like a sheet with named
columns. Selecting one column from a DataFrame hands you back a Series.

You will create DataFrames constantly. The most common patterns are from a dictionary
(keys become column names, values become columns) and from a list of records. Once you
have a DataFrame, your first move on any dataset is always to *look at it*. ``df.head()``
shows the first rows, ``df.shape`` reports ``(rows, columns)``, ``df.columns`` and
``df.dtypes`` tell you the column names and their types, ``df.info()`` summarizes
non-null counts and memory, and ``df.describe()`` gives quick summary statistics for the
numeric columns.

This "look before you leap" habit is the whole reason pandas exists: real data is messy,
and these inspection methods are how you discover that a column you thought was numeric is
actually stored as text, or that 200 of your 1,000 rows are missing. Get fluent with the
Series/DataFrame distinction and these inspection methods now — every later lesson
(filtering, grouping, cleaning, plotting) assumes them.""",
        key_terms={
            "Series": "A 1D labeled array — one column of data plus its index.",
            "DataFrame": "A 2D labeled table: named columns (Series) sharing a common row index.",
            "index": "The row labels of a Series or DataFrame; defaults to 0..n-1 but can be anything.",
            "df.head()": "Returns the first n rows (default 5) for a quick peek.",
            "df.describe()": "Summary statistics (count, mean, std, quartiles) for numeric columns.",
            "df.dtypes": "The data type of each column.",
        },
        code_examples=[
            CodeExample(
                title="Build a DataFrame from a dict and inspect it",
                code="""
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Bo", "Cy"],
    "age": [31, 24, 45],
    "city": ["NYC", "LA", "SF"],
})
print(df.shape)
print(list(df.columns))
print(df["age"].mean())
""",
                explanation="Dict keys become column names; selecting df['age'] returns a Series you can aggregate.",
                output="(3, 3)\n['name', 'age', 'city']\n33.333333333333336",
                line_notes={
                    1: "Import pandas with the universal alias pd.",
                    3: "Each dict key becomes a column; each list is that column's values.",
                    8: "df.shape is a (rows, columns) tuple.",
                    9: "df.columns is an Index of the column names.",
                    10: "df['age'] selects one column as a Series, then .mean() aggregates it.",
                },
            ),
            CodeExample(
                title="A standalone Series carries its own index",
                code="""
import pandas as pd

temps = pd.Series([72, 68, 75], index=["Mon", "Tue", "Wed"], name="temp")
print(temps["Tue"])
print(temps.mean())
""",
                explanation="A Series pairs values with labels, so you can look up by label and still aggregate.",
                output="68\n71.66666666666667",
            ),
        ],
        common_mistakes=[
            "Confusing a Series (one column, 1D) with a DataFrame (whole table, 2D).",
            "Calling df.describe() and assuming it covers every column — by default it only summarizes numeric columns.",
            "Forgetting that df.head() returns a copy for display, not a way to modify the original data.",
            "Treating df.shape like a method — it is an attribute, so use df.shape not df.shape().",
        ],
        practice_prompts=[
            "Create a DataFrame of 3 books with title, author, and pages columns, then print its shape and column names.",
            "Run df.info() and df.describe() on a small DataFrame and explain what each tells you.",
            "Select a single column as a Series and confirm with type() that it is a Series, not a DataFrame.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="What does selecting a single column from a DataFrame with df['col'] return?",
                qtype="multiple_choice",
                correct_answer="A pandas Series",
                options=["A NumPy ndarray", "A pandas Series", "A Python list", "A one-column DataFrame"],
                explanation="Single-bracket single-column access returns a Series; df[['col']] (double brackets) returns a one-column DataFrame.",
                difficulty="medium",
                keywords=[],
            ),
            QuizQuestion(
                question="df.shape returns a tuple in the order (number_of_columns, number_of_rows).",
                qtype="true_false",
                correct_answer="false",
                explanation="It is (rows, columns) — rows first.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The DataFrame method that prints the first n rows (default 5) is df.____().",
                qtype="fill_blank",
                correct_answer="head",
                explanation="df.head() shows the top rows; df.tail() shows the bottom rows.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="In one sentence, what is the difference between a Series and a DataFrame?",
                qtype="short_answer",
                correct_answer="A Series is one labeled column (1D); a DataFrame is a 2D table of multiple columns sharing one row index.",
                explanation="A DataFrame is essentially a dict of Series that all share the same index.",
                difficulty="easy",
                keywords=["column", "table"],
            ),
        ],
        mini_exercise=Exercise(
            id="a21-ex",
            title="Inspect a small sales table",
            instructions=(
                "Build a DataFrame from the given dict of product sales. Print the table's shape, "
                "the list of column names, and the average of the 'units' column. Each on its own line."
            ),
            starter_code=(
                "import pandas as pd\n\n"
                "data = {\n"
                "    'product': ['pen', 'mug', 'notebook'],\n"
                "    'units': [120, 45, 78],\n"
                "    'price': [1.5, 8.0, 4.0],\n"
                "}\n"
                "# TODO: build the DataFrame, then print shape, column names, and mean of 'units'\n"
            ),
            expected_output="(3, 3)\n['product', 'units', 'price']\n81.0",
            hints=[
                "pd.DataFrame(data) builds the table directly from the dict.",
                "df.shape is an attribute (no parentheses); list(df.columns) gives a plain list.",
                "df['units'].mean() averages a single column.",
            ],
            solution=(
                "import pandas as pd\n\n"
                "data = {\n"
                "    'product': ['pen', 'mug', 'notebook'],\n"
                "    'units': [120, 45, 78],\n"
                "    'price': [1.5, 8.0, 4.0],\n"
                "}\n"
                "df = pd.DataFrame(data)\n"
                "print(df.shape)\n"
                "print(list(df.columns))\n"
                "print(df['units'].mean())\n"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="a22",
        title="Selecting, Filtering, and Indexing in pandas",
        level=Level.ADVANCED,
        estimated_minutes=20,
        explanation="""Once you can build a DataFrame, the next skill is pulling out exactly the rows and
columns you want. pandas gives you three doorways, and knowing which to use is the
difference between fluent and frustrated. Plain ``df['col']`` (or ``df[['a', 'b']]``)
selects columns by name. ``df.loc[...]`` selects by *label* — row labels and column
names. ``df.iloc[...]`` selects by *integer position* — like indexing a list. The mental
model: ``loc`` is "what is it called", ``iloc`` is "where is it".

The real workhorse is *boolean filtering*. When you write ``df[df['age'] > 30]``, the
inner expression produces a Series of True/False, one per row, and pandas keeps only the
rows where the mask is True. You can test membership with ``.isin([...])`` and combine
conditions — but here is the single most common beginner trap: you must use the
bitwise operators ``&`` (and), ``|`` (or), ``~`` (not), **not** Python's ``and``/``or``,
and you must wrap each condition in parentheses because ``&`` binds tighter than ``>``.
``df[(df.a > 1) & (df.b < 5)]`` works; dropping the parentheses raises an error.

Selecting rows and columns together is where ``.loc`` shines: ``df.loc[df['age'] > 30,
['name', 'city']]`` reads as "rows where age > 30, just the name and city columns." Master
this row+column selection and you can express most everyday data slicing in a single,
readable line.""",
        key_terms={
            ".loc": "Label-based selection: df.loc[row_labels, column_names].",
            ".iloc": "Integer-position selection: df.iloc[row_positions, column_positions].",
            "boolean mask": "A True/False Series, one per row, used to keep matching rows.",
            ".isin()": "Tests membership of each value against a list of allowed values.",
            "& | ~": "Bitwise and/or/not used to combine boolean masks (NOT Python's and/or).",
            "chained indexing": "df[...][...] in sequence — fragile and may not assign reliably; prefer .loc.",
        },
        code_examples=[
            CodeExample(
                title="Boolean filtering with combined conditions",
                code="""
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Bo", "Cy", "Di"],
    "age": [31, 24, 45, 38],
    "city": ["NYC", "LA", "SF", "NYC"],
})
mask = (df["age"] > 30) & (df["city"] == "NYC")
print(df.loc[mask, ["name", "age"]])
""",
                explanation="Wrap each condition in parentheses and join with & — then .loc picks rows + chosen columns.",
                output="  name  age\n0  Ada   31\n3   Di   38",
                line_notes={
                    8: "Each condition is parenthesised; & combines the two boolean Series.",
                    9: "df.loc[mask, cols] keeps matching rows AND only the listed columns.",
                },
            ),
            CodeExample(
                title="loc vs iloc, and isin",
                code="""
import pandas as pd

df = pd.DataFrame({"x": [10, 20, 30]}, index=["a", "b", "c"])
print(df.loc["b", "x"])     # label-based -> 20
print(df.iloc[0, 0])         # position-based -> 10
print(df[df["x"].isin([10, 30])])
""",
                explanation="loc uses the label 'b'; iloc uses position 0; isin keeps rows whose value is in the list.",
                output="20\n10\n    x\na  10\nc  30",
            ),
        ],
        common_mistakes=[
            "Using Python's `and`/`or` to combine masks — pandas needs the bitwise `&`/`|`.",
            "Forgetting parentheses: `df[df.a > 1 & df.b < 5]` misparses; write `df[(df.a > 1) & (df.b < 5)]`.",
            "Mixing up .loc (labels) and .iloc (integer positions), especially when the index is itself integers.",
            "Relying on chained indexing like df[df.a > 1]['b'] = 0 to assign — use df.loc[df.a > 1, 'b'] = 0 instead.",
        ],
        practice_prompts=[
            "Filter a DataFrame to rows where a numeric column is above its own mean.",
            "Use .isin() to keep only rows whose category is one of three allowed values.",
            "Select the first three rows and the last two columns using a single .iloc call.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which expression correctly keeps rows where age > 30 AND city equals 'NYC'?",
                qtype="multiple_choice",
                correct_answer="df[(df['age'] > 30) & (df['city'] == 'NYC')]",
                options=[
                    "df[df['age'] > 30 and df['city'] == 'NYC']",
                    "df[(df['age'] > 30) & (df['city'] == 'NYC')]",
                    "df[df['age'] > 30 & df['city'] == 'NYC']",
                    "df.loc[df['age'] > 30 or df['city'] == 'NYC']",
                ],
                explanation="Use bitwise & and wrap each condition in parentheses because & binds tighter than the comparisons.",
                difficulty="medium",
                keywords=[],
            ),
            QuizQuestion(
                question=".iloc selects rows and columns by their integer position, not by their labels.",
                qtype="true_false",
                correct_answer="true",
                explanation=".iloc is position-based; .loc is label-based.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="To keep rows whose 'status' value is one of ['open', 'pending'], use df[df['status'].____(['open', 'pending'])].",
                qtype="fill_blank",
                correct_answer="isin",
                explanation=".isin([...]) builds a boolean mask of membership against the given list.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="When should you reach for .loc instead of plain df[...] bracket selection?",
                qtype="short_answer",
                correct_answer="Use .loc when you need to select rows and columns together by label, especially when assigning values, to avoid fragile chained indexing.",
                explanation=".loc selects rows+columns in one call and assigns reliably; chained bracket indexing can silently fail to write back.",
                difficulty="medium",
                keywords=["label", "rows"],
            ),
        ],
        mini_exercise=Exercise(
            id="a22-ex",
            title="Filter high spenders in a city",
            instructions=(
                "From the given DataFrame, select customers who are in 'NYC' AND have spent more "
                "than 100. Print only their 'name' and 'spend' columns using .loc and a combined "
                "boolean mask."
            ),
            starter_code=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({\n"
                "    'name': ['Ada', 'Bo', 'Cy', 'Di'],\n"
                "    'city': ['NYC', 'LA', 'NYC', 'NYC'],\n"
                "    'spend': [150, 200, 80, 130],\n"
                "})\n"
                "# TODO: keep NYC customers spending > 100, show only name and spend\n"
            ),
            expected_output="  name  spend\n0  Ada    150\n3   Di    130",
            hints=[
                "Build the mask as (df['city'] == 'NYC') & (df['spend'] > 100).",
                "Each condition needs its own pair of parentheses.",
                "Pass the mask and the column list to df.loc[mask, ['name', 'spend']].",
            ],
            solution=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({\n"
                "    'name': ['Ada', 'Bo', 'Cy', 'Di'],\n"
                "    'city': ['NYC', 'LA', 'NYC', 'NYC'],\n"
                "    'spend': [150, 200, 80, 130],\n"
                "})\n"
                "mask = (df['city'] == 'NYC') & (df['spend'] > 100)\n"
                "print(df.loc[mask, ['name', 'spend']])\n"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="a23",
        title="GroupBy and Aggregation",
        level=Level.ADVANCED,
        estimated_minutes=20,
        explanation="""Most analytical questions are really "for each group, what is the ___?": average
revenue per region, total orders per customer, max temperature per month. pandas answers
all of these with one idea — *split-apply-combine*. ``df.groupby('region')`` splits the
rows into one bucket per region; you then *apply* an aggregation (mean, sum, count) to
each bucket; pandas *combines* the per-group results back into a tidy table indexed by the
group keys. Once this clicks, a huge class of loop-heavy code collapses into a single
line.

The aggregation step is flexible. ``df.groupby('region')['sales'].mean()`` gives one mean
per region. ``.agg(['mean', 'sum'])`` computes several statistics at once, and you can
even name custom outputs per column with the named-aggregation form. You can group by
*multiple* columns (``groupby(['region', 'product'])``) to get a result indexed by every
combination. For two-dimensional summaries — groups down the rows, a second variable
across the columns — ``pivot_table`` reshapes the same data into a spreadsheet-style
cross-tab. And for a quick "how many of each value?" on a single column, ``value_counts()``
is the fastest path.

The mindset shift to internalize is "don't loop, group." Whenever you catch yourself
writing a ``for`` loop that maintains running totals in a dictionary keyed by some
category, stop — that is a groupby. The grouped version is faster, far less error-prone,
and reads like the question you were trying to answer.""",
        key_terms={
            "groupby": "Splits rows into groups by one or more key columns for per-group aggregation.",
            "split-apply-combine": "The pattern: split into groups, apply a function to each, combine the results.",
            ".agg()": "Applies one or more aggregation functions to each group.",
            "pivot_table": "Reshapes data into a cross-tab: groups on rows, another variable on columns.",
            "value_counts()": "Counts occurrences of each unique value in a Series, sorted by frequency.",
            "aggregation": "A function that reduces many values to one, e.g. sum, mean, count, max.",
        },
        code_examples=[
            CodeExample(
                title="Group and aggregate in one line",
                code="""
import pandas as pd

df = pd.DataFrame({
    "region": ["E", "W", "E", "W", "E"],
    "sales": [100, 200, 150, 50, 120],
})
print(df.groupby("region")["sales"].sum())
""",
                explanation="Split rows by region, sum sales within each, combine into a region-indexed Series.",
                output="region\nE    370\nW    250\nName: sales, dtype: int64",
                line_notes={
                    7: "groupby('region') splits the rows; ['sales'].sum() applies+combines per group.",
                },
            ),
            CodeExample(
                title="Multiple aggregations and value_counts",
                code="""
import pandas as pd

df = pd.DataFrame({
    "team": ["A", "B", "A", "B", "A"],
    "pts": [10, 7, 12, 9, 8],
})
print(df.groupby("team")["pts"].agg(["mean", "max"]))
print(df["team"].value_counts())
""",
                explanation=".agg(list) computes several stats per group; value_counts tallies each unique team.",
                output="      mean  max\nteam            \nA     10.0   12\nB      8.0    9\nteam\nA    3\nB    2\nName: count, dtype: int64",
            ),
        ],
        common_mistakes=[
            "Writing a manual for-loop with a running-totals dict instead of a single groupby.",
            "Forgetting to select a column after groupby — df.groupby('k').mean() aggregates every numeric column, which may not be what you want.",
            "Expecting the group keys as regular columns — they become the index; call .reset_index() if you need them back as columns.",
            "Confusing value_counts() (counts of each value in one column) with groupby().count() (non-null counts per group).",
        ],
        practice_prompts=[
            "Group a sales DataFrame by region and compute the mean, max, and count of sales per region in one .agg() call.",
            "Group by two columns (region and product) and total the revenue for each combination.",
            "Use value_counts() to find the three most common values in a categorical column.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="The pandas pattern behind groupby is best summarized as:",
                qtype="multiple_choice",
                correct_answer="split-apply-combine",
                options=["map-reduce-filter", "split-apply-combine", "fetch-join-sort", "scan-index-merge"],
                explanation="Rows are split into groups, an aggregation is applied to each, and the results are combined.",
                difficulty="easy",
                keywords=[],
            ),
            QuizQuestion(
                question="After df.groupby('region')['sales'].sum(), the region values become the index of the result, not a regular column.",
                qtype="true_false",
                correct_answer="true",
                explanation="Group keys become the index; use .reset_index() to turn them back into columns.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="To compute both the mean and the max of a grouped column at once, pass a list to df.groupby('k')['v'].____(['mean', 'max']).",
                qtype="fill_blank",
                correct_answer="agg",
                explanation=".agg(list_of_functions) applies several aggregations per group.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Explain the 'don't loop, group' mindset in one or two sentences.",
                qtype="short_answer",
                correct_answer="When you would write a loop accumulating per-category totals, use groupby instead — it is faster, less error-prone, and reads like the question.",
                explanation="Per-group accumulation is exactly what split-apply-combine does in compiled, vectorized code.",
                difficulty="medium",
                keywords=["groupby", "loop"],
            ),
        ],
        mini_exercise=Exercise(
            id="a23-ex",
            title="Total revenue per category",
            instructions=(
                "Given a DataFrame of orders, group by 'category' and compute the TOTAL 'revenue' "
                "for each category. Print the resulting Series (category-indexed)."
            ),
            starter_code=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({\n"
                "    'category': ['books', 'toys', 'books', 'toys', 'books'],\n"
                "    'revenue': [30, 50, 20, 10, 40],\n"
                "})\n"
                "# TODO: group by category and sum revenue\n"
            ),
            expected_output="category\nbooks    90\ntoys     60\nName: revenue, dtype: int64",
            hints=[
                "Start with df.groupby('category').",
                "Select the 'revenue' column after grouping.",
                "Call .sum() to combine each group's revenue.",
            ],
            solution=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({\n"
                "    'category': ['books', 'toys', 'books', 'toys', 'books'],\n"
                "    'revenue': [30, 50, 20, 10, 40],\n"
                "})\n"
                "print(df.groupby('category')['revenue'].sum())\n"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="a24",
        title="Cleaning Messy, Real-World Data",
        level=Level.ADVANCED,
        estimated_minutes=22,
        explanation="""Real datasets are messy: missing values, columns stored as the wrong type, duplicate
rows, and text with stray whitespace or inconsistent casing. Data scientists routinely
spend the majority of a project just cleaning. The good news is that pandas has a compact,
well-worn toolkit for each problem, and a reliable loop to follow: *load, inspect, clean,
validate* — then repeat until the data is trustworthy.

Missing data shows up as ``NaN``. ``df.isna()`` flags it, ``df.isna().sum()`` counts it per
column, ``df.dropna()`` removes rows (or columns) that contain it, and ``df.fillna(value)``
substitutes a chosen value (a constant, the column mean, forward-fill, etc.). Choosing
between dropping and filling is a judgment call: dropping loses data, filling invents it —
pick based on how much is missing and why.

Wrong types are the second big category. A column of numbers stored as strings can't be
summed correctly, so you convert with ``.astype(int)``, ``pd.to_numeric(...,
errors='coerce')`` (turning bad values into NaN), or ``pd.to_datetime`` for dates.
Duplicates are found with ``df.duplicated()`` and removed with ``df.drop_duplicates()``.
And messy text is tamed with the vectorized string accessor: ``df['name'].str.strip()``
trims whitespace, ``.str.lower()`` normalizes case. Run the load-inspect-clean-validate
loop on every dataset before you trust a single statistic from it.""",
        key_terms={
            "NaN": "'Not a Number' — pandas' marker for a missing value.",
            ".isna()": "Returns a boolean mask of where values are missing.",
            ".fillna()": "Replaces missing values with a chosen constant or strategy.",
            ".astype()": "Converts a column to a different dtype, e.g. .astype(int).",
            "pd.to_numeric": "Parses a column to numbers; errors='coerce' turns bad entries into NaN.",
            ".str accessor": "Vectorized string methods on a Series, e.g. .str.strip(), .str.lower().",
        },
        code_examples=[
            CodeExample(
                title="Count and fill missing values",
                code="""
import pandas as pd
import numpy as np

df = pd.DataFrame({"score": [10.0, np.nan, 30.0, np.nan]})
print(df["score"].isna().sum())
df["score"] = df["score"].fillna(df["score"].mean())
print(df["score"].tolist())
""",
                explanation="Count the NaNs, then replace them with the column mean so no rows are lost.",
                output="2\n[10.0, 20.0, 30.0, 20.0]",
                line_notes={
                    4: "Construct a column with two missing values (np.nan).",
                    5: ".isna().sum() counts how many values are missing.",
                    6: "fillna replaces each NaN with the mean of the present values.",
                    7: ".tolist() shows the cleaned column as a plain list.",
                },
            ),
            CodeExample(
                title="Fix dtypes, drop duplicates, clean strings",
                code="""
import pandas as pd

df = pd.DataFrame({
    "qty": ["5", "7", "5"],
    "name": [" Ada ", "Bo", " Ada "],
})
df["qty"] = pd.to_numeric(df["qty"])
df["name"] = df["name"].str.strip().str.lower()
df = df.drop_duplicates()
print(df.to_dict("records"))
""",
                explanation="Convert text-numbers to ints, trim+lowercase names, then drop the now-identical duplicate row.",
                output="[{'qty': 5, 'name': 'ada'}, {'qty': 7, 'name': 'bo'}]",
            ),
        ],
        common_mistakes=[
            "Filling NaN with 0 by reflex when 0 changes the meaning (e.g. an unknown price is not a free price).",
            "Calling df.dropna() and forgetting it returns a new DataFrame — reassign it or pass inplace, or your data is unchanged.",
            "Using .astype(int) on a column that still contains NaN, which raises — coerce or fill first.",
            "Comparing strings without normalizing whitespace/case, so ' Ada ' and 'ada' look like different values.",
        ],
        practice_prompts=[
            "Load a small DataFrame with some NaNs and report the missing-value count per column.",
            "Convert a column of numeric strings to integers, coercing any unparseable values to NaN.",
            "Strip and lowercase a name column, then drop the duplicate rows that result.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which method replaces missing values with a chosen value rather than removing them?",
                qtype="multiple_choice",
                correct_answer="df.fillna(value)",
                options=["df.dropna()", "df.fillna(value)", "df.isna()", "df.drop_duplicates()"],
                explanation="fillna substitutes; dropna removes; isna only flags; drop_duplicates handles duplicate rows.",
                difficulty="easy",
                keywords=[],
            ),
            QuizQuestion(
                question="pd.to_numeric(col, errors='coerce') turns values it cannot parse into NaN instead of raising an error.",
                qtype="true_false",
                correct_answer="true",
                explanation="errors='coerce' is the safe option for messy numeric columns.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="To trim leading/trailing whitespace from every value in a string column, use df['name'].str.____().",
                qtype="fill_blank",
                correct_answer="strip",
                explanation=".str.strip() applies str.strip element-wise across the Series.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Name the four repeating steps of the data-cleaning loop.",
                qtype="short_answer",
                correct_answer="Load the data, inspect it, clean the problems, and validate the result — then repeat.",
                explanation="Cleaning is iterative: each clean step can reveal new issues, so you re-inspect and re-validate.",
                difficulty="medium",
                keywords=["load", "inspect", "clean", "validate"],
            ),
        ],
        mini_exercise=Exercise(
            id="a24-ex",
            title="Clean a messy ages column",
            instructions=(
                "The 'age' column is stored as strings and has one missing entry (None). Convert it "
                "to numbers (coercing bad values to NaN), fill the missing value with the column mean, "
                "and print the cleaned ages as a list of floats."
            ),
            starter_code=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({'age': ['20', '40', None]})\n"
                "# TODO: to_numeric (coerce), fill NaN with the mean, print as a list\n"
            ),
            expected_output="[20.0, 40.0, 30.0]",
            hints=[
                "pd.to_numeric(df['age'], errors='coerce') turns None/bad entries into NaN.",
                "df['age'].mean() ignores NaN, so it averages only the present values.",
                "Reassign the column, then use .tolist() to print it.",
            ],
            solution=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({'age': ['20', '40', None]})\n"
                "df['age'] = pd.to_numeric(df['age'], errors='coerce')\n"
                "df['age'] = df['age'].fillna(df['age'].mean())\n"
                "print(df['age'].tolist())\n"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="a25",
        title="Loading and Saving Data (CSV and JSON)",
        level=Level.ADVANCED,
        estimated_minutes=18,
        explanation="""Analysis starts with getting data *into* a DataFrame and ends with getting results
*out*. By far the most common formats are CSV (comma-separated text) and JSON, and pandas
reads both in one line: ``pd.read_csv(path)`` and ``pd.read_json(path)``. But real files
are rarely clean, so ``read_csv`` exposes a rich set of parameters that save you from
manual cleanup. Learn them once and you will reach for them constantly.

The most useful ``read_csv`` options: ``sep`` for non-comma delimiters (tabs, semicolons);
``header`` to say which row holds the column names (or ``header=None`` when there are
none); ``na_values`` to declare extra strings that should count as missing (like
``"N/A"`` or ``"-"``); ``parse_dates`` to convert date columns to real datetime objects on
load; and ``usecols`` to read only the columns you need (faster, less memory). pandas can
also read straight from a URL — pass the URL where you would pass a path — which is handy
for public datasets.

Saving is just as direct: ``df.to_csv('out.csv', index=False)``. The ``index=False`` is
almost always what you want — otherwise pandas writes the row index as an extra unnamed
first column that confuses anyone (including future-you) who reads the file back. Watch for
the classic pitfalls: the wrong delimiter producing a single mangled column, dates loaded
as plain strings because you forgot ``parse_dates``, and the phantom index column from
forgetting ``index=False``.""",
        key_terms={
            "pd.read_csv": "Reads a CSV file (or URL) into a DataFrame.",
            "sep": "The delimiter between fields; default is a comma but can be a tab or semicolon.",
            "na_values": "Extra strings that should be treated as missing (NaN) on load.",
            "parse_dates": "List of columns to convert to datetime while reading.",
            "usecols": "Restricts reading to a subset of columns for speed and memory.",
            "index=False": "Tells to_csv not to write the row index as an extra column.",
        },
        code_examples=[
            CodeExample(
                title="Round-trip a DataFrame through CSV",
                code="""
import pandas as pd

df = pd.DataFrame({"name": ["Ada", "Bo"], "score": [90, 75]})
df.to_csv("scores.csv", index=False)
back = pd.read_csv("scores.csv")
print(back.shape)
print(list(back.columns))
""",
                explanation="index=False keeps the file clean; reading it back gives the same 2x2 table.",
                output="(2, 2)\n['name', 'score']",
                line_notes={
                    4: "Write the DataFrame; index=False omits the phantom index column.",
                    5: "Read the same file straight back into a new DataFrame.",
                    6: "Shape confirms we recovered 2 rows and 2 columns.",
                },
            ),
            CodeExample(
                title="read_csv with real-world options",
                code="""
import pandas as pd
from io import StringIO

raw = "id;when;val\\n1;2024-01-01;5\\n2;2024-01-02;NA"
df = pd.read_csv(StringIO(raw), sep=";",
                 na_values=["NA"], parse_dates=["when"])
print(df["when"].dtype)
print(df["val"].isna().sum())
""",
                explanation="sep handles the semicolons, na_values maps 'NA' to NaN, parse_dates makes a real datetime column.",
                output="datetime64[ns]\n1",
            ),
        ],
        common_mistakes=[
            "Forgetting index=False in to_csv, leaving a phantom unnamed index column in the output file.",
            "Using the default comma separator on a semicolon- or tab-delimited file, producing one mangled column.",
            "Loading date columns as plain strings because parse_dates was not specified.",
            "Not declaring placeholder strings ('N/A', '-', 'null') in na_values, so they stay as text instead of NaN.",
        ],
        practice_prompts=[
            "Write a small DataFrame to CSV with index=False and read it back, confirming the shape matches.",
            "Read a semicolon-delimited string with read_csv, parsing a date column and coercing 'NA' to NaN.",
            "Use usecols to read only two named columns from a wider CSV.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Why is df.to_csv('out.csv', index=False) usually preferred over the default?",
                qtype="multiple_choice",
                correct_answer="It avoids writing the row index as an extra unnamed column",
                options=[
                    "It compresses the file automatically",
                    "It avoids writing the row index as an extra unnamed column",
                    "It is the only way to write headers",
                    "It converts all columns to strings",
                ],
                explanation="Without index=False, pandas writes the index as a leading unnamed column that confuses later reads.",
                difficulty="easy",
                keywords=[],
            ),
            QuizQuestion(
                question="pd.read_csv can read directly from a URL, not just a local file path.",
                qtype="true_false",
                correct_answer="true",
                explanation="Pass an http(s) URL exactly where you would pass a file path.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="To convert date columns to real datetime objects while reading, pass the ____ parameter to read_csv.",
                qtype="fill_blank",
                correct_answer="parse_dates",
                explanation="parse_dates=['col'] parses those columns into datetime64 on load.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="Which read_csv parameter would you use to treat the string 'N/A' as a missing value?",
                qtype="short_answer",
                correct_answer="na_values — e.g. pd.read_csv(path, na_values=['N/A']) maps that string to NaN.",
                explanation="na_values declares extra tokens that should be parsed as missing on load.",
                difficulty="medium",
                keywords=["na_values"],
            ),
        ],
        mini_exercise=Exercise(
            id="a25-ex",
            title="Save and reload a table",
            instructions=(
                "Create the given DataFrame, save it to 'people.csv' WITHOUT the index, read it back "
                "into a new variable, and print the reloaded DataFrame's shape."
            ),
            starter_code=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({'name': ['Ada', 'Bo', 'Cy'], 'age': [31, 24, 45]})\n"
                "# TODO: save to people.csv with index=False, read it back, print the shape\n"
            ),
            expected_output="(3, 2)",
            hints=[
                "df.to_csv('people.csv', index=False) writes the file without the index column.",
                "pd.read_csv('people.csv') reads it back into a new DataFrame.",
                "Print the .shape attribute of the reloaded DataFrame.",
            ],
            solution=(
                "import pandas as pd\n\n"
                "df = pd.DataFrame({'name': ['Ada', 'Bo', 'Cy'], 'age': [31, 24, 45]})\n"
                "df.to_csv('people.csv', index=False)\n"
                "back = pd.read_csv('people.csv')\n"
                "print(back.shape)\n"
            ),
            difficulty="easy",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="a26",
        title="Descriptive Statistics and Distributions",
        level=Level.ADVANCED,
        estimated_minutes=22,
        explanation="""Before any model or chart, you summarize. Descriptive statistics compress a column of
numbers into a few that capture its shape. *Central tendency* answers "what's typical":
the **mean** (average, sensitive to outliers), the **median** (middle value, robust to
outliers), and the **mode** (most frequent). *Spread* answers "how varied": the
**variance** and its square root the **standard deviation**, plus **quantiles** and
**percentiles** (the median is the 50th percentile; quartiles cut the data into fourths).
Whenever a mean and median diverge sharply, suspect skew or outliers.

*Relationships* between two numeric variables are summarized by **correlation**.
``df.corr()`` returns a matrix of correlation coefficients from -1 (perfect inverse) to +1
(perfect direct), with 0 meaning no linear relationship. This is also where you must burn
in the discipline that **correlation is not causation** — two variables can move together
because one causes the other, because a third factor drives both, or by pure coincidence.

It also helps to recognize *distributions*. A **normal** (bell-curve) distribution
clusters symmetrically around its mean; a **uniform** distribution spreads values evenly.
Many statistical tools assume roughly normal data. Finally, a first taste of *inference*:
a hypothesis test like ``scipy.stats.ttest_ind`` compares two groups' means and returns a
**p-value** — roughly, the probability of seeing a difference this large if the groups
were truly identical. A small p-value (commonly < 0.05) means the difference is unlikely to
be pure chance; it does **not** prove your hypothesis or measure effect size.""",
        key_terms={
            "mean": "The arithmetic average; pulled toward outliers.",
            "median": "The middle value (50th percentile); robust to outliers.",
            "standard deviation": "Typical distance of values from the mean; the square root of variance.",
            "percentile": "The value below which a given percentage of data falls (e.g. 90th percentile).",
            "correlation": "A -1 to +1 measure of how linearly two variables move together.",
            "p-value": "Probability of an observed (or larger) difference if the null hypothesis were true.",
        },
        code_examples=[
            CodeExample(
                title="Central tendency and spread",
                code="""
import pandas as pd

s = pd.Series([2, 4, 4, 4, 5, 5, 7, 9])
print(round(s.mean(), 2))
print(s.median())
print(round(s.std(), 2))
print(s.quantile(0.25), s.quantile(0.75))
""",
                explanation="Mean, median, std, and quartiles summarize where the data sits and how spread out it is.",
                output="5.0\n4.5\n2.0\n4.0 5.25",
                line_notes={
                    4: "Series.mean() is the arithmetic average.",
                    5: ".median() is the middle value, robust to outliers.",
                    6: ".std() measures typical spread around the mean.",
                    7: "Quantiles 0.25 and 0.75 are the lower and upper quartiles.",
                },
            ),
            CodeExample(
                title="Correlation and a two-group t-test",
                code="""
import pandas as pd
from scipy import stats

df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [2, 4, 6, 8]})
print(df.corr().loc["x", "y"])
a, b = [20, 21, 19, 22], [30, 31, 29, 33]
t, p = stats.ttest_ind(a, b)
print(p < 0.05)
""",
                explanation="x and y move together perfectly (corr 1.0); the tiny p-value flags a real group difference.",
                output="1.0\nTrue",
            ),
        ],
        common_mistakes=[
            "Reporting only the mean for skewed data — the median is often the more honest 'typical' value.",
            "Reading a strong correlation as proof of causation; a hidden third variable or coincidence is common.",
            "Treating a p-value as the probability the hypothesis is true, or as a measure of effect size — it is neither.",
            "Assuming data is normally distributed without plotting it first, then applying tools that require normality.",
        ],
        practice_prompts=[
            "Compute the mean, median, std, and the 10th and 90th percentiles of a numeric Series.",
            "Build a small DataFrame and print its correlation matrix; identify the strongest pair.",
            "Run scipy.stats.ttest_ind on two sample lists and interpret whether the p-value suggests a real difference.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which statistic is most robust to extreme outliers?",
                qtype="multiple_choice",
                correct_answer="The median",
                options=["The mean", "The median", "The standard deviation", "The variance"],
                explanation="The median only depends on the middle value(s), so a few extreme outliers barely move it.",
                difficulty="medium",
                keywords=[],
            ),
            QuizQuestion(
                question="A correlation coefficient of 0.95 between two variables proves that one variable causes the other.",
                qtype="true_false",
                correct_answer="false",
                explanation="Correlation is not causation — a third factor or coincidence can produce a high correlation.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="The DataFrame method that returns a matrix of pairwise correlation coefficients is df.____().",
                qtype="fill_blank",
                correct_answer="corr",
                explanation="df.corr() gives a square matrix of correlations between numeric columns.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="In plain language, what does a p-value tell you?",
                qtype="short_answer",
                correct_answer="It is the probability of seeing a difference at least this large if there were really no difference (the null hypothesis were true); a small p-value means chance is an unlikely explanation.",
                explanation="A p-value measures surprise under the null hypothesis; it is not the probability the hypothesis is true and says nothing about effect size.",
                difficulty="hard",
                keywords=["probability", "chance"],
            ),
        ],
        mini_exercise=Exercise(
            id="a26-ex",
            title="Summarize a data column",
            instructions=(
                "Given a Series of test scores, print its mean (rounded to 1 decimal), its median, "
                "and its standard deviation (rounded to 2 decimals), each on its own line."
            ),
            starter_code=(
                "import pandas as pd\n\n"
                "scores = pd.Series([70, 80, 80, 90, 100])\n"
                "# TODO: print mean (1 dp), median, and std (2 dp)\n"
            ),
            expected_output="84.0\n80.0\n11.4",
            hints=[
                "scores.mean(), scores.median(), and scores.std() give the three statistics.",
                "Wrap the mean and std in round(value, ndigits).",
                "pandas .std() uses the sample standard deviation by default.",
            ],
            solution=(
                "import pandas as pd\n\n"
                "scores = pd.Series([70, 80, 80, 90, 100])\n"
                "print(round(scores.mean(), 1))\n"
                "print(scores.median())\n"
                "print(round(scores.std(), 2))\n"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
    Lesson(
        id="a27",
        title="Data Visualization with matplotlib and seaborn",
        level=Level.ADVANCED,
        estimated_minutes=20,
        explanation="""A good chart turns a column of numbers into an insight in seconds, and Python's two
go-to libraries are matplotlib (the foundational plotting engine) and seaborn (a
higher-level layer that makes attractive statistical charts in one call). matplotlib's
``pyplot`` interface — imported as ``plt`` — covers the essentials: ``plt.plot`` for line
charts (trends over an ordered axis), ``plt.scatter`` for relationships between two
numeric variables, ``plt.bar`` for comparing categories, and ``plt.hist`` for the
distribution of one variable. Every chart should carry context: ``plt.xlabel``,
``plt.ylabel``, and ``plt.title`` so a reader knows what they are looking at.

It pays to understand matplotlib's *figure/axes* model. The **figure** is the whole canvas;
the **axes** is a single plot inside it. ``fig, ax = plt.subplots()`` gives you both
explicitly, which is the cleaner way to build multi-panel figures and to control each
plot precisely — most production code uses this object-oriented style rather than the
bare ``plt`` calls.

seaborn sits on top and shines for statistical views: ``histplot`` for distributions (often
with a smooth density curve), ``boxplot`` for spread and outliers across categories,
``heatmap`` for visualizing a matrix such as a correlation table, and ``pairplot`` for
all pairwise scatter relationships at once. The skill that separates good analysts is
*choosing the right chart*: line for trends over time, scatter for correlation, bar for
category comparison, histogram/box for distribution. When you want to keep a figure, save
it with ``plt.savefig('chart.png', dpi=150)`` instead of (or before) calling
``plt.show``.""",
        key_terms={
            "pyplot (plt)": "matplotlib's main plotting interface, conventionally imported as plt.",
            "figure": "The entire canvas that holds one or more plots.",
            "axes": "A single plot region within a figure; where data is actually drawn.",
            "histogram": "A chart of how values of one variable are distributed across bins.",
            "heatmap": "A grid where color encodes magnitude, ideal for correlation matrices.",
            "plt.savefig": "Writes the current figure to an image file (e.g. PNG) on disk.",
        },
        code_examples=[
            CodeExample(
                title="A labeled line chart saved to disk",
                code="""
import matplotlib.pyplot as plt

months = [1, 2, 3, 4]
sales = [100, 130, 90, 160]
fig, ax = plt.subplots()
ax.plot(months, sales)
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.set_title("Monthly Sales")
fig.savefig("sales.png", dpi=150)
""",
                explanation="The object-oriented style: build a figure+axes, draw, label every axis, then save the image.",
                output="",
                line_notes={
                    5: "subplots() returns the figure (canvas) and one axes (plot).",
                    6: "ax.plot draws a line connecting the (month, sales) points.",
                    7: "Always label axes so the chart is self-explanatory.",
                    10: "savefig writes the figure to a PNG instead of showing it.",
                },
            ),
            CodeExample(
                title="A seaborn histogram and a correlation heatmap",
                code="""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 4, 6, 8]})
sns.histplot(df["a"], bins=4)
plt.figure()
sns.heatmap(df.corr(), annot=True)
plt.savefig("corr.png")
""",
                explanation="histplot shows one variable's distribution; heatmap renders the correlation matrix with annotations.",
                output="",
            ),
        ],
        common_mistakes=[
            "Shipping a chart with no title or axis labels, leaving readers to guess what it shows.",
            "Calling plt.savefig AFTER plt.show — show clears the figure, so the saved file ends up blank.",
            "Using a line chart for unordered categories; lines imply a meaningful order, so use a bar chart instead.",
            "Drawing a histogram to compare categories (use bar) or a bar chart to show a distribution (use histogram).",
        ],
        practice_prompts=[
            "Plot a line chart of a value over time with a title and labeled x/y axes, then save it as a PNG.",
            "Make a seaborn histogram of a numeric column and describe the distribution's shape.",
            "Build a correlation matrix with df.corr() and visualize it as an annotated seaborn heatmap.",
        ],
        quiz_questions=[
            QuizQuestion(
                question="Which chart type is the best default for showing the relationship between two numeric variables?",
                qtype="multiple_choice",
                correct_answer="A scatter plot",
                options=["A line chart", "A scatter plot", "A pie chart", "A bar chart"],
                explanation="A scatter plot places one variable on each axis, revealing correlation and clusters.",
                difficulty="easy",
                keywords=[],
            ),
            QuizQuestion(
                question="In matplotlib, the figure is a single plot region and the axes is the whole canvas that contains it.",
                qtype="true_false",
                correct_answer="false",
                explanation="It is the reverse: the figure is the whole canvas; an axes is one plot inside it.",
                difficulty="medium",
            ),
            QuizQuestion(
                question="To write the current matplotlib figure to a PNG file, call plt.____('chart.png').",
                qtype="fill_blank",
                correct_answer="savefig",
                explanation="plt.savefig(path) saves the figure; do it before plt.show() clears it.",
                difficulty="easy",
            ),
            QuizQuestion(
                question="Which seaborn function best visualizes a correlation matrix, and why?",
                qtype="short_answer",
                correct_answer="seaborn heatmap, because it encodes each cell's correlation value as a color so patterns across the matrix are visible at a glance.",
                explanation="A heatmap maps magnitude to color, making a grid of correlations easy to scan.",
                difficulty="medium",
                keywords=["heatmap"],
            ),
        ],
        mini_exercise=Exercise(
            id="a27-ex",
            title="Build a labeled bar chart",
            instructions=(
                "Using matplotlib, draw a bar chart comparing units sold per product. Label the x-axis "
                "'Product', the y-axis 'Units', give it the title 'Units Sold', and save it to "
                "'units.png'. (No printed output is expected — the deliverable is the saved figure.)"
            ),
            starter_code=(
                "import matplotlib.pyplot as plt\n\n"
                "products = ['pen', 'mug', 'book']\n"
                "units = [120, 45, 78]\n"
                "# TODO: bar chart with labels, a title, saved to units.png\n"
            ),
            expected_output="",
            hints=[
                "fig, ax = plt.subplots() gives you a figure and an axes to draw on.",
                "ax.bar(products, units) draws the bars; ax.set_xlabel / set_ylabel / set_title add context.",
                "fig.savefig('units.png') writes the image to disk.",
            ],
            solution=(
                "import matplotlib.pyplot as plt\n\n"
                "products = ['pen', 'mug', 'book']\n"
                "units = [120, 45, 78]\n"
                "fig, ax = plt.subplots()\n"
                "ax.bar(products, units)\n"
                "ax.set_xlabel('Product')\n"
                "ax.set_ylabel('Units')\n"
                "ax.set_title('Units Sold')\n"
                "fig.savefig('units.png')\n"
            ),
            difficulty="medium",
        ),
        next_lesson_id=None,
    ),
]
