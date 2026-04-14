import os
from .matrixboard import MatrixBoard

class MatrixpiExtension:
    def __init__(self, app=None):
        self.matrixboard = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        disable_matrix = os.environ.get("DISABLE_MATRIX", "0").lower() in ("1", "true", "yes")

        # MatrixBoard is always created so routes can update the shadow buffer
        # (used by the live web preview). Hardware init is skipped when

        try:
            self.matrixboard = MatrixBoard(30, 30, hardware=not disable_matrix)
            self.matrixboard.init()
            if disable_matrix:
                print("MatrixpiExtension: running in NO-HARDWARE mode (matrix disabled)")
            else:
                print("MATRIX BOARD INITIALIZED")
        except Exception as e:
            print(f"MatrixpiExtension: hardware init failed ({e}); falling back to NO-HARDWARE mode")
            self.matrixboard = MatrixBoard(30, 30, hardware=False)
            self.matrixboard.init()

    def reload(self):
        from .matrixboard import MatrixBoard
        disable_matrix = os.environ.get("DISABLE_MATRIX", "0").lower() in ("1", "true", "yes")
        try:
            self.matrixboard = MatrixBoard(30, 30, hardware=not disable_matrix)
            self.matrixboard.init()
            print("MATRIX BOARD RELOADED")
        except Exception as e:
            print(f"MatrixpiExtension: reload failed ({e}); keeping NO-HARDWARE mode")
            self.matrixboard = MatrixBoard(30, 30, hardware=False)
            self.matrixboard.init()


matrixpi = MatrixpiExtension()
