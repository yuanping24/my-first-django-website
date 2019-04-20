from django.db import models
from django.utils import timezone

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='標題')
    keyword = models.TextField(blank=True, verbose_name='關鍵字')
    slug = models.SlugField(max_length=100, verbose_name='連結', unique=True)
    body = models.TextField(verbose_name='文章內容')
    readcount = models.IntegerField(verbose_name='閱讀次數', default = 0)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='發佈日期')

    class Meta:
        verbose_name = '部落格文章'
        verbose_name_plural = '部落格'
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title