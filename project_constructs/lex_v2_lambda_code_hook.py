from constructs import Construct
from aws_cdk import ( aws_iam as iam, aws_lambda as _lambda)

from config import (PYTHON_LAMBDA_CONFIG)

class LambdaCodeHook(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_function = _lambda.Function(
            self, "l", **PYTHON_LAMBDA_CONFIG, code=_lambda.Code.from_asset("./lambda/code_hook"),
            description='Code Hook para Lex Agenda')


