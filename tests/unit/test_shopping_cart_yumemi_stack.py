import aws_cdk as core
import aws_cdk.assertions as assertions

from shopping_cart_yumemi.shopping_cart_yumemi_stack import ShoppingCartYumemiStack


# example tests. To run these tests, uncomment this file along with the example
# resource in shopping_cart_yumemi/shopping_cart_yumemi_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ShoppingCartYumemiStack(app, "shopping-cart-yumemi")
    assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
