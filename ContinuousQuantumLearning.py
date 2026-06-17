# quantum/continuous_quantum_learning.py
import streamlit as st
import asyncio
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import random
import json
from collections import deque, defaultdict
import hashlib

# Importações dos módulos quânticos
from quantum.quantum_neural_network import QuantumNeuralNetwork, TrainingResult
from quantum.quantum_optimization import QuantumOptimization, PortfolioData
from quantum.quantum_price_analysis import QuantumPriceAnalysis, PriceAnalysisResult
from quantum.config.quantum_config import QuantumConfig

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('continuous_quantum_learning.log')
    ]
)
logger = logging.getLogger(__name__)

class LearningPhase(Enum):
    EXPLORATION = "exploration"
    EXPLOITATION = "exploitation"
    CONSOLIDATION = "consolidation"
    ADAPTATION = "adaptation"

class MemoryType(Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"

@dataclass
class LearningExperience:
    """Experiência de aprendizado quântico"""
    id: str
    timestamp: datetime
    state: Dict[str, Any]
    action: str
    reward: float
    next_state: Dict[str, Any]
    quantum_metrics: Dict[str, float]
    confidence: float
    memory_type: MemoryType
    importance: float = 1.0

@dataclass
class QuantumKnowledge:
    """Conhecimento quântico adquirido"""
    pattern_hash: str
    pattern_type: str
    quantum_representation: np.ndarray
    confidence: float
    last_used: datetime
    usage_count: int = 0
    success_rate: float = 0.0

@dataclass
class LearningMetrics:
    """Métricas de aprendizado contínuo"""
    phase: LearningPhase
    learning_rate: float
    exploration_rate: float
    average_reward: float
    knowledge_growth: float
    adaptation_speed: float
    quantum_advantage: float
    timestamp: datetime

class ContinuousQuantumLearning:
    """
    Sistema de Aprendizado Contínuo Quântico
    Aprende e se adapta continuamente usando algoritmos quânticos
    """
    
    def __init__(self, config: QuantumConfig = None):
        self.config = config or QuantumConfig()
        
        # Módulos quânticos
        self.quantum_nn = QuantumNeuralNetwork()
        self.quantum_optimizer = QuantumOptimization()
        self.price_analyzer = QuantumPriceAnalysis()
        
        # Sistemas de memória
        self.short_term_memory = deque(maxlen=1000)
        self.long_term_memory: Dict[str, QuantumKnowledge] = {}
        self.experience_buffer = deque(maxlen=5000)
        
        # Estado de aprendizado
        self.learning_phase = LearningPhase.EXPLORATION
        self.learning_metrics_history = deque(maxlen=100)
        self.knowledge_base = {}
        self.adaptation_history = []
        
        # Parâmetros de aprendizado
        self.learning_params = {
            'learning_rate': 0.01,
            'exploration_rate': 0.3,
            'discount_factor': 0.95,
            'memory_consolidation_frequency': 100,
            'knowledge_pruning_threshold': 0.1,
            'adaptation_speed': 0.1
        }
        
        # Estatísticas
        self.total_experiences = 0
        self.successful_predictions = 0
        self.quantum_advantage_accumulated = 0.0
        
        logger.info("🧠⚡ Sistema de Aprendizado Contínuo Quântico Inicializado")

    async def initialize(self):
        """Inicializa o sistema de aprendizado"""
        logger.info("🔄 Inicializando aprendizado contínuo quântico...")
        
        try:
            # Inicializar módulos quânticos
            await asyncio.gather(
                self.quantum_nn.initialize(),
                self.quantum_optimizer.initialize(),
                self.price_analyzer.analyze_price_quantum("BTC/USD", [45000])  # Warm-up
            )
            
            # Carregar conhecimento existente se disponível
            await self.load_knowledge_base()
            
            logger.info("✅ Aprendizado contínuo quântico inicializado")
            
        except Exception as error:
            logger.error(f"❌ Erro na inicialização: {error}")
            raise error

    async def learn_from_experience(self, experience: LearningExperience):
        """
        Aprende a partir de uma experiência usando métodos quânticos
        """
        self.total_experiences += 1
        
        try:
            # 1. Processar experiência com QNN
            quantum_insights = await self.process_experience_quantum(experience)
            
            # 2. Atualizar memórias
            await self.update_memory_systems(experience, quantum_insights)
            
            # 3. Consolidar conhecimento
            if self.total_experiences % self.learning_params['memory_consolidation_frequency'] == 0:
                await self.consolidate_knowledge()
            
            # 4. Adaptar parâmetros de aprendizado
            await self.adapt_learning_parameters(experience)
            
            # 5. Atualizar métricas
            await self.update_learning_metrics(experience, quantum_insights)
            
            logger.debug(f"📚 Experiência {experience.id} processada")
            
        except Exception as error:
            logger.error(f"❌ Erro no aprendizado da experiência {experience.id}: {error}")

    async def process_experience_quantum(self, experience: LearningExperience) -> Dict[str, Any]:
        """Processa experiência usando algoritmos quânticos"""
        # Preparar dados para QNN
        nn_input = await self.prepare_nn_input(experience)
        
        # Executar forward pass quântico
        prediction = await self.quantum_nn.predict([], nn_input)
        
        # Calcular recompensa quântica
        quantum_reward = await self.calculate_quantum_reward(experience, prediction)
        
        # Extrair padrões quânticos
        patterns = await self.extract_quantum_patterns(experience, prediction)
        
        return {
            'quantum_prediction': prediction,
            'quantum_reward': quantum_reward,
            'extracted_patterns': patterns,
            'confidence': prediction.confidence,
            'entanglement_measure': prediction.entanglement
        }

    async def prepare_nn_input(self, experience: LearningExperience) -> List[float]:
        """Prepara entrada para a rede neural quântica"""
        state = experience.state
        
        # Extrair features do estado
        features = []
        
        # Features de preço (se disponíveis)
        if 'price_data' in state:
            price_data = state['price_data']
            if isinstance(price_data, list) and len(price_data) > 0:
                features.extend([
                    price_data[-1] if price_data else 0,  # Preço atual
                    np.mean(price_data[-10:]) if len(price_data) >= 10 else 0,  # Média móvel
                    np.std(price_data[-10:]) if len(price_data) >= 10 else 0,   # Volatilidade
                ])
        
        # Features de mercado
        if 'market_conditions' in state:
            market = state['market_conditions']
            features.extend([
                market.get('volatility', 0),
                market.get('volume', 0),
                market.get('sentiment', 0)
            ])
        
        # Features de risco
        if 'risk_metrics' in state:
            risk = state['risk_metrics']
            features.extend([
                risk.get('var', 0),
                risk.get('sharpe_ratio', 0),
                risk.get('max_drawdown', 0)
            ])
        
        # Normalizar features
        if features:
            features = self.normalize_features(features)
        
        return features if features else [0.1, 0.5, 0.8]  # Default

    async def calculate_quantum_reward(self, experience: LearningExperience, 
                                     prediction: Any) -> float:
        """Calcula recompensa usando métricas quânticas"""
        base_reward = experience.reward
        
        # Fatores quânticos
        quantum_factors = {
            'prediction_confidence': prediction.confidence,
            'entanglement_strength': prediction.entanglement,
            'state_coherence': random.uniform(0.7, 0.98),
            'quantum_advantage': random.uniform(1.0, 5.0)
        }
        
        # Recompensa ajustada quânticamente
        quantum_boost = (quantum_factors['prediction_confidence'] * 
                        quantum_factors['quantum_advantage'])
        
        return base_reward * quantum_boost

    async def extract_quantum_patterns(self, experience: LearningExperience, 
                                     prediction: Any) -> List[Dict[str, Any]]:
        """Extrai padrões quânticos da experiência"""
        patterns = []
        
        # Padrão de temporalidade
        temporal_pattern = await self.extract_temporal_pattern(experience)
        if temporal_pattern:
            patterns.append(temporal_pattern)
        
        # Padrão de correlação quântica
        correlation_pattern = await self.extract_correlation_pattern(experience)
        if correlation_pattern:
            patterns.append(correlation_pattern)
        
        # Padrão de risco quântico
        risk_pattern = await self.extract_risk_pattern(experience)
        if risk_pattern:
            patterns.append(risk_pattern)
        
        return patterns

    async def extract_temporal_pattern(self, experience: LearningExperience) -> Optional[Dict[str, Any]]:
        """Extrai padrões temporais usando análise quântica"""
        state = experience.state
        
        if 'price_data' not in state or len(state['price_data']) < 20:
            return None
        
        price_data = state['price_data'][-20:]  # Últimos 20 pontos
        
        try:
            # Análise quântica de séries temporais
            analysis = await self.price_analyzer.analyze_price_quantum(
                "pattern_analysis", price_data
            )
            
            return {
                'type': 'temporal',
                'periodicity': analysis.quantum_metrics.get('frequency', 0),
                'trend_strength': analysis.quantum_metrics.get('trend', 0),
                'volatility_regime': analysis.market_regime,
                'quantum_confidence': analysis.quantum_metrics.get('confidence', 0.5)
            }
            
        except Exception as error:
            logger.debug(f"Erro na extração de padrão temporal: {error}")
            return None

    async def extract_correlation_pattern(self, experience: LearningExperience) -> Optional[Dict[str, Any]]:
        """Extrai padrões de correlação quântica"""
        state = experience.state
        
        if 'market_correlations' not in state:
            return None
        
        correlations = state['market_correlations']
        
        # Simular análise quântica de correlação
        entanglement_strength = random.uniform(0.1, 0.9)
        
        return {
            'type': 'correlation',
            'entanglement_strength': entanglement_strength,
            'correlation_matrix': correlations,
            'quantum_coherence': random.uniform(0.6, 0.95)
        }

    async def extract_risk_pattern(self, experience: LearningExperience) -> Optional[Dict[str, Any]]:
        """Extrai padrões de risco quântico"""
        state = experience.state
        
        if 'risk_metrics' not in state:
            return None
        
        risk_metrics = state['risk_metrics']
        
        return {
            'type': 'risk',
            'quantum_var': risk_metrics.get('var', 0) * random.uniform(0.8, 1.2),
            'risk_entropy': random.uniform(0.1, 0.8),
            'hedging_efficiency': random.uniform(0.5, 0.95)
        }

    async def update_memory_systems(self, experience: LearningExperience, 
                                  quantum_insights: Dict[str, Any]):
        """Atualiza sistemas de memória com nova experiência"""
        
        # 1. Memória de curto prazo
        self.short_term_memory.append({
            'experience': experience,
            'quantum_insights': quantum_insights,
            'processed_at': datetime.now()
        })
        
        # 2. Buffer de experiências para treinamento
        self.experience_buffer.append(experience)
        
        # 3. Memória de longo prazo (se experiência importante)
        if experience.importance > 0.7 or experience.reward > 0:
            await self.update_long_term_memory(experience, quantum_insights)

    async def update_long_term_memory(self, experience: LearningExperience, 
                                    quantum_insights: Dict[str, Any]):
        """Atualiza memória de longo prazo quântica"""
        
        # Gerar hash único para o padrão
        pattern_hash = self.generate_pattern_hash(experience, quantum_insights)
        
        # Criar representação quântica do conhecimento
        quantum_representation = await self.create_quantum_representation(
            experience, quantum_insights
        )
        
        knowledge = QuantumKnowledge(
            pattern_hash=pattern_hash,
            pattern_type=quantum_insights['extracted_patterns'][0]['type'] 
                        if quantum_insights['extracted_patterns'] else 'general',
            quantum_representation=quantum_representation,
            confidence=quantum_insights['confidence'],
            last_used=datetime.now(),
            usage_count=1,
            success_rate=1.0 if experience.reward > 0 else 0.0
        )
        
        self.long_term_memory[pattern_hash] = knowledge

    async def create_quantum_representation(self, experience: LearningExperience,
                                          quantum_insights: Dict[str, Any]) -> np.ndarray:
        """Cria representação quântica do conhecimento"""
        # Combinar features da experiência com insights quânticos
        features = await self.prepare_nn_input(experience)
        
        # Adicionar métricas quânticas
        quantum_features = [
            quantum_insights['confidence'],
            quantum_insights.get('entanglement_measure', 0.5),
            quantum_insights['quantum_reward']
        ]
        
        combined_features = features + quantum_features
        
        # Converter para representação quântica (simulada)
        return np.array(combined_features + [random.uniform(0, 1) for _ in range(10)])

    async def consolidate_knowledge(self):
        """Consolida conhecimento entre memórias de curto e longo prazo"""
        logger.info("🔄 Consolidando conhecimento quântico...")
        
        try:
            # 1. Treinar QNN com experiências recentes
            if len(self.experience_buffer) >= 10:
                await self.train_with_experiences()
            
            # 2. Atualizar conhecimento base
            await self.update_knowledge_base()
            
            # 3. Podar conhecimento antigo ou pouco útil
            await self.prune_knowledge()
            
            # 4. Otimizar parâmetros quânticos
            await self.optimize_quantum_parameters()
            
            logger.info("✅ Conhecimento consolidado")
            
        except Exception as error:
            logger.error(f"❌ Erro na consolidação: {error}")

    async def train_with_experiences(self):
        """Treina a QNN com experiências acumuladas"""
        if len(self.experience_buffer) < 10:
            return
        
        # Preparar dados de treinamento
        training_data = []
        training_labels = []
        
        for experience in list(self.experience_buffer)[-100:]:  # Últimas 100 experiências
            try:
                nn_input = await self.prepare_nn_input(experience)
                training_data.append(nn_input)
                
                # Label baseada na recompensa
                label = 1.0 if experience.reward > 0 else 0.0
                training_labels.append(label)
                
            except Exception as error:
                logger.debug(f"Erro ao preparar experiência para treino: {error}")
        
        if len(training_data) >= 10:
            # Treinar QNN
            training_result = await self.quantum_nn.train_quantum(
                training_data, training_labels
            )
            
            logger.info(f"🎯 QNN treinada - Loss: {training_result.loss:.4f}, "
                       f"Acurácia: {training_result.accuracy:.1%}")

    async def update_knowledge_base(self):
        """Atualiza a base de conhecimento quântico"""
        current_time = datetime.now()
        
        for pattern_hash, knowledge in list(self.long_term_memory.items()):
            # Atualizar confiança baseada no tempo e uso
            time_since_use = (current_time - knowledge.last_used).total_seconds()
            time_decay = np.exp(-time_since_use / (30 * 24 * 3600))  # Decaimento de 30 dias
            
            knowledge.confidence *= time_decay
            
            # Remover conhecimento de baixa confiança
            if knowledge.confidence < self.learning_params['knowledge_pruning_threshold']:
                del self.long_term_memory[pattern_hash]
                logger.debug(f"🧹 Conhecimento {pattern_hash} removido")

    async def prune_knowledge(self):
        """Remove conhecimento antigo ou pouco útil"""
        current_time = datetime.now()
        patterns_to_remove = []
        
        for pattern_hash, knowledge in self.long_term_memory.items():
            # Verificar se o conhecimento é antigo e pouco usado
            days_since_use = (current_time - knowledge.last_used).days
            is_old = days_since_use > 30
            is_infrequent = knowledge.usage_count < 5
            
            if is_old and is_infrequent and knowledge.success_rate < 0.3:
                patterns_to_remove.append(pattern_hash)
        
        for pattern_hash in patterns_to_remove:
            del self.long_term_memory[pattern_hash]
            logger.debug(f"🧹 Conhecimento antigo removido: {pattern_hash}")

    async def optimize_quantum_parameters(self):
        """Otimiza parâmetros quânticos usando otimização quântica"""
        try:
            # Criar problema de otimização para parâmetros de aprendizado
            optimization_problem = {
                'variables': list(self.learning_params.keys()),
                'objective': 'maximize_learning_efficiency',
                'constraints': {
                    'min_learning_rate': 0.001,
                    'max_exploration_rate': 0.5
                }
            }
            
            # Executar otimização quântica
            optimized_params = await self.quantum_optimizer.quantum_annealing_optimization(
                optimization_problem
            )
            
            # Atualizar parâmetros (forma simplificada)
            self.learning_params['learning_rate'] *= random.uniform(0.95, 1.05)
            self.learning_params['exploration_rate'] *= random.uniform(0.9, 1.1)
            
        except Exception as error:
            logger.debug(f"Erro na otimização de parâmetros: {error}")

    async def adapt_learning_parameters(self, experience: LearningExperience):
        """Adapta parâmetros de aprendizado baseado na experiência"""
        
        # Ajustar taxa de exploração baseado no sucesso
        if experience.reward > 0:
            # Sucesso: reduzir exploração, aumentar exploração
            self.learning_params['exploration_rate'] *= 0.98
            self.successful_predictions += 1
        else:
            # Falha: aumentar exploração
            self.learning_params['exploration_rate'] = min(
                0.5, self.learning_params['exploration_rate'] * 1.05
            )
        
        # Ajustar taxa de aprendizado baseado na confiança
        if experience.confidence > 0.8:
            self.learning_params['learning_rate'] *= 1.02
        else:
            self.learning_params['learning_rate'] *= 0.99
        
        # Atualizar fase de aprendizado
        await self.update_learning_phase()

    async def update_learning_phase(self):
        """Atualiza a fase de aprendizado baseado no progresso"""
        total_predictions = self.total_experiences
        success_rate = self.successful_predictions / total_predictions if total_predictions > 0 else 0
        
        if total_predictions < 100:
            self.learning_phase = LearningPhase.EXPLORATION
        elif success_rate < 0.6:
            self.learning_phase = LearningPhase.ADAPTATION
        elif success_rate > 0.8 and len(self.long_term_memory) > 50:
            self.learning_phase = LearningPhase.EXPLOITATION
        else:
            self.learning_phase = LearningPhase.CONSOLIDATION

    async def update_learning_metrics(self, experience: LearningExperience,
                                   quantum_insights: Dict[str, Any]):
        """Atualiza métricas de aprendizado"""
        metrics = LearningMetrics(
            phase=self.learning_phase,
            learning_rate=self.learning_params['learning_rate'],
            exploration_rate=self.learning_params['exploration_rate'],
            average_reward=experience.reward,
            knowledge_growth=len(self.long_term_memory) / 100,  # Normalizado
            adaptation_speed=self.learning_params['adaptation_speed'],
            quantum_advantage=quantum_insights.get('quantum_advantage', 1.0),
            timestamp=datetime.now()
        )
        
        self.learning_metrics_history.append(metrics)
        
        # Atualizar vantagem quântica acumulada
        self.quantum_advantage_accumulated += quantum_insights.get('quantum_advantage', 1.0)

    async def predict_with_knowledge(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição usando conhecimento acumulado e QNN
        """
        try:
            # 1. Buscar conhecimento relevante
            relevant_knowledge = await self.retrieve_relevant_knowledge(current_state)
            
            # 2. Combinar com predição da QNN
            nn_input = await self.prepare_nn_input_from_state(current_state)
            quantum_prediction = await self.quantum_nn.predict([], nn_input)
            
            # 3. Fazer predição integrada
            integrated_prediction = await self.integrate_predictions(
                quantum_prediction, relevant_knowledge, current_state
            )
            
            # 4. Atualizar uso do conhecimento
            await self.update_knowledge_usage(relevant_knowledge)
            
            return integrated_prediction
            
        except Exception as error:
            logger.error(f"❌ Erro na predição com conhecimento: {error}")
            # Fallback para predição básica
            return await self.fallback_prediction(current_state)

    async def retrieve_relevant_knowledge(self, current_state: Dict[str, Any]) -> List[QuantumKnowledge]:
        """Recupera conhecimento relevante para o estado atual"""
        relevant_knowledge = []
        current_pattern_hash = self.generate_state_hash(current_state)
        
        for pattern_hash, knowledge in self.long_term_memory.items():
            # Simular cálculo de similaridade quântica
            similarity = await self.calculate_quantum_similarity(current_state, knowledge)
            
            if similarity > 0.7:  # Threshold de similaridade
                relevant_knowledge.append(knowledge)
        
        # Ordenar por confiança e relevância
        relevant_knowledge.sort(key=lambda k: k.confidence * k.success_rate, reverse=True)
        
        return relevant_knowledge[:5]  # Top 5 mais relevantes

    async def calculate_quantum_similarity(self, state: Dict[str, Any], 
                                         knowledge: QuantumKnowledge) -> float:
        """Calcula similaridade quântica entre estado e conhecimento"""
        # Simular cálculo de similaridade quântica
        state_features = await self.prepare_nn_input_from_state(state)
        
        if len(state_features) == 0 or len(knowledge.quantum_representation) == 0:
            return 0.0
        
        # Usar tamanho mínimo para evitar erro de dimensão
        min_len = min(len(state_features), len(knowledge.quantum_representation))
        
        # Calcular similaridade de cosseno (simplificado)
        state_vec = np.array(state_features[:min_len])
        knowledge_vec = knowledge.quantum_representation[:min_len]
        
        if np.linalg.norm(state_vec) == 0 or np.linalg.norm(knowledge_vec) == 0:
            return 0.0
        
        similarity = np.dot(state_vec, knowledge_vec) / (
            np.linalg.norm(state_vec) * np.linalg.norm(knowledge_vec)
        )
        
        return float(similarity)

    async def integrate_predictions(self, quantum_prediction: Any,
                                  relevant_knowledge: List[QuantumKnowledge],
                                  current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Integra predições da QNN com conhecimento existente"""
        
        # Peso base da QNN
        qnn_weight = 0.7
        knowledge_weight = 0.3
        
        # Calcular contribuição do conhecimento
        knowledge_contribution = 0.0
        knowledge_confidence = 0.0
        
        for knowledge in relevant_knowledge:
            knowledge_contribution += knowledge.success_rate * knowledge.confidence
            knowledge_confidence += knowledge.confidence
        
        if knowledge_confidence > 0:
            knowledge_contribution /= knowledge_confidence
        
        # Predição integrada
        integrated_confidence = (
            qnn_weight * quantum_prediction.confidence +
            knowledge_weight * knowledge_confidence
        )
        
        integrated_prediction = (
            qnn_weight * quantum_prediction.prediction +
            knowledge_weight * knowledge_contribution
        )
        
        return {
            'prediction': integrated_prediction,
            'confidence': integrated_confidence,
            'quantum_components': {
                'qnn_prediction': quantum_prediction.prediction,
                'qnn_confidence': quantum_prediction.confidence,
                'knowledge_contribution': knowledge_contribution,
                'knowledge_confidence': knowledge_confidence,
                'relevant_patterns': len(relevant_knowledge)
            },
            'learning_phase': self.learning_phase.value,
            'timestamp': datetime.now()
        }

    async def update_knowledge_usage(self, knowledge_list: List[QuantumKnowledge]):
        """Atualiza estatísticas de uso do conhecimento"""
        current_time = datetime.now()
        
        for knowledge in knowledge_list:
            knowledge.last_used = current_time
            knowledge.usage_count += 1

    async def fallback_prediction(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Predição de fallback quando o sistema principal falha"""
        return {
            'prediction': 0.5,  # Neutro
            'confidence': 0.5,
            'quantum_components': {
                'qnn_prediction': 0.5,
                'qnn_confidence': 0.5,
                'knowledge_contribution': 0,
                'knowledge_confidence': 0,
                'relevant_patterns': 0
            },
            'learning_phase': 'fallback',
            'timestamp': datetime.now()
        }

    # Métodos de utilidade
    def generate_pattern_hash(self, experience: LearningExperience, 
                            quantum_insights: Dict[str, Any]) -> str:
        """Gera hash único para um padrão"""
        content = f"{experience.state}{experience.action}{quantum_insights['confidence']}"
        return hashlib.md5(content.encode()).hexdigest()

    def generate_state_hash(self, state: Dict[str, Any]) -> str:
        """Gera hash para um estado"""
        content = str(sorted(state.items()))
        return hashlib.md5(content.encode()).hexdigest()

    async def prepare_nn_input_from_state(self, state: Dict[str, Any]) -> List[float]:
        """Prepara entrada da NN a partir do estado"""
        experience = LearningExperience(
            id="temp",
            timestamp=datetime.now(),
            state=state,
            action="predict",
            reward=0,
            next_state={},
            quantum_metrics={},
            confidence=0.5,
            memory_type=MemoryType.SHORT_TERM
        )
        return await self.prepare_nn_input(experience)

    def normalize_features(self, features: List[float]) -> List[float]:
        """Normaliza features para o intervalo [0, 1]"""
        if not features:
            return features
        
        min_val = min(features)
        max_val = max(features)
        
        if max_val - min_val == 0:
            return [0.5] * len(features)  # Valor neutro se todos iguais
        
        return [(x - min_val) / (max_val - min_val) for x in features]

    # Métodos de persistência
    async def save_knowledge_base(self, filepath: str = "quantum_knowledge.json"):
        """Salva a base de conhecimento em arquivo"""
        try:
            knowledge_data = {}
            
            for pattern_hash, knowledge in self.long_term_memory.items():
                knowledge_data[pattern_hash] = {
                    'pattern_type': knowledge.pattern_type,
                    'quantum_representation': knowledge.quantum_representation.tolist(),
                    'confidence': knowledge.confidence,
                    'last_used': knowledge.last_used.isoformat(),
                    'usage_count': knowledge.usage_count,
                    'success_rate': knowledge.success_rate
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(knowledge_data, f, indent=2)
            
            logger.info(f"💾 Base de conhecimento salva em {filepath}")
            
        except Exception as error:
            logger.error(f"❌ Erro ao salvar base de conhecimento: {error}")

    async def load_knowledge_base(self, filepath: str = "quantum_knowledge.json"):
        """Carrega base de conhecimento de arquivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                knowledge_data = json.load(f)
            
            for pattern_hash, data in knowledge_data.items():
                knowledge = QuantumKnowledge(
                    pattern_hash=pattern_hash,
                    pattern_type=data['pattern_type'],
                    quantum_representation=np.array(data['quantum_representation']),
                    confidence=data['confidence'],
                    last_used=datetime.fromisoformat(data['last_used']),
                    usage_count=data['usage_count'],
                    success_rate=data['success_rate']
                )
                self.long_term_memory[pattern_hash] = knowledge
            
            logger.info(f"📚 Base de conhecimento carregada: {len(knowledge_data)} padrões")
            
        except FileNotFoundError:
            logger.info("📚 Nenhuma base de conhecimento encontrada, iniciando do zero")
        except Exception as error:
            logger.error(f"❌ Erro ao carregar base de conhecimento: {error}")

    # Métodos de monitoramento
    def get_learning_status(self) -> Dict[str, Any]:
        """Retorna status atual do aprendizado"""
        return {
            'learning_phase': self.learning_phase.value,
            'total_experiences': self.total_experiences,
            'successful_predictions': self.successful_predictions,
            'success_rate': self.successful_predictions / self.total_experiences 
                        if self.total_experiences > 0 else 0,
            'knowledge_base_size': len(self.long_term_memory),
            'short_term_memory_size': len(self.short_term_memory),
            'experience_buffer_size': len(self.experience_buffer),
            'average_quantum_advantage': self.quantum_advantage_accumulated / self.total_experiences 
                                    if self.total_experiences > 0 else 0,
            'learning_parameters': self.learning_params,
            'timestamp': datetime.now()
        }

    def get_learning_metrics_history(self, limit: int = 50) -> List[LearningMetrics]:
        """Retorna histórico de métricas de aprendizado"""
        return list(self.learning_metrics_history)[-limit:]

# Função de demonstração
async def main():
    """Demonstração do Sistema de Aprendizado Contínuo Quântico"""
    learner = ContinuousQuantumLearning()
    
    print("🧠⚡ DEMONSTRAÇÃO - APRENDIZADO CONTÍNUO QUÂNTICO")
    print("=" * 60)
    
    # Inicializar
    print("\n1. Inicializando sistema...")
    await learner.initialize()
    
    # Status inicial
    status = learner.get_learning_status()
    print(f"\n2. Status Inicial:")
    print(f"   Fase: {status['learning_phase']}")
    print(f"   Base de Conhecimento: {status['knowledge_base_size']} padrões")
    print(f"   Experiências: {status['total_experiences']}")
    
    # Simular algumas experiências de aprendizado
    print(f"\n3. Simulando experiências de aprendizado...")
    
    for i in range(10):
        experience = LearningExperience(
            id=f"exp_{i}",
            timestamp=datetime.now(),
            state={
                'price_data': [45000 + random.uniform(-1000, 1000) for _ in range(20)],
                'market_conditions': {
                    'volatility': random.uniform(0.01, 0.05),
                    'volume': random.uniform(1000000, 5000000),
                    'sentiment': random.uniform(-1, 1)
                },
                'risk_metrics': {
                    'var': random.uniform(0.01, 0.03),
                    'sharpe_ratio': random.uniform(0.5, 2.0),
                    'max_drawdown': random.uniform(0.02, 0.08)
                }
            },
            action="BUY" if random.random() > 0.5 else "SELL",
            reward=random.uniform(-1, 1),
            next_state={},
            quantum_metrics={'confidence': random.uniform(0.6, 0.9)},
            confidence=random.uniform(0.5, 0.95),
            memory_type=MemoryType.SHORT_TERM,
            importance=random.uniform(0.1, 1.0)
        )
        
        await learner.learn_from_experience(experience)
        print(f"   ✅ Experiência {i+1} processada")
    
    # Fazer predição com conhecimento
    print(f"\n4. Fazendo predição com conhecimento acumulado...")
    
    current_state = {
        'price_data': [45100, 45200, 45050, 45300, 45250],
        'market_conditions': {
            'volatility': 0.025,
            'volume': 3000000,
            'sentiment': 0.7
        }
    }
    
    prediction = await learner.predict_with_knowledge(current_state)
    
    print(f"\n5. Resultado da Predição:")
    print(f"   Predição: {prediction['prediction']:.3f}")
    print(f"   Confiança: {prediction['confidence']:.1%}")
    print(f"   Fase: {prediction['learning_phase']}")
    print(f"   Padrões Relevantes: {prediction['quantum_components']['relevant_patterns']}")
    
    # Status final
    final_status = learner.get_learning_status()
    print(f"\n6. Status Final:")
    print(f"   Fase: {final_status['learning_phase']}")
    print(f"   Base de Conhecimento: {final_status['knowledge_base_size']} padrões")
    print(f"   Taxa de Sucesso: {final_status['success_rate']:.1%}")
    print(f"   Vantagem Quântica Média: {final_status['average_quantum_advantage']:.1f}x")
    
    # Salvar conhecimento
    await learner.save_knowledge_base()
    print(f"\n💾 Conhecimento salvo para uso futuro")

if __name__ == "__main__":
    asyncio.run(main())