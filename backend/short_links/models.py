from django.db import models
import hashlib


class LinkPair(models.Model):
    original_link = models.CharField(primary_key=True, verbose_name='Оригинальная ссылка')
    short_link = models.CharField(verbose_name='Прямая ссылка')

    def save(self, *args, **kwargs):
        token = hashlib.shake_256(
            self.original_link.encode()
        ).hexdigest(3)
        self.short_link = f'/s/{token}/'
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
    
    class Meta:
        verbose_name = 'Пара ссылок'
        verbose_name_plural = 'Пары ссылок'