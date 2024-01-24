# Quantitative Token Model radCAD Integration

! This repository is a work in progress !

## Background

The [Quantitative Token Model (QTM)](https://outlierventures.io/quantitative-token-model-a-data-driven-approach-to-stay-ahead-of-the-game/) is an [open source spreadsheet model](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing) developed by [Outlier Ventures](https://outlierventures.io/). It's purpose is to forecast key metrics of different token economies on a higher level by abstracting a set of often leveraged token utilities. It should be used for educational purposes only and not to derive any financial advise. The market making for the token is approximated by a DEX liquidity pool with [constant product relationship](https://balancer.fi/whitepaper.pdf). To understand the usage of the tool please refer to the [User Story Map](https://whimsical.com/qtm-roadmap-FfdpxTyjN44zk1eMhpyEWJ)

## QTM Structure

![Quantitative Token Model](https://github.com/OutlierVentures/QTM-Interface/blob/main/images/Quantitative_Token_Model_Abstraction.jpeg?raw=true)

## Motivation for the radCAD Extension

The goal of the QTM radCAD integration is to extend and to improve the static high-level approach of the QTM spreadsheet model to a more flexible and dynamic one. With the radCad integration one should be able to perform parameter sweeps and optimizations. Furthermore it opens up the capabilities for more dynamic agent behaviors, Monte Carlo runs, and Markov decision trees, which reflect a more realistic approximation of a highly non-linear web3 token ecosystem. At a later stage there should also be a more accessible (web-based) UI.

## Development Roadmap

### V.1 (Static Base Model)

- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Initialize the project, create the development roadmap & README.md
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Implement interface to the QTM spreadsheet parameters
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Update the postprocessing in the `post_processing.py` with respect to the new QTM parameters and conventions
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Update the plot functionallities in the `plots.py` with respect to the new parameter conventions
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the vesting policies
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the incentivisation module
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the airdrop module
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the static agent behavior
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the utility policies
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the liquidity pool interactions
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the user adoption policies
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test protocol bucket allocations
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the rest of token ecosystem KPIs / metrics
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Update the postprocessing w.r.t. the new implemented policies and corresponding state variables
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Web based UI for result output plots
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Improve function & overall code documentation
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Improve the robustness of all functions
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Improve the robustness of all model input parameter
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Staging tests of the whole model
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Case studies & publishing first results in an article
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Write the documentation for the QTM and radCAD integration

### V.2 (Sophisticated Model)

- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build a web-based UI to create another input option
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Implement user authentication and data set shareability between users
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build custom user plot capabilities
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Account for different revenue receiver buckets and track them
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Add external rewards for stakers in diverse assets to mimic bribe markets (can be dependent on revenue received by a certain revenue bucket)
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Add input inconsistency icons to respective input section expander text
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Update fundraising module to more complex scenarios, including SAFTs, SAFT+Ts and SAFTs
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Implement different KPI-driven controller designs based on incentive priorities/optimizations
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Develop risk analysis procedures
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Add more dynamic agent (behavior) policies
  - ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Intelligent agents I: Hard coded logics
    - ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Agents tend to stake tokens if reward APR is above target APR and remove tokens if it is below the target APR
    - ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Add DAO voting caused staking demand based on revenue and business funds
    - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Add market buy behavior based on intrinsic protocol value, which is proportional to business funds and revenue projection
    - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Add market buy behavior based on market sentiment (Brownian Motion) and protocol reputation
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Intelligent agents II: AI driven decision making
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Parameter Optimization
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Implement and test parameter sweep capabilities
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Add advanced optimization procedures
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) LLM support agents

## Installation

Python 3.9 is recommended!

- Clone this repository to your local machine by `git clone https://github.com/OutlierVentures/QTM-Interface.git`
- Create a new Python environment in the projects directory by `python -m venv venv`
- Activate the new environment by `venv/bin/activate`
- Install all required packages by `pip install -r requirements.txt`

## Usage
- Make sure you followed the previous installation section.
- Navigate with your terminal to the main project directory.
- Run `streamlit run .\Welcome.py` within the previously installed and activated environment.
- Expand the Sign-Up expander on the Welcome landing page and create a new user account or use the test user credentials
- Expand and login via the Login expander on the Welcome landing page by using your preferred account credentials.

Test user login data:\
Username: `user`\
Password: `1234`

## New Module Implementation Procedure
Create a function that combines all of these into a single file

    1. Add parameters to ingest external data
    2. Function to initialize values in state variables
    3. The policy and state update functions
    4. Update state update block file
    5. Post-processing and plots to display it

## Resources and Articles
### Tool
- [GitHub Repository](https://github.com/OutlierVentures/QTM-Interface)
- [Whitepaper](https://github.com/OutlierVentures/QTM-Interface/blob/main/Documentation/QTM%20Whitepaper.md)
- [Spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing)
- [User Story Map](https://whimsical.com/qtm-roadmap-FfdpxTyjN44zk1eMhpyEWJ)

### Related Articles
- [Quantitative Token Model: A data-driven approach to stay ahead of the game](https://outlierventures.io/article/quantitative-token-model-a-data-driven-approach-to-stay-ahead-of-the-game/)
- [From Zero to Hero with Token Vesting + QTM case study](https://outlierventures.io/article/from-zero-to-hero-with-token-vesting/)