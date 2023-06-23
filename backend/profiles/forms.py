from .models import Profile
from django import forms

from PIL import Image


class UserForm(forms.ModelForm):
   class Meta:
       model = Profile
       fields = [
            "user",
            "nike",
            "avatar",
            "email_two",
            "phone",
            "first_name",
            "last_name"
       ]

       @property
       def get_avatar_url(self):
           if self.avatar:
               return '/media/{}'.format(self.user)
           else:
               return 'static/img/default.png'

       def save(self, *args, **kwargs):
           super().save(*args, **kwargs)
           if self.avatar:
               img = Image.open(self.avatar.path)
               if img.height > 200 or img.width > 200:
                   output_size = (200, 200)
                   img.thumbnail(output_size)
                   img.save(self.avatar.path)