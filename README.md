# ColorSplashPhotoProcessor

## Description

ColorSplashPhotoProcessor (CSPP) is a component of the overarching ColorSplash web application that can be found at https://thurau.io/colorsplash/. ColorSplash allows users to browse royalty free images that have colors within a certain Euclidean distance of a provided HEX code. CSPP runs in a python-3.8 AWS Lambda runtime and uses [opencv-python](https://github.com/opencv/opencv-python) and [sklearn](https://scikit-learn.org/) to detect colors from a photo and store the results in a useful structure. CSPP runs asynchonously within the larger application context via CloudWatchEvents.


You can see other components of this project in the following Github repos

- [ColorSplashPhotoRetrieval](https://github.com/DanielThurau/ColorSplashPhotoRetrieval)
- [ColorSplashColorDetector](https://github.com/DanielThurau/ColorSplashColorDetector)
- [thurau.io](https://github.com/DanielThurau/thurau.io)

## Motivation

A friend was facing issues when trying to create social media posts for an ecommerce company we recently launched. She had developed a branding guide and had chosen what colors she wanted to include in the website, logos, and eventual marketing material. But when it was time to make marketing posts, trying to apply that style guide was difficult. For all the tools on the internet she used, none were able to query royalty free images that were close to the HEX color codes she had selected. This project was born to remedy this issue. 

I wanted to provide a clean minimal interface on a website that would have a form for a HEX code, and query a REST API that would return royalty free images that had a subset of colors within close to the original HEX code.

## Features And Roadmap

### Features
1. Asynchronous Lambda triggered via CloudWatch Events
2. Uses opencv-python to read images and shape images and sklearn's KMeans to fit the image with the number of colors desired.
3. Updates RGB colors in a database with a set of images that have that color within them.
4. Infrastructure defined in template.yml
5. Machine-specific libraries deployed using Lambda Layers

### Roadmap
1. Write unit tests
2. Define the rest of the infrastructure used in the template.yml
3. Create a script to enable/disable the CloudWatch event from the CLI.
4. CI/CD so `$ sam deploy` is triggered from Github
5. Experiments on quality of feedback in UI

    5.1. Testing better image detection and color fitting

    5.2. Testing number of colors that can be detected

    5.3. Implement Upvote/downvote content


## Tech Used

Due to CSPP's asychronous nature, it was designed to be run in a functional runtime from the start. Due to my history with AWS, I decided to use AWS as the cloud provider and write the project as a serverless application that is deployed using the AWS Serverless Application Model (AWS SAM) CLI tool. You can find out more about AWS SAM on its [homepage](https://aws.amazon.com/serverless/sam/).

CSPP's role is to process the images in the S3 bucket that ColorSplashPhotoRetrieval uploaded. CSPP will list a set of the images from S3 and try to output the N most populous RGB colors. This is a tough thing to implemenet due to two issues

1. How do you group a number of RGB pixels to a single RGB color that is a 'decent' representation of the group
2. Ordering which RGB colors are most populous in the image, and how issue 1 can drastically affect which color we choose

A longer writeup on this can be found here (//TODO include the blogpost here). To solve this problem, I decided to use sklearn and opencv-python which are two extensive libraries in python that, among other things, allow image manipulation and out of the box ML functionality.

## Installation

### Required Tools
1. [git](https://git-scm.com/) - a free and open source distributed version control system
2. [python 3.8](https://www.python.org/downloads/release/python-380/) - an interpreted high-level general-purpose programming language. Includes pip a python dependency management tool
3. [Docker](https://www.docker.com/get-started) - an open source containerization platform. Required to run AWS SAM
4. [AWS CLI](https://aws.amazon.com/cli/) - a unified tool to manage your AWS services
5. [AWS SAM CLI](https://aws.amazon.com/serverless/sam/) - an open-source framework for building serverless applications

### Cloning The Project

You can either fork the repo or clone it directly with

```shell
$ git clone https://github.com/DanielThurau/ColorSplashPhotoProcessor.git
$ cd ColorSplashPhotoProcessor
```

### Configuring AWS

AWS SAM CLI will piggy back off of the AWS CLI configurations. It is worth while to configure this ahead of time. If considering contribution, open an issue on the project and credentials **may** be provided. If you want to clone and deploy to your own AWS accounts, configure your AWS CLI to have credentials via the `~/.aws/credentials` file. It will look like this

```shell
$ aws configure
AWS Access Key ID [None]: <your access key>
AWS Secret Access Key [None]: <your secret key>
Default region name [None]: <deployed region>
Default output format [None]: json
```

### Environmental Variables

There are several environmental variables needed to run this application. An example structure is found in `env.example` (// TODO Link this). Once you fill out the variables for local development, copy it to the src/ folder. The Lambda will also need to be configured with these values in the "Configuration-> Environmental Variables" via the AWS Console.

```shell
$ cp env.example src/.env
```

### AWS Infrastructure

This project uses AWS Lambda, AWS DynamoDB, AWS S3, and AWS CloudWatch. Since it's an AWS SAM application, the infrastructure is defined via the template.yml file which SAM will compile and create a CloudFormation stack. Most of the infrastructure for this component is written in this template.yml, but not all. See the **Roadmap** section to track upcoming improvements. If forking and deploying to a personal AWS account, some of the infrastructure will be missing and need to be manually created.

## Usage

This project uses AWS SAM CLI to build, test, and deploy, but running the code and unit tests via the python executable is also possible. However, it is advisable to use SAM CLI since the tool will mimic the lambda runtime.

### AWS SAM CLI

Start docker either as a background process, in another terminal tab, or via desktop application.

```shell
$ sam build
$ sam local invoke
$ sam deploy
```

### Python

```shell
$ pip install -r tests/requirements.txt --user
$ python -m pytest tests/unit -v
$ AWS_SAM_STACK_NAME=ColorSplashPhotoProcessor python -m pytest tests/integration -v
```

It is worthwhile to have some form of virtualenv while developing on this pacakge for both the IDE and development. I recommend [conda](https://docs.conda.io/en/latest/).

## Contribute

If you'd like to contribute, fork the project and submit a Pull Request. If you'd like access to the infrastructure to test, open an issue and request access. Access requests will be reviewed and granted on a case by case basis.

## Credits

So many tutorials and blog posts deserve to have credits here, but alas I did not think to record all of them. I will be trying to fill this in as I write the ColorSplash blog post. Here are a few that are specific to this component.

* [Color Identification in Images](https://towardsdatascience.com/color-identification-in-images-machine-learning-application-b26e770c4c71) - [Karan Bhanot](https://medium.com/@bhanotkaran22)

    * This tutorial provided some of the code examples and explaination on how to accomplish the color detection and grouping
* [Marcin's](https://stackoverflow.com/users/248823/marcin) answer on [StackOverflow](https://stackoverflow.com/a/64019186/6655640)

    * To get some of these libraries to work in the lambda runtime required a special feature of AWS Lambdas called Lambda Layers. To have gotten this component working in the asynchronous context wouldn't have been possible without his contribution.

## License

See LICENSE.md

> MIT License
>
> Copyright (c) 2021 Daniel Thurau