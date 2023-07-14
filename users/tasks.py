import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id: uuid.UUID) -> None:
    hours_to_expiration = 48

    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=hours_to_expiration)
    record = EmailVerification.objects.create(code=uuid.uuid4(),
                                              user=user,
                                              expiration=expiration)
    record.send_verification_email()
