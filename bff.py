import sys

import paho.mqtt.client as mqtt
from qtpy.QtWidgets import QApplication

from gui import ChatWindow
from mqtt import on_connect, on_message

app = QApplication(sys.argv)
window = ChatWindow()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=window)

client.on_connect = on_connect
client.on_message = on_message

window.client = client
window.show()
sys.exit(app.exec())
