dev:
	uvicorn main:app --host 0.0.0.0 --reload

prod:
	uvicorn main:app --host 0.0.0.0
