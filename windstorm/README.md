# windstorm
Frea Searchの次世代エンジン


## 設計
### server.nim
結果の最適化とリクエストへの応答を行うコンポーネント。高速な処理を必要とするためnimで記述されています。

### google.js
Googleの検索結果をクロールするコンポーネント。柔軟性が高いnodejsで動作します。
