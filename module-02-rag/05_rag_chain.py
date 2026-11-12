from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from common.documents import load_documents, split_documents
from common.llm import get_embeddings, get_llm
"""
The pipeline is: retrieve, then stuff the chunks into the prompt as {context}, then generate. The line ONLY the context is what stops the model answering from memory. Returning the sources lets anyone verify the answer.

Checkpoint, three things to confirm:

“What is RAG?” now gives Retrieval-Augmented Generation, not the gene.
The failure-modes answer matches the document.
The France question gets “I don’t know”. If the model answers “Paris”, it ignored your instruction, which is a real prompt-grounding failure worth writing up in your README
"""
KB = Path(__file__).parent / "sample_data" / "knowledge_base"
chunks = split_documents(load_documents(KB))
store = InMemoryVectorStore.from_documents(chunks, get_embeddings())
retriever = store.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Answer the question using ONLY the context below. If the context does not "
     "contain the answer, say \"I don't know based on the provided documents.\" "
     "Be concise.\n\nContext:\n{context}"),
    ("human", "{question}"),
])
answer_chain = prompt | get_llm() | StrOutputParser()

def format_docs(docs):
    return "\n\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs, 1))

def ask(question):
    docs = retriever.invoke(question)
    answer = answer_chain.invoke({"context": format_docs(docs), "question": question})
    print(f"\nQ: {question}\nA: {answer}\nSources:")
    for i, d in enumerate(docs, 1):
        print(f"  [{i}] {Path(d.metadata['source']).name} (char {d.metadata['start_index']})")

ask("What is RAG?")
ask("Name two failure modes of RAG.")
ask("What is the capital of France?")