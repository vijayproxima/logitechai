from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType

from dotenv import load_dotenv, find_dotenv
import os
import psycopg2

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

DBNAME=os.environ["DBNAME"] 
DBPWD=os.environ["DBPWD"]
DBUSER=os.environ["DBUSER"] 
DBPORT=os.environ["DBPORT"]
DBHOST=os.environ["DBHOST"]

db = SQLDatabase.from_uri(f"postgresql+psycopg2://{DBUSER}:{DBPWD}@localhost:5432/{DBNAME}")

#setup llm

#llm = OpenAI(temperature=0)


#setup the prompt

QUERY = """
feed with the input question, first create correct postgresql query with right syntax which can run, 
secondly observe the results of the query and finally return the answer.
Use the below format while answering:

Input: Input Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""

#setup llm chain
import streamlit as st

st.title("Welcom to Waterworth !!!")

query = st.chat_input("Say something..")

if query:
    st.write(f"user asked:{query}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if query := st.chat_input("Please ask your queries related to your Long term financial model ?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})


with st.spinner("Generating response, please wait...."):
    if query:
        #prompt = f"{context}\nQuestion: {query}\nAnswer:"

        question = QUERY.format(question=query)
        print(agent_executor.run(question))
        response=agent_executor.run(question)
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


# def execute_chain():
#     print("Type 'exit' to quit")


# exeuction from CLI
    # while True:
    #     feed = input("Enter your question: ")

    #     if feed.lower() == 'exit':
    #         print('Exiting...')
    #         break
    #     else:
    #         try:
    #             question = QUERY.format(question=feed)
    #             print(agent_executor.run(question))
    #         except Exception as e:
    #             print(e)


#execute_chain()