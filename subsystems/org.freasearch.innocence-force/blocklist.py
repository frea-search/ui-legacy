import sys
import os
import psycopg2
import msg


def detect_sql_injection(query):
    if "'" in query:
        return True
    else:
        return False

def chk_domain(domain):
    if detect_sql_injection(domain):
        msg.fetal_error("SQL injection detected !!!!!!!")
        return False

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

    cur.execute(f"SELECT url FROM blocklist WHERE url='{domain}'")
    cur.execute(f"SELECT url FROM blocklist WHERE url='{domain.replace('www.', '')}'")
    result=cur.fetchall()

    if len(result) == 0 :
        return False
    else:
        return True


if __name__ == '__main__':
    print(chk_domain("sejuku.net"))