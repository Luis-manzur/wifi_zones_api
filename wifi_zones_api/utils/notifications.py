import logging

import firebase_admin
from firebase_admin import credentials, messaging

logger = logging.getLogger("console")

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "wifi-zones-1534d",
        "private_key_id": "791cb44b4c9419e91ea527d381a797a64e9265e1",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCYmuM8UaN0zIMt\n+d2bOb/qVye1igRDFKgVlEQQ47tBD2VRxaUxplVSbbsmJZJuUEFvXRntGGWTSp/G\nDhHOA4aKdEIPlINQU0v4PQhI6AICXFbaeCjdOVqvfGZJcaHsIsyZVFw7Iksz3C81\n5EX3YT2meECKukPmsjodI5s7Kbl5LztYRzXP7t2EDdpu/Ze8gmF7sOSKu+U4AHeR\nW/vSYY5NjuxOXIbHh4wjQoXkif4VAxlo3Q5fVYAjjn5jwoQFT2KArkV9E8AjBjaM\n1KOzFp2z3QqfAgePu9aGmn/HVS42pte0iM/krnu/q+NydW6G5wtQgo7SQS8ky/X1\ned1UkLwPAgMBAAECggEAMpgnfngSmUa0tymAL1aWKjt7DtUTVKokkAL4DiFyk79m\n+BVvD2b2Ir3+rkcGpUw2ZZWYYuMTyiGTlzZS8Np6YKzquf+jCZ6UMVkKxiEliWLT\n6NqtsaqyRjwYLYFfDcr7yloNug1EoYz+mf90su+qYOa9f0ECAhpU6hREAvlyZJqh\nILjNDjDVn6m71QolbElG/4J/VtIvOIv6UXHl36SGhtzOE3iyGKAseTUKSK4VKT00\nJkwTlDvDgwdJ+RX1JP1HjGm9jMSW8elBT7LYvdXsOdfBqG4kUfKXt5bvkD9d9AM1\nlypjOvUiShjL/mZKdh/LyeIhc41BVGlZtful+IKbAQKBgQDHwAwkTH+m/U+RFexy\nNC4C0qKpp12Bp+k7sopIoWaaEA17YW+u99OdTP9JDDVEacVgp5O460PQIwo+cQho\nzBKep1WgRP9fffnJ6XMvcaM6OGIGQRGnL4yOEgKBtFsHjpeVPrvknZO9BY6JnX1f\nUNnIE8jhWO2XTWw7oTQ3UCCWkwKBgQDDlCethPemr3g2gtioeRNLVBzyk/yrEjiR\nG8DWDElNdgUnNr4GvEJjampoOtMN2QWTY2eRZY+2DHRC9b52he7zPW5lPJQlL8qY\ndMTjqJUzypvfCg2iWqLqdMxQjtespikpRAiOFu9rad3AHALjhLqr76XwVDRuWVJd\nlsD7vdVWFQKBgC5nfiqcnvczV92zwydQ2fOL7YAOQpnRYUyeEKQI4uYdnpQwMZrr\nNf0QGypkLKfFDraCl73Y4fsjeMjCx5pY9mZnJ2xBOzZ69KGkmz7FXo8y9ArR6QD2\n+eczZeOt+4vI44wnc80LknvSI6fyr2KKTN2/QuafGysQMHm13ISRF9EDAoGAIP8x\nBoyFf+Dg5kmDJkFvKOljDOY83dvwIUNOcI6YG3KLAgexXc+LX9yHYVhzXUW9NBW0\nVoqNCYjmYJm3baXBH9bAdmIXGIMMqlYhFcvOiHNpguLeVAL4s5fLFNhUuPM7xJOO\n4fIqqLOuzweq0RoGqJWBKJ/8TJXTWKjjnFV11dUCgYAVVGHgx8TXtW79i4xf5jDE\n+DaHdSOOMVico/0Ns2vlrPHzb4FZEx9PztnVzRijSNhePM80NkmggzPqPmIgFoY+\nKnPjAddyKRRhAIaxvCxImDIS7yL1zrTW/D3/gBuHbraIwFoYD4bu+ontHiQTMFp8\neQ4rkj7Hrw2XTdlr9n8YhQ==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-oz9ah@wifi-zones-1534d.iam.gserviceaccount.com",
        "client_id": "117091518928225553600",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-oz9ah%40wifi-zones-1534d.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com",
    }
)
firebase_admin.initialize_app(cred)


def send_notification(title, msg, devices):
    message = messaging.MulticastMessage(notification=messaging.Notification(title=title, body=msg), tokens=devices)

    response = messaging.send_each_for_multicast(message)

    logger.info(f"messaging response: {response}")
