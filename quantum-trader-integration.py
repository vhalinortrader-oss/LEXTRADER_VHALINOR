# Integração com o quantum trader
from quantum_algorithms_trader import QuantumAlgorithmsTrader
from continuous_quantum_learning import ContinuousQuantumLearning

class TraderComAprendizado(QuantumAlgorithmsTrader):
    def __init__(self):
        super().__init__()
        self.quantum_learner = ContinuousQuantumLearning()
    
    async def initialize(self):
        await super().initialize()
        await self.quantum_learner.initialize()
    
    async def execute_trading_cycle(self):
        # Ciclo normal de trading
        await super().execute_trading_cycle()
        
        # Aprendizado com os resultados
        for trade_result in self.execution_history[-10:]:  # Últimos 10 trades
            experience = self._create_learning_experience(trade_result)
            await self.quantum_learner.learn_from_experience(experience)
    
    async def generate_trading_signals(self, market_data):
        # Usar conhecimento aprendido para gerar sinais
        prediction = await self.quantum_learner.predict_with_knowledge(market_data)
        return self._create_signal_from_prediction(prediction)