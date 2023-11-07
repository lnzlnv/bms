import threading

from django.contrib.auth.forms import PasswordResetForm as BaseForm


class PasswordResetForm(BaseForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        mailing_thread = threading.Thread(
            target=super().send_mail,
            args=(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                to_email,
                html_email_template_name
            )
        )

        mailing_thread.start()
