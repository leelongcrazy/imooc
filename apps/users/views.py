import json

import django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from .email_verify.send_email import send_register_email
from .forms import LoginForm, RegisterForm, ForgetForm, ResetForm, UserImageForm, UserInfoForm
from .models import UserInfo, EmailVerifyRecord, PictureBanner


#  重写用户验证
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class HomeView(View):
    def get(self, request):
        all_banners = PictureBanner.objects.all().order_by('index')
        part_of_courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True).order_by('click_numbers')[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'part_of_courses': part_of_courses,
            'all_banners': all_banners,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class LoginOutView(View):
    """
    用户退出登录操作
    """
    def get(self, requtest):
        logout(request=requtest)
        return HttpResponseRedirect(reverse('home'))


# 基于类的方法来处理用户登录验证
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)  # form表单对象实例化
        if login_form.is_valid():  # 判断表单是否有效
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return render(request, 'login.html', {'msg': "请先激活您的帐号", 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': "注意检查用户名或密码是否有错误..."})
        else:
            return render(request, 'login.html', {'login_form': login_form})  # login_form对象内包含错误信息，可将错误信息输出到前端


# 基于函数的方法来处理用户登录验证
def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        user = authenticate(username=user_name, password=pass_word)
        if user:
            login(request, user)
            return render(request, 'index.html', {})
        else:
            return render(request, 'login.html', {'msg': "注意检查用户名或密码是否有错误..."})

        pass
    elif request.method == 'GET':
        return render(request, 'login.html', {})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            new_user = UserInfo()
            new_user.username = user_name
            new_user.email = user_name
            new_user.password = make_password(password=pass_word)
            try:
                new_user.save()
                return render(request, 'login.html', {'msg': "注册账户成功，请登录..."})
            except django.db.utils.IntegrityError as e:
                return render(request, 'login.html', {'msg': "注册账户已经存在，请直接登录..."})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                user = UserInfo.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            user = UserInfo.objects.filter(email=email)
            if user:
                send_register_email(email, send_type='forget')
                return render(request, 'send_email_successful.html')
            else:
                return render(request, 'forgetpwd.html', {'msg': "该用户不存在"})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    """
    用户密码重设邮箱验证
    """

    def get(self, request, reset_code):
        email = EmailVerifyRecord.objects.filter(code=reset_code).first()
        if email:
            reset_form = ResetForm()
            return render(request, 'password_reset.html', {'reset_form': reset_form, 'email': email})
        else:
            return render(request, 'password_reset_fail.html')


class ResetPwdView(View):
    """
    用户密码重置
    """

    def post(self, request):
        reset_form = ResetForm(request.POST)
        email = request.POST.get('email', '')
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            user = UserInfo.objects.get(email=email)
            if not user:
                return render(request, 'password_reset.html', {'reset_form': reset_form, 'email': email})
            if pwd1 == pwd2:
                user.password = make_password(pwd1)
                user.save()
                verify_mail = EmailVerifyRecord.objects.filter(email=email)
                verify_mail.delete()
                return render(request, 'login.html')
            else:
                return render(request, 'password_reset.html', {'error': "密码不一致"})
        else:
            return render(request, 'password_reset.html', {'reset_form': reset_form, 'email': email})


class UserCenterView(View):
    """
    用户个人信息显示, 及修改
    """


    def get(self, request):
        # 设置一个在 我的信息， 我的课程，我的收藏， 我的信息 页面的区分标志
        active_flag = 'info'
        return render(request, 'usercenter-info.html', {
            'active_flag': active_flag,
        })

    def post(self, requset):
        user_info_form = UserInfoForm(requset.POST, instance=requset.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure", "msg":"用户信息保存失败"}', content_type='application/json')


class UserCenterMyCourseView(View):
    """
    用户课程显示
    """

    def get(self, request):
        # 设置一个在 我的信息， 我的课程， 我的课程，我的消息 页面的区分标志
        active_flag = 'course'
        user_courses = UserCourse.objects.filter(user=request.user).all()
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'active_flag': active_flag,
        })


class UserCenterFavCourseView(View):
    """
    用户收藏课程显示
    """

    def get(self, request):
        user_fav_courses = []
        fav_courses_id = UserFavorite.objects.filter(user=request.user, fav_type=1).all()
        for course_id in fav_courses_id:
            course = Course.objects.get(id=course_id.fav_id)
            user_fav_courses.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'user_fav_courses': user_fav_courses,
        })


class UserCenterFavOrgView(View):
    """
    用户课程机构收藏显示
    """

    def get(self, request):
        # 设置一个在 我的信息， 我的课程， 我的课程，我的消息 页面的区分标志
        active_flag = 'fav_org'
        user_fav_orgs = []
        fav_orgs_id = UserFavorite.objects.filter(user=request.user, fav_type=2).all()
        for org_id in fav_orgs_id:
            org = CourseOrg.objects.get(id=org_id.fav_id)
            user_fav_orgs.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'user_fav_orgs': user_fav_orgs,
            'active_flag': active_flag,
        })


class UserCenterFavTeacherView(View):
    """
    用户 老师收藏显示
    """

    def get(self, request):
        user_fav_teachers = []
        fav_teachers_id = UserFavorite.objects.filter(user=request.user, fav_type=3).all()
        for teacher_id in fav_teachers_id:
            teacher = Teacher.objects.get(id=teacher_id.fav_id)
            user_fav_teachers.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'user_fav_teachers': user_fav_teachers,
        })


class UserCenterMessageView(View):
    """
    用户消息显示
    """

    def get(self, request):
        # 设置一个在 我的信息， 我的课程， 我的课程，我的消息 页面的区分标志
        active_flag = 'message'
        user_messages = UserMessage.objects.filter(user=request.user.id).all()

        # 显示内容数量分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_messages, 9, request=request)

        page_message = p.page(page)

        return render(request, 'usercenter-message.html', {
            'user_messages': page_message,
            'active_flag': active_flag,
        })


class UploadImageView(View):
    """
    用户头像修改
    """

    # 方法一
    # def post(self, request):
    #     image_form = UserImageForm(request.POST, request.FILES)
    #     if image_form.is_valid():
    #         user_image = image_form.cleaned_data['image']
    #         request.user.image = user_image
    #         request.user.save()
    #     pass
    # 方法二
    def post(self, request):
        image_form = UserImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    用户密码的修改
    """

    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            user = request.user
            if not pwd1 or not pwd2:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
            if pwd1 == pwd2:
                user.password = make_password(pwd1)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dump(reset_form.errors), content_type='application/json')


class SendEmailCodeView(View):
    """
    发送邮箱验证码
    """

    def get(self, request):

        email = request.GET.get('email', '')
        if UserInfo.objects.filter(email=email).first():
            return HttpResponse('{"status":"failure", "email":"用户已经存在"}', content_type='application/json')
        else:
            send_register_email(email, send_type='update_email')
            return HttpResponse('{"email":"邮箱验证码已经发送"}', content_type='application/json')


class UpdateEmailView(View):
    """
    修改用户邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if not email and not code:
            return HttpResponse('{"email":"验证失败"}', content_type='application/json')
        email_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if email_records:
            request.user.email = email
            request.user.save()
            email_records.delete()
            return HttpResponse('{"email":"邮箱已经修改成功"}', content_type='application/json')
        elif code != EmailVerifyRecord.objects.filter(email=email).first().code:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')

        else:
            return HttpResponse('{"email":"邮箱修改失败"}', content_type='application/json')


def page_not_found(request):
    """
    配置页面不存在404
    """
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code == 404
    return response


def page_error(request):
    """
    配置页面错误500
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code == 500
    return response