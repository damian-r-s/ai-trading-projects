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

                    short_ma = self.agent.compute_moving_average(self.agent.price_history, window_size=5)
                    long_ma = self.agent.compute_moving_average(self.agent.price_history, window_size=10)

                    if short_ma and long_ma:
                        fee_rate = 0.002  # 0.1% per trade
                        decision = "HOLD"

                        if short_ma > long_ma and not self.agent.in_position:
                            decision = "BUY"
                            self.agent.last_buy_price = price
                            self.agent.in_position = True

                        elif short_ma < long_ma and self.agent.in_position:
                            break_even_price = self.agent.last_buy_price * (1 + 2 * fee_rate)
                            if price > break_even_price:
                                decision = "SELL"
                                self.agent.in_position = False
                            else:
                                decision = "HOLD"

                        print(f"StrategyAgent: Decision based on MAs - {decision}")
                else:
                    print("StrategyAgent: Unknown message type.")
            else:
                print("StrategyAgent: No message received.")

    def compute_moving_average(self, prices, window_size):
        if len(prices) < window_size:
            return None
        return sum(prices[-window_size:]) / window_size

    async def setup(self):
        print("StrategyAgent starting up...")
        self.price_history = []
        self.last_buy_price = None
        self.in_position = False
        receive_behaviour = self.ReceiveBehaviour()
        self.add_behaviour(receive_behaviour)

if __name__ == "__main__":
    async def main():
        agent = StrategyAgent("strategy@xmpp.jp", "Aqq1234$$")
        await agent.start()
        print("StrategyAgent started.")
        await asyncio.sleep(330)  # Let it run long enough to receive messages
        await agent.stop()
        print("StrategyAgent stopped.")

    asyncio.run(main())