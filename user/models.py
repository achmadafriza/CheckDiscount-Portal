from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

# Actually, maybe i need to detail the permissions and group them.
    class Meta:
        permissions = (
            ("is_admin", "Can use CRUD portal."),
            ("can_use_dashboard", "Can use Dashboard that sees Log and API Graph"),
            ("can_see_log", "Can see API and Transaction Logs"),
            ("can_make_transaction", "Can make Transactions to API")
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("signal is procced")
        Profile.objects.create(user=instance)

        instance.is_active = False
        instance.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()