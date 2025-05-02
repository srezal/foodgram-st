from django.db import models
import hashlib


class LinkPair(models.Model):
    original_link = models.CharField()
    short_link = models.CharField()
    pk = models.CompositePrimaryKey("original_link", "short_link")

    def save(self, *args, **kwargs):
        token = hashlib.shake_256(
            self.original_link.encode()
        ).hexdigest(3)
        self.short_link = f'/{token}/'
        super().save(*args, **kwargs)

    @classmethod
    def get_or_create_short_link(cls, original_link):
        try:
            link_pair = cls.objects.get(original_link=original_link)
            return link_pair.short_link
        except cls.DoesNotExist:
            pass
        link_pair = cls.objects.create(
            original_link=original_link
        )
        link_pair.save()
        return link_pair.short_link