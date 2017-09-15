# URL Shortener Microservice #

-----


## Install
In the terminal
```

$ cd urlshortner_microservice
$ pip install -r requriements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

```

## User stories:
1. I can pass a URL as a parameter and I will receive a shortened URL in the JSON response.
2. If I pass an invalid URL that doesn't follow the valid http://www.example.com format, the JSON response will contain an error instead.
3. When I visit that shortened URL, it will redirect me to my original link.


## Example usage:
http://localhost:8000/api/new/http://www.gmail.com
http://localhost:8000/api/new/http://www.yahoo.com/news

## Example output
```
{"original_url": "http://gmail.com/", "short_url": "http://localhost:8000/api/cXede3"}
```

## Usage:
http://localhost:8000/api/cXede3

## Will redirect to:
http://gmail.com/