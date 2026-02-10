run:
	uvicorn app.main:app --reload

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

docbuild:
	docker build -t appfa .

docrun:
	docker run -it --name cont_name appfa

docinf:
	docker ps -a

docimages:
	docker images
	docker run -it --rm appfa /bin/sh - можно посмотреть содержимое контейнера

