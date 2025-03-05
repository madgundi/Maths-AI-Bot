import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory

# Secure API Key Handling
API_KEY = "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"

# Initialize Groq Chat Model
chat = ChatGroq(temperature=0.7, model_name="llama3-70b-8192", groq_api_key=API_KEY)

# Initialize Conversation Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define System Prompt
SYSTEM_PROMPT = """
System Prompt: You are a highly skilled mathematician specializing in advanced concepts such as differential geometry, topology, and abstract algebra.
You apply these concepts to real-world problems, particularly in physics and computer science. Your explanations are clear, rigorous, and structured.

Instructions for Generating Responses:
1. Use a systematic, step-by-step approach like a professor explaining concepts.dont give much sentance
2. Break down problems into smaller logical steps before proceeding to calculations.
3. Use proper LaTeX formatting for mathematical expressions.
4. Provide detailed reasoning behind each step to ensure clarity.
5. If multiple methods exist, explain the advantages and disadvantages of each.
6. Conclude with a final boxed answer (if applicable) for clarity.
"""

def query_math_ai(user_query):
    past_chat_history = memory.load_memory_variables({}).get("chat_history", [])
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Past Chat: {past_chat_history}\n\nQuestion: {user_query}")
    ]
    try:
        response = chat.invoke(messages)
        memory.save_context({"input": user_query}, {"output": response.content})
        return response.content if response else "⚠️ No response received."
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Streamlit Chat UI
def main():
    st.set_page_config(page_title="AlgebrAI", page_icon="🧮", layout="wide")

    # Custom CSS for chat alignment and icons
    st.markdown("""
        <style>
        
        .user-message {
            background-color: rgb(241 234 26);
            color: black;
            padding: 10px;
            border-radius: 10px;
            max-width: 70%;
            text-align: left;
            float: left;
            clear: both;
            margin: 5px 0;
            display: flex;
            align-items: center;
        }
        .ai-message {
            background-color: rgb(163, 168, 184);
            color: black;
            padding: 10px;
            border-radius: 10px;
            max-width: 70%;
            text-align: left;
            float: left;
            clear: both;
            margin: 5px 0;
            display: flex;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Centering the title
    st.markdown("<h1 style='text-align: center;'>AlgebrAI - Advanced Math Chatbot</h1>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat messages
    for message in st.session_state.messages:
        st.markdown(message["content"], unsafe_allow_html=True)

    user_input = st.chat_input("🔢 Type your math question here:")
    if user_input:
        user_message = f"""
            <div class='user-message'>
                <span>😀 : {user_input}</span>
            </div>
        """
        st.session_state.messages.append({"role": "user", "content": user_message})
        st.markdown(user_message, unsafe_allow_html=True)

        with st.spinner("🔍 Thinking..."):
            response = query_math_ai(user_input)

        styled_response = f"""
            <div class="ai-message">
                  <span>🤖 : {response}</span>
            </div>
        """
        st.session_state.messages.append({"role": "assistant", "content": styled_response})
        st.markdown(styled_response, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
