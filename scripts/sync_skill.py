from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "attenza-intervention" / "SKILL.md"
TARGETS = (
    ROOT / "plugins" / "attenza" / "skills" / "attenza-intervention" / "SKILL.md",
    ROOT / "claude-plugins" / "attenza" / "skills" / "attenza-intervention" / "SKILL.md",
    ROOT / "agent-plugins" / "attenza" / "skills" / "attenza-intervention" / "SKILL.md",
)


def main() -> None:
    content = SOURCE.read_text(encoding="utf-8")
    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        print(f"synced {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
