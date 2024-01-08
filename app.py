#!/usr/bin/env python3
import os

import aws_cdk as cdk

from distillery.distillery_amazon import DistilleryAmazon
from distillery.distillery_azure import DistilleryAzure
from distillery.distillery_cloudflare import DistilleryCloudflare
from distillery.distillery_digitalocean import DistilleryDigitalOcean
from distillery.distillery_google import DistilleryGoogle
from distillery.distillery_googlecloud import DistilleryGoogleCloud
from distillery.distillery_netspi import DistilleryNetSpi
from distillery.distillery_o365 import DistilleryO365
from distillery.distillery_okta import DistilleryOkta
from distillery.distillery_oracle import DistilleryOracle
from distillery.distillery_stack import DistilleryStack
from distillery.distillery_tenable import DistilleryTenable
from distillery.distillery_vultr import DistilleryVultr

app = cdk.App()

DistilleryAmazon(
    app, 'DistilleryAmazon',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryAzure(
    app, 'DistilleryAzure',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryCloudflare(
    app, 'DistilleryCloudflare',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryDigitalOcean(
    app, 'DistilleryDigitalOcean',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryGoogle(
    app, 'DistilleryGoogle',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryGoogleCloud(
    app, 'DistilleryGoogleCloud',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryNetSpi(
    app, 'DistilleryNetSpi',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryO365(
    app, 'DistilleryO365',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryOkta(
    app, 'DistilleryOkta',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryOracle(
    app, 'DistilleryOracle',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryStack(
    app, 'DistilleryStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryTenable(
    app, 'DistilleryTenable',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryVultr(
    app, 'DistilleryVultr',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('Alias','Tacklebox')
cdk.Tags.of(app).add('GitHub','https://github.com/4n6ir/distillery')

app.synth()