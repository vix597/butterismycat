from uuid import uuid4
from unittest import TestCase
from unittest.mock import patch
import pytest
from django.core.management import call_command
from hackerchallenge.models import ChallengeParticipant
from canyouhackit.models import ChallengeSubmission
from canyouhackit import settings


@pytest.mark.django_db
class TestSendUpdateEmail(TestCase):

    def setUp(self):
        self.account_id = str(uuid4())
        participant = ChallengeParticipant.objects.create(account_id=self.account_id, points=10)
        ChallengeSubmission.objects.create(participant=participant)

    def test_send_update_email(self):
        args = []
        opts = {}
        call_command("sendupdateemail", *args, **opts)

    @patch("subprocess.Popen")
    def test_real_email(self, _mock_popen):
        settings.DEBUG = False
        args = []
        opts = {}
        call_command("sendupdateemail", *args, **opts)

    @patch("subprocess.Popen", side_effect=Exception("test failure"))
    def test_real_email_failed(self, _mock_popen):
        settings.DEBUG = False
        args = []
        opts = {}
        call_command("sendupdateemail", *args, **opts)
