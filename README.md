# Velkommen!

Dette repoet inneholder kildekoden til [Studentersamfundets Interne Teaters hjemmsider](https://sit.samfundet.no).
Under følger en guide for hvordan du kan bidra til videre utvikling av siden.

Om du trenger hjelp til å installere pakkene du trenger, se [installasjonsinstruksene](/docs/installing_packages.md)

Om du har noen spørsmål, ikke nøl med å [sende oss en e-post](mailto:sit-web@samfundet.no), eller ta [kontakt på Slack](https://sitweb.slack.com).

## Hvordan bidra til siden

Om du ikke vet hvordan Git og Github fungerer anbefaler vi at du aller først bruker litt tid på å lære deg dette. En fin ressurs er [GitHubs egne guider](https://guides.github.com/).

Om du skal gjøre en ikke-triviell endring må du aller først klone repoet til din egen maskin.

```bash
$ git clone https://github.com/Studentersamfundets-Interne-Teater/sit-web.git
$ cd sit-web
```

Koden som ligger på `master` skal alltid være den som er i produksjon. Når en jobber med ny funksjonalitet eller fikser eksisterende feil skal dette arbeidet alltid foregå på egne branches. Om du f.eks. skal lage en ny header ville du ha laget en ny branch som følger:

```bash
# Bytt til master-branchen så du er sikker på at du tar utgangspunkt i rett kode
$ git checkout master
# Hent ned siste endringer fra master
$ git pull
# Lag ny branch og gå til den med en gang
$ git checkout -b new-header
Switched to a new branch 'new-header'
```

Deretter kan du starte med å gjennomføre endringen din.
Pass på å commite ofte, og skriv beskrivende commit-meldinger som beskriver endringen din på en måte som gjør at andre kan forstå hva du har endret. Commit-meldingene skal helst ikke være lenger enn 50 tegn, og skries i imperativ (kommanderende) form. Eksempler kan være
```bash
$ git commit -m "Change header logo to SVG format"
$ git commit -m "Reorder header items"
$ git commit -m "Fix overlapping icons in header in mobile layout"
```

Etter du har gjort alle endringene dine, dytt dem opp til GitHub:
```bash
$ git push -u origin new-header
```
Her må `new-header` erstattes med navnet du valgte til din branch. Flagget `-u` står for `upstream`, og sikrer at dersom du vil dytte flere endringer eller hente eventuelle andre endringer som noen andre gjør på din gren, så kan i fremtiden slippe unna med å skrive kun `git pull` eller `git push`.

Etter å ha skrevet denne kommandoen får du et svar med en link du kan trykke på for å åpne en pull request. For mer informasjon om hvordan dette foregår, se gjerne [GitHub sin egen dokumentasjon](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

Husk å skrive en kort tekst om hvilke endringer du har gjort, og hvorfor.

Etter at du har åpnet en Pull Request må den godkjennes av noen med skrivetilgang i repoet. De vil hente dine endringer ned til sin egen maskin, gå gjennom dem, og se at alt fungerer som det skal. Det kan også hende de vil be om små endringer. Når alt ser bra ut vil de godkjenne Pull Requesten, og du kan trykke på den grønne «Merge»-knappen.

Takk for interessen for siden vår!
