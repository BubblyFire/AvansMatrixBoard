
from PIL import Image
from os.path import basename, join
import sys

def _create(orig, dst_dir):
    img = Image.open(orig)
    img.thumbnail((30, 30), Image.LANCZOS)
    Image.save(join(dst_dir,basename(orig)))


def to_thumbs(srcs, dst_dir, overwrite=False):
    try:
        for src in srcs:
            _create(src, dst_dir)
    except:
        sys.exception().__traceback__

if __name__ == "__main__":
    dummy = 0
    print('hallo')
    print(sys.argv)
    to_thumbs(sys.argv[1], sys.argv[2])
