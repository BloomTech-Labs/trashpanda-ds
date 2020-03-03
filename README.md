# The Trash Panda

You can find the project at [The Trash Panda](https://www.thetrashpanda.com).

## Contributors

|                                              [Timothy Hsu](https://github.com/TimTree)                                               |                                          [Tobias Reaper](https://github.com/tobiasfyi)                                          |                                              [Trevor Clack](https://github.com/tclack88)                                              |                                             [Vera Mendes](https://github.com/VeraMendes)                                             |
| :----------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------: |
|         [<img src="https://avatars2.githubusercontent.com/u/7098478?s=460&v=4" width = "200" />](https://github.com/TimTree)         |    [<img src="https://avatars0.githubusercontent.com/u/45893143?s=400&v=4" width = "200" />](https://github.com/tobias-fyi)     |        [<img src="https://avatars3.githubusercontent.com/u/39845330?s=460&v=4" width = "200" />](https://github.com/tclack88)         |       [<img src="https://avatars0.githubusercontent.com/u/54785435?s=460&v=4" width = "200" />](https://github.com/VeraMendes)       |
|                         [<img src="https://github.com/favicon.ico" width="15">](https://github.com/TimTree)                          |                      [<img src="https://github.com/favicon.ico" width="15">](https://github.com/tobias-fyi)                      |                         [<img src="https://github.com/favicon.ico" width="15">](https://github.com/tclack88)                          |                        [<img src="https://github.com/favicon.ico" width="15">](https://github.com/VeraMendes)                        |
| [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/timothy-hsu-72877a171/) | [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/tobias-ea-reaper/) | [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/trevor-clack-774696184/) | [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/vera-mendes-1b7a60191/) |


![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)

## Project Overview

[Trello Board](https://github.com/Lambda-School-Labs/trashpanda-ds/projects)

[Product Canvas](https://www.notion.so/d2e8748fdffe4c66a0a6641582dd6b63?v=4c919ea10f204aa89cd9184d59a9e6f4)

Trash Panda is an app that uses image recognition AI to help you recycling better. You may search through a list of categories, enter in a material to our search bar, or use your camera to scan the item and discover how to properly dispose of your material! A lot of things end up in garbage bags sent off to the landfill when they might have a better way of being disposed. With Trash Panda, you will become wiser at disposing items and be better to our planet!
You’ll receive proper disposal information specific to your location if you live in the USA. Currently, Trashpanda provides international users with an AI result and general information about how materials can be disposed of properly, but it will not provide disposal locations for international postal codes.

[Deployed Front End](https://thetrashpanda.com/intro)

### Tech Stack

- Python 3
- ForeCut: Automated image background removal
  - [OpenCV](https://github.com/opencv/opencv)
  - [Detectron2](https://github.com/facebookresearch/detectron2)
  - [detectron2-pipeline](https://github.com/tobias-fyi/detectron2-pipeline) forked from [jagin](https://github.com/tobias-fyi/detectron2-pipeline)
- [Mask_RCNN](https://github.com/matterport/Mask_RCNN/)
- [YOLO: Real-Time Object Detection using Darknet](https://github.com/AlexeyAB/darknet)
- [AWS SageMaker](https://aws.amazon.com/sagemaker/)
- [AWS S3](https://aws.amazon.com/s3/)
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)

### Predictions

Our Neural Network Model was trained in a 15GB dataset using darknet framework. It is trained to predict ~ 75 different classes (ex: batteries, CD cases, bicycles) using Computer Vision.


### How to connect to the web API

Check out here: [Trashpanda-be](https://github.com/Lambda-School-Labs/trashpanda-be)

### How to connect to the data API

Check out here: [Trashpanda-ds-api](https://github.com/Lambda-School-Labs/trashpanda-ds-api)

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**

- Check first to see if your issue has already been reported.
- Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
- Create a live example of the problem.
- Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Backend Documentation](https://github.com/Lambda-School-Labs/trashpanda-be) for details on the backend of our project.

See [Front End Documentation](https://github.com/Lambda-School-Labs/trashpanda-fe) for details on the front end of our project.
