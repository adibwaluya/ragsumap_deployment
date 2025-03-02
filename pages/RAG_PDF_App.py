import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv
# """ import pysqlite3 as sqlite3
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3') """
import sqlite3

load_dotenv()

# Streamlit config
st.set_page_config(page_title="RAG PDF Chat", layout="wide")
st.title("Conversational RAG with PDF Upload")
st.write("Upload a PDF and chat with its content.")

api_key = st.text_input("Enter your Groq API key:", type="password")

if api_key:
    ## Initialize Gemma model
    llm = ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")
    session_id = st.text_input("Session ID", value="default_session")

    if "store" not in st.session_state:
        st.session_state["store"] = {}

    uploaded_files = st.file_uploader("Upload a PDF file", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            temppdf = f"./temp.pdf"     # temporary pdfs in local
            with open(temppdf, "wb") as file:
                file.write(uploaded_file.getvalue())

            # load pdf and read content
            loader = PyPDFLoader(temppdf)
            docs = loader.load()
            documents.extend(docs)

        # Split and create embeddings for the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
        splits = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Refer to Langchain docs for vector store usage
        vector_store = Chroma(
            collection_name="test_collection",
            embedding_function=embeddings,
            persist_directory="./chroma"
        )

        batch_size = 50  # Adjust based on the RAM
        for i in range(0, len(splits), batch_size):
            vector_store.add_documents(splits[i:i + batch_size])
        retriever = vector_store.as_retriever()

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Reformulate the question without chat history."),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Use retrieved context to answer. If unknown, say so.\n\n{context}"),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        # Responsible for storing chat history
        def get_session_history(session: str) -> BaseChatMessageHistory:
            if "store" not in st.session_state:
                st.session_state["store"] = {}      # initialize only if missing/doesn't exist

            if session not in st.session_state["store"]:
                ## Initialize the session ID with a ChatMessageHistory if not present
                st.session_state["store"][session] = ChatMessageHistory()
            
            # Return the chat message history for the given session ID
            return st.session_state["store"][session]

        def add_message_to_history(session, message, role="human"):
            # Retrieve chat history for the session
            history = get_session_history(session)
            
            # Ensure the message is not duplicated by checking if it's already in the history
            if message not in [msg.content for msg in history.messages]:
                # Add the message to the history
                history.add_message(role=role, content=message)
        
        # Maintain/keep track of chat history
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        user_input = st.text_input("Your question:")
        if user_input:
            session_history = get_session_history(session_id)
            
            # Call RAG chain to retrieve response
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )

            # session_history.add_user_message(user_input)
            # session_history.add_ai_message(response["answer"])
            
            add_message_to_history(session_id, user_input, role="human")
            add_message_to_history(session_id, response['answer'], role="assistant")

            st.write("Assistant:", response["answer"])

    # Add a link to the chat history page
    st.page_link("pages/RAG_chat_history.py", label="View Chat History 📜")

else:
    st.warning("Please enter your Groq API Key")