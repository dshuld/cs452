# -*- coding: utf-8 -*-
"""openai_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pt1YmfM4LlexW4OqOlWw9jHV5CCuMOn4
"""

!pip install openai

!pip install sqlalchemy
!pip install psycopg2

from openai import OpenAI
import psycopg2
from sqlalchemy import create_engine, text, Table, MetaData
from google.colab import userdata

conn_string = userdata.get('TIMESCALE_CONN')

client = OpenAI(
    api_key = userdata.get('OPENAI_API_KEY'),
    organization = userdata.get('OPENAI_ORG_ID')
)

create_publisher = """
CREATE TABLE publisher (
    publisher_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(15)
);
"""
create_author = """
CREATE TABLE author (
    author_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE
);
"""
create_book = """
CREATE TABLE book (
    book_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(50),
    publish_date DATE,
    author_id INT,
    publisher_id INT,
    FOREIGN KEY (author_id) REFERENCES author(author_id) ON DELETE CASCADE,
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id) ON DELETE SET NULL
);
"""

drop_if_exists = """
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS publisher;
"""
with psycopg2.connect(conn_string) as conn:
    with conn.cursor() as cursor:
        cursor.execute(drop_if_exists)
        cursor.execute(create_publisher)
        cursor.execute(create_author)
        cursor.execute(create_book)

insert_publisher = """
INSERT INTO publisher (publisher_id, name, address, phone)
VALUES
(1, 'Penguin Random House', '1745 Broadway, New York, NY 10019', '212-782-9000'),
(2, 'HarperCollins', '195 Broadway, New York, NY 10007', '212-207-7000'),
(3, 'Simon & Schuster', '1230 Avenue of the Americas, New York, NY 10020', '212-698-7000'),
(4, 'Macmillan Publishers', '120 Broadway, New York, NY 10271', '646-307-5151'),
(5, 'Hachette Book Group', '1290 Avenue of the Americas, New York, NY 10104', '212-364-1100'),
(6, 'Scholastic Inc.', '557 Broadway, New York, NY 10012', '212-343-6100'),
(7, 'Oxford University Press', '198 Madison Avenue, New York, NY 10016', '212-726-6000');
"""
insert_author = """
INSERT INTO author (author_id, first_name, last_name, birth_date)
VALUES
(1, 'George', 'Orwell', '1903-06-25'),
(2, 'J.K.', 'Rowling', '1965-07-31'),
(3, 'F. Scott', 'Fitzgerald', '1896-09-24'),
(4, 'Stephen', 'King', '1947-09-21'),
(5, 'Agatha', 'Christie', '1890-09-15'),
(6, 'Isaac', 'Asimov', '1920-01-02'),
(7, 'Mark', 'Twain', '1835-11-30'),
(8, 'Jane', 'Austen', '1775-12-16'),
(9, 'J.R.R.', 'Tolkien', '1892-01-03'),
(10, 'Arthur', 'Conan Doyle', '1859-05-22'),
(11, 'Mary', 'Shelley', '1797-08-30'),
(12, 'H.G.', 'Wells', '1866-09-21'),
(13, 'Oscar', 'Wilde', '1854-10-16'),
(14, 'Harper', 'Lee', '1926-04-28'),
(15, 'C.S.', 'Lewis', '1898-11-29');
"""
insert_book = """
INSERT INTO book (book_id, title, genre, publish_date, author_id, publisher_id)
VALUES
(1, '1984', 'Dystopian', '1949-06-08', 1, 1),
(2, 'Harry Potter and the Sorcerer''s Stone', 'Fantasy', '1997-06-26', 2, 2),
(3, 'The Great Gatsby', 'Fiction', '1925-04-10', 3, 3),
(4, 'Animal Farm', 'Political Satire', '1945-08-17', 1, 1),
(5, 'Harry Potter and the Chamber of Secrets', 'Fantasy', '1998-07-02', 2, 2),
(6, 'The Shining', 'Horror', '1977-01-28', 4, 4),
(7, 'It', 'Horror', '1986-09-15', 4, 4),
(8, 'Murder on the Orient Express', 'Mystery', '1934-01-01', 5, 2),
(9, 'The Murder of Roger Ackroyd', 'Mystery', '1926-06-01', 5, 2),
(10, 'Foundation', 'Science Fiction', '1951-06-01', 6, 5),
(11, 'I, Robot', 'Science Fiction', '1950-12-02', 6, 5),
(12, 'The Adventures of Tom Sawyer', 'Fiction', '1876-06-01', 7, 7),
(13, 'Pride and Prejudice', 'Romance', '1813-01-28', 8, 7),
(14, 'The Lord of the Rings: The Fellowship of the Ring', 'Fantasy', '1954-07-29', 9, 1),
(15, 'The Hobbit', 'Fantasy', '1937-09-21', 9, 1),
(16, 'A Study in Scarlet', 'Mystery', '1887-11-01', 10, 2),
(17, 'Frankenstein', 'Horror', '1818-01-01', 11, 7),
(18, 'The War of the Worlds', 'Science Fiction', '1898-01-01', 12, 4),
(19, 'The Invisible Man', 'Science Fiction', '1897-06-01', 12, 4),
(20, 'The Catcher in the Rye', 'Fiction', '1951-07-16', 3, 3),
(21, 'The Picture of Dorian Gray', 'Philosophical Fiction', '1890-06-20', 13, 6),
(22, 'To Kill a Mockingbird', 'Fiction', '1960-07-11', 14, 6),
(23, 'The Great Divorce', 'Christian Fiction', '1945-01-01', 15, 1),
(24, 'The Hound of the Baskervilles', 'Mystery', '1902-04-01', 10, 3);
"""

with psycopg2.connect(conn_string) as conn:
    with conn.cursor() as cursor:
        cursor.execute(insert_publisher)
        cursor.execute(insert_author)
        cursor.execute(insert_book)

def generateOpenAIResponse(content):
    stream = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result

def extractSQL(value):
    sqlStart = "```sql"
    sqlEnd = "```"
    if sqlStart in value and sqlEnd in value:
        value = value.split(sqlStart)[1]
        value = value.split(sqlEnd)[0]
        value = value.strip()
    else:
        value = "error"

    return value

def runSQL(sql):
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
    return result

preface = "Given tables represented by the following PostgreSQL create statements:\n" + \
    create_publisher + "\n" + create_author + "\n" + create_book + "\n" + \
    "Answer the following question only in a valid PostgreSQL SELECT statement. " + \
    "Be sure to be case-insensitive unless otherwise specified in words or by quotation marks around a term. " + \
    "Do not include any other words, descriptions, or banter. " + \
    "If the question cannot be answered using a SELECT statement to the database, respond with only the word \"error\"\n" + \
    "The question is: "
explanation_1 = "Given tables represented by the following PostgreSQL create statements:\n" + \
    create_publisher + "\n" + create_author + "\n" + create_book + "\n" + \
    "I asked the question: "
explanation_2 = "\nThe answer I received was in the form of a SQL select statement return value. " + \
    "Can you answer the question based on the results? Do not reference the SQL statement, and use as few words as possible besides for the actual data.\n" + \
    "The results were: "

question = ""
response = generateOpenAIResponse(preface + question)
if(response == "error"):
    print("error")
else:
    sql = extractSQL(response)
    print(sql + "\n")
    result = runSQL(sql)
    friendly_result = generateOpenAIResponse(explanation_1 + question + explanation_2 + str(result))
    print(friendly_result)