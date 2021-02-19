from threading import Thread
from raspberry import *


dht11_thread = Thread(target=run_dht11_sensor)
light_thread = Thread(target=run_light_sensor)

threads = [dht11_thread, light_thread]

for t in threads:
    t.start()


for t in threads:
    t.join()
