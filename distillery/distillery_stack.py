from aws_cdk import (
    aws_dynamodb as _dynamodb,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_ssm as _ssm,
    core as cdk
)


class DistilleryStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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
            removal_policy = cdk.RemovalPolicy.DESTROY
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

        distillerydb = _ssm.StringParameter(
            self, 'distillerydb',
            description = 'Distillery DynamoDB Table',
            parameter_name = '/distillery/dynamodb/table',
            string_value = table.table_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

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

### SEARCH LEX V2 ###

        search = _lambda.Function(
            self, 'search',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.asset('search'),
            handler = 'search.handler',
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            architecture = _lambda.Architecture.ARM_64,
            timeout = cdk.Duration.seconds(30),
            memory_size = 128
        )

        searchlogs = _logs.LogGroup(
            self, 'searchlogs',
            log_group_name = '/aws/lambda/'+search.function_name,
            retention = _logs.RetentionDays.INFINITE,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

### SEARCH LEX V1 ###

        oldsearch = _lambda.Function(
            self, 'oldsearch',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.asset('oldsearch'),
            handler = 'oldsearch.handler',
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            architecture = _lambda.Architecture.ARM_64,
            timeout = cdk.Duration.seconds(30),
            memory_size = 128
        )

        oldsearchlogs = _logs.LogGroup(
            self, 'oldsearchlogs',
            log_group_name = '/aws/lambda/'+oldsearch.function_name,
            retention = _logs.RetentionDays.INFINITE,
            removal_policy = cdk.RemovalPolicy.DESTROY
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
            timeout = cdk.Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = awstracker.parameter_name
            ),
            memory_size = 128
        )

        awslogs = _logs.LogGroup(
            self, 'awslogs',
            log_group_name = '/aws/lambda/'+awscompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        awsevent = _events.Rule(
            self, 'awsevent',
            schedule=_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'
            )
        )
        awsevent.add_target(_targets.LambdaFunction(awscompute))

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
            timeout = cdk.Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = googletracker.parameter_name
            ),
            memory_size = 128
        )

        googlelogs = _logs.LogGroup(
            self, 'googlelogs',
            log_group_name = '/aws/lambda/'+googlecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        googleevent = _events.Rule(
            self, 'googleevent',
            schedule=_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'
            )
        )
        googleevent.add_target(_targets.LambdaFunction(googlecompute))
        
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
            timeout = cdk.Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = gcptracker.parameter_name
            ),
            memory_size = 128
        )

        gcplogs = _logs.LogGroup(
            self, 'gcplogs',
            log_group_name = '/aws/lambda/'+gcpcompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        gcpevent = _events.Rule(
            self, 'gcpevent',
            schedule=_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'
            )
        )
        gcpevent.add_target(_targets.LambdaFunction(gcpcompute))

###