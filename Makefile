clean: clean-test clean-envs clean-pyc

setup:
	pip install --upgrade pip
	pip install -r requirements.txt

test: clean
	python -m pytest -v -s

isort:
	isort oam

lint: clean
	flake8 --max-line-length=120 --ignore=E402 oam

clean-test:
	rm -rf .tox .coverage htmlcov coverage-reports tests.xml tests.html
	rm -rf .converage.*
	rm -rf .pytest_cache

clean-envs:
	rm -rf env

clean-pyc:
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf *.~
	rm -rf oam/*__pycache__*
