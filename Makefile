django-static:
	cd djangoapp && ./manage.py collectstatic

django-migrations:
	cd djangoapp && ./manage.py makemigrations

django-migrate:
	cd djangoapp && ./manage.py migrate

scrapy-run:
	cd scrapping && scrapy crawl CovidSearchDoctorEvidence -a limit=2 && scrapy crawl WhoInt
django-run:
	cd djangoapp && ./manage.py runserver
