'''
eventUtils.wait_all()のテストケース
'''
import time
import threading
from threadUtils import eventUtil
import sys


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

#------------ wait_all()のテスト --------------------
a = threading.Event()
b = threading.Event()

threading.Thread(target=task,name='TaskA',args=(a,'TaskA',3)).start()
threading.Thread(target=task,name='TaskB',args=(b,'TaskB',5)).start()
r = eventUtil.wait_all((a,b))
print(f"All events are set:{r}")

a.clear()
b.clear()
threading.Thread(
    target=task,name='TaskA',args=(a,'TaskA',3),daemon=True).start()
threading.Thread(
    target=task,name='TaskB',args=(b,'TaskB',5),daemon=True).start()
r = eventUtil.wait_all((a,b),1)
print(f"Timeout wait_all()->{r}")

sys.exit(0)
