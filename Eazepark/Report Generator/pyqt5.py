from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton
from PyQt5.uic import loadUi

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("F:\PyQt5 Designer\Login Page.ui", self)  # Replace 'your_file.ui' with your .ui file name

def main():
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
