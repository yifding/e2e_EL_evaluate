import mysql.connector
import sys


class DataBaseQueryUtil:

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

    def escape_string(self, s):
        return self.mydb.converter.escape(s)

    def fetch_document_annotations(self):

        query = f"select * from document_annotation;"
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()

        return result


def main():

    dbq = DataBaseQueryUtil()

    annotated_documents = dbq.fetch_document_annotations()

    for doc in annotated_documents:

        doc_id = doc[0]
        model_type = doc[1]
        annotation_text = doc[2]

        print(doc_id, model_type)
        print(annotation_text)

if __name__ == '__main__':
    main()