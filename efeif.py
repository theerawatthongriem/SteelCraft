
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField()
    phone_number = models.CharField(max_length=10)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone_number']
        labels = {
            'address': 'ที่อยู่',
            'phone_number': 'เบอร์โทร',
        }

        widgets = {
            'phone_number':forms.TextInput(attrs={'placeholder':'กรอกเบอร์โทร','class':''}),

            'address':forms.Textarea(attrs={'placeholder':'กรอกที่อยู่','class':'h-24 '}),
            'phone_number':forms.TextInput(attrs={'placeholder':'กรอกเบอร์โทร','class':''}),
        }

class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


@login_required(login_url='login')
def editprofile(request):
    user = UserProfile.objects.get(user=request.user)
    userprofile = UserProfileForm(instance=user)
    form = EditForm(instance=request.user)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        userprofile = UserProfileForm(request.POST, instance=user)

        if form.is_valid() and userprofile.is_valid():
            userprofile.save()
            form.save()
            return redirect('profile')
        else:
            form = EditForm()
            userprofile = UserProfileForm(instance=user)
    else:
        form = EditForm(instance=request.user)
        userprofile = UserProfileForm(instance=user)

    return render(request,'editprofile.html',{
        'form':form ,'userprofile':userprofile ,
        'favorite_count':favorite_count(request)})

path('editprofile/',editprofile,name='editprofile'),
