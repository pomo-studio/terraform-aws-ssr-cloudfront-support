# terraform-aws-ssr-cloudfront-support

[![Terraform Validation](https://github.com/pomo-studio/terraform-aws-ssr-cloudfront-support/actions/workflows/terraform.yml/badge.svg)](https://github.com/pomo-studio/terraform-aws-ssr-cloudfront-support/actions/workflows/terraform.yml)
[![Terraform Registry](https://img.shields.io/badge/terraform-registry-844FBA?logo=terraform)](https://registry.terraform.io/modules/pomo-studio/ssr-cloudfront-support/aws)

[Changelog](CHANGELOG.md)

The policies a server-rendered CloudFront distribution needs: what to cache, what to forward to the origin, and how to reach private Lambda and S3 origins.

## When to use it

Create the CloudFront support policies instead of hand-writing them: origin access control for a Lambda function URL, an origin access identity for a private S3 bucket, a cache policy, and an origin request policy. Use it for any distribution that reads from a Lambda function URL and a private bucket.

It is also the policy layer of the [Serverless SSR blueprint](https://registry.terraform.io/modules/pomo-studio/serverless-ssr/aws). On its own it serves no traffic; it exists so the distribution can stay focused on routing.

## Quickstart

```hcl
module "cloudfront_support" {
  source  = "pomo-studio/ssr-cloudfront-support/aws"
  version = "~> 0.2"

  providers = { aws = aws.primary }

  app_name = "my-app"
}
```

Hand the outputs to the distribution and the buckets:

```hcl
module "cloudfront" {
  # ...
  lambda_oac_id                          = module.cloudfront_support.lambda_oac_id
  oai_cloudfront_access_identity_path    = module.cloudfront_support.oai_cloudfront_access_identity_path
  lambda_signed_origin_request_policy_id = module.cloudfront_support.lambda_signed_origin_request_policy_id
  ssr_swr_cache_policy_id                = module.cloudfront_support.ssr_swr_cache_policy_id
}

module "storage" {
  # ...
  cloudfront_oai_canonical_user_id = module.cloudfront_support.oai_s3_canonical_user_id
}
```

## What it creates

| | |
|---|---|
| Origin access control | Lets CloudFront sign requests to a Lambda function URL |
| Origin access identity | Lets CloudFront read a private S3 bucket |
| Cache policy | Caches server-rendered pages, and serves a stale copy while refreshing |
| Origin request policy | Decides which headers, cookies and query strings reach the Lambda |

## Design decisions

- **The app decides freshness.** The cache policy passes through the `Cache-Control` header your Lambda sends rather than imposing a fixed time, so caching is a decision you make in code.
- **Only seven headers reach the origin.** Forwarding more splits the cache and lowers the hit rate. `host` is not among them and cannot be, because a Lambda function URL needs its own hostname to verify the signed request.
- **Names come from `app_name`.** Two stacks sharing an `app_name` in one AWS account collide, so keep it unique.

## Reference

<details>
<summary>Reference</summary>

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.0, < 7.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 6.64.0 |

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

</details>

## Support and license

Part of [postmodern.tf](https://pomo.dev), the open-source AWS infrastructure
collection created by [André Pitanga](https://pomo.studio). Regenerate the reference with `terraform-docs` v0.20.0 (`terraform-docs .`); CI fails on drift.

See the [contribution guide](https://github.com/pomo-studio/.github/blob/main/CONTRIBUTING.md) and [security policy](https://github.com/pomo-studio/.github/blob/main/SECURITY.md).

MIT licensed. See [LICENSE](LICENSE).
