PYTHON = python
PIP = pip

.PHONY: install run_pipeline

install:
	$(PIP) install -r requirements.txt

run_pipeline:
	$(PYTHON) -m scripts.run_pipeline