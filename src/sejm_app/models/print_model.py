from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from urllib.parse import urljoin
from django.db.models import F
from django.utils import timezone
from datetime import datetime


class PrintModel(models.Model):
    id = models.CharField(max_length=13, primary_key=True, editable=False)
    number = models.CharField(max_length=10)
    term = models.SmallIntegerField()
    title = models.TextField()
    document_date = models.DateField(db_column="documentDate")
    delivery_date = models.DateField(db_column="deliveryDate")
    change_date = models.DateTimeField(db_column="changeDate")

    def save(self, *args, **kwargs):
        self.document_date = timezone.make_aware(
            datetime.strptime(self.document_date, "%Y-%m-%d")
        )
        self.delivery_date = timezone.make_aware(
            datetime.strptime(self.delivery_date, "%Y-%m-%d")
        )
        self.id = f"{self.term}{self.number}"
        super().save(*args, **kwargs)

    # id is term + number
    @cached_property
    def process_print(self):
        """
        I did not find difference between number and processPrint
        """
        return self.number

    @cached_property
    def pdf_url(self) -> str:
        return f"{settings.SEJM_ROOT_URL}/prints/{self.number}/{self.number}.pdf"

    def __str__(self) -> str:
        return f"{self.number}. {self.title}"


class AdditionalPrint(PrintModel):
    main_print = models.ForeignKey(
        PrintModel,
        related_name="additional_prints",
        on_delete=models.CASCADE,
    )
