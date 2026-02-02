FROM python:3.12.3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app

ADD . ./app/data
ADD . ./app/GBM_files
ADD . ./app/LAT_files

WORKDIR /app

CMD ["python", "sextant.py"]
