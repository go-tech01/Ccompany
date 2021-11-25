from .base import *

env_list = dict()

local_env =open(os.path.join(BASE_DIR, '.env'), encoding='utf-8')        # 운영체제 상 경로(path) / join 합쳐준다 BASE_DIR, '.env'

while True:
    line = local_env.readline()     ##한줄씩 읽다가 없으면 나온다 break
    if not line:
        break
    line = line.replace('\n', '')
    start = line.find('=')             ## SECRET_KEY=django-insecu = 로 좌 -key / 우 -value
    key = line[:start]
    value = line[start+1:]
    env_list[key] = value              ## key, value 나눈걸 딕셔러리에 추가


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = env_list['SECRET_KEY']                ##env_list 딕셔러리 만들어야한다

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]      #"*" 모두 허용한다


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'password1234',   # 더미 비번
        'HOST': 'mariadb',            # 컨테이너 이름
        'PORT': '3306',               # db 포트
    }
}