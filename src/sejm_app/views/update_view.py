from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse
from celery import chain


@method_decorator(csrf_exempt, name="dispatch")  # Consider CSRF implications
class UpdateView(View):

    def get(self, request):
        from sejm_app.tasks import sejm_tasks, eli_tasks

        task_result = chain(t.s() for t in sejm_tasks + eli_tasks).delay()
        return JsonResponse(
            {"message": "Update initiated. Please check back shortly for results."}
        )
