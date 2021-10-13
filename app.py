#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

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

cdk.Tags.of(app).add('distillery','distillery')

app.synth()
