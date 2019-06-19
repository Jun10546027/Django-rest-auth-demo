from django.db import models


# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True,verbose_name="建立時間")
    gender=models.CharField(max_length=1,verbose_name="性別")
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ["email", "gender"]

    class Meta:
        ordering = ('created',)

class Coupon(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon_id = models.CharField(max_length=20, primary_key=True,verbose_name="優惠卷編號")
    coupon_price = models.IntegerField()
    coupon_title = models.CharField("優惠卷標題",max_length=150)
    coupon_class = models.CharField(max_length=20)
    coupon_content = models.CharField(max_length=200)
    coupon_img = models.ImageField(upload_to='coupons', blank=True,null=True)
    coupon_create_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = '優惠卷'
        verbose_name_plural = verbose_name
        ordering = ('coupon_create_at',)

    def __str__(self):
        return self.coupon_title


#使用者收藏
class UserFav(models.Model):

    #兩個外鍵行成關聯表
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="使用者")
    coupons = models.ForeignKey(Coupon, on_delete=models.CASCADE, verbose_name="優惠卷", help_text="優惠卷id")
    user_fav_create_at = models.DateTimeField("添加時間",auto_now_add=True)


    class Meta:
        verbose_name = '使用者收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "coupons")

    def __str__(self):
        return self.user.username

class Music(models.Model):
    song = models.TextField()
    singer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "music"