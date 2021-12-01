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
            code = _lambda.Code.from_asset('search'),
            handler = 'search.handler',
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            architecture = _lambda.Architecture.ARM_64,
            timeout = cdk.Duration.seconds(30),
            memory_size = 512
        )

        searchlogs = _logs.LogGroup(
            self, 'searchlogs',
            log_group_name = '/aws/lambda/'+search.function_name,
            retention = _logs.RetentionDays.INFINITE,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        searchmonitor = _ssm.StringParameter(
            self, 'searchmonitor',
            description = 'Search Distillery Monitor',
            parameter_name = '/distillery/monitor/search',
            string_value = '/aws/lambda/'+search.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

### SEARCH LEX V1 ###

        oldsearch = _lambda.Function(
            self, 'oldsearch',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.from_asset('oldsearch'),
            handler = 'oldsearch.handler',
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name
            ),
            architecture = _lambda.Architecture.ARM_64,
            timeout = cdk.Duration.seconds(30),
            memory_size = 512
        )

        oldsearchlogs = _logs.LogGroup(
            self, 'oldsearchlogs',
            log_group_name = '/aws/lambda/'+oldsearch.function_name,
            retention = _logs.RetentionDays.INFINITE,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        oldsearchmonitor = _ssm.StringParameter(
            self, 'oldsearchmonitor',
            description = 'Old Search Distillery Monitor',
            parameter_name = '/distillery/monitor/oldsearch',
            string_value = '/aws/lambda/'+oldsearch.function_name,
            tier = _ssm.ParameterTier.STANDARD,
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
            memory_size = 512
        )

        awslogs = _logs.LogGroup(
            self, 'awslogs',
            log_group_name = '/aws/lambda/'+awscompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        awsmonitor = _ssm.StringParameter(
            self, 'awsmonitor',
            description = 'AWS Distillery Monitor',
            parameter_name = '/distillery/monitor/aws',
            string_value = '/aws/lambda/'+awscompute.function_name,
            tier = _ssm.ParameterTier.STANDARD,
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
            memory_size = 512
        )

        googlelogs = _logs.LogGroup(
            self, 'googlelogs',
            log_group_name = '/aws/lambda/'+googlecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        googlemonitor = _ssm.StringParameter(
            self, 'googlemonitor',
            description = 'Google Distillery Monitor',
            parameter_name = '/distillery/monitor/google',
            string_value = '/aws/lambda/'+googlecompute.function_name,
            tier = _ssm.ParameterTier.STANDARD,
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
            memory_size = 512
        )

        gcplogs = _logs.LogGroup(
            self, 'gcplogs',
            log_group_name = '/aws/lambda/'+gcpcompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        gcpmonitor = _ssm.StringParameter(
            self, 'gcpmonitor',
            description = 'GCP Distillery Monitor',
            parameter_name = '/distillery/monitor/gcp',
            string_value = '/aws/lambda/'+gcpcompute.function_name,
            tier = _ssm.ParameterTier.STANDARD,
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
            timeout = cdk.Duration.seconds(900),
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
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        azuremonitor = _ssm.StringParameter(
            self, 'azuremonitor',
            description = 'Azure Distillery Monitor',
            parameter_name = '/distillery/monitor/azure',
            string_value = '/aws/lambda/'+azurecompute.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

        azureevent = _events.Rule(
            self, 'azureevent',
            schedule=_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'
            )
        )
        azureevent.add_target(_targets.LambdaFunction(azurecompute))

### CLOUDFLARE CIDRS ###

        cloudflaretracker = _ssm.StringParameter(
            self, 'cloudflaretracker',
            description = 'Cloud Flare Distillery Tracker',
            parameter_name = '/distillery/tracker/cloudflare',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        cloudflarecompute = _lambda.DockerImageFunction(
            self, 'cloudflarecompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/cloudflare'),
            timeout = cdk.Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = cloudflaretracker.parameter_name
            ),
            memory_size = 512
        )

        cloudflarelogs = _logs.LogGroup(
            self, 'cloudflarelogs',
            log_group_name = '/aws/lambda/'+cloudflarecompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        cloudflaremonitor = _ssm.StringParameter(
            self, 'cloudflaremonitor',
            description = 'Cloud Flare Distillery Monitor',
            parameter_name = '/distillery/monitor/cloudflare',
            string_value = '/aws/lambda/'+cloudflarecompute.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

        cloudflareevent = _events.Rule(
            self, 'cloudflareevent',
            schedule=_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'
            )
        )
        cloudflareevent.add_target(_targets.LambdaFunction(cloudflarecompute))

### DIGITAL OCEAN CIDRS ###

        dotracker = _ssm.StringParameter(
            self, 'dotracker',
            description = 'Digital Ocean Distillery Tracker',
            parameter_name = '/distillery/tracker/do',
            string_value = 'EMPTY',
            tier = _ssm.ParameterTier.STANDARD,
        )

        docompute = _lambda.DockerImageFunction(
            self, 'docompute',
            code = _lambda.DockerImageCode.from_image_asset('cidr/do'),
            timeout = cdk.Duration.seconds(900),
            role = role,
            environment = dict(
                DYNAMODB_TABLE = table.table_name,
                SSM_PARAMETER = dotracker.parameter_name
            ),
            memory_size = 512
        )

        dologs = _logs.LogGroup(
            self, 'dologs',
            log_group_name = '/aws/lambda/'+docompute.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        domonitor = _ssm.StringParameter(
            self, 'domonitor',
            description = 'Digital Ocean Distillery Monitor',
            parameter_name = '/distillery/monitor/do',
            string_value = '/aws/lambda/'+docompute.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

        doevent = _events.Rule(
            self, 'doevent',
            schedule=_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'
            )
        )
        doevent.add_target(_targets.LambdaFunction(docompute))

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
            timeout = cdk.Duration.seconds(900),
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
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        oraclemonitor = _ssm.StringParameter(
            self, 'oraclemonitor',
            description = 'Oracle Distillery Monitor',
            parameter_name = '/distillery/monitor/oracle',
            string_value = '/aws/lambda/'+oraclecompute.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

        oracleevent = _events.Rule(
            self, 'oracleevent',
            schedule=_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'
            )
        )
        oracleevent.add_target(_targets.LambdaFunction(oraclecompute))
        
###
