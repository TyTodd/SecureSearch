from langchain.document_loaders import TextLoader
import os
from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Clickhouse, ClickhouseSettings
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

loader = TextLoader("source_documents/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
# embeddings = GPT4AllEmbeddings()
#change
for d in docs:
    d.metadata = {"some": "metadata"}
settings = ClickhouseSettings(table="vector_table", index_type= "Annoy") #vector_table #clickhouse_vector_search_example
docsearch = Clickhouse.from_documents(docs, embeddings, config=settings)