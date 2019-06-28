# Create your views here.
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

#permission(用於我的最愛)
from util.permission import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status,generics,mixins,reverse

from .models import Music,Coupon,User,UserFav
from .serializers import MusicSerializer ,CouponSerializer,UserSerializer ,UserFavSerializer

#設定分頁
from rest_framework.pagination import PageNumberPagination

#設定過濾器
from .filter import CouponFilter
from django_filters.rest_framework import DjangoFilterBackend

#設定搜尋，排序
from rest_framework.filters import SearchFilter , OrderingFilter

# to post activate
from rest_framework.views import APIView
import requests

#隨機密碼
from .random_passwd import RandomPassword

from django.contrib.auth.tokens import default_token_generator

from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings

from django.views.generic import TemplateView

# class HomePageView(TemplateView):
#     template_name = 'homepage.html'

class PasswordResetEmail(BaseEmailMessage):
    template_name = 'email/password_reset.html'

    def get_context_data(self):
        context = super(PasswordResetEmail, self).get_context_data()

        user = context.get('user')
        context['uid'] = utils.encode_uid(user.pk)
        context['token'] = default_token_generator.make_token(user)
        context['url'] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        # context['new_password'] = RandomPassword() ##修改的地方
        return context

##激活帳號
class ActivateUserByGet(APIView):
    def get (self, request, uid, token):

            #獲取網址中的uid和token，透過requests中的post方法自行post進去做激活
            protocol = 'https://' if request.is_secure() else 'http://'
            web_url = protocol + request.get_host()
            post_url = web_url + "/auth/users/activate/"
            post_data = {'uid': uid, 'token': token}
            result = requests.post(post_url, data = post_data)

            #判斷成功激活或失敗
            if result.status_code == 204:
                return Response({'detail': 'all good sir'})
            else:
                return Response(result.json())

##重設密碼
class ResetPasswordUserByGet(APIView):

    def get (self, request, uid, token):
            #獲取網址中的uid和token，透過requests中的post方法自行post進去做激活
            new_password = RandomPassword()
            protocol = 'https://' if request.is_secure() else 'http://'
            web_url = protocol + request.get_host()
            post_url = web_url + "/auth/password/reset/confirm/"
            post_data = {'uid': uid, 'token': token,'new_password':new_password}
            result = requests.post(post_url, data = post_data)

            #判斷成功激活或失敗
            if result.status_code == 204:
                return Response({'new_password':new_password})
            else:
                return Response(result.json())

##Coupont自訂分頁
class CouponPagination(PageNumberPagination):
    #每頁顯示個數
    page_size = 10
    #允許動態改變每頁顯示個數
    page_size_query_param = 'page_size'
    #設定頁碼參數
    page_query_param = 'page'
    #最多多少頁
    max_page_size = 100

# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    parser_classes = (JSONParser,)
    #permission_classes = [AllowAny]
    permission_classes = (IsAuthenticated,)

class UserViewSet(viewsets.GenericViewSet,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin):
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Create your views here.
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    #載入自定義Pagination
    pagination_class = CouponPagination

    #自定義filter
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = CouponFilter

    #permission設置(JWT)
    permission_classes = ()

    #search設定
    search_fields = ("coupon_title","coupon_class")

    #ordering_fields -->  設定可排序的參數      ordering  ->  默認排序
    ordering_fields = ('coupon_price',)
    ordering=('coupon_title',)



#我的最愛
class UserFavViewset(viewsets.GenericViewSet
                    ,mixins.RetrieveModelMixin
                    , mixins.ListModelMixin
                    , mixins.CreateModelMixin
                    , mixins.DestroyModelMixin):

    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

    #透過自定permission，來判斷使用者是誰
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    #因為在serializers 是 coupons ->所以這裡不是coupon_id
    lookup_field = 'coupons_id'

    def get_queryset(self):
        # 只能看到自己的收藏，不能看到別人的
        return UserFav.objects.filter(user=self.request.user)
