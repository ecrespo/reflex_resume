"""Step 1 of the GitHub EDA: list the repositories and mirror their history.

Every public repository of `ecrespo` and every repository of the `prismal-ai`
organisation is cloned with `git clone --bare --filter=blob:none`: the commit
graph and the directory trees, no file contents (the manifests read later are
fetched one blob at a time). A second run fetches instead of cloning.

    uv run python utils/github_eda/collect.py --workdir ~/.cache/github-eda

Writes `<workdir>/repos.json` (GitHub metadata) and `<workdir>/repos/<owner>/<name>.git`.
Needs the GitHub CLI (`gh`) logged in; no token is stored.
"""

import argparse
import json
import shutil
import subprocess  # nosec B404
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OWNERS = (("ecrespo", "public"), ("prismal-ai", None))
FIELDS = "name,nameWithOwner,isFork,stargazerCount,forkCount,primaryLanguage,pushedAt,createdAt,description"


def list_repos() -> list[dict]:
    repos = []
    for owner, visibility in OWNERS:
        cmd = ["gh", "repo", "list", owner, "--limit", "1000", "--json", FIELDS]
        if visibility:
            cmd += ["--visibility", visibility]
        out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout  # nosec B603
        for repo in json.loads(out):
            repo["owner"] = owner
            repos.append(repo)
    return repos


def mirror(repo: dict, root: Path) -> tuple[str, bool]:
    target = root / repo["owner"] / f"{repo['name']}.git"
    url = f"https://github.com/{repo['nameWithOwner']}.git"
    if target.exists():
        cmd = ["git", "-C", str(target), "fetch", "--quiet", "--prune", "--tags", "origin",
               "+refs/heads/*:refs/heads/*"]  # fmt: skip
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["git", "clone", "--quiet", "--bare", "--filter=blob:none", url, str(target)]
    result = subprocess.run(cmd, capture_output=True, text=True)  # nosec B603
    if result.returncode != 0 and not (target / "HEAD").exists():
        shutil.rmtree(target, ignore_errors=True)
    return repo["nameWithOwner"], result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workdir", type=Path, default=Path.home() / ".cache" / "github-eda")
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    args.workdir.mkdir(parents=True, exist_ok=True)

    repos = list_repos()
    (args.workdir / "repos.json").write_text(json.dumps(repos, indent=1))
    with ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda r: mirror(r, args.workdir / "repos"), repos))
    failed = [name for name, ok in results if not ok]
    print(f"{len(repos)} repositories, {len(repos) - len(failed)} mirrored")
    for name in failed:
        print(f"  failed: {name}")


if __name__ == "__main__":
    main()
