.SILENT: clean env release test
.PHONY: clean env release test

VERSION=2.6
PYTHON=env/bin/python$(VERSION)
EASY_INSTALL=env/bin/easy_install-$(VERSION)
PYTEST=env/bin/py.test-$(VERSION)
NOSE=env/bin/nosetest-$(VERSION)

all: clean test release

debian:
	apt-get -yq update
	apt-get -yq dist-upgrade
	# How to Compile Python from Source
	# http://mindref.blogspot.com/2011/09/compile-python-from-source.html
	apt-get -yq install libbz2-dev build-essential python \
		python-dev python-setuptools python-virtualenv \
		mercurial

env:
	PYTHON_EXE=/usr/local/bin/python$(VERSION); \
	if [ ! -x $$PYTHON_EXE ]; then \
		PYTHON_EXE=/usr/bin/python$(VERSION); \
	fi;\
	virtualenv --python=$$PYTHON_EXE \
		--no-site-packages env
	$(EASY_INSTALL) coverage mocker \
		nose pytest pytest-pep8 pytest-cov wsgiref

clean:
	find src/ -name '*.py[co]' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info

release:
	$(PYTHON) setup.py -q bdist_egg

test:
	$(PYTEST) -q -x --pep8 --doctest-modules \
		src/wheezy/routing

doctest-cover:
	$(NOSE) --where=src/wheezy/routing --match=^test \
		--with-doctest --detailed-errors --with-coverage \
		--cover-package=wheezy.routing

test-cover:
	$(PYTEST) -q --cov wheezy.routing \
		--cov-report term-missing \
		src/wheezy/routing/tests

test-demos:
	$(PYTEST) -q -x --pep8 demos/

run-hello:
	$(PYTHON) demos/hello/helloworld.py

run-time:
	$(PYTHON) demos/time/app.py
