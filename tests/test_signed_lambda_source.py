"""Source assertions only; no HCL evaluation, Terraform plan, or AWS integration.

Run from the repository root: python3 -B -m unittest discover -s tests -v
"""

from pathlib import Path
import re
import unittest


class SignedLambdaSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (Path(__file__).resolve().parents[1] / "main.tf").read_text()

    def resource(self, resource_type, name):
        # Root resource closing braces are unindented in terraform fmt output.
        match = re.search(
            rf'^resource "{resource_type}" "{name}" \{{\n(.*?)^\}}',
            self.source,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, f"Missing resource {resource_type}.{name}")
        return match.group(1)

    def test_signed_lambda_header_allowlist(self):
        policy = self.resource("aws_cloudfront_origin_request_policy", "lambda_signed")
        self.assertRegex(policy, r'header_behavior\s*=\s*"whitelist"')
        items = re.search(r'items\s*=\s*\[([^\]]*)\]', policy)
        self.assertIsNotNone(items)
        self.assertCountEqual(
            re.findall(r'"([^"]+)"', items.group(1)),
            [
                "accept", "accept-language", "cache-control", "content-type",
                "origin", "referer", "user-agent", "x-amz-content-sha256",
            ],
        )
        self.assertRegex(policy, r'cookie_behavior\s*=\s*"all"')
        self.assertRegex(policy, r'query_string_behavior\s*=\s*"all"')

    def test_lambda_oac_keeps_always_sigv4_signing(self):
        oac = self.resource("aws_cloudfront_origin_access_control", "lambda")
        for attribute, value in (
            ("origin_access_control_origin_type", "lambda"),
            ("signing_behavior", "always"),
            ("signing_protocol", "sigv4"),
        ):
            with self.subTest(attribute=attribute):
                self.assertRegex(oac, rf'{attribute}\s*=\s*"{value}"')


if __name__ == "__main__":
    unittest.main()
