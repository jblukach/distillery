import datetime

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment,
    aws_ssm as _ssm
)

from constructs import Construct

class DistilleryStackUse2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        day = datetime.datetime.now().strftime('%d')

    ### PARAMETER ###

        organization = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'organization',
            parameter_name = '/organization/id'
        )

    ### LAMBDA LAYER ###

        packages = _s3.Bucket.from_bucket_name(
            self, 'packages',
            bucket_name = 'packages-use2-lukach-io'
        )

        requests = _lambda.LayerVersion(
            self, 'requests',
            layer_version_name = 'requests',
            description = str(year)+'-'+str(month)+'-'+str(day)+' deployment',
            code = _lambda.Code.from_bucket(
                bucket = packages,
                key = 'requests.zip'
            ),
            compatible_architectures = [
                _lambda.Architecture.ARM_64
            ],
            compatible_runtimes = [
                _lambda.Runtime.PYTHON_3_13
            ],
            removal_policy = RemovalPolicy.DESTROY
        )

        requestsparameter = _ssm.StringParameter(
            self, 'requestsparameter',
            parameter_name = '/layer/requests',
            string_value = requests.layer_version_arn,
            description = 'Requests Lambda Layer ARN',
            tier = _ssm.ParameterTier.STANDARD
        )

    ### S3 BUCKET ###

        staged = _s3.Bucket(
            self, 'staged',
            bucket_name = 'distillery-staged-use2-lukach-io',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        deployment = _deployment.BucketDeployment(
            self, 'deployment',
            sources = [_deployment.Source.asset('code')],
            destination_bucket = staged,
            prune = False
        )

        bucket_policy = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:ListBucket'
            ],
            resources = [
                staged.bucket_arn
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        staged.add_to_resource_policy(bucket_policy)

        object_policy = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:GetObject'
            ],
            resources = [
                staged.arn_for_objects('*')
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        staged.add_to_resource_policy(object_policy)

        research = _s3.Bucket(
            self, 'research',
            bucket_name = 'distillery-research-lukach-io',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = False,
            enforce_ssl = True,
            versioned = False
        )

        bucket_policy_two = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:ListBucket'
            ],
            resources = [
                research.bucket_arn
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        research.add_to_resource_policy(bucket_policy_two)

        object_policy_two = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:GetObject'
            ],
            resources = [
                research.arn_for_objects('*')
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        research.add_to_resource_policy(object_policy_two)

        temporary = _s3.Bucket(
            self, 'temporary',
            bucket_name = 'distillery-temporary-lukach-io',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        temporary.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )

    ### OIDC ###

        provider = _iam.OpenIdConnectProvider(
            self, 'provider',
            url = 'https://token.actions.githubusercontent.com',
            client_ids = [
                'sts.amazonaws.com'
            ]
        )

        github = _iam.Role(
            self, 'github',
            assumed_by = _iam.WebIdentityPrincipal(provider.open_id_connect_provider_arn).with_conditions(
                {
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub": "repo:jblukach/distillery:*"
                    }
                }
            )
        )

        github.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'ReadOnlyAccess'
            )
        )   

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'cloudformation:CreateChangeSet',
                    'cloudformation:DeleteChangeSet',
                    'cloudformation:DescribeChangeSet',
                    'cloudformation:DescribeStacks',
                    'cloudformation:ExecuteChangeSet',
                    'cloudformation:CreateStack',
                    'cloudformation:UpdateStack',
                    'cloudformation:RollbackStack',
                    'cloudformation:ContinueUpdateRollback',
                    'cloudformation:DescribeStackEvents',
                    'cloudformation:GetTemplate',
                    'cloudformation:DeleteStack',
                    'cloudformation:UpdateTerminationProtection',
                    'cloudformation:GetTemplateSummary'
                ],
                resources = [
                    '*'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    's3:GetObject*',
                    's3:GetBucket*',
                    's3:List*',
                    's3:Abort*',
                    's3:DeleteObject*',
                    's3:PutObject*'
                ],
                resources = [
                    '*'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'kms:Decrypt',
                    'kms:DescribeKey',
                    'kms:Encrypt',
                    'kms:ReEncrypt*',
                    'kms:GenerateDataKey*'
                ],
                resources = [
                    '*'
                ],
                conditions = {
                    "StringEquals": {
                        "kms:ViaService": "s3.us-east-1.amazonaws.com"
                    }
                }
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'kms:Decrypt',
                    'kms:DescribeKey',
                    'kms:Encrypt',
                    'kms:ReEncrypt*',
                    'kms:GenerateDataKey*'
                ],
                resources = [
                    '*'
                ],
                conditions = {
                    "StringEquals": {
                        "kms:ViaService": "s3.us-east-2.amazonaws.com"
                    }
                }
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'kms:Decrypt',
                    'kms:DescribeKey',
                    'kms:Encrypt',
                    'kms:ReEncrypt*',
                    'kms:GenerateDataKey*'
                ],
                resources = [
                    '*'
                ],
                conditions = {
                    "StringEquals": {
                        "kms:ViaService": "s3.us-west-2.amazonaws.com"
                    }
                }
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'iam:PassRole'
                ],
                resources = [
                    'arn:aws:iam::'+str(account)+':role/cdk-lukach-cfn-exec-role-'+str(account)+'-us-east-1',
                    'arn:aws:iam::'+str(account)+':role/cdk-lukach-cfn-exec-role-'+str(account)+'-us-east-2',
                    'arn:aws:iam::'+str(account)+':role/cdk-lukach-cfn-exec-role-'+str(account)+'-us-west-2'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'sts:GetCallerIdentity'
                ],
                resources = [
                    '*'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'ssm:GetParameter',
                    'ssm:GetParameters'
                ],
                resources = [
                    'arn:aws:ssm:us-east-1:'+str(account)+':parameter/cdk-bootstrap/lukach/version',
                    'arn:aws:ssm:us-east-2:'+str(account)+':parameter/cdk-bootstrap/lukach/version',
                    'arn:aws:ssm:us-west-2:'+str(account)+':parameter/cdk-bootstrap/lukach/version'
                ]
            )
        )
