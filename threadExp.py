import threading
import time
import signal
import multiprocessing
import os



def task(waitTime):
    print(f'Process {os.getpid()} Start')
    time.sleep(waitTime)
    os.kill(os.getppid(),signal.CTRL_BREAK_EVENT)

def sighandler(signum,frame):
    print(f'sighandler:signum={signum}')    
    raise OSError("おしまい！")

if __name__ == '__main__':
    signal.signal(signal.CTRL_BREAK_EVENT, sighandler)
    multiprocessing.Process(target=task,args=(5,)).start()

    while True:
        try:
            input('Input> ')
        except OSError as e:
            print(f'OSError発生')
            for s in e.args:
                print(f'{s}')
            







