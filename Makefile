default :
	node_modules/.bin/webpack

watch :
	node_modules/.bin/webpack --watch

clean :
	rm -rf static/*

shell :
	python manage.py shell_plus --ipython

server :
	python manage.py runserver

