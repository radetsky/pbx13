from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    site_header = "PBX Setup"
    index_title = "PBX Administration"
