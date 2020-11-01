# TODO
- [x] DB
- [x] models
- [x] json
- [x] k:v
- [x] docker: chrome
- [x] docker: createsu
- [x] docker: start qcluster
- [ ] django env
- [ ] logging

# DOCKER DEPLOY
```
cd x_1

sudo docker-compose up

docker exec -ti CID___ bash

# create su django/django
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('dj', '', 'dj')" | pipenv run python manage.py shell

# run task
pipenv run python manage.py qcluster

# then open http://127.0.0.1:8000/
```


---
