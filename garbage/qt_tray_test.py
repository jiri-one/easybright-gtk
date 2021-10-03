import logging
import sys

from PySide2.QtGui import QIcon, QWheelEvent
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QAction, QMessageBox


def run_something():
	print("Running something...")


def show_message():
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Information)

	msg.setWindowTitle("MessageBox demo")
	msg.setText("This is a message box")

	msg.setInformativeText("This is additional information")
	msg.setDetailedText("The details are as follows:")
	msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
	msg.exec_()


def show_tray_message(tray: QSystemTrayIcon):
	tray.showMessage("Hoooo", "Message from tray")


if __name__ == '__main__':

	app = QApplication([])
	app.setQuitOnLastWindowClosed(False)

	tray = QSystemTrayIcon(QIcon("tray.png"), app)
	menu = QMenu()

	action_test = QAction("Show a message box")
	action_test.triggered.connect(show_message)
	menu.addAction(action_test)

	action_tray_message = QAction("Show a message from tray")
	action_tray_message.triggered.connect(lambda: show_tray_message(tray))
	menu.addAction(action_tray_message)

	action_exit = QAction("Exit")
	action_exit.triggered.connect(app.exit)
	menu.addAction(action_exit)

	tray.setContextMenu(menu)
	tray.setToolTip("Tool tip")
	tray.show()

	sys.exit(app.exec_())