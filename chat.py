from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Clickhouse, ClickhouseSettings
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
import os
import time
from dotenv import load_dotenv

load_dotenv()
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

settings = ClickhouseSettings(table="vector_table", index_type= "minmax") #vector_table #clickhouse_vector_search_example
db = Clickhouse(embeddings, config=settings)

retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
callbacks = [StreamingStdOutCallbackHandler()] #[] if args.mute_stream else [StreamingStdOutCallbackHandler()]

llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gptj', n_batch=model_n_batch, callbacks=callbacks, verbose=False)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= True) #not args.hide_source)



while True:
    query = input("Prompt>")

    # query = "What did the president say about Ketanji Brown Jackson"
    print("Starting Query...")
    start = time.time()
    print("Models Response: ")
    res = qa(query)
    print("\nQuery completed in: ", str(time.time() - start) + "s")
    answer, docs = res['result'], res['source_documents'] #[] if args.hide_source else res['source_documents']
    # docs = db.similarity_search(query)
    print()
    print("Sources:")
    for document in docs:
        # print("\n> " + document.metadata["source"] + ":")
        print(document.page_content)
    print()

    # for doc in docs:
    #     print("Doc\n")
    #     print(doc.page_content)