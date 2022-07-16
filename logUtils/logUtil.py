

from logging import Logger, FileHandler, StreamHandler, Formatter
import logging


def getLogger(name: str, level=logging.INFO, logfile: str = "") -> Logger:
    """loggerを取得する

    Args:
        name (str): モジュール名
        level (_Level, optional): ログレベル. Defaults to logging.INFO.
        logfile (str, optional): ログファイル名(設定しないとファイル出力なし). Defaults to "".

    Returns:
        Logger: 取得したLogger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # formatは全てのハンドラで共通
    f = Formatter('%(asctime)s %(name)s %(filename)s:%(lineno)d %(funcName)s [%(levelname)s] %(message)s')

    # StreamHandler設定
    h = StreamHandler()
    h.setFormatter(f)
    logger.addHandler(h)

    # FileHandler設定
    if len(logfile) != 0:
        h = FileHandler(logfile)
        h.setFormatter(f)
        logger.addHandler(h)
    
    return logger
