from sejm_app.models import FAQ


from django.views.generic import ListView


class FAQListView(ListView):
    model = FAQ
    template_name = "faq_list.html"  # replace with your template
    context_object_name = "faqs"
