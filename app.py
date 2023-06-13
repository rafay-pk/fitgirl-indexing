import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

pwd = os.getcwd()
data_folder = pwd + "/data"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitGirl Repacks!!!")
        l_main = QVBoxLayout()
        l_main.setSpacing(0)
        l_main.setContentsMargins(0, 0, 0, 0)
        l_main.setAlignment(Qt.AlignmentFlag.AlignTop)
        w_main = QWidget()
        w_main.setLayout(l_main)
        self.setCentralWidget(w_main)

        w_searchbar = QWidget()
        l_searchbar = QHBoxLayout()
        l_searchbar.setContentsMargins(2, 2, 2, 2)
        w_searchbar.setLayout(l_searchbar)
        l_main.addWidget(w_searchbar)
        self.w_search = QLineEdit()
        self.w_search.returnPressed.connect(self.search)
        l_searchbar.addWidget(self.w_search)
        l_searchbar.addWidget(QLabel("Sort:"))
        w_sort = QComboBox()
        w_sort.addItems(["Name", "Developer", "Size"])
        l_searchbar.addWidget(w_sort)
        w_tags = QPushButton("Tags")
        w_tags.clicked.connect(self.tags)
        l_searchbar.addWidget(w_tags)

        l_grid = QGridLayout()
        l_main.addLayout(l_grid)
        l_grid.addWidget(QLabel("Title"), 0, 0)

    def search(self):
        print(self.w_search.text())

    def tags(self):
        print("tags")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
