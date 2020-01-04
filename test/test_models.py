from uuid import uuid4

from unittest import TestCase

import pytest

from hackerchallenge.models import ChallengeParticipant

from canyouhackit.models import ChallengeSubmission


@pytest.mark.django_db
class TestModels(TestCase):

    def setUp(self):
        self.account_id = str(uuid4())
        participant = ChallengeParticipant.objects.create(account_id=self.account_id, points=10)
        ChallengeSubmission.objects.create(participant=participant)

    def test_participant(self):
        participant = ChallengeParticipant.objects.get(account_id=self.account_id)
        submission = ChallengeSubmission.objects.get(participant_id=self.account_id)
        self.assertEqual(participant.points, 10)
        self.assertFalse(submission.email_submitted)

    def test_submission_str(self):
        participant = ChallengeParticipant.objects.get(account_id=self.account_id)
        submission = ChallengeSubmission.objects.get(participant_id=self.account_id)
        self.assertEqual(
            str(submission), "{} has 10 points and has not submitted their score yet.".format(self.account_id))
        submission.email_submitted = True
        self.assertEqual(
            str(submission), "{} has 10 points and has submitted their score already.".format(self.account_id))
