import os


def generate_css(main_color, secondary_color):
    """
    Generate CSS file with colors.

    :param main_color:
    :param secondary_color:
    """
    filename = "static/css/colors.css"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        css_file_contents = f":root {{\n--main-color: {main_color};\n--secondary-color: {secondary_color};\n}}"
        f.write(css_file_contents)
