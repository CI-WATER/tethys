import yaml
import json
import getpass
from os import devnull
from pathlib import Path
from subprocess import call, Popen, PIPE, STDOUT
from argparse import Namespace
from collections.abc import Mapping
import sys

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from tethys_cli.cli_colors import (
    write_msg,
    write_error,
    write_warning,
    write_success,
)
from tethys_cli.services_commands import services_list_command
from tethys_cli.cli_helpers import (
    setup_django,
    generate_salt_string,
)
from tethys_apps.utilities import (
    link_service_to_app_setting,
    get_app_settings,
    get_service_model_from_type,
    get_tethys_home_dir,
)

from .gen_commands import download_vendor_static_files
from tethys_portal.optional_dependencies import optional_import, has_module

# optional imports
conda_run, Commands = optional_import(
    ("run_command", "Commands"), from_module="conda.cli.python_api"
)

FNULL = open(devnull, "w")


def add_install_parser(subparsers):
    # Install Commands

    application_install_parser = subparsers.add_parser(
        "install", help="Install and Initialize Applications"
    )
    application_install_parser.add_argument(
        "-d",
        "--develop",
        help="Will run pip install with editable option.",
        action="store_true",
    )
    application_install_parser.add_argument(
        "-f", "--file", type=str, help="The path to the Install file. "
    )
    application_install_parser.add_argument(
        "-s",
        "--services-file",
        type=str,
        help="The path to the Services.yml config file",
    )
    application_install_parser.add_argument(
        "--force-services",
        help="Force Services.yml file over portal_config.yml file",
        action="store_true",
    )
    application_install_parser.add_argument(
        "-q", "--quiet", help="Skips interactive mode.", action="store_true"
    )
    application_install_parser.add_argument(
        "-n",
        "--no-sync-stores",
        help="Skips syncstores when linked persistent stores are found.",
        action="store_true",
    )
    application_install_parser.add_argument(
        "-N",
        "--no-db-sync",
        help="Skips any database related commands.",
        action="store_true",
    )
    application_install_parser.add_argument(
        "-v",
        "--verbose",
        help="Will show all pip install output when enabled.",
        action="store_true",
    )
    application_install_parser.add_argument(
        "-u",
        "--update-installed",
        help="Will attempt to update already installed dependencies to versions "
        "listed in the install.yml. WARNING: This may break your Tethys "
        "installation and is not recommended.",
        action="store_true",
    )
    application_install_parser.add_argument(
        "-o",
        "--only-dependencies",
        help="Install only the dependencies of an app or extension.",
        action="store_true",
    )

    application_install_parser.add_argument(
        "-w",
        "--without-dependencies",
        help="Install the app or extension without installing its dependencies.",
        action="store_true",
    )

    application_install_parser.set_defaults(func=install_command)


def open_file(file_path):
    try:
        with file_path.open() as f:
            return yaml.safe_load(f)

    except Exception as e:
        write_error(str(e))
        write_error("An unexpected error occurred reading the file. Please try again.")
        exit(1)


def validate_service_id(service_type, service_id):
    service_model = get_service_model_from_type(service_type)
    try:
        service_model.objects.get(id=service_id)  # noqa: F841
        return True
    except (ObjectDoesNotExist, ValueError):
        try:
            service_model.objects.get(name=service_id)  # noqa: F841
            return True
        except ObjectDoesNotExist:
            pass

    return False


def get_setting_type_from_setting(setting):
    from tethys_apps.models import (
        PersistentStoreDatabaseSetting,
        PersistentStoreConnectionSetting,
        SpatialDatasetServiceSetting,
        DatasetServiceSetting,
        WebProcessingServiceSetting,
    )

    if setting.__class__ == PersistentStoreDatabaseSetting or isinstance(
        setting, PersistentStoreDatabaseSetting
    ):
        return "ps_database"

    elif setting.__class__ == PersistentStoreConnectionSetting or isinstance(
        setting, PersistentStoreConnectionSetting
    ):
        return "ps_connection"

    elif setting.__class__ == SpatialDatasetServiceSetting or isinstance(
        setting, SpatialDatasetServiceSetting
    ):
        return "ds_spatial"

    elif setting.__class__ == DatasetServiceSetting or isinstance(
        setting, DatasetServiceSetting
    ):
        return "ds_dataset"

    elif setting.__class__ == WebProcessingServiceSetting or isinstance(
        setting, WebProcessingServiceSetting
    ):
        return "wps"

    raise RuntimeError(f"Could not determine setting type for setting: {setting}")


def get_service_type_from_setting(setting):
    from tethys_apps.models import (
        PersistentStoreDatabaseSetting,
        PersistentStoreConnectionSetting,
        SpatialDatasetServiceSetting,
        DatasetServiceSetting,
        WebProcessingServiceSetting,
    )

    if setting.__class__ == PersistentStoreDatabaseSetting or isinstance(
        setting, PersistentStoreDatabaseSetting
    ):
        return "persistent"

    elif setting.__class__ == PersistentStoreConnectionSetting or isinstance(
        setting, PersistentStoreConnectionSetting
    ):
        return "persistent"

    elif setting.__class__ == SpatialDatasetServiceSetting or isinstance(
        setting, SpatialDatasetServiceSetting
    ):
        return "spatial"

    elif setting.__class__ == DatasetServiceSetting or isinstance(
        setting, DatasetServiceSetting
    ):
        return "dataset"

    elif setting.__class__ == WebProcessingServiceSetting or isinstance(
        setting, WebProcessingServiceSetting
    ):
        return "wps"

    raise RuntimeError(f"Could not determine service type for setting: {setting}")


# Pulling this function out, so I can mock this for inputs to the interactive mode
def get_interactive_input():
    return input("")


def get_service_name_input():
    return input("")


def print_unconfigured_settings(app_name, unlinked_settings):
    if len(unlinked_settings) > 0:
        write_msg(
            f"\nThe following settings were not configured for app: {app_name}:\n"
        )
        write_msg("{0: <50}{1: <50}{2: <15}".format("Name", "Type", "Required"))

        for unlinked_setting in unlinked_settings:
            write_msg(
                "{0: <50}{1: <50}{2: <15}".format(
                    unlinked_setting.name,
                    unlinked_setting.__class__.__name__,
                    str(unlinked_setting.required),
                )
            )


def run_sync_stores(app_name, linked_settings):
    from tethys_apps.models import (
        PersistentStoreConnectionSetting,
        PersistentStoreDatabaseSetting,
    )

    linked_persistent = False
    for setting in linked_settings:
        if isinstance(setting, PersistentStoreDatabaseSetting) or isinstance(
            setting, PersistentStoreConnectionSetting
        ):
            linked_persistent = True

    if linked_persistent:
        write_msg("Running syncstores for app {}".format(app_name))
        call(["tethys", "syncstores", app_name])


def get_setting_type(setting):
    from tethys_apps.models import (
        PersistentStoreConnectionSetting,
        PersistentStoreDatabaseSetting,
        SpatialDatasetServiceSetting,
        DatasetServiceSetting,
        WebProcessingServiceSetting,
        CustomSettingBase,
        CustomSetting,
        SecretCustomSetting,
        JSONCustomSetting,
    )

    setting_type_dict = {
        PersistentStoreConnectionSetting: "persistent",
        PersistentStoreDatabaseSetting: "persistent",
        SpatialDatasetServiceSetting: "spatial",
        DatasetServiceSetting: "dataset",
        WebProcessingServiceSetting: "wps",
        CustomSettingBase: "custom_setting_base",
        CustomSetting: "custom_setting",
        SecretCustomSetting: "secret_custom_setting",
        JSONCustomSetting: "json_custom_setting",
    }

    return setting_type_dict[type(setting)]


def run_interactive_services(app_name):
    write_msg(
        "Running Interactive Service Mode. "
        "Any configuration options in services.yml or portal_config.yml will be ignored..."
    )
    write_msg("Hit return at any time to skip a step.")

    app_settings = get_app_settings(app_name)

    # In the case the app isn't installed, has no settings, or it is an extension,
    # skip configuring services/settings
    if not app_settings:
        write_msg(
            f'No settings found for app "{app_name}". Skipping interactive configuration...'
        )
        return

    unlinked_settings = app_settings["unlinked_settings"]

    for setting in unlinked_settings:
        valid = False
        configure_text = "Configuring {}".format(setting.name)
        star_out = "*" * len(configure_text)
        write_msg(f"\n{star_out}\n{configure_text}\n{star_out}")
        write_msg(
            f"Type: {setting.__class__.__name__}\n"
            f"Description: {setting.description}\n"
            f"Required: {setting.required}"
        )

        # extra code to generate a salt string
        if (
            getattr(setting, "type_custom_setting", None) is not None
            and setting.type_custom_setting == "SECRET"
        ):
            proceed = input(
                "Do you want to generate a salt string for this secret or use the default behavior: [y/n]"
            )
            while proceed not in ["y", "n", "Y", "N"]:
                proceed = input('Please enter either "y" or "n": ')

            if proceed in ["y", "n", "Y", "N"]:
                # with pretty_output(FG_GREEN) as p:
                TETHYS_HOME = Path(get_tethys_home_dir())
                secrets_yaml_file = TETHYS_HOME / "secrets.yml"
                portal_secrets = {}

                if proceed in ["y", "Y"] and not secrets_yaml_file.exists():
                    write_warning("No secrets.yml found. Generating one...")
                    call(["tethys", "gen", "secrets"])
                    write_msg("secrets file generated.")
                if secrets_yaml_file.exists():
                    with secrets_yaml_file.open("r") as secrets_yaml:
                        portal_secrets = yaml.safe_load(secrets_yaml) or {}
                        if app_name not in portal_secrets["secrets"]:
                            # always reset on a new install
                            portal_secrets["secrets"][app_name] = {}
                        if (
                            "custom_settings_salt_strings"
                            not in portal_secrets["secrets"][app_name]
                        ):
                            write_msg(
                                f"No custom_settings_salt_strings in the app definition for the app {app_name} in the apps portion in the portal_config.yml. Generating one..."
                            )
                            portal_secrets["secrets"][app_name][
                                "custom_settings_salt_strings"
                            ] = {}

                        if proceed in ["y", "Y"]:
                            salt_string = generate_salt_string().decode()
                            portal_secrets["secrets"][app_name][
                                "custom_settings_salt_strings"
                            ][setting.name] = salt_string
                            msge = "Successfully created salt string for {0} Secret Custom Setting!".format(
                                setting.name
                            )
                            write_msg(msge)
                        else:
                            if (
                                setting.name
                                in portal_secrets["secrets"][app_name][
                                    "custom_settings_salt_strings"
                                ]
                            ):
                                del portal_secrets["secrets"][app_name][
                                    "custom_settings_salt_strings"
                                ][setting.name]
                        with secrets_yaml_file.open("w") as secrets_yaml:
                            yaml.dump(portal_secrets, secrets_yaml)
                            write_msg(
                                f"custom_settings_salt_strings created for setting: {setting.name} in app {app_name}"
                            )

        if hasattr(setting, "value"):
            while not valid:
                write_msg(
                    "\nEnter the desired value for the current custom setting: {}".format(
                        setting.name
                    )
                )
                try:
                    value = ""
                    if setting.type_custom_setting == "JSON":
                        proceed = input(
                            "Do you want to upload the json from a file: [y/n] "
                        )
                        while proceed not in ["y", "n", "Y", "N"]:
                            proceed = input('Please enter either "y" or "n": ')

                        if proceed in ["y", "Y"]:
                            json_path = input(
                                "Please provide a file containing a Json (e.g: /home/user/myjsonfile.json): "
                            )
                            try:
                                value = json.loads(Path(json_path).read_text())
                            except FileNotFoundError:
                                write_warning("The current file path was not found")
                        else:
                            # String with JSON format
                            data_JSON_example = '{"size": "Medium", "price": 15.67, "toppings": ["Mushrooms", "Extra Cheese", "Pepperoni", "Basil"]}'
                            write_msg(
                                f"Please provide a Json string (e.g: {data_JSON_example})"
                            )
                            try:
                                value = json.loads(get_interactive_input())
                            except json.decoder.JSONDecodeError:
                                write_msg("Invalid Json provided")
                    else:
                        if setting.type_custom_setting != "SECRET":
                            value = get_interactive_input()
                        else:
                            value = getpass.getpass(prompt="")
                    if value != "":
                        try:
                            setting.value = value
                            setting.clean()
                            setting.save()
                            valid = True
                            if setting.type_custom_setting != "SECRET":
                                write_success(
                                    "{} successfully set with value: {}.".format(
                                        setting.name, value
                                    )
                                )
                            else:
                                write_success(
                                    "{} successfully set".format(setting.name)
                                )
                        except ValidationError:
                            write_error(
                                "Incorrect value type given for custom setting '{}'. Please try again".format(
                                    setting.name
                                )
                            )

                    else:
                        write_msg("Skipping setup of {}".format(setting.name))
                        valid = True

                except (KeyboardInterrupt, SystemExit):
                    write_msg("\nInstall Command cancelled.")
                    exit(0)
        else:
            # List existing services
            args = Namespace()

            for conf in ["spatial", "persistent", "wps", "dataset"]:
                setattr(args, conf, False)

            setattr(args, get_setting_type(setting), True)
            services = services_list_command(args)[0]

            if len(services) <= 0:
                write_warning(
                    "No compatible services found. See:\n\n  tethys services create {} -h\n".format(
                        get_setting_type(setting)
                    )
                )
                continue

            while not valid:
                write_msg(
                    "\nEnter the service ID/Name to link to the current service setting: {}.".format(
                        setting.name
                    )
                )
                try:
                    service_id = get_interactive_input()
                    if service_id != "":
                        try:
                            setting_type = get_setting_type_from_setting(setting)
                            service_type = get_service_type_from_setting(setting)
                        except RuntimeError as e:
                            write_error(str(e) + " Skipping...")
                            break

                        # Validate the given service id
                        valid_service = validate_service_id(service_type, service_id)

                        if valid_service:
                            link_service_to_app_setting(
                                service_type,
                                service_id,
                                app_name,
                                setting_type,
                                setting.name,
                            )

                            valid = True
                        else:
                            write_error("Incorrect service ID/Name. Please try again.")

                    else:
                        write_msg("Skipping setup of {}".format(setting.name))
                        valid = True

                except (KeyboardInterrupt, SystemExit):
                    write_msg("\nInstall Command cancelled.")
                    exit(0)


def find_and_link(service_type, setting_name, service_id, app_name, setting):
    valid_service = validate_service_id(service_type, service_id)
    setting_type = get_setting_type_from_setting(setting)
    if valid_service:
        link_service_to_app_setting(
            service_type, service_id, app_name, setting_type, setting_name
        )
    else:
        write_error(
            f'Warning: Could not find service of type: "{service_type}" with the Name/ID: "{service_id}"'
        )


def configure_services_from_file(services, app_name):
    from tethys_apps.models import TethysApp, CustomSettingBase

    if "version" in services:
        del services["version"]

    db_app = TethysApp.objects.get(package=app_name)

    for service_type in services:
        if services[service_type] is not None:
            current_services = services[service_type]
            for setting_name in current_services:
                if service_type == "custom_settings":
                    try:
                        custom_setting = (
                            CustomSettingBase.objects.filter(tethys_app=db_app.id)
                            .select_subclasses()
                            .get(name=setting_name)
                        )
                    except ObjectDoesNotExist:
                        write_warning(
                            f'Custom setting named "{setting_name}" could not be found in app "{app_name}". '
                            f"Skipping..."
                        )
                        continue

                    try:
                        if custom_setting.type_custom_setting == "JSON":
                            custom_setting.value = assign_json_value(
                                current_services[setting_name]
                            )
                            if custom_setting.value is None:
                                write_warning(
                                    f'Custom setting named "{setting_name}" is not valid in app "{app_name}". '
                                    f"Skipping..."
                                )
                                continue
                        else:
                            custom_setting.value = current_services[setting_name]
                        custom_setting.clean()
                        custom_setting.save()
                        write_success(
                            f'CustomSetting: "{setting_name}" was assigned the value: '
                            f'"{current_services[setting_name]}"'
                        )

                    except ValidationError:
                        write_error(
                            "Incorrect value type given for custom setting '{}'. Please adjust "
                            "services.yml or set the value in the app's settings page.".format(
                                setting_name
                            )
                        )
                else:
                    app_settings = get_app_settings(app_name)

                    # In the case the app isn't installed, has no settings, or it is an extension,
                    # skip configuring services/settings
                    if not app_settings:
                        write_msg(
                            f'No settings found for app "{app_name}". Skipping automated configuration...'
                        )
                        return

                    unlinked_settings = app_settings["unlinked_settings"]

                    setting_found = False
                    for setting in unlinked_settings:
                        if setting.name != setting_name:
                            continue

                        setting_found = True

                        service_id = current_services[setting_name]
                        if not service_id:
                            write_warning(
                                f'No service given for setting "{setting_name}". Skipping...'
                            )
                            continue

                        find_and_link(
                            service_type,
                            setting_name,
                            service_id,
                            app_name,
                            setting,
                        )

                    if not setting_found:
                        write_warning(
                            f'Service setting "{setting_name}" already configured or does not exist in app '
                            f'"{app_name}". Skipping...'
                        )


def run_portal_install(app_name):
    file_path = Path(get_tethys_home_dir()) / "portal_config.yml"

    if not file_path.exists():
        write_msg(
            "No Portal Services file found. Searching for local app level services.yml..."
        )
        return False

    write_msg("Portal install file found...Processing...")
    portal_options = open_file(file_path)
    app_check = portal_options and "apps" in portal_options and portal_options["apps"]
    if (
        app_check
        and app_name in portal_options["apps"]
        and "services" in portal_options["apps"][app_name]
    ):
        services = portal_options["apps"][app_name]["services"]
        if services and len(services) > 0:
            configure_services_from_file(services, app_name)
        else:
            write_msg(
                "No app configuration found for app: {} in portal config file. "
                "Searching for local app level services.yml... ".format(app_name)
            )
            return False

    else:
        write_msg(
            "No apps configuration found in portal config file. "
            "Searching for local app level services.yml... "
        )
        return False

    return True


def run_services(app_name, args):
    file_path = (
        Path("./services.yml")
        if args.services_file is None
        else Path(args.services_file)
    )

    if not file_path.exists():
        write_msg("No Services file found.")
        return

    services = open_file(file_path)

    if services and len(services) > 0:
        configure_services_from_file(services, app_name)
    else:
        write_msg("No Services listed in Services file.")


def install_packages(conda_config, update_installed=False):
    # Compile channels arguments
    install_args = []
    if validate_schema("channels", conda_config):
        channels = conda_config["channels"]
        for channel in channels:
            install_args.extend(["-c", channel])

    # Install all Packages
    if validate_schema("packages", conda_config):
        if not update_installed:
            install_args.extend(["--freeze-installed"])
        else:
            write_warning(
                "Warning: Updating previously installed packages. This could break your Tethys environment."
            )
        install_args.extend(conda_config["packages"])
        write_msg("Running conda installation tasks...")
        [resp, err, code] = conda_run(
            Commands.INSTALL,
            *install_args,
            use_exception_handler=False,
            stdout=None,
            stderr=None,
        )
        if code != 0:
            write_error(
                "Warning: Packages installation ran into an error. Please try again or a manual install"
            )


def install_command(args):
    """
    install Command
    """
    app_name = None
    skip_config = False
    file_path = Path("./install.yml" if args.file is None else args.file)

    # Check for install.yml file
    if not file_path.exists():
        write_warning("WARNING: No install file found.")
        if not args.quiet:
            valid_inputs = ("y", "n", "yes", "no")
            no_inputs = ("n", "no")

            generate_input = input(
                "Would you like to generate a template install.yml file in your current directory "
                "now? (y/n): "
            )

            while generate_input not in valid_inputs:
                generate_input = input("Invalid option. Try again. (y/n): ").lower()

            if generate_input in no_inputs:
                skip_config = True
                write_msg("Generation of Install File cancelled.")
            else:
                call(["tethys", "gen", "install"])
                write_msg(
                    "Install file generated. Fill out necessary information and re-install."
                )
                exit(0)

        write_warning("Continuing install without configuration.")

    # Install Dependencies
    if not skip_config:
        write_msg("Installing dependencies...")
        install_options = open_file(file_path)

        if "name" in install_options:
            app_name = install_options["name"]

        if validate_schema("requirements", install_options):
            requirements_config = install_options["requirements"]
            skip = False
            if "skip" in requirements_config:
                skip = requirements_config["skip"]

            if skip:
                write_warning("Skipping package installation, Skip option found.")
            elif args.without_dependencies:
                write_warning("Skipping package installation.")
            else:
                if validate_schema("conda", requirements_config):  # noqa: E501
                    if has_module(conda_run):
                        conda_config = requirements_config["conda"]
                        install_packages(
                            conda_config,
                            update_installed=args.update_installed,
                        )
                    else:
                        write_warning("Conda is not installed...")
                        if not args.quiet:
                            proceed = input(
                                "Attempt to install conda packages with pip and continue the installation process: [y/n]"
                            )
                            while proceed not in ["y", "n", "Y", "N"]:
                                proceed = input('Please enter either "y" or "n": ')
                        else:
                            proceed = "y"

                        if proceed in ["y", "n", "Y", "N"]:
                            if proceed in ["y", "Y"]:
                                try:
                                    call(
                                        [
                                            "pip",
                                            "install",
                                            *requirements_config["conda"]["packages"],
                                        ]
                                    )
                                except Exception as e:
                                    write_error(
                                        f"Installing conda packages with pip failed with the following exception: {e}"
                                    )
                            else:
                                write_msg("\nInstall Command cancelled.")
                                exit(0)

                if validate_schema("pip", requirements_config):
                    write_msg("Running pip installation tasks...")
                    call(["pip", "install", *requirements_config["pip"]])
                try:
                    public_resources_dir = [
                        *Path().glob(str(Path("tethysapp", "*", "public"))),
                        *Path().glob(str(Path("tethysapp", "*", "static"))),
                    ][0]
                except IndexError:
                    write_warning(
                        "No public directory detected. Unable to process JavaScript dependencies."
                    )
                else:
                    package_json_file = public_resources_dir / "package.json"
                    if validate_schema("npm", requirements_config):
                        npm_requirements = requirements_config["npm"]
                        try:
                            assert isinstance(npm_requirements, dict)
                        except AssertionError:
                            write_error(
                                "The npm requirements are not formatted correctly. "
                                'It should be provided as key-value (e.g. "package_name: 1.0").'
                            )
                        else:
                            with package_json_file.open("w") as f:
                                json.dump({"dependencies": npm_requirements}, f)
                    if package_json_file.exists():
                        download_vendor_static_files(
                            None, cwd=str(public_resources_dir)
                        )

    # Skip the rest if we are installing dependencies only
    if args.only_dependencies:
        write_success(f"Successfully installed dependencies for {app_name}.")
        return

    # Install Python Package
    write_msg("Running application install....")

    if args.develop:
        cmd = ["pip", "install", "-e", "."]
    else:
        cmd = ["pip", "install", "."]

    if args.verbose:
        call(cmd, stderr=STDOUT)
    else:
        call(cmd, stdout=FNULL, stderr=STDOUT)

    if args.no_db_sync:
        write_success(f"Successfully installed {app_name}.")
        return

    call(["tethys", "db", "sync"])

    # Run Portal Level Config if present
    if not skip_config:
        setup_django()
        if args.force_services:
            run_services(app_name, args)
        else:
            portal_result = run_portal_install(app_name)
            if not portal_result:
                run_services(app_name, args)

        if args.quiet:
            write_msg(
                "Quiet mode: No additional service setting validation will be performed."
            )
        else:
            run_interactive_services(app_name)

        write_success("Services Configuration Completed.")
        app_settings = get_app_settings(app_name)

        if app_settings is not None:
            linked_settings = app_settings["linked_settings"]
            unlinked_settings = app_settings["unlinked_settings"]
            if args.no_sync_stores:
                write_msg("Skipping syncstores.")
            else:
                run_sync_stores(app_name, linked_settings)

            print_unconfigured_settings(app_name, unlinked_settings)

        # Check to see if any extra scripts need to be run
        if validate_schema("post", install_options):
            write_msg("Running post installation tasks...")
            for post in install_options["post"]:
                path_to_post = file_path.resolve().parent / post
                # Attempting to run processes.
                if path_to_post.name.endswith(".py"):
                    path_to_post = f"{sys.executable} {path_to_post}"
                process = Popen(str(path_to_post), shell=True, stdout=PIPE)
                stdout = process.communicate()[0]
                write_msg("Post Script Result: {}".format(stdout))
    write_success(f"Successfully installed {app_name}.")


def validate_schema(check_str, check_list):
    return (
        check_str in check_list
        and check_list[check_str]
        and len(check_list[check_str]) > 0
    )


def assign_json_value(value):
    # Check if the value is a file path
    if isinstance(value, str):
        try:
            try_path = Path(value)
            if try_path.is_file():
                json_data = json.loads(try_path.read_text())
                return json_data
            else:
                # Check if the value is a valid JSON string
                json_data = json.loads(value)
                return json_data
        except ValueError:
            write_error(
                f"The current file path/JSON string: {value} is not a file path or does not contain a valid JSONstring."
            )
            return None
    if isinstance(value, Mapping):
        # when the dict is read from the portal_config.yaml, if it is not a proper dict, the portal will fail, so it is not possible to test it
        return value
    else:
        write_error(f"The current value: {value} is not a dict or a valid file path")
        return None
