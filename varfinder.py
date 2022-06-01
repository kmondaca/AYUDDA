from fillpdf.fillpdfs import (
    get_form_fields,
    write_fillable_pdf,
)

BLANK_FORM = "DDD-2069A-S-blank.pdf"

#pdf is in directory it knows what to get
form_fields = get_form_fields(BLANK_FORM)

# Just to see how everything starts out
for childName, current_value in form_fields.items():
    if current_value == "":
        current_value = "<blank>"
    print(f"{childName}: {current_value}")