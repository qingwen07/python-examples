import sqlite3

def create_connection(db_file):
    """创建数据库连接"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"连接到SQLite数据库 {db_file} 成功")
    except sqlite3.Error as e:
        print(f"连接SQLite数据库失败：{e}")
    return conn

def create_table(conn):
    """创建表"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        print("表创建成功或已存在")
    except sqlite3.Error as e:
        print(f"创建表失败：{e}")

def insert_user(conn, user):
    """插入用户数据"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, age, email)
            VALUES (?, ?, ?)
        ''', user)
        conn.commit()
        print("插入数据成功")
    except sqlite3.Error as e:
        print(f"插入数据失败：{e}")

def select_all_users(conn):
    """查询所有用户数据"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"查询数据失败：{e}")
        return []

def update_user_age(conn, name, age):
    """更新用户年龄"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET age = ?
            WHERE name = ?
        ''', (age, name))
        conn.commit()
        print("更新数据成功")
    except sqlite3.Error as e:
        print(f"更新数据失败：{e}")

def delete_user(conn, name):
    """删除用户数据"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users
            WHERE name = ?
        ''', (name,))
        conn.commit()
        print("删除数据成功")
    except sqlite3.Error as e:
        print(f"删除数据失败：{e}")

def main():
    database = "example.db"

    # 创建数据库连接
    conn = create_connection(database)

    if conn is not None:
        # 创建表
        create_table(conn)

        # 插入数据
        insert_user(conn, ('Alice', 30, 'alice@example.com'))
        insert_user(conn, ('Bob', 25, 'bob@example.com'))

        # 查询数据
        users = select_all_users(conn)
        print("所有用户数据：")
        for user in users:
            print(user)

        # 更新数据
        update_user_age(conn, 'Alice', 31)
        print("更新后Alice的数据：")
        user = select_all_users(conn)
        for u in user:
            if u[1] == 'Alice':
                print(u)

        # 删除数据
        delete_user(conn, 'Bob')
        print("删除后所有用户数据：")
        users = select_all_users(conn)
        for user in users:
            print(user)

        # 关闭连接
        conn.close()
    else:
        print("错误！无法创建数据库连接。")

if __name__ == '__main__':
    main()

