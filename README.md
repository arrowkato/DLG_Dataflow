# このリポジトリは何するものぞ？
データラーニングギルドのデータパイプライン講座の一部です。

ETL処理をDataflow上でPythonを使って書くのが主目的です。

# 環境構築
Python 3系をインストールしてください。
僕の環境は、3.8.3です。

## 事前に設定するもの
gitの管理対象から外しています。
### SlackのAPIトークン
src/slack_token.txt に保存。  
トークン自体は自分で作るか、所属コミュニティの管理者からもらってください。

## GCPのservice account key  
src/DLG_service_account_key.json に保存。  
キーは自分で作るか、所属コミュニティの管理者からもらってください。




# 参考文献
- [Dataflow公式ドキュメント](https://cloud.google.com/dataflow/docs?hl=ja)
- [Apache Beam](https://beam.apache.org/documentation/)
- [Apach Beamの公式サンプル:wordcount.pyの解説](https://qiita.com/arrowKato/items/9cd957f429660290ae14)
- [Apache Beamの概念説明](https://qiita.com/esakik/items/3c5c18d4a645db7a8634)
- [Apache Beam example](https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples)
- [Cloud Composer & Dataflow による バッチETLの再構築](https://speakerdeck.com/yuzutas0/20190719?slide=49)
- [Cloud Dataflow PythonSDKによるビッグデータ処理実装応用](https://allabout-tech.hatenablog.com/entry/2017/08/16/114800)


## BigQuery
- [BigQuery クライアント ライブラリ](https://cloud.google.com/bigquery/docs/reference/libraries?hl=ja#client-libraries-install-python)

