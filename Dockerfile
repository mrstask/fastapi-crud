FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8021
CMD python app.py