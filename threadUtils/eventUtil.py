from threading import Thread, current_thread
from time import sleep, time
import threading

def __waitEventAllTask(event: threading.Event, barrier):
    print(f"Waiting event{current_thread().name}")
    r = event.wait()
    print(f"event{current_thread().name} Set")
    try:
        barrier.wait()
    except:
        return


def wait_all(events, timeover=None) -> bool:
    """全てのイベントがセットされるまで待機する

    Args:
        events (tuppel(Event)): 待機するEvent flagのリスト
        timeover (float, optional): タイムアウト時間. Defaults to None.

    Returns:
        bool: 全てのイベントが発火したらTrue、Timeout発生時はFalse。
    """
    b = threading.Barrier(len(events)+1,timeout=timeover)
    idx = 0
    for e in events:
        t = Thread(
            target=__waitEventAllTask,
            args=(e,b),name=f"{idx}",daemon=True).start()
        idx += 1
    try:
        b.wait()
    except threading.BrokenBarrierError:
        print("Timeout 発生!")
        return False
    return True

def wait_any(events,timeover=None) -> int:
    pass