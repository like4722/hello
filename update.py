import pymysql
import pandas as pd




#数据库连接
def get_conn():
    conn = pymysql.connect(host="10.243.26.240", user="like", password="229398", database="sales", charset="utf8")
    return conn

#读文件
def read_csv():
    df = pd.read_csv(r'D:\combine\1.csv', encoding='gbk', parse_dates=['飞行日期'])
    print(df.head())

# 一个根据pandas自动识别type来设定table的type
def make_table_sql():
    df = pd.read_csv(r'D:\combine\1.csv', encoding='gbk', parse_dates=['飞行日期'])
    columns = df.columns.tolist()
    types = df.ftypes
    # 添加id 制动递增主键模式
    make_table = []
    for item in columns:
        if 'int' in types[item]:
            char = item + ' INT'
        elif 'float' in types[item]:
            char = item + ' FLOAT'
        elif 'object' in types[item]:
            char = item + ' VARCHAR(255)'
        elif 'datetime' in types[item]:
            char = item + ' DATETIME'
        make_table.append(char)
    print(','.join(make_table))
    return ','.join(make_table)

# csv 格式输入 mysql 中
def csvtomysql():
    conn = get_conn()
    cursor = conn.cursor()
    filepath = r'//DESKTOP-L0OLDCN/upload/1.csv'
    df = pd.read_csv(filepath, encoding='gb18030')
    df.to_csv(filepath,index = None,encoding='gbk')

    #write =r"LOAD DATA INFILE '\\DESKTOP-L0OLDCN\\upload\\1.csv' INTO TABLE cabin_dss FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY "+ "'" +'"'+"'"+ " LINES TERMINATED BY '\\r\\n'"
    write ="LOAD DATA INFILE \'//DESKTOP-L0OLDCN/upload/1.csv\' INTO TABLE cabin_dss1 FIELDS TERMINATED BY \',\' OPTIONALLY ENCLOSED BY \'\"\' LINES TERMINATED BY \'\\r\\n\'"
    print(write)
    cursor.execute(write)
    conn.commit()
    conn.close()

    """
    # 创建database
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    # 选择连接database
    conn.select_db(db_name)
    # 创建table
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    cursor.execute('CREATE TABLE {}({})'.format(table_name,make_table_sql(df)))
    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    df['飞行日期'] = df['飞行日期'].astype('str')
    values = df.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(df.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name,s), values)
    """
def main():
    csvtomysql()
    #sql = "LOAD DATA LOCAL INFILE " +"'"+ r'D:\combine\result.csv'+"'"+" INTO TABLE cabin_dss FIELD TERMINATED BY ',' ENCLOSED BY " + "'"+r'"' + "'"+" LINES TERMINATED BY "+ "'"+r'\n' +"'"+" IGNORE 1 ROWS"
    #insert_mysql()
if __name__ == '__main__':
    main()