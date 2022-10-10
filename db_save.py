import os 
import time
import MySQLdb


host = os.getenv('Host')
user = os.getenv('User')
passwd = os.getenv('Password')


def db_info(db_name, retry=15):
    """
    This function make a connection with server
    :param db_name: name of the data-base
    :return: database connection and cursor from sql
    """
    try:
        db = MySQLdb.connect(host=host, user=user,
                             passwd=passwd, db=db_name)
        cur = db.cursor()
        if retry < 15:
            print("\nConnection reestablished.")
    except Exception as e:
        print(e)
        # Retry a maximum of 60 times.
        if retry == 0:
            raise
        print("Connection failed!  Retrying (" + str(15 - retry) + "/15) ", end="\r", flush=True)
        # Wait 5 seconds between each retry.
        time.sleep(5)
        return db_info(db_name, retry - 1)
    return db, cur


def add_bin_folder(db_name,bin_name):
    """
    The module connects to the db and adds bin name
    :param db_name: name of the data-base
    :param bin_name : folder name for tapes
    :return: database connection and cursor from sql
    """
    db, cur = db_info(db_name)
    q_stmt = "INSERT INTO bins (`name`,client_id,project_id,created_at, updated_at) VALUES "
    comp_stmt = "('" + str(bin_name) + "', 1,1, NOW(), NOW()), "
    q_stmt += comp_stmt
    q_stmt = q_stmt[:-2] + ";"
    try:
        cur.execute(q_stmt)
        bin_id = cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        db.commit()
    return bin_id


def db_add_images(path,db_name,bin_id):
    """
    The module connects to the db and adds bin name
    :param db_name: name of the data-base
    :param bin_id : folder id for tapes
    :return: database connection and cursor from sql
    """
    db, cur = db_info(db_name)
    q_stmt = "INSERT INTO tapes (`name`,`bin_id`,client_id,project_id,`barcode`,created_at, updated_at) VALUES "
    split = os.path.splitext(path)
    comp_stmt = "('" + str(path) + "','" + str(bin_id) + "', 1,1, '" + str(split[0]) + "', NOW(), NOW()), "
    q_stmt += comp_stmt
    q_stmt = q_stmt[:-2] + ";"
    try:
        cur.execute(q_stmt)
    except Exception as e:
        print(e)
    finally:
        db.commit()
    time.sleep(5)

