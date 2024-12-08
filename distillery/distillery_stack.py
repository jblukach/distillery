import cdk_nag

from aws_cdk import (
    Aspects,
    Duration,
    RemovalPolicy,
    Stack,
    aws_certificatemanager as _acm,
    aws_cloudfront as _cloudfront,
    aws_cloudfront_origins as _origins,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_route53 as _route53,
    aws_route53_targets as _r53targets,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment,
    aws_ssm as _ssm
)

from constructs import Construct

class DistilleryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### CDK NAG ###

        Aspects.of(self).add(
            cdk_nag.AwsSolutionsChecks()
        )

        Aspects.of(self).add(
            cdk_nag.HIPAASecurityChecks()    
        )

        Aspects.of(self).add(
            cdk_nag.NIST80053R5Checks()
        )

        Aspects.of(self).add(
            cdk_nag.PCIDSS321Checks()
        )

        cdk_nag.NagSuppressions.add_stack_suppressions(
            self, suppressions = [
                {"id":"HIPAA.Security-S3BucketLevelPublicAccessProhibited","reason":"The S3 bucket does not prohibit public access through bucket level settings - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-S3BucketLoggingEnabled","reason":"The S3 Bucket does not have server access logs enabled - (Control IDs: 164.308(a)(3)(ii)(A), 164.312(b))."},
                {"id":"HIPAA.Security-S3BucketPublicReadProhibited","reason":"The S3 Bucket does not prohibit public read access through its Block Public Access configurations and bucket ACLs - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-S3BucketPublicWriteProhibited","reason":"The S3 Bucket does not prohibit public write access through its Block Public Access configurations and bucket ACLs - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-S3BucketReplicationEnabled","reason":"The S3 Bucket does not have replication enabled - (Control IDs: 164.308(a)(7)(i), 164.308(a)(7)(ii)(A), 164.308(a)(7)(ii)(B))."},
                {"id":"HIPAA.Security-S3BucketSSLRequestsOnly","reason":"The S3 Bucket or bucket policy does not require requests to use SSL - (Control IDs: 164.312(a)(2)(iv), 164.312(c)(2), 164.312(e)(1), 164.312(e)(2)(i), 164.312(e)(2)(ii))."},
                {"id":"HIPAA.Security-S3BucketVersioningEnabled","reason":"The S3 Bucket does not have versioning enabled - (Control IDs: 164.308(a)(7)(i), 164.308(a)(7)(ii)(A), 164.308(a)(7)(ii)(B), 164.312(c)(1), 164.312(c)(2))."},
                {"id":"HIPAA.Security-S3DefaultEncryptionKMS","reason":"The S3 Bucket is not encrypted with a KMS Key by default - (Control IDs: 164.312(a)(2)(iv), 164.312(e)(2)(ii))."},
                {"id":"HIPAA.Security-IAMNoInlinePolicy","reason":"The IAM Group, User, or Role contains an inline policy - (Control IDs: 164.308(a)(3)(i), 164.308(a)(3)(ii)(A), 164.308(a)(3)(ii)(B), 164.308(a)(4)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(B), 164.308(a)(4)(ii)(C), 164.312(a)(1))."},
                {"id":"HIPAA.Security-IAMPolicyNoStatementsWithAdminAccess","reason":"The IAM policy grants admin access, meaning the policy allows a principal to perform all actions on all resources - (Control IDs: 164.308(a)(3)(i), 164.308(a)(3)(ii)(A), 164.308(a)(3)(ii)(B), 164.308(a)(4)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(B), 164.308(a)(4)(ii)(C), 164.312(a)(1))."},
                {"id":"HIPAA.Security-IAMPolicyNoStatementsWithFullAccess","reason":"The IAM policy grants full access, meaning the policy allows a principal to perform all actions on individual resources - (Control IDs: 164.308(a)(3)(i), 164.308(a)(3)(ii)(A), 164.308(a)(3)(ii)(B), 164.308(a)(4)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(B), 164.308(a)(4)(ii)(C), 164.312(a)(1))."},
                {"id":"HIPAA.Security-IAMUserNoPolicies","reason":"The IAM policy is attached at the user level - (Control IDs: 164.308(a)(3)(i), 164.308(a)(3)(ii)(A), 164.308(a)(3)(ii)(B), 164.308(a)(4)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(B), 164.308(a)(4)(ii)(C), 164.312(a)(1))."},
                {"id":"HIPAA.Security-LambdaConcurrency","reason":"The Lambda function is not configured with function-level concurrent execution limits - (Control ID: 164.312(b))."},
                {"id":"HIPAA.Security-LambdaDLQ","reason":"The Lambda function is not configured with a dead-letter configuration - (Control ID: 164.312(b))."},
                {"id":"HIPAA.Security-LambdaInsideVPC","reason":"The Lambda function is not VPC enabled - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-LambdaFunctionPublicAccessProhibited","reason":"The Lambda function permission grants public access - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-CloudWatchLogGroupEncrypted","reason":"The CloudWatch Log Group is not encrypted with an AWS KMS key - (Control IDs: 164.312(a)(2)(iv), 164.312(e)(2)(ii))."},
                {"id":"HIPAA.Security-CloudWatchLogGroupRetentionPeriod","reason":"The CloudWatch Log Group does not have an explicit retention period configured - (Control ID: 164.312(b))."},
                {"id":"NIST.800.53.R5-S3BucketLevelPublicAccessProhibited","reason":"The S3 bucket does not prohibit public access through bucket level settings - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(7), SC-7(9)(a), SC-7(11), SC-7(20), SC-7(21), SC-7(24)(b), SC-7(25), SC-7(26), SC-7(27), SC-7(28), SC-25)."},
                {"id":"NIST.800.53.R5-S3BucketLoggingEnabled","reason":"The S3 Buckets does not have server access logs enabled - (Control IDs: AC-2(4), AC-3(1), AC-3(10), AC-4(26), AC-6(9), AU-2b, AU-3a, AU-3b, AU-3c, AU-3d, AU-3e, AU-3f, AU-6(3), AU-6(4), AU-6(6), AU-6(9), AU-8b, AU-10, AU-12a, AU-12c, AU-12(1), AU-12(2), AU-12(3), AU-12(4), AU-14a, AU-14b, AU-14b, AU-14(3), CA-7b, CM-5(1)(b), CM-6a, CM-9b, IA-3(3)(b), MA-4(1)(a), PM-14a.1, PM-14b, PM-31, SC-7(9)(b), SI-1(1)(c), SI-3(8)(b), SI-4(2), SI-4(17), SI-4(20), SI-7(8), SI-10(1)(c))."},
                {"id":"NIST.800.53.R5-S3BucketPublicReadProhibited","reason":"The S3 Bucket does not prohibit public read access through its Block Public Access configurations and bucket ACLs - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), CM-6a, CM-9b, MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(7), SC-7(9)(a), SC-7(11), SC-7(12), SC-7(16), SC-7(20), SC-7(21), SC-7(24)(b), SC-7(25), SC-7(26), SC-7(27), SC-7(28), SC-25)."},
                {"id":"NIST.800.53.R5-S3BucketPublicWriteProhibited","reason":"The S3 Bucket does not prohibit public write access through its Block Public Access configurations and bucket ACLs - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), CM-6a, CM-9b, MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(7), SC-7(9)(a), SC-7(11), SC-7(12), SC-7(16), SC-7(20), SC-7(21), SC-7(24)(b), SC-7(25), SC-7(26), SC-7(27), SC-7(28), SC-25)."},
                {"id":"NIST.800.53.R5-S3BucketReplicationEnabled","reason":"The S3 Bucket does not have replication enabled - (Control IDs: AU-9(2), CM-6a, CM-9b, CP-1(2), CP-2(5), CP-6a, CP-6(1), CP-6(2), CP-9a, CP-9b, CP-9c, CP-10, CP-10(2), SC-5(2), SI-13(5))."},
                {"id":"NIST.800.53.R5-S3BucketSSLRequestsOnly","reason":"The S3 Bucket or bucket policy does not require requests to use SSL - (Control IDs: AC-4, AC-4(22), AC-17(2), AC-24(1), AU-9(3), CA-9b, CM-6a, CM-9b, IA-5(1)(c), PM-11b, PM-17b, SC-7(4)(b), SC-7(4)(g), SC-8, SC-8(1), SC-8(2), SC-8(3), SC-8(4), SC-8(5), SC-13a, SC-16(1), SC-23, SI-1a.2, SI-1a.2, SI-1c.2)."},
                {"id":"NIST.800.53.R5-S3BucketVersioningEnabled","reason":"The S3 Bucket does not have versioning enabled - (Control IDs: AU-9(2), CP-1(2), CP-2(5), CP-6a, CP-6(1), CP-6(2), CP-9a, CP-9b, CP-9c, CP-10, CP-10(2), PM-11b, PM-17b, SC-5(2), SC-16(1), SI-1a.2, SI-1a.2, SI-1c.2, SI-13(5))."},
                {"id":"NIST.800.53.R5-S3DefaultEncryptionKMS","reason":"The S3 Bucket is not encrypted with a KMS Key by default - (Control IDs: AU-9(3), CP-9d, CP-9(8), SC-8(3), SC-8(4), SC-13a, SC-28(1), SI-19(4))."},
                {"id":"NIST.800.53.R5-IAMNoInlinePolicy","reason":"The IAM Group, User, or Role contains an inline policy - (Control IDs: AC-2i.2, AC-2(1), AC-2(6), AC-3, AC-3(3)(a), AC-3(3)(b)(1), AC-3(3)(b)(2), AC-3(3)(b)(3), AC-3(3)(b)(4), AC-3(3)(b)(5), AC-3(3)(c), AC-3(3), AC-3(4)(a), AC-3(4)(b), AC-3(4)(c), AC-3(4)(d), AC-3(4)(e), AC-3(4), AC-3(7), AC-3(8), AC-3(12)(a), AC-3(13), AC-3(15)(a), AC-3(15)(b), AC-4(28), AC-6, AC-6(3), AC-24, CM-5(1)(a), CM-6a, CM-9b, MP-2, SC-23(3))."},
                {"id":"NIST.800.53.R5-IAMPolicyNoStatementsWithAdminAccess","reason":"The IAM policy grants admin access, meaning the policy allows a principal to perform all actions on all resources - (Control IDs: AC-2i.2, AC-2(1), AC-2(6), AC-3, AC-3(3)(a), AC-3(3)(b)(1), AC-3(3)(b)(2), AC-3(3)(b)(3), AC-3(3)(b)(4), AC-3(3)(b)(5), AC-3(3)(c), AC-3(3), AC-3(4)(a), AC-3(4)(b), AC-3(4)(c), AC-3(4)(d), AC-3(4)(e), AC-3(4), AC-3(7), AC-3(8), AC-3(12)(a), AC-3(13), AC-3(15)(a), AC-3(15)(b), AC-4(28), AC-5b, AC-6, AC-6(2), AC-6(3), AC-6(10), AC-24, CM-5(1)(a), CM-6a, CM-9b, MP-2, SC-23(3), SC-25)."},
                {"id":"NIST.800.53.R5-IAMPolicyNoStatementsWithFullAccess","reason":"The IAM policy grants full access, meaning the policy allows a principal to perform all actions on individual resources - (Control IDs: AC-3, AC-5b, AC-6(2), AC-6(10), CM-5(1)(a))."},
                {"id":"NIST.800.53.R5-IAMUserNoPolicies","reason":"The IAM policy is attached at the user level - (Control IDs: AC-2i.2, AC-2(1), AC-2(6), AC-3, AC-3(3)(a), AC-3(3)(b)(1), AC-3(3)(b)(2), AC-3(3)(b)(3), AC-3(3)(b)(4), AC-3(3)(b)(5), AC-3(3)(c), AC-3(3), AC-3(4)(a), AC-3(4)(b), AC-3(4)(c), AC-3(4)(d), AC-3(4)(e), AC-3(4), AC-3(7), AC-3(8), AC-3(12)(a), AC-3(13), AC-3(15)(a), AC-3(15)(b), AC-4(28), AC-6, AC-6(3), AC-24, CM-5(1)(a), CM-6a, CM-9b, MP-2, SC-23(3), SC-25)."},
                {"id":"NIST.800.53.R5-LambdaConcurrency","reason":"The Lambda function is not configured with function-level concurrent execution limits - (Control IDs: AU-12(3), AU-14a, AU-14b, CA-7, CA-7b, PM-14a.1, PM-14b, PM-31, SC-6)."},
                {"id":"NIST.800.53.R5-LambdaDLQ","reason":"The Lambda function is not configured with a dead-letter configuration - (Control IDs: AU-12(3), AU-14a, AU-14b, CA-2(2), CA-7, CA-7b, PM-14a.1, PM-14b, PM-31, SC-36(1)(a), SI-2a)."},
                {"id":"NIST.800.53.R5-LambdaInsideVPC","reason":"The Lambda function is not VPC enabled - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(9)(a), SC-7(11), SC-7(12), SC-7(16), SC-7(20), SC-7(21), SC-7(24)(b), SC-25)."},
                {"id":"NIST.800.53.R5-LambdaFunctionPublicAccessProhibited","reason":"The Lambda function permission grants public access - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(7), SC-7(9)(a), SC-7(11), SC-7(12), SC-7(16), SC-7(20), SC-7(21), SC-7(24)(b), SC-7(25), SC-7(26), SC-7(27), SC-7(28), SC-25)."},
                {"id":"NIST.800.53.R5-CloudWatchLogGroupEncrypted","reason":"The CloudWatch Log Group is not encrypted with an AWS KMS key - (Control IDs: AU-9(3), CP-9d, SC-8(3), SC-8(4), SC-13a, SC-28(1), SI-19(4))."},
                {"id":"NIST.800.53.R5-CloudWatchLogGroupRetentionPeriod","reason":"The CloudWatch Log Group does not have an explicit retention period configured - (Control IDs: AC-16b, AT-4b, AU-6(3), AU-6(4), AU-6(6), AU-6(9), AU-10, AU-11(1), AU-11, AU-12(1), AU-12(2), AU-12(3), AU-14a, AU-14b, CA-7b, PM-14a.1, PM-14b, PM-21b, PM-31, SC-28(2), SI-4(17), SI-12)."},
                {"id":"PCI.DSS.321-S3BucketLevelPublicAccessProhibited","reason":"The S3 bucket does not prohibit public access through bucket level settings - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 1.3.6, 2.2.2)."},
                {"id":"PCI.DSS.321-S3BucketLoggingEnabled","reason":"The S3 Buckets does not have server access logs enabled - (Control IDs: 2.2, 10.1, 10.2.1, 10.2.2, 10.2.3, 10.2.4, 10.2.5, 10.2.7, 10.3.1, 10.3.2, 10.3.3, 10.3.4, 10.3.5, 10.3.6)."},
                {"id":"PCI.DSS.321-S3BucketPublicReadProhibited","reason":"The S3 Bucket does not prohibit public read access through its Block Public Access configurations and bucket ACLs - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 1.3.6, 2.2, 2.2.2)."},
                {"id":"PCI.DSS.321-S3BucketPublicWriteProhibited","reason":"The S3 Bucket does not prohibit public write access through its Block Public Access configurations and bucket ACLs - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 1.3.6, 2.2, 2.2.2)."},
                {"id":"PCI.DSS.321-S3BucketReplicationEnabled","reason":"The S3 Bucket does not have replication enabled - (Control IDs: 2.2, 10.5.3)."},
                {"id":"PCI.DSS.321-S3BucketSSLRequestsOnly","reason":"The S3 Bucket or bucket policy does not require requests to use SSL - (Control IDs: 2.2, 4.1, 8.2.1)."},
                {"id":"PCI.DSS.321-S3BucketVersioningEnabled","reason":"The S3 Bucket does not have versioning enabled - (Control ID: 10.5.3)."},
                {"id":"PCI.DSS.321-S3DefaultEncryptionKMS","reason":"The S3 Bucket is not encrypted with a KMS Key by default - (Control IDs: 3.4, 8.2.1, 10.5)."},
                {"id":"PCI.DSS.321-IAMNoInlinePolicy","reason":"The IAM Group, User, or Role contains an inline policy - (Control IDs: 2.2, 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-IAMPolicyNoStatementsWithAdminAccess","reason":"The IAM policy grants admin access, meaning the policy allows a principal to perform all actions on all resources - (Control IDs: 2.2, 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-IAMPolicyNoStatementsWithFullAccess","reason":"The IAM policy grants full access, meaning the policy allows a principal to perform all actions on individual resources - (Control IDs: 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-IAMUserNoPolicies","reason":"The IAM policy is attached at the user level - (Control IDs: 2.2, 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-LambdaInsideVPC","reason":"The Lambda function is not VPC enabled - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 2.2.2)."},
                {"id":"PCI.DSS.321-LambdaFunctionPublicAccessProhibited","reason":"The Lambda function permission grants public access - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 2.2.2)."},
                {"id":"PCI.DSS.321-CloudWatchLogGroupEncrypted","reason":"The CloudWatch Log Group is not encrypted with an AWS KMS key - (Control ID: 3.4)."},
                {"id":"PCI.DSS.321-CloudWatchLogGroupRetentionPeriod","reason":"The CloudWatch Log Group does not have an explicit retention period configured - (Control IDs: 3.1, 10.7)."},
                {"id":"AwsSolutions-S1","reason":"The S3 Bucket has server access logs disabled."},
                {"id":"AwsSolutions-S2","reason":"The S3 Bucket does not have public access restricted and blocked."},
                {"id":"AwsSolutions-S5","reason":"The S3 static website bucket either has an open world bucket policy or does not use a CloudFront Origin Access Identity (OAI) in the bucket policy for limited getObject and/or putObject permissions."},
                {"id":"AwsSolutions-S10","reason":"The S3 Bucket or bucket policy does not require requests to use SSL."},
                {"id":"AwsSolutions-IAM4","reason":"The IAM user, role, or group uses AWS managed policies."},
                {"id":"AwsSolutions-IAM5","reason":"The IAM entity contains wildcard permissions and does not have a cdk-nag rule suppression with evidence for those permission."},
                {"id":"AwsSolutions-L1","reason":"The non-container Lambda function is not configured to use the latest runtime version."},
                {"id":"AwsSolutions-CFR1","reason":"The CloudFront distribution may require Geo restrictions."},
                {"id":"AwsSolutions-CFR2","reason":"The CloudFront distribution may require integration with AWS WAF."},
                {"id":"AwsSolutions-CFR3","reason":"The CloudFront distribution does not have access logging enabled."},
                {"id":"AwsSolutions-CFR4","reason":"The CloudFront distribution allows for SSLv3 or TLSv1 for HTTPS viewer connections."},
                {"id":"AwsSolutions-CFR5","reason":"The CloudFront distributions uses SSLv3 or TLSv1 for communication to the origin."},
                {"id":"AwsSolutions-CFR7","reason":"The CloudFront distribution does not use an origin access control with an S3 origin."},
            ]
        )

    ### LAMBDA LAYERS ###

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:getpublicip:14'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:requests:7'
        )

    ### S3 BUCKET ###

        bucket = _s3.Bucket(
            self, 'bucket',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'copyfiles',
            sources = [
                _deployment.Source.asset('code')
            ],
            destination_bucket = bucket,
            prune = False
        )

        distillerystagebucket = _s3.Bucket(
            self, 'distillerystagebucket',
            bucket_name = 'distillerystagebucket',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

    ### PARAMETER ###

        parameter = _ssm.StringParameter(
            self, 'parameter',
            description = 'Distillery Status Change',
            parameter_name = '/distillery/status',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

    ### LAMBDA ###

        search = _lambda.Function(
            self, 'search',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('search'),
            timeout = Duration.seconds(7),
            handler = 'search.handler',
            environment = dict(
                AWS_ACCOUNT = account
            ),
            memory_size = 128,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        url = search.add_function_url(
            auth_type = _lambda.FunctionUrlAuthType.NONE
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+search.function_name,
            retention = _logs.RetentionDays.THIRTEEN_MONTHS,
            removal_policy = RemovalPolicy.DESTROY
        )

    ### IAM ###

        buildrole = _iam.Role(
            self, 'buildrole',
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        buildrole.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        buildrole.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    's3:GetBucketLocation',
                    's3:GetObject',
                    's3:ListBucket',
                    's3:PutObject'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        build = _lambda.Function(
            self, 'build',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('build'),
            timeout = Duration.seconds(900),
            handler = 'build.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'distillerystagebucket',
                UP_BUCKET = bucket.bucket_name
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = buildrole,
            layers = [
                getpublicip
            ]
        )

        buildlogs = _logs.LogGroup(
            self, 'buildlogs',
            log_group_name = '/aws/lambda/'+build.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        buildevent = _events.Rule(
            self, 'buildevent',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        buildevent.add_target(
            _targets.LambdaFunction(build)
        )

    ### IAM ###

        deployrole = _iam.Role(
            self, 'deployrole',
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        deployrole.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        deployrole.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'lambda:UpdateFunctionCode',
                    's3:GetObject',
                    's3:PutObject',
                    'ssm:GetParameter',
                    'ssm:PutParameter'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        deploy = _lambda.Function(
            self, 'deploy',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('deploy'),
            timeout = Duration.seconds(900),
            handler = 'deploy.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DEPLOY_BUCKET = bucket.bucket_name,
                LAMBDA_FUNCTION = search.function_name,
                SSM_PARAMETER_GIT = '/github/releases',
                SSM_PARAMETER_STATUS = parameter.parameter_name
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = deployrole,
            layers = [
                getpublicip,
                requests
            ]
        )

        deploylogs = _logs.LogGroup(
            self, 'deploylogs',
            log_group_name = '/aws/lambda/'+deploy.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        deployevent = _events.Rule(
            self, 'deployevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        deployevent.add_target(
            _targets.LambdaFunction(deploy)
        )

    ### HOSTZONE ###

        hostzoneid = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'hostzoneid',
            parameter_name = '/r53/tundralabs.net'
        )

        hostzone = _route53.HostedZone.from_hosted_zone_attributes(
             self, 'hostzone',
             hosted_zone_id = hostzoneid.string_value,
             zone_name = 'tundralabs.net'
        )   

        cdnlogs = _logs.LogGroup(
            self, 'cdnlogs',
            log_group_name = '/aws/cloudfront/cidrtundralabsnet',
            retention = _logs.RetentionDays.THIRTEEN_MONTHS,
            removal_policy = RemovalPolicy.DESTROY
        )

    ### ACM CERTIFICATE ###

        acm = _acm.Certificate(
            self, 'acm',
            domain_name = 'cidr.tundralabs.net',
            validation = _acm.CertificateValidation.from_dns(hostzone)
        )

    ### CLOUDFRONT ###

        cidrdistribution = _cloudfront.Distribution(
            self, 'cidrdistribution',
            comment = 'cidr.tundralabs.net',
            default_behavior = _cloudfront.BehaviorOptions(
                origin = _origins.FunctionUrlOrigin(url),
                viewer_protocol_policy = _cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy = _cloudfront.CachePolicy.CACHING_DISABLED
            ),
            domain_names = [
                'cidr.tundralabs.net'
            ],
            error_responses = [
                _cloudfront.ErrorResponse(
                    http_status = 404,
                    response_http_status = 200,
                    response_page_path = '/'
                )
            ],
            certificate = acm,
            minimum_protocol_version = _cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            price_class = _cloudfront.PriceClass.PRICE_CLASS_100,
            http_version = _cloudfront.HttpVersion.HTTP2_AND_3,
            enable_ipv6 = True
        )

    ### DNS ENTRY ###

        cidrurl = _route53.ARecord(
            self, 'cidrurl',
            zone = hostzone,
            record_name = 'cidr.tundralabs.net',
            target = _route53.RecordTarget.from_alias(_r53targets.CloudFrontTarget(cidrdistribution))
        )
