default :
	node_modules/.bin/webpack

watch :
	node_modules/.bin/webpack --watch

clean :
	rm -rf static/*

shell :
	python manage.py shell_plus

server :
	python manage.py runserver

test :
	pytest -s
