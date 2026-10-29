run:
	uvicorn main:app --reload
test:
	python -m pytest

docker-build:
	docker build -t brushstorm-backend .

docker-run:
	docker run --rm -p 8000:8000 brushstorm-backend
