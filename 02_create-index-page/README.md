# 建立我們的首頁
## 關鍵字： django、CSS、html

2019年4月12日

還記得我們上次建立的首頁嗎？我們不可能永遠都只有一個Hello World的首頁。因此我們現在要做的，就是漂亮地顯示我們的首頁。

這邊會用到一些CSS和html的設定，都是為了讓我們的頁面更好看。在開始之前，我們首先要設定好我們的django，讓接著會用到的CSS等靜態檔案可以正確地呈現在首頁中。

### 一、設定django

#### 設定django後台admin的帳號及密碼

首先，我們按照上次的步驟，加載我們的虛擬開發環境，在cmd中輸入`django-venv\Scripts\activate`。然後切換到我們django網站的資料夾，`cd mysite`

接著輸入`python manage.py migrate`，將我們django網站中所有的models，在有任何變更時進行更新。在這裡執行後會將我們後台管理頁面所含的models匯入到django網站。

再來，輸入`python manage.py createsuperuser`就可以建立我們的後台管理者了。

![建立後台管理者](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/12/cmd-createsuperuser.png)

之後，我們使用`python manage.py runserver`開啟我們的網站伺服之後，在網址列輸入`http://127.0.0.1:8000/admin/`

使用剛剛建立的帳號和密碼登入，就可以看到下面的管理頁面了。

![後台管理頁面](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/12/django-admin-page.png)

未來我們還會 在這個後台進行更多網站的管理。

#### 修改django設定檔settings.py

接下來，我們要開始進行一些設定的修改，才能確保django知道我們靜態檔案所存放的位置。

在第二層的mysite資料夾中找到settings.py，這邊可以更改我們django網站的設定。在檔案最下面`# Internationalization`的部分，從這裡開始到最後，調整為
```
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
`LANGUAGE_CODE = 'zh-Hant'`，將我們的網站更改成以繁體中文顯示。

![中文後台登入頁](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/12/django-admin-zh-tw-login.png)

`TIME_ZONE = 'Asia/Taipei'`，調整我們網站的時區以台北時間為標準。

`STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]`，將我們網站會用到的靜態檔案，像是圖片、JavaScript、和CSS檔案，告訴django我們會放置於static這個資料夾中。

`MEDIA_URL`和`MEDIA_ROOT`的設定則是在日後網站使用者上傳檔案時，儲存這些檔案的位置。

為了讓MEDIA的檔案中可以被django網站找到，我們還必須修改mysite資料夾中的urls.py檔案。
```
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", blog.views.index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
先匯入`settings`和`static`兩個函數，然後在`urlpatterns`最後面加上我們的`MEDIA`設定。

### 二、修改首頁

#### 新增CSS和javascript檔案至static靜態檔案資料夾

可以從下面的圖中看到，右邊的網頁會比左邊的要來得精美些。這是因為我們有使用CSS的設定，來讓網頁有更好的排版和版面設計。

![CSS比較](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/12/css-comparison.png)

要達到這樣的效果很簡單，我們只要添加Bootstrap [https://getbootstrap.com/](https://getbootstrap.com/)到靜態文件資料夾中就可以了。

首先，在mysite資料夾中新增資料夾命名為static。接下來到[https://getbootstrap.com/docs/3.3/getting-started/#download](https://getbootstrap.com/docs/3.3/getting-started/#download)這邊下載壓縮檔，解壓縮到static資料夾中。我們在這個網站中所使用的是Bootstrap v3.3.7 版本。

除此之外，要正確地使用Bootstrap，還需要JQuery.js [https://jquery.com/](https://jquery.com/)。我們在這個網站中所使用的是JQuery v2.1.4版本，可以在這裡找到[https://code.jquery.com/jquery/](https://code.jquery.com/jquery/)。下載https://code.jquery.com/jquery-2.1.4.min.js這個檔案，放到static/js/中。

#### 修改首頁html

因為我們已經設定好settings.py，現在只需要在index.html檔案中寫好路徑，首頁就可以抓到static中的檔案，並讓我們的頁面更好看。

```
<!-- index.html -->
{% load static %}
<!DOCTYPE HTML>
<html lang="zh-Hant">
<head>
  <title>
     My First Django Website 
  </title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="description" content="我的第一個django網站" />
  <!-- Latest compiled and minified CSS -->
  <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet" type="text/css" media="all">
  <!-- Latest compiled and minified JavaScript -->
  <script type="text/javascript" src="{% static 'js/jquery-2.1.4.min.js' %}"></script>
  <script type="text/javascript" src="{% static 'js/bootstrap.min.js' %}"></script>
</head>
```

在上次我們建立的blog/templates/index.html中，以上面的內容做為開頭。

`{% load static %}`在django的html中，是宣告讀取靜態資料夾的資訊。然後`<link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">`就可以將我們的css和js檔案讀到網頁中了。

另外，`<meta name="viewport" content="width=device-width, initial-scale=1">`這個句子還可以判斷網頁瀏覽者所使用的是智慧手機還是一般電腦，然後以響應式網頁的形式，適當地顯示頁面。

如果需要自行設定其他的CSS內容，也可以添加至`<style> </style>`中。

```
  <style>
    body{
      font-family:Microsoft JhengHei;
      background: url(/static/images/wbp.png);
    }
  </style>
```

例如在這裡做的設定，將我們網頁的文字使用微軟正黑體的字體做顯示，以及指定網頁背景所使用的圖檔。

另外，因為這邊的網頁還會顯示一些程式代碼。因此還從[https://highlightjs.org/](https://highlightjs.org/)這裡下載了highlight.pack.js和railcasts.css。

```
<pre>
<code>def index(request):
    return render(request, "index.html")
</code>
</pre>
```

這樣子，上面的文字在網頁中就能以代碼的形式顯示出來。

![網頁中顯示代碼](https://github.com/yuanping24/yuanping24-django/blob/master/media/uploads/2019/04/12/code-in-page.png)

我們這一次透過一些CSS的應用，讓網頁能夠更鮮活地顯現出來，未來我們還會再提到更多CSS和html的部分。

下一次，我們會開始django中model的建立和應用。還會提及更多html的設置。
