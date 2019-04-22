from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.utils.html import format_html
from integree_test.models import Investor, Project, Task, Comment


class InlineInvestor(admin.StackedInline):
    model = Project


class InlineTask(admin.StackedInline):
    model = Comment


class UserAdmin(admin.ModelAdmin):
    date_hierarchy = "date_joined"
    search_fields = ("first_name", "last_name", "login", "email")
    list_filter = ("is_active", "is_staff", "is_superuser")


class InvestorAdmin(admin.ModelAdmin):

    def investor_projects_count(self, obj):
        return obj.project_set.count()

    investor_projects_count.short_description = "Project Count"

    search_fields = ("name", )
    inlines = (InlineInvestor, )
    list_display = ("investor_projects_count", "name", )


class ProjectAdmin(admin.ModelAdmin):

    def project_counter(self, obj):
        count_new = obj.task_set.filter(status=1).count()
        count_in_progress = obj.task_set.filter(status=2).count()
        return f"{count_new}/{count_in_progress}"

    search_fields = ("name",)
    list_filter = ("investor",)
    list_display = ("investor", "name", "project_counter")


class TaskAdmin(admin.ModelAdmin):

    def color_of_status(self, obj):
        if obj.status == 1:
            return format_html(f'<span style="color:red">{obj.get_status_display()}</span>')
        elif obj.status == 2:
            return format_html(f'<span style="color:orange">{obj.get_status_display()}</span>')
        elif obj.status == 3:
            return format_html(f'<span style="color:green">{obj.get_status_display()}</span>')
        else:
            return format_html(f'<span style="color:gray">{obj.get_status_display()}</span>')

    search_fields = ("subject", "description")
    list_filter = ("status", "project", "project__investor")
    date_hierarchy = "add_date"
    inlines = (InlineTask, )
    list_display = ("project", "subject", "status", "add_date", "color_of_status")


admin.site.register(Investor, InvestorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
