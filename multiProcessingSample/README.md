# multiprocessing moduleを使った複数プロセス制御サンプル

main moduleが複数のプロセスからメッセージを受け取って処理するシステムのサンプル。下記の構成を持つ。  

```
main process
  server process
  worker process_1
  worker process_2
  ...
  console process_1
  ...
  console process_N
```
## 1.1. main process
- 起動時に一つのserver process(制御コンソールプロセス接続管理用)、及び複数のworker processを起動する。この時各プロセスには通信用のパイプを設定する。
- メッセージループへ入る。作成したserver process及びworker processのパイプを待ち受けに用いる。
- server processからconnection moduleを受信したら、それを待ち受け配列に加える。
- メッセージループでは、各プロセスに対応したメッセージ処理を行う。それぞれのプロセスに対するメッセージ処理規則は下記の通り。
  - server process
    - connection moduleを受信したら、それを待ち受け配列に加える。
  - worker process
    - 後述する共通メッセージ以外のメッセージは標準出力に出力する。
  - control console process
    - *QuitWorker Name*は*Name*を持つworker processを停止する。
    - *QuitAll*は全てのサブプロセスを停止させた後、main process自身を終了させる。
    - *Status*を受け取ったら現在の状態をconsole processへ返す。
  - 共通規則
    - *ReadyToQuit*を受けたら送信プロセスに対し*FinishToQuit*を送信し、pipeを待ち行列から削除する。
 
 ## 1.2. server process
外部クライアントプロセスからの接続を待機し、接続に成功したら生成した接続オブジェクト(実体はソケット)をmain processへ送付する。なお、この外部クライアントがcontrol consoleとなる。

## 1.3. worker process
このサンプルでは、定期的にmain controlへの文字列送信を行うのみ。

## 1.4. console process
標準入力から入力された命令をフォーマットしてmain processへ送付する。命令とその機能は下記の通り。

- Status: main processが管理する全てのworker process名称を取得して表示する。
- QuitWorker: 指定したworkerを停止させる。
- QuitAll: 全てのworkerを停止させる。




