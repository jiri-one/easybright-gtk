
from PySide2.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("<font color=red size=40>Hello World!</font>")
label.show()
app.exec_()