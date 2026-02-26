# terraform-aws-ssr-cloudfront-support

Reusable CloudFront support resources for SSR stacks.

This module provisions:
- CloudFront Origin Access Identity for S3 origins
- CloudFront Origin Access Control for Lambda Function URL origins
- Origin request policy for signed Lambda origin requests
- Cache policy tuned for SSR stale-while-revalidate behavior

## Inputs

| Name | Type | Description |
| --- | --- | --- |
| app_name | string | Normalized app name used in resource names |

## Outputs

| Name | Description |
| --- | --- |
| oai_cloudfront_access_identity_path | OAI path for S3 origin config |
| oai_s3_canonical_user_id | Canonical user ID for S3 bucket policies |
| lambda_oac_id | OAC ID for Lambda origins |
| lambda_signed_origin_request_policy_id | Origin request policy ID for Lambda origins |
| ssr_swr_cache_policy_id | Cache policy ID for SSR SWR behavior |
