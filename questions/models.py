# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Count


class UserManager(UserManager):
    def all_users(self):
        return self.all()

    def best_users(self):
        return self.annotate(num_users=Count('answerlike')).order_by("-num_users")[:10]

    def create_user(self, login, email, nickname, password=None, photo=None):
        if not login:
            raise ValueError('У пользователья должен быть логин!')

        user = self.model(
            username=login,
            email=email,
            nickname=nickname,
            upload=photo

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def edit_user(self, user, login=None, email=None, nickname=None, photo=None):

        if email != '':
            user.email = email
        if nickname != '':
            user.nickname = nickname
        if photo:
            user.upload = photo

        user.save()

        return user


class User(AbstractUser):  # Profile в ТЗ
    objects = UserManager()
    upload = models.ImageField(upload_to='uploads/%Y/%m/%d', default='uploads/default_image.jpg')
    nickname = models.CharField(max_length=100)


class TagManager(models.Manager):
    def all_tags(self):
        return self.all()

    def best_tags(self):
        return self.annotate(num_tags=Count('question')).order_by("-num_tags")[:10]

    def get_tag_by_name(self, name):
        return self.get(title=name)

    def create_tag(self, title):
        tag = self.model(
            title=title
        )

        tag.save()

        return tag


class Tag(models.Model):
    objects = TagManager()
    title = models.CharField(max_length=50, verbose_name=u"Тэги")

    def __str__(self):
        return self.title


class QuestionManager(models.Manager):

    def get_absolute_url(self, id):
        return "/question/%i/" % id

    def all_questions(self):
        return self.all()

    def get_question_by_id(self, id):
        return self.annotate(num_likes=Count('questionlike', distinct=True),
                             num_dislikes=Count('questiondislike', distinct=True)).get(id=id)

    def get_questions_by_tag(self, tagname):
        tag = Tag.objects.get(title=tagname)
        result = self.filter(tags=tag).annotate(num_likes=Count('questionlike', distinct=True),
                                                num_dislikes=Count('questiondislike', distinct=True),
                                                num_answers=Count("answer", distinct=True))

        return result

    def get_question_by_popular(self):
        return self.all().annotate(num_likes=Count('questionlike', distinct=True),
                                   num_dislikes=Count('questiondislike', distinct=True),
                                   num_answers=Count("answer", distinct=True)).order_by('-num_likes')[:10]

    def get_question_by_date(self):
        return self.all().annotate(num_likes=Count("questionlike", distinct=True),
                                   num_dislikes=Count("questiondislike", distinct=True),
                                   num_answers=Count("answer", distinct=True)).order_by("-create_date")

    def create_question(self, author, title, text, tags):
        question = self.model(
            author=author,
            title=title,
            text=text,
        )

        question.save()

        tag = tags.split(',')
        tags_for_filter = [tag[i].split(' ') for i in range(len(tag))]

        if tags_for_filter:
            for t in tags_for_filter:
                for j in t:
                    if j != '':
                        try:
                            new_tag = Tag.objects.get_tag_by_name(j)
                        except:
                            new_tag = Tag.objects.create_tag(j)

                        question.tags.add(new_tag)

        return question


class Question(models.Model):
    objects = QuestionManager()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("question", "user"),)


class QuestionDislike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AnswerManager(models.Manager):
    def all_answers(self):
        return self.all()

    def get_answers_by_id(self, id):
        return self.filter(question__id=id).annotate(num_likes=Count('answerlike', distinct=True),
                                                     num_dislikes=Count("answerdislike", distinct=True))

    def get_absolute_url(self, question, answer):
        return "/question/%i/?page=%i" % (question.id, answer.paginator.num_pages)

    def create_answer(self, author, question, text):
        answer = self.model(
            author=author,
            question=question,
            text=text,
        )

        answer.save()

        return answer


class Answer(models.Model):
    objects = AnswerManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(verbose_name=u"Текст вопроса")
    is_correct = models.BooleanField(default=False, verbose_name=u"Корректность вопроса")

    def __str__(self):
        return self.text


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AnswerDislike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
