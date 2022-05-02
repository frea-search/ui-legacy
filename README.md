## Frea Search
信頼性の高い検索結果のみを表示するクリーンな検索エンジンを目指したsearxngのカスタムインスタンス

### ブラックリストについて
`searx/settings.yml`に検索エンジンの設定と検索結果に表示しないサイトの一覧があります。これに追加、削除したいドメインや質問がある場合、issueかPRを開いてください。

### インストール方法
予め`curl`と`git`をインストールしてください <br>
```
git clone https://git.sda1.net/frea/search
cd search
sudo -H ./utils/searx.sh install all
```

### インスタンスのアップデート方法
コマンド一つで自動的にGitリポジトリからの変更がPullされ適用されます。
```
cd search
sudo -H ./utils/searx.sh update searx
```
