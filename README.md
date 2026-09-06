# terraform-aws-ssr-cloudfront-support

[![Terraform Validation](https://github.com/pomo-studio/terraform-aws-ssr-cloudfront-support/actions/workflows/terraform.yml/badge.svg)](https://github.com/pomo-studio/terraform-aws-ssr-cloudfront-support/actions/workflows/terraform.yml)
[![Terraform Registry](https://img.shields.io/badge/terraform-registry-844FBA?logo=terraform)](https://registry.terraform.io/modules/pomo-studio/ssr-cloudfront-support/aws)

- [Changelog](CHANGELOG.md)

Reusable CloudFront support resources for SSR stacks.

This module provisions:
- CloudFront Origin Access Identity for S3 origins
- CloudFront Origin Access Control for Lambda Function URL origins
- Origin request policy for signed Lambda origin requests
- Cache policy tuned for SSR stale-while-revalidate behavior

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
| <a name="output_lambda_oac_id"></a> [lambda\_oac\_id](#output\_lambda\_oac\_id) | n/a |
| <a name="output_lambda_signed_origin_request_policy_id"></a> [lambda\_signed\_origin\_request\_policy\_id](#output\_lambda\_signed\_origin\_request\_policy\_id) | n/a |
| <a name="output_oai_cloudfront_access_identity_path"></a> [oai\_cloudfront\_access\_identity\_path](#output\_oai\_cloudfront\_access\_identity\_path) | n/a |
| <a name="output_oai_s3_canonical_user_id"></a> [oai\_s3\_canonical\_user\_id](#output\_oai\_s3\_canonical\_user\_id) | n/a |
| <a name="output_ssr_swr_cache_policy_id"></a> [ssr\_swr\_cache\_policy\_id](#output\_ssr\_swr\_cache\_policy\_id) | n/a |
<!-- END_TF_DOCS -->
