import streamlit as st

st.set_page_config(page_title = "Multipage GenAI Application", layout = "wide")
st.title("Welcome to Multipage GenAI Application!")
st.sidebar.success("Select a page above")

st.write("""
This multi-page application allows you to interact with two powerful AI tools to streamline information retrieval.
""")

st.info("""

**Note:** These GenAI applications are developed as part of the submission requirements for the Independent Coursework 2 (IC2).
The goal of this development is to understand some of the processes of applying advanced AI techniques, such as Retrieval-Augmented Generation (RAG) and Natural Language Processing (NLP).
Furthermore, designing a basic user-friendly UI for these applications with streamlit is also part of the goals.
"""        
)

# RAG PDF App section
st.subheader("📄 Conversational RAG with PDF Upload and Chat History Features")
st.write("""
   
   With this application, you can have an interactive and intelligent conversation with AI based on the uploaded PDF file.
   Using RAG, the AI can fetch and process the relevant parts/sections from the document you uploaded and then provide you with the accurate, contextual responses.
   
   - 📂 **Upload a PDF**: After you uploaded the PDF, the AI will use its content as a knowledge base.
   - 🧠 **Memory-Powered Chat**: The chat history ensures the AI remembers past interactions within the session.
   - 🔍 **Ask Anything**: Clarify concepts or content, extract summaries, as well as get detailed explanations directly regarding the uploaded document.    
"""         
)
st.warning("""
           
    **Note:** The RAG PDF app **may take a while to load**, especially for large documents. The reasons would be that:
    - The system needs to extract and process text from the uploaded PDF
    - The model is initialized with the necessary resources
    - As the app splits text of the document into chunks and embeds them into vector store with Chroma, a huge number of chunks may cause **memory overload** or **Chroma database storage issue**
    
    If you experience delays or the app taking a bit of a time to process, please allow a few moments for the system to complete its operation/setup.          
"""
)

# Content Summarization App section
st.subheader("🌍 Summarize Contents from YouTube or Websites")
st.write("""
   
   This application can provide you with summarized content from large amounts of information that a YouTube video or online sources may contain, and you don't have to go through the whole entire content.
   
   - 🎥 **YouTube Video Summarization**: Enter a YouTube URL, and the video's transcript will be analysed by the AI to generate key takeaways.
   - 🌐 **Webpage Summarization**: Paste the link to any article, research papers, or webpage, and the AI will extract essential details.
   - 📊 **Concise and Insightful**: Get short structured summaries to achieve more efficient research and learning processes.     
"""         
)
st.warning("""
           
   **Note:** The Content Summarization app may not work properly for longer YouTube videos (duration > 25 minutes). This is because:
   - **Transcript Limitations:** It's possible that some videos may not provide a full transcript or may have large gaps in the auto-generated transcript.
   - **API Constraints:** Some YouTube APIs may impose restrictions on processing very long transcripts.
   - **Memory & Processing Constraints:** Handling extremely long transcripts can exceed system limits, leading to incomplete or inaccurate summaries.        

If you happen to be experiencing these issues with long videos, consider summarizing shorter clips instead.
"""           
)

st.info("""

**Before you start:**
In order to interact with these GenAI applications, you are required to have a Groq API key. It's basically for:
- accessing Groq's Gemma Model, which powers the conversational capabilities in the app
- authenticating your request and allows the app to interact with Groq's ML platform to generate responses.

To get your API key, you need to **sign up** for an account with Groq and **request an API key** from their platform.

For more information, read the following [documentation](https://console.groq.com/docs/quickstart)
"""        
)

# Basic Navigation How-To
st.subheader("How to Navigate...")
st.write("""
         
   To switch between these applications, use the **sidebar** menu on the left. Happy interacting!      
"""         
)

st.success("Get started now and try these AI-powered tools!")