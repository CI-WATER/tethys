"""
********************************************************************************
* Name: helpers.py
* Author: tbayer, mlebarron
* Created On: February 22, 2019
* Copyright: (c) Aquaveo 2018
********************************************************************************
"""

import logging
from django.conf import settings
from django.core.exceptions import PermissionDenied


log = logging.getLogger("tethys." + __name__)


def sync_resource_quota_handlers():
    from tethys_quotas.models import ResourceQuota
    from tethys_quotas.handlers.base import ResourceQuotaHandler
    from tethys_sdk.quotas import codenames

    if hasattr(settings, "RESOURCE_QUOTA_HANDLERS"):
        quota_codenames = []
        for quota_class_str in settings.RESOURCE_QUOTA_HANDLERS:
            try:
                components = quota_class_str.split(".")
                mod = __import__(".".join(components[:-1]), fromlist=[components[-1]])
                class_obj = getattr(mod, components[-1])
            except Exception:
                log.warning(
                    "Unable to load ResourceQuotaHandler: {} is not correctly formatted class or does not exist".format(
                        quota_class_str
                    )
                )
                continue

            if not issubclass(class_obj, ResourceQuotaHandler):
                log.warning(
                    "Unable to load ResourceQuotaHandler: {} is not a subclass of ResourceQuotaHandler".format(
                        quota_class_str
                    )
                )
                continue
            else:
                for entity in class_obj.applies_to:
                    entity_type = entity.split(".")[-1]
                    codename = "{}_{}".format(entity_type.lower(), class_obj.codename)
                    quota_codenames.append(codename)

                    if not ResourceQuota.objects.filter(codename=codename).exists():
                        resource_quota = ResourceQuota(
                            codename="{}_{}".format(
                                entity_type.lower(), class_obj.codename
                            ),
                            name="{} {}".format(entity_type, class_obj.name),
                            description=class_obj.description,
                            default=class_obj.default,
                            units=class_obj.units,
                            applies_to=entity,
                            impose_default=True,
                            help=class_obj.help,
                            _handler=quota_class_str,
                        )
                        resource_quota.save()

        for rq in ResourceQuota.objects.all():
            if rq.codename not in quota_codenames:
                rq.delete()
            else:
                setattr(codenames, rq.codename.upper(), rq.codename)


def passes_quota(entity, codename, raise_on_false=True):
    """
    Checks to see if the quota has been exceeded or not

    Args:
        entity(User or TethysApp): the entity on which to check.
        codename(str): codename of the Quota to check
        raise_on_false(bool): raise error if entity does not pass quota.

    Returns:
        False if the entity has exceeded the quota, otherwise True.

    Raises: PermissionDenied error if `raise_on_false` is True and user does not pass quota.
    """
    from tethys_quotas.models import ResourceQuota

    try:
        rq = ResourceQuota.objects.get(codename=codename)
        passes = rq.check_quota(entity)
        if not passes and raise_on_false:
            raise PermissionDenied(rq.help)
        return passes

    except ResourceQuota.DoesNotExist:
        if codename not in settings.SUPPRESS_QUOTA_WARNINGS:
            log.info(f"ResourceQuota with codename {codename} does not exist.")
        return True


def get_resource_available(entity, codename):
    """
    Checks the quantity of resources remaining before the quota is met

    Args:
        entity (User or TethysApp): the entity on which to check.
        codename (str): codename of the Quota to check

    Returns:
        dict (resource_available, units): Dictionary with two keys: resource_available(int) - amount of resource remaining, units(str) - units of amount, if applicable  # noqa: E501
    """
    from tethys_quotas.models import ResourceQuota

    try:
        rq = ResourceQuota.objects.get(codename=codename)
        rqh = rq.handler(entity)
        current_use = rqh.get_current_use()

    except ResourceQuota.DoesNotExist:
        log.warning(
            "Invalid Codename: ResourceQuota with codename {} does not exist.".format(
                codename
            )
        )
        return None

    total_available = get_quota(entity, codename)
    if total_available["quota"]:
        total_available = total_available["quota"]
        resource_available = total_available - current_use
    else:
        return None

    if resource_available < 0:
        resource_available = 0

    return {"resource_available": resource_available, "units": rq.units}


def get_quota(entity, codename):
    """
    Gets the quota value

    Args:
        entity (User or TethysApp): the entity on which to perform quota check.
        codename (str): codename of the Quota to get

    Returns:
        dict (quota, units): Dictionary with two keys: quota(int) - value of quota, units(str) - units of value, if applicable  # noqa: E501
    """
    from django.contrib.auth.models import User
    from tethys_apps.models import TethysApp
    from tethys_quotas.models import ResourceQuota, UserQuota, TethysAppQuota

    result = {
        "quota": None,
        "units": None,
    }
    try:
        rq = ResourceQuota.objects.get(codename=codename)
        result["units"] = rq.units

    except ResourceQuota.DoesNotExist:
        log.warning(
            "Invalid Codename: ResourceQuota with codename {} does not exist.".format(
                codename
            )
        )
        return result

    if not rq.active:
        return result

    try:
        if isinstance(entity, User):
            if entity.is_staff:
                return result
            eq = UserQuota.objects.get(entity=entity)

        elif isinstance(entity, TethysApp):
            eq = TethysAppQuota.objects.get(entity=entity)

        else:
            raise ValueError("Entity needs to be User or TethysApp")

        quota = eq.value
        if quota:
            result["quota"] = quota
            return result

    except (UserQuota.DoesNotExist, TethysAppQuota.DoesNotExist):
        pass

    if rq.impose_default:
        result["quota"] = rq.default

    return result


# Adapted from https://pypi.org/project/hurry.filesize/
def _convert_storage_units(units, amount):
    base_units = _get_storage_units()

    base_conversion = [item[0] for item in base_units if units.upper() in item[1]]
    if not base_conversion:
        return None

    amount = amount * base_conversion[0]

    for factor, suffix in base_units:  # noqa: B007
        if amount >= factor:
            break
    amount = int(amount / factor)
    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


def _get_storage_units():
    return [
        (1024 ** 5, " PB"),
        (1024 ** 4, " TB"),
        (1024 ** 3, " GB"),
        (1024 ** 2, " MB"),
        (1024 ** 1, " KB"),
        (1024 ** 0, (" byte", " bytes")),
    ]
