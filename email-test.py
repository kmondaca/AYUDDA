import yagmail

APP_PASSWORD = "asgjqxybengsypbj"
APP_GMAIL_ADDRESS = "ayudda.app@gmail.com"

subject = "Testing another thing"
recipient = ["kmondaca@ymail.com", "cschatz@mills.edu"]
# contents = """
# Hello from AYUDDA.COM.
#
# There's actually no ayudda.com, but this is
# a test of an email sent from the app email address.
#
# Make choices, fight everbody!
# """
contents = """
One more test.
I want to make sure CCing works the way I think.
"""

with yagmail.SMTP(APP_GMAIL_ADDRESS, APP_PASSWORD) as yag:
    yag.send(
        to=recipient,
        subject=subject,
        contents=contents,
        cc=APP_GMAIL_ADDRESS)
    print("Email sent.")
