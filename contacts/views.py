from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView

from . import models
from . import forms

from accounts.models import Account


# Create your views here.


class ContactMixin(object):
    model = models.Contact

    def get_context_data(self, **kwargs):
        kwargs.update({'object_name': 'Contact'})
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactMixin, self).dispatch(*args, **kwargs)

class ContactDelete(ContactMixin, DeleteView):
    template_name = 'common/object_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(ContactDelete, self).get_object()
        if obj.owner != self.request.user:
            raise Http404

        account = Account.objects.get(id=obj.account.id)
        self.account = account

        return obj

    def get_success_url(self):
        return reverse('accounts:detail', args=(self.account.uuid))

@login_required()
def contact_cru(request, uuid=None, account=None):
    if uuid:
        contact = get_object_or_404(models.Contact, uuid=uuid)
        if contact.owner != request.user:
            return HttpResponseForbidden()
    else:
        contact = models.Contact(owner=request.user)

    if request.POST:
        form = forms.ContactForm(request.POST, instance=contact)
        if form.is_valid():
            account = form.cleaned_data['account']
            if account.owner != request.user:
                return HttpResponseForbidden()

            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()

            if request.is_ajax():
                return render(request, 'contacts/item_view.html', {'account': account, 'contact': contact})

            reverse_url = reverse('accounts:detail', args=(account.uuid,))

            return HttpResponseRedirect(reverse_url)
    else:
        form = forms.ContactForm(instance=contact)

    if request.GET.get('account', ''):
        account = Account.objects.get(id=request.GET.get('account', ''))

    variables = {
        'form': form,
        'contact': contact,
        'account': account,
    }

    if request.is_ajax():
        template = 'contacts/item_form.html'
    else:
        template = 'contacts/cru.html'

    return render(request, template, variables)

@login_required()
def contact_detail(request, uuid):
    contact = models.Contact.objects.get(uuid=uuid)

    return render(request, 'contacts/detail.html', {'contact': contact})
