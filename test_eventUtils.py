'''
eventUtils.pyのテストケース
'''
import time
import threading
from threadUtils import eventUtil


def task(event, name, sleepTime):
    """指定時間だけスリープした後eventをsetする

    Args:
        event (Event): setするイベント
        name (string): スレッド名称
        sleepTime (float): スリープ時間[sec]
    """
    print("Thread {} is start".format(name))
    time.sleep(sleepTime)
    event.set()

a = threading.Event()
b = threading.Event()

threading.Thread(target=task,name='TaskA',args=(a,'TaskA',3)).start()
threading.Thread(target=task,name='TaskB',args=(b,'TaskB',5)).start()

eventUtil.wait_all((a,b))

print('All events are set')


