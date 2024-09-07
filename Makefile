.PHONY: env
env:
	conda create -n neuroslide python==3.11.*

.PHONY: start_service
start_service:
	uvicorn main:app --host 127.0.0.1 --port 8000

.PHONY: install
install:
	pip install -r requirements.txt
