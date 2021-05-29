import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    pathlib.Path(gitdir / ref).touch()
    with open(gitdir / ref, "w") as file:
        file.write(new_value)
        file.close()


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    with open(gitdir / name, "w") as file:
        file.write(ref)
        file.close()


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    if refname == "HEAD" and not is_detached(gitdir):
        return resolve_head(gitdir)
    if (gitdir / refname).exists():
        with (gitdir / refname).open() as file:
            return file.read().strip()
    return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    if pathlib.Path.exists(gitdir / get_ref(gitdir)):
        return ref_resolve(gitdir, "HEAD")
    return None


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    if get_ref(gitdir) == "":
        return True
    return False


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD", "r") as file:
        data = file.read().strip().split()
        if len(data) == 2: return data[1]
        else: return ""
