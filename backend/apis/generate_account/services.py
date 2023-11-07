import threading
import string
import secrets
from faker import Faker

from django.core.mail import send_mail


def generate_username():
    fake = Faker()
    return fake.user_name()


def generate_password():
    length = 16
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def send_user_credentials_to_email_address(
    *,
    email: str,
    username: str,
    password: str
):
    subject = 'BUCAL User Credentials'
    message = \
        """Greetings!\n
This is the credentials that will be used to sign-in in BUCAL Basketball Management System:\n
Username: {}
Password: {}\n
It this is a mistake please ignore this message.\n
Regards,
BUCAL
        """.format(username, password)
    from_email = 'no-reply@bucal.com'
    recipient_list = [email]

    mailing_thread = threading.Thread(
        target=send_mail,
        args=(subject, message, from_email, recipient_list)
    )
    mailing_thread.start()


class ActivationStatus:
    def __init__(self, email, is_approved, site_url):
        self.message = self._approved_message(site_url) if is_approved else self._reject_message()
        self.subject = 'Account Activation Status'
        self.from_email = 'bucal'
        self.recipient_list = [email]


    def send_email_status(self):
        mailing_thread = threading.Thread(
            target=send_mail,
            args=(
                self.subject,
                self.message,
                self.from_email,
                self.recipient_list
            )
        )
        mailing_thread.start()

    def _approved_message(self, site_url):
        return """Greetings!\n
Your account activation request has been approved. You may now sign-in at {}.\n
Thank you!
        """.format(site_url)

    def _reject_message(self):
        return """Greetings!\n
Your account activation request has been denied. You may request another one.\n
Please contact the commissioner for more details.\n
Thank you!
"""