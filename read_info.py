# Run this file by typing sudo python useage.py in terminal

from __future__ import print_function
from time import sleep
import paho.mqtt.client as paho

last_idle = last_total = 0
broker = "whale.simasware.com"
port = 1883

def on_publish(client, userdata, mid):
	print("mid: " + str(mid))

client = paho.Client()
client.on_publish = on_publish
client.connect(broker, port)
client.loop_start()


while True:
	with open('/proc/stat') as f:
		fields = [float(column) for column in f.readline().strip().split()[1:]]
	idle, total = fields[3], sum(fields)
	idle_delta, total_delta = idle - last_idle, total - last_total
	last_idle, last_total = idle, total
	utilization = 100.0 * (1.0 - idle_delta / total_delta)
	print("%.3f" % utilization)
	(rc, mid) = client.publish("rpi/useage", str(utilization), qos=1)
	sleep(1.1)

