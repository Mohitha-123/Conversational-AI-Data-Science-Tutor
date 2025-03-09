import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize memory
memory = ConversationBufferMemory()

# Initialize Gemini 1.5 Pro Model (Replace with actual API key and settings)
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key="AIzaSyBItvysBggCo5T2iE61M209b24e36FmiBo")

def conversational_tutor(user_input):
    """Function to interact with the conversational AI tutor."""
    memory.save_context({"human": user_input}, {"ai": "Processing..."})  # Temporary response
    
    conversation_history = memory.load_memory_variables({})
    
    prompt = f"""
    You are a data science tutor. Answer ONLY data science-related questions.
    If the user asks something unrelated, politely decline.
    Keep the conversation aware using memory.
    
    Conversation history: {conversation_history}
    
    User: {user_input}
    """
    
    response = chat_model.invoke(prompt)
    
    # Extract content properly
    if isinstance(response, dict):
        response_text = response.get("content", "I'm sorry, I couldn't generate a response.")
    elif hasattr(response, 'content'):  
        response_text = response.content  
    else:
        response_text = str(response)  

    # Store cleaned response in memory
    memory.save_context({"human": user_input}, {"ai": response_text})  

    return response_text


# Streamlit UI
def main():
    st.image("C:\\Users\\DELL\\Downloads\\181.jpg", use_container_width=True)
    
    st.title("Conversational AI Data Science Tutor")
    st.write("Ask me anything about Data Science!")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        response = conversational_tutor(user_input)
        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()
