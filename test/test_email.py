import uuid
import json
from unittest import TestCase
from unittest.mock import patch, PropertyMock

import pytest

from hackerchallenge.models import ChallengeParticipant
from hackerchallenge.loader import ChallengeLoader

from canyouhackit import settings
from canyouhackit.email import (
    send_email_to_hr, _get_vendor_string,
    _parse_completed_challenges,
    _format_challenge_timestamps
)


@pytest.mark.django_db
class TestEmail(TestCase):

    def setUp(self):
        self.participant = ChallengeParticipant.objects.create(
            points=100,
            account_id=str(uuid.uuid4()),
            source_ip="192.168.1.1",
            source_country="Afghanistan"
        )

    def test_hr_email(self):
        vendor_info = {
            "VENDOR_ID": "test-vendor",
            "VENDOR_NAME": "blah blah",
            "VENDOR_WEBSITE": "blah.com",
            "VENDOR_INFO": "some info",
            "VENDOR_MAIN_OVERRIDE": "blah blah blah",
            "VENDOR_MODAL_OVERRIDE": "blah blah blah"
        }

        # Get a challenge
        challenges = {stub.meta.challenge_id: stub() for stub in ChallengeLoader.get()}
        challenge_id = list(challenges.keys())[0]
        challenge = challenges[challenge_id]
        challenge.challenge_opened()  # Mark it as opened to model the API
        challenge.check("blah")
        challenge.solved = True
        self.participant.completed_challenges = json.dumps([challenge.to_db()])

        self.assertTrue(send_email_to_hr("test@test.com", self.participant, vendor_info))

    def test_hr_email_retired_challenge(self):
        # Get a challenge
        challenges = {stub.meta.challenge_id: stub() for stub in ChallengeLoader.get()}
        challenge_id = list(challenges.keys())[0]
        challenge = challenges[challenge_id]
        challenge.challenge_opened()  # Mark it as opened to model the API
        challenge.check("blah")
        challenge.solved = True
        challenge.meta.retired = True
        self.participant.completed_challenges = json.dumps([challenge.to_db()])

        self.assertTrue(send_email_to_hr("test@test.com", self.participant, None))

    def test_invalid_vendor_info(self):
        vendor_info = {"blah": "invalid"}
        fmt = _get_vendor_string(vendor_info)
        self.assertEqual(fmt, "<unknown-id>: <unknown-vendor>")

    def test_invalid_challenge_list(self):
        self.participant.completed_challenges = "{invalid-JSON"
        self.assertEqual(_parse_completed_challenges(self.participant), [])

    def test_invalid_challenge_timestamps(self):
        challenge = {
            "time_opened": "ferp"
        }
        opened, started, completed = _format_challenge_timestamps(challenge)
        self.assertEqual(opened, "Error")
        self.assertEqual(started, "Error")
        self.assertEqual(completed, "Error")

    def test_no_challenge_timestamps(self):
        challenge = {}
        opened, started, completed = _format_challenge_timestamps(challenge)
        self.assertEqual(opened, "Never")
        self.assertEqual(started, "Never")
        self.assertEqual(completed, "Never")

    @patch("subprocess.Popen")
    def test_real_email(self, mock_popen):
        settings.DEBUG = False
        self.assertTrue(send_email_to_hr("test@test.com", self.participant, None))

    @patch("subprocess.Popen", side_effect=Exception("test failure"))
    def test_real_email(self, mock_popen):
        settings.DEBUG = False
        self.assertFalse(send_email_to_hr("test@test.com", self.participant, None))
