from langchain_openai import ChatOpenAI
from pydantic import SecretStr

llm = ChatOpenAI(base_url="http://localhost:9931/v1", api_key=SecretStr("none"), max_completion_tokens=4096, temperature=0.7,top_p=0.7)