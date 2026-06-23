"""Test configuration.

Adds the ``src`` directory to ``sys.path`` so the test-suite runs whether or not
the package has been installed with ``pip install -e .``.
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
