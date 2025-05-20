import lancedb
from ollama import ChatResponse

# --------------------------------------------------------------
# Connect to the database
# --------------------------------------------------------------
from ollama import chat
uri = "data/lancedb"
db = lancedb.connect(uri)

from rapidfuzz import fuzz
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


# --------------------------------------------------------------
# Load the table
# --------------------------------------------------------------

table = db.open_table("arth_hack2future")

# text =table.search(query="what was the revenue in 2024", query_type="vector").limit(5).to_pandas().iloc[0]["text"]
# text
# --------------------------------------------------------------
# Search the table
# --------------------------------------------------------------

 
def get_context(query: str, table, num_results: int , company: str) -> str:
    """Search the database for relevant context.

    Args:
        query: User's question
        table: LanceDB table object
        num_results: Number of results to return

    Returns:
        str: Concatenated context from relevant chunks with source information
    """
  
    results = table.search(query=query, query_type="vector").where("metadata.company = '"+ company +"'" ).to_pandas()
    results
    contexts = []
    
    for _, row in results.iterrows():
        # Extract metadata
         
        

        contexts.append(f"{row['text']}")

    return results
pass


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
  
    # Create the streaming response
    stream: ChatResponse  = chat(
        model="llama3.2:1b",
        messages=messages_with_context,
        stream=True,
    )   
    for chunk in stream:
       print(chunk['message']['content'], end='', flush=True)
    # Use Streamlit's built-in streaming capability
     
   
pass
pri = 'can you tell me the REVENUE of OYO'

known_companies = ['oyo', 'seruminstitute']

 
company = resolve_company_name_custom(pri,known_companies)
print(company)
 
context = get_context(pri,table,100,company)
 
response = get_chat_response(pri, context)