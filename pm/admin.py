from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import UserProfile, RelationShip, Paint, Comment, Message
from django.contrib.auth.models import User
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户信息'


class UserAdmin(BaseAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('状态'), {'fields': ('is_active', 'is_superuser')}),
        )
    inlines = (ProfileInline,)


    list_display = ('username', 'is_active', 'is_superuser')






class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PaintAdmin(admin.ModelAdmin):
    def preview(self, obj):
        return '<img src="/media/%s" height="64" width="64" />'%(obj.image)

    def like_count(self, obj):
        return obj.liker.count()
    like_count.short_description = '点赞数'

    def comment_count(self, obj):
        return Comment.objects.filter(paint=obj).count()
    comment_count.short_description = '评论数'

    preview.allow_tags = True
    preview.short_description = "picture"
    list_display = ('id', "preview", "describe", "pub_date", "author", 'like_count', 'comment_count')
    list_display_links = ('describe', 'preview')
    search_fields = ('describe',)
    inlines = [CommentInline,]
    # date_hierarchy = 'pub_date'
    list_filter = ('author', 'pub_date', 'challenge')
    filter_horizontal = ('liker',)



    fields = (('image', 'author'), 'describe','liker')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'paint', 'from_user', 'to_user', 'pub_date')
    list_display_links = ('text',)
    date_hierarchy = 'pub_date'

class RelationShipAdmin(admin.ModelAdmin):

    short_description = 'dsa'
    list_display = ('from_rs', 'to_rs')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('send_by', 'send_to', 'type', 'paint', 'comment', 'readed', 'pub_date')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Paint, PaintAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(RelationShip, RelationShipAdmin)

admin.site.register(Message, MessageAdmin)
