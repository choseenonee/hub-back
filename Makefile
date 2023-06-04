all: create-image compose

clean:
	docker-compose rm
	docker rmi hubapi

stop-api:
	docker stop hub-hubapi-1

create-image:
	docker build -t hubapi .

compose:
	docker-compose up

