from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

embeddings = OpenAIEmbeddings(
  model="hehe",
  base_url="http://localhost:9932/v1",
  check_embedding_ctx_length=False,
  api_key=SecretStr("none")
)