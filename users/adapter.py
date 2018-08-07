from allauth.account.adapter import DefaultAccountAdapter

class MySaveUserAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from .utils import user_username, user_email, user_field

        data = form.cleaned_data
        email = data.get('email')
        username = data.get('username')
        biography = data.get('biography')
        user_email(user, email)
        user_username(user, username)
        if 'mcname' in data:
            mcname = data.get('mcname')
        else:
            mcname = data.get('username')
        if 'icon' in data:
            icon = data.get('icon')
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user
