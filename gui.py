from qtpy.QtWidgets import (
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from mqtt import APP


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = None
        self.setWindowTitle("MQChat")

        layout_settings = QVBoxLayout()
        layout_main = QVBoxLayout()
        layout_chat = QVBoxLayout()

        page_settings = QWidget()
        page_chat = QWidget()

        self.stack = QStackedWidget()
        self.stack.addWidget(page_settings)
        self.stack.addWidget(page_chat)

        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Message...")

        self.broker_set = QLineEdit()
        self.broker_set.setPlaceholderText("Broker")

        self.port_set = QLineEdit()
        self.port_set.setPlaceholderText("Port")

        self.room_set = QLineEdit()
        self.room_set.setPlaceholderText("Room")

        self.username_set = QLineEdit()
        self.username_set.setPlaceholderText("Nickname")

        self.msg_input.returnPressed.connect(self.handle_send)

        self.btn_connect = QPushButton("Connect")

        self.btn_connect.clicked.connect(self.handle_connection)
        self.username_set.returnPressed.connect(self.handle_connection)

        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_disconnect.clicked.connect(self.handle_disconnect)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        layout_chat.addWidget(self.chat_history)
        layout_chat.addWidget(self.msg_input)
        layout_chat.addWidget(self.btn_disconnect)

        layout_settings.addWidget(self.room_set)
        layout_settings.addWidget(self.broker_set)
        layout_settings.addWidget(self.port_set)
        layout_settings.addWidget(self.username_set)
        layout_settings.addWidget(self.btn_connect)

        layout_main.addWidget(self.stack)

        page_settings.setLayout(layout_settings)
        page_chat.setLayout(layout_chat)
        self.setLayout(layout_main)

    def handle_send(self):
        msg = self.msg_input.text()
        username = self.username_set.text()
        room = self.room_set.text()
        if msg and username and room:
            topic = f"{APP}/{room}/{username}/message"
            self.client.publish(topic, msg)
            self.msg_input.clear()

    def handle_connection(self):
        broker = self.broker_set.text()
        port_text = self.port_set.text()

        if broker and port_text:
            port = int(port_text)
            self.stack.setCurrentIndex(1)
            self.client.connect(broker, port)
            self.client.loop_start()

    def handle_disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
        self.stack.setCurrentIndex(0)
