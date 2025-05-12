import logging
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Default prompt for crypto assistant
DEFAULT_CRYPTO_PROMPT = """
You are a knowledgeable AI assistant specialized in cryptocurrency.
Answer the user's question using the provided context.
If the answer is not in the context, say "I don't know."
Avoid guessing and do not provide unrelated information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

def get_available_models():
    """Return a list of available Ollama models"""
    return ["llama3", "llama3:8b", "mistral", "gemma:7b"]

def get_llm(model_name="llama3"):
    """Get Ollama LLM instance"""
    try:
        return ChatOllama(model=model_name)
    except Exception as e:
        logger.error(f"Error initializing Ollama LLM {model_name}: {e}")
        logger.info("Falling back to llama3 model")
        return ChatOllama(model="llama3")

def create_qa_chain(vectorstore, model_name="llama3", prompt_template=DEFAULT_CRYPTO_PROMPT):
    """Create a question-answering chain with Ollama LLM and vector store"""
    try:
        # Get LLM
        llm = get_llm(model_name)
        
        # Create prompt
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_template
        )
        
        # Create chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 5, "fetch_k": 10}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return chain
        
    except Exception as e:
        logger.error(f"Error creating QA chain: {e}")
        raise e
