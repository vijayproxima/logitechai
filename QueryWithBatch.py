from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType

from dotenv import load_dotenv
load_dotenv()

import os
import psycopg2

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

DBNAME=os.environ["DBNAME"] 
DBPWD=os.environ["DBPWD"]
DBUSER=os.environ["DBUSER"] 
DBPORT=os.environ["DBPORT"]
DBHOST=os.environ["DBHOST"]

db = SQLDatabase.from_uri(f"postgresql+psycopg2://{DBUSER}:{DBPWD}@localhost:5432/{DBNAME}")

toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
#setup llm

#llm = OpenAI(temperature=0)


#setup the prompt

QUERY = """
feed with the input question, create correct postgresql query with right syntax which can run and exclude LIMIT, 
secondly observe the results of the query and finally return the answer. Do not truncate or limit the final answer.
Use the below format while answering:

Input: Input Question here
SQLQuery: generate an SQL query
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""

#setup llm chain
import streamlit as st

# Define a function to retrieve data in batches
def fetch_data_in_batches(query, batch_size):
    offset = 0
    all_results = []

    while True:
        with st.spinner("Generating response, please wait...."):
        # Create the SQL query with a LIMIT clause for the current batch
        
   
        #prompt = f"{context}\nQuestion: {query}\nAnswer:"

            question = QUERY.format(question=query)
            print(agent_executor.run(question))
            response=agent_executor.run(question)
        
            with st.chat_message("assistant"):
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        query_with_limit = f"{query} OFFSET {offset} LIMIT {batch_size}"

        # Execute the SQL query to fetch the current batch
        result = db._execute(query_with_limit)

        # Check if the current batch is empty
        if not result:
            break

        # Append the current batch to the list of all results
        all_results.extend(result)

        # Increment the offset
        offset += batch_size

    return all_results

st.title("Welcome to Logitech !!!")

query = st.chat_input("Say something..")

if query:
    st.write(f"user asked: {query}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if query := st.chat_input("Please ask your queries related to Logitech?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})


# Define the user's SQL query (generic)
user_query = query  # You can adapt this to handle any user's query

# Set the batch size (you can adjust this as needed)
batch_size = 10

# Fetch data in batches using the user's query
query_results=[]
if query:
    query_results = fetch_data_in_batches(user_query, batch_size)

# Display the results
with st.chat_message("assistant"):
    #st.markdown("The results of the query are:")
    for row in query_results:
        st.markdown(row)  # Display the results as they are in the database

    st.session_state.messages.append({"role": "assistant", "content": "The results of the query are listed above."})
