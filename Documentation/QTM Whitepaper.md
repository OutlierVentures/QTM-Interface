! This Whitepaper is a work in progress !

# Quantitative Token Model

The [Quantitative Token Model (QTM)](https://outlierventures.io/quantitative-token-model-a-data-driven-approach-to-stay-ahead-of-the-game/) is an open source spreadsheet model developed by [Outlier Ventures](https://outlierventures.io/). Its purpose is to forecast key metrics of different token economies on a higher level by abstracting a set of often leveraged token utilities. It should be used for educational purposes only and not to derive any financial advice. The market making for the token is approximated by a DEX liquidity pool with [constant product relationship](https://balancer.fi/whitepaper.pdf).

## Motivation and Benefits
It has always been a huge challenge to create a feasible web3 project economy. The rate of uncertainty when developing an idea, constructing a meaningful business model and  introducing value-adding token model has always come at a high cost for a founding team. The amount of variables and interdependencies causes a huge headache for the token designers and engineers on a way to constructing a value generating business model where the numbers add-up.

The Outlier Ventures took the first step into solving the challenges of complicated and costly validations of token economy feasibility introducing the Qualitative Token Model. Even though the spreadsheet model was a huge pain reliever for those who wanted to test out their assumptions on token economy there was a need for a tool that could provide answers to questions of a more advanced setting. There is a need to introduce a more complex and sophisticated logic supported by the agent-based modelling to bring the simulation result as close as it could be to the natural non-deterministic environment.

This tool is focused on providing an approach to design,validate and modify the token economy outlook for the project founders and stakeholder involved in token economy development. Among the major benefits we are looking to ease up the following processes of token economy development:
* Experiment with token utilities modifications
* Sophisticated agent behavior introductions
* Searching for economic feasibility in multiple extreme scenarios
* Stress testing of the parameters change
* Smoothing out the way to optimize ecosystem parameters
* Monitoring change and analyzing results


## 1.QTM Structure Breakdown

The QTM consists of the following elements:
1. Model inputs
2. Token and Signal flow architecture
3. The analysis section

### 1.2 Model Inputs
This element is dedicated to describe a specific environment of the project's token model. Here one can test out their hypothesis on the environmental settings of the token economy, user parameters, token utilities and how those affect the financial stability of the crypto project. For convenience the Model inputs are split into the 3 blocks:
* Fundraising
* Inputs 
* Utility modules


#### 1.2.1 Fundraising
In this section building blocks describe:
1. Basic Token Parameters - identifies the basic token setting one wishes to implement in their crypto project, including future valuation and share of equity owned by external shareholders, or in other words share of project valuation to be excluded from the project token capitalization.(The complete table can be found at A.1.1)

2. Fundraising Module - defines the project’s fundraising goals at the different token sale stages and expenses in the form of bonuses given to the seed and pre-sale investors (The complete table can be found at A.1.2)

3. Initial token allocation and Vesting schedules  - includes an extensive list of allocation pools for you to match your distribution plans. (The complete table can be found at A.1.3)

#### 1.2.2 Inputs 
The Inputs section describes the price setting and expected amount of initial liquidity along with expected user project adoption. The given settings are then matched with the expected project's financial model.
The Inputs section comprises the following blocks:
* Liquidity Pool Module - describes the token price at launch, parameters of funds allocation to the liquidity pools and the paired token information.*
 *add information on how such numbers are derived*

* User Adoption -  includes parameters expected user base, product adoption, hypothesis on token adoption and use in a form of expected utility, holding, selling and utility removal allocation. (The complete table can be found at A.2.2)

* Business Assumptions - comprises expected project revenue streams  and expenses forming a quasi general project budget model. (The complete table can be found at A.2.3)


#### 1.2.3 Utility Modules
The Utility Modules sections if focused on activation/ or deactivation of certain utilities. In also includes an assumed weighting with respect to token allocation and specific parameters for each individual utility out of Holding, Burning, Locking, Transferring and Liquidity Mining.  The Utility Modules consist of the following blocks:

* Utility adoption distribution - 
* Utility Modules
*** some text goes here ***

## A.QTM User Inputs

#### A.1 Fundraising

##### A.1.1 Basic Token Parameters
#
| Variable                              | Possible Inputs                   | Examples    |
|---------------------------------------|-----------------------------------|-------------|
| Supply type                           | Fixed, Inflationary, Deflationary | Fixed       | 
| Initial Total Supply of Tokens        | *numerical*                       | 100,000,000 |
| Launch Date                           | *dd.mm.yy*                        | 1.1.24      |
| % Public Sale of Supply (up to)       | *x%*                              | 3.50%       |
| Public Sale Valuation in USD          | *numerical*                       | 40,000,000  |
| Equity Owned by External Shareholders | *x%*                              | 10.00%      |


##### A.1.2 Fundraising Module
#
| Variable                                | Possible Inputs | Examples   |
|-----------------------------------------|-----------------|------------|
| Early Backers / Angels Raised, USD      | *numerical*     | 250,000    | 
| Seed Raised, USD                        | *numerical*     | 750,000    |
| Pre-Sale 1 Raised, USD                  | *numerical*     | 1,500,000  |
| Pre-Sale 2 Raised, USD                  | *numerical*     | 0          |
| Public Sale Raised, USD                 | *numerical*     | 1,400,000  |
| Sum of Raised Capital, USD / USD Raised | *numerical*     | 3,900,000  |
| Early Backers / Angels Valuation        | *numerical*     | 9,000,000  |
| Seed Valuation, USD                     | *numerical*     | 15,000,000 |
| Pre-Sale 1 Valuation, USD               | *numerical*     | 25,000,000 | 
| Pre-Sale 2 Valuation, USD               | *numerical*     | 50,000,000 |
| Early Backers / Angels Bonus Amount     | *x%*            | 91.00%     |
| Seed Bonus Amount                       | *x%*            | 50.00%     |
| Pre-Sale 1 Bonus Amount                 | *x%*            | 25.00%     |
| Pre-Sale 2 Bonus Amount                 | *x%*            | 15.00%     |


##### A.1.3 Initial Token Allocation and Vesting Schedules
#
| Variable                                       | Possible Inputs | Examples |
|------------------------------------------------|-----------------|----------|
| Founders / Team Token Allocation               | *x%*            | 25.00%   | 
| Outlier Ventures Token Allocation              | *x%*            | 6.00%    |
| Advisors Token Allocation                      | *x%*            | 4.00%    |
| Strategic Partners Token Allocation            | *x%*            | 0.00%    |
| Reserve Token Allocation                       | *x%*            | 10.00%   |
| Community Token Allocation                     | *x%*            | 0.00%    |
| Foundation Token Allocation                    | *x%*            | 0.00%    | 
| Incentivisation Token Allocation               | *x%*            | 33.00%   |
| Placeholder Token Allocation                   | *x%*            | 0.00%    |
| Liquidity Pool Token Allocation                | *x%*            | 2.72%    |
| Airdrop Allocation                             | *x%*            | 2.00%    |
| Airdrop Date 1                                 | *dd.mm.yy*      | 1.1.24   |
| Airdrop Amount 1                               | *x%*            | 35.00%   |
| Airdrop Date 2                                 | *dd.mm.yy*      | 1.6.24   |
| Aidrop Amount 2                                | *x%*            | 35.00%   |
| Airdrop Date 3                                 | *dd.mm.yy*      | 1.4.25   |
| Aidrop Amount 3                                | *x%*            | 30.00%   |
| Early Backers / Angels Initial Vesting         | *numerical*     | 0        |
| Seed Initial Vesting                           | *numerical*     | 0        |
| Pre-Sale 1 Initial Vesting                     | *numerical*     | 0        |
| Pre-Sale 2 Initial Vesting                     | *numerical*     | 0        | 
| Public Sale Initial Vesting                    | *numerical*     | 25       |
| Founders / Team Initial Vesting                | *numerical*     | 0        |
| Outlier Ventures Initial Vesting               | *numerical*     | 0        |
| Advisors Initial Vesting                       | *numerical*     | 0        |
| Strategic Partners Initial Vesting             | *numerical*     | 100      | # is it in days or months?
| Reserve Initial Vesting                        | *numerical*     | 100      | 
| Community Initial Vesting                      | *numerical*     | 0        |
| Foundation Initial Vesting                     | *numerical*     | 0        |
| Incentivisation Initial Vesting                | *numerical*     | 0.5      |
| Placeholder Initial Vesting                    | *numerical*     | 0        |
| Liquidity Pool Initial Vesting                 | *numerical*     | 100      |
| Early Backers / Angels Cliff Months            | *numerical*     | 6        | 
| Seed Cliff Months                              | *numerical*     | 6        |
| Pre-Sale 1 Cliff Months                        | *numerical*     | 6        |
| Pre-Sale 2 Cliff Months                        | *numerical*     | 1        |
| Public Sale Cliff Months                       | *numerical*     | 0        |
| Founders / Team Cliff Months                   | *numerical*     | 6        |
| Outlier Ventures Cliff Months                  | *numerical*     | 6        |
| Advisors Cliff Months                          | *numerical*     | 3        |
| Strategic Partners Cliff Months                | *numerical*     | 0        |
| Reserve Cliff Months                           | *numerical*     | 0        |
| Community Cliff Months                         | *numerical*     | 0        |
| Foundation Cliff Months                        | *numerical*     | 0        |
| Incentivisation Cliff Months                   | *numerical*     | 0        |
| Placeholder Cliff Months                       | *numerical*     | 0        |
| Early Backers / Angels Vesting Duration Months | *numerical*     | 24       |
| Seed Vesting Duration Months                   | *numerical*     | 24       |
| Pre-Sale 1 Vesting Duration Months             | *numerical*     | 18       |
| Pre-Sale 2 Vesting Duration Months             | *numerical*     | 9        |
| Public Sale Vesting Duration Months            | *numerical*     | 6        |
| Founders / Team Vesting Duration Months        | *numerical*     | 36       |
| Outlier Ventures Vesting Duration Months       | *numerical*     | 24       |
| Advisors Vesting Duration Months               | *numerical*     | 24       |
| Strategic Partners Vesting Duration Months     | *numerical*     | 0        |
| Reserve Vesting Duration Months                | *numerical*     | 0        |
| Community Vesting Duration Months              | *numerical*     | 0        |
| Foundation Vesting Duration Months             | *numerical*     | 0        |
| Incentivisation Vesting Duration Months        | *numerical*     | 84       | 
| Placeholder Vesting Duration Months            | *numerical*     | 0        |


#### A.2 Inputs

##### A.2.1 Liquidity Pool Module
* *to clarify* 


##### A.2.2 User Adoption
#
| Variable                                       | Possible Inputs | Examples |
|------------------------------------------------|-----------------|----------|
| Initial Product Users/ Angels Raised, USD      | *numerical*     | 250      | 
| Product Users after 10 years                   | *numerical*     | 50000    |
| Product Adoption Velocity (curve shape)        | *numerical*     | 1        |
| One-Time Product Revenue per User / $          | *numerical*     | 25       |
| Regular Product Revenue per User per Month / $ | *numerical*     | 10       |
| Initial Token Holders                          | *numerical*     | 250      |
| Token Holders after 10 years                   | *numerical*     | 250      |
| Token Adoption Velocity (curve shape)          | *numerical*     | 1        |
| One-Time Token Buy per User / $                | *numerical*     | 100      | 
| Regular Token Buy per User per Month / $       | *numerical*     | 20       |
| Avg. Token Utility Allocation / %              | *x%*            | 65       |
| Avg. Token Holding / %                         | *x%*            | 10       |
| Avg. Token Selling / %                         | *x%*            | 25       |
| Avg. Token Utility Removal / %                 | *x%*            | 3        |

##### A.2.3 Business Assumptions
# 
| Variable                                                      | Possible Inputs                       | Examples  |
|---------------------------------------------------------------|---------------------------------------|-----------|
| Product Income per Month / $                                  | *numerical*                           | 332,695   | 
| Royalty Income per Month / $                                  | *numerical*                           | 2,500     |
| Other Income per Month / $                                    | *numerical*                           | 0         |
| Treasury Income per Month / $                                 | *numerical*                           | 500       |
| Regular Income Sum per Month / $ / $                          | *numerical*                           | 335,695   |
| One-Time Payments after Pre-Sales / $                         | *numerical*                           | 150,000   |
| Planned One-Time Investments after Launch / $                 | *numerical*                           | 350,000   |
| Salaries per Month / $                                        | *numerical*                           | 50,000    |
| License Costs per Month / $                                   | *numerical*                           | 350       | 
| Other Monthly Costs / $                                       | *numerical*                           | 500       |
| Buyback fixed/percentage of cash reserve                      | *Fixed*, *Percentage of cash reserve* | Fixed     |
| Token Buybacks per Month / % of cash reserves                 | *%*                                   | -4        |
| Token Buybacks per Month / $                                  | *numerical*                           | 80,000    |
| Buyback bucket                                                | *nominal ???*                         | Reserve   |
| Buyback start date                                            | *dd.mm.yy*                            | 1.7.24    | 
| Buyback end date                                              | *dd.mm.yy*                            | 1.7.28    |
| Burn token supply as percentage of init. total supply / month | *%*                                   | 0.01      |
| Burn project bucket tokens start date                         | *dd.mm.yy*                            | 1.7.24    |
| Burn project bucket tokens end date                           | *dd.mm.yy*                            | 1.7.28    |
| Burn from project bucket                                      | *nominal???*                          | Reserve   |
| Regular Expenditures Sum per Month / $                        | *numerical*                           | 176,320   | 
| Cash Reserve after Launch / $                                 | *numerical*                           | 2,263,261 |
| Monthly Income vs. Expenditures Balance / $                   | *numerical*                           | 159,375   |

##



