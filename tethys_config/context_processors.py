"""
********************************************************************************
* Name: context_processors.py
* Author: Nathan Swain
* Created On: 2014
* Copyright: (c) Brigham Young University 2014
* License: BSD 2-Clause
********************************************************************************
"""
import datetime as dt


def tethys_global_settings_context(request):
    """
    Add the current Tethys app metadata to the template context.
    """
    from .models import Setting
    from termsandconditions.models import TermsAndConditions

    # Get settings
    site_globals = Setting.as_dict()

    # Get terms and conditions
    site_globals.update({'documents': TermsAndConditions.get_active_terms_list()})

    context = {
        'site_globals': site_globals,
        'site_defaults': {
            'copyright': f'Copyright © {dt.datetime.utcnow():%Y} Your Organization',
        }
    }

    return context
