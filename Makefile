clean:
	rm -rf build build.zip
	rm -rf __pycache__

build-lambda-package: clean
	mkdir build
	if [ ! -d bin ]; then mkdir bin; fi
	if [ ! -d lib ]; then mkdir lib; fi
	cp -r src build/.	
	cp -r src lib/.
	cp -r src bin/.
	find build/src | grep -E "(__pycache__|\.pyc|\.pyo$|\.log)" | xargs rm -rf
	pip3 install -r requirements.txt -t build/lib/.
	cd build; zip -9r ../build.zip .
	rm -rf build

update-lambda-package:
	mkdir build
	cp -r src build/.
	find build/src | grep -E "(__pycache__|\.pyc|\.pyo$|\.log)" | xargs rm -rf
	cd build; zip -ur ../build.zip src
	rm -rf build