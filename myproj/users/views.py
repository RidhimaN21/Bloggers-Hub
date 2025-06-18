from django.shortcuts import render , redirect
from django.contrib.auth import login , logout
from .forms import CustomForm , OTPForm , UserForm , UserProfileForm , BackupOrPasswordLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model , authenticate
User = get_user_model()
from .models import EmailOTP , UserProfile
from .utils import generate_otp,send_otp_email
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy , reverse
import secrets
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            otp = generate_otp()
            EmailOTP.objects.create(user=user,otp=otp)
            send_otp_email(user,otp)
            
            request.session['pending_user_id'] = user.id
            return redirect("users:verify_otp")
    else:
        form = CustomForm()

    return render(request,'users/register.html',{"form":form})

def verify_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('register')

    user = User.objects.get(id=user_id)
    otp_obj = EmailOTP.objects.get(user=user)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if str(otp_obj.otp) == str(entered_otp):
                user.is_active = True
                token = secrets.token_urlsafe(6)[:6]
                user.backup_token = token
                user.save()
                otp_obj.delete()
                del request.session['pending_user_id']

                

                return render(request,'users/display_token.html',{'token' : token})
            else:
                form.add_error('otp','Invalid OTP')
    else:
        form = OTPForm()
    return render(request,'users/verify_otp.html',{"form":form})

def customLoginView(request):
    form = BackupOrPasswordLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        token = form.cleaned_data['token']
        login_method = form.cleaned_data.get('login_method')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            form.add_error(None, "Invalid username.")
            return render(request, 'users/login.html', {'form': form})

        user_auth = None
        new_token = None  
        if login_method == 'password' and password:
            user_auth = authenticate(request, username=username, password=password)

        if not user_auth and login_method == 'token' and token:
            if user.backup_token == token:
                user_auth = user
                new_token = secrets.token_hex(3)
                user.backup_token = new_token
                user.save()

        if user_auth:
            login(request, user_auth, backend='django.contrib.auth.backends.ModelBackend')
            next_url = request.POST.get('next') or 'blogs:list'
            if new_token:
                return render(request, 'users/show_token.html', {'new_token': new_token})
            else:
                return redirect(next_url)
        else:
            form.add_error(None, "Invalid credentials or token.")
    return render(request, 'users/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect("blogs:list")
        
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("users:profile")


    return render(request,'users/profile.html',{
        "user_form" : user_form,
        "profile_form" : profile_form,
    })

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "users/change_password.html"
    success_url = reverse_lazy('users:profile')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        EmailOTP.objects.filter(user=user).delete()

        otp = generate_otp();
        EmailOTP.objects.update_or_create(user=user,defaults={'otp' : otp})
        send_otp_email(user,otp)

        self.request.session['pending_user_id'] = user.id
        return redirect("users:verify_otp")




# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request,user)

#             next_url = request.POST.get('next') or reverse('blogs:list')
#             return redirect(next_url)
#     else:
#         form = AuthenticationForm()
#     return render(request,'users/login.html', {"form" : form})
















