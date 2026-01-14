#!/usr/bin/env python3
import os

import aws_cdk as cdk

from distillery.distillery_stackuse1 import DistilleryStackUse1
from distillery.distillery_stackuse2 import DistilleryStackUse2
from distillery.distillery_stackusw2 import DistilleryStackUsw2
from sources.distillery_amazon import DistilleryAmazon

app = cdk.App()

DistilleryStackUse1(
    app, 'DistilleryStackUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryStackUse2(
    app, 'DistilleryStackUse2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryStackUsw2(
    app, 'DistilleryStackUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryAmazon(
    app, 'DistilleryAmazon',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

cdk.Tags.of(app).add('Alias','distillery')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/distillery')
cdk.Tags.of(app).add('Org','lukach.io')

app.synth()