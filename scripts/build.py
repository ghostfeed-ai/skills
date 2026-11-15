"""Build the public skills from the Ghostfeed source skills.

Usage: python3 scripts/build.py <path to docs/skills in the Ghostfeed repo>

The source skill text is copied unchanged. Each public copy gets a
`compatibility` line in its frontmatter and one block under the frontmatter
that says the skill needs the Ghostfeed MCP server.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP_URL = "https://api.ghostfeed.ai/api/v2/mcp"

# Skills that stay on the server. An agent reads them with `get_skill` once
# Ghostfeed is connected.
SERVER_ONLY = {"ghostfeed-slideshow-taste"}

COMPATIBILITY = (
    "compatibility: Requires the Ghostfeed MCP server "
    f"({MCP_URL}) and a Ghostfeed account."
)

REQUIRES = f"""> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `{{name}}` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `{MCP_URL}`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.
"""


def build_skill(source: Path) -> str:
    lines = source.read_text().split("\n")
    if lines[0] != "---":
        raise ValueError(f"{source} has no frontmatter")
    close = lines.index("---", 1)
    name = next(l.split(":", 1)[1].strip() for l in lines[1:close] if l.startswith("name:"))
    if name != source.parent.name:
        raise ValueError(f"{source}: name {name!r} does not match its folder")
    head = lines[1:close] + [COMPATIBILITY]
    body = "\n".join(lines[close + 1 :]).lstrip("\n")
    return "\n".join(["---", *head, "---", "", REQUIRES.replace("{name}", name), body])


def main() -> None:
    source_root = Path(sys.argv[1]).resolve()
    sources = sorted(p for p in source_root.glob("*/SKILL.md") if p.parent.name not in SERVER_ONLY)
    if not sources:
        raise SystemExit(f"No skills found in {source_root}")
    destination = ROOT / "skills"
    shutil.rmtree(destination, ignore_errors=True)
    for source in sources:
        target = destination / source.parent.name
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text(build_skill(source))
    print(f"Built {len(sources)} skills. Server only: {', '.join(sorted(SERVER_ONLY))}")


if __name__ == "__main__":
    main()
