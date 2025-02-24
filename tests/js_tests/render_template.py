import json
import os
import sys

import django
from django.conf import settings
from django.template.loader import render_to_string, select_template

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tethys_portal.settings")

# Add tests templates directory to settings so that django finds them
TEST_TEMPLATE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "templates")
)
if TEST_TEMPLATE_DIR not in settings.TEMPLATES[0]["DIRS"]:
    settings.TEMPLATES[0]["DIRS"].append(TEST_TEMPLATE_DIR)

django.setup()


def confirm_template_path(template_name):
    try:
        # Second try block wrapping is required for handling
        # django errors and getting it to print in js testing
        try:
            select_template([template_name])

        except Exception as e:
            print(f"Error finding template: {e}")
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

    except Exception as e:
        print(f"Error finding template: {e}")
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


def form_output_name(template_name):
    template = template_name.removesuffix(".html")
    return f"{template}_output.html"


def render_template(template_name, context):
    try:
        # Confirm the template path exists
        confirm_template_path(template_name)

        # Render template using context
        try:
            try:
                rendered_html = render_to_string(template_name, context)

            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc(file=sys.stdout)
                sys.exit(1)

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

        output_path = f"./rendered_templates/test_{os.path.basename(form_output_name(template_name))}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the rendered html into the result file
        with open(output_path, "w") as file:
            file.write(rendered_html)

        print(f"Template rendered to {output_path}")
    except Exception as e:
        print(f"Error rendering template: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # breakpoint()
    if len(sys.argv) < 3:
        print("Usage: python render_template.py <template_name> '<json_context>'")
        sys.exit(1)

    template_name = sys.argv[1]
    context = json.loads(sys.argv[2])
    render_template(template_name, context)
