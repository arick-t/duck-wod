#!/usr/bin/env python3
"""
Add Source API (local / GitHub Pages compatible)
"""

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from sources_api import add_source

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "message": "Usage: add_source.py <name> <url>"
        }))
        return

    name = sys.argv[1]
    url = sys.argv[2]

    success, message = add_source(name, url)

    print(json.dumps({
        "success": success,
        "message": message
    }))


if __name__ == "__main__":
    main()
