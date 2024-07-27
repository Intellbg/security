from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models import Household


@login_required
def household_table(request):
    return render(request, "administrator/houses/table.html")


def getHouseContext(request):
    house_id = request.GET.get("house_id", None)
    house = Household.objects.get(id=house_id)
    address = house.address
    context = {"address": address, "house_id": house_id}
    return context


@login_required
def create_household_person(request):
    context = getHouseContext(request)
    return render(request, "administrator/household_persons/form.html", context)


@login_required
def household_details(request):
    context = getHouseContext(request)
    return render(request, "administrator/household_details/details.html", context)


@login_required
def household_tags_table(request):
    return render(request, "administrator/household_tags/tags_table.html")


@login_required
def household_persons_table(request):
    return render(request, "administrator/persons/table.html")


@login_required
def pending_authorizations(request):
    return render(request, "administrator/user_sites/table.html")


@login_required
def operations_table(request):
    return render(request, "administrator/operations/table.html")
