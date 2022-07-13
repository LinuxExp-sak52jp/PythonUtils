import signal
import time

def handler(signum, frame):
  print(f'handlerが呼び出されました(signum={signum})')
  raise OSError("シグナルの割り込みがありました")

# signal.SIGALRMのシグナルハンドラを登録
signal.signal(signal.SIGA, handler)
# 5秒後にsignal.SIGALRMで割り込み予約
signal.alarm(5)

try:
    pass
except OSError as e:
    print(e.args)

# 時間のかかる処理／割り込みによって中断したい処理
while True:

  print("hellow.")
  time.sleep(0.7)

# signal.SIGALRMのアラーム設定を解除
signal.alarm(0)