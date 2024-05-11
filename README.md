# Python AWS Rekognition

A web application written in Python that uses AWS Rekognition to detect objects.

## Example

To see an example of the result, you can check the `example` folder.

## Requirements

- Python 3
- An AWS account and user with permissions to use AWS Rekognition programatically
- AWS CLI

## How to use

```sh
# Install the required packages
> pip install -r requirements.txt

# Configure your AWS credentials
> aws configure

# (Alternative) Environment variables
AWS_ACCESS_KEY_ID=<access-key-id>
AWS_SECRET_ACCESS_KEY=<secret-access-key>

# Run the project
> reflex run
```

## How to use without the AWS CLI

If you don't have the AWS CLI installed, you can create the `credentials` file using `touch ~/.aws/credentials`.

Then you can add the lines below inside that file.

```
[default]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret-key>
```

## (Alternative) How to use environment variables

You can also simply create an `.env` file and enter the environment variables the way it is shown in [how to use](#how-to-use).
