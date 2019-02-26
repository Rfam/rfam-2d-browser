import pymysql.cursors

# Connect to the public Rfam database
connection = pymysql.connect(host='mysql-rfam-public.ebi.ac.uk',
                             user='rfamro',
                             db='Rfam',
                             port=4497,
                             cursorclass=pymysql.cursors.DictCursor)


def get_rfam_families():
    data = []
    try:
        with connection.cursor() as cursor:
            sql = """SELECT rfam_acc, rfam_id, description, type
                     FROM family
                     ORDER BY type, rfam_acc"""
            cursor.execute(sql)
            for result in cursor.fetchall():
                data.append(result)
    finally:
        connection.close()
    return data
