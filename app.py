#!/usr/bin/env python3
import os

import aws_cdk as cdk

from distillery.distillery_build import DistilleryBuild
from distillery.distillery_deploy import DistilleryDeploy
from distillery.distillery_stackuse1 import DistilleryStackUse1
from distillery.distillery_stackuse2 import DistilleryStackUse2
from distillery.distillery_stackusw2 import DistilleryStackUsw2
from sources.distillery_amazon import DistilleryAmazon
from sources.distillery_atlassian import DistilleryAtlassian
from sources.distillery_azure import DistilleryAzure
from sources.distillery_azurechina import DistilleryAzureChina
from sources.distillery_azuregermany import DistilleryAzureGermany
from sources.distillery_azuregovernment import DistilleryAzureGovernment
from sources.distillery_bingbot import DistilleryBingbot
from sources.distillery_cloudflare import DistilleryCloudflare
from sources.distillery_datadog import DistilleryDatadog
from sources.distillery_digitalocean import DistilleryDigitalOcean
from sources.distillery_fastly import DistilleryFastly
from sources.distillery_github import DistilleryGithub
from sources.distillery_google import DistilleryGoogle
from sources.distillery_googlebots import DistilleryGoogleBots
from sources.distillery_googlecloud import DistilleryGoogleCloud
from sources.distillery_googlecrawlers import DistilleryGoogleCrawlers
from sources.distillery_googlefetchers import DistilleryGoogleFetchers
from sources.distillery_icloudprivate import DistilleryIcloudprivate
from sources.distillery_jdcloud import DistilleryJdcloud
from sources.distillery_linode import DistilleryLinode
from sources.distillery_microsoft import DistilleryMicrosoft
from sources.distillery_netspi import DistilleryNetspi
from sources.distillery_newrelic import DistilleryNewrelic
from sources.distillery_o365china import DistilleryO365China
from sources.distillery_o365usdod import DistilleryO365USDod
from sources.distillery_o365usgov import DistilleryO365USGov
from sources.distillery_o365world import DistilleryO365World
from sources.distillery_okta import DistilleryOkta
from sources.distillery_openaibot import DistilleryOpenaibot
from sources.distillery_openaisearch import DistilleryOpenaisearch
from sources.distillery_openaiuser import DistilleryOpenaiuser
from sources.distillery_oracle import DistilleryOracle
from sources.distillery_perplexitybot import DistilleryPerplexitybot
from sources.distillery_perplexityuser import DistilleryPerplexityuser
from sources.distillery_salesforce import DistillerySalesforce
from sources.distillery_tailscale import DistilleryTailscale
from sources.distillery_tenable import DistilleryTenable
from sources.distillery_vultr import DistilleryVultr
from sources.distillery_zdxbeta import DistilleryZdxBeta
from sources.distillery_zdxcloud import DistilleryZdxCloud
from sources.distillery_zdxgov import DistilleryZdxGov
from sources.distillery_zdxten import DistilleryZdxTen
from sources.distillery_zpabeta import DistilleryZpaBeta
from sources.distillery_zpaprivate import DistilleryZpaPrivate
from sources.distillery_zpatwo import DistilleryZpaTwo
from sources.distillery_zscaler import DistilleryZscaler
from sources.distillery_zscalerbeta import DistilleryZscalerBeta
from sources.distillery_zscalergov import DistilleryZscalerGov
from sources.distillery_zscalerone import DistilleryZscalerOne
from sources.distillery_zscalerten import DistilleryZscalerTen
from sources.distillery_zscalerthree import DistilleryZscalerThree
from sources.distillery_zscalertwo import DistilleryZscalerTwo
from sources.distillery_zscloud import DistilleryZsCloud
from sources.distillery_zslogin import DistilleryZsLogin
from sources.distillery_zsloginbeta import DistilleryZsLoginBeta

app = cdk.App()

DistilleryBuild(
    app, 'DistilleryBuild',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryDeploy(
    app, 'DistilleryDeploy',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

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

DistilleryAtlassian(
    app, 'DistilleryAtlassian',
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

DistilleryBingbot(
    app, 'DistilleryBingbot',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryCloudflare(
    app, 'DistilleryCloudflare',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryDatadog(
    app, 'DistilleryDatadog',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryDigitalOcean(
    app, 'DistilleryDigitalOcean',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryFastly(
    app, 'DistilleryFastly',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryGithub(
    app, 'DistilleryGithub',
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

DistilleryIcloudprivate(
    app, 'DistilleryIcloudprivate',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryJdcloud(
    app, 'DistilleryJdcloud',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryLinode(
    app, 'DistilleryLinode',
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

DistilleryNetspi(
    app, 'DistilleryNetspi',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryNewrelic(
    app, 'DistilleryNewrelic',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryO365China(
    app, 'DistilleryO365China',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryO365USDod(
    app, 'DistilleryO365USDod',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryO365USGov(
    app, 'DistilleryO365USGov',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryO365World(
    app, 'DistilleryO365World',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryOkta(
    app, 'DistilleryOkta',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryOpenaibot(
    app, 'DistilleryOpenaibot',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryOpenaisearch(
    app, 'DistilleryOpenaisearch',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryOpenaiuser(
    app, 'DistilleryOpenaiuser',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryOracle(
    app, 'DistilleryOracle',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryPerplexitybot(
    app, 'DistilleryPerplexitybot',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryPerplexityuser(
    app, 'DistilleryPerplexityuser',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistillerySalesforce(
    app, 'DistillerySalesforce',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryTailscale(
    app, 'DistilleryTailscale',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryTenable(
    app, 'DistilleryTenable',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryVultr(
    app, 'DistilleryVultr',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZdxBeta(
    app, 'DistilleryZdxBeta',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZdxCloud(
    app, 'DistilleryZdxCloud',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZdxGov(
    app, 'DistilleryZdxGov',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZdxTen(
    app, 'DistilleryZdxTen',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZpaBeta(
    app, 'DistilleryZpaBeta',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZpaPrivate(
    app, 'DistilleryZpaPrivate',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZpaTwo(
    app, 'DistilleryZpaTwo',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZscaler(
    app, 'DistilleryZscaler',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZscalerBeta(
    app, 'DistilleryZscalerBeta',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZscalerGov(
    app, 'DistilleryZscalerGov',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZscalerOne(
    app, 'DistilleryZscalerOne',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZscalerTen(
    app, 'DistilleryZscalerTen',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZscalerThree(
    app, 'DistilleryZscalerThree',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZscalerTwo(
    app, 'DistilleryZscalerTwo',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZsCloud(
    app, 'DistilleryZsCloud',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZsLogin(
    app, 'DistilleryZsLogin',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DistilleryZsLoginBeta(
    app, 'DistilleryZsLoginBeta',
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