import configparser
import re

from sqlalchemy import create_engine, MetaData


def create_models():
    # 第一部分
    model_file1 = "# coding: utf-8\n\r" \
                  "from sqlalchemy import BigInteger, Column, DateTime, Integer, String\n\r" \
                  "from sqlalchemy.ext.declarative import declarative_base\n\r\n\r" \
                  "Base = declarative_base()\n\r" \
                  "metadata = Base.metadata\n\r\n\r"
    # 第二部分
    model_file2 = ""
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    url = config.get("database", "url")
    # 创建数据库连接
    engine = create_engine(url)
    # # 创建元数据对象
    metadata = MetaData()
    # 获取所有表名和字段信息
    metadata.reflect(engine)

    # 打印库里的表名和列名
    for table in metadata.sorted_tables:
        table_name = table.name
        # 类名大写
        class_name = table_name.capitalize()
        # 转换成驼峰命名
        class_name = re.sub(r'_(\w)', lambda m: m.group(1).upper(), class_name)
        model_file2 = model_file2 + "class " + class_name + "(Base):\n\r"
        model_file2 = model_file2 + "    __tablename__ = \"" + table_name + "\"\n\r\n\r"
        # 类属性
        for column in table.columns:
            # 字段名称
            column_name = column.name
            # 字段类型
            column_type = mysql_type_to_python_type(column.type.__class__.__name__)
            # 字段小数位数
            # 字段主键
            column_PK = column.primary_key
            # 字段注释
            column_comment = column.comment
            column_file = column_name + "=Column(" + column_type
            if column_type == "String":
                # 字段长度
                column_type_length = format(column.type.length)
                column_file = column_file + "(" + column_type_length + ")"
            if column_PK:
                column_file = column_file + ",primary_key=True"
            column_file = column_file + ",info='" + column_comment + "')"
            model_file2 = model_file2 + "    " + column_file + "\n\r"
        model_file2 = model_file2 + "\n\r"
        #   __repr__方法
        model_file21 = "    def __repr__(self):\n\r"
        model_file21 = model_file21 + "\t\treturn f\"{self.__class__.__name__}:\"\\\n\r"
        for i in range(0, len(table.columns)):
            column1 = table.columns[i]
            # 字段名称
            column_name1 = column1.name
            if i == len(table.columns) - 1:
                column_file1 = "\t\t   f\"" + column_name1 + "= {self." + column_name1 + "}\""
            else:
                column_file1 = "\t\t   f\"" + column_name1 + "= {self." + column_name1 + "},\" \\"
            column_file1 = column_file1
            model_file21 = model_file21 + "    " + column_file1 + "\n\r"
        model_file2 = model_file2 + model_file21 + "\n\r"
    model_file = model_file1 + model_file2
    print(model_file)

    # 遍历元数据中的表信息并打印
    # for table in metadata.sorted_tables:
    #     print(f"Table: {table.name}")
    #     print(f"Columns:")
    #     for column in table.columns:
    #         print(f"\t{column.name}: {column.type.__class__.__name__}")
    #         print(f"\t\tLength: {column.type.length}")
    #         print(f"\t\tDecimal: {column.type.decimal}")
    #         print(f"\t\tPrimary Key: {table.primary_key.__class__.__name__}")
    #         print(f"\t\tComment: {column.comment}")
    #         print("")


def mysql_type_to_python_type(mysql_type):
    python_type = None
    if mysql_type == 'VARCHAR':
        python_type = 'String'
    elif mysql_type == 'INT':
        python_type = 'int'
    elif mysql_type == 'INTEGER':
        python_type = 'Integer'
    elif mysql_type == 'TEXT':
        python_type = 'String'
    elif mysql_type == 'DATE':
        python_type = 'datetime.date'
    elif mysql_type == 'DATETIME':
        python_type = 'DateTime'
    elif mysql_type == 'BOOLEAN':
        python_type = 'bool'
    elif mysql_type == 'FLOAT':
        python_type = 'float'
    elif mysql_type == 'DOUBLE':
        python_type = 'float'
    elif mysql_type == 'BLOB':
        python_type = 'bytes'
    elif mysql_type == 'BIGINT':
        python_type = 'BigInteger'

    return python_type


if __name__ == '__main__':
    # print(f"\tColumn: {column_name}, Type: {column.type.__class__.__name__}")
    create_models()
