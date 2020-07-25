BigQueryUtilを書いたけど、APIの抽象化のレベルが高いので、不要疑惑が浮上中。
コードのサンプルとしてみるくらいが良さそうですね。

# 1.命名規則的なもの
データセット名、テーブル名
命名規則的なもの

## 1.1. project
データパイプライン講座用のプロジェクト名:  
**salck-visualization**  
今の所、slackの可視化プロジェクトと共用です。

## 1.2. dataset
DWHを意識すると、rawデータと加工したデータは別の方が良さそうです。
また、BigQueryへのSQL発行を動かしてみるサンプルが必要なので、
下記の3種類のデータセットを作成します。

- data_pipeline_lesson_raw
- data_pipeline_lesson_processed
- data_pipeline_lesson_sample


## 1.3. table
datasetの規約に沿ってテーブルが格納されていればよいです。
特にprocessedデータセット配下のテーブルは、howよりもwhyを意識したテーブル名だと良さそうです。

# 2. ERD
テーブル間の結合までは今のところ考えていないです。

# 99. 参考文献
https://googleapis.dev/python/bigquery/latest/usage/index.html

