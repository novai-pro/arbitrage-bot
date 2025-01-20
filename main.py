import asyncio
import logging
import os
import random
import uuid
from typing import Dict, Optional

import eth_account
from hyperliquid.exchange import Exchange
from hyperliquid.utils.signing import TriggerOrderType
from hyperliquid.utils.types import Cloid

SYMBOL = [
    "TRUMP"
]

logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger(__name__)

class FundingArbitrage:
    def __init__(self, private_key: str, wallet_address, base_url: str = "https://api.hyperliquid-testnet.xyz"):
        """
        Initialize the funding arbitrage class
        :param private_key: Wallet private key
        :param base_url: API base URL
        """
        account = eth_account.Account.from_key(private_key)
        self.exchange = Exchange(wallet=account, base_url=base_url, account_address=wallet_address)
        self.min_profit_threshold = 0.0001  # Minimum profit threshold 0.01%

    async def get_funding_rates(self) -> Dict[str, Dict]:
        """
        Get funding rates for all trading pairs
        return {'TRUMP': {'fundingRate': '0.00023018', 'nextFundingTime': 1737367200000}}
        """
        funding_rates = {}
        coin = SYMBOL[0]
        
        try:
            # Make sure the response is properly awaited
            funding_rate_response = self.exchange.post("/info", {"type": "predictedFundings"})
            
            for coin in funding_rate_response:
                # ['BSV', [['BinPerp', {'fundingRate': '0.00005', 'nextFundingTime': 1737374400000}], ['HlPerp', {'fundingRate': '0.0000125', 'nextFundingTime': 1737367200000}], ['BybitPerp', {'fundingRate': '0.00005', 'nextFundingTime': 1737374400000}]]]
                # get funding rate from HlPerp
                symbol = coin[0]
                value = coin[1]
                if symbol == "TRUMP":
                    for funding_rate_exchange_info in value:
                        if funding_rate_exchange_info[0] == "HlPerp":
                            funding_rates[symbol] = funding_rate_exchange_info[1]
                            break

        except Exception as e:
            logger.warning(f"Error getting funding rates: {e}", exc_info=True)
        
        return funding_rates


    async def run_arbitrage(self):
        """
        Run the main funding arbitrage logic
        """
        while True:
            try:
                # Get funding rates for all trading pairs
                funding_rates = await self.get_funding_rates()
                print(funding_rates)
                
                # Sort by funding rate to find highest and lowest
                # {'TRUMP': {'fundingRate': '0.00023018', 'nextFundingTime': 1737367200000}}
                        
                # Set trade size for each direction
                trade_size = 100  # USDC, adjust as needed

                # Place spot buy order
                print(f"Placing spot buy order for {SYMBOL[0]}")
                market = {"trigger": {"triggerPx": 0.0, "isMarket": True, "tpsl": "tp"}}
                spot_order_result = self.exchange.order(
                    name=SYMBOL[0],
                    is_buy=True,
                    limit_px=0.0,
                    sz=trade_size,
                    order_type=market,
                    reduce_only=False,
                    cloid=self.generate_cloid()
                )
                logger.info(f"Spot order result: {spot_order_result}")

                # Place perp short order
                print(f"Placing perp short order for {SYMBOL[0]}")
                perp_order_result = self.exchange.order(
                    name=SYMBOL[0],
                    is_buy=False,
                    sz=trade_size,
                    limit_px=0.0,
                    order_type=market,
                    reduce_only=False,
                    cloid=self.generate_cloid()
                )

                logger.info(f"Perp order result: {perp_order_result}")

                # Wait before next check
                print("Waiting for next iteration...")
                
                # Wait before next check
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.warning(f"Error running arbitrage: {e}", exc_info=True)
                await asyncio.sleep(60)

    def generate_cloid(self) -> Cloid:
        # random number as client order id
        value = random.randint(1000, 1000000000)
        return Cloid.from_int(value)


async def main():
    # Initialize arbitrage bot
    private_key = os.getenv("PRIVATE_KEY")
    wallet_address = os.getenv("WALLET_ADDRESS")
    if private_key is None:
        raise Exception("Private key not set")
    arb_bot = FundingArbitrage(private_key=private_key, wallet_address=wallet_address)
    
    # Run arbitrage logic
    await arb_bot.run_arbitrage()

if __name__ == "__main__":
    asyncio.run(main())