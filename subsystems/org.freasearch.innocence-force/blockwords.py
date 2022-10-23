def is_included_in_list(title, words_list):
    for detect_word in words_list:
        if detect_word in title:
            return True
        return False

def chk_title(title):
    try:
        db_host = os.environ['POSTGRESQL_HOST'] 
        db_user = os.environ['POSTGRESQL_USER']
        db_password = os.environ['POSTGRESQL_PASSWORD']
    except KeyError as e:
        msg.fetal_error("Environment variable " + str(e) + " is undefined")
        return False
    except Exception as e:
        msg.fetal_error(e)
        return False

    conn = psycopg2.connect(database="freasearch", host=db_host, user=db_user, password=db_password, port="5432")
    cur = conn.cursor() 

    cur.execute(f"SELECT url FROM blockwords WHERE level='block_words'")
    block_words=cur.fetchall()

    cur.execute(f"SELECT url FROM blockwords WHERE level='detect_words_1'")
    detect_words_1=cur.fetchall()

    cur.execute(f"SELECT url FROM blockwords WHERE level='detect_words_2'")
    detect_words_2=cur.fetchall()


    if is_included_in_list(title, detect_words_1):
        if is_included_in_list(title, detect_words_2):
            return False
        else:
            return True
    elif is_included_in_list(title, block_words):
        return False
    else:
        return True
