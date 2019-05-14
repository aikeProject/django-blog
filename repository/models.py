from django.db import models
from django.core.validators import RegexValidator, EmailValidator


# Create your models here.

class UserInfo(models.Model):
    """
    用户表
    """

    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(
        verbose_name='密码',
        max_length=64,
        validators=[
            RegexValidator(regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
                           message='密码必须包含数字，字母、特殊字符')
        ])
    nickname = models.CharField(verbose_name='昵称', max_length=64)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='static/avatar')
    creat_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    # 多对多关系
    fans = models.ManyToManyField(
        verbose_name='粉丝们',
        to='UserInfo',
        through='UserFans',
        related_name='f',
        through_fields=('user', 'follower')
    )

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客表
    """

    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    # 一对一
    user = models.OneToOneField(to='UserInfo', to_field='nid')

    def __str__(self):
        return self.title


class UserFans(models.Model):
    """
    粉丝关系表
    """

    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')

    class Meta:
        # 联合唯一索引
        unique_together = [('user', 'follower'), ]


class Category(models.Model):
    """
    博主个人文章分类
    """

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    # 一对多
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章
    """

    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=128)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True)

    type_choices = [
        (1, 'Python'),
        (2, 'Linux'),
        (3, '哈哈'),
        (4, '嘿嘿'),
    ]

    article_type_id = models.IntegerField(choices=type_choices, default=None)

    # 多对多关系
    tags = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag')
    )


class ArticleDetail(models.Model):
    """
    文章详细表
    """

    content = models.TextField(verbose_name='文章内容', )
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')


class UpDown(models.Model):
    """
    文章 赞 踩表
    """

    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid')
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):
    """
    评论表
    """

    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论人', to='UserInfo', to_field='nid')


class Tag(models.Model):
    """
    标签表
    """

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')


class Article2Tag(models.Model):
    """
    文章标签关系表
    """

    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to='Tag', to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag')
        ]
