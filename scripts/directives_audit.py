#!/usr/bin/env python3
"""Cross-project audit for promotion candidates and drift.

Walks each project listed in `projects.yml`, compares its Claude Code assets
(`.claude/hooks/`, `.claude/commands/`, `scripts/`) to the canonical shared
locations in dotfiles/directives, and flags:

- **Promotion candidates**: generic-looking assets that exist in a project but
  not upstream. Files meeting the strict "auto" heuristic get a draft PR
  against dotfiles. Others are reported for manual review.
- **Drift**: broken references, stale command names, URL rot.

Output: comment appended to a rolling monthly issue in suniljames/directives
labeled `automation-log`. Draft PRs opened in dotfiles for auto candidates.
On any exception, opens an issue with label `automation-failure`.

Designed for launchd cron on the Mac Mini. LLM-agnostic (uses `gh` CLI only;
no Claude/Gemini shell-out in this MVP — add later when heuristics prove
insufficient).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any

DIRECTIVES_REPO = "suniljames/directives"
DOTFILES_REPO = "suniljames/dotfiles"

AUDIT_LABEL = "automation-log"
FAILURE_LABEL = "automation-failure"
DRIFT_LABEL = "drift"


# ---------- utilities ----------


def run(cmd: list[str], **kwargs: Any) -> tuple[int, str, str]:
    """Run subprocess, return (returncode, stdout, stderr). Never raises."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=False, **kwargs)
    return result.returncode, result.stdout, result.stderr


def gh(args: list[str]) -> tuple[int, str, str]:
    return run(["gh", *args])


def gh_api_json(endpoint: str, *, method: str = "GET", body: dict | None = None) -> Any:
    """Call `gh api ENDPOINT`, return parsed JSON. Raises on error."""
    cmd = ["gh", "api", endpoint, "-X", method]
    if body is not None:
        for k, v in body.items():
            if isinstance(v, (list, dict)):
                cmd += ["-F", f"{k}={json.dumps(v)}"]
            elif isinstance(v, bool):
                cmd += ["-F", f"{k}={'true' if v else 'false'}"]
            else:
                cmd += ["-F", f"{k}={v}"]
    rc, out, err = run(cmd)
    if rc != 0:
        raise RuntimeError(f"gh api {method} {endpoint} failed: {err.strip()}")
    return json.loads(out) if out.strip() else None


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- YAML loading ----------


def load_yaml(path: Path) -> dict:
    """Load a YAML file. Requires PyYAML."""
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError(
            "PyYAML is required. Install with: pip install pyyaml"
        ) from e

    with open(path) as f:
        return yaml.safe_load(f) or {}


# ---------- core logic ----------


def expand_path(p: str) -> Path:
    return Path(os.path.expanduser(p))


def load_projects(repo_root: Path) -> dict:
    cfg = repo_root / "projects.yml"
    if not cfg.exists():
        raise FileNotFoundError(f"projects.yml not found at {cfg}")
    return load_yaml(cfg)


def git_pull_if_clean(local_path: Path) -> str:
    """Pull latest on main if the repo is clean; return status note."""
    if not local_path.exists():
        return "not cloned"
    rc, out, _ = run(["git", "status", "--porcelain"], cwd=local_path)
    if rc != 0:
        return "not a git repo"
    if out.strip():
        return "dirty — skipped pull"
    rc, out, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=local_path)
    branch = out.strip()
    if branch != "main":
        return f"on branch {branch} — skipped pull"
    rc, _, err = run(["git", "pull", "--ff-only"], cwd=local_path)
    return "pulled" if rc == 0 else f"pull failed: {err.strip()[:100]}"


def walk_scan_paths(project: dict) -> list[Path]:
    """Return all files under any of project['scan'] paths."""
    local = expand_path(project["local_path"])
    files: list[Path] = []
    for scan in project.get("scan", []):
        base = local / scan
        if not base.exists():
            continue
        for root, _dirs, names in os.walk(base):
            for n in names:
                if n.startswith("."):
                    continue
                files.append(Path(root) / n)
    return files


def classify_file(
    path: Path,
    content: str,
    vocabulary: list[str],
    shared_digests: set[str],
    shared_names: set[str],
    all_project_names: dict[str, list[tuple[str, Path]]],
) -> dict:
    """Return classification dict with keys: status, reasons, auto_promote."""
    reasons: list[str] = []
    name = path.name

    # Already shared (exact content)?
    if file_digest(path) in shared_digests:
        return {"status": "already-shared", "reasons": ["digest match in shared"], "auto_promote": False}

    # Project-specific vocabulary check
    hits = [v for v in vocabulary if v.lower() in content.lower()]
    if hits:
        reasons.append(f"contains project-specific strings: {', '.join(hits[:5])}")
        return {"status": "project-specific", "reasons": reasons, "auto_promote": False}

    # Reuse signal: same filename in another project?
    dupes = all_project_names.get(name, [])
    dupe_in_other = [d for d in dupes if d[1] != path]
    if len(dupe_in_other) >= 1:
        reasons.append(f"same filename appears in {len(dupe_in_other) + 1} projects")
        # Strong signal — auto
        return {"status": "candidate-auto", "reasons": reasons, "auto_promote": True}

    # Exists upstream by name but content differs (divergence)
    if name in shared_names:
        reasons.append("filename exists in shared but content differs")
        return {"status": "candidate-divergent", "reasons": reasons, "auto_promote": False}

    # Otherwise: generic-looking but single-project use
    reasons.append("no project-specific content; single-project use")
    return {"status": "candidate-single", "reasons": reasons, "auto_promote": False}


def scan_shared_targets(shared_targets: list[dict]) -> tuple[set[str], dict[str, Path]]:
    """Return (set of digests, dict of name -> path) across shared targets."""
    digests: set[str] = set()
    names: dict[str, Path] = {}
    for target in shared_targets:
        local = expand_path(target["local_path"])
        for path_kind, rel in target.get("paths", {}).items():
            base = local / rel
            if not base.exists():
                continue
            for p in base.rglob("*"):
                if p.is_file() and not p.name.startswith("."):
                    digests.add(file_digest(p))
                    names[p.name] = p
    return digests, names


def index_all_projects(projects: list[dict]) -> dict[str, list[tuple[str, Path]]]:
    """name -> [(project_name, path), ...] — used to detect cross-project reuse."""
    idx: dict[str, list[tuple[str, Path]]] = {}
    for project in projects:
        local = expand_path(project["local_path"])
        if not local.exists():
            continue
        for scan in project.get("scan", []):
            base = local / scan
            if not base.exists():
                continue
            for p in base.rglob("*"):
                if p.is_file() and not p.name.startswith("."):
                    idx.setdefault(p.name, []).append((project["name"], p))
    return idx


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def detect_drift(repo_root: Path, shared_targets: list[dict]) -> list[str]:
    """Return a list of drift descriptions. Focused checks, not exhaustive."""
    findings: list[str] = []

    # 1. Dotfiles CLAUDE.md references to directives/* — check URLs resolve locally
    dotfiles_target = next((t for t in shared_targets if t["name"] == "dotfiles"), None)
    directives_local = repo_root  # this script lives inside directives
    if dotfiles_target:
        df_local = expand_path(dotfiles_target["local_path"])
        claude_md = df_local / ".claude/CLAUDE.md"
        if claude_md.exists():
            text = read_text_safe(claude_md)
            # Find links to directives/... paths
            pattern = r"https://github\.com/suniljames/directives/blob/main/([^\s\)]+)"
            for match in re.finditer(pattern, text):
                rel = match.group(1).rstrip(")")
                if not (directives_local / rel).exists():
                    findings.append(
                        f"dotfiles CLAUDE.md references missing path: directives/{rel}"
                    )

    # 2. Pipeline command name consistency between dotfiles CLAUDE.md and directives manifest.yml
    manifest = directives_local / "teams/engineering/manifest.yml"
    if dotfiles_target and manifest.exists():
        df_local = expand_path(dotfiles_target["local_path"])
        claude_md = df_local / ".claude/CLAUDE.md"
        if claude_md.exists():
            claude_text = read_text_safe(claude_md)
            manifest_text = read_text_safe(manifest)
            canonical_cmds = set(re.findall(r"command:\s*/(\w+)", manifest_text))
            dotfiles_cmds = set(re.findall(r"\|\s*`/(\w+)`\s*\|", claude_text))
            missing_in_dotfiles = canonical_cmds - dotfiles_cmds
            extra_in_dotfiles = dotfiles_cmds - canonical_cmds
            if missing_in_dotfiles:
                findings.append(
                    f"dotfiles CLAUDE.md missing commands from manifest: {sorted(missing_in_dotfiles)}"
                )
            if extra_in_dotfiles:
                findings.append(
                    f"dotfiles CLAUDE.md has stale commands not in manifest: {sorted(extra_in_dotfiles)}"
                )

    return findings


# ---------- GitHub posting ----------


def find_or_create_monthly_issue(repo: str, dry_run: bool) -> int | None:
    """Return issue number for this month's rolling audit log."""
    now = dt.datetime.now()
    title_tag = f"{now.year:04d}-{now.month:02d}"
    # Ensure label exists before any list/create operation. --force is idempotent.
    gh([
        "label", "create", AUDIT_LABEL, "--repo", repo,
        "--color", "0366d6",
        "--description", "Rolling log for directives-audit cron",
        "--force",
    ])
    # Search for open issue with label + title containing tag
    rc, out, _ = gh(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--label",
            AUDIT_LABEL,
            "--state",
            "open",
            "--json",
            "number,title",
            "--limit",
            "20",
        ]
    )
    issues = json.loads(out or "[]") if rc == 0 else []

    for issue in issues:
        if title_tag in issue["title"]:
            return issue["number"]

    if dry_run:
        return None

    title = f"Automation: directives-audit log — {title_tag}"
    body = (
        f"Rolling log of weekly audits and daily drift checks for {title_tag}.\n\n"
        "Each run appends a comment with heartbeat + findings. Silence past "
        "one week means the cron is broken — check /tmp/directives-audit.log "
        "on the Mini."
    )
    rc, out, err = gh(
        [
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            title,
            "--body",
            body,
            "--label",
            AUDIT_LABEL,
        ]
    )
    if rc != 0:
        raise RuntimeError(f"failed to create monthly issue: {err}")
    # gh prints URL on success; extract number
    m = re.search(r"/issues/(\d+)", out)
    if not m:
        raise RuntimeError(f"couldn't parse issue number from: {out}")
    return int(m.group(1))


def append_comment(repo: str, issue_number: int, body: str, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] would append comment to {repo}#{issue_number}:\n{body[:500]}")
        return
    rc, _, err = gh(
        [
            "issue",
            "comment",
            str(issue_number),
            "--repo",
            repo,
            "--body",
            body,
        ]
    )
    if rc != 0:
        raise RuntimeError(f"failed to append comment: {err}")


def open_promotion_pr(
    candidate: dict, shared_target: dict, dry_run: bool
) -> str | None:
    """Open a draft PR against a shared target promoting a candidate file.

    Uses a temporary git worktree so the user's main checkout is never
    modified. Worktree is removed on every exit path.

    Returns PR URL on success, or None on dry-run / existing PR / error.
    """
    import shutil

    src_path: Path = candidate["path"]
    name = src_path.name
    dest_repo = f"{shared_target['owner']}/{shared_target['repo']}"
    dest_rel = (
        shared_target["paths"]["hooks"]
        if "hook" in str(src_path).lower()
        else shared_target["paths"].get("scripts", "scripts")
    )
    dest_path = f"{dest_rel}/{name}"
    branch = f"auto-promote/{name.replace('.', '-')}"

    # Check for existing open PR on this branch
    rc, out, _ = gh(
        ["pr", "list", "--repo", dest_repo, "--head", branch, "--state", "open",
         "--json", "number,url", "--limit", "1"]
    )
    if rc == 0:
        existing = json.loads(out or "[]")
        if existing:
            return existing[0]["url"]

    if dry_run:
        print(f"[dry-run] would open draft PR on {dest_repo} branch {branch} for {dest_path}")
        return None

    dest_local = expand_path(shared_target["local_path"])
    # Work in an isolated worktree to avoid modifying the user's main checkout
    temp_worktree = Path("/tmp") / f"audit-{shared_target['name']}-{branch.replace('/', '-')}"
    if temp_worktree.exists():
        shutil.rmtree(temp_worktree, ignore_errors=True)

    try:
        rc, _, err = run(["git", "fetch", "origin"], cwd=dest_local)
        if rc != 0:
            return None
        rc, _, err = run(
            ["git", "worktree", "add", "-B", branch, str(temp_worktree), "origin/main"],
            cwd=dest_local,
        )
        if rc != 0:
            return None

        target_full = temp_worktree / dest_path
        target_full.parent.mkdir(parents=True, exist_ok=True)
        target_full.write_bytes(src_path.read_bytes())
        if os.access(src_path, os.X_OK):
            os.chmod(target_full, 0o755)

        rc, _, _ = run(["git", "add", dest_path], cwd=temp_worktree)
        if rc != 0:
            return None

        src_rel = str(src_path.relative_to(expand_path(candidate["project_root"])))
        msg = (
            f"auto-promote: add {dest_path} from {candidate['project']}\n\n"
            f"Automated promotion by directives-audit.sh.\n"
            f"Source: {candidate['project']}:{src_rel}\n"
            f"Reasons:\n" + "\n".join(f"  - {r}" for r in candidate["reasons"])
        )
        rc, _, err = run(["git", "commit", "-m", msg], cwd=temp_worktree)
        if rc != 0:
            return None
        rc, _, err = run(["git", "push", "-u", "origin", branch], cwd=temp_worktree)
        if rc != 0:
            return None

        rc, out, err = gh(
            ["pr", "create", "--repo", dest_repo, "--draft", "--base", "main",
             "--head", branch,
             "--title", f"auto-promote: {name} from {candidate['project']}",
             "--body", _pr_body(candidate, dest_path)]
        )
        if rc != 0:
            return None
        return out.strip()
    finally:
        # Always clean up the worktree, regardless of success
        run(["git", "worktree", "remove", "--force", str(temp_worktree)], cwd=dest_local)
        if temp_worktree.exists():
            shutil.rmtree(temp_worktree, ignore_errors=True)


def _pr_body(candidate: dict, dest_path: str) -> str:
    reasons = "\n".join(f"- {r}" for r in candidate["reasons"])
    return (
        f"**Automated draft PR** from `directives-audit.sh`. Review before merging.\n\n"
        f"## What\n\n"
        f"Promote `{candidate['path'].name}` from `{candidate['project']}` into `{dest_path}`.\n\n"
        f"## Why (heuristic)\n\n{reasons}\n\n"
        f"## Before merging\n\n"
        f"- [ ] Confirm the file is genuinely generic (no project-coupled logic)\n"
        f"- [ ] Confirm no existing shared version is meaningfully different\n"
        f"- [ ] If merging, also open follow-up to delete project-local copies and repoint settings.json\n"
    )


def open_failure_issue(repo: str, traceback_str: str) -> None:
    title = f"directives-audit failure — {dt.datetime.now().isoformat(timespec='minutes')}"
    body = f"```\n{traceback_str}\n```"
    gh(["label", "create", FAILURE_LABEL, "--repo", repo, "--color", "b60205", "--force"])
    gh(["issue", "create", "--repo", repo, "--title", title, "--body", body, "--label", FAILURE_LABEL])


# ---------- report generation ----------


def format_report(
    mode: str,
    project_states: list[tuple[str, str]],
    candidates: list[dict],
    drift: list[str],
    draft_prs: list[str],
) -> str:
    now = dt.datetime.now().isoformat(timespec="minutes")
    lines = [f"## {mode} — {now}", "", "**Heartbeat:** OK"]

    if project_states:
        lines.append("")
        lines.append("### Project pull status")
        for name, status in project_states:
            lines.append(f"- `{name}`: {status}")

    auto_cand = [c for c in candidates if c["status"] == "candidate-auto"]
    single_cand = [c for c in candidates if c["status"] == "candidate-single"]
    divergent = [c for c in candidates if c["status"] == "candidate-divergent"]
    proj_specific = [c for c in candidates if c["status"] == "project-specific"]
    already = [c for c in candidates if c["status"] == "already-shared"]

    if auto_cand or single_cand or divergent:
        lines.append("")
        lines.append("### Promotion candidates")
    if auto_cand:
        lines.append("")
        lines.append("**Auto-promote (strong reuse signal)**:")
        for c in auto_cand:
            lines.append(f"- `{c['path'].name}` from `{c['project']}` — {'; '.join(c['reasons'])}")
    if single_cand:
        lines.append("")
        lines.append("**Single-project generic** (manual review — may be too niche to promote):")
        for c in single_cand:
            lines.append(f"- `{c['path'].name}` from `{c['project']}` — {'; '.join(c['reasons'])}")
    if divergent:
        lines.append("")
        lines.append("**Divergent from shared** (filename exists upstream but content differs):")
        for c in divergent:
            lines.append(f"- `{c['path'].name}` from `{c['project']}` — {'; '.join(c['reasons'])}")

    if drift:
        lines.append("")
        lines.append("### Drift detected")
        for d in drift:
            lines.append(f"- {d}")

    if draft_prs:
        lines.append("")
        lines.append("### Draft PRs opened")
        for url in draft_prs:
            lines.append(f"- {url}")

    if not (auto_cand or single_cand or divergent or drift or draft_prs):
        lines.append("")
        lines.append("_No findings this run._")

    # Footer: counts for quick scanning
    lines.append("")
    lines.append(
        f"<sub>Scanned: {len(candidates)} files "
        f"({len(auto_cand)} auto, {len(single_cand)} manual, "
        f"{len(divergent)} divergent, {len(proj_specific)} project-specific, "
        f"{len(already)} already shared)</sub>"
    )
    return "\n".join(lines)


# ---------- main ----------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, help="Path to directives repo")
    parser.add_argument("--weekly", action="store_true", help="Full audit + auto-PRs")
    parser.add_argument("--drift-only", action="store_true", help="Only drift checks")
    parser.add_argument("--dry-run", action="store_true", help="Don't post or open PRs")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    mode = "Weekly audit" if args.weekly else ("Drift check" if args.drift_only else "Audit (manual run)")

    try:
        config = load_projects(repo_root)
        projects = config.get("projects", [])
        shared_targets = config.get("shared_targets", [])
        vocabulary = config.get("project_specific_vocabulary", [])

        project_states: list[tuple[str, str]] = []
        candidates: list[dict] = []

        if not args.drift_only:
            # Pull latest
            for project in projects:
                local = expand_path(project["local_path"])
                state = git_pull_if_clean(local)
                project_states.append((project["name"], state))
            for target in shared_targets:
                local = expand_path(target["local_path"])
                state = git_pull_if_clean(local)
                project_states.append((target["name"], state))

            # Index shared assets
            shared_digests, shared_name_paths = scan_shared_targets(shared_targets)
            shared_names = set(shared_name_paths.keys())

            # Index cross-project filename reuse
            project_name_idx = index_all_projects(projects)

            # Classify each project file
            for project in projects:
                files = walk_scan_paths(project)
                for path in files:
                    content = read_text_safe(path)
                    cls = classify_file(
                        path, content, vocabulary, shared_digests, shared_names, project_name_idx
                    )
                    candidates.append(
                        {
                            "path": path,
                            "project": project["name"],
                            "project_root": project["local_path"],
                            **cls,
                        }
                    )

        drift = detect_drift(repo_root, shared_targets)

        # Open draft PRs for auto candidates (weekly mode only)
        draft_prs: list[str] = []
        if args.weekly:
            # Deduplicate: one PR per filename (pick first project with the file)
            seen_names: set[str] = set()
            dotfiles_target = next((t for t in shared_targets if t["name"] == "dotfiles"), None)
            if dotfiles_target:
                for c in candidates:
                    if c["status"] != "candidate-auto":
                        continue
                    if c["path"].name in seen_names:
                        continue
                    seen_names.add(c["path"].name)
                    url = open_promotion_pr(c, dotfiles_target, args.dry_run)
                    if url:
                        draft_prs.append(url)

        report = format_report(mode, project_states, candidates, drift, draft_prs)
        print(report)

        if not args.dry_run:
            issue_num = find_or_create_monthly_issue(DIRECTIVES_REPO, args.dry_run)
            if issue_num:
                append_comment(DIRECTIVES_REPO, issue_num, report, args.dry_run)

        return 0

    except Exception:
        tb = traceback.format_exc()
        print(tb, file=sys.stderr)
        if not args.dry_run:
            try:
                open_failure_issue(DIRECTIVES_REPO, tb)
            except Exception as e2:
                print(f"Additionally failed to open failure issue: {e2}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
