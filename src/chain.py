from langchain_core.prompts import ChatPromptTemplate            #formats the pdf context and user's question into a prompt
from langchain_core.output_parsers import StrOutputParser        #converts the model's response into a plain string
from src.generation import get_chat_model
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import logging

logger = logging.getLogger(__name__)

def format_docs(docs):
    logger.info("formatting %d documents for the prompt", len(docs))
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(retriever):
    logger.info("building rag chain")

    prompt = ChatPromptTemplate.from_template("""
    Answer the question using only the given context. If the answer is not in the context or there isn't a strong correlation in context and
    question then say you don't know.
    
    CONTEXT: {context}
    
    QUESTION: {question}
    """)

    model = get_chat_model()

    chain = (                                     #Build the RAG pipeline using LangChain Expression Language (LCEL)
        {
            "context": retriever|RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        |prompt                #Insert the context and question into the prompt
        |model                 #Send the formatted prompt to the model
        |StrOutputParser()     #Convert the model response into a plain python string
    )

    logger.info("rag chain created successfully")
    return chain