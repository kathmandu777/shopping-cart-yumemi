#!/usr/bin/env python3
import os

import aws_cdk as cdk

from shopping_cart_yumemi.shopping_cart_yumemi_stack import ShoppingCartYumemiStack

app = cdk.App()
ShoppingCartYumemiStack(
    app,
    "ShoppingCartYumemiStack",
    # for local development
    # env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")),
    # for github actions development
    env=cdk.Environment(account=os.getenv("AWS_ACCOUNT_ID"), region=os.getenv("AWS_REGION")),
)

app.synth()
