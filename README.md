Run local:    
   ```bash
   docker-compose up --build
   ``` 

Run tests:
   ```bash
   docker-compose -f docker-compose-test.yml up --build 
   docker-compose -f docker-compose-test.yml run app-test pytest -s -v
   ```

### Web
http://localhost:8000/

### Swagger
http://localhost:8000/docs#/

### Миграции
   ```bash
   docker-compose exec app sh   
   alembic init -t async migrations # инит
   alembic revision  --autogenerate -m "Add model" # create migrate
   alembic upgrade head # apply
   alembic downgrade 8ac14e223d1  # down
   alembic downgrade base  # This command will undo all migrations
   ```
