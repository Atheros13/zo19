from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from zo.models.user import UserTemporaryPassword

class StaffView(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff

class TempPasswordCheck(UserPassesTestMixin):

    def test_func(self):

        user = self.request.user
        if UserTemporaryPassword.objects.filter(user=user):
            return False
        return True

    def handle_no_permission(self):

        return redirect('user_settings')
