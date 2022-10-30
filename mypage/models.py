from django.db import models

# Create your models here.
# Member
class Member(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    username = models.CharField(max_length=64,verbose_name = '사용자명')
    password = models.CharField(max_length=64,verbose_name = '비밀번호')
    email = models.CharField(max_length=64,verbose_name = '이메일')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    #저장되는 시점의 시간을 자동으로 삽입해준다.

    def __str__(self):
        return self.username

    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'test_user'