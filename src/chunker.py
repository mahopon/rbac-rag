from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


splitter = RecursiveCharacterTextSplitter(
  chunk_size=1000, chunk_overlap=100
)

def chunk_document(pages: list[str]) -> list[Document]:
  docs = [Document(page_content=text, metadata={"page": i + 1}) for i, text in enumerate(pages)]
  chunks = splitter.split_documents(docs)
  return chunks