FROM python:3.6.8
COPY ./ /
WORKDIR /
RUN pip install -r requirments.txt

EXPOSE 5000
CMD ["python", "./app/app.py"]
