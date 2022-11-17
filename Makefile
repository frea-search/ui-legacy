build:
	docker build --tag nexryai/frea-ui:devel --file Dockerfile .

run:
	docker build --tag nexryai/frea-ui:devel --file Dockerfile .
	docker-compose up
	
release:
	docker build --tag nexryai/frea-ui:latest --file Dockerfile .
	docker push nexryai/frea:latest
	
upload-devel:
	docker build --tag nexryai/frea-ui:devel --file Dockerfile .
	docker push nexryai/frea:devel
