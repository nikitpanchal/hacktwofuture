from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

 
print(os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENAI_API_KEY"))
print (os.environ)