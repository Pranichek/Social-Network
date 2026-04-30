from ..forms import WelcomeForm

def global_form(request):
    form = WelcomeForm(request.POST)
    
    return {'welcome_form': form}