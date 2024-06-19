# mp3MusicDownloader

## 概要
youtube上にあるプレイリストをそのままmp3ファイルに変換しディレクトリにまとめます.
(今時ないけど)mp3しか再生できないシステムの車とかに使えます.

## 使い方
まず,`bin/mp3MusicDownloader`に実行権限を与え，パスを通します.
適当な名前のディレクトリを作り，そこからこのファイルを実行します.
その際,第一引数にplaylistのURLを指定します.

## 例
"七人のカリスマ"の,"カリスマジャンボリー"プレイリストををダウンロードする場合を考えます. <br>
- リンク: https://youtu.be/V8tzcj14CeQ?list=OLAK5uy_nnMRNR5oZmp2RIg8z3vLyGSBDfKHEVuLw <br>

上記の，`?list=`より下の文字列をURLとここでは呼称しています.
ディレクトリ構成が,

```
app.py
カリスマ/
 └カリスマジャンボリー/
```

で,いま`カリスマジャンボリー/`がカレントディレクトリとすると,コンソールで

```
> [mp3MusicDownloader] --url "OLAK5uy_nnMRNR5oZmp2RIg8z3vLyGSBDfKHEVuLw"

```
を実行することで,`カリスマジャンボリー/`内に.mp3音楽ファイルが生成されます.

## オプション
- `--url [url] `<必須> <br>
youtube playlistのurlを指定します.
- `--save_videos [bool] `<任意> <br>
ダウンロードに使用した動画をtmpファイル内に保存するかどうかです.デフォルトの値はFalseです.
- `--auto_metadata` <任意> <br>
メタデータを自動挿入するかです．このオプションを指定した場合,ファイル名も自動でspotifyから取得したタイトルになります.
- `--auto_title` <任意> <br>
タイトルをメタデータとして自動挿入します.ファイル名も自動でspotifyから取得したタイトルになります.
- `--auto_artists` <任意> <br>
アーティストをメタデータとして自動挿入します.
- `--auto_date` <任意> <br>
リリース日をメタデータとして自動挿入します.
