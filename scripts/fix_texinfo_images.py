
#!/usr/bin/env python3
"""Rewrite Texinfo image references to generated PNG files."""

from pathlib import Path
import re
import sys

texi = Path(sys.argv[1])
images = Path(sys.argv[2])

content = texi.read_text(encoding="utf-8")

pattern = re.compile(r"@image\{([^}\n]+)\}")
missing = []
converted = 0


def replace(match: re.Match[str]) -> str:
    global converted

    fields = match.group(1).split(",")
    name = fields[0].strip()

    # Generated images preserve the original relative paths.
    png = images / f"{name}.png"

    if not png.is_file():
        missing.append(str(png))
        return match.group(0)

    converted += 1

    # Texinfo searches this base name through --image-dir.
    return f"@image{{{name}}}"


result = pattern.sub(replace, content)

if missing:
    print("Missing images:")
    for path in sorted(set(missing)):
        print(f"  {path}")
    raise SystemExit(1)

texi.write_text(result, encoding="utf-8")
print(f"Updated {converted} image references")
