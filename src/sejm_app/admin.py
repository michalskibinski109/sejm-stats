from django.contrib import admin
from sejm_app.models import (
    Club,
    Envoy,
    Voting,
    Vote,
    Scandal,
    FAQ,
    PrintModel,
    AdditionalPrint,
    Process,
    Stage,
)


# Register your models here.
@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Process)
class process_admin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )


@admin.register(PrintModel)
class PrintModelAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "title")


@admin.register(AdditionalPrint)
class AdditionalPrintAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number",
        "title",
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question")


@admin.register(Scandal)
class ScandalAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # if this is a new object, set the author
            obj.author = request.user
        super().save_model(request, obj, form, change)


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
