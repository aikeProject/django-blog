from django.contrib import admin
import repository.models as repository


# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('nid', 'username', 'password', 'nickname', 'email', 'avatar')


class BlogAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'site', 'theme', 'user')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'summary', 'create_time', 'blog', 'category', 'article_type_id')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('nid', 'content', 'create_time', 'reply', 'article', 'user')


admin.site.register(repository.UserInfo, UserInfoAdmin)
admin.site.register(repository.Blog, BlogAdmin)
admin.site.register(repository.UserFans)
admin.site.register(repository.UpDown)
admin.site.register(repository.Article, ArticleAdmin)
admin.site.register(repository.Tag)
admin.site.register(repository.Category)
admin.site.register(repository.ArticleDetail)
admin.site.register(repository.Comment, CommentAdmin)
admin.site.register(repository.Article2Tag)
