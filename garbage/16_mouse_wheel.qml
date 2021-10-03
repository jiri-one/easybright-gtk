import QtQuick 2.0

SystemTrayIcon {
	visible: true
	icon.source: "qrc:/images/tray-icon.png"

	onMessageClicked: console.log("Message clicked")
	Component.onCompleted: showMessage("Message title", "Something important came up. Click this to know more.")
}

SystemTrayIcon {
	visible: true
	icon.source: "qrc:/home/jiri/Workspace/EasyBright/easybright_gtk/tray.png"

	menu: Menu {
		MenuItem {
			text: qsTr("Quit")
			onTriggered: Qt.quit()
		}
	}
}