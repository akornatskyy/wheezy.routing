.SILENT: clean release test
.PHONY: clean release test

all: clean test release

env:
	virtualenv --no-site-packages env
	env/bin/easy_install nose coverage mocker

clean:
	find src/ -name '*.py[co]' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info

release:
	python setup.py -q bdist_egg sdist

test:
	env/bin/nosetests --where=src/wheezy/routing --match=^test --with-doctest\
		--detailed-errors --with-coverage --cover-package=wheezy.routing
