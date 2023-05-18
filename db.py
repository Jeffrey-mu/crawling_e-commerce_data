import csv
import pymysql


import pymysql

# 查询
def execute_query(query):
    """
    Executes a SELECT query and returns the results as a list of dictionaries.

    Args:
        query (str): SQL query to execute

    Returns:
        list: A list of dictionaries representing the rows returned by the query
    """
    # Establish connection to database
    conn = pymysql.connect(
        host="localhost",
        user="root",
        port=3306,
        password="123456",
        database="djangol6hz8",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        # Execute query
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    finally:
        # Close connection
        conn.close()

# 插入
def execute_insert(insert_query, values):
    """
    Executes an INSERT query and inserts the provided values into the specified table.

    Args:
        insert_query (str): SQL query with placeholders for values to be inserted
        values (tuple): A tuple of values to be inserted

    Returns:
        int: The last insert ID
    """
    # Establish connection to database
    conn = pymysql.connect(
        host="localhost",
        user="root",
        port=3306,
        password="123456",
        database="djangol6hz8",
    )

    try:
        # Execute insert query
        with conn.cursor() as cursor:
            cursor.execute(insert_query, values)
            last_insert_id = cursor.lastrowid
            conn.commit()
            return last_insert_id

    finally:
        # Close connection
        conn.close()


def execute_insert_xin(insert_query, values):
    """
    Executes an INSERT query and inserts the provided values into the specified table.

    Args:
        insert_query (str): SQL query with placeholders for values to be inserted
        values (tuple): A tuple of values to be inserted

    Returns:
        int: The last insert ID
    """
    # Establish connection to database
    conn = pymysql.connect(
        host="172.16.3.57",
        user="root",
        port=3306,
        password="123456",
        database="django-vue-admin3",
    )

    try:
        # Execute insert query
        with conn.cursor() as cursor:
            cursor.execute(insert_query, values)
            last_insert_id = cursor.lastrowid
            conn.commit()
            return last_insert_id

    finally:
        # Close connection
        conn.close()


def insert_xin():
   for item in  execute_query('SELECT * FROM goods'):
       val = (item['g_number'], item['g_price'],
              item['g_details'], item['g_picture'], item['g_color'], item['g_size'], item['g_brand'])
       execute_insert_xin(
           'INSERT INTO dvadmin_jd_goods (g_number, g_price, g_details, g_picture, g_color, g_size, g_brand) VALUES (%s, %s, %s, %s, %s, %s, %s)', val)


# insert_xin()


def insert_com():
   for item in execute_query('SELECT * FROM comment'):
       val = (item['c_number'], item['c_comment'],
              item['c_size'], item['c_color'], item['c_score'], item['c_nickname'])
       execute_insert_xin(
           'INSERT INTO dvadmin_jd_comment (c_number, c_comment, c_size, c_color, c_score, c_nickname) VALUES (%s, %s, %s, %s, %s, %s)', val)



def insert():
  # 打开CSV文件并读取数据
  with open('./data/goods_numbers电脑.csv', newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        # 解析CSV行并插入到MySQL表中
        sql = "INSERT INTO comment (c_number, c_comment, c_size, c_color, c_score, c_nickname) VALUES (%s, %s, %s, %s, %s, %s)"
        g_name = ''
        val = (row['c_number'], g_name, row['c_comment'], row['c_size'],
               row['c_color'], row['c_score'], row['c_nickname'])
        execute_insert(sql, val)

