.SILENT: clean release test
.PHONY: clean release test

PYTHON=/usr/bin/python

all: clean test release

env:
	virtualenv -q --python=$(PYTHON) --no-site-packages \
		--relocatable env
	env/bin/easy_install coverage mocker \
		nose pytest pytest-pep8 pytest-cov

clean:
	find src/ -name '*.py[co]' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info

release:
	python setup.py -q bdist_egg sdist

test:
	env/bin/py.test -q -x --pep8 --doctest-modules \
		src/wheezy/routing

doctest-cover:
	env/bin/nosetests --where=src/wheezy/routing --match=^test \
		--with-doctest --detailed-errors --with-coverage \
		--cover-package=wheezy.routing

test-cover:
	env/bin/py.test -q --cov wheezy.routing \
		--cov-report term-missing \
		src/wheezy/routing/tests
