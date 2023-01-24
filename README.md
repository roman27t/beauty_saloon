Run local:    
   ```bash
   docker-compose up --build
   ``` 

Run tests:
   ```bash
   docker-compose -f docker-compose-test.yml up --build 
   docker-compose -f docker-compose-test.yml run app-test pytest -s -v
   ```

### Swagger
http://localhost:8000/docs#/

### Web
http://localhost:8000/

### admin
http://localhost:8000/admin/


### Migrations
   ```bash
   docker-compose exec app sh   
   alembic init -t async migrations # init
   alembic revision  --autogenerate -m "X_Add model" # create migrate
   alembic upgrade head # apply
   alembic downgrade 8ac14e223d1  # down
   alembic downgrade base  # This command will undo all migrations
   ```

### Project - Entities
* Employee - salon staff
* Client - users of salon
* Category - salon services are divided into categories
* Service_name - beauty salon services
* Offer - Each salon employee must complete the services that he can provide
* Order - The client can reserve a specific offer for a specific time

### API
* each entity has a simple API
* there are API with a full set of information
  * /offer/full/{ifilter}/{pk}/
  * /order/full/{ifilter}/{pk}/?page=1
* service API, for the initial filling of the database: /init-stub/
* Statistic API: /order/stats/{ifilter}/

### Client workflow
1. Choose category: GET /category/
2. Choose choice of specific service: GET /service/
3. Getting a list of employees for a service: GET /offer/full/service_name/1/
4. Booking of specific service: POST /offer/
5. Payment/Cancel of specific order: POST /order/payment/{pk}/ or DELETE /order/id/
6. Viewing Your Reservations /order/full/client/1/?page=1

### Employee workflow
1. Add your offer of specific service: POST /offer/
2. Getting a list of offers: GET /offer/full/employee/1/
3. Block non-working hours: POST /offer/
4. Cancel of specific order: DELETE /order/id/
5. Viewing Your Reservations /order/full/employee/1/?page=1


#### best practice FATAPI
https://github.com/zhanymkanov/fastapi-best-practices
