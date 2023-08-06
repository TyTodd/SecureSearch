# SecureSearch

## Download Model
[ggml-gpt4all-j-v1.3-groovy.bin](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin)

## Inititialize Vector Store Database
The database used is [Clickhouse](https://clickhouse.com/). To run it first set up the local server with docker
```
docker run -d -p 8123:8123 -p9000:9000 --name langchain-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server:23.4.2.11
```
Next install the client driver
```
pip install clickhouse-connect
```
