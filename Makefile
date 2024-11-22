

cwd = ${shell pwd}

build:
	-rm -rf build
	-rm -rf dist
	python3 -m build

test_upload:
	python3 -m twine upload -u __token__ --repository testpypi dist/*

upload:
	python3 -m twine upload -u __token__ --repository pypi dist/*
