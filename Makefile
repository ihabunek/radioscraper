clean :
	rm -rf static/*

shell :
	python manage.py shell_plus

server :
	python manage.py runserver

test :
	pytest -s

css:
	sassc ui/styles/app.scss ui/dist/styles.css

css-watch: css
	@while true; do \
		inotifywait -qre close_write ui/styles; make css; \
	done
