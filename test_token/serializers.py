from rest_framework import serializers

#使用者收藏
from rest_framework.validators import UniqueTogetherValidator

from .models import Music,Coupon,User,UserFav


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id','username', 'email', 'last_name', 'password')

class CouponSerializer(serializers.ModelSerializer):

    # image_url = serializers.SerializerMethodField('get_url')
    coupon_img = serializers.ImageField(required=False,max_length=None,
                                     allow_empty_file=True, use_url=True)

    class Meta:
        model = Coupon
        fields = ('coupon_id','coupon_title','coupon_class','coupon_content','coupon_price','coupon_img')

    # def get_url(self, obj):
    #     return str(obj.coupon_img.url)

class UserFavSerializer(serializers.ModelSerializer):
    #獲取當前使用者是誰
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # 設定validate使一個coupons只能收藏一次
        validators = [
            #只能一個
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'coupons'),
                # message的信息可以自定义
                message="已經收藏"
            )
        ]
        model = UserFav
        # 收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少
        fields = ("user", "coupons", 'id')


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('song','singer')