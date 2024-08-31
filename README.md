> sudo chown -R $USER:$USER ./data/postgres
> sudo chmod -R 700 ./data/postgres

> docker exec -it election_issues_postgres pg_isready -U ${POSTGRES_USER}