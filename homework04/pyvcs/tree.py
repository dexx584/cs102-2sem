import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    # PUT YOUR CODE HERE
    temp = b""
    for i in index:
        if "/" in i.name:
            s_dir = b""
            s_dir += oct(i.mode)[2:].encode() + b" "
            s_dir += i.name[i.name.find("/") + 1:].encode() + b"\0"
            s_dir += i.sha1
            temp += b"40000 "
            temp += i.name[: i.name.find("/")].encode() + b"\0"
            temp += bytes.fromhex(hash_object(s_dir, "tree", True))
        else:
            temp += oct(i.mode)[2:].encode() + b" "
            temp += i.name.encode() + b"\0"
            temp += i.sha1
    return hash_object(temp, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    timezone = (time.strftime("%z", time.gmtime()))
    if author is None:
        author = os.environ["GIT_AUTHOR_NAME"] + " " + os.environ["GIT_AUTHOR_EMAIL"]
    data = f"tree {tree}\n"
    if parent is not None:
        data += f"parent {parent}\n"
    data += f"author {author} {str(int(time.mktime(time.localtime())))} {timezone}\n" \
            f"committer {author} {str(int(time.mktime(time.localtime())))} {timezone}\n" \
            f"\n{message}\n"
    return hash_object(data.encode(), "commit", True)
