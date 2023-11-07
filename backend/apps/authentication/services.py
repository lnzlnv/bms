import threading

from django.core.mail import send_mail


class ActivationStatus:
    def __init__(self, email, is_approved, site_url):
        self.message = self._approved_message() if is_approved else self._reject_message()
        self.subject = 'Account Activation Status'
        self.from_email = 'bucal'
        self.recipient_list = [email]
        self.site_url = site_url

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

    def _approved_message(self):
        return """Greetings!\n
Your account activation request has been approved. You may now sign-in at {}.\n

Thank you!
        """.format(self.site_url)

    def _reject_message(self):
        return """Greetings!\n
Your account activation request has been denied. You may request another one.\n

Please contact the commissioner for more details.\n

Thank you!
"""