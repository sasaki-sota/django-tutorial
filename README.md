# Djangoについて

viewsを作成してから`urls.py`の作成  

## URL
まず、作成したアプリケーションの**polls**の方にurlの部分を追加してから  

    urlpatterns = [
    path('', views.index, name='index'),
    ]
と記述し、プロジェクト側の**sample**の方に

        path('polls/', include('polls.urls'))
と記述する。

##### ここの部分のドキュメント
https://docs.djangoproject.com/en/3.1/intro/tutorial01/  

