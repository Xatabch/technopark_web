from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(QuestionLike)
admin.site.register(QuestionDislike)
admin.site.register(AnswerLike)
admin.site.register(AnswerDislike)
