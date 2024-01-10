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

## To run the app
 
Debug: `flask run`

Small-scale production: `waitress-serve --listen=127.0.0.1:8080 app:app`

