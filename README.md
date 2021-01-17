# Djangoについて

※前提としてしっくりこない部分は理解が浅いので書きません :shit:

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

## 管理者ユーザーの作成¶
    $ python manage.py createsuperuser
このコマンドで自動で作れる  
`http://127.0.0.1:8000/admin/` のURLを叩くと入れる

管理者画面でPOLLSを追加
polls/admin.pyを使用することで追加することができる

    from django.contrib import admin

    # 管理者のインターフェースの設定
    from .models import Question
    
    admin.site.register(Question)

##### ※管理者画面の設定はモデルに依存するなど困ったらドキュメントを読む

ここまでのドキュメント  
https://docs.djangoproject.com/en/3.1/intro/tutorial02/

## 詳細画面

    def detail(request, question_id):
        return HttpResponse("You're so in my happy %s" % question_id)

とrailsでいうコントローラ(views.py)に記述し、

    path('<int:question_id>/', views.detail, name='detail'),

山かっこを使用すると、  
URLの一部が「キャプチャ」され、キーワード引数としてビュー関数に送信
***これであとはviewの部分を用意すれば完了**

### indexのviews

    {% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}

と**template側**に記述(railsのview)

ここまでのドキュメント  
https://docs.djangoproject.com/ja/3.1/intro/tutorial03/

### コントローラー側の作成

    from django.shortcuts import render

    from .models import Question
    
    
    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)

### 404の発生方法

    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question})

このように**get_object_or_404**メソッドを使用するだけなので超楽！

### 投稿の実装

投稿できるようにformのビューを作成する

    <h1>{{ question.question_text }}</h1>

    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    
    <form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
    <input type="submit" value="Vote">
    </form>

コントローラー側の部分

    def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'それは選べないよん',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # データが二重に投稿されることを防ぎます
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

エラーメッセージのところはしっかりと復習する必要がある

## 汎用ビューにする

    from django.urls import path

    from . import views
    
    app_name = 'polls'
    urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        # pkでいける(もともとpkで平気)
        path('<int:pk>/', views.DetailView.as_view(), name='detail'),
        path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]

と変更し、それぞれのビューコントローラも

    class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


    class DetailView(generic.DetailView):
        model = Question
        template_name = 'polls/detail.html'
    
    
    class ResultsView(generic.DetailView):
        model = Question
        template_name = 'polls/results.html'

とする。  
-> すごくわかりやすくなる

汎用ビューのドキュメント  
https://docs.djangoproject.com/ja/3.1/topics/class-based-views/

ここまでのドキュメント  
https://docs.djangoproject.com/ja/3.1/intro/tutorial04/

## モデル部分のテスト

    import datetime

    from django.test import TestCase
    from django.utils import timezone
    
    from polls.models import Question
    

    # 未来の日付の pub_date を持つ Question のインスタンスを生成するメソッドを持つ django.test.TestCase を継承したサブクラスを作っています。
    # それから、was_published_recently() の出力をチェック
    class QuestionModelTests(TestCase):
        def test_was_published_recently_with_future_questions(self):
            time = timezone.now() + datetime.timedelta(days=30)
            future_question = Question(pub_date=time)
            self.assertIs(future_question.was_published_recently(), False)
    
        # 過去のテスト    
        def test_was_published_recently_with_old_question(self):
            time = timezone.now() - datetime.timedelta(days=1, seconds=1)
            old_question = Question(pub_date=time)
            self.assertIs(old_question.was_published_recently(), False)
    
        def test_was_published_recently_with_recent_question(self):
            time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
            recent_question = Question(pub_date=time)
            self.assertIs(recent_question.was_published_recently(), True)

これで現在、過去、未来のテストをすることができるようになる  
-> これを行うことでメソッドの完成を保証する

テスト部分は記事が多いのでドキュメントを参照  
https://docs.djangoproject.com/ja/3.1/intro/tutorial05/  

