from fillpdf.fillpdfs import (
    # get_form_fields,
    write_fillable_pdf,
)

# endings for blank vs completed PDF filenames
BLANK = "-blank.pdf"
COMPLETE = "-completed.pdf"
OUTPUT_DIR = "output"


def fill_one_pdf(form_name, data):
    blank_file = f"{form_name}{BLANK}"
    output_file = f"{OUTPUT_DIR}/{form_name}{COMPLETE}"
    write_fillable_pdf(blank_file, output_file, data, flatten=True)
    return output_file
