from capture import Node


node = Node()
node.setup_sensor()
node.connect_wifi()
node.loop()
