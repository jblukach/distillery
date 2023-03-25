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

        Aspects.of(self).add(
            cdk_nag.AwsSolutionsChecks(
                log_ignores = True,
                verbose = True
            )
        )

        cdk_nag.NagSuppressions.add_stack_suppressions(
            self, suppressions = [
                {'id': 'AwsSolutions-IAM4','reason': 'GitHub Issue'},
                {'id': 'AwsSolutions-IAM5','reason': 'GitHub Issue'}
            ]
        )

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAMBDA LAYER ###

        layer = _lambda.LayerVersion.from_layer_version_arn(
            self, 'layer',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:3'
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
            runtime = _lambda.Runtime.PYTHON_3_9,
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
