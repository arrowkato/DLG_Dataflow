import pandas as pd
from pathlib import Path
from google.cloud import bigquery
import const
import pytz

# デフォルトのservice_account_keyのパス
const.DEFAULT_SERVICE_ACCOUNT_KEY_PATH = "src/DLG_service_account_key.json"
# データパイプライン講座用のdatasetのprefix
const.DATASET_PREFIX = "data_pipeline_lesson_"


class BigQueryUtil:
    '''
    BigQuery操作を行う
    1. クエリを投げて結果の取得
    2. BigQueryのテーブルへのデータの追加
    '''

    def __init__(self, service_account_key_path=const.DEFAULT_SERVICE_ACCOUNT_KEY_PATH) -> None:
        '''
        接続用のservice account keyを指定する
        プロジェクト名は、service accunt keyに記載されているものを指定
        :param service_account_key_path: サービスアカウントキーのpath。デフォルトは{project_root}/src/DLG_service_account_key.json
        '''
        is_default = True
        if service_account_key_path == const.DEFAULT_SERVICE_ACCOUNT_KEY_PATH:
            sak_path = str(Path(Path.cwd()).parent) + "/src/DLG_service_account_key.json"
            if not Path(sak_path).exists():
                raise FileExistsError("There is no file at :" + sak_path)
        else:
            if not Path(service_account_key_path).exists():
                raise FileExistsError("There is no file at :" + service_account_key_path)
            is_default = False

        if is_default:
            self.__credentials = sak_path
            self.client = bigquery.Client.from_service_account_json(sak_path)
        else:
            self.__credentials = service_account_key_path
            self.client = bigquery.Client.from_service_account_json(service_account_key_path)
        pass

    def get_datasets(self) -> list:
        '''
        プロジェクトにあるDatasetを取得して、listで返す
        :return: list
        '''
        return list(self.client.list_datasets())

    def list_dataset(self) -> None:
        '''
        プロジェクトにあるDataset一覧表示
        :return None:
        '''
        datasets = self.get_datasets()
        project = self.client.project

        if datasets:
            print("Datasets in project {}:".format(project))
            for dataset in datasets:
                print("\t{}".format(dataset.dataset_id))
        else:
            print("{} project does not contain any datasets.".format(project))

    def create_dataset(self, dataset_name: str) -> None:
        '''
        :param dataset_name: データセットの名前。
        データパイプライン講座関連のテーブルなら、定数:const.DATASET_PREFIX に
        入っている文字列をprefixとしてつけること推奨します。
        :return: None
        '''
        self.client.create_dataset(dataset_name)
        print(dataset_name + " is created")

    def create_table(self, dataset_name, table_name, schema) -> None:
        '''
        プロジェクト内に、tableを作成する
        :param dataset_name: dataset名
        :param table_name: table名
        :param schema: スキーマ(テーブルの構造)
        :return: None
        '''
        table_id = "{}.{}.{}".format(self.client.project, dataset_name, table_name)
        table = bigquery.Table(table_id, schema=schema)
        table = self.client.create_table(table)  # Make an API request.
        print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

    def list_tables(self, dataset_name: str) -> None:
        '''
        テーブル一覧を表示
        :param dataset_name:
        :return: None
        '''
        table_list = self.get_tables(dataset_name)
        if table_list:
            print("'{}' project '{}' dataset has tables below:".format(self.client.project, dataset_name))
            for table in table_list:
                print(table.table_id)
        else:
            print("no tables in '{}' project '{}' dataset ".format(self.client.project, dataset_name))

    def get_tables(self, dataset_name) -> list:
        '''
        テーブル一覧をlistで取得
        :param dataset_name: データセット名
        :return: list
        '''
        return self.client.list_tables(dataset=dataset_name)

    def delete_dataset(self, dataset_name):
        raise Exception("人のDatasetを消すのが怖いので未実装")

    def delete_table(self, dataset_name, table_name):
        table_id = "{}.{}.{}".format(self.client.project, dataset_name, table_name)
        self.client.delete_table(table_id)
        print("Deleted table '{}'.".format(table_id))

    def get_table_all_records(self, dataset, table) -> pd.DataFrame:
        '''
        指定したテーブルのすべてのレコードを取得して、pandas.DataFrameに入れて返す
        :return: pandas.DataFrame
        '''
        query = """ SELECT * FROM `{}.{}` """.format(dataset, table)
        return self.client.query(query).to_dataframe()

    def query(self, query: str) -> pd.DataFrame:
        '''
        指定したqueryの結果をDataframeに入れて返す
        :param query: クエリ
        :return: DataFrame
        '''

        return self.client.query(query, project=self.client.project).to_dataframe()

    def show_table_schema(self, dataset, table) -> None:
        '''
        指定したテーブルのスキーマ情報を表示,プロジェクトはコンストラクタで指定した値を使用
        :param dataset: データセット名
        :param table:テーブル名
        :return: None
        '''
        client = bigquery.Client()
        table = client.get_table(self.__make_table_id(dataset, table))
        print("Table schema: {}".format(table.schema))

    def insert_from_list(self, target_dataset, target_table, insert_records: list):
        # 型チェック
        if isinstance(insert_records, list):
            raise Exception("insert_records must be list type")

        target_table = self.client.get_table(self.__make_table_id(target_dataset, target_table))
        errors = self.client.insert_rows(target_table, insert_records)  # Make an API request.
        if not errors:
            print("New rows have been added.")
        pass

    def insert_from_dataframe(self, target_dataset, target_table, insert_df: pd.DataFrame):
        # 型チェック
        if type(insert_df) != pd.DataFrame:
            raise Exception("insert_records must be list type")

        insert_df.to_gbq(
            project_id=self.client.project,
            destination_table="{}.{}".format(target_dataset, target_table),
            if_exists="append"
        )
        pass

    # TODO:実装
    def insert_from_GCS(self, target_table, gcs_key):
        raise Exception("This method is not implemented")
        pass

    def __make_table_id(self, dataset_name, table_name) -> str:
        return "{}.{}.{}".format(self.client.project, dataset_name, table_name)


if __name__ == "__main__":
    dataset_name = "data_pipeline_lesson_sample"
    table_name = "create_sample"

    bq = BigQueryUtil()

    records = [("Angela", 19),
               ("Duran", 17),
               ("Hawkeye", 18),
               ("flee", 16),
               ("Kevin", 15),
               ("Charlotte", 15)]
    # insert
    # bq.insert_from_list(dataset_name,table_name,records)





