'''
このパッケージのモジュールからimportしたい兄弟パッケージ
を検索パスに追加するための処理を行う。
対象は
- logUtils

である。本モジュールをimportしておけば上記兄弟パッケージ
内部のモジュールをimport可能となる。
'''
import os
import sys
sys.path.append(os.path.abspath(f'{os.path.dirname(__file__)}/../logUtils'))
