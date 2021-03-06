from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from account_management.models import Account
from _helpers.db import TimeModel


class BookAd(TimeModel):
    SALE = 'sale'
    BUY = 'buy'

    AD_CHOICES = (
        (SALE, 'فروش'),
        (BUY, 'خرید'),
    )
    AD_KINDS = tuple(dict(AD_CHOICES).keys())

    APPROVED = 'approved'
    DISAPPROVED = 'disapproved'
    PENDING = 'pending'

    STATUS_CHOICES = (
        (APPROVED, 'تایید شده'),
        (DISAPPROVED, 'رد شده'),
        (PENDING, 'در انتظار')
    )
    STATUS_KINDS = tuple(dict(STATUS_CHOICES).keys())

    poster = models.ImageField(verbose_name="تصویر", upload_to='ad_posters/', null=True, blank=True, )
    title = models.CharField(verbose_name="نام کتاب", max_length=30)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='نویسنده')
    description = models.TextField(verbose_name="توضیحات", max_length=500)
    ad_type = models.CharField(verbose_name="نوع درخواست", choices=AD_CHOICES, default=SALE, db_index=True, max_length=20)
    price = models.IntegerField(verbose_name="قیمت", default=20000)
    authorName = models.CharField(verbose_name='نام نویسنده', default='بی‌نام', max_length=30)
    status = models.CharField(verbose_name='وضعیت', choices=STATUS_CHOICES, default=PENDING, max_length=20)

    def __str__(self):
        return str(self.title) + ' / ' + str(self.authorName)

    def get_absolute_url(self):
        return reverse('ad', kwargs={'pk': self.pk})

    def clean(self):
        if self.poster and self.ad_type == self.BUY:
            raise ValidationError("posters are not allowed for buy advertisements")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BookAd, self).save(*args, **kwargs)
