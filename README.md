# mini-search
mini search system based on pgvector and BERT

## Environments
- Python 3.9.4
- Docker

---
## Run
### Local
```shell
# launch FastAPI application server
pip3 install -r backend/requirements.txt \
  && cd backend/src \
  && uvicorn main:app --port 8080 --reload
```
```shell
# launch Streamlit application server
pip3 install -r frontend/requirements.txt \
  && cd frontend/src \
  && streamlit run main.py --server.port 8501
```

### Docker container
```shell
docker-compose up --build
```
---
## URL
### UI
- [http://localhost:8501](http://localhost:8501)

### Docs
- [http://localhost:8080/docs](http://localhost:8080/docs)

---
## TODO
- [ ] implement batch which loads embedding vectors to db
- [ ] implement pgvector orm
- [ ] implement search api
- [ ] implement UI
- [ ] execute app on docker container
- [ ] porting web application using streamlit 