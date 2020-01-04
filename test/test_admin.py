import os
import json
from uuid import uuid4
from unittest import TestCase
import pytest
from django.utils.safestring import mark_safe
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from canyouhackit.models import ChallengeSubmission, VendorReferral
from canyouhackit.admin import ChallengeSubmissionAdmin
from hackerchallenge.models import ChallengeParticipant


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


@pytest.mark.django_db
class ModelAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        participant = ChallengeParticipant.objects.create(
            points=100,
            account_id=str(uuid4())
        )
        participant2 = ChallengeParticipant.objects.create(
            points=100,
            account_id=str(uuid4())
        )

        referral = VendorReferral.objects.create(
            vendor_id=1234,
            vendor_name="Sweet games"
        )

        self.submission = ChallengeSubmission.objects.create(
            participant=participant
        )

        self.submission_referral = ChallengeSubmission.objects.create(
            participant=participant2,
            referral=referral
        )

    def test_submission_format(self):
        ma = ChallengeSubmissionAdmin(ChallengeSubmission, self.site)

        self.assertEqual(
            list(ma.get_readonly_fields(request)),
            ["view_participant_link", "view_referral_link"]
        )

        self.assertEqual(list(ma.get_exclude(request, self.submission)), ["participant", "referral"])

        link = ma.view_participant_link(self.submission)

        url = "/admin/hackerchallenge/challengeparticipant/{}".format(self.submission.participant.account_id)
        self.assertEqual(link, mark_safe("<a href='{}'>{}</a>".format(url, str(self.submission.participant))))

        link = ma.view_referral_link(self.submission)
        self.assertEqual(link, "No referral")

        link = ma.view_referral_link(self.submission_referral)
        url = "/admin/canyouhackit/vendorreferral/{}".format(self.submission_referral.referral.vendor_id)
        self.assertEqual(link, mark_safe("<a href='{}'>{}</a>".format(url, str(self.submission_referral.referral))))

        string = ma.model_string_field(self.submission)
        self.assertEqual(string, str(self.submission))
