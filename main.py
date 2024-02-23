import sys

from PySide6 import QtWidgets

from general_windows import GeneralWindow
from variables import Variables


def load_general_menu():
    app = QtWidgets.QApplication([])
    screen = app.primaryScreen()
    size = screen.size()
    Variables.screen_width = size.width()
    Variables.screen_height = size.height()
    Variables.general_window = GeneralWindow()
    Variables.general_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    load_general_menu()
