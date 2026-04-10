from django.contrib import admin
from .models import Student, Event, Request


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'group', 'email', 'total_points']
    search_fields = ['full_name', 'email']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'date']
    list_filter = ['level']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'event', 'role', 'status', 'points_awarded']
    list_filter = ['status', 'role']
