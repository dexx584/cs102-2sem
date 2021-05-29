import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    # PUT YOUR CODE HERE
    header = f"{fmt} {len(data)}\0"
    temp = hashlib.sha1(header.encode() + data).hexdigest()
    if write:
        obj_dir = repo_find() / "objects" / temp[0:2]
        if not obj_dir.exists(): obj_dir.mkdir()
        with open(obj_dir / temp[2:], "wb") as file:
            file.write(zlib.compress((fmt + " " + str(len(data))).encode() + b"\00" + data))
    return temp


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    if len(obj_name) not in range(4, 41) or not os.path.isdir(gitdir / "objects" / obj_name[:2]):
        raise AssertionError(f"Not a valid object name {obj_name}")
    _dir = gitdir / "objects" / obj_name[:2]
    _list = []
    for file in os.listdir(_dir):
        if os.path.isfile(_dir / file) and file == obj_name[2:] or file[0:len(obj_name[2:])] == obj_name[2:]:
            _list.append(obj_name[:2] + file)
    if len(_list) == 0:
        raise AssertionError(f"Not a valid object name {obj_name}")
    return _list


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    return resolve_object(obj_name, gitdir)[0]


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    road = find_object(sha, gitdir)
    file = open(gitdir / "objects" / road[0:2] / road[2:], "rb")
    data = zlib.decompress(file.read())
    right, left = data.find(b" "), data.find(b"\x00")
    content = data[left + 1:]
    fmt = data[0:right].decode()
    file.close()
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    result = []
    while len(data) > 0:
        start = data.find(b"\x00")
        fmt_code, fmt_name = data[:start].split(b" ")
        sha = data[start + 1: start + 21]
        result.append((int(fmt_code.decode()), fmt_name.decode(), sha.hex()))
        data = data[start + 21:]
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    dir = repo_find()
    data = read_object(obj_name, dir)
    if data[0] == "commit" or data[0] == "blob":
        print(data[1].decode())
    else:
        for tree in read_tree(data[1]):
            if tree[0] == 40000:
                print(f"{tree[0]:06}", "tree", tree[2] + "\t" + tree[1])
            else:
                print(f"{tree[0]:06}", "blob", tree[2] + "\t" + tree[1])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    fmt, data = read_object(tree_sha, gitdir)
    objects = read_tree(data)
    arr = []
    for i in objects:
        if i[0] == 100644 or i[0] == 100755:
            arr.append((i[1], i[2]))
        else:
            sub_objects = find_tree_files(i[2], gitdir)
            for sub_obj in sub_objects:
                arr.append((i[1] + "/" + sub_obj[0], sub_obj[1]))
    return arr


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
