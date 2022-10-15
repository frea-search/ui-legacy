build:
	docker build --tag nexryai/frea:devel --file Dockerfile .

run:
	docker build --tag nexryai/frea:devel --file Dockerfile .
	docker-compose up
	
release:
	docker build --tag nexryai/frea:latest --file Dockerfile .
	docker push nexryai/frea:latest
	
upload-devel:
	docker build --tag nexryai/frea:devel --file Dockerfile .
	docker push nexryai/frea:devel
