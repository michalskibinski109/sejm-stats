from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from urllib.parse import urljoin


class Print(models.Model):
    number = models.CharField(max_length=10)
    title = models.TextField()
    term = models.SmallIntegerField()
    document_date = models.DateField(db_column="documentDate")
    delivery_date = models.DateField(db_column="deliveryDate")
    change_date = models.DateTimeField(db_column="changeDate")

    # id is term + number
    @cached_property
    def process_print(self):
        """
        I did not find difference between number and processPrint
        """
        return self.number

    @cached_property
    def pdf_url(self) -> str:
        return urljoin(
            settings.SEJM_ROOT_URL, f"prints/{self.number}/{self.number}.pdf"
        )


class AdditionalPrint(Print):
    main_print = models.ForeignKey(
        Print,
        related_name="additional_prints",
        on_delete=models.CASCADE,
    )
    number_associated = models.CharField(db_column="numberAssociated", max_length=10)
