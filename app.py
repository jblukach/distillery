#!/usr/bin/env python3
import os

import aws_cdk as cdk

from distillery.distillery_stackuse1 import DistilleryStackUse1
from distillery.distillery_stackuse2 import DistilleryStackUse2
from distillery.distillery_stackusw2 import DistilleryStackUsw2
from sources.distillery_amazon import DistilleryAmazon
from sources.distillery_azure import DistilleryAzure
from sources.distillery_azurechina import DistilleryAzureChina
from sources.distillery_azuregermany import DistilleryAzureGermany
from sources.distillery_azuregovernment import DistilleryAzureGovernment
from sources.distillery_google import DistilleryGoogle
from sources.distillery_googlebots import DistilleryGoogleBots
from sources.distillery_googlecloud import DistilleryGoogleCloud
from sources.distillery_googlecrawlers import DistilleryGoogleCrawlers
from sources.distillery_googlefetchers import DistilleryGoogleFetchers
from sources.distillery_microsoft import DistilleryMicrosoft

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

DistilleryAzure(
    app, 'DistilleryAzure',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryAzureChina(
    app, 'DistilleryAzureChina',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryAzureGermany(
    app, 'DistilleryAzureGermany',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryAzureGovernment(
    app, 'DistilleryAzureGovernment',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryGoogle(
    app, 'DistilleryGoogle',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryGoogleBots(
    app, 'DistilleryGoogleBots',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryGoogleCloud(
    app, 'DistilleryGoogleCloud',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryGoogleCrawlers(
    app, 'DistilleryGoogleCrawlers',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryGoogleFetchers(
    app, 'DistilleryGoogleFetchers',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryMicrosoft(
    app, 'DistilleryMicrosoft',
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