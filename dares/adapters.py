from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data
        first_name = extra_data.get('given_name', '')
        last_name = extra_data.get('family_name', '')

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
            
        return user