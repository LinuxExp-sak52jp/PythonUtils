

import sys
import os

import definepath
#sys.path.append(os.path.abspath(f'{os.path.dirname(__file__)}/../logUtils'))
import logging
from multiprocessing import Process, connection, Pipe
from typing import Any, List
import logUtil
from server import server
import time


def workerProcess(name: str, conn):
    logger = logUtil.getLogger(__name__, logging.DEBUG)
    logger.debug(f'プロセス開始:name={name}')

    #-- 接続儀式 --
    conn.send([name,'StartRequest'])
    if not conn.poll(3):
        logger.error(f'{name}:main processとの接続に失敗')
        return
    elif conn.recv().lower() != 'start':
        logger.error(f'{name}:main processからの返答が異常')
        return
    logger.debug(f'{name}:お仕事開始')
    #-- お仕事 --
    bt = time.time()
    cnt = 1
    while True:
        if not conn.poll(5):
            conn.send(
                [name,f'お知らせ回数:{cnt}',
                f'開始後の経過時間:{time.time()-bt}(sec)'])
            cnt += 1
            continue
        msg = conn.recv().lower()
        if msg == 'quit':
            logger.info('Quit受領 終了処理開始')
            conn.send([name,'ReadyToQuit'])
            msg1 = conn.recv().lower()
            if msg1 == 'finishtoquit':
                logger.debug('FinishToQuit受領')
                break
            logger.warning(f'mainから想定外の応答:{msg1}')
    
    logger.info(f'{name}プロセス終了')

def changeWorkerStatus(name: str, status: bool, workers: List):
    for w in workers:
        if w[0] == name:
            w[2] = status
            return

def printUsage(progName: str):
    print(f'Usage:{progName}')

def quitWorker(wp: List,console,targetName: str = ""):
    """Worker Process停止処理

    Args:
        wp (list): Worker Process管理情報
          wp[i]=[name,connection,status(True|False)]
        console (connection): console processへの接続オブジェクト
        targetName (str, optional): 対象となるworker識別名(""の時は全てが対象)
    """
    isFound = False
    for p in wp:
        if targetName == "" or p[0].lower() == targetName.lower():
            print(f'{p[0]}を停止します')
            if p[2] == True:
                p[1].send('Quit')
            else:
                print(f'{p[0]}は既に停止しています')
            isFound = True
    if isFound:
        s = '全てのworker'
        if len(targetName) != 0:
            s = targetName
        c.send(f'{s}を停止しました')
    else:
        print(f'{targetName}の停止を指示されましたが見つかりませんでした')
        c.send(f'{targetName}の停止を指示されましたが見つかりませんでした')


def isAllworkerQuited(procs: List):
    """全てのワーカーが停止しているかどうかを調べる

    Args:
        procs (List): worker process情報
    """
    isComplete = True
    for wp in procs:
        if wp[2] == True:
            isComplete = False
            break

    return isComplete

'''
TODO 7/15 
- printUsage()を完成させること
'''
if __name__ == '__main__':

    logger = logUtil.getLogger(__name__, logging.DEBUG)

    #-- Server addr/port 設定 --
    serverAddr = 'localhost'
    serverPort = 12345
    if len(sys.argv) > 1:
        for i in range(1,len(sys.argv)):
            if i == 1:
                # addr
                serverAddr = sys.argv[i]
            elif i == 2:
                # port
                try:
                    serverPort = int(sys.argv[i])
                except Exception as e:
                    printUsage(sys.argv[0])
                    exit(-1)
            else:
                # 間違い
                printUsage(sys.argv[0])
                exit(-1)

    #-- worker processを２つ作成 --
    # workerProcs = [[name,connection,status(True|False)],...]
    workerProcs = []
    workerPipes = []
    for i in range(2):
        (c1,c2) = Pipe()
        name = f'Worker_{i}'
        p = Process(
            target=workerProcess,
            args=(name,c2),
            daemon=True
        )
        p.start()
        workerProcs.append([name,c1,False,p])
        workerPipes.append(c1)

    #-- server processを起動 --
    (c1,c2) = Pipe()
    s = Process(
        target=server,
        args=('Server',c2,serverAddr,serverPort),
        daemon=True
    )
    s.start()
    serverProc = ('Server',c1,s)
    serverPipe = c1

    #-- メッセージループ開始準備 --
    isContinue = True
    isShutdown = False
    waitConns = []
    for c in workerPipes:
        waitConns.append(c)
    waitConns.append(serverPipe)

    #-- メッセージループ開始 --
    # msg = [processName, command, data,....]
    while isContinue:
        for c in connection.wait(waitConns):
            msg = c.recv()
            # -- 共通メッセージへの対応 --
            if msg[1].lower() == 'readytoquit':
                logger.debug(f'ReadyToQuit受領:{msg[0]}')
                waitConns.remove(c)
                c.send('FinishToQuit')
                # 送信元がworkerだったらstatusを更新
                changeWorkerStatus(msg[0], False, workerProcs)
                # shutdown flagが立っていて全てのworkerが停止していたら
                # 全ての処理を終了する
                if isShutdown:
                    # isComplete = True
                    # for i in range(len(workerProcs)):
                    #     wp = workerProcs[i]
                    #     if wp[2] == True:
                    #         isComplete = False
                    #         break
                    isComplete = isAllworkerQuited(workerProcs)
                    if isComplete:
                        isContinue = False
            elif msg[1].lower() == 'startrequest':
                logger.debug(f'StartRequest受領:{msg[0]}')
                c.send('Start')
                # 送信元がworkerだったらstatusを更新
                changeWorkerStatus(msg[0], True, workerProcs)
            # -- server process --
            elif msg[0] == serverProc[0]:
                if msg[1].lower() == 'addconn':
                    logger.debug(f'AddConn受領:{msg[0]}')
                    waitConns.append(msg[2])
            # -- worker process --
            elif msg[0].find('Worker_') == 0:
                print(f'Message from {msg[0]}: ',end='')
                for s in range(1,len(msg)):
                    print(msg[s],end=' ')
                print()
            # -- console process --
            else:
                #logger.debug(f'Consoleから受領:{msg[0]}')
                # -- 指定されたworker procを停止する --
                if msg[1].lower() == 'quitworker':
                    logger.debug(f'Consoleから受信:{msg[1]}')
                    quitWorker(workerProcs,c,msg[2])
                # -- 全てのworker procを停止する --
                elif msg[1].lower() == 'quitall':
                    logger.debug(f'Consoleから受信:{msg[1]}')
                    quitWorker(workerProcs,c)
                # -- statusを返す --
                elif msg[1].lower() == 'status':
                    logger.debug(f'Consoleから受信:{msg[1]}')
                    c.send([(wp[0],wp[2]) for wp in workerProcs])
                # -- プロセス全体を終了する --
                elif msg[1].lower() == 'shutdown':
                    print('シャットダウンを開始します')
                    waitConns.remove(c)
                    if isAllworkerQuited(workerProcs):
                        c.send('全てのworkerは停止済みです')
                        isContinue = False
                        break
                    isShutdown = True
                    # workerの停止
                    quitWorker(workerProcs,c)
    #-- 終了処理 --
    # Server停止
    serverProc[2].kill()
    serverProc[2].join()

    # connection close
    serverProc[1].close()
    for wp in workerProcs:
        wp[1].close()

    print('正常にシャットダウンしました')   

