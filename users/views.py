from django.shortcuts import render

from django.utils.translation import gettext as _

# Create your views here.
def login(request):
    return render(request, "login_page.html")