from django.db import models
from django.contrib.auth.models import User


class RelationshipManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # don't delete client if RM is deleted
    relationship_manager = models.ForeignKey(
        RelationshipManager,
        models.SET_NULL,
        blank=True,
        null=True,
    )


class Document(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "user_{0}/{1}".format(instance.client.user.id, filename)

    name = models.CharField(max_length=150)
    file = models.FileField(upload_to=user_directory_path, null=True)
    valid = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
