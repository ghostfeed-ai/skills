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

# Public folder and skill name for each source skill. The server keeps the
# source name, which is the one `get_skill` takes.
PUBLIC_NAMES = {
    "ghostfeed-video-ads": "ai-video-ads",
    "ghostfeed-ad-style-whiteboard": "whiteboard-animation-ads",
    "ghostfeed-ad-style-skeleton": "skeleton-animation-ads",
    "ghostfeed-ad-style-zack-d": "zack-d-style-ads",
    "ghostfeed-ad-style-claymation": "claymation-ads",
    "ghostfeed-ad-style-paper": "paper-animation-ads",
    "ghostfeed-ad-style-3d-cartoon": "3d-cartoon-ads",
    "ghostfeed-ad-style-2d-cartoon": "2d-cartoon-ads",
    "ghostfeed-ad-style-realistic": "realistic-video-ads",
    "ghostfeed-ad-style-cinematic": "cinematic-product-ads",
    "ghostfeed-song": "ai-song-ads",
    "ghostfeed-ad-copy": "video-ad-scripts",
    "ghostfeed-ad-characters": "consistent-ad-characters",
    "ghostfeed-ugc-reactions": "ai-ugc-videos",
    "ghostfeed-avatars": "ai-ugc-avatars",
    "ghostfeed-slideshows": "tiktok-slideshows",
    "ghostfeed-slideshow-clone": "clone-tiktok-slideshows",
}

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


def build_skill(source: Path, public_name: str) -> str:
    lines = source.read_text().split("\n")
    if lines[0] != "---":
        raise ValueError(f"{source} has no frontmatter")
    close = lines.index("---", 1)
    server_name = source.parent.name
    head = [f"name: {public_name}" if l.startswith("name:") else l for l in lines[1:close]]
    if f"name: {public_name}" not in head:
        raise ValueError(f"{source} has no name line")
    body = "\n".join(lines[close + 1 :]).lstrip("\n")
    requires = REQUIRES.replace("{name}", server_name)
    return "\n".join(["---", *head, COMPATIBILITY, "---", "", requires, body])


def main() -> None:
    source_root = Path(sys.argv[1]).resolve()
    sources = sorted(p for p in source_root.glob("*/SKILL.md") if p.parent.name not in SERVER_ONLY)
    if not sources:
        raise SystemExit(f"No skills found in {source_root}")
    destination = ROOT / "skills"
    shutil.rmtree(destination, ignore_errors=True)
    for source in sources:
        public_name = PUBLIC_NAMES.get(source.parent.name, source.parent.name)
        target = destination / public_name
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text(build_skill(source, public_name))
    print(f"Built {len(sources)} skills. Server only: {', '.join(sorted(SERVER_ONLY))}")


if __name__ == "__main__":
    main()
