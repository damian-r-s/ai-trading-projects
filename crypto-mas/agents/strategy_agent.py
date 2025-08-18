# agents/strategy_agent.py
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio
import json

class StrategyAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Wait up to 10 seconds for a message
            if msg:
                print(f"StrategyAgent received: {msg.body}")
                data = json.loads(msg.body)
                if data.get("type") == "price":
                    price = data.get("price")
                    symbol = data.get("symbol")
                    print(f"StrategyAgent: Received price for {symbol}: {price}")
                    # Here you can implement your trading strategy logic based on the price
                    
                else:
                    print("StrategyAgent: Unknown message type.")
            else:
                print("StrategyAgent: No message received.")

    async def setup(self):
        print("StrategyAgent starting up...")
        receive_behaviour = self.ReceiveBehaviour()
        self.add_behaviour(receive_behaviour)

if __name__ == "__main__":
    async def main():
        agent = StrategyAgent("strategy@xmpp.jp", "Aqq1234$$")
        await agent.start()
        print("StrategyAgent started.")
        await asyncio.sleep(160)  # Let it run long enough to receive messages
        await agent.stop()
        print("StrategyAgent stopped.")

    asyncio.run(main())
