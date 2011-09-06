.SILENT: clean release test
.PHONY: clean release test

PYTHON=/usr/bin/python

all: clean test release

debian:
	apt-get -yq update
	apt-get -yq dist-upgrade
	apt-get -yq install build-essential python python-dev \
		python-setuptools python-virtualenv mercurial

env:
	virtualenv -q --python=$(PYTHON) --no-site-packages env
	env/bin/easy_install coverage mocker \
		nose pytest pytest-pep8 pytest-cov wsgiref

clean:
	find src/ -name '*.py[co]' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info

release:
	env/bin/python setup.py -q bdist_egg sdist

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

# In order to run demos ensure:
# 1. make env
# 2. env/bin/python setup.py develop

test-demos:
	env/bin/py.test -q -x --pep8 demos/

run-hello:
	env/bin/python demos/hello/helloworld.py

run-time:
	env/bin/python demos/time/app.py
