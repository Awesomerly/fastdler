import shutil
import bz2
import os


def add_ext(path, ext):
    return path.parent / (path.name + ext)


def compress(path):
    if path.is_file():
        with (
            open(path, "rb") as fr,
            bz2.BZ2File(add_ext(path, ".bz2"), "wb") as fw,
        ):
            shutil.copyfileobj(fr, fw)
        remove(path)


def duplicate(src, dest):
    try:
        shutil.copy(src, dest)
    except IOError as io_err:
        os.makedirs(os.path.dirname(dest))
        shutil.copy(src, dest)


def remove(path):
    if path.is_dir():
        print("Removing dir ", path)
        shutil.rmtree(path)
    if path.is_file():
        print("Removing file ", path)
        os.remove(path)
