from dotenv import load_dotenv
load_dotenv() ##load all environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load Google Gemini, provide sql query as response

def get_gemini_respone(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    question = str(question)

    response = model.generate_content([prompt[0],question])
    return response.text

## Retrieve quer from sql database 
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Defining the prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION , MARKS \nFor example,

    \nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;

    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT where CLASS="Data Science"; 

    \nExample 3 - Give me the names of students having marks above 60?, 
    the SQL command will be something like this SELECT * FROM STUDENT where MARKS>60;

    \nExample 4 - Furnish the count of distinct students along with the highest marks achieved in the entire STUDENT database,
    the SQL command will be something like this SELECT DISTINCT COUNT(*) FROM STUDENT WHERE MARKS = (SELECT MAX(MARKS) FROM STUDENT); 

    \nExample 5 - Retrieve the names, classes, and marks of students who are enrolled in the Data Science class and belong to Section 'A',
    the SQL command will be something like this SELECT NAME,CLASS,MARKS FROM STUDENT WHERE CLASS = 'Data Science' AND SECTION = 'A'; 

    \nExample 6 - Display the names, classes, and average marks of students who are enrolled in the 'Machine Learning' class, sorted in descending order of their average marks,
    the SQL command will be something like this SELECT NAME,CLASS,AVG(MARKS) FROM STUDENT WHERE CLASS = 'Machine Learning' ORDER BY AVG(MARKS) DESC; 

    \nExample 7 - Present a list of students from the STUDENT database who have marks greater than 60 and are enrolled in classes other than 'App Development'.Sort the data in asscending order of their names,
    the SQL command will be something like this SELECT NAME FROM STUDENT WHERE CLASS NOT IN ('App Development') AND MARKS>60 ORDER BY NAME ASC; 
    also the sql code should not have ``` in beginning or end and sql word in output


    """
]

## Streamlit Application

st.set_page_config(page_title="SQL Query Retrieval")
st.header("SQL Data Retriever")

question = st.text_input("Input: ", key="input")

submit = st.button("Submit")

if submit:
        response =get_gemini_respone(question,prompt)
        print(response)
        data = read_sql_query(response,"student.db")
        st.subheader("Response")
        for row in data:
            print(row)
            st.header(row)
        
