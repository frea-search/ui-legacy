import sys
import os
import yaml
import psycopg2


def msg_info(message):
    sys.stdout.write("\033[32m[INFO]\033[0m " + str(message) + "\n")

def msg_error(message):
    sys.stderr.write("\033[31m" + str(message) + "\033[0m\n")

def fetal_error(message):
    msg_error("=!=========FETAL ERROR=========!=")
    msg_error(message)
    msg_error("=================================")
    sys.exit (1)


try:
    db_host = os.environ['POSTGRESQL_HOST'] 
    db_user = os.environ['POSTGRESQL_USER']
    db_password = os.environ['POSTGRESQL_PASSWORD']
except KeyError as e:
    fetal_error("Environment variable " + str(e) + " is undefined")
except Exception as e:
    fetal_error(e)

conn = psycopg2.connect(database="freasearch", host=db_host, user=db_user, password=db_password, port="5432")
cur = conn.cursor() 


def db_error(message):
    cur.execute("ROLLBACK")
    msg_error ("[ERROR] DB error occurred!")
    fetal_error(message)

def detect_sql_injection(query):
    if "'" in query:
        return True
    else:
        return False

def init_db():
    try: 
        cur.execute("CREATE TABLE blocklist (url  varchar(100), src  varchar(30), reason  varchar(100))")
    except psycopg2.errors.DuplicateTable:
        cur.execute("ROLLBACK")
        cur.execute("DROP TABLE blocklist")
        cur.execute("CREATE TABLE blocklist (url  varchar(100), src  varchar(30), reason  varchar(100))")
        msg_info("skip!")
    except Exception as e:
        db_error(e)
    else:
        conn.commit()

def add_record(url, src, reason):
    if detect_sql_injection(url) or detect_sql_injection(src) or detect_sql_injection(reason):
        fetal_error("SQL injection detected !!!!!!!")
        sys.exit(1)

    try:
        cur.execute(f"INSERT INTO blocklist VALUES ('{url}', '{src}', '{reason}')")
    except Exception as e:
        db_error(e)

def load_blocklist(listname):
    try:
        with open(f"/var/frea/subsystems/org.freasearch.innocence-force/blocklists/{listname}.yml", "r") as yml:
            blocklist = yaml.safe_load(yml)
    except Exception as e:
        msg_error("[ERROR] faild to load blocklist")
        fetal_error(e)
    else:
        for block_url in blocklist["blocklist"]:
            add_record(block_url, blocklist["src"], blocklist["reason"])

def load_all_records():
    cur.execute("SELECT * FROM blocklist")
    msg_info(cur.fetchall())

def close_db():
    conn.commit()
    cur.close()
    conn.close()

init_db()
load_blocklist("main")

close_db()
sys.exit(0)