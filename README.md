# AI Trading Projects
Source code and experiments related to algorithmic crypto trading using Python, Freqtrade, and reinforcement learning agents.

## Set Up Development Environment
1. Install Python and Virtual Environment
    conda create -n agent_env python=3.10
    conda activate agent_env

    conda create -n trading_env python=3.10
    conda activate trading_env

2. Insall Core Libraries
    conda activate agent_env
    conda install -c conda-forge ccxt pandas numpy
    pip install spade

3. Add AI/ML Tools
    conda activate trading_env
    conda install -c conda-forge scikit-learn matplotlib
    pip install stable-baselines3