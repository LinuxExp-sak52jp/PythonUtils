from audioop import add
from multiprocessing import Pipe
from multiprocessing.connection import Listener


def server(
    name: str,
    sndPort: Pipe,
    address: str = 'localhost',
    port: int = 12345):

    listener = Listener(address=(address,port))
    isContinue = True
    while isContinue:
        conn = listener.accept()
        # -- mainCtrlへ外部コンソールとの接続オブジェクト
        # を渡す
        sndPort.send([name,'addConn',conn])
