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
    Interpellation,
    Reply,
    ClubVote,
)


@admin.register(ClubVote)
class ClubVoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "club",
    )


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "key")


@admin.register(Interpellation)
class InterpellationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "fromMember")


# Register your models here.
@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("id", "decision", "stage_name", "date", "process")


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
    list_display = ("id", "name", "phone", "fax", "email")


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
        "firstName",
        "secondName",
        "lastName",
    )
