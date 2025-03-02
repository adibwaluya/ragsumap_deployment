import streamlit as st

st.title("RAG PDF Chat History")

# Ensure chat history exists
if "store" in st.session_state and st.session_state["store"]:
    session_id = st.text_input("Session ID", value="default_session")
    
    if session_id in st.session_state["store"]:
        history = st.session_state["store"][session_id].messages
        
        if history:
            st.subheader(f"Chat History for Session: {session_id}")
            
            for msg in history:
                role = "🤖 Assistant:" if msg.type == "ai" else "🧑 You:"
                st.markdown(f"**{role}** {msg.content}")
        else:
            st.write("No messages in this session yet.")
    else:
        st.write("No chat history available for this session.")
else:
    st.write("No chat history found.")

# Add a button to go back
st.page_link("pages/RAG_PDF_App.py", label="Back to Chat")