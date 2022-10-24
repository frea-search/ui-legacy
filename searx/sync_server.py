'''
import hashlib
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import psycopg2


def msg_info(message):
    sys.stdout.write("\033[32m[INFO]\033[0m " + str(message) + "\n")

def msg_error(message):
    sys.stderr.write("\033[31m" + str(message) + "\033[0m\n")

def fetal_error(message):
    msg_error("=!=========FETAL ERROR=========!=")
    msg_error(message)
    msg_error("=================================")

def detect_sql_injection(query):
    if "'" in query:
        return True
    else:
        return False

def create_aes(password, iv):
    sha = SHA256.new()
    sha.update(password.encode())
    key = sha.digest()
    return AES.new(key, AES.MODE_CFB, iv)


def upload(user_id, user_password, new_account, config_data):
    try:
        db_host = os.environ['POSTGRESQL_HOST'] 
        db_user = os.environ['POSTGRESQL_USER']
        db_password = os.environ['POSTGRESQL_PASSWORD']
    except KeyError as e:
        fetal_error("Environment variable " + str(e) + " is undefined")
        return "ERR_INTERNAL_SERVER_ERROR"
    except Exception as e:
        fetal_error(e)
        return "ERR_INTERNAL_SERVER_ERROR"

    conn = psycopg2.connect(database="freasearch", host=db_host, user=db_user, password=db_password, port="5432")
    cur = conn.cursor() 

    # ユーザー重複確認
    if new_account:
        cur.execute(f"SELECT url FROM userdata WHERE id='{user_id}'")
        result=cur.fetchall()
        if len(result) != 0 :
            return "ERR_USERNAME_DUPLICATION"

    # パスワードとデータのハッシュ取得
    password_hash = hashlib.sha512(user_password).hexdigest()
    data_checksum = hashlib.sha256(config_data).hexdigest()

    # 暗号化
    iv = Random.new().read(AES.block_size)
    data_encrypted = iv + create_aes(password, iv).encrypt(config_data)

    if detect_sql_injection(user_id) or detect_sql_injection(password_hash) or detect_sql_injection(data_encrypted) or detect_sql_injection(data_checksum):
        fetal_error("SQL injection detected !!!!!!!")
        return "ERR_INTERNAL_SERVER_ERROR"

    try:
        cur.execute(f"INSERT INTO userdata VALUES ('{user_id}', '{password_hash}', '{data_encrypted}', '{data_checksum}')")
    except Exception as e:
        fetal_error(e)
        return "ERR_INTERNAL_SERVER_ERROR"


def download(user_id, user_password):
    try:
        db_host = os.environ['POSTGRESQL_HOST'] 
        db_user = os.environ['POSTGRESQL_USER']
        db_password = os.environ['POSTGRESQL_PASSWORD']
    except KeyError as e:
        fetal_error("Environment variable " + str(e) + " is undefined")
        return "ERR_INTERNAL_SERVER_ERROR"
    except Exception as e:
        fetal_error(e)
        return "ERR_INTERNAL_SERVER_ERROR"

    conn = psycopg2.connect(database="freasearch", host=db_host, user=db_user, password=db_password, port="5432")
    cur = conn.cursor() 


    password_hash = hashlib.sha512(user_password).hexdigest()

    # 復号化
    iv, cipher = data[:AES.block_size], data_encrypted[AES.block_size:]
    config_data = create_aes(password, iv).decrypt(cipher)

    decrypted_checksum = hashlib.sha256(config_data).hexdigest()

'''