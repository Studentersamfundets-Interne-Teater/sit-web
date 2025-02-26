import pytest
import datetime as dt
from ..views import get_ar, get_blesteliste

from SITdata import models


@pytest.mark.django_db()
def test_that_year_is_created_if_it_does_not_exist() -> None:
    found_year = models.Ar.objects.filter(pk=2025).first()
    assert found_year is None
    ar = get_ar(2025)
    assert ar is not None
    found_year_again = models.Ar.objects.get(pk=2025)
    assert found_year_again is not None


@pytest.mark.django_db()
def test_that_get_blesteliste_gets_relevant_productions():
    today = dt.date(2025, 2, 1)  # 1 february 2025
    now = dt.datetime(2025, 2, 1, 12, 0)

    # Create some productions that we expect to find
    first_to_find = models.Produksjon(
        tittel="Snart premiere!",
        premieredato=today + dt.timedelta(days=2),
        blestestart=today - dt.timedelta(days=1),
    )
    first_to_find.save()

    second_to_find = models.Produksjon(
        tittel="Har hatt premiere, men har fremdeles forestillinger igjen",
        premieredato =today - dt.timedelta(days=2),
        blestestart=today - dt.timedelta(days=7)
    )
    second_to_find.save()
    models.Forestilling(
        produksjon=second_to_find,
        tidspunkt=now + dt.timedelta(days=1)
    ).save()

    # Also create some productions which should be ignored
    models.Produksjon(
        tittel="Har hatt blæstestart, men var kun én preimere og er nå ferdigspilt.",
        premieredato=today - dt.timedelta(days=1),
        blestestart=today - dt.timedelta(days=2),
    ).save()

    production_to_ignore = models.Produksjon(
        tittel="Denne er også ferdigspilt, men hadde flere forestillinger",
        premieredato=today - dt.timedelta(days=2),
        blestestart=today - dt.timedelta(days=3),
    )
    production_to_ignore.save()
    models.Forestilling(
        produksjon=production_to_ignore,
        tidspunkt=now - dt.timedelta(days=1)
    ).save()

    models.Produksjon(
        tittel="Har blæstestart i fremtiden",
        premieredato=today + dt.timedelta(days=10),
        blestestart=today + dt.timedelta(days=7)
    )

    found_productions = get_blesteliste(today)

    # Compare titles of actually found productions to names of productions we expect to find
    assert set(p.tittel for p in found_productions) == set(
       [ first_to_find.tittel, second_to_find.tittel]
    )
