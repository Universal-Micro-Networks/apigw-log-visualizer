# apigw-log-visualizer




### blackの設定
コミット時にチェックするため設定は任意です。
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
