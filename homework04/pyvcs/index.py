import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        # PUT YOUR CODE HERE
        temp = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino & 0xFFFFFFFF,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode()
        )
        return struct.pack("!10I20sh" + str(len(self.name)) + "s" + str(8 - (62 + len(self.name)) % 8) + "x", *temp)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        # PUT YOUR CODE HERE
        (
            ctime_s,
            ctime_n,
            mtime_s,
            mtime_n,
            dev,
            ino,
            mode,
            uid,
            gid,
            size,
            sha1,
            flags,
        ) = struct.unpack(">10i20sh", data[:62])
        data = data[62:]
        l_b = data.find(b"\x00\x00\x00")
        name = data[:l_b].decode()
        return GitIndexEntry(
            ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    index_arr = []
    if not pathlib.Path(gitdir / "index").exists(): return index_arr
    with (gitdir / "index").open("rb") as f:
        header = f.read(12)
        data = f.read()
    u_head = (struct.unpack(">i", header[8:])[0])
    for i in range(u_head):
        end = len(data)
        for j in range(63, end, 8):
            if data[j] == 0:
                end = j
                break
        index_arr.append(GitIndexEntry.unpack(data[:end]))
        data = data[end + 1:]
    return index_arr


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    head = struct.pack("!4sLL", b"DIRC", 2, len(entries))
    data = b""
    for index in entries:
        data = data + GitIndexEntry.pack(index)
    sha = hashlib.sha1(head + data).digest()
    with open(gitdir / "index", "wb") as file:
        file.write(head + data + sha)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    data = read_index(gitdir)
    if details:
        for file in data:
            print(oct(file.mode)[2:], file.sha1.hex(), "0\t" + file.name)
    else:
        for file in data:
            print(file.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    result = []
    if os.path.isfile(gitdir / "index"):
        result = read_index(gitdir)
    else:
        pathlib.Path(gitdir / "index").touch()
    for road in paths:
        info = os.stat(road)
        file = open(road, "r")
        data = file.read()
        file.close()
        sha = hashlib.sha1((f"blob {len(data)}\0" + data).encode())
        entry = GitIndexEntry(
            int(info.st_ctime),
            0,
            int(info.st_mtime),
            0,
            info.st_dev,
            info.st_ino,
            info.st_mode,
            info.st_uid,
            info.st_gid,
            info.st_size,
            sha.digest(),
            0,
            str(road.as_posix()),
        )
        if entry in result:
            continue
        hash_object(data.encode(), "blob", True)
        it = 0
        while it < len(result):
            if result[it].name == entry.name:
                result[it] = entry
                break
            it += 1
        if it == len(result): result.append(entry)
    result.sort(key=lambda x: x.name)
    write_index(gitdir, reuslt)
