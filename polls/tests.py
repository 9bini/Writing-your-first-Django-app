import datetime
from django.http import response

from django.test import TestCase
from django.utils import timezone

from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    # text로 시작하는 메소드를 찾기 때문에 앞에 test작성하는 것을 잊지말자
    def test_was_published_recently_with_future_question(self):
        """
        미래의 질문이기 때문에 false 반환
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        하루가 지난 질문이기 때문에 false 반환
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        하루가 지나기전 잘문이기 때문에 ture 반환
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        
def create_question(question_text, days):
    """
        days가 과거의 질문일 경우 음수
                미래의 질문은      양수이다.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        질문이 없을 때 적절한 메시지 출력하는지 테스트
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        질문에 pub_date가 과거일 경우 색인 페이지에 표시되는지 테스트
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    def test_future_question(self):
        """
         질문에 pub_date가 미래일 경우 색인 페이지에 표시않되는지 테스트
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")

    def test_future_question_and_past_question(self):
        """
        과거 및 미래 질문이 모두 존재하더라도 과거 질문만 표시됩니다.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    def test_two_past_questions(self):
        """
        과거 질문이 여러개 일경우
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        아직 게시되지않는 게시판에 접근시 404 not found가 리턴하는지 테스트
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        과거 질문이 표시될 수 있는지 테스트
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)