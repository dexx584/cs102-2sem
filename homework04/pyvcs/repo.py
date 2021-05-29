import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    rep_dir = os.environ.get("GIT_DIR", ".git")
    workdir = pathlib.Path(workdir).absolute()
    if workdir != workdir.root:
        workdir = workdir / rep_dir
        if workdir.is_dir(): return workdir
    raise Exception("Not a git repository")

def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # PUT YOUR CODE HERE
    rep_dir = os.environ.get("GIT_DIR", ".git")
    workdir = pathlib.Path(workdir)
    if not workdir.is_dir(): raise Exception(f"{workdir.name} is not a directory")
    workdir = workdir / rep_dir
    os.makedirs(workdir / "refs" / "heads")
    os.makedirs(workdir / "refs" / "tags")
    os.makedirs(workdir / "objects")
    with open(workdir / "HEAD", "w") as f: f.write("ref: refs/heads/master\n")
    with open(workdir / "config", "w")as f:
        f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    with open(workdir / "description", "w") as f: f.write("Unnamed pyvcs repository.\n")
    return workdir