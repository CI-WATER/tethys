"""
********************************************************************************
* Name: user.py
* Author: Nathan Swain
* Created On: 2014
* Copyright: (c) Brigham Young University 2014
* License: BSD 2-Clause
********************************************************************************
"""

from django.conf import settings as django_settings
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import never_cache

from tethys_apps.harvester import SingletonHarvester
from tethys_portal.forms import UserSettingsForm, UserPasswordChangeForm
from tethys_apps.models import TethysApp
from tethys_apps.base.paths import get_user_workspace, get_user_media
from tethys_apps.utilities import get_app_class
from tethys_apps.decorators import login_required
from tethys_quotas.handlers.workspace import WorkspaceQuotaHandler
from tethys_quotas.utilities import get_quota, _convert_storage_units
from tethys_config.models import get_custom_template

from tethys_portal.optional_dependencies import optional_import, has_module

# optional imports
has_mfa = optional_import("has_mfa", from_module="mfa.helpers")
Token = optional_import("Token", from_module="rest_framework.authtoken.models")


def get_user_context(request):
    """
    Create the context object used in both the profile and the settings views.
    """
    user = request.user
    user_token_key = None
    if has_module(Token):
        user_token, _ = Token.objects.get_or_create(user=user)
        user_token_key = user_token.key
    codename = "user_workspace_quota"
    rqh = WorkspaceQuotaHandler(user)
    current_use = _convert_storage_units(rqh.units, rqh.get_current_use())
    quota = get_quota(user, codename)
    quota = _check_quota_helper(quota)
    user_has_mfa = mfa_is_required = False
    if has_module(has_mfa):
        user_has_mfa = has_mfa(username=user.username, request=request)
        mfa_is_required = getattr(django_settings, "MFA_REQUIRED", False)
    show_user_token_mfa = not mfa_is_required or (mfa_is_required and user_has_mfa)

    context = {
        "user_token": user_token_key,
        "current_use": current_use,
        "quota": quota,
        "has_mfa": user_has_mfa,
        "mfa_required": mfa_is_required,
        "show_user_token_mfa": show_user_token_mfa,
    }
    return context


@login_required()
@never_cache
def profile(request):
    """
    Handle the profile view.
    """
    context = get_user_context(request)
    template = get_custom_template(
        "User Page Template", "tethys_portal/user/profile.html"
    )
    return render(request, template, context)


@login_required()
@never_cache
def settings(request):
    """
    Handle the settings view. Access to change settings are not publicly accessible
    """
    # Get the user object from model
    user = request.user

    if request.method == "POST" and "user-settings-submit" in request.POST:
        # Create a form populated with request data
        form = UserSettingsForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]

            # Update the User Model
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            # Save changes
            user.save()

            # Redirect
            return redirect("user:profile")
    else:
        # Create a form populated with data from the instance user
        form = UserSettingsForm(instance=user)

    context = get_user_context(request)
    context["form"] = form
    template = get_custom_template(
        "User Settings Page Template", "tethys_portal/user/settings.html"
    )
    return render(request, template, context)


@login_required()
@never_cache
def change_password(request):
    """
    Handle change password request.
    """
    # Get the user object from model
    request_user = request.user

    # Handle form
    if request.method == "POST" and "change-password-submit" in request.POST:
        # Create a form populated with request data
        form = UserPasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            # Validate the old and new passwords
            form.clean_old_password()
            form.clean_new_password2()

            # If no exceptions raised to here, then the old password is valid and the new passwords match.
            # Save the new passwords to the database.
            form.save()

            # Return to the settings page
            return redirect("user:settings")

    else:
        # Create a form populated with data from the instance user
        form = UserPasswordChangeForm(user=request_user)

    # Create template context object
    context = {"form": form}

    return render(request, "tethys_portal/accounts/change_password.html", context)


@login_required()
def social_disconnect(request, provider, association_id):
    """
    Display a confirmation for disconnect a social account.
    """

    context = {"provider": provider, "association_id": association_id}
    return render(request, "tethys_portal/user/disconnect.html", context)


@login_required()
def delete_account(request):
    """
    Handle account delete requests.
    """
    # Handle form submission
    if request.method == "POST" and "delete-account-submit" in request.POST:
        # Delete user
        request.user.delete()

        # Perform user logout
        logout(request)

        # Give feedback
        messages.success(request, "Your account has been successfully deleted.")

        # Redirect to home
        if django_settings.MULTIPLE_APP_MODE:
            return redirect("home")
        else:
            return redirect("accounts:login")

    context = {}

    return render(request, "tethys_portal/user/delete.html", context)


@login_required()
def clear_workspace(request, root_url):
    """
    Handle clear workspace requests.
    """

    app = TethysApp.objects.get(root_url=root_url)

    # Handle form submission
    if request.method == "POST" and "clear-workspace-submit" in request.POST:
        app = get_app_class(app)

        user = request.user
        workspace = get_user_workspace(app, user, bypass_quota=True)

        app.pre_delete_user_workspace(user)
        workspace.clear()
        app.post_delete_user_workspace(user)

        media = get_user_media(app, user)
        app.pre_delete_user_media(user)
        media.clear()
        app.post_delete_user_media(user)

        # Give feedback
        messages.success(
            request,
            "Your workspace and media directory have been successfully cleared.",
        )

        # Redirect to home
        return redirect("user:manage_storage")

    context = {"app_name": app.name}

    return render(request, "tethys_portal/user/clear_workspace.html", context)


@login_required()
def manage_storage(request):
    """
    Handle clear workspace requests.
    """

    apps = SingletonHarvester().apps
    user = request.user

    for app in apps:
        workspace = get_user_workspace(app, user, bypass_quota=True)
        app.current_use = _convert_storage_units("gb", workspace.get_size("gb"))

    codename = "user_workspace_quota"
    rqh = WorkspaceQuotaHandler(user)
    current_use = _convert_storage_units(rqh.units, rqh.get_current_use())
    quota = get_quota(user, codename)
    quota = _check_quota_helper(quota)

    context = {
        "apps": apps,
        "current_use": current_use,
        "quota": quota,
    }

    return render(request, "tethys_portal/user/manage_storage.html", context)


def _check_quota_helper(quota):
    if quota["quota"]:
        return _convert_storage_units(quota["units"], quota["quota"])
    else:
        return None
