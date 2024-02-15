# MKTH - A Resource for Health Claims
_Description:_ A web-based tool to collect and relate health claims about foods, nutrients, substances, interventions, and therapies with published research.

The tool as several goals:
1. Allow a user to quickly identify the source and veracity of various claims about health-related topics, as well as uncover and compare relationships from other sources.
1. Provide an streamlined way to enter sources, health claims, references, and research.
1. Make it as efficient as possible to review and cross-check entered information.
1. Give links to access the sources and research cited.

## How to clone and build

Make sure you have installed prerequisites:
- Python 3.x
- Git 2.x

Creating and activating a venv is recommended before proceeding:
`python -m venv venv`
`source venv/bin/activate`

Clone from GitHub: `git clone https://github.com/melja/mkth0`
Install required packages: `pip install -r requirements.txt`
Initialize database: `flask --app manage init-db`
Import test data: `flask --app manage load-test-data`

## To run the app
 
Development: `flask --app manage run --debug`

The application will be running on http://127.0.0.1:5000/


