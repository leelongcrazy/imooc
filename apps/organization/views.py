from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View

from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CourseOrg, Cities, Teacher


class OrgListView(View):
    def get(self, request):
        orgs = CourseOrg.objects.all()
        cities = Cities.objects.all()

        # 授课机构点击量降序排名
        ordered_orgs = orgs.order_by('-click_num')[:3]

        # 添加机构搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            orgs = orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 机构类别筛选
        org_type = request.GET.get('ct', '')
        if org_type:
            orgs = orgs.filter(org_type=org_type)

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            orgs = orgs.filter(city_id=int(city_id)).all()

        # 对学习人数/课程数量降序排列
        key_word = request.GET.get('sort', '')
        if key_word == 'students':
            orgs = orgs.order_by('-students')
        elif key_word == 'courses':
            orgs = orgs.order_by('-course_nums')
        else:
            pass

        orgs_nums = orgs.count()  # 筛选后数量统计

        # 显示内容数量分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(orgs, 5, request=request)

        org = p.page(page)

        return render(request, 'org-list.html', {
            'orgs': org,
            'cities': cities,
            'orgs_nums': orgs_nums,
            'city_id': city_id,
            'org_type': org_type,
            'ordered_orgs': ordered_orgs,
            'key_word': key_word,
        })


class UserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        # print('<<<<<<<<<<<<<<<<<<')
        # print(dir(user_ask_form))
        # print('<<<<<<<<<<<<<<<<<<')
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return HttpResponse('{"status":"success", "msg":"信息已经成功提交"}',
                                content_type='application/json')

        else:
            return HttpResponse('{"status":"fail", "msg":"数据保存失败"}',
                                content_type='application/json')


class OrgHomeView(View):
    """
    课程机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'

        org_courses = CourseOrg.objects.get(id=int(org_id))

        # 课程机构点击量增加
        org_courses.click_num += 1
        org_courses.save()

        all_courses = org_courses.course_set.all()[:3]
        all_teachers = org_courses.teacher_set.all()[:2]

        has_fav = False  # 当前已登录用户是否收藏该课程机构的标志
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_courses.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'org_courses': org_courses,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        org_courses = CourseOrg.objects.get(id=int(org_id))
        all_courses = org_courses.course_set.all()

        has_fav = False  # 当前已登录用户是否收藏该课程机构的标志
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_courses.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'org_courses': org_courses,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        org_courses = CourseOrg.objects.get(id=int(org_id))

        has_fav = False  # 当前已登录用户是否收藏该课程机构的标志
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_courses.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'org_courses': org_courses,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeachView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        org_courses = CourseOrg.objects.get(id=int(org_id))
        all_teachers = org_courses.teacher_set.all()

        has_fav = False  # 当前已登录用户是否收藏该课程机构的标志
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_courses.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'org_courses': org_courses,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgUserFavoriteView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')
        if not fav_id or not fav_type:
            return HttpResponse('{"status":"fail", "msg":"收藏出错"}',
                                content_type='application/json')
        has_login = request.user.is_authenticated()
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',
                                content_type='application/json')
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if not exist_record:
            # 如果记录不存在，则添加收藏
            new_record = UserFavorite()
            new_record.user = request.user
            new_record.fav_id = int(fav_id)
            new_record.fav_type = int(fav_type)
            new_record.save()
            return HttpResponse('{"status":"success", "msg":"已收藏"}',
                                content_type='application/json')
        else:
            # 删除收藏
            exist_record.delete()
            return HttpResponse('{"status":"fail", "msg":"取消收藏"}',
                                content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 人气排序
        key_word = request.GET.get('sort', '')
        if key_word:
            all_teachers = all_teachers.order_by('-click_num')

        # 讲师排行榜
        top_teachers = all_teachers.order_by('-click_num')[:3]

        # 添加老师搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(org__teacher__work_company__icontains=search_keywords)\
                | Q(work_company__icontains=search_keywords))

        # 显示内容数量分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)

        teachers = p.page(page)

        return  render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'top_teachers': top_teachers,
            'key_word': key_word,
        })
