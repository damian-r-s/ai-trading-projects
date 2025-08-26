from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import aiohttp
import json

class MarketWatcherAgent(Agent):
    class SendPriceBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                price = await self.get_binance_price()  # Fetch ticker

                msg = Message(to="strategy@xmpp.jp")
                msg.set_metadata("performative", "inform")
                msg.body = json.dumps({
                    "type": "price",
                    "symbol": "BTC/USDT",
                    "price": price
                })
                await self.send(msg)
                print(f"MarketWatcher: Sent price update: {price}")
            except Exception as e:
                print(f"MarketWatcher: Error fetching price: {e}")
            finally:
                await asyncio.sleep(5)
                
        async def get_binance_price(self):
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()            
                    return float(data['price'])

    async def setup(self):
        print("MarketWatcherAgent setup.")
        self.add_behaviour(self.SendPriceBehaviour())

if __name__ == "__main__":
    async def main():
        agent = MarketWatcherAgent("marketwatcher@xmpp.jp", "Aqq1234$$")
        await agent.start()
        print("Agent started. Press Ctrl+C to stop.")
        await asyncio.sleep(1330)
        await agent.stop()
        print("Agent stopped.")

    asyncio.run(main())
