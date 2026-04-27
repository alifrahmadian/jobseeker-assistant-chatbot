PYTHON = python
PIP = pip

.PHONY: install

install:
	$(PIP) install -r requirements.txt