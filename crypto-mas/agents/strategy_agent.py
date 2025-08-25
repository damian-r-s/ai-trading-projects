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
                    if len(self.agent.price_history) > 100:
                        self.agent.price_history.pop(0)

                    short_ma = self.agent.compute_moving_average(self.agent.price_history, window_size=self.agent.short_ma_window)
                    long_ma = self.agent.compute_moving_average(self.agent.price_history, window_size=self.agent.long_ma_window)
                    rsi = self.agent.compute_rsi(self.agent.price_history, self.agent.rsi_windows)

                    if rsi and short_ma and long_ma:
                        print(f"RSI: {rsi:.2f}, Short MA: {short_ma:.2f}, Long MA: {long_ma:.2f}")

                        if rsi < 30 and short_ma > long_ma and not self.agent.in_position:
                            decision = "BUY"
                            self.agent.in_position = True
                            self.agent.last_buy_price = price

                        elif rsi > 70 and short_ma < long_ma and self.agent.in_position:
                            break_even_price = self.agent.last_buy_price * (1 + self.agent.fee_percentage * 2)

                            if price > break_even_price:
                                decision = "SELL"
                                self.agent.in_position = False
                                self.agent.last_buy_price = None
                            else:
                                decision = "HOLD"
                        else:
                            decision = "HOLD"

                        print(f"StrategyAgent: Decision based on RSI + MA: {decision}")
                else:
                    print("StrategyAgent: Unknown message type.")
            else:
                print("StrategyAgent: No message received.")

    def compute_moving_average(self, prices, window_size):
        if len(prices) < window_size:
            return None
        return sum(prices[-window_size:]) / window_size
    
    def compute_rsi(self, prices, window=14):
        if len(prices) < window + 1:
            return None
        gains = []
        losses = []

        for i in range(1, window + 1):
            change = prices[-i] - prices[-i - 1]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))

        avg_gain = sum(gains) / window
        avg_loss = sum(losses) / window

        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    async def setup(self):
        print("StrategyAgent starting up...")
        self.price_history = []
        self.fee_percentage = 0.001
        self.last_buy_price = None
        self.in_position = False
        self.short_ma_window = 10
        self.long_ma_window = 30
        self.rsi_windows = 14
        receive_behaviour = self.ReceiveBehaviour()
        self.add_behaviour(receive_behaviour)

if __name__ == "__main__":
    async def main():
        agent = StrategyAgent("strategy@xmpp.jp", "Aqq1234$$")
        await agent.start()
        print("StrategyAgent started.")
        await asyncio.sleep(1330)  # Let it run long enough to receive messages
        await agent.stop()
        print("StrategyAgent stopped.")

    asyncio.run(main())