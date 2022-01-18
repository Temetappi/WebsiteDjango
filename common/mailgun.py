import os
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:

    SUBJECT = 'Message from teemurahkonen.com'
    RECIPIENT = 'teemurahkonen@gmail.com'
    FROM_EMAIL = os.environ.get('MAILGUN_ADDRESS', None)

    @classmethod
    def send_mail(cls, email: str, message: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)

        if api_key is None:
            raise MailgunException('Failed to load Mailgun API key.')
        if domain is None:
            raise MailgunException('Failed to load Mailgun domain.')
        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={
                            "from": f"{email} <{cls.FROM_EMAIL}>",
                            "to": cls.RECIPIENT,
                            "subject": cls.SUBJECT,
                            "text": message})
        if response.status_code != 200:
            raise MailgunException('AN error occurred while sending e-mail.')
        return response
