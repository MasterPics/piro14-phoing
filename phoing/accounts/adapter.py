from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


# class MyAccountAdapter(DefaultAccountAdapter):

#     def save_user(self, request, user, form, commit=True):
#         """
#         This is called when saving user via allauth registration.
#         We override this to set additional data on user object.
#         """
#         # Do not persist the user yet so we pass commit=False
#         # (last argument)
#         user = super(UserAccountAdapter, self).save_user(
#             request, user, form, commit=commit)
#         if not user.username:
#             user.usernmae = user.email.split('@')[0]
#         user.save()  # This would be called later in your custom SignupForm


# class MySocialAccountAdapter(DefaultSocialAccountAdapter):

#     def save_user(self, request, user, form, commit=False):
#         """
#         This is called when saving user via allauth registration.
#         We override this to set additional data on user object.
#         """
#         # Do not persist the user yet so we pass commit=False
#         # (last argument)
#         user = super(UserAccountAdapter, self).save_user(
#             request, user, form, commit=commit)
#         if not user.username:
#             user.usernmae = user.email.split('@')[0]
#         user.save()  # This would be called later in your custom SignupForm
