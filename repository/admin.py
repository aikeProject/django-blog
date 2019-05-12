from django.contrib import admin
import repository.models as repository
# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):

    list_display = ('nid', 'username', 'password', 'nickname', 'email', 'avatar')


admin.site.register(repository.UserInfo, UserInfoAdmin)
admin.site.register(repository.Blog)
admin.site.register(repository.UserFans)
admin.site.register(repository.UpDown)
admin.site.register(repository.Article)
admin.site.register(repository.Tag)
admin.site.register(repository.Category)
admin.site.register(repository.ArticleDetail)
admin.site.register(repository.Comment)
admin.site.register(repository.Article2Tag)