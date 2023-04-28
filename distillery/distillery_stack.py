import cdk_nag

from aws_cdk import (
    Aspects,
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as _dynamodb,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_logs_destinations as _destinations,
    aws_sns_subscriptions as _subs,
    aws_ssm as _ssm,
)

from constructs import Construct

class DistilleryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

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
                {"id":"AwsSolutions-DDB3","reason":"The DynamoDB table does not have Point-in-time Recovery enabled."},
                {"id":"AwsSolutions-IAM4","reason":"The IAM user, role, or group uses AWS managed policies."},
                {"id":"AwsSolutions-IAM5","reason":"The IAM entity contains wildcard permissions and does not have a cdk-nag rule suppression with evidence for those permission."},
                {"id":"AwsSolutions-L1","reason":"The non-container Lambda function is not configured to use the latest runtime version."},
                {"id":"HIPAA.Security-DynamoDBAutoScalingEnabled","reason":"The provisioned capacity DynamoDB table does not have Auto Scaling enabled on it's indexes - (Control IDs: 164.308(a)(7)(i), 164.308(a)(7)(ii)(C))."},
                {"id":"HIPAA.Security-DynamoDBInBackupPlan","reason":"The DynamoDB table is not in an AWS Backup plan - (Control IDs: 164.308(a)(7)(i), 164.308(a)(7)(ii)(A), 164.308(a)(7)(ii)(B))."},
                {"id":"HIPAA.Security-DynamoDBPITREnabled","reason":"The DynamoDB table does not have Point-in-time Recovery enabled - (Control IDs: 164.308(a)(7)(i), 164.308(a)(7)(ii)(A), 164.308(a)(7)(ii)(B))."},
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
                {"id":"NIST.800.53.R5-DynamoDBAutoScalingEnabled","reason":"The provisioned capacity DynamoDB table does not have Auto Scaling enabled on it's indexes - (Control IDs: CP-1a.1(b), CP-1a.2, CP-2a, CP-2a.6, CP-2a.7, CP-2d, CP-2e, CP-2(5), CP-2(6), CP-6(2), CP-10, SC-5(2), SC-6, SC-22, SC-36, SI-13(5))."},
                {"id":"NIST.800.53.R5-DynamoDBInBackupPlan","reason":"The DynamoDB table is not in an AWS Backup plan - (Control IDs: CP-1(2), CP-2(5), CP-6a, CP-6(1), CP-6(2), CP-9a, CP-9b, CP-9c, CP-10, CP-10(2), SC-5(2), SI-13(5))."},
                {"id":"NIST.800.53.R5-DynamoDBPITREnabled","reason":"The DynamoDB table does not have Point-in-time Recovery enabled - (Control IDs: CP-1(2), CP-2(5), CP-6(2), CP-9a, CP-9b, CP-9c, CP-10, CP-10(2), SC-5(2), SI-13(5))."},
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
                {"id":"PCI.DSS.321-IAMNoInlinePolicy","reason":"The IAM Group, User, or Role contains an inline policy - (Control IDs: 2.2, 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-IAMPolicyNoStatementsWithAdminAccess","reason":"The IAM policy grants admin access, meaning the policy allows a principal to perform all actions on all resources - (Control IDs: 2.2, 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-IAMPolicyNoStatementsWithFullAccess","reason":"The IAM policy grants full access, meaning the policy allows a principal to perform all actions on individual resources - (Control IDs: 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-IAMUserNoPolicies","reason":"The IAM policy is attached at the user level - (Control IDs: 2.2, 7.1.2, 7.1.3, 7.2.1, 7.2.2)."},
                {"id":"PCI.DSS.321-LambdaInsideVPC","reason":"The Lambda function is not VPC enabled - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 2.2.2)."},
                {"id":"PCI.DSS.321-LambdaFunctionPublicAccessProhibited","reason":"The Lambda function permission grants public access - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 2.2.2)."},
                {"id":"PCI.DSS.321-CloudWatchLogGroupEncrypted","reason":"The CloudWatch Log Group is not encrypted with an AWS KMS key - (Control ID: 3.4)."},
                {"id":"PCI.DSS.321-CloudWatchLogGroupRetentionPeriod","reason":"The CloudWatch Log Group does not have an explicit retention period configured - (Control IDs: 3.1, 10.7)."},
            ]
        )

    ### LAMBDA LAYER ###

        layer = _lambda.LayerVersion.from_layer_version_arn(
            self, 'layer',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:5'
        )

    ### DYNAMODB ###

        table = _dynamodb.Table(
            self, 'cidr',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'sk',
                'type': _dynamodb.AttributeType.STRING
            },
            billing_mode = _dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery = True,
            removal_policy = RemovalPolicy.DESTROY
        )

        table.add_global_secondary_index(
            index_name = 'firstip',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'firstip',
                'type': _dynamodb.AttributeType.NUMBER
            },
            projection_type = _dynamodb.ProjectionType.INCLUDE,
            non_key_attributes = ['created']
        )

        table.add_global_secondary_index(
            index_name = 'lastip',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'lastip',
                'type': _dynamodb.AttributeType.NUMBER
            },
            projection_type = _dynamodb.ProjectionType.INCLUDE,
            non_key_attributes = ['created']
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

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'dynamodb:PutItem',
                    'dynamodb:Query',
                    'ssm:GetParameter',
                    'ssm:PutParameter',
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### ERROR ###

        error = _lambda.Function.from_function_arn(
            self, 'error',
            'arn:aws:lambda:'+region+':'+account+':function:shipit-error'
        )

        timeout = _lambda.Function.from_function_arn(
            self, 'timeout',
            'arn:aws:lambda:'+region+':'+account+':function:shipit-timeout'
        )

    ### SEARCH ###

        search = _lambda.Function(
            self, 'search',
            function_name = 'cidr',
            runtime = _lambda.Runtime.PYTHON_3_10,
            code = _lambda.Code.from_asset('search'),
            handler = 'search.handler',
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            architecture = _lambda.Architecture.ARM_64,
            timeout = Duration.seconds(60),
            memory_size = 512,
            layers = [
                layer
            ]
        )

        url = search.add_function_url(
            auth_type = _lambda.FunctionUrlAuthType.NONE
        )

        parameter = _ssm.StringParameter(
            self, 'parameter',
            description = 'Distillery Lambda URL',
            parameter_name = '/distillery/lambda/url',
            string_value = url.url,
            tier = _ssm.ParameterTier.STANDARD,
        )

        searchlogs = _logs.LogGroup(
            self, 'searchlogs',
            log_group_name = '/aws/lambda/'+search.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        searchsub = _logs.SubscriptionFilter(
            self, 'searchsub',
            log_group = searchlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        searchtime= _logs.SubscriptionFilter(
            self, 'searchtime',
            log_group = searchlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

    ### AWS CIDRS ###

        awstracker = _ssm.StringParameter(
            self, 'awstracker',
            description = 'AWS Distillery Tracker',
            parameter_name = '/distillery/tracker/aws',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        awscompute = _lambda.DockerImageFunction(
            self, 'awscompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/aws'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = awstracker.parameter_name
            ),
            memory_size = 512
        )

        awslogs = _logs.LogGroup(
            self, 'awslogs',
            log_group_name = '/aws/lambda/'+awscompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        awssub = _logs.SubscriptionFilter(
            self, 'awssub',
            log_group = awslogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        awstime = _logs.SubscriptionFilter(
            self, 'awstime',
            log_group = awslogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        awsevent = _events.Rule(
            self, 'awsevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        awsevent.add_target(
            _targets.LambdaFunction(awscompute)
        )

    ### GOOGLE CIDRS ###

        googletracker = _ssm.StringParameter(
            self, 'googletracker',
            description = 'Google Distillery Tracker',
            parameter_name = '/distillery/tracker/google',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        googlecompute = _lambda.DockerImageFunction(
            self, 'googlecompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/google'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = googletracker.parameter_name
            ),
            memory_size = 512
        )

        googlelogs = _logs.LogGroup(
            self, 'googlelogs',
            log_group_name = '/aws/lambda/'+googlecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        googlesub = _logs.SubscriptionFilter(
            self, 'googlesub',
            log_group = googlelogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        googletime = _logs.SubscriptionFilter(
            self, 'googletime',
            log_group = googlelogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        googleevent = _events.Rule(
            self, 'googleevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        googleevent.add_target(
            _targets.LambdaFunction(googlecompute)
        )
        
    ### GCP CIDRS ###

        gcptracker = _ssm.StringParameter(
            self, 'gcptracker',
            description = 'GCP Distillery Tracker',
            parameter_name = '/distillery/tracker/gcp',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        gcpcompute = _lambda.DockerImageFunction(
            self, 'gcpcompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/gcp'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = gcptracker.parameter_name
            ),
            memory_size = 512
        )

        gcplogs = _logs.LogGroup(
            self, 'gcplogs',
            log_group_name = '/aws/lambda/'+gcpcompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        gcpsub = _logs.SubscriptionFilter(
            self, 'gcpsub',
            log_group = gcplogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        gcptime = _logs.SubscriptionFilter(
            self, 'gcptime',
            log_group = gcplogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        gcpevent = _events.Rule(
            self, 'gcpevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        gcpevent.add_target(
            _targets.LambdaFunction(gcpcompute)
        )

    ### AZURE CIDRS ###

        azuretracker = _ssm.StringParameter(
            self, 'azuretracker',
            description = 'Azure Distillery Tracker',
            parameter_name = '/distillery/tracker/azure',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        azurecompute = _lambda.DockerImageFunction(
            self, 'azurecompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/azure'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = azuretracker.parameter_name
            ),
            memory_size = 512
        )

        azurelogs = _logs.LogGroup(
            self, 'azurelogs',
            log_group_name = '/aws/lambda/'+azurecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        azuresub = _logs.SubscriptionFilter(
            self, 'azuresub',
            log_group = azurelogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        azuretime = _logs.SubscriptionFilter(
            self, 'azuretime',
            log_group = azurelogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        azureevent = _events.Rule(
            self, 'azureevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        azureevent.add_target(
            _targets.LambdaFunction(azurecompute)
        )

    ### CLOUDFLARE CIDRS ###

        cloudflarecompute = _lambda.DockerImageFunction(
            self, 'cloudflarecompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/cloudflare'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            memory_size = 512
        )

        cloudflarelogs = _logs.LogGroup(
            self, 'cloudflarelogs',
            log_group_name = '/aws/lambda/'+cloudflarecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        cloudflaresub = _logs.SubscriptionFilter(
            self, 'cloudflaresub',
            log_group = cloudflarelogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        cloudflaretime = _logs.SubscriptionFilter(
            self, 'cloudflaretime',
            log_group = cloudflarelogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        cloudflareevent = _events.Rule(
            self, 'cloudflareevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        cloudflareevent.add_target(
            _targets.LambdaFunction(cloudflarecompute)
        )

    ### DIGITAL OCEAN CIDRS ###

        docompute = _lambda.DockerImageFunction(
            self, 'docompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/do'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            memory_size = 512
        )

        dologs = _logs.LogGroup(
            self, 'dologs',
            log_group_name = '/aws/lambda/'+docompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        dosub = _logs.SubscriptionFilter(
            self, 'dosub',
            log_group = dologs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        dotime = _logs.SubscriptionFilter(
            self, 'dotime',
            log_group = dologs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        doevent = _events.Rule(
            self, 'doevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        doevent.add_target(
            _targets.LambdaFunction(docompute)
        )

    ### ORACLE CIDRS ###

        oracletracker = _ssm.StringParameter(
            self, 'oracletracker',
            description = 'Oracle Distillery Tracker',
            parameter_name = '/distillery/tracker/oracle',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        oraclecompute = _lambda.DockerImageFunction(
            self, 'oraclecompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/oracle'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = oracletracker.parameter_name
            ),
            memory_size = 512
        )

        oraclelogs = _logs.LogGroup(
            self, 'oraclelogs',
            log_group_name = '/aws/lambda/'+oraclecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        oraclesub = _logs.SubscriptionFilter(
            self, 'oraclesub',
            log_group = oraclelogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        oracletime = _logs.SubscriptionFilter(
            self, 'oracletime',
            log_group = oraclelogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        oracleevent = _events.Rule(
            self, 'oracleevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        oracleevent.add_target(
            _targets.LambdaFunction(oraclecompute)
        )
        
    ### O365 CIDRS ###

        o365trackerworldwide = _ssm.StringParameter(
            self, 'o365trackerworldwide',
            description = 'o365 Distillery Tracker - Worldwide',
            parameter_name = '/distillery/tracker/o365/worldwide',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        o365trackerusgovdod = _ssm.StringParameter(
            self, 'o365trackerusgovdod',
            description = 'o365 Distillery Tracker - USGovDoD',
            parameter_name = '/distillery/tracker/o365/usgovdod',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )
        
        o365trackerusgovgcchigh = _ssm.StringParameter(
            self, 'o365trackerusgovgcchigh',
            description = 'o365 Distillery Tracker - USGovGCCHigh',
            parameter_name = '/distillery/tracker/o365/usgovgcchigh',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )
        
        o365trackerchina = _ssm.StringParameter(
            self, 'o365trackerchina',
            description = 'o365 Distillery Tracker - China',
            parameter_name = '/distillery/tracker/o365/china',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )
        
        o365trackergermany = _ssm.StringParameter(
            self, 'o365trackergermany',
            description = 'o365 Distillery Tracker - Germany',
            parameter_name = '/distillery/tracker/o365/germany',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        o365compute = _lambda.DockerImageFunction(
            self, 'o365compute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/o365'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                WORLD_PARAMETER = o365trackerworldwide.parameter_name,
                DOD_PARAMETER = o365trackerusgovdod.parameter_name,
                HIGH_PARAMETER = o365trackerusgovgcchigh.parameter_name,
                CHINA_PARAMETER = o365trackerchina.parameter_name,
                GERMANY_PARAMETER = o365trackergermany.parameter_name
            ),
            memory_size = 512
        )

        o365logs = _logs.LogGroup(
            self, 'o365logs',
            log_group_name = '/aws/lambda/'+o365compute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        o365sub = _logs.SubscriptionFilter(
            self, 'o365sub',
            log_group = o365logs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        o365time = _logs.SubscriptionFilter(
            self, 'o365time',
            log_group = o365logs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        o365event = _events.Rule(
            self, 'o365event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        o365event.add_target(
            _targets.LambdaFunction(o365compute)
        )

    ### NETSPI CIDRS ###

        netspicompute = _lambda.DockerImageFunction(
            self, 'netspicompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/netspi'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            memory_size = 512
        )

        netspilogs = _logs.LogGroup(
            self, 'netspilogs',
            log_group_name = '/aws/lambda/'+netspicompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        netspisub = _logs.SubscriptionFilter(
            self, 'netspisub',
            log_group = netspilogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        netspitime = _logs.SubscriptionFilter(
            self, 'netspitime',
            log_group = netspilogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        netspievent = _events.Rule(
            self, 'netspievent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        netspievent.add_target(
            _targets.LambdaFunction(netspicompute)
        )

    ### TENABLE CIDRS ###

        tenabletracker = _ssm.StringParameter(
            self, 'tenabletracker',
            description = 'Tenable Distillery Tracker',
            parameter_name = '/distillery/tracker/tenable',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        tenablecompute = _lambda.DockerImageFunction(
            self, 'tenablecompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/tenable'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = tenabletracker.parameter_name
            ),
            memory_size = 512
        )

        tenablelogs = _logs.LogGroup(
            self, 'tenablelogs',
            log_group_name = '/aws/lambda/'+tenablecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        tenablesub = _logs.SubscriptionFilter(
            self, 'tenablesub',
            log_group = tenablelogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        tenabletime = _logs.SubscriptionFilter(
            self, 'tenabletime',
            log_group = tenablelogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        tenableevent = _events.Rule(
            self, 'tenableevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        tenableevent.add_target(
            _targets.LambdaFunction(tenablecompute)
        )

    ### VULTR CIDRS ###

        vultrtracker = _ssm.StringParameter(
            self, 'vultrtracker',
            description = 'Vultr Distillery Tracker',
            parameter_name = '/distillery/tracker/vultr',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        vultrcompute = _lambda.DockerImageFunction(
            self, 'vultrcompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/vultr'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = vultrtracker.parameter_name
            ),
            memory_size = 512
        )

        vultrlogs = _logs.LogGroup(
            self, 'vultrlogs',
            log_group_name = '/aws/lambda/'+vultrcompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        vultrsub = _logs.SubscriptionFilter(
            self, 'vultrsub',
            log_group = vultrlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        vultrtime = _logs.SubscriptionFilter(
            self, 'vultrtime',
            log_group = vultrlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        vultrevent = _events.Rule(
            self, 'vultrevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        vultrevent.add_target(
            _targets.LambdaFunction(vultrcompute)
        )

    ### OKTA CIDRS ###

        oktacompute = _lambda.DockerImageFunction(
            self, 'oktacompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/okta'),
            timeout = Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            memory_size = 512
        )

        oktalogs = _logs.LogGroup(
            self, 'oktalogs',
            log_group_name = '/aws/lambda/'+oktacompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        oktasub = _logs.SubscriptionFilter(
            self, 'oktasub',
            log_group = oktalogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        oktatime = _logs.SubscriptionFilter(
            self, 'oktatime',
            log_group = oktalogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        oktaevent = _events.Rule(
            self, 'oktaevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        oktaevent.add_target(
            _targets.LambdaFunction(oktacompute)
        )
