from django.contrib import admin
from core.models import Club, Envoy, Voting, Vote

# Register your models here.


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "fax", "email", "members_count")


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "date",
    )


@admin.register(Envoy)
class EnvoyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "second_name",
        "last_name",
    )
