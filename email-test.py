import yagmail

APP_PASSWORD = "asgjqxybengsypbj"
APP_GMAIL_ADDRESS = "ayudda.app@gmail.com"

subject = "Testing this thing"
recipient = ["kmondaca@ymail.com", "cschatz@mills.edu"]
contents = """
Hello from AYUDDA.COM.

There's actually no ayudda.com, but this is
a test of an email sent from the app email address.

Make choices, fight everbody!
"""

with yagmail.SMTP(APP_GMAIL_ADDRESS, APP_PASSWORD) as yag:
    yag.send(recipient, subject, contents)
    print("Email sent.")
