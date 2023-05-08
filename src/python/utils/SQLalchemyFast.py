from sqlalchemy import create_engine, delete, update, text, alias
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker

from src.file.FileReadAndWrite import FileReadAndWrite
from src.log.Log import Log


class SQLalchemyFast(object):
    Base = declarative_base()
    """
    功能: SQLalchemy工具
    """

    def __init__(self, dbFile):
        file = FileReadAndWrite.readPropertiesFile(dbFile)
        self.engine = create_engine(
            url=file['url'],
            echo=bool(file['echo']),
            pool_size=int(file['pool_size']),
            pool_recycle=int(file['pool_recycle']),
            pool_timeout=int(file['pool_timeout']),
            isolation_level=file['isolation_level'],
        )

        SQLalchemyFast.Base.metadata.create_all(self.engine)  # 创建表,如果表存在则不创建(必须对象继承Base)

    # 创建会话
    def createSession(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    # 添加一条数据
    def addData(self, object):
        with self.createSession() as conn:
            conn.add(object)
            conn.commit()

    # 添加多条数据
    def addDataList(self, objectList):
        with self.createSession() as conn:
            conn.add_all(objectList)
            conn.commit()

    # 删除主键id的数据
    def deleteDataById(self, cla, id):
        with self.createSession() as conn:
            conn.query(cla).filter(cla.id == id).delete()
            conn.commit()

    # 删除指定数据(where是并且的关系,不支持or和其他复杂查询)
    def deleteDataWhere(self, cla, *where):
        with self.createSession() as conn:
            stmt = delete(cla).where(*where)
            conn.execute(stmt)
            conn.commit()

    # 清空表
    def truncateTable(self, cla):
        with self.createSession() as conn:
            conn.query(cla).delete()
            conn.commit()

    # 更新指定主键id的数据
    def updateDataById(self, cla, id, data):
        """
        :param cla:  类(表)
        :param id:  主键id
        :param data:  {'key': "value",...}  key为表中的字段名,value为要修改的值
        :return:
        """
        with self.createSession() as conn:
            stmt = update(cla).where(cla.id == id).values(data)
            result = conn.execute(stmt)
            conn.commit()
            return result

    # 更新指定条件的数据 (where是并且的关系,不支持or和其他复杂查询)
    def updateDataWhere(self, cla, data, *where):
        """
        :param cla:  类(表)
        :param data:  {'key': "value",...}  key为表中的字段名,value为要修改的值
        :param where:  过滤条件
        :return:
        """
        with self.createSession() as conn:
            stmt = update(cla).where(*where).values(data)
            conn.execute(stmt)
            conn.commit()

    # 查询全部数据
    def queryDataAll(self, cla):
        with self.createSession() as conn:
            result = conn.query(cla).all()
        return result

    # 查询主键id的数据
    def queryDataById(self, cla, id):
        with self.createSession() as conn:
            result = conn.query(cla).filter(cla.id == id).first()
        return result

    # 查询指定数据,不支持分组查询(因为聚合后的数据无法转换成对象)
    def queryDataWhere(self, cla,aliasName=None, column=None, where=None,
                       join=None, on=None, left=None, full=None,
                       order="", limit="", offset="", distinct=None, params=None):
        with self.createSession() as conn:
            stmt = select(cla)
            if aliasName:
                stmt = select(alias(cla,aliasName))
            if column:
                stmt = stmt.with_only_columns(text(column)) .select_from(cla)
            if join is not None and on is not None:
                if left:
                    stmt = stmt.join(join, text(on), isouter=True)
                elif full:
                    stmt = stmt.join(join, text(on), full=True)
                else:
                    stmt = stmt.join(join, text(on))
            if where:
                stmt = stmt.where(text(where))
            if order:
                stmt = stmt.order_by(text(order))
            if limit:
                stmt = stmt.limit(limit)
            if offset:
                stmt = stmt.offset(offset)
            if distinct:
                stmt = stmt.distinct()
            result = conn.execute(stmt,params).all()
            result= [row[0] for row in result]
        return result

    # 创建事物(运行多条sql语句 ,function(conn)是一个函数,里面包含多条sql语句,需要使用原生的sqlalchemy)
    def createTransaction(self, function):
        with  self.createSession() as conn:
            conn.begin()
            try:
                function(conn)
                conn.commit()
            except Exception as e:
                Log.logError(e)
                conn.rollback()

    # 执行sql语句(包括增删改查,和存储过程...只要是sql语句都可以执行)
    def executeSql(self, sql, params=None):
        """
        :param sql:  sql语句  如: "select * from User where id = :id and name = :name "
        :param params:  参数  例如: {"id":1,"name":"张三"} 注意:参数名必须和sql语句中的参数名一致
        发送多个参数时,参数名必须以列表的形式传入,例如: {"id":["1","2"],"name":"张三"}
        "INSERT INTO some_table (x, y) VALUES (:x, :y)" 参数可以是 [{"x": 11, "y": 12}, {"x": 13, "y": 14}]
        :return:
        """
        with self.createSession() as conn:
            result = conn.execute(text(sql), params)
            conn.commit()
        return result

    # 执行构建sql语句
    def executeSqlBuild(self, sql):
        with self.createSession() as conn:
            result = conn.execute(sql)
            conn.commit()
        return result

