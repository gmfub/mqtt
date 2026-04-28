APP = "MQChat"


def on_connect(client, userdata, flags, rc, properties=None):
    room = userdata.room_set.text()
    topic_listen = f"{APP}/{room}/+/message"
    client.subscribe(topic_listen)
    print(f"Connected! Subscribed to {topic_listen}")


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    nickname = msg.topic.split("/")[2]
    userdata.chat_history.append(f"<b>{nickname}:</b> {message}")
