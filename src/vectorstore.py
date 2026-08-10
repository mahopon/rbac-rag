import os
from pathlib import Path
from typing import Optional, cast

from langchain_community.vectorstores import FAISS
from src.embed import embeddings
from langchain_core.documents import Document
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore

FAISS_INDEX_PATH: str = str(Path(__file__).parent / "faiss_index")

vectorstore: Optional[FAISS] = None


def cold_start_faiss() -> None:
  global vectorstore
  if os.path.isdir(FAISS_INDEX_PATH):
      vectorstore = FAISS.load_local(
          folder_path=FAISS_INDEX_PATH,
          embeddings=embeddings,
          allow_dangerous_deserialization=True,
      )
  else:
        dim = len(embeddings.embed_query(""))
        vectorstore = FAISS(
            embedding_function=embeddings,
            index=faiss.IndexFlatL2(dim),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        vectorstore.save_local(FAISS_INDEX_PATH)


def get_vectorstore() -> Optional[FAISS]:
  return vectorstore


def add_documents_to_faiss(docs: list[Document]) -> FAISS:
  if len(docs) == 0:
    raise RuntimeError("FAISS db not started")
  global vectorstore
  if vectorstore is not None:
    vectorstore.add_documents(docs)
    vectorstore.save_local(FAISS_INDEX_PATH)
  else:
    raise RuntimeError("FAISS db not started")
  return vectorstore


def inspect_faiss() -> dict:
    cold_start_faiss()
    vs = get_vectorstore()
    info = {
        "num_vectors": vs.index.ntotal,
        "index_dimension": vs.index.d,
    }
    doc_count = len(vs.docstore._dict)
    info["num_documents"] = doc_count
    if doc_count > 0:
        sample_ids = list(vs.docstore._dict.keys())[:5]
        samples = {}
        for doc_id in sample_ids:
            doc = vs.docstore._dict[doc_id]
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            metadata_preview = {k: v for k, v in doc.metadata.items()}
            samples[str(doc_id)] = {
                "content": content_preview,
                "metadata": metadata_preview,
            }
        info["sample_documents"] = samples
    return info


def create_vectorstore(docs: list[Document]) -> FAISS:
  return FAISS.from_documents(docs, embeddings)

