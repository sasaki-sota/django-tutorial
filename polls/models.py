import datetime

from django.utils import timezone
from django.db import models

# モデルの定義
class Question(models.Model):
    # CharField = 文字列フィールド
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    # ForeignKey = 1対多などを合わすことができるようになる
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    Choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text