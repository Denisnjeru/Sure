import sys
sys.path.append("...")

from backend.aws_session import aws_tendersure_session

tendersure_sqs = aws_tendersure_session.resource('sqs')