# olo

Basic commands

```sh
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
python manage.py collectstatic
```

Create fresh secret key

```sh
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
