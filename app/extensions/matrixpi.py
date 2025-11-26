import os

class MatrixpiExtension:
    def __init__(self, app=None):
        self.matrixboard = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        disable_matrix = os.environ.get("DISABLE_MATRIX", "0").lower() in ("1", "true", "yes")

        if disable_matrix:
            print("MatrixpiExtension: running in NO-HARDWARE mode (matrix disabled)")
            self.matrixboard = None
        else:
            from .matrixboard import MatrixBoard

            self.matrixboard = MatrixBoard(30, 30)
            self.matrixboard.init()
            print("MATRIX BOARD INITIALIZED")


matrixpi = MatrixpiExtension()
