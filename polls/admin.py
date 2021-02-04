# 기본적으로 페이징 기능 제공
from django.contrib import admin

# 관련된 객체를 추가하려면 해당 객체를 import 해야됨!
from .models import Question, Choice

# StackedInline => TabularInline
class ChoiceInline(admin.TabularInline):
    model = Choice
    # 기본적으로 3가지 선택 항목을 제공
    # 초이스 객체가 n개 있으면 추가로 3가지 선택 항목제공
    extra = 3

# admin 클래서 생성 -> admin.site.register() 두번째 인수로 전달
class QuestionAdmin(admin.ModelAdmin):
    # 발행일(pub_date), 설문(question_text) 순으로 필드 앞에 오게 만듭니다.
    # fileds = ['pub_date', 'question_text']
    fieldsets = [
        # fieldsets 첫 번째 인자(None, 'Date information')는 제목을 의미한다.
        (None,               {'fields': ['question_text']}),
        # classes???
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    # 기본적으로 __str__을 표시합니다.
    # 개별 필드를 표시 할 수 있는 경우 가끔 도움이 될 수 있습니다.
    # list_displays는 객체의 변경 목록 페이지에서 열로 표시 할 파두 아름들의 튜플입니다.
    # was_published_recently 임의이 메소드의 출력에 의한 정렬은 지원되지 않는다.
    # 그외에는 정렬을 지원한다.
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date'] # 데이터 필터링
    search_fields = ['question_text'] # 필드 검색(like)

admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)