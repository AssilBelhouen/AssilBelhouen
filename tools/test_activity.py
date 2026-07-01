import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import unittest
import urllib.error
import xml.etree.ElementTree as ET
from update_activity import ActivityError, fetch_activity, normalize, render, window

def sample():
    return {'data': {'viewer': {'login': 'AssilBelhouen'}, 'user': {'contributionsCollection': {
        'restrictedContributionsCount': 40, 'totalCommitContributions': 50,
        'totalPullRequestContributions': 8, 'totalPullRequestReviewContributions': 2,
        'contributionCalendar': {'totalContributions': 100}}}}}

class Response(io.BytesIO):
    headers = {'X-OAuth-Scopes': 'read:user'}

class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.end = dt.datetime(2026,10,11,12,tzinfo=dt.timezone.utc)
        self.start,self.end = window(self.end)

    def test_private_counts_are_not_added_twice(self):
        counts = normalize(sample())
        self.assertEqual(counts['contributions'],100)
        self.assertEqual(counts['restricted'],40)

    def test_success_and_private_response_not_persisted(self):
        payload = sample()
        payload['data']['private_repository_name'] = 'PRIVATE-NAME-MUST-NOT-LEAK'
        counts = fetch_activity('SECRET-MUST-NOT-LEAK',self.start,self.end,
            opener=lambda *a,**k: Response(json.dumps(payload).encode()))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertEqual(render(out,counts,self.start,self.end),3)
            self.assertEqual(render(out,counts,self.start,self.end),0)
            for file in out.iterdir():
                text = file.read_text(encoding='utf-8')
                self.assertNotIn('MUST-NOT-LEAK',text)
                if file.suffix == '.svg': ET.fromstring(text)

    def test_missing_token_before_any_request(self):
        with self.assertRaisesRegex(ActivityError,'missing'):
            fetch_activity('',self.start,self.end,opener=lambda *a,**k: self.fail('Network should not run'))

    def test_failed_api_preserves_previous_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            render(out,normalize(sample()),self.start,self.end)
            before={p.name:p.read_bytes() for p in out.iterdir()}
            def fail(*args,**kwargs):
                raise urllib.error.HTTPError('https://api.github.com/graphql',401,'SECRET',{},None)
            with self.assertRaisesRegex(ActivityError,'HTTP 401'):
                fetch_activity('secret',self.start,self.end,opener=fail)
            self.assertEqual(before,{p.name:p.read_bytes() for p in out.iterdir()})

    def test_graphql_error_is_redacted(self):
        with self.assertRaises(ActivityError) as caught:
            normalize({'errors':[{'message':'private-name secret'}]})
        self.assertNotIn('private-name',str(caught.exception))

    def test_invalid_counts_and_wrong_owner_fail(self):
        payload=sample(); payload['data']['viewer']['login']='SomeoneElse'
        with self.assertRaises(ActivityError): normalize(payload)
        payload=sample(); payload['data']['user']['contributionsCollection']['totalCommitContributions']=-1
        with self.assertRaises(ActivityError): normalize(payload)

    def test_leap_day_window(self):
        start,_=window(dt.datetime(2024,2,29,tzinfo=dt.timezone.utc))
        self.assertEqual(str(start.date()),'2023-02-28')

if __name__ == '__main__': unittest.main()
