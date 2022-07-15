import multiprocessing
from multiprocessing import Process, connection, Pipe
import sys
import os
from server import server


def workerProcess(*args):
    pass

if __name__ == '__main__':
    #-- worker processを２つ作成 --
    workerProcs = []
    workerConns = []
    for i in range(2):
        (c1,c2) = Pipe()
        name = f'Worker_{i}'
        p = Process(
            target=workerProcess,
            args=(name,c2),
        )
        p.start()
        workerProcs.append((name,p))
        workerConns.append(c1)
    
    #-- server processを起動 --
    (c1,c2) = Pipe()
    s = Process(
        target=server,
        args=('Server',c2),
    )
    s.start()
    serverProc = ('Server',s)
    serverConn = c1

    #-- メッセージループ開始準備 --
    isContinue = True
    waitConns = []
    for c in workerConns:
        waitConns.append(c)
    waitConns.append(serverConn)
    msg = ['StartWork']
    for c in workerConns:
        c.send(msg)
    #-- メッセージループ開始 --
    # msg = [processName, command, data,....]
    while isContinue:
        for c in connection.wait(waitConns):
            msg = c.recv()
            # -- 共通メッセージへの対応 --
            if msg[1].lower() == 'readytoquit':
                c.send(['FinishToQuit'])
                waitConns.remove(c)
            # -- server process --
            elif msg[0] == serverProc[0]:
                if msg[1].lower() == 'addconn':
                    waitConns.append(msg[2])
            # -- worker process --
            elif msg[0].find('Worker_') == 0:
                print(f'Message from {msg[0]}: ',end='')
                for s in range(1,len(msg)):
                    print(s)
            # -- console process TODO 7/13 --
            else:
                pass
            pass
        pass

    pass