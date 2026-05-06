from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added, pre_social_login, social_account_updated
from .models import Researcher


@receiver(social_account_added)
def my_callback(sender, **kwargs):
    account = kwargs["sociallogin"].account
    #token = sl.token
    #user = sl.user
    orcid_profile = account.extra_data
    given_names = orcid_profile['person']['name']['given-names']['value']
    family_name = orcid_profile['person']['name']['family-name']['value']
    researcher, created = Researcher.objects.get_or_create(last_name=family_name, first_name=given_names)
    if researcher.orcid:
        assert researcher.orcid == account.uid
    else:
        researcher.orcid = account.uid
        researcher.save()
