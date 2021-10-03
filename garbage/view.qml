import QtQuick 2.0

SystemTrayIcon {
	visible: true
	icon.source: "qrc:tray.png"

	menu: Menu {
		MenuItem {
			text: qsTr("Quit")
			onTriggered: Qt.quit()
		}
	}
}