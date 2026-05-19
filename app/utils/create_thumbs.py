
import sys
import traceback
from os.path import basename, join

from PIL import Image


def _create(orig, dst_dir):
    img = Image.open(orig)
    img.thumbnail((30, 30), Image.LANCZOS)
    # Save the resized image instance (not the Image class itself).
    img.save(join(dst_dir, basename(orig)))


def to_thumbs(srcs, dst_dir, overwrite=False):
    try:
        for src in srcs:
            _create(src, dst_dir)
    except Exception:
        # Print the traceback instead of silently discarding it.
        traceback.print_exc()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        print("Usage: python create_thumbs.py <src> [<src> ...] <dst_dir>")
        sys.exit(1)
    # All arguments except the last are source files; the last is the target dir.
    to_thumbs(sys.argv[1:-1], sys.argv[-1])
