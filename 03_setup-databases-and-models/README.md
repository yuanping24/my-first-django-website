# 設定資料庫和建立django model
## 關鍵字： django、PostgreSQL

2019年4月20日

今天我們要開始建立django中的model。在django架構中，主要由MTV所組成。其中Template負責網頁的顯示，View負責資料、程式、邏輯的處理。我們在上次有看過這兩部分簡單的範例。剩下的Model，主要負責資料的儲存和內容。在開始使用model之前，我們會先介紹一下資料庫的部分，以及在django中如何串接資料庫。

### 一、選擇和建立資料庫

#### 資料庫介紹：SQLite、MySQL、PostgreSQL

一般常見的資料庫主要有SQLite、MySQL、PostgreSQL，在django中都有支援。django預設使用的是SQLite。SQLite的好處是所佔容量小和移轉方便。但是在安全性上沒有任何保護，任何人只要取得我們的SQLite資料庫，就能直接讀取裡面的資料。因此大部分是在測試階段中才會使用SQLite。

MySQL是這三種資料庫中擁有最多的使用者和開放資源，速度也是最快的。不過缺點是更新的開發速度較慢，並沒有兼容全部的SQL標準。另外，如果當網站有很多使用者需要同時寫入資料時，MySQL的表現也不盡理想。

PostgreSQL具有非常好的可擴性。由於完全開源，可以在網路上找到很多的資源。和MySQL相比，也有較多的SQL兼容性。但是在記憶體的分配上表現較差，速度沒有比MySQL快。

如果要確保資料庫的安全性，MySQL和PostgreSQL都是和SQLite相比較好的選擇。由於之後選擇發佈的網站直接支援PostgreSQL，因此接下來會介紹PostgreSQL的設定。

#### 設定PostgreSQL

首先，我們必須先在本機端裝設PostgreSQL的伺服器。在[https://www.postgresql.org/download/](https://www.postgresql.org/download/)可以找到符合作業系統的安裝檔或安裝方式。

作業系統是windows的使用者，可以在[https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)這裡找到安裝檔。但是要注意，如果是windows 10的版本，目前這邊的安裝檔只有測試到PostgreSQL 10的版本。

![PostgreSQL在Windows中支援版本](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/20/postgresql-support-version.png)

完裝下載後，在安裝過程中會需要輸入資料庫密碼，請記得所輸入的密碼，我們接下來會在django的設定檔中用到。

安裝完成後，PostgreSQL的伺服器就會自動運行了。或是我們可以開啟pgAdmin來檢視我們的伺服器或是進行任何的修改。

![PostgreSQL伺服器](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/20/postgresql-server-pgadmin.png)

在除了密碼外，沒有進行任何PostgreSQL變更的情況下，我們在django中的settings.py修改如下。
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
將DATABASES的資料庫ENGINE從改為sqlite3改為postgresql，在資料庫的名字、使用者、密碼、和連接埠，如果在資料庫伺服器中有做修改，這邊需要做適當的調整。例如，我的資料庫名字和使用者名稱都是預設的postgres，而使用者的密碼是123，連接埠則是5432。

另外，我們還需安裝Psycopg2，才能正確地讓django使用PostgreSQL資料庫。`pip install psycopg2`

接著啟動我們網站的伺服器，看看是不是有正常運作。

![安裝Psycopg2](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/20/install-psycopg2.png)

雖然可以執行我們的首頁，但是在[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)要登入時，卻會發生錯誤。

這是因為，我們之前所使用的SQLite資料庫中所包含的admin資料，並沒有被轉移到新的PostgreSQL資料庫。

雖然有兩個資料庫之間轉移的方法，但是因為目前我們的資料庫還沒有太多的使用。因此只需重新再建立一次admin帳號即可。`python manage.py migrate`，`python manage.py createsuperuser`

![更新migrate和建立使用者](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/20/migrate-createsuperuser.png)

在這之後，原本資料夾中的db.sqlite3檔案，就不需要再保留，可以刪除了。

接下來，我們就要正式開始建立django中的model。

### 二、建立model

首先，在我們之前建立的blog資料夾中，找到models.py和admin.py這兩個檔案。接下來，我們透過修改這兩個檔案，來增加model，以及讓這個model可以透過django的後台顯示。

#### models.py

```
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
```
我們在models.py中，建立一個部落格文章的model。這個model中，包含了文章的標題、關鍵字、連結、內容、閱讀次數、和發佈日期。此外，我們還設定文章排序以較新發佈的文章排在前面。

#### admin.py
```
from django.contrib import admin
from .models import BlogPost
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'keyword', 'slug', 'readcount', 'pub_date')

admin.site.register(BlogPost, PostAdmin)
```
為了讓admin後台中找到我們剛建好的model，必須設定我們的admin.py。其中，在後台的文章列表中，顯示文章的標題、關鍵字、連結、閱讀次數、和發佈日期。至於內容就等點選進去後，才會看到。

都設定好之後，執行`python manage.py makemigrations`和`python manage.py migrate`，將新的model更新到django中。

![執行makemigations](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/20/makemigrations-migrate.png)

到後台管理介面[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)，就可以看到剛建立的部落格了。之後可以在這裡新增我們的部落格文章。

![後台添加部落格文章](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/20/admin-with-blog.png)

下一次，我們將修改views.py，讓在後台新增的文章，顯示在網頁中。