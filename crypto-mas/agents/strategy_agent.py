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

                    self.agent.price_history.append(price)
                    if len(self.agent.price_history) > 20:
                        self.agent.price_history.pop(0)

                    short_ma = self.agent.compute_moveing_average(self.agent.price_history, window_size=5)
                    long_ma = self.agent.compute_moveing_average(self.agent.price_history, window_size=10)

                    if short_ma and long_ma:
                        if short_ma > long_ma:
                            decision = "BUY"
                        elif short_ma < long_ma:
                            decision = "SELL"
                        else:
                            decision = "HOLD"                        
                        print(f"StrategyAgent: Decision based on MAs - {decision}")
                else:
                    print("StrategyAgent: Unknown message type.")
            else:
                print("StrategyAgent: No message received.")

    def compute_moveing_average(self, prices, window_size): 
        if len(prices) < window_size:
            return None
        return sum(prices[-window_size:]) / window_size

    async def setup(self):
        print("StrategyAgent starting up...")
        self.price_history = []
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
