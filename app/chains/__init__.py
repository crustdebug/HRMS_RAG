from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from app.prompts.qa_prompt import qa_prompt, partial_prompt
from app.prompts.intent_prompt import intent_prompt
from app.prompts.ack_response_prompt import ack_response_prompt
from app.chains.config import assistant_name, company_name, role, rules_str
from app.utils.memory_manager import get_user_memory

import os

embedding = HuggingFaceEmbeddings(model_name="thenlper/gte-large", encode_kwargs={"normalize_embeddings": True})
db = FAISS.load_local("data/faiss_index_gemini_CO_gtelarge", embedding, allow_dangerous_deserialization=True)

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

# List of models to try in order (primary + fallbacks) - Free tier only
MODEL_FALLBACKS = [
    "gemini-2.5-flash-lite",  # Primary - Best for free tier (15 RPM, 1000 RPD)
    "gemini-2.5-flash",       # Fallback 1 - Good balance (10 RPM, 250 RPD)
    "gemini-2.5-pro",         # Fallback 2 - Most capable (2 RPM, 50-100 RPD)
]

def create_llm_with_fallback():
    """Create LLM with fallback models"""
    for model_name in MODEL_FALLBACKS:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.1,
                google_api_key=gemini_api_key
            )
            # Test the model with a simple call
            llm.invoke("test")
            print(f"✓ Successfully initialized LLM with model: {model_name}")
            return llm
        except Exception as e:
            print(f"✗ Failed to initialize {model_name}: {str(e)[:100]}")
            continue
    
    # If all models fail, raise an error
    raise Exception("All fallback models failed to initialize")

llm = create_llm_with_fallback()  

retriever = db.as_retriever(search_kwargs={"k": 10, "fetch_k": 15})

intent_chain = LLMChain(llm=llm, prompt=intent_prompt)
ack_chain = LLMChain(llm=llm, prompt=ack_response_prompt)

ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True,k=2)
