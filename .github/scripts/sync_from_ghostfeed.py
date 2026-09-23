"""Mirror the approved skills published by the Ghostfeed production site."""

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


BASE_URL = "https://ghostfeed.ai/skills"
ROOT = Path(__file__).resolve().parents[2]
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
DIGEST_PATTERN = re.compile(r"[a-f0-9]{64}\Z")


def download(name: str) -> bytes:
    return subprocess.run(
        [
            "curl",
            "--fail",
            "--silent",
            "--show-error",
            "--location",
            "--max-time",
            "30",
            f"{BASE_URL}/{name}",
        ],
        check=True,
        capture_output=True,
    ).stdout


def verify_digest(content: bytes, expected: str, name: str) -> None:
    if not isinstance(expected, str) or not DIGEST_PATTERN.fullmatch(expected):
        raise ValueError(f"Invalid digest in manifest for {name}")
    if hashlib.sha256(content).hexdigest() != expected:
        raise ValueError(f"Published {name} does not match its manifest; retry after deployment settles")


def main() -> None:
    manifest = json.loads(download("manifest.json"))
    if manifest.get("schemaVersion") != 1 or not isinstance(manifest.get("skills"), list):
        raise ValueError("Unsupported Ghostfeed skill manifest")

    with TemporaryDirectory() as temporary_directory:
        staged = Path(temporary_directory)
        readme = download("README.md")
        verify_digest(readme, manifest.get("readmeSha256"), "README.md")
        (staged / "README.md").write_bytes(readme)

        seen: set[str] = set()
        for entry in manifest["skills"]:
            if not isinstance(entry, dict):
                raise ValueError("Invalid skill manifest entry")
            slug = entry.get("slug")
            if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug) or slug in seen:
                raise ValueError(f"Invalid or repeated skill slug: {slug!r}")
            seen.add(slug)
            content = download(f"{slug}.md")
            verify_digest(content, entry.get("sha256"), slug)
            skill_dir = staged / "skills" / slug
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_bytes(content)

        if not seen:
            raise ValueError("Refusing to publish an empty skill manifest")

        # Complete and verify every download before changing the public repo.
        shutil.copyfile(staged / "README.md", ROOT / "README.md")
        destination = ROOT / "skills"
        destination.mkdir(exist_ok=True)
        for slug in seen:
            target = destination / slug
            target.mkdir(exist_ok=True)
            shutil.copyfile(staged / "skills" / slug / "SKILL.md", target / "SKILL.md")


if __name__ == "__main__":
    main()
