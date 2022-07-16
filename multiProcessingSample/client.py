#!/usr/bin/env python

from multiprocessing.connection import Client
from sys import argv

def verifyInput(line: str) -> bool:
    if len(line) == 0:
        return False
    cmd = line.split()[0]
    validCmds = ('quitworker','quitall','status','exit')
    for c in validCmds:
        if cmd == c:
            return True
    return False

def printUsage():
    print('--- Valid commands below: ---')
    print('  Status                     : Main processの状態を取得')
    print('  QuitWorker <Worker Process>: 指定したWorker Processを停止する')
    print('  QuitAll                    : 全てのWorker Processを停止する')
    print('  Exit                       : このクライアントを終了する')

if __name__ == '__main__':
    
    '''
    引数でServerが指定されていたらそれに従う
    デフォルトは localhost:12345
    '''
    serverAddr = ('localhost',12345)
    for i in range(1,len(argv)):
        serverAddr[i-1] = argv[i]

    print(f'Server:{serverAddr}への接続待ちです')
    conn = Client(serverAddr)
    print('Serverに接続しました')

    # -- serverレスポンスのタイムアウト値(sec) --
    serverTimeout = 3
    while True:
        line = input('Input> ').strip().lower()
        if verifyInput(line) is not True:
            printUsage()
            continue
        # -- コマンド処理 --
        if line == 'status':
            conn.send(['Console',line])
            r = conn.recv()
            print('Serverのステータス:')
            print(r)
        elif line == 'quitall':
            print('全てのワーカープロセスの停止処理を開始しました')
            conn.send(['Console',line])
            reply = conn.recv()
            print(reply)
        elif line.startswith('quitworker '):
            msg = line.split()
            print(f'{msg[1]}の停止処理を開始しました')
            conn.send(['Console',msg[0],msg[1]])
            reply = conn.recv()
            print(reply)
        elif line == 'exit':
            print('終了処理を開始しました')
            conn.send(['Console','ReadyToQuit'])
            reply = conn.recv()
            if reply.lower() == 'finishtoquit':
                print('正常終了')
            else:
                print('異常終了')
            break
        else:
            printUsage()
