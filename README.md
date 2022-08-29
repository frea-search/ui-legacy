## Frea Search
信頼性の高い検索結果のみを表示するクリーンな検索エンジンを目指したsearxngのカスタムインスタンス<br>

 - [公式インスタンス](https://freasearch.org/)
 - [公式onionインスタンス](http://fcy6tvcy5fq7qogwjfovb54kodrgdpf5i6afda3an4oc5ndgbziegyyd.onion/)


### ブロックリストについて 🚫
`searx/settings.yml`に検索エンジンの設定と検索結果に表示しないサイトの一覧があります。これに追加、削除したいドメインや質問がある場合、issueかPRを開いてください。

### API 💫
Frea Searchには完全無償で使えるAPIが付属しています。検索結果をjsonで取得できます。
```
https://freasearch.org/search?q=検索したいワード&format=json
```

### インストール方法 💿
Frea Searcchのインストール方法はスクリプトを使う方式からdocker-composeを使用する方式に置き換わりました。従来のスクリプトは放棄されました。

#### step 0
FreaのコンテナはまだDockerHubにありません。ビルドする必要があります。  
このリポジトリをcloneし`docker build --tag frea:devel --file Dockerfile .`を実行してください。

#### step1
以下のジトリをcloneします。  
https://git.sda1.net/frea/frea-docker

#### step2
そのまま実行します。  
`docker-compose up`

###  よくありそうな質問
他にあればissueまで

#### assets.freasearch.orgとは何ですか？
`https://assets.freasearch.org`ではライセンスの関係上このリポジトリには同梱できないフォントやアイコンなどのファイルがホストされています。これらのコンテンツもセルフホストしたい方向けのソリューションは現在準備中です。

#### Cloudflareについて
CloudflareはSSLのトラストモデルを破壊し、さらにキャッシュやページ書き換えによる不具合を引き起こすためFrea Searchでの使用は推奨しておらず、サポートもされていません。<br>もし使用する場合は、キャッシュやメールアドレスを隠す機能などページを書き換える機能を無効化するとトラブルが起きにくくなります。


### Special thanks (敬称略・順不同)🙏
 - SearXNGの[開発者、貢献者](https://github.com/searxng/searxng/graphs/contributors)の方々
 - [tukimi](https://github.com/kr-tukimi)  - ロゴ作成
 - [nullcat](https://github.com/nullnyat)  - [404ページ](https://freasearch.org/404)のイラスト提供
 - [code-raisan](https://github.com/code-raisan)  - 公式インスタンス用の画像プロキシシステム構築、提供

#### ブラックリストの改善協力
 - [HonokaNo](https://github.com/HonokaNo)
 - ゆう
 - 秋山めい
 - 松村咲穂
 - 永田琴乃
 - 島谷直樹
 - 西室涼乃

