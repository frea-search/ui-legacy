## Frea Search
信頼性の高い検索結果のみを表示するクリーンな検索エンジンを目指したsearxngのカスタムインスタンス<br>

 - [公式インスタンス](https://freasearch.org/)
 - [公式onionインスタンス](http://fcy6tvcy5fq7qogwjfovb54kodrgdpf5i6afda3an4oc5ndgbziegyyd.onion/)


### ブラックリストについて 🚫
`searx/settings.yml`に検索エンジンの設定と検索結果に表示しないサイトの一覧があります。これに追加、削除したいドメインや質問がある場合、issueかPRを開いてください。

### API 💫
Frea Searchには完全無償で使えるAPIが付属しています。検索結果をjsonで取得できます。
```
https://freasearch.org/search?q=検索したいワード&format=json
```

### インストール方法 💿
予め`curl`と`git`、`caddy`をインストールしてください <br>
```
git clone https://git.sda1.net/frea/search
cd search
sudo -H ./utils/searx.sh install all
```

<br>

`/etc/caddy/Caddyfile` に以下の内容を書き込みます。

```
freasearch.org {
        header Access-Control-Allow-Origin "https://assets.freasearch.org"
        reverse_proxy localhost:8888
}
```

<br>

最後に変更を適用

```
sudo systemctl reload caddy
```

#### 他のhttpサーバーでは駄目なのですか？
Frea Searchではセキュリティとパフォーマンス、設定ファイルの美しさの観点からcaddyを使用することを推奨しています。<br>
`Access-Control-Allow-Origin`を`https://assets.freasearch.org`に設定し、`localhost:8888`へリバースプロキシを行う設定を書けばnginxやApacheでも同じことが可能ですが、必ずcertbotなどを使用しエンドツーエンドを暗号化してください。

#### assets.freasearch.orgとは何ですか？
`https://assets.freasearch.org`ではライセンスの関係上このリポジトリには同梱できないフォントやアイコンなどのファイルがホストされています。これらのコンテンツもセルフホストしたい方向けのソリューションは現在準備中です。

#### Cloudflareについて
CloudflareはSSLのトラストモデルを破壊し、さらにキャッシュやページ書き換えによる不具合を引き起こすためFrea Searchでの使用は推奨しておらず、サポートもされていません。

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
・松村咲穂 <br>
・永田琴乃 <br>
・島谷直樹 <br>
・西室涼乃

