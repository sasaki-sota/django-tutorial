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

## モデルの作成方法とデータベースの更新
##### 更新コマンド

    $ python manage.py migrate
とする。  
  
##### モデルの作成
models.py

    from django.db import models


    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
    
    
    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)
とすることで**Question**と**Choice**のモデルの作成 -> 

プロジェクトの`sample/settings.py`についか  

    INSTALLED_APPS = [
        'polls.apps.PollsConfig',
    ]
を追加 ->  

アプリごとのデータベースの更新

    $ python manage.py makemigrations polls

スキーマのように確認する方法

    $ python manage.py sqlmigrate polls 0001
とすれば大丈夫だが、  
注意としてターミナル上に表示されるだけでフォーマットを整える必要あり

その後、更新　→　railsと同じでmigrationファイルを作成したら更新する
    
    $ python manage.py migrate

##### rails consoleの部分

    $ python manage.py shell
とするとコンソールモードになる

    >>> from polls.models import Choice, Question  # Import the model classes we just wrote.
    >>> Question.objects.all()
    <QuerySet []>
    >>> from django.utils import timezone
    >>> q = Question(question_text="What's new?", pub_date=timezone.now())
    >>> q.save()
    >>> q.id
    1
    >>> q.question_text
    "What's new?"
    >>> q.pub_date
    datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)
    >>> q.question_text = "What's up?"
    >>> q.save()
    >>> Question.objects.all()
    <QuerySet [<Question: Question object (1)>]>
と確認することができる。

その他の確認はドキュメントで
https://docs.djangoproject.com/en/3.1/intro/tutorial02/