# apigw-log-visualizer

## 開発環境の前提条件

- VSCodeでの開発
  - 次の拡張機能のインストール
    - Black
    - Pylance
    - isort
    - Python

## 開発環境の構築

開発を始める前に、必要なライブラリのインストールとコミット前にフォーマットとLintをチェックするために下記コマンドを実行してください。

```shell: terminal
poetry install
poetry run pre-commit install
```

### blackの設定

コミット時にチェックするため設定は任意ですが、事前に設定しておくと保存時に都度フォーマットをかけてくれるので便利です。

1. `Preferences or Settings -> Tools -> File Watchers` を開き `+` をクリックしてwatcherを追加します:
   - Name: Black
   - File type: Python
   - Scope: Project Files
   - Program: (which poetryで出力されるパス)
   - Arguments: `run black $FilePath$`
   - Output paths to refresh: `$FilePath$`
   - Working directory: `$ProjectFileDir$`
   - In Advanced Options
     - "Auto-save edited files to trigger the watcher" のチェックを外す
     - "Trigger the watcher on external changes" のチェックを外す

以上
