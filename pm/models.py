from django.db import models
from django.contrib.auth.models import User
# Create your models here.

SEX_CHOICE = ((0, '女'),
              (1, '男'),
             )

MESSAGE_CHOICE = (
    (0, '评论'),#
    (1, '消息'),
    (2, '@'),
    (3, '喜欢'),#
    (4, '关注'),#
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    sex = models.IntegerField('性别', choices=SEX_CHOICE, default=0)
    age = models.PositiveIntegerField('年龄', default=5)
    profile = models.TextField('简介', max_length=32, default='...')
    avatar = models.ImageField('头像', blank=True)

    def __str__(self):
        return self.user.username


class Paint(models.Model):
    image = models.ImageField('图片')
    describe = models.TextField('描述', max_length=128)
    pub_date = models.DateTimeField('发布时间', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paints')
    liker = models.ManyToManyField(User, related_name="likes")

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = '画'
        verbose_name_plural = '画'

    def __str__(self):
        return self.describe[:10]


class Comment(models.Model):
    paint = models.ForeignKey(Paint, on_delete=models.CASCADE,
                              related_name='comments')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='send_by_me')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='send_to_me')
    text = models.TextField('内容', max_length=128)
    pub_date = models.DateTimeField('发布时间', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return self.text


class ChallengeShip(models.Model):
    paint = models.ForeignKey(Paint)
    challenge = models.ForeignKey('Challenge')
    vote = models.IntegerField(default=0)


class Challenge(models.Model):
    title = models.TextField('标题', max_length=128)
    desc = models.TextField('描述', max_length=128)
    pub_date = models.DateTimeField('发布时间', auto_now_add=True)
    days = models.IntegerField(default=7)
    paints = models.ManyToManyField(Paint, through=ChallengeShip)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = '挑战'
        verbose_name_plural = '挑战'

    def __str__(self):
        return self.title

#海报
# class Poster(models.Model):
#     image = models.Ima
#     challenge = models.ForeignKey('Challenge')
#     vote = models.IntegerField(default=0)


class Message(models.Model):
    send_to = models.ForeignKey(User, related_name='message_to_me', on_delete=models.CASCADE)
    send_by = models.ForeignKey(User, related_name='message_by_me', on_delete=models.CASCADE)
    type = models.IntegerField('类型', choices=MESSAGE_CHOICE)
    paint = models.ForeignKey(Paint, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('发布时间', auto_now_add=True)
    readed = models.BooleanField('已读',default=False)
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = '消息'
        verbose_name_plural = '消息'


# from_rs 关注 to_rs
# u1关注u2 ：
# 创建个relationship from设成u1 to设成u2 保存


class RelationShip(models.Model):
    from_rs = models.ForeignKey(User, related_name='follow', on_delete=models.CASCADE)
    to_rs = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '粉丝关系'
        verbose_name_plural = '粉丝关系'

    def __str__(self):
        return str(self.from_rs) + " 关注 " + str(self.to_rs)
