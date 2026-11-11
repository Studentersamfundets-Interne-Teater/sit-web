from django.urls import reverse
import pytest
import datetime as dt
from ..views import get_ar, get_blesteliste, get_infotekst

from SITdata import models

from django.test import Client


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
        premieredato=today - dt.timedelta(days=2),
        blestestart=today - dt.timedelta(days=7),
    )
    second_to_find.save()
    models.Forestilling(
        produksjon=second_to_find, tidspunkt=now + dt.timedelta(days=1)
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
        produksjon=production_to_ignore, tidspunkt=now - dt.timedelta(days=1)
    ).save()

    models.Produksjon(
        tittel="Har blæstestart i fremtiden",
        premieredato=today + dt.timedelta(days=10),
        blestestart=today + dt.timedelta(days=7),
    )

    found_productions = get_blesteliste(today)

    # Compare titles of actually found productions to names of productions we expect to find
    assert [p.tittel for p in found_productions] == [
        second_to_find.tittel,
        first_to_find.tittel,
    ]


@pytest.mark.django_db()
def test_that_get_infotekst_returns_empty_string_when_no_appropriate_title_is_found() -> None:
    found = get_infotekst()
    assert found == ""


@pytest.mark.django_db()
def test_that_appropriate_infotekst_is_found() -> None:
    models.Uttrykk(tittel="Studentersamfundets Interne Teater", beskrivelse="For en flott gjeng!").save()
    found = get_infotekst()
    assert found == "For en flott gjeng!"


@pytest.mark.django_db()
def test_that_searching_for_a_single_name_finds_the_appropriate_members(client: Client) -> None:
    last_year = dt.date.today().year - 1

    member_to_find = models.Medlem(fornavn="Live", etternavn="Jacobsen", opptaksar=last_year, status=1, undergjeng=1)
    member_to_find.save()
    member_to_ignore = models.Medlem(fornavn="Erik", etternavn="Jakobsen", opptaksar=last_year, status=1, undergjeng=2)
    member_to_ignore.save()

    response = client.get(reverse("medlemmer"), query_params={"navn": "jaCoBSEn"})
    assert response.status_code == 200

    returned_members = response.context["medlemsliste"]
    assert member_to_find in returned_members
    assert member_to_ignore not in returned_members


@pytest.mark.django_db()
def test_that_searching_for_full_name_finds_the_appropriate_member(client: Client) -> None:
    last_year = dt.date.today().year - 1

    member_to_ignore = models.Medlem(fornavn="Live", etternavn="Jacobsen", opptaksar=last_year, status=1, undergjeng=1)
    member_to_ignore.save()
    member_to_find = models.Medlem(fornavn="Erik", mellomnavn="André", etternavn="Jakobsen", opptaksar=last_year, status=1, undergjeng=2)
    member_to_find.save()

    response = client.get(reverse("medlemmer"), query_params={"navn": "eRik ANDRé JaKObsen"})
    assert response.status_code == 200

    returned_members = response.context["medlemsliste"]
    assert member_to_find in returned_members
    assert member_to_ignore not in returned_members

@pytest.mark.django_db()
def test_that_searching_for_full_name_does_not_find_people_sharing_one_of_the_names(
    client: Client,
) -> None:
    last_year = dt.date.today().year - 1

    member_to_ignore = models.Medlem(
        fornavn="Live",
        etternavn="Jakobsen",
        opptaksar=last_year,
        status=1,
        undergjeng=1,
    )
    member_to_ignore.save()
    member_to_find = models.Medlem(
        fornavn="Erik",
        mellomnavn="André",
        etternavn="Jakobsen",
        opptaksar=last_year,
        status=1,
        undergjeng=2,
    )
    member_to_find.save()

    response = client.get(
        reverse("medlemmer"),
        query_params={"navn": "eRik ANDRé JaKObsen"},
    )
    assert response.status_code == 200

    returned_members = response.context["medlemsliste"]
    assert member_to_find in returned_members
    assert member_to_ignore not in returned_members


@pytest.mark.django_db()
def test_admin_bulk_assign_verv_creates_erfaring_for_all_selected_members(client: Client) -> None:
    User = __import__("django.contrib.auth.models", fromlist=["User"]).User
    admin_user = User.objects.create_superuser("admin", "admin@example.com", "secret123")
    client.force_login(admin_user)

    member_one = models.Medlem(fornavn="Anna", etternavn="Andersen", opptaksar=2024, status=1, undergjeng=1)
    member_two = models.Medlem(fornavn="Bjørn", etternavn="Berg", opptaksar=2024, status=1, undergjeng=2)
    member_one.save()
    member_two.save()

    role = models.Verv.objects.create(tittel="Kulissebygger", vervtype=3, erfaringsoverforing=True)
    url = reverse("admin:SITdata_erfaring_assign_verv")

    response = client.post(
        url,
        {
            "member_ids": [str(member_one.pk), str(member_two.pk)],
            "verv": str(role.pk),
            "ar": "2025",
            "member_roles": ["Kulissebygger", "Kulissebygger"],
        },
        follow=True,
    )

    assert response.status_code == 200
    assert models.Erfaring.objects.filter(medlem=member_one, verv=role, ar=2025).count() == 1
    assert models.Erfaring.objects.filter(medlem=member_two, verv=role, ar=2025).count() == 1


@pytest.mark.django_db()
def test_experience_bulk_page_searches_and_assigns_members(client: Client) -> None:
    User = __import__("django.contrib.auth.models", fromlist=["User"]).User
    admin_user = User.objects.create_superuser("admin", "admin@example.com", "secret123")
    client.force_login(admin_user)

    member_one = models.Medlem(fornavn="Ada", etternavn="Andersen", opptaksar=2024, status=1, undergjeng=1)
    member_two = models.Medlem(fornavn="Bjørn", etternavn="Berg", opptaksar=2024, status=1, undergjeng=2)
    member_one.save()
    member_two.save()
    role = models.Verv.objects.create(tittel="Kulissebygger", vervtype=3, erfaringsoverforing=True)

    url = reverse("admin:SITdata_erfaring_assign_verv")
    search_response = client.get(url, {"member_search": "Ada Andersen"})

    assert search_response.status_code == 200
    assert str(member_one) in search_response.content.decode()
    assert str(member_two) not in search_response.content.decode()

    response = client.post(
        url,
        {
            "member_ids": [str(member_one.pk), str(member_two.pk)],
            "verv": str(role.pk),
            "ar": "2029",
            "member_roles": ["Bygger", "Bas"],
        },
        follow=True,
    )

    assert response.status_code == 200
    assert models.Erfaring.objects.filter(medlem=member_one, verv=role, ar=2029, rolle="Bygger").count() == 1
    assert models.Erfaring.objects.filter(medlem=member_two, verv=role, ar=2029, rolle="Bas").count() == 1
