from matrixboard import MatrixBoard

matrixboard = MatrixBoard(30, 30)
matrixboard.init()

matrixboard.render_text(0, 0, "hello", (255, 0, 255))
matrixboard.render_text(0, 1, "hello", (0, 0, 255))
matrixboard.render_text(0, 2, "hello", (0, 0, 255))
matrixboard.show()
