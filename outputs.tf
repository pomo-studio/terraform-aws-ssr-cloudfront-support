output "oai_cloudfront_access_identity_path" {
  description = "Origin access identity path, passed to a distribution so it can read from private S3 origins."
  value       = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
}

output "oai_s3_canonical_user_id" {
  description = "Canonical user ID of the origin access identity, used in S3 bucket policies to grant CloudFront read access."
  value       = aws_cloudfront_origin_access_identity.main.s3_canonical_user_id
}

output "lambda_oac_id" {
  description = "Origin access control ID used to sign CloudFront requests to Lambda function URLs."
  value       = aws_cloudfront_origin_access_control.lambda.id
}

output "lambda_signed_origin_request_policy_id" {
  description = "Origin request policy ID for Lambda origins, controlling which headers, cookies and query strings are forwarded."
  value       = aws_cloudfront_origin_request_policy.lambda_signed.id
}

output "ssr_swr_cache_policy_id" {
  description = "Cache policy ID providing stale-while-revalidate caching for SSR responses."
  value       = aws_cloudfront_cache_policy.ssr_swr.id
}
