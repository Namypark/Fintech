from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from .models import Account
from django.contrib import messages


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    """
    A signal handler that automatically creates an Account when a new User is registered. and saves it if the account is registered or updated
    """

    if created:
        """
        checks if account just got created
        then creates a user using the instance(user) that just registered
        prints a success message
        """
        Account.objects.create(user=instance, account_balance=0.00)
        print(instance)
        print("user account created successfully")
        instance.account.save()
        # messages.success("Account created successfully")
