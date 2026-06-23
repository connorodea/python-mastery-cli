from __future__ import annotations

from ..models import Project

PROJECTS: list[Project] = [
    Project(
        id="p01",
        title="Build a Calculator CLI",
        difficulty="easy",
        concepts=["functions", "input/output", "conditionals", "error handling"],
        requirements=[
            "Prompt the user for two numbers and an operator (+, -, *, /).",
            "Compute and print the result.",
            "Handle division by zero gracefully with a clear error message.",
            "Loop until the user types 'q' to quit.",
        ],
        build_guide=[
            "Create a calculate(a, op, b) function that handles +, -, *, /.",
            "Read input with input() and convert number strings with float().",
            "Use if/elif to dispatch on the operator string.",
            "Guard against division by zero before performing division.",
            "Wrap everything in a while True loop that breaks when the user types 'q'.",
            "Wrap the conversion and dispatch in a try/except to catch bad input.",
        ],
        starter_code='''\
def calculate(a: float, op: str, b: float) -> float:
    # TODO: implement +, -, *, /
    # Raise ZeroDivisionError for division by zero
    # Raise ValueError for unknown operator
    ...


def main() -> None:
    print("Simple Calculator  (type q to quit)")
    while True:
        raw = input("> a op b: ").strip()
        # TODO: handle quit, parse input, call calculate, print result
        ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "calculate() returns correct results for all four operators.",
            "Division by zero prints a friendly message instead of crashing.",
            "The REPL loop quits cleanly on 'q' and recovers from bad input.",
        ],
        stretch_goals=[
            "Add exponentiation (**) and modulo (%) operators.",
            "Keep a session history and print it when the user types 'history'.",
            "Support chained expressions like '3 + 4 * 2' using eval() safely.",
        ],
        solution='''\
def calculate(a: float, op: str, b: float) -> float:
    """Apply binary operator op to a and b."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
    raise ValueError(f"Unknown operator: {op!r}")


def main() -> None:
    print("Simple Calculator  (type q to quit)")
    while True:
        raw = input("> a op b: ").strip()
        if raw.lower() == "q":
            print("Goodbye!")
            break
        try:
            parts = raw.split()
            if len(parts) != 3:
                raise ValueError("Expected: number operator number")
            a, op, b = parts
            result = calculate(float(a), op, float(b))
            print(f"  = {result}")
        except ZeroDivisionError as exc:
            print(f"  Error: {exc}")
        except ValueError as exc:
            print(f"  Error: {exc}  (example: 3 + 4)")


if __name__ == "__main__":
    main()
''',
        estimated_minutes=45,
    ),

    Project(
        id="p02",
        title="Build a File Organizer",
        difficulty="easy",
        concepts=["pathlib", "file I/O", "dictionaries", "loops", "conditionals"],
        requirements=[
            "Accept a target directory path from the command line (or prompt for one).",
            "Scan all files in the directory (non-recursively).",
            "Move each file into a subdirectory named after its extension (e.g. 'pdf/', 'jpg/').",
            "Skip subdirectories — only move files.",
            "Print a summary of how many files were moved per extension.",
            "Do not overwrite existing files — append a counter suffix if a name clash exists.",
        ],
        build_guide=[
            "Use pathlib.Path to accept and validate the target directory.",
            "Iterate with Path.iterdir() and filter with p.is_file().",
            "Build a mapping of extension → destination subfolder (create with mkdir if needed).",
            "Move files with Path.rename(); resolve name clashes before renaming.",
            "Track a counter dict {ext: count} for the summary.",
            "Print the summary table at the end.",
            "Test with a small scratch folder before pointing at real files.",
        ],
        starter_code='''\
import sys
from pathlib import Path


def get_destination(file: Path, base_dir: Path) -> Path:
    """Return the destination path for file, creating the subfolder if needed."""
    ext = file.suffix.lower().lstrip(".") or "no_extension"
    # TODO: build subfolder path, create it, return destination path
    ...


def safe_move(src: Path, dst: Path) -> Path:
    """Move src to dst, appending _1, _2 … to avoid overwriting."""
    # TODO: if dst exists, find a free name with a counter suffix
    ...


def organise(directory: Path) -> dict[str, int]:
    """Move files into extension subfolders; return {ext: count}."""
    counts: dict[str, int] = {}
    for item in directory.iterdir():
        # TODO: skip non-files, move files, update counts
        pass
    return counts


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(input("Directory: "))
    # TODO: validate path, call organise, print summary
''',
        milestones=[
            "Script correctly identifies all files and their extensions.",
            "Files move into the right subfolders without overwriting anything.",
            "Summary is printed and the counts are accurate.",
        ],
        stretch_goals=[
            "Add a --dry-run flag that prints what would happen without moving anything.",
            "Support recursive scanning of nested subdirectories.",
            "Let the user supply a custom extension→folder mapping via a JSON config file.",
        ],
        solution='''\
import sys
from pathlib import Path


def get_destination_folder(file: Path, base_dir: Path) -> Path:
    ext = file.suffix.lower().lstrip(".") or "no_extension"
    folder = base_dir / ext
    folder.mkdir(exist_ok=True)
    return folder


def safe_move(src: Path, dst_folder: Path) -> Path:
    dst = dst_folder / src.name
    if dst.exists():
        stem, suffix = src.stem, src.suffix
        counter = 1
        while dst.exists():
            dst = dst_folder / f"{stem}_{counter}{suffix}"
            counter += 1
    src.rename(dst)
    return dst


def organise(directory: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in directory.iterdir():
        if not item.is_file():
            continue
        folder = get_destination_folder(item, directory)
        safe_move(item, folder)
        ext = item.suffix.lower().lstrip(".") or "no_extension"
        counts[ext] = counts.get(ext, 0) + 1
    return counts


def main() -> None:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path(input("Target directory: ").strip())

    if not path.is_dir():
        print(f"Error: {path!r} is not a directory.")
        sys.exit(1)

    counts = organise(path)
    if not counts:
        print("No files found to organise.")
        return
    print(f"\\nOrganised {sum(counts.values())} file(s):")
    for ext, n in sorted(counts.items()):
        print(f"  .{ext:<15} {n} file(s)")


if __name__ == "__main__":
    main()
''',
        estimated_minutes=60,
    ),

    Project(
        id="p03",
        title="Build a To-Do List CLI",
        difficulty="easy",
        concepts=["lists", "dictionaries", "JSON persistence", "argparse", "CRUD operations"],
        requirements=[
            "Support add, list, complete, and delete commands via argparse subcommands.",
            "Persist tasks between runs by saving to a JSON file (~/.todo.json).",
            "Each task has an id, description, done flag, and created timestamp.",
            "list command shows all tasks with their id, status ([ ] / [x]), and description.",
            "complete <id> marks a task done; delete <id> removes it.",
            "Auto-increment task IDs (never reuse a deleted ID).",
        ],
        build_guide=[
            "Set up argparse with subparsers: add, list, complete, delete.",
            "Define load_tasks() and save_tasks() using json.load / json.dump on ~/.todo.json.",
            "On 'add', append a new dict with a next_id, description, done=False, and an ISO timestamp.",
            "On 'list', iterate tasks and print formatted rows.",
            "On 'complete', find the task by id and set done=True.",
            "On 'delete', filter the task out by id.",
            "Store next_id alongside the task list so IDs never repeat.",
        ],
        starter_code='''\
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

TODO_FILE = Path.home() / ".todo.json"


def load_data() -> dict:
    """Return {"next_id": int, "tasks": list[dict]}."""
    # TODO: load from TODO_FILE, return default if missing
    ...


def save_data(data: dict) -> None:
    # TODO: write data to TODO_FILE as pretty JSON
    ...


def cmd_add(args: argparse.Namespace) -> None:
    # TODO: create task, append to data, save
    ...


def cmd_list(args: argparse.Namespace) -> None:
    # TODO: print all tasks
    ...


def cmd_complete(args: argparse.Namespace) -> None:
    # TODO: find task by id, mark done, save
    ...


def cmd_delete(args: argparse.Namespace) -> None:
    # TODO: remove task by id, save
    ...


def build_parser() -> argparse.ArgumentParser:
    # TODO: build parser with subcommands
    ...


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
''',
        milestones=[
            "add and list subcommands work; tasks survive a restart.",
            "complete and delete work correctly by task ID.",
            "IDs never repeat after deletions.",
        ],
        stretch_goals=[
            "Add a --priority flag (low/medium/high) and sort the list by priority.",
            "Add a due date field and warn on overdue tasks in list.",
            "Add a clear command to delete all completed tasks.",
        ],
        solution='''\
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TODO_FILE = Path.home() / ".todo.json"


def load_data() -> dict:
    if TODO_FILE.exists():
        with TODO_FILE.open() as f:
            return json.load(f)
    return {"next_id": 1, "tasks": []}


def save_data(data: dict) -> None:
    with TODO_FILE.open("w") as f:
        json.dump(data, f, indent=2)


def cmd_add(args: argparse.Namespace) -> None:
    data = load_data()
    task = {
        "id": data["next_id"],
        "description": args.description,
        "done": False,
        "created": datetime.now(timezone.utc).isoformat(),
    }
    data["tasks"].append(task)
    data["next_id"] += 1
    save_data(data)
    print(f"Added task #{task['id']}: {task['description']}")


def cmd_list(args: argparse.Namespace) -> None:
    data = load_data()
    if not data["tasks"]:
        print("No tasks yet. Use: todo add <description>")
        return
    for t in data["tasks"]:
        status = "[x]" if t["done"] else "[ ]"
        print(f"  {t['id']:>3}  {status}  {t['description']}")


def cmd_complete(args: argparse.Namespace) -> None:
    data = load_data()
    for t in data["tasks"]:
        if t["id"] == args.id:
            t["done"] = True
            save_data(data)
            print(f"Completed task #{args.id}.")
            return
    print(f"Task #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_delete(args: argparse.Namespace) -> None:
    data = load_data()
    original = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != args.id]
    if len(data["tasks"]) == original:
        print(f"Task #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    save_data(data)
    print(f"Deleted task #{args.id}.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="Minimal To-Do CLI")
    sub = p.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("description", nargs="+", type=str)
    add_p.set_defaults(func=lambda a: cmd_add(
        argparse.Namespace(description=" ".join(a.description))
    ))

    lst = sub.add_parser("list", help="List all tasks")
    lst.set_defaults(func=cmd_list)

    done = sub.add_parser("complete", help="Mark a task complete")
    done.add_argument("id", type=int)
    done.set_defaults(func=cmd_complete)

    rm = sub.add_parser("delete", help="Delete a task")
    rm.add_argument("id", type=int)
    rm.set_defaults(func=cmd_delete)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
''',
        estimated_minutes=75,
    ),

    Project(
        id="p04",
        title="Build a CSV Analyzer",
        difficulty="medium",
        concepts=["csv module", "data wrangling", "statistics", "argparse", "pathlib", "dictionaries"],
        requirements=[
            "Accept a CSV file path and an optional column name via argparse.",
            "Print a summary: row count, column names, and detected data types per column.",
            "For a specified numeric column: compute min, max, mean, median, and standard deviation.",
            "Detect and report missing/empty values per column as a count and percentage.",
            "Support a --groupby flag: count rows grouped by a categorical column.",
            "Output results in a clean, aligned text table.",
        ],
        build_guide=[
            "Use argparse to accept --file, --column (optional), and --groupby (optional).",
            "Read the CSV with csv.DictReader so column names are automatic.",
            "Write a detect_type(values) helper that returns 'numeric', 'date', or 'text'.",
            "Implement describe_numeric(values) using the statistics module for mean/median/stdev.",
            "Implement count_missing(rows, col) to tally empty-string and None values.",
            "Implement groupby_count(rows, col) using a collections.Counter.",
            "Format all tables with str.ljust/rjust for aligned columns.",
            "Handle FileNotFoundError and missing column names gracefully.",
        ],
        starter_code='''\
import argparse
import csv
import statistics
from collections import Counter
from pathlib import Path


def load_csv(path: Path) -> list[dict]:
    """Return list of row dicts from a CSV file."""
    # TODO: open with utf-8, use csv.DictReader, return list
    ...


def detect_type(values: list[str]) -> str:
    """Return "numeric", "date", or "text" based on the non-empty values."""
    # TODO: try float() conversion on a sample; fall back to text
    ...


def describe_numeric(values: list[str]) -> dict:
    """Return {"min","max","mean","median","stdev"} for a numeric column."""
    # TODO: filter empties, convert to float, use statistics module
    ...


def count_missing(rows: list[dict], col: str) -> tuple[int, float]:
    """Return (count, percentage) of missing values in col."""
    # TODO: count rows where value is "" or None
    ...


def groupby_count(rows: list[dict], col: str) -> Counter:
    # TODO: return Counter of values for col
    ...


def print_summary(rows: list[dict]) -> None:
    # TODO: print row count, column names, detected types, missing value report
    ...


def main() -> None:
    # TODO: parse args, load CSV, call appropriate analysis functions
    ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "CSV loads correctly and the summary table shows row/column counts.",
            "Numeric column statistics are accurate for a sample dataset.",
            "Missing value report shows correct counts and percentages.",
            "--groupby produces a sorted frequency table.",
        ],
        stretch_goals=[
            "Add a --histogram flag that renders a text-based bar chart for a numeric column.",
            "Support Excel .xlsx files using the openpyxl library.",
            "Add a --filter 'col=value' flag to subset rows before analysis.",
            "Export the summary to a JSON report file with --output.",
        ],
        solution='''\
import argparse
import csv
import statistics
import sys
from collections import Counter
from pathlib import Path


def load_csv(path: Path) -> tuple[list[dict], list[str]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = list(reader.fieldnames or [])
    return rows, cols


def detect_type(values: list[str]) -> str:
    non_empty = [v for v in values if v.strip()]
    if not non_empty:
        return "empty"
    sample = non_empty[:50]
    numeric = 0
    for v in sample:
        try:
            float(v)
            numeric += 1
        except ValueError:
            pass
    return "numeric" if numeric / len(sample) >= 0.8 else "text"


def describe_numeric(col: str, rows: list[dict]) -> dict:
    nums = []
    for r in rows:
        v = r.get(col, "").strip()
        if v:
            try:
                nums.append(float(v))
            except ValueError:
                pass
    if not nums:
        return {}
    return {
        "count": len(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": statistics.mean(nums),
        "median": statistics.median(nums),
        "stdev": statistics.stdev(nums) if len(nums) > 1 else 0.0,
    }


def count_missing(rows: list[dict], col: str) -> tuple[int, float]:
    missing = sum(1 for r in rows if not r.get(col, "").strip())
    pct = missing / len(rows) * 100 if rows else 0.0
    return missing, pct


def print_summary(rows: list[dict], cols: list[str]) -> None:
    print(f"Rows   : {len(rows)}")
    print(f"Columns: {len(cols)}")
    print()
    header = f"  {'Column':<25} {'Type':<10} {'Missing':>10} {'Missing%':>10}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for col in cols:
        values = [r.get(col, "") for r in rows]
        dtype = detect_type(values)
        missing, pct = count_missing(rows, col)
        print(f"  {col:<25} {dtype:<10} {missing:>10} {pct:>9.1f}%")


def main() -> None:
    p = argparse.ArgumentParser(description="Analyse a CSV file from the command line.")
    p.add_argument("file", type=Path, help="Path to CSV file")
    p.add_argument("--column", "-c", help="Numeric column to describe")
    p.add_argument("--groupby", "-g", help="Categorical column to count by group")
    args = p.parse_args()

    if not args.file.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    rows, cols = load_csv(args.file)
    print_summary(rows, cols)

    if args.column:
        if args.column not in cols:
            print(f"\\nColumn {args.column!r} not found. Available: {cols}", file=sys.stderr)
            sys.exit(1)
        stats = describe_numeric(args.column, rows)
        if not stats:
            print(f"\\nColumn {args.column!r} has no numeric data.")
        else:
            print(f"\\nStatistics for '{args.column}':")
            for k, v in stats.items():
                print(f"  {k:<10} {v:.4g}")

    if args.groupby:
        if args.groupby not in cols:
            print(f"\\nColumn {args.groupby!r} not found.", file=sys.stderr)
            sys.exit(1)
        counts = Counter(r.get(args.groupby, "") for r in rows)
        print(f"\\nGroup counts for '{args.groupby}':")
        for val, n in counts.most_common():
            bar = "#" * min(n, 40)
            print(f"  {val:<20} {n:>5}  {bar}")


if __name__ == "__main__":
    main()
''',
        estimated_minutes=90,
    ),

    Project(
        id="p05",
        title="Build a JSON API Fetcher",
        difficulty="medium",
        concepts=["HTTP requests", "JSON parsing", "argparse", "error handling", "urllib/requests"],
        requirements=[
            "Accept a URL via argparse and fetch it with an HTTP GET request.",
            "Pretty-print the JSON response with indentation.",
            "Support a --key flag to extract a nested key path (e.g. 'data.results.0.name').",
            "Show HTTP status code and response time in a header line.",
            "Handle HTTP errors (4xx/5xx) and network errors with friendly messages.",
            "Support a --save flag to write the raw JSON to a file.",
        ],
        build_guide=[
            "Use argparse to accept the URL, an optional --key, and an optional --save path.",
            "Fetch the URL with urllib.request.urlopen (or requests.get if available).",
            "Time the request using time.perf_counter() before and after.",
            "Parse the response body as JSON with json.loads.",
            "Implement extract_key(data, dotted_path) that drills into nested dicts/lists.",
            "Pretty-print the result with json.dumps(indent=2).",
            "Save to file if --save is given.",
            "Wrap network code in try/except for URLError, HTTPError, JSONDecodeError.",
        ],
        starter_code='''\
import argparse
import json
import sys
import time
import urllib.error
import urllib.request


def fetch(url: str) -> tuple[int, float, bytes]:
    """Return (status_code, elapsed_seconds, body_bytes)."""
    # TODO: time the request, return status, elapsed, body
    ...


def extract_key(data, dotted_path: str):
    """Drill into nested dicts/lists using a dot-separated path like "a.b.0.c"."""
    # TODO: split on ".", traverse dicts with key, lists with int index
    ...


def main() -> None:
    # TODO: parse args, fetch, extract key, print, optionally save
    ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "Fetching a public JSON API prints pretty-printed output.",
            "--key correctly extracts nested values including list indices.",
            "HTTP errors and network failures print a clean error instead of a traceback.",
        ],
        stretch_goals=[
            "Support POST with a --data flag that accepts a JSON string body.",
            "Add --headers to supply custom request headers as key:value pairs.",
            "Colorise JSON output (strings in green, numbers in cyan) using ANSI codes.",
        ],
        solution='''\
import argparse
import json
import sys
import time
import urllib.error
import urllib.request


def fetch(url: str) -> tuple[int, float, bytes]:
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            body = resp.read()
            status = resp.status
    except urllib.error.HTTPError as e:
        return e.code, time.perf_counter() - start, b""
    elapsed = time.perf_counter() - start
    return status, elapsed, body


def extract_key(data, dotted_path: str):
    parts = dotted_path.split(".")
    current = data
    for part in parts:
        try:
            current = current[int(part)] if isinstance(current, list) else current[part]
        except (KeyError, IndexError, TypeError) as exc:
            raise KeyError(f"Key path failed at {part!r}: {exc}") from exc
    return current


def main() -> None:
    p = argparse.ArgumentParser(description="Fetch and inspect a JSON API endpoint.")
    p.add_argument("url", help="URL to fetch")
    p.add_argument("--key", "-k", help="Dot-separated key path to extract (e.g. data.0.name)")
    p.add_argument("--save", "-s", help="Write raw JSON to this file path")
    args = p.parse_args()

    try:
        status, elapsed, body = fetch(args.url)
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        sys.exit(1)

    print(f"HTTP {status}  |  {elapsed*1000:.0f} ms  |  {len(body)} bytes")

    if not body:
        print("(empty body)")
        sys.exit(0 if status < 400 else 1)

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        print(f"JSON decode error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Saved to {args.save}")

    if args.key:
        try:
            result = extract_key(data, args.key)
        except KeyError as exc:
            print(f"Key error: {exc}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
''',
        estimated_minutes=75,
    ),

    Project(
        id="p06",
        title="Build a Password Generator",
        difficulty="easy",
        concepts=["random/secrets", "string module", "argparse", "loops", "functions"],
        requirements=[
            "Generate a password of a user-specified length (default 16).",
            "Support flags to include/exclude: uppercase, lowercase, digits, symbols.",
            "Ensure at least one character from each requested category.",
            "Generate multiple passwords with a --count flag.",
            "Print a strength indicator (weak / fair / strong / very strong).",
            "Support a --no-ambiguous flag to remove visually similar characters (0, O, l, 1, I).",
        ],
        build_guide=[
            "Use argparse for --length, --count, --no-uppercase, --no-lowercase, --no-digits, --no-symbols, --no-ambiguous.",
            "Build the character pool from string.ascii_uppercase/lowercase/digits and a symbols string.",
            "Guarantee at least one char from each included category by sampling one from each first.",
            "Fill the rest of the password with random.choices from the full pool.",
            "Shuffle the guaranteed + filler chars with random.shuffle to avoid predictable positions.",
            "Use secrets.choice instead of random.choice for cryptographic quality.",
            "Implement strength_label(length, pool_size) based on entropy bits = log2(pool_size**length).",
        ],
        starter_code='''\
import argparse
import math
import secrets
import string


AMBIGUOUS = set("0Ol1I")
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"


def build_pool(uppercase: bool, lowercase: bool, digits: bool, symbols: bool,
               no_ambiguous: bool) -> str:
    """Return the character pool string based on flags."""
    # TODO: concatenate the selected character sets
    # If no_ambiguous, filter out AMBIGUOUS chars
    ...


def generate_password(length: int, pool: str, categories: list[str]) -> str:
    """Return a password with at least one char from each category string."""
    # TODO: guarantee one from each category, fill rest from pool, shuffle
    ...


def strength_label(length: int, pool_size: int) -> str:
    """Return Weak / Fair / Strong / Very Strong based on entropy."""
    # TODO: entropy = length * log2(pool_size); map to labels
    ...


def main() -> None:
    # TODO: parse args, build pool, generate passwords, print with strength
    ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "Passwords of the correct length are generated from the right character set.",
            "Each password contains at least one character from every enabled category.",
            "Strength label prints and changes based on length/complexity.",
        ],
        stretch_goals=[
            "Add a --passphrase mode that generates a memorable word-separator password.",
            "Copy the first generated password to the clipboard using pyperclip.",
            "Add a --check flag that rates the strength of a user-supplied password.",
        ],
        solution='''\
import argparse
import math
import secrets
import string

AMBIGUOUS = set("0Ol1I")
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"


def build_pool(uppercase: bool, lowercase: bool, digits: bool,
               symbols: bool, no_ambiguous: bool) -> tuple[str, list[str]]:
    categories: list[str] = []
    if uppercase:
        categories.append(string.ascii_uppercase)
    if lowercase:
        categories.append(string.ascii_lowercase)
    if digits:
        categories.append(string.digits)
    if symbols:
        categories.append(SYMBOLS)
    pool = "".join(categories)
    if no_ambiguous:
        pool = "".join(c for c in pool if c not in AMBIGUOUS)
        categories = [
            "".join(c for c in cat if c not in AMBIGUOUS) for cat in categories
        ]
        categories = [c for c in categories if c]  # drop now-empty categories
    return pool, categories


def generate_password(length: int, pool: str, categories: list[str]) -> str:
    if not pool:
        raise ValueError("Character pool is empty — enable at least one character type.")
    # Guarantee at least one character from each category
    guaranteed = [secrets.choice(cat) for cat in categories]
    if len(guaranteed) > length:
        guaranteed = guaranteed[:length]
    remaining = length - len(guaranteed)
    filler = [secrets.choice(pool) for _ in range(remaining)]
    chars = guaranteed + filler
    # Shuffle in-place using secrets-quality randomness
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def strength_label(length: int, pool_size: int) -> str:
    if pool_size < 2:
        return "Weak"
    entropy = length * math.log2(pool_size)
    if entropy < 40:
        return "Weak"
    if entropy < 60:
        return "Fair"
    if entropy < 80:
        return "Strong"
    return "Very Strong"


def main() -> None:
    p = argparse.ArgumentParser(description="Generate secure passwords.")
    p.add_argument("-l", "--length", type=int, default=16, help="Password length (default 16)")
    p.add_argument("-n", "--count", type=int, default=1, help="Number of passwords (default 1)")
    p.add_argument("--no-uppercase", dest="uppercase", action="store_false", default=True)
    p.add_argument("--no-lowercase", dest="lowercase", action="store_false", default=True)
    p.add_argument("--no-digits", dest="digits", action="store_false", default=True)
    p.add_argument("--no-symbols", dest="symbols", action="store_false", default=True)
    p.add_argument("--no-ambiguous", action="store_true", default=False)
    args = p.parse_args()

    pool, categories = build_pool(
        args.uppercase, args.lowercase, args.digits, args.symbols, args.no_ambiguous
    )
    label = strength_label(args.length, len(pool))
    print(f"Pool size: {len(pool)} chars  |  Strength: {label}\\n")
    for _ in range(args.count):
        print(generate_password(args.length, pool, categories))


if __name__ == "__main__":
    main()
''',
        estimated_minutes=60,
    ),

    Project(
        id="p07",
        title="Build a Personal Finance Tracker",
        difficulty="medium",
        concepts=["JSON persistence", "argparse", "datetime", "data aggregation", "formatting"],
        requirements=[
            "Support add, list, summary, and delete commands via argparse subcommands.",
            "Each transaction has: id, date (YYYY-MM-DD), description, amount, and category.",
            "Persist all transactions in a JSON file (~/.finances.json).",
            "summary command shows total income, total expenses, and net balance.",
            "summary --month YYYY-MM filters to a specific month.",
            "list supports --category and --limit flags.",
            "Amounts are stored as integers in cents to avoid float rounding errors.",
        ],
        build_guide=[
            "Set up argparse with subparsers: add, list, summary, delete.",
            "Design the JSON schema: {next_id, transactions: [{id, date, description, amount_cents, category}]}.",
            "On 'add', parse --amount as a float, multiply by 100 and round to int.",
            "Implement format_amount(cents) that renders $1,234.56 with sign.",
            "On 'summary', separate income (amount > 0) from expenses (amount < 0) and total each.",
            "Filter by month with a string prefix match on the date field (date.startswith(month)).",
            "On 'list', apply --category and --limit filters before printing.",
            "Print all tables with str.ljust/rjust alignment.",
        ],
        starter_code='''\
import argparse
import json
from datetime import date
from pathlib import Path

FINANCE_FILE = Path.home() / ".finances.json"


def load_data() -> dict:
    # TODO: load from FINANCE_FILE or return default {next_id: 1, transactions: []}
    ...


def save_data(data: dict) -> None:
    # TODO: write to FINANCE_FILE as pretty JSON
    ...


def format_amount(cents: int) -> str:
    """Format cents as currency string, e.g. +$1,234.56 or -$12.00."""
    # TODO: divide by 100, format with commas, prepend sign
    ...


def cmd_add(args: argparse.Namespace) -> None:
    # TODO: parse amount to cents, build transaction dict, append, save
    ...


def cmd_list(args: argparse.Namespace) -> None:
    # TODO: filter by category/limit, print table
    ...


def cmd_summary(args: argparse.Namespace) -> None:
    # TODO: filter by month if given, compute income/expenses/net, print
    ...


def cmd_delete(args: argparse.Namespace) -> None:
    # TODO: remove transaction by id, save
    ...


if __name__ == "__main__":
    # TODO: build parser, parse args, call func
    pass
''',
        milestones=[
            "add and list work; transactions persist between runs.",
            "format_amount renders dollars correctly from integer cents.",
            "summary shows correct totals; --month filter works.",
        ],
        stretch_goals=[
            "Add a bar chart of spending by category using text-based bars.",
            "Add a --budget flag to set a monthly spending limit and warn when exceeded.",
            "Export transactions to CSV with a export subcommand.",
        ],
        solution='''\
import argparse
import json
import sys
from datetime import date
from pathlib import Path

FINANCE_FILE = Path.home() / ".finances.json"


def load_data() -> dict:
    if FINANCE_FILE.exists():
        with FINANCE_FILE.open() as f:
            return json.load(f)
    return {"next_id": 1, "transactions": []}


def save_data(data: dict) -> None:
    with FINANCE_FILE.open("w") as f:
        json.dump(data, f, indent=2)


def format_amount(cents: int) -> str:
    sign = "+" if cents >= 0 else "-"
    dollars = abs(cents) / 100
    return f"{sign}${dollars:,.2f}"


def cmd_add(args: argparse.Namespace) -> None:
    data = load_data()
    cents = round(float(args.amount) * 100)
    tx = {
        "id": data["next_id"],
        "date": args.date or date.today().isoformat(),
        "description": args.description,
        "amount_cents": cents,
        "category": args.category or "uncategorised",
    }
    data["transactions"].append(tx)
    data["next_id"] += 1
    save_data(data)
    print(f"Added #{tx['id']}: {tx['description']}  {format_amount(cents)}")


def cmd_list(args: argparse.Namespace) -> None:
    data = load_data()
    txs = data["transactions"]
    if args.category:
        txs = [t for t in txs if t["category"].lower() == args.category.lower()]
    if args.limit:
        txs = txs[-args.limit:]
    if not txs:
        print("No transactions found.")
        return
    print(f"  {'#':>4}  {'Date':<12} {'Category':<15} {'Amount':>12}  Description")
    print("  " + "-" * 65)
    for t in txs:
        print(f"  {t['id']:>4}  {t['date']:<12} {t['category']:<15} "
              f"{format_amount(t['amount_cents']):>12}  {t['description']}")


def cmd_summary(args: argparse.Namespace) -> None:
    data = load_data()
    txs = data["transactions"]
    if args.month:
        txs = [t for t in txs if t["date"].startswith(args.month)]
    income = sum(t["amount_cents"] for t in txs if t["amount_cents"] > 0)
    expenses = sum(t["amount_cents"] for t in txs if t["amount_cents"] < 0)
    net = income + expenses
    label = f"Month: {args.month}" if args.month else "All time"
    print(f"\\n{label}  ({len(txs)} transaction(s))")
    print(f"  Income  : {format_amount(income):>12}")
    print(f"  Expenses: {format_amount(expenses):>12}")
    print(f"  Net     : {format_amount(net):>12}")


def cmd_delete(args: argparse.Namespace) -> None:
    data = load_data()
    before = len(data["transactions"])
    data["transactions"] = [t for t in data["transactions"] if t["id"] != args.id]
    if len(data["transactions"]) == before:
        print(f"Transaction #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    save_data(data)
    print(f"Deleted transaction #{args.id}.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="finance", description="Personal Finance Tracker")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="Record a transaction")
    a.add_argument("description", help="Short description")
    a.add_argument("amount", type=float, help="Amount in dollars (negative = expense)")
    a.add_argument("--category", "-c", default="")
    a.add_argument("--date", "-d", default="", help="YYYY-MM-DD (default: today)")
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", help="List transactions")
    ls.add_argument("--category", "-c", default="")
    ls.add_argument("--limit", "-l", type=int, default=0, help="Show last N transactions")
    ls.set_defaults(func=cmd_list)

    sm = sub.add_parser("summary", help="Show income/expense summary")
    sm.add_argument("--month", "-m", default="", help="YYYY-MM filter")
    sm.set_defaults(func=cmd_summary)

    rm = sub.add_parser("delete", help="Delete a transaction")
    rm.add_argument("id", type=int)
    rm.set_defaults(func=cmd_delete)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
''',
        estimated_minutes=90,
    ),

    Project(
        id="p08",
        title="Build a Web Scraper",
        difficulty="medium",
        concepts=["HTTP requests", "HTML parsing", "regular expressions", "csv export", "argparse"],
        requirements=[
            "Accept a URL via argparse and fetch its HTML.",
            "Extract all hyperlinks (<a href=...>) and print them.",
            "Support a --tag flag to extract all text content from a specified HTML tag.",
            "Support a --save-csv flag to export results to a CSV file.",
            "Respect robots.txt by checking it before scraping (warn, don't block).",
            "Support a --depth flag (default 0) to follow links one level deep.",
            "Handle HTTP errors and malformed HTML gracefully.",
        ],
        build_guide=[
            "Use urllib.request to fetch pages and urllib.robotparser for robots.txt.",
            "Parse HTML with html.parser via html.parser.HTMLParser subclass.",
            "Implement a LinkExtractor(HTMLParser) that collects href values from <a> tags.",
            "Implement a TagTextExtractor(HTMLParser) that collects text inside a given tag.",
            "Normalise relative URLs to absolute with urllib.parse.urljoin.",
            "For --depth 1, fetch each found link once (skip non-http and already-visited).",
            "Write results to CSV with csv.writer if --save-csv is given.",
            "Install the optional `requests` library for nicer HTTP; fall back to urllib.",
        ],
        starter_code='''\
import argparse
import csv
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser


class LinkExtractor(HTMLParser):
    """Collect all href values from <a> tags."""
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        # TODO: if tag == "a", find href attr, normalise to absolute URL, append
        ...


class TagTextExtractor(HTMLParser):
    """Collect text content of all occurrences of a given tag."""
    def __init__(self, target_tag: str):
        super().__init__()
        self.target_tag = target_tag
        self.results: list[str] = []
        self._inside = False
        self._buffer = ""

    def handle_starttag(self, tag, attrs):
        # TODO: set _inside flag when tag matches
        ...

    def handle_data(self, data):
        # TODO: accumulate data when _inside
        ...

    def handle_endtag(self, tag):
        # TODO: when closing tag matches, append _buffer to results, reset state
        ...


def fetch_html(url: str) -> tuple[int, str]:
    # TODO: return (status_code, html_text)
    ...


def main() -> None:
    # TODO: parse args, fetch, extract, print/save
    ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "LinkExtractor correctly finds and normalises all links on a page.",
            "TagTextExtractor returns text for a given tag (e.g. h1, p).",
            "--save-csv writes a valid CSV file.",
        ],
        stretch_goals=[
            "Add rate limiting (time.sleep) between requests to be polite.",
            "Support --depth 2 with a proper visited-set BFS/DFS.",
            "Add --match-pattern to filter links by a regex.",
        ],
        solution='''\
import argparse
import csv
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser


class LinkExtractor(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, val in attrs:
                if attr == "href" and val:
                    abs_url = urllib.parse.urljoin(self.base_url, val)
                    if abs_url.startswith(("http://", "https://")):
                        self.links.append(abs_url)


class TagTextExtractor(HTMLParser):
    def __init__(self, target_tag: str):
        super().__init__()
        self.target_tag = target_tag.lower()
        self.results: list[str] = []
        self._inside = False
        self._buffer = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() == self.target_tag:
            self._inside = True
            self._buffer = ""

    def handle_data(self, data):
        if self._inside:
            self._buffer += data

    def handle_endtag(self, tag):
        if self._inside and tag.lower() == self.target_tag:
            text = self._buffer.strip()
            if text:
                self.results.append(text)
            self._inside = False
            self._buffer = ""


def fetch_html(url: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            charset = "utf-8"
            ct = resp.headers.get("Content-Type", "")
            if "charset=" in ct:
                charset = ct.split("charset=")[-1].split(";")[0].strip()
            return resp.status, resp.read().decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def check_robots(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch("*", url)
    except Exception:
        return True  # assume allowed if robots.txt unreadable


def main() -> None:
    p = argparse.ArgumentParser(description="Scrape links and text from a webpage.")
    p.add_argument("url", help="URL to scrape")
    p.add_argument("--tag", "-t", default="", help="HTML tag to extract text from (e.g. h1)")
    p.add_argument("--save-csv", "-s", default="", help="Save results to this CSV file")
    p.add_argument("--depth", "-d", type=int, default=0, choices=[0, 1],
                   help="Follow links 1 level deep (default 0)")
    args = p.parse_args()

    if not check_robots(args.url):
        print(f"Warning: robots.txt disallows scraping {args.url}", file=sys.stderr)

    status, html = fetch_html(args.url)
    print(f"HTTP {status}  {args.url}")
    if not html:
        print("No content returned.")
        sys.exit(1)

    extractor = LinkExtractor(args.url)
    extractor.feed(html)
    links = extractor.links

    results = []

    if args.tag:
        te = TagTextExtractor(args.tag)
        te.feed(html)
        print(f"\\n<{args.tag}> text on page ({len(te.results)} found):")
        for i, text in enumerate(te.results, 1):
            short = text[:120].replace("\\n", " ")
            print(f"  {i:>3}. {short}")
            results.append({"type": args.tag, "url": args.url, "text": text})
    else:
        print(f"\\nLinks found: {len(links)}")
        for link in links:
            print(f"  {link}")
            results.append({"type": "link", "url": link, "text": ""})

    if args.depth == 1:
        visited = {args.url}
        print(f"\\nFollowing {min(len(links), 10)} links (depth=1) …")
        for link in links[:10]:
            if link in visited:
                continue
            visited.add(link)
            time.sleep(0.5)
            s2, h2 = fetch_html(link)
            print(f"  {s2}  {link}")
            if h2 and args.tag:
                te2 = TagTextExtractor(args.tag)
                te2.feed(h2)
                for text in te2.results:
                    results.append({"type": args.tag, "url": link, "text": text})

    if args.save_csv and results:
        with open(args.save_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["type", "url", "text"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\\nSaved {len(results)} rows to {args.save_csv}")


if __name__ == "__main__":
    main()
''',
        estimated_minutes=105,
    ),

    Project(
        id="p09",
        title="Build a SQLite Contact Book",
        difficulty="medium",
        concepts=["sqlite3", "SQL", "argparse", "CRUD", "data validation"],
        requirements=[
            "Store contacts in a SQLite database (~/.contacts.db).",
            "Support add, search, list, update, and delete subcommands.",
            "Each contact has: id, name, email, phone, and notes fields.",
            "search matches name or email with a case-insensitive LIKE query.",
            "update <id> accepts --name/--email/--phone/--notes to change individual fields.",
            "Validate email format with a simple regex before inserting.",
            "list shows a paginated table (--limit, --offset).",
        ],
        build_guide=[
            "Use sqlite3.connect with the db path; call create_tables() on startup.",
            "Write the CREATE TABLE IF NOT EXISTS SQL with an auto-increment primary key.",
            "Implement add_contact() using a parameterised INSERT statement.",
            "Implement search_contacts() using LIKE with % wildcards.",
            "Implement update_contact() that builds the SET clause dynamically from non-None kwargs.",
            "Implement delete_contact() using DELETE WHERE id = ?.",
            "Validate email with re.fullmatch(r'[^@]+@[^@]+\\.[^@]+', email).",
            "Format the contacts table using str.ljust and aligned columns.",
        ],
        starter_code='''\
import argparse
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path.home() / ".contacts.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    # TODO: CREATE TABLE IF NOT EXISTS contacts (...)
    ...


def validate_email(email: str) -> bool:
    # TODO: return True if email matches a simple regex pattern
    ...


def add_contact(conn, name: str, email: str, phone: str, notes: str) -> int:
    # TODO: INSERT and return lastrowid
    ...


def search_contacts(conn, query: str) -> list[sqlite3.Row]:
    # TODO: SELECT WHERE name LIKE ? OR email LIKE ?
    ...


def update_contact(conn, contact_id: int, **kwargs) -> bool:
    # TODO: build dynamic SET clause, return True if a row was updated
    ...


def delete_contact(conn, contact_id: int) -> bool:
    # TODO: DELETE WHERE id = ?, return True if row deleted
    ...


def print_contacts(rows) -> None:
    # TODO: print aligned table of contacts
    ...


def main() -> None:
    # TODO: set up argparse, connect, create tables, dispatch commands
    ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "Contacts are created and persisted in the SQLite database.",
            "search returns correct matches for partial name and email queries.",
            "update changes only the specified fields; delete removes the record.",
        ],
        stretch_goals=[
            "Add a --export-vcf flag that writes all contacts as a .vcf vCard file.",
            "Add an import-csv subcommand to bulk-import from a CSV file.",
            "Add birthday field and a show-upcoming command for contacts with birthdays this month.",
        ],
        solution='''\
import argparse
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path.home() / ".contacts.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            email TEXT    NOT NULL DEFAULT '',
            phone TEXT    NOT NULL DEFAULT '',
            notes TEXT    NOT NULL DEFAULT ''
        )
    """)
    conn.commit()


def validate_email(email: str) -> bool:
    if not email:
        return True  # email is optional
    return bool(re.fullmatch(r"[^@\\s]+@[^@\\s]+\\.[^@\\s]+", email))


def add_contact(conn: sqlite3.Connection, name: str, email: str,
                phone: str, notes: str) -> int:
    cur = conn.execute(
        "INSERT INTO contacts (name, email, phone, notes) VALUES (?, ?, ?, ?)",
        (name, email, phone, notes),
    )
    conn.commit()
    return cur.lastrowid  # type: ignore[return-value]


def list_contacts(conn: sqlite3.Connection, limit: int = 50,
                  offset: int = 0) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM contacts ORDER BY name LIMIT ? OFFSET ?", (limit, offset)
    ).fetchall()


def search_contacts(conn: sqlite3.Connection, query: str) -> list[sqlite3.Row]:
    pattern = f"%{query}%"
    return conn.execute(
        "SELECT * FROM contacts WHERE name LIKE ? OR email LIKE ? ORDER BY name",
        (pattern, pattern),
    ).fetchall()


def update_contact(conn: sqlite3.Connection, contact_id: int, **kwargs) -> bool:
    updates = {k: v for k, v in kwargs.items() if v is not None}
    if not updates:
        return False
    set_clause = ", ".join(f"{col} = ?" for col in updates)
    values = list(updates.values()) + [contact_id]
    cur = conn.execute(f"UPDATE contacts SET {set_clause} WHERE id = ?", values)
    conn.commit()
    return cur.rowcount > 0


def delete_contact(conn: sqlite3.Connection, contact_id: int) -> bool:
    cur = conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    return cur.rowcount > 0


def print_contacts(rows) -> None:
    if not rows:
        print("No contacts found.")
        return
    header = f"  {'ID':>4}  {'Name':<22} {'Email':<28} {'Phone':<16}  Notes"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in rows:
        notes = (r["notes"] or "")[:30]
        print(f"  {r['id']:>4}  {r['name']:<22} {r['email']:<28} {r['phone']:<16}  {notes}")


def main() -> None:
    p = argparse.ArgumentParser(prog="contacts", description="SQLite Contact Book")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="Add a contact")
    a.add_argument("name")
    a.add_argument("--email", default="")
    a.add_argument("--phone", default="")
    a.add_argument("--notes", default="")

    sub.add_parser("list", help="List all contacts").add_argument(
        "--limit", type=int, default=50
    )

    s = sub.add_parser("search", help="Search contacts")
    s.add_argument("query")

    u = sub.add_parser("update", help="Update a contact")
    u.add_argument("id", type=int)
    u.add_argument("--name")
    u.add_argument("--email")
    u.add_argument("--phone")
    u.add_argument("--notes")

    d = sub.add_parser("delete", help="Delete a contact")
    d.add_argument("id", type=int)

    args = p.parse_args()
    conn = get_connection()
    create_tables(conn)

    if args.command == "add":
        if not validate_email(args.email):
            print(f"Invalid email: {args.email!r}", file=sys.stderr)
            sys.exit(1)
        cid = add_contact(conn, args.name, args.email, args.phone, args.notes)
        print(f"Added contact #{cid}: {args.name}")
    elif args.command == "list":
        print_contacts(list_contacts(conn, limit=args.limit))
    elif args.command == "search":
        print_contacts(search_contacts(conn, args.query))
    elif args.command == "update":
        ok = update_contact(conn, args.id,
                            name=args.name, email=args.email,
                            phone=args.phone, notes=args.notes)
        print(f"Updated #{args.id}." if ok else f"Contact #{args.id} not found.")
    elif args.command == "delete":
        ok = delete_contact(conn, args.id)
        print(f"Deleted #{args.id}." if ok else f"Contact #{args.id} not found.")


if __name__ == "__main__":
    main()
''',
        estimated_minutes=105,
    ),

    Project(
        id="p10",
        title="Build a Mini Data Dashboard",
        difficulty="hard",
        concepts=["pandas", "matplotlib", "argparse", "data wrangling", "statistical summaries", "visualization"],
        requirements=[
            "Accept a CSV file via argparse and load it with pandas.",
            "Print a rich summary: shape, dtypes, missing-value counts, and descriptive stats.",
            "Plot a correlation heatmap of numeric columns and save it as PNG.",
            "Plot a histogram for a user-specified column with --hist-col.",
            "Plot a time-series line chart if a date column and value column are specified.",
            "Support --output-dir to control where PNGs are saved (default: current dir).",
            "Requires pip install pandas matplotlib (note this in the output on startup).",
        ],
        build_guide=[
            "Install pandas and matplotlib: pip install pandas matplotlib.",
            "Use argparse to accept --file, --hist-col, --date-col, --value-col, --output-dir.",
            "Load the CSV with pd.read_csv(); parse date columns with parse_dates.",
            "Print shape, dtypes, df.isnull().sum(), and df.describe() for the summary.",
            "For the heatmap: compute df.select_dtypes('number').corr(), plot with matplotlib imshow or seaborn.heatmap.",
            "For the histogram: df[col].plot.hist(bins=30) and save the figure.",
            "For time-series: set the date column as index, plot df[value_col] as a line.",
            "Save each figure with fig.savefig() and print the path to stdout.",
            "Wrap all pandas/matplotlib imports in a try/except ImportError with install hint.",
        ],
        starter_code='''\
import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")  # non-interactive backend for saving PNGs
    import matplotlib.pyplot as plt
except ImportError:
    print("This project requires: pip install pandas matplotlib", file=sys.stderr)
    sys.exit(1)


def print_summary(df: "pd.DataFrame") -> None:
    # TODO: print shape, dtypes, missing counts, and df.describe()
    ...


def plot_correlation_heatmap(df: "pd.DataFrame", output_dir: Path) -> Path:
    # TODO: compute corr matrix, plot with imshow, add colorbar, save PNG
    ...


def plot_histogram(df: "pd.DataFrame", col: str, output_dir: Path) -> Path:
    # TODO: df[col].plot.hist(bins=30), save PNG
    ...


def plot_timeseries(df: "pd.DataFrame", date_col: str,
                    value_col: str, output_dir: Path) -> Path:
    # TODO: parse dates, set index, plot line, save PNG
    ...


def main() -> None:
    # TODO: parse args, load CSV, call relevant functions
    ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "CSV loads and the summary table is printed with correct statistics.",
            "Correlation heatmap PNG is generated for datasets with multiple numeric columns.",
            "Histogram and time-series charts are saved when the relevant flags are provided.",
        ],
        stretch_goals=[
            "Add a --scatter col1 col2 flag to plot a scatter plot between two numeric columns.",
            "Detect and impute missing values, printing a before/after comparison.",
            "Add a --pairplot flag to generate a seaborn pairplot for all numeric columns.",
            "Output an HTML summary page that embeds all generated charts inline.",
        ],
        solution='''\
import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("This project requires: pip install pandas matplotlib numpy", file=sys.stderr)
    sys.exit(1)


def print_summary(df: pd.DataFrame) -> None:
    print(f"\\nShape  : {df.shape[0]} rows x {df.shape[1]} columns")
    print("\\nDtypes:")
    for col, dtype in df.dtypes.items():
        missing = df[col].isnull().sum()
        pct = missing / len(df) * 100
        print(f"  {str(col):<30} {str(dtype):<12}  missing: {missing} ({pct:.1f}%)")
    print("\\nDescriptive Statistics (numeric columns):")
    print(df.describe().to_string())


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: Path) -> Path:
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        print("Not enough numeric columns for a correlation heatmap (need >= 2).")
        return Path()
    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=(max(6, len(corr)), max(5, len(corr) - 1)))
    im = ax.imshow(corr.values, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                    fontsize=8, color="black")
    fig.colorbar(im, ax=ax, label="Pearson r")
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()
    out = output_dir / "correlation_heatmap.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_histogram(df: pd.DataFrame, col: str, output_dir: Path) -> Path:
    if col not in df.columns:
        print(f"Column {col!r} not found.", file=sys.stderr)
        return Path()
    fig, ax = plt.subplots(figsize=(8, 5))
    df[col].dropna().plot.hist(bins=30, ax=ax, edgecolor="white")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.set_title(f"Distribution of '{col}'")
    fig.tight_layout()
    safe_col = col.replace("/", "_").replace(" ", "_")
    out = output_dir / f"histogram_{safe_col}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_timeseries(df: pd.DataFrame, date_col: str,
                    value_col: str, output_dir: Path) -> Path:
    if date_col not in df.columns or value_col not in df.columns:
        print(f"Columns {date_col!r} or {value_col!r} not found.", file=sys.stderr)
        return Path()
    ts = df[[date_col, value_col]].copy()
    ts[date_col] = pd.to_datetime(ts[date_col], errors="coerce")
    ts = ts.dropna().sort_values(date_col).set_index(date_col)
    fig, ax = plt.subplots(figsize=(10, 5))
    ts[value_col].plot(ax=ax)
    ax.set_title(f"{value_col} over time")
    ax.set_ylabel(value_col)
    fig.tight_layout()
    safe = value_col.replace("/", "_").replace(" ", "_")
    out = output_dir / f"timeseries_{safe}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Mini Data Dashboard — CSV analysis & charts")
    p.add_argument("file", type=Path, help="Path to CSV file")
    p.add_argument("--hist-col", help="Column name for histogram")
    p.add_argument("--date-col", help="Date column for time-series")
    p.add_argument("--value-col", help="Value column for time-series")
    p.add_argument("--output-dir", type=Path, default=Path("."),
                   help="Directory to save PNG charts (default: .)")
    args = p.parse_args()

    if not args.file.exists():
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.file)
    print_summary(df)

    out = plot_correlation_heatmap(df, args.output_dir)
    if out.name:
        print(f"\\nCorrelation heatmap saved: {out}")

    if args.hist_col:
        out = plot_histogram(df, args.hist_col, args.output_dir)
        if out.name:
            print(f"Histogram saved: {out}")

    if args.date_col and args.value_col:
        out = plot_timeseries(df, args.date_col, args.value_col, args.output_dir)
        if out.name:
            print(f"Time-series chart saved: {out}")


if __name__ == "__main__":
    main()
''',
        estimated_minutes=120,
    ),

    Project(
        id="p11",
        title="Build an Automation Script Runner",
        difficulty="hard",
        concepts=["subprocess", "YAML/JSON config", "argparse", "scheduling concepts", "logging", "pathlib"],
        requirements=[
            "Load a list of named tasks from a JSON config file (default: tasks.json).",
            "Each task has a name, command (list of args), working_dir, and enabled flag.",
            "Support run <task-name> to execute a single task via subprocess.",
            "Support run-all to execute all enabled tasks sequentially.",
            "Log stdout/stderr of each task to a dated log file in a logs/ directory.",
            "Print a live summary: task name, status (OK/FAIL), return code, and elapsed time.",
            "Support a --dry-run flag that prints what would run without executing.",
            "Handle missing tasks and failed subprocesses without crashing the runner.",
        ],
        build_guide=[
            "Define the JSON config schema: {tasks: [{name, command, working_dir, enabled}]}.",
            "Write load_config(path) and validate_config(data) to parse and verify the JSON.",
            "Implement run_task(task, dry_run) using subprocess.run with capture_output=True.",
            "Inside run_task, measure elapsed time with time.perf_counter().",
            "Write the task's stdout+stderr to logs/<task_name>_<YYYY-MM-DD>.log.",
            "Print a status line: '[OK]' or '[FAIL]' + return code + elapsed.",
            "In run_all, collect results and print a final summary table.",
            "Set up argparse with subparsers: run, run-all, list.",
        ],
        starter_code='''\
import argparse
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

DEFAULT_CONFIG = Path("tasks.json")
LOGS_DIR = Path("logs")


def load_config(path: Path) -> list[dict]:
    """Load and return the task list from a JSON config file."""
    # TODO: open and parse, return data["tasks"]
    ...


def run_task(task: dict, dry_run: bool = False) -> dict:
    """Execute a task and return a result dict with status, returncode, elapsed, log_path."""
    # TODO: if dry_run, print command and return success-mock
    # TODO: run subprocess, capture output, write log, return result dict
    ...


def cmd_run(args: argparse.Namespace, tasks: list[dict]) -> None:
    # TODO: find task by name, run it, print result
    ...


def cmd_run_all(args: argparse.Namespace, tasks: list[dict]) -> None:
    # TODO: filter enabled tasks, run each, print summary table
    ...


def cmd_list(args: argparse.Namespace, tasks: list[dict]) -> None:
    # TODO: print formatted table of all tasks and their enabled status
    ...


def main() -> None:
    # TODO: parse args, load config, dispatch command
    ...


if __name__ == "__main__":
    main()
''',
        milestones=[
            "Config loads and list command shows all tasks.",
            "run executes a task and writes output to a log file.",
            "run-all processes all enabled tasks and prints a summary.",
        ],
        stretch_goals=[
            "Add a --parallel flag to run-all that executes tasks concurrently with threading.",
            "Add task dependencies (depends_on list) and topological sort before execution.",
            "Add a --notify flag that prints a desktop notification on task completion.",
            "Support environment variable injection per task in the config.",
        ],
        solution='''\
import argparse
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

DEFAULT_CONFIG = Path("tasks.json")
LOGS_DIR = Path("logs")


def load_config(path: Path) -> list[dict]:
    if not path.exists():
        print(f"Config file not found: {path}", file=sys.stderr)
        print(\'Create a tasks.json with: {"tasks": [{"name": "hello", "command": ["echo", "hello"], "working_dir": ".", "enabled": true}]}\')
        sys.exit(1)
    with path.open() as f:
        data = json.load(f)
    tasks = data.get("tasks", [])
    for i, t in enumerate(tasks):
        if "name" not in t or "command" not in t:
            print(f"Task #{i} missing required fields (name, command).", file=sys.stderr)
            sys.exit(1)
        t.setdefault("working_dir", ".")
        t.setdefault("enabled", True)
    return tasks


def run_task(task: dict, dry_run: bool = False) -> dict:
    name = task["name"]
    cmd = task["command"]
    cwd = task.get("working_dir", ".")

    if dry_run:
        print(f"  [DRY-RUN] {name}: {' '.join(cmd)}  (cwd={cwd})")
        return {"name": name, "status": "DRY-RUN", "returncode": 0, "elapsed": 0.0, "log": None}

    LOGS_DIR.mkdir(exist_ok=True)
    log_path = LOGS_DIR / f"{name}_{date.today().isoformat()}.log"

    start = time.perf_counter()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    elapsed = time.perf_counter() - start

    with log_path.open("a", encoding="utf-8") as lf:
        lf.write(f"=== {name} @ {date.today().isoformat()} ===\\n")
        lf.write(f"Command: {cmd}\\n")
        lf.write(f"Return code: {result.returncode}\\n")
        lf.write("--- stdout ---\\n")
        lf.write(result.stdout or "(empty)\\n")
        lf.write("--- stderr ---\\n")
        lf.write(result.stderr or "(empty)\\n\\n")

    status = "OK" if result.returncode == 0 else "FAIL"
    return {
        "name": name,
        "status": status,
        "returncode": result.returncode,
        "elapsed": elapsed,
        "log": log_path,
    }


def print_result(r: dict) -> None:
    tag = "[OK]  " if r["status"] == "OK" else "[FAIL]"
    print(f"  {tag} {r['name']:<25}  rc={r['returncode']}  {r['elapsed']:.2f}s"
          + (f"  -> {r['log']}" if r["log"] else ""))


def cmd_run(args: argparse.Namespace, tasks: list[dict]) -> None:
    matches = [t for t in tasks if t["name"] == args.name]
    if not matches:
        print(f"Task {args.name!r} not found. Run 'list' to see available tasks.", file=sys.stderr)
        sys.exit(1)
    r = run_task(matches[0], dry_run=args.dry_run)
    print_result(r)
    sys.exit(0 if r["returncode"] == 0 else 1)


def cmd_run_all(args: argparse.Namespace, tasks: list[dict]) -> None:
    enabled = [t for t in tasks if t.get("enabled", True)]
    print(f"Running {len(enabled)} enabled task(s)…\\n")
    results = []
    for task in enabled:
        r = run_task(task, dry_run=args.dry_run)
        print_result(r)
        results.append(r)
    ok = sum(1 for r in results if r["status"] in ("OK", "DRY-RUN"))
    fail = len(results) - ok
    print(f"\\nSummary: {ok} passed, {fail} failed out of {len(results)} task(s).")
    if fail:
        sys.exit(1)


def cmd_list(args: argparse.Namespace, tasks: list[dict]) -> None:
    print(f"  {'Name':<25} {'Enabled':<10} Command")
    print("  " + "-" * 60)
    for t in tasks:
        enabled = "yes" if t.get("enabled", True) else "no"
        cmd_str = " ".join(t["command"])[:40]
        print(f"  {t['name']:<25} {enabled:<10} {cmd_str}")


def main() -> None:
    p = argparse.ArgumentParser(description="Automation Script Runner")
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to tasks.json")
    p.add_argument("--dry-run", action="store_true", help="Print commands without running")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("run", help="Run a specific task by name")
    r.add_argument("name")

    sub.add_parser("run-all", help="Run all enabled tasks")
    sub.add_parser("list", help="List all configured tasks")

    args = p.parse_args()
    tasks = load_config(args.config)

    if args.command == "run":
        cmd_run(args, tasks)
    elif args.command == "run-all":
        cmd_run_all(args, tasks)
    elif args.command == "list":
        cmd_list(args, tasks)


if __name__ == "__main__":
    main()
''',
        estimated_minutes=120,
    ),

    Project(
        id="p12",
        title="Build a Complete CLI App From Scratch",
        difficulty="hard",
        concepts=["argparse", "sqlite3", "JSON/CSV I/O", "subprocess", "packaging", "OOP", "testing concepts"],
        requirements=[
            "Design and build a CLI app of your own choosing with at least 4 subcommands.",
            "Use a SQLite database for persistent storage.",
            "Support import (from CSV or JSON) and export subcommands.",
            "Include a --version flag and a --verbose mode.",
            "Write at least 3 unit tests using unittest or pytest.",
            "Package the app with a pyproject.toml so it is installable with pip install -e .",
            "Write a README section documenting installation and all subcommands.",
            "Demonstrate at least one use of a class or dataclass to model domain data.",
        ],
        build_guide=[
            "Choose your domain: a habit tracker, recipe book, bookmark manager, bug tracker, etc.",
            "Sketch the data model on paper: what entities exist, what fields do they have?",
            "Write the dataclass or class for your core domain object.",
            "Create the SQLite schema: one or more CREATE TABLE statements.",
            "Implement CRUD operations (add, list, update, delete) as functions or methods.",
            "Add import/export subcommands using csv or json from the standard library.",
            "Add --version using argparse's version action and store __version__ = '0.1.0'.",
            "Write 3+ unit tests using unittest.TestCase or pytest fixtures with an in-memory DB.",
            "Create pyproject.toml with [project] metadata and a [project.scripts] entry point.",
            "Write a short README: installation steps, usage examples for every subcommand.",
        ],
        starter_code='''\
"""
my_cli_app — replace this with your own app name and description.

Domain: <choose your domain here>
"""
import argparse
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path

__version__ = "0.1.0"
DB_PATH = Path.home() / ".my_app.db"


@dataclass
class Item:
    """Replace with your domain model."""
    id: int = 0
    name: str = ""
    # TODO: add fields relevant to your chosen domain


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    # TODO: CREATE TABLE IF NOT EXISTS ...
    conn.commit()


def cmd_add(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    # TODO: insert a new item
    ...


def cmd_list(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    # TODO: query and print items
    ...


def cmd_delete(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    # TODO: delete item by id
    ...


def cmd_export(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    # TODO: write all items to a CSV or JSON file
    ...


def cmd_import(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    # TODO: read items from a CSV or JSON file and insert
    ...


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="My CLI App")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--verbose", "-v", action="store_true")
    # TODO: add subparsers for add, list, delete, export, import
    return p


def main() -> None:
    args = build_parser().parse_args()
    conn = get_connection()
    create_schema(conn)
    # TODO: dispatch to command handler


if __name__ == "__main__":
    main()
''',
        milestones=[
            "Domain model and database schema are designed and working.",
            "All CRUD subcommands (add, list, delete) are implemented and tested manually.",
            "Import and export round-trip correctly (export then re-import produces the same data).",
            "Unit tests pass and the app is installable via pip install -e .",
        ],
        stretch_goals=[
            "Add a search subcommand with full-text search using SQLite FTS5.",
            "Add a TUI (text user interface) mode using the curses module.",
            "Publish to PyPI and add a GitHub Actions workflow for automated testing.",
            "Add a REST API layer exposing the same operations via http.server.",
        ],
        solution='''\
"""
habit_tracker — a minimal daily habit tracker CLI.

This is a reference implementation of the p12 capstone. Students are
encouraged to build their OWN app; this serves as a worked example.
"""
import argparse
import csv
import json
import sqlite3
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

__version__ = "0.1.0"
DB_PATH = Path.home() / ".habits.db"


@dataclass
class Habit:
    id: int
    name: str
    description: str
    created: str
    streak: int = 0


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL DEFAULT \\'\\',
            created     TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
            completed_on TEXT NOT NULL,
            PRIMARY KEY (habit_id, completed_on)
        )
    """)
    conn.commit()


def get_streak(conn: sqlite3.Connection, habit_id: int) -> int:
    rows = conn.execute(
        "SELECT completed_on FROM completions WHERE habit_id = ? ORDER BY completed_on DESC",
        (habit_id,),
    ).fetchall()
    if not rows:
        return 0
    from datetime import timedelta
    streak = 0
    check = date.today()
    for row in rows:
        d = date.fromisoformat(row["completed_on"])
        if d == check or d == check - timedelta(days=streak):
            streak += 1
            check = d - timedelta(days=1)
        else:
            break
    return streak


def cmd_add(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    try:
        conn.execute(
            "INSERT INTO habits (name, description, created) VALUES (?, ?, ?)",
            (args.name, args.description or "", date.today().isoformat()),
        )
        conn.commit()
        print(f"Habit added: {args.name!r}")
    except sqlite3.IntegrityError:
        print(f"Habit {args.name!r} already exists.", file=sys.stderr)


def cmd_list(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT * FROM habits ORDER BY name").fetchall()
    if not rows:
        print("No habits yet. Use: habits add <name>")
        return
    today = date.today().isoformat()
    print(f"  {'ID':>4}  {'Habit':<25} {'Streak':>7}  {'Done today'}")
    print("  " + "-" * 55)
    for r in rows:
        done = conn.execute(
            "SELECT 1 FROM completions WHERE habit_id=? AND completed_on=?",
            (r["id"], today),
        ).fetchone()
        streak = get_streak(conn, r["id"])
        mark = "[x]" if done else "[ ]"
        print(f"  {r['id']:>4}  {r['name']:<25} {streak:>7}  {mark}")


def cmd_complete(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    today = date.today().isoformat()
    try:
        conn.execute(
            "INSERT INTO completions (habit_id, completed_on) VALUES (?, ?)",
            (args.id, today),
        )
        conn.commit()
        print(f"Habit #{args.id} marked complete for {today}.")
    except sqlite3.IntegrityError:
        print(f"Habit #{args.id} already completed today.")


def cmd_delete(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    cur = conn.execute("DELETE FROM habits WHERE id = ?", (args.id,))
    conn.commit()
    if cur.rowcount:
        print(f"Deleted habit #{args.id}.")
    else:
        print(f"Habit #{args.id} not found.", file=sys.stderr)


def cmd_export(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT * FROM habits").fetchall()
    out_path = Path(args.output)
    if out_path.suffix == ".json":
        data = [dict(r) for r in rows]
        out_path.write_text(json.dumps(data, indent=2))
    else:
        with out_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "description", "created"])
            writer.writerows([[r["id"], r["name"], r["description"], r["created"]] for r in rows])
    print(f"Exported {len(rows)} habit(s) to {out_path}.")


def cmd_import(args: argparse.Namespace, conn: sqlite3.Connection) -> None:
    src = Path(args.input)
    if not src.exists():
        print(f"File not found: {src}", file=sys.stderr)
        sys.exit(1)
    if src.suffix == ".json":
        records = json.loads(src.read_text())
    else:
        with src.open(newline="") as f:
            records = list(csv.DictReader(f))
    count = 0
    for r in records:
        try:
            conn.execute(
                "INSERT INTO habits (name, description, created) VALUES (?, ?, ?)",
                (r["name"], r.get("description", ""), r.get("created", date.today().isoformat())),
            )
            count += 1
        except sqlite3.IntegrityError:
            pass  # skip duplicates
    conn.commit()
    print(f"Imported {count} habit(s).")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="habits", description="Daily Habit Tracker")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--verbose", "-v", action="store_true")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="Add a new habit")
    a.add_argument("name")
    a.add_argument("--description", default="")

    sub.add_parser("list", help="List habits with streaks")

    c = sub.add_parser("complete", help="Mark today's completion for a habit")
    c.add_argument("id", type=int)

    d = sub.add_parser("delete", help="Delete a habit")
    d.add_argument("id", type=int)

    ex = sub.add_parser("export", help="Export habits to CSV or JSON")
    ex.add_argument("output", help="Output file (.csv or .json)")

    im = sub.add_parser("import", help="Import habits from CSV or JSON")
    im.add_argument("input", help="Input file (.csv or .json)")

    return p


def main() -> None:
    args = build_parser().parse_args()
    conn = get_connection()
    create_schema(conn)
    dispatch = {
        "add": cmd_add,
        "list": cmd_list,
        "complete": cmd_complete,
        "delete": cmd_delete,
        "export": cmd_export,
        "import": cmd_import,
    }
    dispatch[args.command](args, conn)


if __name__ == "__main__":
    main()
''',
        estimated_minutes=180,
    ),
]
