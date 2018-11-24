from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from questions.models import User, Tag, Question, QuestionLike, Answer, AnswerLike, QuestionDislike, AnswerDislike
import random


class Command(BaseCommand):
    help = "This command fills existing tables in your data base"

    def handle(self, *args, **options):
        self.create_tags()
        self.create_users()
        self.create_questions()
        self.create_question_likes()
        self.create_question_dislikes()
        self.create_answers()
        self.create_answer_likes()
        self.create_answer_dislikes()

    def create_users(self):
        if User.objects.count() > 9:
            return
        faker = Faker()
        for i in range(10):
            user = User()
            user.first_name = faker.first_name()
            user.last_name = faker.last_name()
            user.password = "12345"
            user.username = user.first_name + user.last_name
            user.save()

    def create_tags(self):
        if Tag.objects.count() > 10:
            return
        faker = Faker()
        random_tags = faker.words(nb=10, ext_word_list=None)
        for tag in random_tags:
            t = Tag()
            t.title = tag
            t.save()
            # self.stdout.write('add tag [%s]' % tag)

    def create_questions(self):
        if Question.objects.count() > 99:
            return

        fake = Faker()
        tags_set = Tag.objects.all()
        author_set = User.objects.all()
        print()
        for i in range(100):
            post = Question()
            post.author = random.choice(author_set)
            post.title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            post.text = fake.text(max_nb_chars=100, ext_word_list=None)
            post.create_date = fake.date(pattern="%Y-%m-%d", end_datetime=None)
            post.id = i
            post.save()

            for j in range(3):
                t = random.choice(tags_set)
                post.tags.add(t)
                # self.stdout.write('add tag [%s] in article [%d]' % (t, i))

            # self.stdout.write('add article [%d]' % post.id)

    def create_question_likes(self):
        if QuestionLike.objects.count() > 1000:
            return

        question_set = Question.objects.all_questions()
        user_set = User.objects.all_users()
        pairs = []
        temp = [0, 0]
        j = 0
        for i in range(Question.objects.count()):
            like = QuestionLike()
            like.question = random.choice(question_set)
            like.user = random.choice(user_set)
            temp[0] = like.question
            temp[1] = like.user
            if temp not in pairs:
                pairs.append([])
                pairs[j].append(like.question)
                pairs[j].append(like.user)
                like.save()
                j += 1

    def create_question_dislikes(self):
        if QuestionDislike.objects.count() > 1000:
            return

        question_set = Question.objects.all_questions()
        user_set = User.objects.all_users()
        pairs = []
        temp = [0, 0]
        j = 0

        for i in range(Question.objects.count()):
            dislike = QuestionDislike()
            dislike.question = random.choice(question_set)
            dislike.user = random.choice(user_set)
            temp[0] = dislike.question
            temp[1] = dislike.user
            if temp not in pairs:
                pairs.append([])
                pairs[j].append(dislike.question)
                pairs[j].append(dislike.user)
                dislike.save()
                j += 1

    def create_answers(self):
        if Answer.objects.count() > 99:
            return

        faker = Faker()

        question_set = Question.objects.all()
        author_set = User.objects.all()

        for i in range(100):
            answer = Answer()
            answer.author = random.choice(author_set)
            answer.question = random.choice(question_set)
            answer.text = faker.text(max_nb_chars=200, ext_word_list=None)
            try:
                answer.save()
            except:
                print("Повторился пользователь с вопросом")

    def create_answer_likes(self):
        if AnswerLike.objects.count() > 1000:
            return

        answer_set = Answer.objects.all_answers()
        user_set = User.objects.all_users()
        pairs = []
        temp = [0, 0]
        j = 0

        for i in range(Answer.objects.count()):
            like = AnswerLike()
            like.answer = random.choice(answer_set)
            like.user = random.choice(user_set)
            temp[0] = like.answer
            temp[1] = like.user
            if temp not in pairs:
                pairs.append([])
                pairs[j].append(like.answer)
                pairs[j].append(like.user)
                like.save()
                j += 1

    def create_answer_dislikes(self):
        if AnswerDislike.objects.count() > 1000:
            return

        answer_set = Answer.objects.all_answers()
        user_set = User.objects.all_users()
        pairs = []
        temp = [0, 0]
        j = 0

        for i in range(Answer.objects.count()):
            dislike = AnswerDislike()
            dislike.answer = random.choice(answer_set)
            dislike.user = random.choice(user_set)
            temp[0] = dislike.answer
            temp[1] = dislike.user
            if temp not in pairs:
                pairs.append([])
                pairs[j].append(dislike.answer)
                pairs[j].append(dislike.user)
                dislike.save()
                j += 1
