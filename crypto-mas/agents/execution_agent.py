from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json

class ExecutionAgent(Agent):
    class ReceiveDecisionBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Wait up to 10 seconds for a message
            if msg:
                print(f"ExecutionAgent received: {msg.body}")
                data = json.loads(msg.body)

                if data.get("type") == "signal":
                    action = data.get("action")
                    price = data.get("price")
                    symbol = data.get("symbol")
                    print(f"ExecutionAgent: Received decision for {symbol}: {action} at price {price}")

                    self.agent.simulate_trade(action, symbol, price)                    
                else:
                    print("ExecutionAgent: Unknown message type.")
            else:
                print("ExecutionAgent: No message received.")
    
    def simulate_trade(self, action, symbol, price):
        if action == "BUY":
            print(f"[SIMULATED TRADE] Buying {symbol} at {price}")
            self.last_trade = {"action": "BUY", "symbol": symbol, "price": price}
        elif action == "SELL":
            print(f"[SIMULATED TRADE] Selling {symbol} at {price}")
            self.last_trade = {"action": "SELL", "symbol": symbol, "price": price}
        else:
            print(f"[SIMULATED TRADE] Holding position")

    async def setup(self):
        print("ExecutionAgent setup.")
        self.last_trade = None
        trade_behaviour = self.ReceiveDecisionBehaviour()
        self.add_behaviour(trade_behaviour)

if __name__ == "__main__":
    import asyncio
    async def main():
        agent = ExecutionAgent("execution@xmpp.jp", "Aqq1234$$")
        await agent.start()
        print("ExecutionAgent  started. Press Ctrl+C to stop.")
        await asyncio.sleep(1330)
        await agent.stop()
        print("ExecutionAgent  stopped.")

    asyncio.run(main())