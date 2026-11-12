from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

"""
A Document is page_content (the text) plus metadata (such as the source path).
add_start_index=True records where each chunk began. We’ll use it for citations and for chunk IDs in Module 3.
encoding="utf-8" avoids Windows encoding errors.
"""
def load_documents(folder, glob: str = "**/*.md") -> list[Document]:
    loader = DirectoryLoader(
        str(folder), glob=glob, loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def split_documents(docs, chunk_size: int = 500, chunk_overlap: int = 80):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True,
    )
    return splitter.split_documents(docs)