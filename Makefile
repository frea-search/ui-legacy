build:
	docker build --tag nexryai/frea:latest --file Dockerfile .

run:
	docker build --tag nexryai/frea:latest --file Dockerfile .
	docker-compose up
	
upload:
	docker build --tag nexryai/frea:latest --file Dockerfile .
	docker push nexryai/frea:latest
