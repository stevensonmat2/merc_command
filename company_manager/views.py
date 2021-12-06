from django.shortcuts import render


def create_mech(request):
    return render(request, "mechs/add_mech.html")
