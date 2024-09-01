provider "aws" {
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"
  endpoints {
    lambda       = "http://localhost:4566"
    cloudwatch   = "http://localhost:4566"
    iam          = "http://localhost:4566"
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow",
      Sid = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "my_lambda" {
  function_name    = "my_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler"
  runtime          = "python3.8"
  filename         = "lambda.zip"
  source_code_hash = filebase64sha256("lambda_function/lambda.zip")

  environment {
    variables = {
      LOG_LEVEL = "DEBUG"
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/my_lambda"
  retention_in_days = 1
}

output "lambda_function_name" {
  value = aws_lambda_function.my_lambda.function_name
}
