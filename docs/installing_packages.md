## Installasjonsinstrukser

Vi bruker `pipenv` for å holde styr på hvilke Python-pakker vi trenger. For å lære hvordan du skaffer deg dette kan du se [dokumentasjonen](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) eller spørre om hjelp på Slack-kanalen `#techsupport`.

Etter at du har installert `pipenv` skaffer du deg Django på denne måten: Åpne terminalen din (Terminal/iTerm/Git Bash/det du foretrekker) og pass på at du er i korrekt mappe:

```bash
$ pwd
/dine-mapper/sit-web
```

Deretter installerer du pakkene du trenger ganske enkelt:

```shell
$ pipenv install
Installing dependencies from Pipfile.lock (a6086c)…
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

Dette oppretter et virtuelt Python-miljø på maskinen din som sørger for at Django ikke krangler med noen andre pakker du har installert fra før. Du må aktivere dette miljøet før du kan kjøre prosjektet:

```shell
$ pipenv shell
Launching subshell in virtual environment…
```

Deretter kan du starte Django sin utviklingsserver og se prosjektet i sin nåværende tilstand:

```shell
$ python sit/manage.py runserver
Django version 3.0.8, using settings 'sit.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Du kan se siden i sin nåværende form ved å navigere til http://127.0.0.1:8000/ eller [localhost:8000](http://127.0.0.1:8000/).