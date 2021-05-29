import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    # PUT YOUR CODE HERE
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    # PUT YOUR CODE HERE
    p_commit = commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, resolve_head(gitdir), author)
    update_ref(gitdir, get_ref(gitdir), p_commit)
    return p_commit


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    # PUT YOUR CODE HERE
    reference = get_ref(gitdir)
    if os.path.isfile(gitdir / reference):
        file = open(gitdir / reference, "r")
        reference = file.read()
        file.close()
    fmt, prev_content = read_object(reference, gitdir)
    objects = find_tree_files(prev_content.decode()[5:45], gitdir)
    fs = gitdir.absolute().parent
    for index in objects:
        os.remove(fs / index[0])
        _path = pathlib.Path(index[0]).parent
        while len(_path.parents) > 0:
            os.rmdir(_path)
            _path = pathlib.Path(_path).parent
    file = pathlib.Path(gitdir / "HEAD").open("w")
    file.write(obj_name)
    file.close()
    fmt, content = read_object(obj_name, gitdir)
    objects = find_tree_files(content.decode()[5:45], gitdir)
    for index in objects:
        par_path = fs
        for par in range(len(pathlib.Path(index[0]).parents) - 2, -1, -1):
            par_path /= pathlib.Path(index[0]).parents[par]
            if not os.path.isdir(par_path):
                os.mkdir(par_path)
        fmt, obj_content = read_object(index[1], gitdir)
        if fmt == "blob":
            pathlib.Path(fs / index[0]).touch()
            file = open(fs / index[0], "w")
            file.write(obj_content.decode())
            file.close()
        else:
            os.mkdir(fs / index[0])
