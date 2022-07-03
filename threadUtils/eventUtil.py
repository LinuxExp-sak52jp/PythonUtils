#from multiprocessing.dummy import Event
from threading import Thread
from time import sleep, time
import threading

def __waitEventTask(event, barrier, idx):
    print("Waiting event{}".format(idx))
    event.wait()
    print("event{} Set".format(idx))
    barrier.wait()
    

def wait_all(events, timeout=0):
    b = threading.Barrier(len(events)+1)
    idx = 0
    for e in events:
        Thread(target=__waitEventTask,args=(e,b,idx)).start()
        idx += 1
    b.wait()
