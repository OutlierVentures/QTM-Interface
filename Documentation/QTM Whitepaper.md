! This Whitepaper is a work in progress !

# Quantitative Token Model

The [Quantitative Token Model (QTM)](https://outlierventures.io/quantitative-token-model-a-data-driven-approach-to-stay-ahead-of-the-game/) is an open source spreadsheet model developed by [Outlier Ventures](https://outlierventures.io/). Its
purpose is to forecast key metrics of different token economies on a higher level by abstracting a set of often
leveraged token utilities. It should be used for educational purposes only and not to derive any financial advice.
The market making for the token is approximated by a DEX liquidity pool with [constant product relationship](https://balancer.fi/whitepaper.pdf).

## Motivation and Benefits

It has always been a huge challenge to create a feasible web3 project economy. The rate of uncertainty when developing
an idea, constructing a meaningful business model and introducing value-adding token model has always come at a high
cost for a founding team. The amount of variables and interdependencies causes a huge headache for the token designers
and engineers on a way to constructing a value generating business model.

Outlier Ventures took the first step into solving the challenges of complicated and costly validations of token
economy feasibility introducing the Qualitative Token Model. Even though the spreadsheet model was a huge pain reliever
for those who wanted to test out their assumptions on token economy there was a need for a tool that could provide
answers to questions of a more advanced setting. There is a need to introduce a more complex and sophisticated logic
supported by the agent-based modelling to bring the simulation result as close as it could be to the natural
non-deterministic environment.

This tool is focused on providing an approach to design, validate, and modify the token economy outlook for the project
founders and stakeholders involved in the token economy development. Among the major benefits we are looking to ease up the
following processes of token economy design and engineering:

- Fundraising and token allocation and vesting modelling
- Business revenue and runway forecasts
- Experimenting with token utilities modifications
- Diverse agent behavior models (static, stochastic, dynamic, LLM based)
- Searching for economic feasibility in multiple extreme scenarios
- Stress testing of the parameter space and risk assessments
- Ecosystem optimization according to target KPIs
- Monitoring in-market behaviors

## 1.QTM Structure Breakdown

The QTM consists of the following elements:

1. Model inputs
2. Token and signal flow architecture
3. The analysis section

### 1.2 Model Inputs

This element is dedicated to describe a specific environment of the project's token model. Here one can test out their
hypothesis on the environmental settings of the fundraising and business assumptions, token economy, user parameters, token utilities and how those affect the
financial feasibility of the Web3 initiative. For convenience the model inputs are split into the 3 blocks:

- Fundraising
- Inputs
- Utility modules

#### 1.2.1 Fundraising

In this section building blocks describe:

1. Basic Token Parameters - identifies the basic token setting one wishes to implement in their Web3 project,
   including launch valuation and share of equity owned by external shareholders, or in other words share of project
   valuation to be excluded from the project token capitalization.(The complete table can be found at A.1.1)

2. Fundraising Module - defines the project’s fundraising goals at the different token sale stages and expenses in the
   form of bonuses given to the seed and pre-sale investors (The complete table can be found at A.1.2)

3. Initial token allocation and vesting schedules - includes an extensive list of allocation pools to match distribution plans.(The complete table can be found at A.1.3)

#### 1.2.2 Inputs

The Inputs section describes the DEX liquidity pool setting and expected amount of initial liquidity along with expected user project
adoption. The given settings are then matched with the expected project's business assumptions.
The Inputs section comprises the following blocks:

- Liquidity Pool Module - describes the token price at launch, parameters of funds allocation to the liquidity pool and
  the paired token information. For the sake of simplicity the paired token is always assumed to be a stablecoin valued at $1.

- User Adoption - includes parameters expected user base, product adoption, hypothesis on token adoption and use in a
  form of expected utility, holding, selling and utility removal allocation. These metrics determin the overall sentiment
  in the ecosystem. (The complete table can be found at A.2.2)

- Business Assumptions - comprises expected project revenue streams and expenses forming a quasi general project budget
  model. (The complete table can be found at A.2.3)

#### 1.2.3 Utility Modules

The Utility Modules section is focused on activation or deactivation of certain token utilities. It describes the
weight of token utility utilization with respect to the assumed user behavior. The model allows Holding, Burning,
Locking, Transferring and Liquidity Mining.

- Staking - mechanism of locking the project tokens to receive rewards in the same token. Note that the QTM entails
  3 different staking reward mechanisms: (1) Fixed staking APR rewards, based on a prescribed reward APR of tokens for
  stakers. (2) Staking rewards based on revenue share boughtback tokens (3) Staking rewards based on a fixed prescribed
  vesting schedule, defined in the fundraising section.
- Liquidity Mining - tokens added to the liquidity pool, together with owners additional funds for the counterpart token
  (token2) against which the project token is valued. The rewards will be paid from the payout source according to the
  payout APR and the amount (share) of tokens provided in the liquidity pool.
- Burning - tokens burned (removed) from the circulation supply. No rewards paid out with this utility.
- Holding - tokens held in the wallet. Rewards paid out according to the token payout APR and the
  amount (share) of tokens held in the wallet
- Transfer for Benefit - tokens transferred and no rewards paid out to the wallet. This utility is often used to
  simulate diverse shops where one can use the token to purchase assets/items.

(The complete input table can be found at A.2.3)

## A.QTM User Inputs

#### A.1 FUNDRAISING

#

##### A.1.1 Basic Token Parameters

| Variable                              | Possible Inputs                   | Examples    |
| ------------------------------------- | --------------------------------- | ----------- |
| Supply type                           | Fixed, Inflationary, Deflationary | Fixed       |
| Initial Total Supply of Tokens        | _numerical_                       | 100,000,000 |
| Launch Date                           | _dd.mm.yy_                        | 1.1.24      |
| % Public Sale of Supply (up to)       | _x%_                              | 3.50%       |
| Public Sale Valuation in USD          | _numerical_                       | 40,000,000  |
| Equity Owned by External Shareholders | _x%_                              | 10.00%      |

#

##### A.1.2 Fundraising Module

| Variable                                | Possible Inputs | Examples   |
| --------------------------------------- | --------------- | ---------- |
| Early Backers / Angels Raised, USD      | _numerical_     | 250,000    |
| Seed Raised, USD                        | _numerical_     | 750,000    |
| Pre-Sale 1 Raised, USD                  | _numerical_     | 1,500,000  |
| Pre-Sale 2 Raised, USD                  | _numerical_     | 0          |
| Public Sale Raised, USD                 | _numerical_     | 1,400,000  |
| Sum of Raised Capital, USD / USD Raised | _numerical_     | 3,900,000  |
| Early Backers / Angels Valuation        | _numerical_     | 9,000,000  |
| Seed Valuation, USD                     | _numerical_     | 15,000,000 |
| Pre-Sale 1 Valuation, USD               | _numerical_     | 25,000,000 |
| Pre-Sale 2 Valuation, USD               | _numerical_     | 50,000,000 |
| Early Backers / Angels Bonus Amount     | _x%_            | 91.00%     |
| Seed Bonus Amount                       | _x%_            | 50.00%     |
| Pre-Sale 1 Bonus Amount                 | _x%_            | 25.00%     |
| Pre-Sale 2 Bonus Amount                 | _x%_            | 15.00%     |

#

##### A.1.3 Initial Token Allocation and Vesting Schedules

| Variable                                       | Possible Inputs | Examples |
| ---------------------------------------------- | --------------- | -------- |
| Founders / Team Token Allocation               | _x%_            | 25.00%   |
| Outlier Ventures Token Allocation              | _x%_            | 6.00%    |
| Advisors Token Allocation                      | _x%_            | 4.00%    |
| Strategic Partners Token Allocation            | _x%_            | 0.00%    |
| Reserve Token Allocation                       | _x%_            | 10.00%   |
| Community Token Allocation                     | _x%_            | 0.00%    |
| Foundation Token Allocation                    | _x%_            | 0.00%    |
| Incentivisation Token Allocation               | _x%_            | 33.00%   |
| Staking Vesting Token Allocation               | _x%_            | 0.00%    |
| Liquidity Pool Token Allocation                | _x%_            | 2.72%    |
| Airdrop Allocation                             | _x%_            | 2.00%    |
| Airdrop Date 1                                 | _dd.mm.yy_      | 1.1.24   |
| Airdrop Amount 1                               | _x%_            | 35.00%   |
| Airdrop Date 2                                 | _dd.mm.yy_      | 1.6.24   |
| Aidrop Amount 2                                | _x%_            | 35.00%   |
| Airdrop Date 3                                 | _dd.mm.yy_      | 1.4.25   |
| Aidrop Amount 3                                | _x%_            | 30.00%   |
| Early Backers / Angels Initial Vesting         | _numerical_     | 0        |
| Seed Initial Vesting                           | _numerical_     | 0        |
| Pre-Sale 1 Initial Vesting                     | _numerical_     | 0        |
| Pre-Sale 2 Initial Vesting                     | _numerical_     | 0        |
| Public Sale Initial Vesting                    | _numerical_     | 25       |
| Founders / Team Initial Vesting                | _numerical_     | 0        |
| Outlier Ventures Initial Vesting               | _numerical_     | 0        |
| Advisors Initial Vesting                       | _numerical_     | 0        |
| Strategic Partners Initial Vesting             | _numerical_     | 100      |
| Reserve Initial Vesting                        | _numerical_     | 100      |
| Community Initial Vesting                      | _numerical_     | 0        |
| Foundation Initial Vesting                     | _numerical_     | 0        |
| Incentivisation Initial Vesting                | _numerical_     | 0.5      |
| Staking Vesting Initial Vesting                | _numerical_     | 0        |
| Liquidity Pool Initial Vesting                 | _numerical_     | 100      |
| Early Backers / Angels Cliff Months            | _numerical_     | 6        |
| Seed Cliff Months                              | _numerical_     | 6        |
| Pre-Sale 1 Cliff Months                        | _numerical_     | 6        |
| Pre-Sale 2 Cliff Months                        | _numerical_     | 1        |
| Public Sale Cliff Months                       | _numerical_     | 0        |
| Founders / Team Cliff Months                   | _numerical_     | 6        |
| Outlier Ventures Cliff Months                  | _numerical_     | 6        |
| Advisors Cliff Months                          | _numerical_     | 3        |
| Strategic Partners Cliff Months                | _numerical_     | 0        |
| Reserve Cliff Months                           | _numerical_     | 0        |
| Community Cliff Months                         | _numerical_     | 0        |
| Foundation Cliff Months                        | _numerical_     | 0        |
| Incentivisation Cliff Months                   | _numerical_     | 0        |
| Staking Vesting Cliff Months                   | _numerical_     | 0        |
| Early Backers / Angels Vesting Duration Months | _numerical_     | 24       |
| Seed Vesting Duration Months                   | _numerical_     | 24       |
| Pre-Sale 1 Vesting Duration Months             | _numerical_     | 18       |
| Pre-Sale 2 Vesting Duration Months             | _numerical_     | 9        |
| Public Sale Vesting Duration Months            | _numerical_     | 6        |
| Founders / Team Vesting Duration Months        | _numerical_     | 36       |
| Outlier Ventures Vesting Duration Months       | _numerical_     | 24       |
| Advisors Vesting Duration Months               | _numerical_     | 24       |
| Strategic Partners Vesting Duration Months     | _numerical_     | 0        |
| Reserve Vesting Duration Months                | _numerical_     | 0        |
| Community Vesting Duration Months              | _numerical_     | 0        |
| Foundation Vesting Duration Months             | _numerical_     | 0        |
| Incentivisation Vesting Duration Months        | _numerical_     | 84       |
| Staking Vesting Duration Months                | _numerical_     | 0        |

#

#### A.2 INPUTS

##### A.2.1 Liquidity Pool Module

The liquidity pool parameters are calculated based on the previously provided information.
In this case we focus on initial token price, initial liquidity pool token allocation, and initial required amount of
stablecoins (in our case USDC):

- Initial Token Price - defined by taking Public Sale Valuation and dividing it by Initial Total Supply of Tokens
  mentioned in A.1.1 Basic Token Parameters.
- Initial Liquidity Pool Token Allocation - the required amount corresponds to the initial unlock of tokens from
  the Liquidity Pool Token Allocation _*(needs* *to* *be* *revised)*_
- Initial Amount of Stablecoins - is calculated by taking the product of Initial Token Price and Initial Liquidity Pool
  Token Allocation.

#

##### A.2.2 User Adoption

| Variable                                       | Possible Inputs | Examples |
| ---------------------------------------------- | --------------- | -------- |
| Initial Product Users/ Angels Raised, USD      | _numerical_     | 250      |
| Product Users after 10 years                   | _numerical_     | 50000    |
| Product Adoption Velocity (curve shape)        | _numerical_     | 1        |
| One-Time Product Revenue per User / $          | _numerical_     | 25       |
| Regular Product Revenue per User per Month / $ | _numerical_     | 10       |
| Initial Token Holders                          | _numerical_     | 250      |
| Token Holders after 10 years                   | _numerical_     | 250      |
| Token Adoption Velocity (curve shape)          | _numerical_     | 1        |
| One-Time Token Buy per User / $                | _numerical_     | 100      |
| Regular Token Buy per User per Month / $       | _numerical_     | 20       |
| Avg. Token Utility Allocation / %              | _x%_            | 65       |
| Avg. Token Holding / %                         | _x%_            | 10       |
| Avg. Token Selling / %                         | _x%_            | 25       |
| Avg. Token Utility Removal / %                 | _x%_            | 3        |

#

##### A.2.3 Business Assumptions

| Variable                                                      | Possible Inputs                       | Examples  |
| ------------------------------------------------------------- | ------------------------------------- | --------- |
| Product Income per Month / $                                  | _numerical_                           | 332,695   |
| Royalty Income per Month / $                                  | _numerical_                           | 2,500     |
| Other Income per Month / $                                    | _numerical_                           | 0         |
| Treasury Income per Month / $                                 | _numerical_                           | 500       |
| Regular Income Sum per Month / $ / $                          | _numerical_                           | 335,695   |
| One-Time Payments after Pre-Sales / $                         | _numerical_                           | 150,000   |
| Planned One-Time Investments after Launch / $                 | _numerical_                           | 350,000   |
| Salaries per Month / $                                        | _numerical_                           | 50,000    |
| License Costs per Month / $                                   | _numerical_                           | 350       |
| Other Monthly Costs / $                                       | _numerical_                           | 500       |
| Buyback fixed/percentage of cash reserve                      | _Fixed_, _Percentage of cash reserve_ | Fixed     |
| Token Buybacks per Month / % of cash reserves                 | _%_                                   | -4        |
| Token Buybacks per Month / $                                  | _numerical_                           | 80,000    |
| Buyback bucket                                                | _nominal ???_                         | Reserve   |
| Buyback start date                                            | _dd.mm.yy_                            | 1.7.24    |
| Buyback end date                                              | _dd.mm.yy_                            | 1.7.28    |
| Burn token supply as percentage of init. total supply / month | _%_                                   | 0.01      |
| Burn project bucket tokens start date                         | _dd.mm.yy_                            | 1.7.24    |
| Burn project bucket tokens end date                           | _dd.mm.yy_                            | 1.7.28    |
| Burn from project bucket                                      | _nominal???_                          | Reserve   |
| Regular Expenditures Sum per Month / $                        | _numerical_                           | 176,320   |
| Cash Reserve after Launch / $                                 | _numerical_                           | 2,263,261 |
| Monthly Income vs. Expenditures Balance / $                   | _numerical_                           | 159,375   |

#

##### A.3.1 Utility Modules

| Variable                                        | Possible Inputs | Examples |
| ----------------------------------------------- | --------------- | -------- |
| Staking Base APR Utility Share / %              | _numerical_     | 10       |
| PStaking Buyback & Distribute Utility Share / % | _numerical_     | 61       |
| Liquidity Mining Utility Share / %              | _numerical_     | 10       |
| Burning Utility Share / %                       | _numerical_     | 2        |
| Holding Utility Share / %                       | _numerical_     | 2        |
| Transfer for Benefit Utility Share / %          | _numerical_     | 15       |
| Locking APR/%                                   | _numerical_     | 4        |
| Locking Payout Source                           | _nominal_       | Reserve  |
| Locking Revenue Buyback Share /%                | _numerical_     | 50       |
| Liquidity Mining APR/%                          | _numerical_     | 10       |
| Liquidity Mining Payout Source                  | _nominal_       | Reserve  |
| Token Holding APR / %                           | _numerical_     | 2        |
| Token Holding Reward Payout Source              | _nominal_       | Reserve  |
| Token Transfer Destination                      | _nominal_       | Reserve  |
| Incentivise Through Minting / %                 | _numerical_     | 0        |
| Incentivisation Payout Source                   | _nominal_       | Reserve  |

#
