from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from pure_pagination import Paginator, PageNotAnInteger

# Create your views here.
from django.views.generic import View

from courses.models import Course
from operation.models import CourseComment, UserFavorite


class CourseHomeView(View):
    """
    课程主页显示
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.order_by('-like_numbers')[:3]

        # 搜索功能
        search_keywors = request.GET.get('keywords', '')
        if search_keywors:
            all_courses = all_courses.filter(Q(name__icontains=search_keywors) | Q(desc__icontains=search_keywors) |
                                             Q(detail__icontains=search_keywors))

        # 对热门 / 参与人数排序
        key_word = request.GET.get('sort', '')
        if key_word:
            if key_word == 'hot':
                all_courses = all_courses.order_by('-like_numbers').all()
            elif key_word == 'students':
                all_courses = all_courses.all().order_by('-students')

        # 显示内容数量分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'key_word': key_word,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_numbers += 1
        course.save()
        relate_courses = Course.objects.filter(course_type=course.course_type).all()[:2]

        # 用户是否收藏该课程及课程机构标志
        has_fav_course = has_fav_organization = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_organization = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav': has_fav_course,
            'has_fav_organization': has_fav_organization,
        })


class CourseVideoView(View):
    """
    课程学习页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = course.lesson_set.all()
        relate_courses = Course.objects.filter(course_type=course.course_type).all()[:2]
        return render(request, 'course-video.html', {
            'course': course,
            'relate_courses': relate_courses,
            'lessons': lessons,
        })


class CourseCommentView(View):
    """
    课程评论页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        comments = course.coursecomment_set.all()
        # organization = course.o
        relate_courses = Course.objects.filter(course_type=course.course_type).all()[:2]
        return render(request, 'course-comment.html', {
            'course': course,
            'relate_courses': relate_courses,
            'comments': comments,
        })


class AddCommentView(View):
    """
    课程添加评论
    """
    def post(self, request):
        course_id = request.POST.get('course_id', '')
        course_comment = request.POST.get('comments', '')
        if not course_id and not course_comment:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}',
                                content_type='application/json')
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',
                                content_type='application/json')
        try:
            course = Course.objects.get(id=int(course_id))
            new_comment = CourseComment()
            new_comment.course = course
            new_comment.user = request.user
            new_comment.comment = course_comment
            new_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}',
                                content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}',
                                content_type='application/json')

