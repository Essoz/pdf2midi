"""Check that the installed score-conversion skill contains its shared files."""

from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "INSTALL.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/app-workflow.md",
    "references/native-mscz.md",
    "references/proofreading.md",
    "scripts/check_install.py",
    "scripts/inspect_score.py",
)


def main():
    root = Path(__file__).resolve().parent.parent
    missing = []
    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file() or path.stat().st_size == 0:
            missing.append(name)
    if missing:
        print("安装不完整，以下文件缺失或为空：")
        for name in missing:
            print(f"  {name}")
        return 1
    print(f"安装文件齐全（{len(REQUIRED_FILES)} 个）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
