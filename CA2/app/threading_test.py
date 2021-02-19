from threading import Thread
from raspberry import *


t1 = Thread(target = get_light_data)
t2 = Thread(target = store_light_data)
t3 = Thread(target = get_dht_data)
t4 = Thread(target = store_dht_data)


threads = [t1, t2, t3, t4]

for t in threads:
    t.start()


for t in threads:
    t.join()
