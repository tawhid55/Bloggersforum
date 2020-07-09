from django.contrib import admin
from blog.models import Post,Comment,UserProfileInfo,Contact
# Register your models here.


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfileInfo)
admin.site.register(Contact)