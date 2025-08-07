import streamlit as st
import threading
from utils.rag_utils import load_documents, retrieve_relevant_chunks, start_watchdog
from utils.web_search import search_web
from utils.response_modes import format_response
from utils.prompt_engineering import format_prompt
from models.llm import get_llm_response

@st.cache_resource
def start_file_watcher():
    thread = threading.Thread(target=start_watchdog, daemon=True)
    thread.start()
    return True

def instructions_page():
    st.title("CivicBot: Urban Planning Feedback Assistant - Instructions")
    st.markdown("""
    Welcome to CivicBot! Here's how to use this assistant:

    - Enter your urban planning or project-related query on the **Chat** page.
    - Choose the response mode: **Concise** or **Detailed**.
    - Click Submit to get insights.
    - Clear chat history anytime from the sidebar.
    - Download chat history as .txt file.

    **Sample Questions:**
    - What are the rules for public art installations?
    - Can you find examples of how other municipalities have managed traffic during large construction projects?
    - What is the city's policy on water conservation?
    - What are the specific materials being used for the new community center's roof?
    """
    )

def chat_page():
    st.title("CivicBot: Urban Planning Feedback Assistant")
    start_file_watcher()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.messages:
        st.markdown("### Chat History")
        for entry in st.session_state.messages:
            st.markdown(f"**You:** {entry['query']}")
            st.markdown(f"**CivicBot:** {entry['response']}")
            st.markdown("---")

    query = st.text_input("Ask about a project:")
    mode = st.radio("Response Mode", ["Concise", "Detailed"])
    model_choice = st.selectbox("Choose Model", ["llama-3.3-70b-versatile"])

    if st.button("Submit") and query.strip() != "":
        documents = load_documents()
        chunks = retrieve_relevant_chunks(query, documents)
        context = "\n".join(chunks)

        if "study" in query.lower() or "research" in query.lower():
            web_info = search_web(query)
            context += "\nWeb Info: " + web_info

        user_prompt = format_prompt(query, mode)
        prompt = f"{context}\n\n{user_prompt}"

        response = get_llm_response(prompt, model=model_choice)
        formatted_response = format_response(response, mode.lower())

        st.session_state.messages.append({
            "query": query,
            "response": formatted_response
        })

        st.markdown("### Latest Response")
        st.write(formatted_response)


def main():
    st.set_page_config(
        page_title="CivicBot",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to:", ["Instructions", "Chat"])

        if page == "Chat":
            st.divider()
            if st.button("Clear Chat History"):
                st.session_state.messages = []
            history_text = get_chat_history_txt()
            st.download_button(
                label="Download Chat History (.txt)",
                data=history_text,
                file_name="chat_history.txt",
                mime="text/plain"
            )

    if page == "Instructions":
        instructions_page()
    elif page == "Chat":
        chat_page()

def get_chat_history_txt():
    if "messages" not in st.session_state or not st.session_state.messages:
        return "No chat history available."

    lines = []
    for entry in st.session_state.messages:
        lines.append(f"You: {entry['query']}")
        lines.append(f"CivicBot: {entry['response']}")
        lines.append("")  
    return "\n".join(lines)

if __name__ == "__main__":
    main()
