import pandas as pd
import sqlite3
import os


def import_index_to_db(excel_file, path_to_db, db_name):
    if not os.path.isfile(excel_file):
        print("File '" + excel_file + "' does not exist")
        return
    data = pd.read_excel(excel_file)
    # print(data)
    conn = sqlite3.connect(path_to_db)
    data.to_sql(name=db_name, con=conn, if_exists="replace", index=False)

    # commit the changes to db
    conn.commit()
    conn.close()

    print("Data from '" + excel_file +
          "' is written to '" + db_name + "'")


if __name__ == "__main__":
    db = "db/index.db"

    import_index_to_db('dja_19900101_20230730.xlsx', db, 'DJA')
    import_index_to_db('ixic_19900101_20230730.xlsx', db, 'IXIC')
    import_index_to_db('spx_19900101_20230730.xlsx', db, 'SPX')
    import_index_to_db('ssec_20050101_20230730.xlsx', db, 'SSEC')
