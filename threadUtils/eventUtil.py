from threading import Thread, current_thread, Event, Barrier
from time import sleep, time
import threading
from typing import List, Tuple

def __waitEventAllTask(event: Event, barrier: Barrier):
    print(f"Waiting event{current_thread().name}")
    r = event.wait()
    print(f"event{current_thread().name} Set")
    try:
        barrier.wait()
    except:
        return

def __waitEventAnyTask(refEvent: Event, repoEvent: Event):
    print(f"Waiting event{current_thread().name}")
    refEvent.wait()
    print(f"event{current_thread().name} Set")
    repoEvent.set()

def wait_all(events: Tuple[Event], timeover=None) -> bool:
    """全てのイベントがセットされるまで待機する

    Args:
        events (tuppel(Event)): 待機するEvent flagのリスト
        timeover (float, optional): タイムアウト時間. Defaults to None.

    Returns:
        bool: 全てのイベントが発火したらTrue、Timeout発生時はFalse。
    """
    b = Barrier(len(events)+1,timeout=timeover)
    idx = 0
    for e in events:
        Thread(
            target=__waitEventAllTask,
            args=(e,b),
            name=f"{idx}",
            daemon=True).start()
    try:
        b.wait()
    except threading.BrokenBarrierError:
        print("Timeout 発生!")
        return False
    return True

def wait_any(events: Tuple[threading.Event],timeover=None) -> int:
    repoEvent = threading.Event()
    idx = 0
    for e in events:
        Thread(
            target=__waitEventAnyTask,
            args=(e,repoEvent),
            name=f"{idx}",
            daemon=True).start()
        idx += 1
    r = repoEvent.wait(timeout=timeover)
    if r == True:
        for i in range(len(events)):
            if events[i].is_set() == True:
                return i
        return -2
    return -1
