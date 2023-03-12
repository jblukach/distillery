#!/usr/bin/env python3
import os

import aws_cdk as cdk

from distillery.distillery_stack import DistilleryStack

app = cdk.App()

DistilleryStack(
    app, 'DistilleryStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('Alias','Tacklebox')
cdk.Tags.of(app).add('GitHub','https://github.com/4n6ir/distillery')

app.synth()
