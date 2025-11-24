from .matrixboard import MatrixBoard

class MatrixpiExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.matrixboard = MatrixBoard(30, 30)
        self.matrixboard.init()
        print("MATRIX BOARD INITIALIZED")

matrixpi = MatrixpiExtension()
