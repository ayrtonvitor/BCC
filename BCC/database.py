import sqlite3

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

cursor.execute("""
               CREATE TABLE pages (
                   class_code TEXT,
                   title TEXT NOT NULL,
                   url TEXT NOT NULL,
                   PRIMARY KEY(class_code)
              );
               """)

cursor.execute("""
               CREATE TABLE page_sections (
                   class_code TEXT,
                   title TEXT NOT NULL,
                   section_text TEXT,
                   download_link TEXT,
                   section_order INT NOT NULL,
                   FOREIGN KEY(class_code) REFERENCES pages (class_code),
                   PRIMARY KEY (class_code, section_order)
              );
               """)

cursor.execute("""
               CREATE TABLE redirections (
                   inner_redirect_link TEXT NOT NULL,
                   class_code TEXT NOT NULL,
                   section_order INTEGER NOT NULL,
                   FOREIGN KEY (class_code, section_order) REFERENCES
               page_sections (class_code, section_order),
                   FOREIGN KEY (inner_redirect_link) REFERENCES pages (url)
              );
               """)

cursor.execute("""
                CREATE TABLE outter_links (
                    url TEXT NOT NULL,
                    class_code TEXT NOT NULL,
                    section_order INTEGER NOT NULL,
                    url_order INTEGER NOT NULL,
                    FOREIGN KEY (class_code, section_order) REFERENCES page_sections
                      (class_code, section_order)
              );
               """)

cursor.execute("""
                CREATE TABLE Downloads (
                    url TEXT NOT NULL,
                    is_gdrive INTEGER NOT NULL,
                    class_code TEXT NOT NULL,
                    section_order INTEGER NOT NULL,
                    url_order INTEGER NOT NULL,
                    path TEXT,
                    FOREIGN KEY (class_code, section_order) REFERENCES page_sections
                      (class_code, section_order)
              );
               """)

connection.commit()
connection.close()
