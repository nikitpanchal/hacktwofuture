import streamlit as st
import lancedb
from openai import OpenAI
from dotenv import load_dotenv
from ollama import chat
from ollama import ChatResponse
from rapidfuzz import fuzz
# Load environment variables
load_dotenv()

 


# Initialize LanceDB connection
@st.cache_resource
def init_db():
    """Initialize database connection.

    Returns:
        LanceDB table object
    """
    db = lancedb.connect("/Users/nikitpanchal/Documents/hacktwofuture/hack2future/hack2_chatagent/data/lancedb")
    return db.open_table("arth_hack2future")


known_companies = ['oyo', 'seruminstitute']

def resolve_company_name_custom(query: str, known_names: list[str], threshold: int = 80):
    query = query.lower()
    tokens = query.split()
    max_len = 5  # max n-gram length to test

    best_match = None
    best_score = 0

    for i in range(len(tokens)):
        for j in range(i + 1, min(i + max_len + 1, len(tokens) + 1)):
            candidate = ' '.join(tokens[i:j])
            for name in known_names:
                score = fuzz.partial_ratio(candidate, name.lower())
                if score > best_score:
                    best_score = score
                    best_match = name

    if best_score >= threshold:
        return best_match
    return None



def get_context(query: str, table, num_results: int = 5) -> str:
    """Search the database for relevant context.

    Args:
        query: User's question
        table: LanceDB table object
        num_results: Number of results to return

    Returns:
        str: Concatenated context from relevant chunks with source information
    """
    company = resolve_company_name_custom(query, known_companies)
    print("metadata.company = '"+company+"'")
    results = table.search(query).limit(num_results).where("metadata.company = '"+company+"'").to_pandas()
    contexts = []

    for _, row in results.iterrows():
        # Extract metadata
        filename = row["metadata"]["filename"]
        page_numbers = row["metadata"]["page_numbers"]
        title = row["metadata"]["title"]
        page_numbers = page_numbers[:1]
        #Build source citation
        source_parts = []
        if filename:
            source_parts.append(filename)
        if page_numbers:
            source_parts.append(f"p. {', '.join(str(p) for p in page_numbers)}")

        source = f"\nSource: {' - '.join(source_parts)}"
        if title:
            source += f"\nTitle: {title}"

        contexts.append(f"{row['text']}{source}")

    return "\n\n".join(contexts)
def llm_stream(messages_with_context):
     response: ChatResponse  = chat(
        model="llama3.2:1b",
        messages=messages_with_context,
        stream=True,
        )  
     for chunk in response:
            yield chunk['message']['content']

def get_chat_response(messages, context: str) -> str:
     
    system_prompt = f"""You are a helpful assistant that reponse prompts based on the provided context.
    Use only the information from the context to answer questions. If you're unsure or the context
    doesn't contain the relevant information, say so.
    Prompt: 
    {messages}
    Context:
    {context} 
    """

    messages_with_context = [{"role": "system", "content": system_prompt}]
    def llm_stream():
            stream: ChatResponse  = chat(
        model="llama3.2:1b",
        messages=messages_with_context,
        stream=True,
     )  
            for chunk in stream:
                yield chunk['message']['content']
    # Create the streaming response
      
    # for chunk in stream:
    #     yield chunk['message']['content']
    # Use Streamlit's built-in streaming capability
    response = st.write_stream(llm_stream())
    return response


# Initialize Streamlit app
st.title("Arth")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize database connection
table = init_db()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the document"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get relevant context
    with st.status("Searching document...", expanded=False) as status:
        context = get_context(prompt, table,30)
        st.markdown(
            """
            <style>
            .search-result {
                margin: 10px 0;
                padding: 10px;
                border-radius: 4px;
                background-color: #f0f2f6;
            }
            .search-result summary {
                cursor: pointer;
                color: #0f52ba;
                font-weight: 500;
            }
            .search-result summary:hover {
                color: #1e90ff;
            }
            .metadata {
                font-size: 0.9em;
                color: #666;
                font-style: italic;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        st.write("Found relevant sections:")
        for chunk in context.split("\n\n"):
            # Split into text and metadata parts
            parts = chunk.split("\n")
            text = parts[0]
            metadata = {
                line.split(": ")[0]: line.split(": ")[1]
                for line in parts[1:]
                if ": " in line
            }
            source = metadata.get("Source", "Unknown source")
            title = metadata.get("Title", "Untitled section")
           

            st.markdown(
                f"""
               <div class="search-result">
                    <details>
                        <summary>{source}</summary>
                        <div class="metadata">Section: {title}</div>
                        <div style="margin-top: 8px;">{text}</div>
                    </details>
                </div>
            """,
                unsafe_allow_html=True,
            )

    # Display assistant response first
    with st.chat_message("assistant"):
        # Get model response with streaming
        response = get_chat_response(st.session_state.messages, context)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})