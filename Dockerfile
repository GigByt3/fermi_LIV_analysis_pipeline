FROM python:3.12.3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app

ADD . ./app/data
ADD . ./app/data/n0
ADD . ./app/data/n1
ADD . ./app/data/n2
ADD . ./app/data/n3
ADD . ./app/data/n4
ADD . ./app/data/n5
ADD . ./app/data/n6
ADD . ./app/data/n7
ADD . ./app/data/n8
ADD . ./app/data/n9

WORKDIR /app

CMD ["python", "sextant.py"]
