# terraform-aws-ssr-cloudfront-support

The cache policies, origin request policies and origin access controls that a serverless
SSR distribution needs. Separated from the distribution itself because these are
account-level, reusable, and slow to change.

Composed by [`serverless-ssr`](https://registry.terraform.io/modules/pomo-studio/serverless-ssr/aws)
and consumed by [`ssr-cloudfront`](https://registry.terraform.io/modules/pomo-studio/ssr-cloudfront/aws),
which takes every one of this module's outputs as an input.

## What it creates

| Resource | Purpose |
|---|---|
| Origin access control | Signs CloudFront requests to Lambda function URLs |
| Origin access identity | Lets CloudFront read from private S3 buckets |
| Cache policy | Stale-while-revalidate caching for SSR responses |
| Origin request policy | Controls which headers, cookies and query strings reach the Lambda |

## Design decisions

**The cache policy honours the origin.** It forwards `Cache-Control` from the Lambda
rather than imposing a fixed TTL, so freshness is an application decision.

**The origin request policy forwards a whitelist, not everything.** `accept`,
`accept-language`, `cache-control`, `content-type`, `origin`, `referer` and `user-agent`.
Forwarding more would fragment the cache; forwarding `host` is not possible, because a
Lambda function URL behind OAC requires its own host for SigV4 signing.

## Usage

```hcl
module "cloudfront_support" {
  source  = "pomo-studio/ssr-cloudfront-support/aws"
  version = "~> 0.2"

  providers = { aws = aws.primary }

  app_name = "my-app"
}
```

Then pass its outputs to the distribution and the buckets:

```hcl
module "cloudfront" {
  source = "pomo-studio/ssr-cloudfront/aws"
  # ...
  lambda_oac_id                          = module.cloudfront_support.lambda_oac_id
  oai_cloudfront_access_identity_path    = module.cloudfront_support.oai_cloudfront_access_identity_path
  lambda_signed_origin_request_policy_id = module.cloudfront_support.lambda_signed_origin_request_policy_id
  ssr_swr_cache_policy_id                = module.cloudfront_support.ssr_swr_cache_policy_id
}

module "storage" {
  source = "pomo-studio/ssr-storage/aws"
  # ...
  cloudfront_oai_canonical_user_id = module.cloudfront_support.oai_s3_canonical_user_id
}
```

## Notes

Policy names are derived from `app_name` and must be unique within the account. Deploying
two stacks with the same `app_name` in one account will conflict.

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.0, < 7.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 6.63.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudfront_cache_policy.ssr_swr](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_cache_policy) | resource |
| [aws_cloudfront_origin_access_control.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_origin_access_control) | resource |
| [aws_cloudfront_origin_access_identity.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_origin_access_identity) | resource |
| [aws_cloudfront_origin_request_policy.lambda_signed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_origin_request_policy) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app_name"></a> [app\_name](#input\_app\_name) | Normalized app name for support resource naming | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_oac_id"></a> [lambda\_oac\_id](#output\_lambda\_oac\_id) | Origin access control ID used to sign CloudFront requests to Lambda function URLs. |
| <a name="output_lambda_signed_origin_request_policy_id"></a> [lambda\_signed\_origin\_request\_policy\_id](#output\_lambda\_signed\_origin\_request\_policy\_id) | Origin request policy ID for Lambda origins, controlling which headers, cookies and query strings are forwarded. |
| <a name="output_oai_cloudfront_access_identity_path"></a> [oai\_cloudfront\_access\_identity\_path](#output\_oai\_cloudfront\_access\_identity\_path) | Origin access identity path, passed to a distribution so it can read from private S3 origins. |
| <a name="output_oai_s3_canonical_user_id"></a> [oai\_s3\_canonical\_user\_id](#output\_oai\_s3\_canonical\_user\_id) | Canonical user ID of the origin access identity, used in S3 bucket policies to grant CloudFront read access. |
| <a name="output_ssr_swr_cache_policy_id"></a> [ssr\_swr\_cache\_policy\_id](#output\_ssr\_swr\_cache\_policy\_id) | Cache policy ID providing stale-while-revalidate caching for SSR responses. |
<!-- END_TF_DOCS -->
