run:
	uvicorn app.main:app --reload

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

docbuild:
	docker build -t appfastapi .

docrun:
	docker run -it --name cont_name appfastapi

docinf:
	docker ps -a

docimages:
	docker images
	docker run -it --rm appfa /bin/sh - можно посмотреть содержимое контейнера


runn:
	uvicorn new_app.main:app --reload
