from django import forms
from django.core.mail import send_mail
from django.urls import reverse_lazy
import re
from .models import Document, Client, RelationshipManager


class ClientInfoForm(forms.Form):
    """Show client details and documents. Check if documents are valid or not, and send document requests."""

    def __init__(self, *args, **kwargs):
        """Add dynamic fields according to documents of client."""
        document_set = kwargs.pop("document_set")
        super().__init__(*args, **kwargs)
        for document in document_set:
            self.fields["document_{}_valid".format(document.id)] = forms.BooleanField(
                required=False
            )
            self.fields["document_{}_request".format(document.id)] = forms.BooleanField(
                required=False
            )

    def save(self, pk, request):
        # we need request to build the absolute url in the email
        # loop through fields to save relevant data and send request if needed
        data = self.cleaned_data
        request_ids = []
        url_params = "?"
        for d in data:
            # save valid
            if interval := re.fullmatch("document_[0-9]+_valid", d):
                id = int(re.search("[0-9]+", interval.group()).group())
                doc = Document.objects.get(id=id)
                doc.valid = data[d]
                doc.save()
            # doc request
            elif interval := re.fullmatch("document_[0-9]+_request", d):
                id = int(re.search("[0-9]+", interval.group()).group())
                if data[d]:
                    request_ids.append(id)
                    url_params += "&{}=True".format(Document.objects.get(id=id).name)
        url = "{}{}".format(reverse_lazy("client-submission", args=[pk]), url_params)
        url = request.build_absolute_uri(url)
        if request_ids:
            client = Client.objects.get(id=pk)
            rm = RelationshipManager.objects.get(id=client.relationship_manager.id)
            document_list = ""
            for doc in Document.objects.filter(id__in=request_ids):
                document_list += "\n  - {}".format(doc.name)

            message = """Dear {client_first_name} {client_last_name},
            
Please submit the following documents at {form_url} :
{document_list}

Kind Regards,
{rm_first_name} {rm_last_name}
""".format(
                client_first_name=client.user.first_name,
                client_last_name=client.user.last_name,
                form_url=url,
                document_list=document_list,
                rm_first_name=rm.user.first_name,
                rm_last_name=rm.user.last_name,
            )
            send_mail(
                "Document Submission Request",
                message,
                rm.user.email,
                [client.user.email],
                fail_silently=False,
            )


class ClientSubmissionForm(forms.Form):
    """Dynamic form for requested documents from relationship manager."""

    def __init__(self, *args, **kwargs):
        """Add dynamic fields according to requested documents."""
        client_docs = kwargs.pop("client_docs")
        super().__init__(*args, **kwargs)
        for d in client_docs:
            self.fields["document_{}_file".format(d.id)] = forms.FileField()

    def save(self, pk, request):
        data = self.cleaned_data

        document_list = ""
        for d in data:
            # save file
            if interval := re.fullmatch("document_[0-9]+_file", d):
                id = int(re.search("[0-9]+", interval.group()).group())
                doc = Document.objects.get(id=id)
                doc.file = data[d]
                doc.save()
                document_list += "\n  - {}".format(doc.name)

        client = Client.objects.get(id=pk)
        rm = RelationshipManager.objects.get(id=client.relationship_manager.id)
        url = request.build_absolute_uri(reverse_lazy("client-info", args=[pk]))
        message = """Dear {rm_first_name} {rm_last_name},

{client_first_name} {client_last_name} has submitted the following documents available at {form_url} :
{document_list}
""".format(
            client_first_name=client.user.first_name,
            client_last_name=client.user.last_name,
            form_url=url,
            document_list=document_list,
            rm_first_name=rm.user.first_name,
            rm_last_name=rm.user.last_name,
        )

        send_mail(
            "Document Submission Request",
            message,
            "admin@admin.com",
            [rm.user.email],
            fail_silently=False,
        )
