import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a QWebEngineView widget
        self.view = QWebEngineView(self)
        # Set the HTML file path
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "nx.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.view.load(local_url)
        # Set the QWebEngineView widget as the central widget
        self.setCentralWidget(self.view)
        # Set window title
        self.setWindowTitle('Graph Visualization')
        # Set window size
        self.resize(800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec_())
