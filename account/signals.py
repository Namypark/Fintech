from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Account
from userAuth.models import User
from django.contrib import messages


@receiver(post_save, sender=User)
def create_save_account(sender, instance, created, **kwargs):
    """
    A signal handler that automatically creates an Account when a new User is registered. and saves it if the account is registered or updated
    """

    if created or instance.account is None:
        Account.objects.create(user=instance)
        print(instance)
        print("Account created successfully")

    else:
        # If the user already has an associated account, save it
        instance.account.save()
        print(instance)
        print("Account saved successfully")


# # @receiver(post_delete, sender=User)
# # def delete_user(sender, instance, **kwargs):
# #     """
# #     Delete an account from the database and alert the user.
# #     """
# #     # Check if the deletion was initiated by an admin user
# #     if instance != instance.account.user:
# #         print(instance)
# #         # Get the associated account
# #         account = instance.account if hasattr(instance, "account") else None

# #         if account:
# #             # Delete the account from the database
# #             account.delete()

# #             # Alert the user
# #             if instance == instance.account.user:
# #                 print(instance)
# #                 messages.info(instance, "Your account has been deleted.")
# #             else:
# #                 messages.info(instance, "An admin user has deleted your account.")
