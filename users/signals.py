from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def populate_profile(sociallogin, user, **kwargs):    

    if sociallogin.account.provider == 'facebook':
        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"            
        email = user_data['email']
        first_name = user_data['first_name']

    if sociallogin.account.provider == 'google':
        print("user.socialaccount_set>>>>>>>",user.socialaccount_set)
    # user.profile.avatar_url = picture_url
    # user.profile.email_address = email
    # user.profile.first_name = first_name
    # user.profile.save()         