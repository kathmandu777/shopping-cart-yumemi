from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_dynamodb as dynamodb  # Duration,; aws_sqs as sqs,
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class ShoppingCartYumemiStack(Stack):
    PROJECT_NAME = "shopping-cart-yumemi"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:  # type: ignore
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        table = dynamodb.Table(
            self,
            "shopping_cart_table",
            table_name="shopping_carts",
            partition_key=dynamodb.Attribute(name="cart_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="variant_id", type=dynamodb.AttributeType.STRING),
        )
        table.add_global_secondary_index(
            index_name="user_id-idx",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.KEYS_ONLY,
        )

        create_cart_func = _lambda.Function(
            self,
            "create-cart",
            code=_lambda.Code.from_asset("lambda"),
            handler="create_cart.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "BASE_URL": self.node.try_get_context("base_url"),
                "STAGE_NAME": self.node.try_get_context("stage_name"),
            },
        )
        put_content_func = _lambda.Function(
            self,
            "put-content",
            code=_lambda.Code.from_asset("lambda"),
            handler="put_content.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
        )
        delete_cart_func = _lambda.Function(
            self,
            "delete-cart",
            code=_lambda.Code.from_asset("lambda"),
            handler="delete_cart.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
        )
        get_cart_func = _lambda.Function(
            self,
            "get-cart",
            code=_lambda.Code.from_asset("lambda"),
            handler="get_cart.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
        )
        authenticate_func = _lambda.Function(
            self,
            "authenticate",
            code=_lambda.Code.from_asset("lambda"),
            handler="authenticate.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
        )

        table.grant_full_access(create_cart_func)
        table.grant_full_access(put_content_func)
        table.grant_full_access(delete_cart_func)
        table.grant_full_access(get_cart_func)

        api = apigateway.RestApi(self, "shopping-cart-api")
        carts_resources = api.root.add_resource("carts")
        carts_resources.add_method("POST", apigateway.LambdaIntegration(create_cart_func))

        cart_resources = carts_resources.add_resource("{cart_id}")
        cart_resources.add_method("GET", apigateway.LambdaIntegration(get_cart_func))
        cart_resources.add_method("DELETE", apigateway.LambdaIntegration(delete_cart_func))

        content_resources = cart_resources.add_resource("contents")
        content_resources.add_method("PUT", apigateway.LambdaIntegration(put_content_func))

        authenticate_resources = api.root.add_resource("auth")
        authenticate_resources.add_method("POST", apigateway.LambdaIntegration(authenticate_func))
