import os
from .matrixboard import MatrixBoard

MATRIX_WIDTH = 30
MATRIX_HEIGHT = 30


def _hardware_disabled() -> bool:
    return os.environ.get("DISABLE_MATRIX", "0").lower() in ("1", "true", "yes")


class MatrixpiExtension:
    def __init__(self, app=None):
        self.matrixboard = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._build(reason="INITIALIZED")

    def reload(self):
        self._build(reason="RELOADED")

    # MatrixBoard is always created so routes can update the shadow buffer
    # (used by the live web preview). Hardware init is skipped when
    # DISABLE_MATRIX is set, or when hardware init raises (e.g. no GPIO).
    def _build(self, reason: str):
        want_hardware = not _hardware_disabled()
        try:
            self.matrixboard = MatrixBoard(MATRIX_WIDTH, MATRIX_HEIGHT, hardware=want_hardware)
            self.matrixboard.init()
            if want_hardware:
                print(f"MATRIX BOARD {reason}")
            else:
                print(f"MatrixpiExtension: {reason} in NO-HARDWARE mode (matrix disabled)")
        except Exception as e:
            print(f"MatrixpiExtension: hardware init failed ({e}); falling back to NO-HARDWARE mode")
            self.matrixboard = MatrixBoard(MATRIX_WIDTH, MATRIX_HEIGHT, hardware=False)
            self.matrixboard.init()


matrixpi = MatrixpiExtension()
