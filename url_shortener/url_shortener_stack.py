from aws_cdk import core
from aws_cdk.core import Construct, Duration
from aws_cdk import aws_dynamodb, aws_lambda, aws_apigateway, aws_sns, aws_s3, aws_s3_deployment, aws_sns_subscriptions

from cdk_watchful import Watchful


class UrlShortenerStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwarg) -> None:
        super().__init__(scope, id, **kwarg)

        # define the table that maps short codes to URLs.
        table = aws_dynamodb.Table(self, "Table",
                                   partition_key=aws_dynamodb.Attribute(
                                       name="id",
                                       type=aws_dynamodb.AttributeType.STRING),
                                   read_capacity=10,
                                   write_capacity=5)

        # define the API gateway request handler. all API requests will go to the same function.
        handler = aws_lambda.Function(self, "UrlShortenerFunction",
                                      code=aws_lambda.Code.asset("./lambda"),
                                      handler="handler.main",
                                      timeout=Duration.minutes(5),
                                      runtime=aws_lambda.Runtime.PYTHON_3_7)

        # generate the topic to publish to
        topic = aws_sns.Topic(self, "Topic", display_name="Url created topic")
        topic.add_subscription(aws_sns_subscriptions.EmailSubscription("nausherwan.korai@gmail.com"))

        # pass the table name to the handler through an environment variable and grant
        # the handler read/write permissions on the table.
        handler.add_environment('TABLE_NAME', table.table_name)
        handler.add_environment('TOPIC_ARN', topic.topic_arn)
        table.grant_read_write_data(handler)
        topic.grant_publish(handler)

        # define the API endpoint and associate the handler
        api = aws_apigateway.LambdaRestApi(self, "UrlShortenerApi", handler=handler)

        # define the static website hosting
        frontendBucket = aws_s3.Bucket(self, "UrlShortenerWebsiteBucket",
                                       public_read_access=True,
                                       removal_policy=core.RemovalPolicy.DESTROY,
                                       website_index_document="index.html")

        deployment = aws_s3_deployment.BucketDeployment(self, "deployStaticWebsite",
                                                        sources=[aws_s3_deployment.Source.asset("./frontend")],
                                                        destination_bucket=frontendBucket)

        # define a Watchful monitoring system and watch the entire scope
        # this will automatically find all watchable resources and add
        # them to our dashboard
        wf = Watchful(self, 'watchful', alarm_email='nausherwan.korai@gmail.com')
        wf.watch_scope(self)
