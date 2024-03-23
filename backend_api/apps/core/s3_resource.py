import sys
sys.path.append("...")

from backend.aws_session import aws_tendersure_session

tendersure_s3 = aws_tendersure_session.resource('s3')