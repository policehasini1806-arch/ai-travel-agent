"""
RAG chatbot for uploaded travel documents.
Uses HuggingFace embeddings (free, local) + Groq LLM + FAISS vector store.
"""
import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


QA_PROMPT = PromptTemplate(
    template="""You are a helpful travel assistant. Use the context from uploaded
travel documents to answer the question. If the answer isn't in the context, say so.

Context:
{context}

Question: {question}

Answer:""",
    input_variables=["context", "question"],
)


def _format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)


class RAGChatbot:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.chain = None
        # Load embeddings once at startup (runs locally, no API key needed)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def load_documents(self, file_paths: List[str]) -> None:
        if not self.groq_api_key:
            raise EnvironmentError("GROQ_API_KEY not set in .env")

        docs = []
        for path in file_paths:
            try:
                if path.endswith(".pdf"):
                    loader = PyPDFLoader(path)
                elif path.endswith(".txt"):
                    loader = TextLoader(path)
                else:
                    continue
                docs.extend(loader.load())
            except Exception as e:
                print(f"Could not load {path}: {e}")

        if not docs:
            raise ValueError("No documents could be loaded.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.groq_api_key,
            temperature=0,
        )

        self.chain = (
            {"context": retriever | _format_docs, "question": RunnablePassthrough()}
            | QA_PROMPT
            | llm
            | StrOutputParser()
        )

    def query(self, question: str) -> str:
        if self.chain is None:
            return "⚠️ No documents indexed yet. Please upload documents in the sidebar first."
        try:
            return self.chain.invoke(question)
        except Exception as e:
            return f"RAG error: {e}"