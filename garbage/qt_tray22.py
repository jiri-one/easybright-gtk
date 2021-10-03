from PySide2.QtGui import QWheelEvent, QIcon
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("tray.png")

def func(reason):
	print("func has been called!")
	print(reason.text())

# Create the tray

tray = QSystemTrayIcon(parent=app)
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
action = QAction("A menu item")
menu.addAction(action)

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec_()