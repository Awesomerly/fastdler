import argparse
from pathlib import Path
from watchfiles import watch
from fastdler.handler import *


parser = argparse.ArgumentParser()

parser.add_argument("source", type=Path)
parser.add_argument("dest", type=Path)
args = parser.parse_args()


def del_bz2(path):
    if path.is_file():
        try:
            remove(add_ext(path, ".bz2"))
        except:
            remove(path)
    else:
        remove(path)


def main():
    try:
        for changes in watch(args.source):
            changes = list(changes)
            for change in changes:
                change_type = change[0]
                change_path = Path(change[1])

                relative_path = change_path.relative_to(args.source)
                change_dest = args.dest / relative_path

                if change_type == 1:
                    # added
                    if change_path.is_dir():
                        continue
                    duplicate(change_path, change_dest)
                    compress(change_dest)
                    remove(change_dest)
                elif change_type == 2:
                    # modified
                    if change_path.is_dir():
                        continue
                    del_bz2(change_dest)
                    duplicate(change_path, change_dest)
                    compress(change_dest)
                else:
                    # deleted
                    del_bz2(change_dest)

    except Exception as e:
        print(e)
