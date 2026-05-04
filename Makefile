PYTHON = python
PIP = pip

.PHONY: install run_pipeline run

install:
	$(PIP) install -r requirements.txt

run_pipeline:
	$(PYTHON) -m scripts.run_pipeline

run:
	streamlit run main.py