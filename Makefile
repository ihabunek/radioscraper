default : 
	node_modules/.bin/webpack

watch :
	node_modules/.bin/webpack --watch

clean :
	rm -rf static/*

