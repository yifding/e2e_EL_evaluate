import mysql.connector
import sys


class DataBaseQueryUtil:
    """
    mysql fetch class to fetch the document and annotation results from dsg4;
    written by Nick and Yifan;


    databse: reddit_phrase_adoption
    mysql> show tables;
    +----------------------------------+
    | Tables_in_reddit_phrase_adoption |
    +----------------------------------+
    | annotations                      |
    | combinations_completed           |
    | document                         |
    | document_annotation              |
    | user_information                 |
    | verified_annotations             |
    +----------------------------------+

    annotations: original annotations.

    mysql> describe annotations; original annotations;
    +-------------+--------------+------+-----+---------+----------------+
    | Field       | Type         | Null | Key | Default | Extra          |
    +-------------+--------------+------+-----+---------+----------------+
    | id          | int(11)      | NO   | PRI | NULL    | auto_increment |
    | document_id | varchar(300) | YES  | MUL | NULL    |                |
    | model_enum  | varchar(200) | YES  |     | NULL    |                |
    | mention     | varchar(200) | YES  |     | NULL    |                |
    | entity      | varchar(200) | YES  |     | NULL    |                |
    | start_pos   | int(11)      | YES  |     | NULL    |                |
    | end_pos     | int(11)      | YES  |     | NULL    |                |
    +-------------+--------------+------+-----+---------+----------------+


    mysql> describe document; original documents (should not be changed in the whole process);
    +----------+----------------+------+-----+---------+-------+
    | Field    | Type           | Null | Key | Default | Extra |
    +----------+----------------+------+-----+---------+-------+
    | doc_id   | varchar(300)   | NO   | PRI | NULL    |       |
    | doc_body | varchar(15000) | YES  |     | NULL    |       |
    +----------+----------------+------+-----+---------+-------+


    mysql> describe document_annotation; annotated results; should perform post-processing to get standard format.
    +-------------+----------------+------+-----+---------+-------+
    | Field       | Type           | Null | Key | Default | Extra |
    +-------------+----------------+------+-----+---------+-------+
    | doc_id      | varchar(300)   | NO   | PRI | NULL    |       |
    | model_enum  | varchar(300)   | YES  |     | NULL    |       |
    | entire_text | varchar(15000) | YES  |     | NULL    |       |
    +-------------+----------------+------+-----+---------+-------+

    mysql> describe combinations_completed; document_id-model pair;
    +-------------+--------------+------+-----+---------+----------------+
    | Field       | Type         | Null | Key | Default | Extra          |
    +-------------+--------------+------+-----+---------+----------------+
    | id          | int(11)      | NO   | PRI | NULL    | auto_increment |
    | document_id | varchar(300) | YES  | MUL | NULL    |                |
    | model_enum  | varchar(100) | YES  |     | NULL    |                |
    | checked_out | tinyint(1)   | YES  |     | 0       |                |
    | completed   | tinyint(1)   | YES  |     | 0       |                |
    +-------------+--------------+------+-----+---------+----------------+

    """

    def __init__(self):

        # Create a connection to the database that we can hold onto and use for future queries
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="reddit_linking_db",
            port=3306,
            passwd="sneakyplatypusofdoom",
            database="reddit_phrase_adoption",
            auth_plugin='mysql_native_password',
            use_pure=True
        )

        self.mycursor = self.mydb.cursor()

    def fetch(self, query):
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        return result

    @property
    def query_doc_anno(self):
        return f"select * from document_annotation;"

    @property
    def query_ori_doc(self):
        return f"select * from document;"

    @property
    def query_ori_anno(self):
        return f"select * from annotations;"

    @property
    def query_doc_model_pair(self):
        return f"select * from combinations_completed;"

    @property
    def query_accept_user_doc_anno(self):
        return f"select * from document_annotation where user_id in (select user_id from user_information where (control_passed = 1 and result_code is not NULL));"

    @property
    def query_reject_user_doc_anno(self):
        return f"select * from document_annotation where user_id in (select user_id from user_information where (control_passed = 0 and result_code is not NULL));"

