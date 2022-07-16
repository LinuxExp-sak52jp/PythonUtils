from audioop import add
from multiprocessing import Pipe
from multiprocessing.connection import Listener
import logUtil


def server(
    name: str,
    sndPort: Pipe,
    address: str = 'localhost',
    port: int = 12345):
    
    logger = logUtil.getLogger(__name__)
    logger.info(f'Server起動=>name={name},ip={address}:{port}')

    listener = Listener(address=(address,port))
    isContinue = True
    while isContinue:
        conn = listener.accept()
        logger.debug('Clientと接続')

        # -- mainCtrlへ外部コンソールとの接続オブジェクト
        # を渡す
        sndPort.send([name,'addConn',conn])
