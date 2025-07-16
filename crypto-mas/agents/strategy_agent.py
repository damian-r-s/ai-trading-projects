# agents/strategy_agent.py
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio

class StrategyAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Wait up to 10 seconds for a message
            if msg:
                print(f"StrategyAgent received: {msg.body}")
                # You can add your logic here
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
