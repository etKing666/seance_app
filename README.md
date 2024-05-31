# SEANCE Threat Modelling Tool

## Description

SEANCE Threat Modelling Tool is a web-based threat modelling tool which provides users with a risk score and a data flow diagram of their organisation as well as recommendations to enhance their cyber security posture.

SEANCE Threat Modelling tool is based on SEANCE Threat Modelling Framework and Django Web Framework. 

### Features

The app provides the following features:

- Generate cyber security recommendations to the user based on the user's answers to the questions
- Calculate a risk score on a scale of 0-5, higher scores indicating higher risks
- Generate a data flow diagram of the user's organisation
- Ability to download the resulting report as a .pdf file

## Table of Contents

- [Dependencies](#dependencies)
  - [Python Packages](#python-packages)
  - [Non-Python Dependencies](#non-python-dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Overall risk rating and evaluation](#overall-risk-rating-and-evaluation)
  - [Recommendations](#recommendations)
  - [Data Flow Diagram](#data-flow-diagram)
- [Contact Information](#contact-information)
- [Tests](#tests)
- [License](#license)

## Dependencies

The application relies on a number Python packages and have a few dependencies to provide the intended functionalities.

### Python Packages

The application uses the following Python packages that are not included in the Python Standard Library:

- xhtml2pdf
- diagrams

All the dependencies (except for non-Python dependencies) of the application are included in the requirements.txt file. 

### Non-Python Dependencies

In order to ensure the correct functioning of the tool, a system-wide installation of Graphviz (an open source graph visualisation software) is required. 

## Installation

In order to install and run the application, follow the steps blow:

1. Unzip the application files in your preferred directory.
2. Install Graphviz to the system. 

You can download it from: https://graphviz.org/download/ The installation has been tested on Mac system, but as pointed out by some users (for example: https://stackoverflow.com/questions/35064304/runtimeerror-make-sure-the-graphviz-executables-are-on-your-systems-path-aft) for Windows some additional configurations might be required, even though it has not been explicitly stated so by Graphviz.

3. Install all requirements from requirements.txt by running:


    pip install -r requirements.txt

Before installing the dependencies by running the command above, it is recommended to create a virtual environment. 

4. Navigate to the project's root directory and run the following command to start the Django development server:


    python manage.py runserver

## Usage

After starting the Django development server, in your browser, go to:

    http://localhost:8000

The homepage of the web application will open. 

### Pages

Apart from the homepage, the web application has three pages:
1. Start Threat Modelling, where the users start threat modelling by answering questions.
2. About SEANCE, where the users get to know more about the SEANCE Framework.
3. Contact, where the users can contact the SEANCE team.

### Overall risk rating and evaluation

When users answer all questions, the application calculates a risk score based on the user's answers. Higher risk scores indicate higher risk.

| **Overall rating** | **Evaluation** |
|:------------------:|:--------------:|
|    4.00 - 5.00     |    Very High   |
|    3.00 - 3.99     |      High      |
|    2.00 - 2.99     |    Moderate    |
|    1.00 - 1.99     |       Low      |
|      0 - 0.99      |    Very Low    |


### Recommendations

The application provides the user with recommendations based on threat indicators derived from the user's responses. The recommendations are based on industry-standard sources but are presented in an easy-to-understand, non-technical manner.

### Data Flow Diagram

A Data Flow Diagram (DFD) is generated from user input to provide MB owners with a holistic view of their system, including their assets, employees and customers, and how they interact with each other. The application uses diagrams package to draw the DFD.

![sampleDFD.png](seance%2Fstatic%2FsampleDFD.png)

## Contact Information

You can contact the developer (Etkin Getir) at etkingetir@gmail.com for questions, queries, ideas and contributions. All queries will be responded within 72 hours.

## Tests

A total of 45 tests were written to verify the correct functioning of the application. Of these, 42 were unit tests and 3 were functional (API) tests, all of which were successfully passed.

The tests were grouped into different categories and separate test files were created for models, views, helpers, DFD and API. For models and views, the test coverage was 100% and all key functions and classes were tested. 

The tests can be found in the 'tests' folder and can be run by running the following command:

    python manage.py test

## License

MIT License (MIT)

Copyright (c) 2024 Etkin Getir

Permission is hereby granted, free of charge, to any person obtaining a copy  of this software and associated documentation files (the "Software"), to deal  in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
