from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pprint import pformat
from app.models.query_model import Query
from app.chains import intent_chain, ack_chain, assistant_name, company_name, role, MODEL_FALLBACKS
from app.chains.qa_chain import get_qa_chain_for_user
from app.utils.gibberish import is_gibberish
from app.utils.memory_manager import get_user_memory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.llm import LLMChain
from app.prompts.intent_prompt import intent_prompt
from app.prompts.ack_response_prompt import ack_response_prompt
import os

router = APIRouter()

def execute_with_fallback(chain, **kwargs):
    """Execute chain with model fallback on failure"""
    last_error = None
    
    for model_name in MODEL_FALLBACKS:
        try:
            # Try with current model
            result = chain.run(**kwargs)
            return result
        except Exception as e:
            last_error = e
            error_msg = str(e).lower()
            
            # Check if it's a model-related error
            if "not found" in error_msg or "404" in error_msg or "model" in error_msg:
                print(f"✗ Model failed, trying next fallback...")
                
                # Try next model
                try:
                    gemini_api_key = os.getenv("GOOGLE_API_KEY")
                    new_llm = ChatGoogleGenerativeAI(
                        model=model_name,
                        temperature=0.1,
                        google_api_key=gemini_api_key
                    )
                    
                    # Update chain's LLM
                    if hasattr(chain, 'llm'):
                        chain.llm = new_llm
                    
                    # Retry with new model
                    result = chain.run(**kwargs)
                    print(f"✓ Successfully switched to fallback model: {model_name}")
                    return result
                except:
                    continue
            else:
                # Non-model error, raise immediately
                raise e
    
    # All models failed
    raise Exception(f"All fallback models failed. Last error: {last_error}")

@router.post("/chat")
async def chat(query: Query):
    try:
        user_input = query.query.strip()
        user_id = query.user_id

        memory = get_user_memory(user_id)
        qa_chain = get_qa_chain_for_user(user_id)
        qa_chain.memory = memory

        if is_gibberish(user_input):
            return JSONResponse(content={"response": "It seems like that was a typo. Could you please rephrase your question?"})

        # Use fallback for intent classification
        intent = execute_with_fallback(
            intent_chain,
            query=user_input,
            chat_history=memory.buffer
        ).strip().lower()

        if intent == "ack":
            memory.clear()
            # Use fallback for acknowledgment response
            response = execute_with_fallback(
                ack_chain,
                query=user_input,
                assistant_name=assistant_name,
                company_name=company_name,
                role=role
            )
        else:
            # Use fallback for QA
            response = execute_with_fallback(qa_chain, question=user_input)

        formatted_output = pformat(response) if isinstance(response, (dict, list)) else str(response)
        return JSONResponse(content={"response": formatted_output})
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"Sorry, I encountered an error: {str(e)}"},
            status_code=500
        )