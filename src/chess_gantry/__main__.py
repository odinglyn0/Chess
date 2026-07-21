from __future__ import annotations

import sys

from .cli import main


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1].endswith(".json") and not sys.argv[1].startswith("-"):
        sys.argv.insert(1, "run")
    main()
