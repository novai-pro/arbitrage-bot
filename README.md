# Hyperliquid Funding Rate Arbitrage Bot

A sophisticated trading bot that executes funding rate arbitrage strategies on Hyperliquid exchange. The bot capitalizes on funding rate differentials between spot and perpetual futures markets to generate potential profits.

## Key Features

- **Automated Trading**: Fully automated execution of funding rate arbitrage strategies
- **Market Coverage**: Currently optimized for TRUMP-USD trading pair
- **Real-time Monitoring**: Continuous monitoring of funding rates and market conditions
- **Risk Management**: 
  - Configurable profit thresholds
  - Automated position management
  - Built-in error handling and recovery
- **Comprehensive Logging**: Detailed logging system for monitoring and debugging

## How It Works

1. Monitors funding rates on Hyperliquid exchange in real-time
2. Identifies profitable arbitrage opportunities based on configurable thresholds
3. Executes simultaneous spot and perpetual futures trades
4. Manages positions automatically to capture funding rate differentials

## Prerequisites

- Python 3.10 or higher
- Hyperliquid exchange account
- Private key and wallet address
- Required Python packages:
  - `eth_account`
  - `hyperliquid-python-sdk`
  - `asyncio`
  - Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/novai-pro/arbitrage-bot.git
cd arbitrage-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export PRIVATE_KEY="your_private_key"
export WALLET_ADDRESS="your_wallet_address"
export BASE_URL="https://api.hyperliquid.xyz"
```

## Configuration

The bot can be configured through environment variables:
- `PRIVATE_KEY`: Your wallet private key
- `WALLET_ADDRESS`: Your wallet address
- `BASE_URL`: Hyperliquid API endpoint (testnet or mainnet)

Additional parameters can be adjusted in the code:
- `min_profit_threshold`: Minimum profit threshold for trade execution (default: 0.01%)
- `trade_size`: Size of each trade in USDC (default: 100 USDC)

## Usage

Run the bot:
```bash
python main.py
```

## Safety Considerations

- **Test First**: Always test with small amounts on testnet before running on mainnet
- **Private Keys**: Never share or commit your private keys
- **Risk Management**: Understand the risks involved in automated trading
- **Monitor Regularly**: Keep track of the bot's performance and positions

## Monitoring and Logging

The bot includes a comprehensive logging system that:
- Tracks all trade executions
- Records funding rate checks
- Logs errors and exceptions
- Provides debugging information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Disclaimer

Trading cryptocurrencies carries significant risk. This bot is provided as-is with no guarantees. Use at your own risk.

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.


