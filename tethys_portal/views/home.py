from django.shortcuts import render, redirect
from django.conf import settings


def home(request):
    # Some installations may wish to bypass the default home page
    # The BYPASS_TETHYS_HOME_PAGE setting in settings.py allows them to do so
    if hasattr(settings, 'BYPASS_TETHYS_HOME_PAGE') and settings.BYPASS_TETHYS_HOME_PAGE:
        return redirect('app_library')

    return render(request, 'tethys_portal/home.html', {})