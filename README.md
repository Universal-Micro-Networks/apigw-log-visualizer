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

## Docker関連コマンド

make docker-up
make docker-reset

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

## Batchの実行

### S3からログファイルのダウンロード

#### 前提条件: AWSへの接続設定が済んでおり、Profileがわかっていること

```shell: terminal
AWS_PROFILE=<AWS_PROFILE> make fetch-log-<environment>
```

- <AWS_PROFILE>はログを取得するAPI Gatewayのログが保存されているS3へ接続できるProfile名
- environmentは取得するAPI Gatewayのstage名

コマンド入力後、MFAを求められる場合があるので、そのときはスマートフォンのMFAアプリでワンタイムパスワードを入力する。

```shell: terminal
Enter MFA code for arn:aws:iam::xxxxxxxxxxxx:mfa/xxxxxxxxxxx:
```

### ログファイルをデータベースに取り込み

```shell: terminal
python make fetch-log-<environment>
```

- environmentは取得するAPI Gatewayのstage名

以上
