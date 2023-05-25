import configparser

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


def create_models():
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    url = config.get("database", "url")

    # 创建数据库连接
    engine = create_engine(url)

    # 创建元数据对象
    metadata = MetaData()

    # 获取所有表名和字段信息
    metadata.reflect(engine)

    # 打印所有表名和字段信息
    for table_name, table in metadata.tables.items():
        print(f"Table: {table_name}")
        for column_name, column in table.columns.items():
            print(f"\tColumn: {column_name}, Type: {column.type.__class__.__name__}")




if __name__ == '__main__':
    create_models()
