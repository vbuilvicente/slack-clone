from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404

# Create your views here.
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from plataforma.models import Profile
from system_account.forms import ProfileForm, UserForm


@login_required(login_url='/login/')
def setting_account(request):
    return render_to_response('account/acc_settings.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def setting_log(request):
    return render_to_response('account/acc_logs.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def setting_profile(request):
    return render_to_response('account/acc_profile.html', context_instance=RequestContext(request))


@csrf_protect
@login_required(login_url='/login/')
def setting_profile_edit(request):
    args = {}
    args.update(csrf(request))
    if request.method == "POST":
        user = get_object_or_404(User, username=request.user)
        # form_user = UserForm(request.POST, instance=request.user)
        form = ProfileForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
        else:
            args['form'] = form
    else:
        form = ProfileForm(instance=request.user.profile)
    return render_to_response('account/acc_edit_profile.html', {'form': form},
                              context_instance=RequestContext(request))
