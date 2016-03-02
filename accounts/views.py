from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from contacts.models import Contact

from . import forms, models


# Create your views here.


@login_required()
def account_cru(request, uuid=None):
    if uuid:
        account = get_object_or_404(models.Account, uuid=uuid)
        if account.owner != request.user:
            return HttpResponseForbidden()
    else:
        account = models.Account(owner=request.user)

    if request.POST:
        form = forms.AccountForm(request.POST, instance=account)

        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()

            redirect_url = reverse('accounts.views.account_detail', args=(account.uuid,))

            return HttpResponseRedirect(redirect_url)
    else:
        form = forms.AccountForm(instance=account)

    variables = {
        'form': form,
        'account': account,
    }

    template = 'accounts/new.html'

    return render(request, template, variables)

@login_required()
def account_detail(request, uuid):
    account = models.Account.objects.get(uuid=uuid)

    if account.owner != request.user:
        return HttpResponseForbidden()

    contacts = Contact.objects.filter(account=account)

    variables = {
        'account': account,
        'contacts': contacts,
    }

    return render(request, 'accounts/detail.html', variables)

class AccountList(ListView):
    model = models.Account
    paginate_by = 12
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        try:
            a = self.request.GET.get('account')
        except KeyError:
            a = None

        if a:
            account_list = models.Account.objects.filter(
                name__icontains=a,
                owner=self.request.user
            )
        else:
            account_list = models.Account.objects.filter(owner=self.request.user)
        return account_list

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountList, self).dispatch(*args, **kwargs)
