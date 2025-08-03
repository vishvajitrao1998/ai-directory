import datetime
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_application_reference(prefix="APP", length=8):
    """
    Generates a unique application reference number of ai tool.

    Args:
        prefix (str): A string prefix for the reference number (e.g., "APP", "ORD").
        length (int): The desired length of the random alphanumeric suffix.

    Returns:
        str: A unique application reference number.
    """
    # Get current timestamp for uniqueness
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate a random alphanumeric suffix
    characters = string.ascii_uppercase + string.digits
    random_suffix = ''.join(random.choice(characters) for _ in range(length))

    # Combine prefix, timestamp, and random suffix
    reference_number = f"{prefix}-{timestamp}-{random_suffix}"
    return reference_number


def send_mail(recepient, ref_number, username, email_type):
    try:
        html_content = render_to_string('admin_notify.html', {'ref_number': ref_number, "username": username, 'email_type': email_type})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject='🎉 Welcome to Our Platform',
            body=text_content,
            from_email='vishvajitrao@gmail.com',         # Replace with your sender email
            to=[recepient]                             # Assumes your model has `email` field
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        return False

