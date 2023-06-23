# Quantitative Token Model radCAD Integration

! This repository is work in progress !

## Background

The [Quantitative Token Model (QTM)](https://outlierventures.io/quantitative-token-model-a-data-driven-approach-to-stay-ahead-of-the-game/) is an open source spreadsheet model developed by [Outlier Ventures](https://outlierventures.io/). It's purpose is to forecast key metrics of different token economies on a higher level by abstracting a set of often leveraged token utilities. The market making for the token is approximated by a DEX liquidity pool with [constant product relationship](https://balancer.fi/whitepaper.pdf).

## QTM Structure

![Quantitative Token Model](https://github.com/achimstruve/QTM-Interface/blob/tree/restructuring_branch/images/Quantitative_Token_Model_Abstraction.jpeg?raw=true)

## Motivation for the radCAD Extension

The goal of the QTM radCAD integration is to extend and to improve the static high-level approach of the QTM spreadsheet model, developed by Outlier Ventures.

## Development Roadmap

- Update the postprocessing in the `processing.py` with respect to the new streamlined adoption of the QTM parameters and conventions
- Build the utility policies
- Build the trading policies (interactions with the liquidity pool)
- Build the user adoption policies
- Build the business policies
- Update the postprocessing w.r.t. the new implemented policies and corresponding state variables
- Test and improve the robustness of all functions -> unit tests
- Staging tests of the whole model
- Test parameter sweep capabilities
- Case studies & publishing first results in an article
- Add more dynamic agent (behavior) policies
- Add advanced optimization procedures

## Installation

Run the setup file on a new python env (3.9) to setup all dependencies

## Usage

Run `python simulation.py`
