import psycopg2
from contextlib import closing
from psycopg2.extras import DictCursor
from datetime import datetime
import time


def getCurrentTime():
    current_time = datetime.now().time()
    current_time_str = current_time.strftime('%H:%M:%S')
    return current_time_str

class Data:

    def __init__(self, chat_data):
        self.chat_data = chat_data
        self.conn = self.getConn()
        self.cursor = self.getCursor()

    def getConn(self):
        conn = psycopg2.connect(
            dbname='virus',
            user='virus',
            password='virus',
            host='localhost',
            port='5010'
        )

        return conn

    def getCursor(self):
        cursor = self.conn.cursor()
        return cursor

    def create(self, name):
        check = f'select exists(SELECT chat_id FROM chats WHERE chat_id = \'{self.chat_data.id}\')'
        self.cursor.execute(check)
        result = self.cursor.fetchone()
        if (result[0] == False):
            try:
                sql_chat = "INSERT INTO chats (chat_id, name) VALUES (%s, %s)"
                values_chat = (self.chat_data.id, name)
                self.cursor.execute(sql_chat, values_chat)

                sql_task = "INSERT INTO tasks (chat_id, name) VALUES (%s, %s)"
                values_task = (self.chat_data.id, name)
                self.cursor.execute(sql_task, values_task)

                sql_question_answer = "INSERT INTO question_answer_1 (chat_id) VALUES (%s)"
                values_question_answer = (self.chat_data.id,)
                self.cursor.execute(sql_question_answer, values_question_answer)

                sql_question_answer_end = "INSERT INTO question_answer_2 (chat_id) VALUES (%s)"
                values_question_answer_end = (self.chat_data.id,)
                self.cursor.execute(sql_question_answer_end, values_question_answer_end)

                self.conn.commit()
                self.cursor.close()
                self.conn.close()
            except Exception as error:
                print(error)

    def get_question(self):
        self.cursor.execute('SELECT '
                            'question_1,'
                            'question_2,'
                            'question_3,'
                            'question_4,'
                            'question_5,'
                            'question_6,'
                            'question_7,'
                            'question_8,'
                            'question_9 '
                            'FROM tasks '
                            'WHERE chat_id = \'{}\''.format(self.chat_data.id))
        rec = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return rec

    def start_entrance_at(self, column_name):
        query = f'UPDATE tasks SET {column_name} = \'{getCurrentTime()}\' WHERE chat_id = \'{self.chat_data.id}\''
        self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def check_end_time(self, column_name):
        self.cursor.execute(f'SELECT {column_name} FROM tasks WHERE chat_id = \'{self.chat_data.id}\'')
        rec = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return rec[0]

    def response_answer(self, table_name, column_name):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(f'SELECT {column_name} FROM {table_name} WHERE chat_id = \'{self.chat_data.id}\'')
        rec = dict_cur.fetchone()

        return rec

    def replace_answer(self, table_name, column_name):
        self.cursor.execute(f'UPDATE {table_name} SET {column_name} = true WHERE chat_id = \'{self.chat_data.id}\'')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def replace(self, column_name):
        self.cursor.execute(f'UPDATE tasks SET {column_name} = true WHERE chat_id = \'{self.chat_data.id}\'')
        self.cursor.execute(
            f'SELECT count FROM chats WHERE chat_id = \'{self.chat_data.id}\'')
        rec = self.cursor.fetchone()
        count = rec[0] + 1
        self.cursor.execute(f'UPDATE chats SET count = {count} WHERE chat_id = \'{self.chat_data.id}\'')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def check_answer_final(self, table_name):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(f'SELECT answer_1, answer_2, answer_3 FROM {table_name} WHERE chat_id = \'{self.chat_data.id}\'')
        rec = dict_cur.fetchone()
        self.cursor.close()
        self.conn.close()
        return rec

    def get_count(self):
        query = "SELECT name, count FROM chats"
        self.cursor.execute(query)

        result = {}
        rows = self.cursor.fetchall()

        for row in rows:
            name, count = row
            result[name] = count

        self.cursor.close()
        self.conn.close()

        return result

    def check_final(self, block):
        if block == 1:
            self.cursor.execute(
                f'SELECT '
                f'question_1, question_2, question_3 '
                f'FROM tasks '
                f'WHERE chat_id = \'{self.chat_data.id}\'')
            rec = self.cursor.fetchone()
        elif block == 2:
            self.cursor.execute(
                f'SELECT '
                f'question_4, question_5, question_6 '
                f'FROM tasks '
                f'WHERE chat_id = \'{self.chat_data.id}\'')
            rec = self.cursor.fetchone()
        elif block == 3:
            self.cursor.execute(
                f'SELECT '
                f'question_7, question_8, question_9 '
                f'FROM tasks '
                f'WHERE chat_id = \'{self.chat_data.id}\'')
            rec = self.cursor.fetchone()
        else:
            self.cursor.execute(
                f'SELECT '
                f'question_1, question_2, question_3,'
                f'question_4, question_5, question_6,'
                f'question_7, question_8, question_9 '
                f'FROM tasks '
                f'WHERE chat_id = \'{self.chat_data.id}\'')
            rec = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return rec



    def find_group_database(self, first_second_name):
        self.cursor.execute(f'SELECT group_url FROM groups WHERE name = \'{first_second_name}\'')
        rec = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        if bool(rec):
            if len(rec) == 1:
                return rec[0]
            else:
                return "Много"
        else:
            return None

    # ------------------------------------------------------------------------------------------------------------------
