from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic import FormView
from django.db.models import Count, Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from .models import Client, RelationshipManager, Document
from .forms import ClientInfoForm, ClientSubmissionForm


def index(request):
    template = loader.get_template("manage_docs/index.html")
    return HttpResponse(template.render({}, request))


def submission_success(request, pk):
    # Client successfully submitted documents
    template = loader.get_template("manage_docs/submission_success.html")
    context = {}
    if client := Client.objects.filter(id=pk):
        context["client"] = client[0]
    return HttpResponse(template.render(context, request))


class ClientView(UserPassesTestMixin, ListView):
    model = Client
    paginate_by = 50
    # #TODO pagination not implemented in this demo
    template_name = "manage_docs/clients.html"

    def test_func(self):
        """Block invalid RM id's."""
        if RelationshipManager.objects.filter(id=self.kwargs["pk"]).exists():
            return True
        return False

    def get_queryset(self):
        """Assume the correct user is already logged in.
        Normally you would determine the queryset from the user that is logged
        in without needing extra params in the url."""
        if rm := RelationshipManager.objects.filter(id=self.kwargs["pk"]):
            clients = Client.objects.filter(relationship_manager=rm[0])
            # add annotation for showing <valid documents>/<total documents> in table
            # this could also have been done with a custom filter in the template
            clients = clients.annotate(
                valid_document_count=Count("document", filter=Q(document__valid=True))
            )
            return clients
        else:
            return Client.objects.none()


class ClientInfoView(UserPassesTestMixin, FormView):
    """Show client info, and manage their documents."""

    form_class = ClientInfoForm
    template_name = template_name = "manage_docs/client_info.html"

    def test_func(self):
        """Assume RM is already logged in and has acess to this client. Normally this would also be checked here.
        Only block invalid client id's."""
        if Client.objects.filter(id=self.kwargs["pk"]).exists():
            return True
        return False

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("client-info", kwargs={"pk": self.kwargs["pk"]})

    def get_form_kwargs(self):
        """Add dynamic fields according to documents of client."""
        kwargs = super().get_form_kwargs()
        kwargs["document_set"] = Client.objects.get(
            id=self.kwargs["pk"]
        ).document_set.all()
        return kwargs

    def form_valid(self, form):
        form.save(self.kwargs["pk"], self.request)
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        documents = (
            Client.objects.get(id=self.kwargs["pk"])
            .document_set.all()
            .values(
                "id",
                "name",
                "file",
                "valid",
            )
        )
        if documents:
            for document in documents:
                initial.update(
                    {"document_{}_valid".format(document["id"]): document["valid"]}
                )
        return initial

    def get_context_data(self, **kwargs):
        """Add client object to context."""
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context


class ClientSubmissionView(UserPassesTestMixin, FormView):
    """Client requested document submission."""

    form_class = ClientSubmissionForm
    template_name = template_name = "manage_docs/client_submission.html"

    def test_func(self):
        """Assume Client is already logged in and has acess to this url. Normally the
        Client id would not be needed if they were logged in.
        Only block invalid client id's."""
        if Client.objects.filter(id=self.kwargs["pk"]).exists():
            return True
        return False

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("client-submission-success", kwargs={"pk": self.kwargs["pk"]})

    def get_form_kwargs(self):
        """Add dynamic fields according to documents of client."""
        kwargs = super().get_form_kwargs()
        name_list = []
        for param in self.request.GET:
            if self.request.GET[param] == "True":
                name_list.append(param)
        kwargs["client_docs"] = Document.objects.filter(
            client__id=self.kwargs["pk"]
        ).filter(name__in=name_list)
        # TODO display empty message about params...
        return kwargs

    def form_valid(self, form):
        form.save(self.kwargs["pk"], self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add client object to context."""
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context
