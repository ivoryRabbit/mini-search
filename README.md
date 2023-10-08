# mini-search
mini search system based on pgvector and BERT

## Environments
- Python 3.9.4
- Docker

---
## Run
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
- [x] implement batch which loads embedding vectors to db
- [x] implement pgvector orm
- [x] implement search api
- [x] implement UI
- [x] execute app on docker container
- [ ] split out bootstrap scripts of server application 