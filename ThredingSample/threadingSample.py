from threading import Thread
from time import sleep, time

def waitEventTask(event, barrier, idx):
    print("Waiting event{}".format(idx))
    event.wait()
    print("event{} Set".format(idx))
    barrier.wait()
    

def waitAllEvent(args):
    b = threading.Barrier(len(args)+1)
    idx = 0
    for e in args:
        Thread(target=waitEventTask,args=(e,b,idx)).start()
        idx += 1

    b.wait()


def task(event, name, sleepTime):
    print("Thread {} is start".format(name))
    sleep(sleepTime)
    event.set()

a = threading.Event()
b = threading.Event()

Thread(target=task,name='TaskA',args=(a,'TaskA',3)).start()
Thread(target=task,name='TaskB',args=(b,'TaskB',5)).start()

waitAllEvent((a,b))

print('All events are set')


