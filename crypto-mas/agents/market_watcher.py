# agents/market_watcher.py
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio  

class MarketWatcherAgent(Agent):
    class SendPriceBehaviour(CyclicBehaviour):
        async def run(self):
            msg = Message(to="strategy@xmpp.jp")
            msg.set_metadata("performative", "inform")
            msg.body = "BTC/USDT price: 30000" # Example price
            await self.send(msg)
            print("MarketWatcher: Sent price update.")
            await asyncio.sleep(5)  # Wait for 5 seconds before sending the next update

        async def setup(self):
            print("MarketWatcher started.")
            self.add_behaviour(self.SendPriceBehaviour())

if __name__ == "__main__":
    async def main():
        agent = MarketWatcherAgent("marketwatcher@xmpp.jp", "Aqq1234$$")
        await agent.start()
        print("Agent started. Press Ctrl+C to stop.")
        await asyncio.sleep(130)
        await agent.stop()
        print("Agent stopped.")

    asyncio.run(main())