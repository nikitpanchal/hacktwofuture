from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI
from utils.tokenizer import OpenAITokenizerWrapper
import os
load_dotenv()

# Initialize OpenAI client (make sure you have OPENAI_API_KEY in your environment variables)
client = OpenAI(
    # This is the default and can be omitted
    api_key='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',
)


tokenizer = OpenAITokenizerWrapper()  # Load our custom tokenizer for OpenAI
MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length


# --------------------------------------------------------------
# Extract the data
# --------------------------------------------------------------

converter = DocumentConverter()
result = converter.convert("/Users/nikitpanchal/Documents/hacktwofuture/hack2_future/docling/OYO202430.pdf")
 
# --------------------------------------------------------------
# Apply hybrid chunking
# --------------------------------------------------------------

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=MAX_TOKENS,
    merge_peers=True,
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks =list(chunk_iter)
chunks[0].model_dump()
#len(chunks)
