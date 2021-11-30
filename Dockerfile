FROM python:3.9.0

WORKDIR /home/

RUN echo "a-5"

RUN git clone https://github.com/go-tech01/Ccompany.git

WORKDIR /home/Ccompany/

RUN echo "SECRET_KEY=django-insecure-e^bjt0z)t$f%viq&a*dk9wdiddk4obubjese=5j_spjs8d(u#6" > .env

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN python manage.py migrate

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn","Ccompany.wsgi","--bind","0.0.0.0:8000"]