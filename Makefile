

cwd = ${shell pwd}

build:
	python3 -m build

test_upload:
	python3 -m twine upload -u __token__ --repository testpypi dist/*

upload:
	python3 -m twine upload -u __token__ --repository pypi dist/*
