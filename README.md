## Frea Search
信頼性の高い検索結果のみを表示するクリーンな検索エンジンを目指したsearxngのカスタムインスタンス

### ブラックリストについて 🚫
`searx/settings.yml`に検索エンジンの設定と検索結果に表示しないサイトの一覧があります。これに追加、削除したいドメインや質問がある場合、issueかPRを開いてください。

### API 💫
Frea Searchには完全無償で使えるAPIが付属しています。検索結果をjsonで取得できます。
```
https://freasearch.org/search?q=検索したいワード&format=json
```

### インストール方法 💿
予め`curl`と`git`、`nginx`をインストールしてください <br>
```
git clone https://git.sda1.net/frea/search
cd search
sudo -H ./utils/searx.sh install all
```

<br>

`/etc/nginx/conf.d/frea.conf` に以下の内容を書き込みます。

```
server {
        server_name [サーバーのIPアドレスもしくはドメイン];
        listen 80;

        location / {
                proxy_pass http://127.0.0.1:8888;

                proxy_set_header Host $host;
                proxy_set_header Connection       $http_connection;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Scheme $scheme;
                proxy_buffering off;
        }
        
}
```

<br>

最後に変更を適用

```
sudo nginx -s reload
```

### インスタンスのアップデート方法  🔁
コマンド一つで自動的にGitリポジトリからの変更がPullされ適用されます。
```
cd search
sudo -H ./utils/searx.sh update searx

```

### Special thanks (敬称略・順不同)🙏
・SearXNGの[開発者、貢献者](https://github.com/searxng/searxng/graphs/contributors)の方々<br>
<br>
・[kr-tukimi](https://github.com/kr-tukimi) <br>
ロゴ作成 <br>
<br>
・[nullcat](https://github.com/nullnyat) <br>
[404ページ](https://freasearch.org/404)のイラスト提供 <br>
<br>
#### ブラックリストの改善協力
・[HonokaNo](https://github.com/HonokaNo)<br>
・ゆう <br>
・秋山めい <br>
・松村咲穂



