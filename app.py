#!/usr/bin/env python3
import os

import aws_cdk as cdk

from distillery.distillery_amazon import DistilleryAmazon
from distillery.distillery_azure import DistilleryAzure
from distillery.distillery_azurechina import DistilleryAzureChina
from distillery.distillery_azuregermany import DistilleryAzureGermany
from distillery.distillery_azuregovernment import DistilleryAzureGovernment
from distillery.distillery_censys import DistilleryCensys
from distillery.distillery_cloudflare import DistilleryCloudflare
from distillery.distillery_digitalocean import DistilleryDigitalOcean
from distillery.distillery_fastly import DistilleryFastly
from distillery.distillery_github import DistilleryGithub
from distillery.distillery_google import DistilleryGoogle
from distillery.distillery_googlebots import DistilleryGoogleBots
from distillery.distillery_googlecloud import DistilleryGoogleCloud
from distillery.distillery_googlecrawlers import DistilleryGoogleCrawlers
from distillery.distillery_googlefetchers import DistilleryGoogleFetchers
from distillery.distillery_jdcloud import DistilleryJDCloud
from distillery.distillery_linode import DistilleryLinode
from distillery.distillery_microsoft import DistilleryMicrosoft
from distillery.distillery_netspi import DistilleryNetSpi
from distillery.distillery_newrelic import DistilleryNewrelic
from distillery.distillery_o365 import DistilleryO365
from distillery.distillery_okta import DistilleryOkta
from distillery.distillery_oracle import DistilleryOracle
from distillery.distillery_stack import DistilleryStack
from distillery.distillery_tailscale import DistilleryTailscale
from distillery.distillery_tenable import DistilleryTenable
from distillery.distillery_vultr import DistilleryVultr
from distillery.distillery_zscalar import DistilleryZscalar

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

DistilleryAzureChina(
    app, 'DistilleryAzureChina',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryAzureGermany(
    app, 'DistilleryAzureGermany',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryAzureGovernment(
    app, 'DistilleryAzureGovernment',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryCensys(
    app, 'DistilleryCensys',
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

DistilleryFastly(
    app, 'DistilleryFastly',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryGithub(
    app, 'DistilleryGithub',
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

DistilleryGoogleBots(
    app, 'DistilleryGoogleBots',
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

DistilleryGoogleCrawlers(
    app, 'DistilleryGoogleCrawlers',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryGoogleFetchers(
    app, 'DistilleryGoogleFetchers',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryJDCloud(
    app, 'DistilleryJDCloud',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryLinode(
    app, 'DistilleryLinode',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DistilleryMicrosoft(
    app, 'DistilleryMicrosoft',
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

DistilleryNewrelic(
    app, 'DistilleryNewrelic',
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

DistilleryTailscale(
    app, 'DistilleryTailscale',
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

DistilleryZscalar(
    app, 'DistilleryZscalar',
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