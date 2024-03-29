import psycopg2


def init_database():
    conn = psycopg2.connect(
        dbname='virus',
        user='virus',
        password='virus',
        host='localhost',
        port='5010'
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'chats')")
    table_exists = cur.fetchone()[0]

    # Create a table
    if not table_exists:
        init_chat = """
                        create table chats
                (
                    id SERIAL PRIMARY KEY,
                    chat_id varchar not null,
                    name     varchar not null,
                    count int default 0
                );
        """
        init_task = """
                        create table tasks
                (
                    id          SERIAL PRIMARY KEY,
                    chat_id     varchar not null,
                    name     varchar not null,
                    start_entrance1 time NULL,
                    start_entrance2 time NULL,
                    start_entrance3 time NULL,
                    question_1  boolean default false,
                    question_2  boolean default false,
                    question_3  boolean default false,
                    question_4  boolean default false,
                    question_5  boolean default false,
                    question_6  boolean default false,
                    question_7  boolean default false,
                    question_8  boolean default false,
                    question_9  boolean default false
                    
                );
        """
        question_4 = """
                                create table question_answer_1
                        (
                            id          SERIAL PRIMARY KEY,
                            chat_id     varchar not null,
                            answer_1    boolean default false,
                            answer_2       boolean default false,
                            answer_3   boolean default false
                        );
                """

        question_8 = """
                                        create table question_answer_2
                                (
                                    id          SERIAL PRIMARY KEY,
                                    chat_id     varchar not null,
                                    answer_1    boolean default false,
                                    answer_2       boolean default false,
                                    answer_3   boolean default false
                                );
                        """

        group_data = """
                                                create table groups
                                        (
                                            id          SERIAL PRIMARY KEY,
                                            name     varchar,
                                            group_url    varchar
                                        );
                                """
        cur.execute(init_chat)
        cur.execute(init_task)
        cur.execute(question_4)
        cur.execute(question_8)
        cur.execute(group_data)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    init_database()
