from django.contrib import admin

# 管理者のインターフェースの設定
from .models import Question

admin.site.register(Question)