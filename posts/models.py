from django.db import models

from accounts.models import Profile


def tweet_image_store(instance, filename):
    return f"profile/{instance.profile.user.username}/{instance.created_at}/{filename}"


class Tweet(models.Model):
    text = models.CharField(max_length=140)
    image = models.ImageField(upload_to=tweet_image_store, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self):
        return self.text
