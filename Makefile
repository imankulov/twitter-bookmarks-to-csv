web:
	FLASK_APP=twitter_bookmarks_to_csv.app:app FLASK_ENV=development poetry run flask run

requirements: requirements.txt requirements_dev.txt

requirements.txt: poetry.lock
	poetry export -o requirements.txt -f requirements.txt

requirements_dev.txt: poetry.lock
	poetry export --dev -o requirements_dev.txt -f requirements.txt

.PHONY: requirements
