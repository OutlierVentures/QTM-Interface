# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Quantitative Token Model (QTM) radCAD Integration - a token economics simulation framework developed by Outlier Ventures. It transforms their static Excel-based QTM into a dynamic radCAD simulation with a Streamlit web interface for modeling token economies, agent behaviors, and ecosystem dynamics.

## Development Commands

### Setup and Running (uv - Recommended)
- Install dependencies and create virtual environment: `uv sync`
- Run the application: `uv run streamlit run Welcome.py`
- Run tests: `uv run pytest tests/`
- Code formatting: `uv run black .` (if needed for development)
- Linting: `uv run pylint` (available but no specific command defined)

### Setup and Running (pip - Alternative)
- Install dependencies: `pip install -r requirements.txt`
- Run the application: `streamlit run Welcome.py`
- Run tests: `pytest tests/`
- Code formatting: `black .` (if needed for development)
- Linting: `pylint` (available but no specific command defined)

### Python Environment
- Recommended Python version: 3.9+
- Primary approach: Uses uv for dependency management and virtual environment
- Alternative approach: Uses virtual environment: `python -m venv venv` then `venv/bin/activate`

## Architecture Overview

### Core Structure
The project follows a modular radCAD simulation architecture:

1. **Model/**: Core simulation engine
   - `simulation.py`: Main simulation orchestrator using radCAD framework
   - `state_variables.py`: Initializes system state (agents, liquidity pools, token economy)
   - `sys_params.py`: System parameter processing and agent allocation calculations
   - `state_update_blocks.py`: Defines simulation execution order and state transitions
   - `post_processing.py`: Results processing and data transformation

2. **Model/parts/**: Simulation modules organized by domain
   - `ecosystem/`: Token economics (vesting, airdrops, burns, liquidity pools)
   - `business/`: Business logic (user adoption, revenue, buybacks)
   - `agents_behavior/`: Agent decision-making and meta-bucket behaviors
   - `utilities/`: Token utility mechanisms (staking, mining, transfers)

3. **UserInterface/**: Streamlit UI components for data input and visualization
   - Input modules for different simulation aspects (fundraising, business, tokens)
   - `plots.py`: Data visualization and chart generation
   - `consistencyChecks.py`: Parameter validation logic

4. **pages/**: Streamlit multi-page application structure
   - Numbered pages for simulation workflow (Inputs → Fundraising → Business → etc.)

### Data Flow
1. Parameters loaded from CSV files in `data/` directory or user input
2. `get_initial_state()` initializes all system components (agents, pools, adoption curves)
3. radCAD executes simulation using `state_update_blocks` sequence
4. Results stored in SQLite (`simulationData.db`) for caching
5. Post-processing generates metrics and visualizations

### Key Simulation Components
- **Agent Types**: Early investors, team, protocol buckets, market participants
- **Token Utilities**: Staking (mint/burn, revenue share, vesting), liquidity mining, burning, holding
- **Market Simulation**: DEX liquidity pools with constant product formula
- **User Adoption**: S-curve growth models for product and token adoption
- **Business Model**: Revenue streams, expenditures, buyback mechanisms

### Authentication
Uses `streamlit-authenticator` with YAML config file for user management and data persistence.

### Database
SQLite database (`simulationData.db`) stores:
- System parameters with unique IDs
- Simulation results indexed by parameter combinations
- User scenario data

## Development Notes

- Simulation results are cached using `@st.cache_data` to avoid re-running identical parameter sets
- Parameter uniqueness prevents duplicate simulations via UUID-based identification
- All monetary values processed through utility functions in `Model/parts/utils.py`
- Brownian motion generator available for market volatility simulation
- Extensive parameter validation and consistency checking implemented