from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


"""
def index(request)는 polls/index.html 템플릿을 불러온 후, context를 전달합니다. 
context는템플릿에서 쓰이는 변수명과 파이썬 객체를 연결하는 사전형 값입니다.
"""
# render 적용 전
"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
"""

# render 적용 후
"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# get_object_or_404() 적용 전
"""
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
"""

# get_object_or_404() 전용 후
"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
"""

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

"""
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    # pk가 변수 question_id인 튜플이 없을 경우 에러 발생
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 요청한 form 데이터를 request.POST['choice'] 이런 형태으로 불러오네
            # 요청 매서드가 get일 경우 request.GET으로 접근 가능하다.  
            
        # pk=question_id인 질문에 관계된 선택 중 pk=request.POST['choice'](초이스 기본키)인 것을 조회
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # KeyError는 request.POST['choice']가 없을 경우 확인
        # Choice.DoesNotExist는 조회한 데이터가 없는 경우 확인
    except (KeyError, Choice.DoesNotExist):
        # detail 페이지를 다시 보여준다.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # 경쟁 상태 문제를 가지고 있다.
        selected_choice.votes += 1
        selected_choice.save()
        # post 데이터를성공적으로 처리한후 HttpResponseRedirect를 항상 반환해야한다
        # reverse사용자가 재전송될 URL
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
