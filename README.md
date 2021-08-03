# ColorSplashPhotoProcessor



## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```


## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
ColorSplashPhotoProcessor$ sam build --use-container
```

The SAM CLI installs dependencies defined in `src/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
ColorSplashPhotoProcessor$ sam local invoke ColorSplashPhotoProcessorFunction --event events/event.json
```


## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.


## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
ColorSplashPhotoProcessor$ pip install -r tests/requirements.txt --user
# unit test
ColorSplashPhotoProcessor$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
ColorSplashPhotoProcessor$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

## Instructions

1. Via the command line, use conda to activate the correct environment. 

>`$ conda activate colorSplash`

If Visual Studio code does not immediately select the interpreter for running, use the command palette (cmd + shift + p) and select `Python Select Interpreter` and choose `colorSplash: conda`.

I'm going to do the intial color determinartion via this tutorial: https://towardsdatascience.com/color-identification-in-images-machine-learning-application-b26e770c4c71


2. To make the opencv python module available to the lambda function, I followed this StackOverflow post to create a Lambda layer with required libraries. The layer can be found at `arn:aws:lambda:us-west-1:015914662809:layer:cv2-python38:4
`
