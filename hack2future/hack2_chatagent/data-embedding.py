from typing import List
import os
import lancedb
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from openai import OpenAI
from utils.tokenizer import OpenAITokenizerWrapper
from transformers import AutoTokenizer,  pipelines
from sentence_transformers import SentenceTransformer
 

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

resolve_company_name_custom("Hi could you tell me what is Serum institure about ", known_companies)
# Initialize OpenAI client (make sure you have OPENAI_API_KEY in your environment variables)
 
# # --------------------------------------------------------------
# # Create a LanceDB database and table
# # --------------------------------------------------------------
filename = 'OYO_202430.pdf'
 # Create a LanceDB database
db = lancedb.connect("data/lancedb")

func = get_registry().get("ollama").create(name="all-minilm:l6-v2",host='http://localhost:11434')

class ChunkMetadata(LanceModel):
       
        company: str | None
        filename: str | None
        page_numbers: List[int] | None
        title: str | None
       


    # Define the main Schema
class Chunks(LanceModel):
        text: str = func.SourceField()
        vector: Vector(func.ndims()) = func.VectorField()  # type: ignore
        metadata: ChunkMetadata

if "arth_hack2future" not in db.table_names():
    table = db.create_table("arth_hack2future", schema=Chunks, mode="create")
else:
    table = db.open_table("arth_hack2future")

def file_already_ingested(table, filename):
    dummy_vector = [0.0] * 384
    result = table.search(dummy_vector).where("metadata.filename = '"+ filename +"'").limit(1).to_pandas()
     
    return not result.empty

# # --------------------------------------------------------------
# # Prepare the chunks for the table
# # --------------------------------------------------------------
if not file_already_ingested(table, filename):
     
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    MAX_TOKENS = 215  # text-embedding-3-large's maximum context length



    # # --------------------------------------------------------------
    # # Extract the data
    # # --------------------------------------------------------------

    converter = DocumentConverter()
    result = converter.convert("/Users/nikitpanchal/Documents/hacktwofuture/hack2future/hack2_chatagent/pdfs/"+filename)


    # # --------------------------------------------------------------
    # # Apply hybrid chunking
    # # --------------------------------------------------------------

    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=MAX_TOKENS,
        merge_peers=True,
    )

    chunk_iter = chunker.chunk(dl_doc=result.document)
    chunks = list(chunk_iter)

    # # Get the OpenAI embedding function
    #func = get_registry().get("ollama").create(name="all-minilm:l6-v2",host='http://localhost:11434')
    # #func = get_registry().get("huggingface").create(name="sentence-transformers/all-MiniLM-L6-v2")
    # #func = SentenceTransformer("intfloat/e5-large-v2")

    # # Define a simplified metadata schema
    # # Create table with processed chunks
    processed_chunks = [
         
        {
            
            "text": chunk.text,
            "metadata": {
                "company" : chunk.meta.origin.filename.split("_")[0].lower(),
                "filename": chunk.meta.origin.filename,
                "page_numbers": [
                    page_no
                    for page_no in sorted(
                        set(
                            prov.page_no
                            for item in chunk.meta.doc_items
                            for prov in item.prov
                        )
                    )
                ]
                or None,
                "title": chunk.meta.headings[0] if chunk.meta.headings else None
                
            }
        }
        for chunk in chunks
    ]
     
    table.add(processed_chunks)
    
table.to_pandas()

 
