import cdk_nag

from aws_cdk import (
    Aspects,
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_logs_destinations as _destinations,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment
)

from constructs import Construct

class DistilleryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### CDK NAG ###

        Aspects.of(self).add(
            cdk_nag.AwsSolutionsChecks(
                log_ignores = True,
                verbose = True
            )
        )

        cdk_nag.NagSuppressions.add_stack_suppressions(
            self, suppressions = [
                {"id":"AwsSolutions-S1","reason":"The S3 Bucket has server access logs disabled."},
                {"id":"AwsSolutions-S2","reason":"The S3 Bucket does not have public access restricted and blocked."},
                {"id":"AwsSolutions-S5","reason":"The S3 static website bucket either has an open world bucket policy or does not use a CloudFront Origin Access Identity (OAI) in the bucket policy for limited getObject and/or putObject permissions."},
                {"id":"AwsSolutions-S10","reason":"The S3 Bucket or bucket policy does not require requests to use SSL."},
                {"id":"AwsSolutions-IAM4","reason":"The IAM user, role, or group uses AWS managed policies."},
                {"id":"AwsSolutions-IAM5","reason":"The IAM entity contains wildcard permissions and does not have a cdk-nag rule suppression with evidence for those permission."},
                {"id":"AwsSolutions-L1","reason":"The non-container Lambda function is not configured to use the latest runtime version."},
            ]
        )

    ### LAMBDA LAYERS ###

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:10'
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
            runtime = _lambda.Runtime.PYTHON_3_12,
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
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        sub = _logs.SubscriptionFilter(
            self, 'sub',
            log_group = logs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        time = _logs.SubscriptionFilter(
            self, 'time',
            log_group = logs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
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
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('build'),
            timeout = Duration.seconds(900),
            handler = 'build.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'stage.tundralabs.net',
                UP_BUCKET = 'static.tundralabs.net'
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
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        buildsub = _logs.SubscriptionFilter(
            self, 'buildsub',
            log_group = buildlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        buildtime = _logs.SubscriptionFilter(
            self, 'buildtime',
            log_group = buildlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        buildevent = _events.Rule(
            self, 'buildevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '10',
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
                    's3:PutObject'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        deploy = _lambda.Function(
            self, 'deploy',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('deploy'),
            timeout = Duration.seconds(900),
            handler = 'deploy.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DEPLOY_BUCKET = bucket.bucket_name,
                DOWN_BUCKET = 'static.tundralabs.net'
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = deployrole,
            layers = [
                getpublicip
            ]
        )

        deploylogs = _logs.LogGroup(
            self, 'deploylogs',
            log_group_name = '/aws/lambda/'+deploy.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        deploysub = _logs.SubscriptionFilter(
            self, 'deploysub',
            log_group = deploylogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        deploytime = _logs.SubscriptionFilter(
            self, 'deploytime',
            log_group = deploylogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        deployevent = _events.Rule(
            self, 'deployevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        #deployevent.add_target(
        #    _targets.LambdaFunction(deploy)
        #)
