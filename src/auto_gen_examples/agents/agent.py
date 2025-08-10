from autogen_agentchat.agents import BaseChatAgent

class tradeAgent(BaseChatAgent):
    def __init__(self, model_client, **kwargs):
        super().__init__(model_client, **kwargs)
        self.trading_data = None
        self.trade_history = []
        self.current_position = None
        self.balance = 10000  # Starting balance for trading


    async def on_message(self, message):
        # Process incoming messages and update trading data
        if message.content:
            self.trading_data = message.content
            await self.process_trading_data()

    async def process_trading_data(self):
        # Implement your trading logic here
        pass