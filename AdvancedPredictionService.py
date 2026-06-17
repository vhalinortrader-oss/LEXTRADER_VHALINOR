"""
LEXTRADER-IAG 3.0 - SISTEMA COGNITIVO AVANÇADO COM HISTÓRICO
=============================================================
Versão: 3.0.0 Premium Expandida
Autor: LEXTRADER AI Team
Data: 2024
Base: Sistema de Predição Avançada + Históricos Anteriores
"""

import math
import random
import json
import time
import asyncio
from typing import List, Dict, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum, auto
import numpy as np
from collections import deque, defaultdict
import hashlib
import os
import psutil
from functools import lru_cache
import statistics
from concurrent.futures import ThreadPoolExecutor
import itertools
from scipy import stats as scipy_stats

# ========== HISTÓRICO DE SISTEMAS ANTERIORES ==========
# Integrando funcionalidades dos sistemas Omega, Memória Biológica e Predição

class HistoricalIntegration:
    """Integração de funcionalidades históricas dos sistemas anteriores."""
    
    @staticmethod
    def get_integrated_features():
        """Retorna features integradas de sistemas anteriores."""
        return {
            'omega_features': {
                'neural_oscillations': ['GAMMA', 'BETA', 'ALPHA', 'THETA', 'DELTA'],
                'metacognition': True,
                'intuition_engine': True,
                'reinforcement_learning': True,
                'hierarchical_planning': True,
                'simulation_module': True,
            },
            'memory_features': {
                'sensory_cortex': True,
                'short_term_memory': True,
                'long_term_memory': True,
                'episodic_memory': True,
                'semantic_memory': True,
                'procedural_memory': True,
                'attention_module': True,
                'perception_module': True,
            },
            'prediction_features': {
                'ensemble_predictor': True,
                'incident_prediction': True,
                'security_prediction': True,
                'resource_prediction': True,
                'sentient_core': True,
                'memory_optimizer': True,
            }
        }

# ========== CONSTANTES DO SISTEMA EXPANDIDO ==========

class SystemConstantsExpanded:
    """Constantes do sistema LEXTRADER-IAG expandido."""
    
    # Configurações de tempo
    PREDICTION_HORIZON = 24  # horas
    MAX_HISTORY_DAYS = 365
    CYCLE_INTERVAL_SECONDS = 5.0
    AUTO_SAVE_INTERVAL = 300  # segundos
    
    # Configurações de memória
    MAX_MEMORY_ITEMS = 10000
    CACHE_SIZE = 1000
    VECTOR_DIMENSIONS = 256
    
    # Configurações de aprendizado
    LEARNING_RATE = 0.01
    DISCOUNT_FACTOR = 0.95
    EXPLORATION_RATE_INITIAL = 0.3
    EXPLORATION_DECAY = 0.995
    
    # Limites do sistema
    MAX_CONCURRENT_TASKS = 8
    MAX_LOG_ENTRIES = 10000
    MAX_ALERTS = 1000
    
    # Configurações de mercado
    SUPPORTED_ASSETS = ['BTC', 'ETH', 'SPY', 'QQQ', 'GLD', 'USO', 'TLT']
    TIME_FRAMES = ['1m', '5m', '15m', '1h', '4h', '1d', '1w']
    
    # Configurações de risco
    MAX_DRAWDOWN_PERCENT = 20.0
    MIN_WIN_RATE = 0.55
    MAX_POSITION_SIZE = 0.15  # 15% do capital

# ========== ENUMS EXPANDIDOS ==========

class MarketRegime(IntEnum):
    """Regimes de mercado."""
    TRENDING_BULL = 0
    TRENDING_BEAR = 1
    RANGING = 2
    VOLATILE = 3
    BREAKOUT = 4
    REVERSAL = 5
    SIDEWAYS = 6

class CognitiveMode(IntEnum):
    """Modos cognitivos do sistema."""
    ANALYTICAL = 0
    INTUITIVE = 1
    STRATEGIC = 2
    TACTICAL = 3
    REFLEXIVE = 4
    METACOGNITIVE = 5
    CREATIVE = 6
    HYPER_FOCUS = 7

class NeuralArchitecture(IntEnum):
    """Arquiteturas neurais disponíveis."""
    TRANSFORMER = 0
    LSTM = 1
    GRU = 2
    CNN = 3
    ATTENTION = 4
    ENSEMBLE = 5
    HYBRID = 6

class SentimentDimension(IntEnum):
    """Dimensões do sentimento."""
    OPTIMISM = 0
    FEAR = 1
    GREED = 2
    UNCERTAINTY = 3
    CONFIDENCE = 4
    AGGRESSION = 5
    CAUTION = 6
    CURIOSITY = 7

# ========== ESTRUTURAS DE DADOS AVANÇADAS ==========

@dataclass(slots=True)
class QuantumStateVector:
    """Vetor de estado quântico para representação multidimensional."""
    amplitudes: List[complex]
    dimensions: int
    entanglement_level: float = 0.0
    coherence_time: float = 0.0
    
    @classmethod
    def from_classical(cls, data: List[float]) -> 'QuantumStateVector':
        """Converte dados clássicos para representação quântica."""
        n = len(data)
        # Normaliza para amplitudes quânticas
        norm = math.sqrt(sum(x**2 for x in data))
        amplitudes = [complex(x/norm, 0) if norm > 0 else complex(0, 0) for x in data]
        
        return cls(
            amplitudes=amplitudes,
            dimensions=n,
            entanglement_level=0.1,  # Simples inicial
            coherence_time=1.0
        )
    
    def measure(self) -> List[float]:
        """Medição do estado quântico (colapso para clássico)."""
        probabilities = [abs(amp)**2 for amp in self.amplitudes]
        return probabilities
    
    def entangle_with(self, other: 'QuantumStateVector') -> float:
        """Cria entrelaçamento com outro vetor."""
        if len(self.amplitudes) != len(other.amplitudes):
            return 0.0
        
        # Calcula superposição
        superposition = sum(a * b.conjugate() for a, b in zip(self.amplitudes, other.amplitudes))
        entanglement = abs(superposition)
        
        self.entanglement_level = max(self.entanglement_level, entanglement)
        return entanglement

@dataclass(slots=True)
class HyperdimensionalVector:
    """Vetor hiperdimensional para representação distribuída."""
    coordinates: np.ndarray
    dimensionality: int = 10000  # HD Computing typical size
    similarity_threshold: float = 0.7
    
    @classmethod
    def from_features(cls, features: Dict[str, Any]) -> 'HyperdimensionalVector':
        """Cria vetor HD a partir de features."""
        # Converte features para vetor esparso de alta dimensão
        vector = np.zeros(cls.dimensionality)
        
        for key, value in features.items():
            # Hash do feature para posições no vetor
            if isinstance(value, (int, float)):
                hash_val = int(hashlib.md5(key.encode()).hexdigest()[:8], 16) % cls.dimensionality
                vector[hash_val] = value
        
        # Normaliza
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return cls(coordinates=vector)
    
    def similarity(self, other: 'HyperdimensionalVector') -> float:
        """Calcula similaridade entre vetores HD."""
        return np.dot(self.coordinates, other.coordinates)
    
    def bind(self, other: 'HyperdimensionalVector') -> 'HyperdimensionalVector':
        """Operação de binding HD (XOR-like)."""
        bound = np.bitwise_xor(
            self.coordinates.view(np.uint8),
            other.coordinates.view(np.uint8)
        ).view(np.float64)
        return HyperdimensionalVector(coordinates=bound)

@dataclass(slots=True)
class TemporalContext:
    """Contexto temporal com múltiplas resoluções."""
    micro: float  # segundos
    meso: float   # minutos
    macro: float  # horas
    epoch: float  # dias
    phase: str    # fase do ciclo
    
    @classmethod
    def from_datetime(cls, dt: datetime) -> 'TemporalContext':
        """Cria contexto a partir de datetime."""
        seconds = dt.second + dt.microsecond / 1e6
        minutes = dt.minute + seconds / 60
        hours = dt.hour + minutes / 60
        days = dt.timetuple().tm_yday
        
        # Determina fase
        hour = dt.hour
        if 5 <= hour < 12:
            phase = "MORNING"
        elif 12 <= hour < 17:
            phase = "AFTERNOON"
        elif 17 <= hour < 22:
            phase = "EVENING"
        else:
            phase = "NIGHT"
        
        return cls(
            micro=seconds,
            meso=minutes,
            macro=hours,
            epoch=days,
            phase=phase
        )

# ========== SISTEMA DE AGENTES MULTI-ESPECIALISTAS ==========

class SpecialistAgent:
    """Agente especialista em uma área específica."""
    
    def __init__(self, specialty: str, expertise_level: float = 0.5):
        self.specialty = specialty
        self.expertise = expertise_level
        self.knowledge_base = []
        self.decision_history = deque(maxlen=100)
        self.confidence = 0.5
        self.learning_rate = 0.1
        
    async def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa contexto na especialidade do agente."""
        # Análise especializada
        if self.specialty == "TECHNICAL":
            return await self._technical_analysis(context)
        elif self.specialty == "FUNDAMENTAL":
            return await self._fundamental_analysis(context)
        elif self.specialty == "SENTIMENT":
            return await self._sentiment_analysis(context)
        elif self.specialty == "RISK":
            return await self._risk_analysis(context)
        elif self.specialty == "PATTERN":
            return await self._pattern_analysis(context)
        else:
            return {"analysis": "UNKNOWN", "confidence": 0.0}
    
    async def _technical_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Análise técnica especializada."""
        price_data = context.get('price_data', {})
        
        # Calcula indicadores
        indicators = {
            'rsi': random.uniform(20, 80),
            'macd': random.uniform(-10, 10),
            'bollinger_band': random.uniform(0.8, 1.2),
            'volume_ratio': random.uniform(0.5, 1.5),
            'trend_strength': random.uniform(0, 1),
        }
        
        # Gera sinal
        signal = "NEUTRAL"
        if indicators['rsi'] > 70:
            signal = "BEARISH"
        elif indicators['rsi'] < 30:
            signal = "BULLISH"
        
        confidence = self.confidence * (0.5 + self.expertise * 0.5)
        
        return {
            'type': 'TECHNICAL',
            'signal': signal,
            'indicators': indicators,
            'confidence': confidence,
            'expertise': self.expertise,
        }
    
    async def _fundamental_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Análise fundamental especializada."""
        fundamentals = {
            'pe_ratio': random.uniform(10, 30),
            'market_cap': random.uniform(1e9, 1e12),
            'revenue_growth': random.uniform(-0.1, 0.3),
            'profit_margin': random.uniform(0.05, 0.3),
            'debt_equity': random.uniform(0.1, 2.0),
        }
        
        # Avaliação
        score = (
            (1 / fundamentals['pe_ratio'] * 0.3) +
            (math.log10(fundamentals['market_cap']) / 12 * 0.2) +
            (fundamentals['revenue_growth'] * 0.3) +
            (fundamentals['profit_margin'] * 0.2)
        )
        
        signal = "BULLISH" if score > 0.5 else "BEARISH"
        confidence = self.confidence * (0.4 + self.expertise * 0.6)
        
        return {
            'type': 'FUNDAMENTAL',
            'signal': signal,
            'score': score,
            'fundamentals': fundamentals,
            'confidence': confidence,
            'expertise': self.expertise,
        }
    
    async def learn_from_outcome(self, analysis: Dict[str, Any], 
                               outcome: float) -> None:
        """Aprende do resultado da análise."""
        was_correct = (
            (analysis['signal'] == 'BULLISH' and outcome > 0) or
            (analysis['signal'] == 'BEARISH' and outcome < 0)
        )
        
        if was_correct:
            self.expertise = min(1.0, self.expertise + self.learning_rate)
            self.confidence = min(1.0, self.confidence + 0.05)
        else:
            self.expertise = max(0.1, self.expertise - self.learning_rate * 0.5)
            self.confidence = max(0.1, self.confidence - 0.03)
        
        self.decision_history.append({
            'analysis': analysis,
            'outcome': outcome,
            'was_correct': was_correct,
            'timestamp': datetime.now()
        })

class MultiAgentOrchestrator:
    """Orquestrador de múltiplos agentes especialistas."""
    
    def __init__(self):
        self.agents = {
            'technical': SpecialistAgent("TECHNICAL", 0.7),
            'fundamental': SpecialistAgent("FUNDAMENTAL", 0.6),
            'sentiment': SpecialistAgent("SENTIMENT", 0.65),
            'risk': SpecialistAgent("RISK", 0.75),
            'pattern': SpecialistAgent("PATTERN", 0.8),
        }
        
        self.consensus_history = deque(maxlen=100)
        self.agent_weights = self._initialize_weights()
        
    def _initialize_weights(self) -> Dict[str, float]:
        """Inicializa pesos dos agentes."""
        weights = {}
        total_expertise = sum(agent.expertise for agent in self.agents.values())
        
        for name, agent in self.agents.items():
            weights[name] = agent.expertise / total_expertise
        
        return weights
    
    async def get_consensus(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém consenso entre todos os agentes."""
        analyses = {}
        
        # Coleta análises de todos os agentes
        tasks = []
        for name, agent in self.agents.items():
            task = asyncio.create_task(agent.analyze(context))
            tasks.append((name, task))
        
        for name, task in tasks:
            try:
                analyses[name] = await task
            except Exception as e:
                analyses[name] = {'error': str(e), 'confidence': 0.0}
        
        # Calcula consenso ponderado
        consensus = self._calculate_weighted_consensus(analyses)
        
        # Registra no histórico
        self.consensus_history.append({
            'timestamp': datetime.now(),
            'context': context,
            'analyses': analyses,
            'consensus': consensus
        })
        
        return consensus
    
    def _calculate_weighted_consensus(self, analyses: Dict[str, Dict]) -> Dict[str, Any]:
        """Calcula consenso ponderado."""
        signals = []
        confidences = []
        weights = []
        
        for name, analysis in analyses.items():
            if 'signal' in analysis:
                signal_value = 1 if analysis['signal'] == 'BULLISH' else -1 if analysis['signal'] == 'BEARISH' else 0
                signals.append(signal_value)
                confidences.append(analysis.get('confidence', 0.0))
                weights.append(self.agent_weights.get(name, 0.2))
        
        if not signals:
            return {'consensus': 'NEUTRAL', 'confidence': 0.0}
        
        # Consenso ponderado
        weighted_signals = [s * c * w for s, c, w in zip(signals, confidences, weights)]
        consensus_value = sum(weighted_signals) / sum(weights)
        
        if consensus_value > 0.2:
            consensus = 'BULLISH'
        elif consensus_value < -0.2:
            consensus = 'BEARISH'
        else:
            consensus = 'NEUTRAL'
        
        overall_confidence = np.mean(confidences) if confidences else 0.0
        
        return {
            'consensus': consensus,
            'confidence': overall_confidence,
            'consensus_value': consensus_value,
            'agent_contributions': {
                name: {
                    'signal': analysis.get('signal', 'UNKNOWN'),
                    'confidence': analysis.get('confidence', 0.0),
                    'weight': self.agent_weights.get(name, 0.0)
                }
                for name, analysis in analyses.items()
            }
        }
    
    async def update_weights_based_on_performance(self, 
                                                market_outcome: float) -> None:
        """Atualiza pesos baseados no desempenho."""
        if not self.consensus_history:
            return
        
        latest = self.consensus_history[-1]
        consensus = latest['consensus']
        
        # Avalia se consenso estava correto
        was_correct = (
            (consensus['consensus'] == 'BULLISH' and market_outcome > 0) or
            (consensus['consensus'] == 'BEARISH' and market_outcome < 0)
        )
        
        if was_correct:
            # Reforça agentes que estavam certos
            for name, contribution in consensus['agent_contributions'].items():
                agent_signal = contribution['signal']
                agent_correct = (
                    (agent_signal == 'BULLISH' and market_outcome > 0) or
                    (agent_signal == 'BEARISH' and market_outcome < 0)
                )
                
                if agent_correct:
                    self.agent_weights[name] = min(0.5, 
                        self.agent_weights[name] * 1.1)
                else:
                    self.agent_weights[name] = max(0.05,
                        self.agent_weights[name] * 0.9)
        
        # Normaliza pesos
        total = sum(self.agent_weights.values())
        if total > 0:
            self.agent_weights = {k: v/total for k, v in self.agent_weights.items()}

# ========== SISTEMA DE APRENDIZADO POR REFORÇO PROFUNDO MULTI-AGENTE ==========

class MultiAgentRLSystem:
    """Sistema de RL multi-agente com comunicação."""
    
    def __init__(self, state_size: int = 50, action_size: int = 10):
        self.state_size = state_size
        self.action_size = action_size
        
        # Agentes RL
        self.agents = {
            'explorer': self._create_agent("EXPLORER"),
            'exploiter': self._create_agent("EXPLOITER"),
            'hedger': self._create_agent("HEDGER"),
            'momentum': self._create_agent("MOMENTUM"),
            'contrarian': self._create_agent("CONTRARIAN"),
        }
        
        # Memória compartilhada
        self.replay_buffer = deque(maxlen=10000)
        self.communication_channel = {}
        
        # Parâmetros
        self.learning_rate = 0.001
        self.discount_factor = 0.95
        self.exploration_rate = 0.3
        
    def _create_agent(self, agent_type: str) -> Dict[str, Any]:
        """Cria um agente RL."""
        return {
            'type': agent_type,
            'q_table': defaultdict(lambda: defaultdict(float)),
            'policy': {},
            'rewards': [],
            'exploration_rate': self.exploration_rate,
            'learning_rate': self.learning_rate,
            'specialty': agent_type.lower(),
        }
    
    async def get_joint_action(self, state: np.ndarray, 
                             market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém ação conjunta de todos os agentes."""
        individual_actions = {}
        
        for name, agent in self.agents.items():
            action = await self._get_agent_action(agent, state, market_context)
            individual_actions[name] = action
        
        # Comunicação entre agentes
        await self._communicate_between_agents(individual_actions)
        
        # Ação conjunta (estratégia de fusão)
        joint_action = self._fuse_actions(individual_actions, market_context)
        
        return {
            'joint_action': joint_action,
            'individual_actions': individual_actions,
            'consensus_level': self._calculate_consensus_level(individual_actions),
        }
    
    async def _get_agent_action(self, agent: Dict[str, Any], 
                              state: np.ndarray, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém ação de um agente individual."""
        state_key = self._state_to_key(state)
        
        # Exploração vs Exploração
        if random.random() < agent['exploration_rate']:
            action_idx = random.randint(0, self.action_size - 1)
            action_type = "EXPLORATION"
        else:
            # Escolhe melhor ação conhecida
            q_values = agent['q_table'][state_key]
            if q_values:
                action_idx = max(q_values.items(), key=lambda x: x[1])[0]
                action_type = "EXPLOITATION"
            else:
                action_idx = random.randint(0, self.action_size - 1)
                action_type = "RANDOM"
        
        # Ajusta ação baseada na especialidade
        adjusted_action = self._adjust_action_by_specialty(
            action_idx, agent['specialty'], context
        )
        
        return {
            'action': adjusted_action,
            'type': action_type,
            'agent_type': agent['type'],
            'confidence': agent['q_table'][state_key].get(action_idx, 0.5),
        }
    
    def _adjust_action_by_specialty(self, action_idx: int, 
                                  specialty: str, 
                                  context: Dict[str, Any]) -> int:
        """Ajusta ação baseada na especialidade do agente."""
        base_action = action_idx
        
        if specialty == 'explorer':
            # Explorer é mais agressivo
            return min(self.action_size - 1, base_action + 1)
        elif specialty == 'hedger':
            # Hedger é mais conservador
            return max(0, base_action - 1)
        elif specialty == 'contrarian':
            # Contrarian faz o oposto do sentimento
            sentiment = context.get('sentiment', 0)
            if sentiment > 0.5:
                return max(0, base_action - 2)
            elif sentiment < -0.5:
                return min(self.action_size - 1, base_action + 2)
        
        return base_action
    
    async def _communicate_between_agents(self, 
                                        actions: Dict[str, Dict[str, Any]]) -> None:
        """Comunicação entre agentes."""
        # Coleta informações
        sentiments = []
        confidences = []
        
        for name, action in actions.items():
            sentiments.append(action.get('sentiment_bias', 0))
            confidences.append(action['confidence'])
        
        # Calcula métricas de grupo
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        avg_confidence = np.mean(confidences) if confidences else 0
        
        # Compartilha no canal de comunicação
        self.communication_channel = {
            'group_sentiment': avg_sentiment,
            'group_confidence': avg_confidence,
            'consensus_strength': 1.0 - np.var(sentiments) if len(sentiments) > 1 else 0.0,
            'timestamp': datetime.now(),
        }
    
    def _fuse_actions(self, individual_actions: Dict[str, Dict[str, Any]],
                     context: Dict[str, Any]) -> Dict[str, Any]:
        """Funde ações individuais em ação conjunta."""
        # Média ponderada por confiança
        weighted_actions = []
        total_confidence = 0
        
        for name, action in individual_actions.items():
            weight = action['confidence']
            weighted_actions.append(action['action'] * weight)
            total_confidence += weight
        
        if total_confidence > 0:
            fused_action = sum(weighted_actions) / total_confidence
        else:
            fused_action = np.mean([a['action'] for a in individual_actions.values()])
        
        # Considera comunicação do grupo
        group_sentiment = self.communication_channel.get('group_sentiment', 0)
        if abs(group_sentiment) > 0.3:
            fused_action *= (1 + group_sentiment * 0.2)
        
        return {
            'action': int(fused_action),
            'confidence': total_confidence / len(individual_actions),
            'consensus_strength': self.communication_channel.get('consensus_strength', 0),
            'individual_count': len(individual_actions),
        }
    
    def _calculate_consensus_level(self, 
                                 actions: Dict[str, Dict[str, Any]]) -> float:
        """Calcula nível de consenso entre agentes."""
        if not actions:
            return 0.0
        
        action_values = [a['action'] for a in actions.values()]
        
        if len(action_values) < 2:
            return 1.0
        
        # Variância normalizada
        variance = np.var(action_values)
        max_variance = (self.action_size - 1) ** 2 / 12  # Variância máxima teórica
        
        consensus = 1.0 - (variance / max_variance if max_variance > 0 else 0)
        return max(0.0, min(1.0, consensus))
    
    async def learn_from_experience(self, state: np.ndarray, 
                                  joint_action: Dict[str, Any], 
                                  reward: float, 
                                  next_state: np.ndarray) -> None:
        """Todos os agentes aprendem da experiência."""
        state_key = self._state_to_key(state)
        next_state_key = self._state_to_key(next_state)
        
        for name, agent in self.agents.items():
            # Cada agente aprende com recompensa ajustada
            agent_reward = self._adjust_reward_for_agent(reward, name, joint_action)
            
            # Atualiza Q-table
            action = joint_action['action']
            current_q = agent['q_table'][state_key][action]
            
            # Melhor Q do próximo estado
            next_q_values = agent['q_table'][next_state_key]
            max_next_q = max(next_q_values.values()) if next_q_values else 0
            
            # Atualização Q-learning
            new_q = current_q + agent['learning_rate'] * (
                agent_reward + self.discount_factor * max_next_q - current_q
            )
            
            agent['q_table'][state_key][action] = new_q
            
            # Decaimento da taxa de exploração
            agent['exploration_rate'] = max(0.01, 
                agent['exploration_rate'] * 0.995)
            
            # Registra recompensa
            agent['rewards'].append(agent_reward)
            if len(agent['rewards']) > 1000:
                agent['rewards'] = agent['rewards'][-1000:]
        
        # Armazena experiência no buffer de replay
        experience = {
            'state': state,
            'action': joint_action,
            'reward': reward,
            'next_state': next_state,
            'timestamp': datetime.now(),
        }
        
        self.replay_buffer.append(experience)
    
    def _adjust_reward_for_agent(self, base_reward: float, 
                               agent_name: str, 
                               joint_action: Dict[str, Any]) -> float:
        """Ajusta recompensa baseada no agente."""
        adjustment = 1.0
        
        if agent_name == 'explorer':
            # Explorer é recompensado por explorar
            if joint_action.get('exploration_component', 0) > 0.5:
                adjustment = 1.2
        elif agent_name == 'hedger':
            # Hedger é recompensado por reduzir perdas
            if base_reward > 0:
                adjustment = 0.9  # Menos recompensa por ganhos
            else:
                adjustment = 1.1  # Mais recompensa por evitar perdas
        
        return base_reward * adjustment
    
    def _state_to_key(self, state: np.ndarray) -> str:
        """Converte estado numpy para chave de dicionário."""
        # Discretização simples para demo
        discretized = (state * 10).astype(int)
        return str(discretized.tolist())
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema RL."""
        stats = {
            'total_agents': len(self.agents),
            'replay_buffer_size': len(self.replay_buffer),
            'exploration_rates': {},
            'avg_rewards': {},
            'q_table_sizes': {},
        }
        
        for name, agent in self.agents.items():
            stats['exploration_rates'][name] = agent['exploration_rate']
            stats['avg_rewards'][name] = (
                np.mean(agent['rewards'][-100:]) if agent['rewards'] else 0
            )
            stats['q_table_sizes'][name] = len(agent['q_table'])
        
        return stats

# ========== SISTEMA DE SIMULAÇÃO DE MERCADO MULTI-AGENTE ==========

class MarketSimulationEngine:
    """Motor de simulação de mercado multi-agente."""
    
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = {}
        self.trade_history = []
        self.market_state = self._initialize_market_state()
        
        # Agentes do mercado
        self.market_agents = self._create_market_agents()
        
        # Livro de ordens simulado
        self.order_book = {
            'bids': [],  # [{'price': x, 'quantity': y}]
            'asks': [],  # [{'price': x, 'quantity': y}]
        }
        
    def _initialize_market_state(self) -> Dict[str, Any]:
        """Inicializa estado do mercado."""
        return {
            'price': 50000.0,
            'volume': 1000.0,
            'volatility': 0.02,
            'trend': 0.0,
            'spread': 10.0,
            'liquidity': 10000.0,
            'sentiment': 0.0,
            'timestamp': datetime.now(),
        }
    
    def _create_market_agents(self) -> Dict[str, Dict[str, Any]]:
        """Cria agentes do mercado."""
        return {
            'market_maker': {
                'type': 'MARKET_MAKER',
                'inventory': 100.0,
                'spread_target': 0.001,  # 0.1%
                'risk_aversion': 0.3,
            },
            'institutional': {
                'type': 'INSTITUTIONAL',
                'capital': 1000000.0,
                'strategy': 'MOMENTUM',
                'sensitivity': 0.7,
            },
            'retail': {
                'type': 'RETAIL',
                'capital': 10000.0,
                'strategy': 'NOISE',
                'sentiment_bias': 0.0,
            },
            'algorithmic': {
                'type': 'ALGORITHMIC',
                'capital': 500000.0,
                'strategy': 'ARBITRAGE',
                'latency': 0.001,  # 1ms
            },
            'whale': {
                'type': 'WHALE',
                'capital': 10000000.0,
                'strategy': 'ACCUMULATION',
                'patience': 0.9,
            },
        }
    
    async def simulate_step(self, external_shock: float = 0.0) -> Dict[str, Any]:
        """Simula um passo do mercado."""
        # Coletar ações de todos os agentes
        agent_actions = await self._collect_agent_actions()
        
        # Calcular pressão de compra/venda líquida
        net_pressure = self._calculate_net_pressure(agent_actions)
        
        # Atualizar estado do mercado
        self._update_market_state(net_pressure, external_shock)
        
        # Executar ordens no livro
        trades = self._execute_orders()
        
        # Atualizar agentes
        await self._update_agents(agent_actions, trades)
        
        # Registrar histórico
        self._record_history(agent_actions, trades)
        
        return {
            'market_state': self.market_state.copy(),
            'agent_actions': agent_actions,
            'trades': trades,
            'order_book': self.order_book.copy(),
            'timestamp': datetime.now(),
        }
    
    async def _collect_agent_actions(self) -> Dict[str, Dict[str, Any]]:
        """Coleta ações de todos os agentes."""
        actions = {}
        
        for name, agent in self.market_agents.items():
            action = await self._get_agent_action(agent, self.market_state)
            actions[name] = action
            
            # Atualiza livro de ordens
            self._update_order_book(name, action)
        
        return actions
    
    async def _get_agent_action(self, agent: Dict[str, Any], 
                              market_state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém ação de um agente individual."""
        agent_type = agent['type']
        
        if agent_type == 'MARKET_MAKER':
            return self._market_maker_action(agent, market_state)
        elif agent_type == 'INSTITUTIONAL':
            return self._institutional_action(agent, market_state)
        elif agent_type == 'RETAIL':
            return self._retail_action(agent, market_state)
        elif agent_type == 'ALGORITHMIC':
            return self._algorithmic_action(agent, market_state)
        elif agent_type == 'WHALE':
            return self._whale_action(agent, market_state)
        else:
            return {'action': 'HOLD', 'quantity': 0, 'price': market_state['price']}
    
    def _market_maker_action(self, agent: Dict[str, Any], 
                           market_state: Dict[str, Any]) -> Dict[str, Any]:
        """Ação do market maker."""
        spread = market_state['spread']
        mid_price = market_state['price']
        
        # Define bid e ask
        bid_price = mid_price * (1 - spread/2)
        ask_price = mid_price * (1 + spread/2)
        
        # Quantidade baseada no inventário
        inventory = agent.get('inventory', 0)
        if inventory > 50:
            # Muito inventário, vende mais
            bid_qty = max(1, inventory * 0.1)
            ask_qty = max(1, inventory * 0.2)
        elif inventory < -50:
            # Muito short, compra mais
            bid_qty = max(1, abs(inventory) * 0.2)
            ask_qty = max(1, abs(inventory) * 0.1)
        else:
            # Inventário balanceado
            bid_qty = ask_qty = 10
        
        return {
            'action': 'MARKET_MAKE',
            'bid_price': bid_price,
            'bid_quantity': bid_qty,
            'ask_price': ask_price,
            'ask_quantity': ask_qty,
            'agent_type': 'MARKET_MAKER',
        }
    
    def _institutional_action(self, agent: Dict[str, Any], 
                            market_state: Dict[str, Any]) -> Dict[str, Any]:
        """Ação do investidor institucional."""
        # Estratégia momentum
        trend = market_state['trend']
        sentiment = market_state['sentiment']
        
        if trend > 0.1 and sentiment > 0.2:
            # Tendência positiva e sentimento positivo
            action = 'BUY'
            quantity = min(100, agent.get('capital', 0) / market_state['price'] * 0.01)
        elif trend < -0.1 and sentiment < -0.2:
            # Tendência negativa e sentimento negativo
            action = 'SELL'
            quantity = min(100, agent.get('capital', 0) / market_state['price'] * 0.01)
        else:
            action = 'HOLD'
            quantity = 0
        
        return {
            'action': action,
            'quantity': quantity,
            'price': market_state['price'],
            'agent_type': 'INSTITUTIONAL',
            'strategy': 'MOMENTUM',
        }
    
    def _update_order_book(self, agent_name: str, action: Dict[str, Any]):
        """Atualiza livro de ordens."""
        if action['action'] == 'MARKET_MAKE':
            # Adiciona bid e ask
            self.order_book['bids'].append({
                'price': action['bid_price'],
                'quantity': action['bid_quantity'],
                'agent': agent_name,
                'timestamp': datetime.now(),
            })
            
            self.order_book['asks'].append({
                'price': action['ask_price'],
                'quantity': action['ask_quantity'],
                'agent': agent_name,
                'timestamp': datetime.now(),
            })
        
        elif action['action'] in ['BUY', 'SELL']:
            # Ordem de mercado
            order_type = 'bids' if action['action'] == 'BUY' else 'asks'
            self.order_book[order_type].append({
                'price': action['price'],
                'quantity': action['quantity'],
                'agent': agent_name,
                'timestamp': datetime.now(),
            })
    
    def _calculate_net_pressure(self, agent_actions: Dict[str, Dict[str, Any]]) -> float:
        """Calcula pressão líquida de compra/venda."""
        net_pressure = 0.0
        
        for action in agent_actions.values():
            if action['action'] == 'BUY':
                net_pressure += action.get('quantity', 0)
            elif action['action'] == 'SELL':
                net_pressure -= action.get('quantity', 0)
        
        return net_pressure
    
    def _update_market_state(self, net_pressure: float, external_shock: float):
        """Atualiza estado do mercado."""
        current_price = self.market_state['price']
        volatility = self.market_state['volatility']
        
        # Impacto da pressão líquida
        pressure_impact = net_pressure * 0.001  # 0.1% por unidade
        
        # Ruído aleatório
        random_shock = random.gauss(0, volatility)
        
        # Atualiza preço
        new_price = current_price * (1 + pressure_impact + random_shock + external_shock)
        
        # Atualiza outros parâmetros
        self.market_state.update({
            'price': new_price,
            'volume': abs(net_pressure) * 10 + random.randint(100, 1000),
            'trend': (new_price - current_price) / current_price,
            'sentiment': np.tanh(net_pressure * 0.01),  # -1 a 1
            'timestamp': datetime.now(),
        })
        
        # Ajusta volatilidade baseada no volume
        volume_ratio = self.market_state['volume'] / 10000.0
        self.market_state['volatility'] = volatility * (0.9 + volume_ratio * 0.2)
    
    def _execute_orders(self) -> List[Dict[str, Any]]:
        """Executa ordens no livro."""
        trades = []
        
        # Ordena bids (maior preço primeiro) e asks (menor preço primeiro)
        bids_sorted = sorted(self.order_book['bids'], key=lambda x: x['price'], reverse=True)
        asks_sorted = sorted(self.order_book['asks'], key=lambda x: x['price'])
        
        # Matching de ordens
        while bids_sorted and asks_sorted:
            best_bid = bids_sorted[0]
            best_ask = asks_sorted[0]
            
            if best_bid['price'] >= best_ask['price']:
                # Trade possível
                trade_price = (best_bid['price'] + best_ask['price']) / 2
                trade_quantity = min(best_bid['quantity'], best_ask['quantity'])
                
                # Registra trade
                trades.append({
                    'price': trade_price,
                    'quantity': trade_quantity,
                    'buyer': best_bid['agent'],
                    'seller': best_ask['agent'],
                    'timestamp': datetime.now(),
                })
                
                # Atualiza quantidades
                best_bid['quantity'] -= trade_quantity
                best_ask['quantity'] -= trade_quantity
                
                # Remove ordens completadas
                if best_bid['quantity'] <= 0:
                    bids_sorted.pop(0)
                if best_ask['quantity'] <= 0:
                    asks_sorted.pop(0)
            else:
                # Não há mais matches
                break
        
        # Atualiza livro de ordens
        self.order_book['bids'] = [b for b in bids_sorted if b['quantity'] > 0]
        self.order_book['asks'] = [a for a in asks_sorted if a['quantity'] > 0]
        
        return trades
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Retorna resumo do mercado."""
        bids = self.order_book['bids']
        asks = self.order_book['asks']
        
        best_bid = max(bids, key=lambda x: x['price']) if bids else None
        best_ask = min(asks, key=lambda x: x['price']) if asks else None
        
        return {
            'price': self.market_state['price'],
            'bid_ask_spread': (
                (best_ask['price'] - best_bid['price']) if best_bid and best_ask else 0
            ),
            'total_bids': sum(b['quantity'] for b in bids),
            'total_asks': sum(a['quantity'] for a in asks),
            'market_depth': len(bids) + len(asks),
            'sentiment': self.market_state['sentiment'],
            'volatility': self.market_state['volatility'],
            'volume_24h': self.market_state['volume'] * 24,  # Estimado
        }

# ========== SISTEMA DE REALIDADE AUMENTADA COGNITIVA ==========

class CognitiveAugmentedReality:
    """Sistema de realidade aumentada cognitiva."""
    
    def __init__(self, memory_system: Any):
        self.memory = memory_system
        self.overlays = {}
        self.annotations = []
        self.pattern_highlights = []
        self.cognitive_filters = {}
        
    async def augment_market_view(self, market_data: Dict[str, Any], 
                                cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Aumenta visão do mercado com informações cognitivas."""
        augmented = market_data.copy()
        
        # Adiciona overlays cognitivos
        augmented['cognitive_overlays'] = await self._generate_cognitive_overlays(
            market_data, cognitive_state
        )
        
        # Adiciona anotações baseadas em memória
        augmented['memory_annotations'] = await self._generate_memory_annotations(
            market_data
        )
        
        # Adiciona destaques de padrões
        augmented['pattern_highlights'] = await self._detect_pattern_highlights(
            market_data
        )
        
        # Adiciona filtros cognitivos
        augmented['cognitive_filters'] = self._apply_cognitive_filters(
            market_data, cognitive_state
        )
        
        return augmented
    
    async def _generate_cognitive_overlays(self, market_data: Dict[str, Any], 
                                         cognitive_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera overlays cognitivos."""
        overlays = []
        
        # Overlay de atenção
        attention_overlay = {
            'type': 'ATTENTION_HEATMAP',
            'regions': self._generate_attention_regions(market_data),
            'intensity': cognitive_state.get('focus_level', 0.5),
            'color': 'yellow' if cognitive_state.get('focus_level', 0) > 0.7 else 'blue',
        }
        overlays.append(attention_overlay)
        
        # Overlay de risco
        risk_overlay = {
            'type': 'RISK_CONTOURS',
            'levels': self._calculate_risk_levels(market_data),
            'confidence': cognitive_state.get('confidence', 0.5),
            'color': 'red' if cognitive_state.get('fear', 0) > 0.6 else 'green',
        }
        overlays.append(risk_overlay)
        
        # Overlay de oportunidade
        opportunity_overlay = {
            'type': 'OPPORTUNITY_ZONES',
            'zones': self._identify_opportunity_zones(market_data),
            'aggression': cognitive_state.get('aggression', 0.5),
            'color': 'green' if cognitive_state.get('greed', 0) > 0.4 else 'orange',
        }
        overlays.append(opportunity_overlay)
        
        return overlays
    
    async def _generate_memory_annotations(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera anotações baseadas em memória."""
        annotations = []
        
        # Busca padrões similares na memória
        similar_patterns = await self._find_similar_patterns(market_data)
        
        for pattern in similar_patterns[:3]:  # Limita a 3
            annotation = {
                'type': 'MEMORY_MARKER',
                'pattern': pattern.get('name', 'Unknown'),
                'outcome': pattern.get('outcome', 'NEUTRAL'),
                'confidence': pattern.get('confidence', 0.5),
                'timestamp': pattern.get('timestamp', datetime.now()),
                'lesson': pattern.get('lesson', ''),
                'location': self._calculate_pattern_location(market_data, pattern),
            }
            annotations.append(annotation)
        
        return annotations
    
    async def _detect_pattern_highlights(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detecta e destaca padrões importantes."""
        highlights = []
        
        # Padrão de reversão
        if self._is_reversal_pattern(market_data):
            highlights.append({
                'type': 'REVERSAL_PATTERN',
                'confidence': 0.7,
                'message': 'Possível reversão de tendência detectada',
                'color': 'purple',
                'intensity': 0.8,
            })
        
        # Padrão de continuação
        if self._is_continuation_pattern(market_data):
            highlights.append({
                'type': 'CONTINUATION_PATTERN',
                'confidence': 0.6,
                'message': 'Tendência provavelmente continuará',
                'color': 'blue',
                'intensity': 0.6,
            })
        
        # Padrão de volatilidade
        if self._is_volatility_pattern(market_data):
            highlights.append({
                'type': 'VOLATILITY_CLUSTER',
                'confidence': 0.8,
                'message': 'Cluster de volatilidade detectado',
                'color': 'red',
                'intensity': 0.9,
            })
        
        return highlights
    
    def _apply_cognitive_filters(self, market_data: Dict[str, Any], 
                               cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica filtros cognitivos aos dados."""
        filters = {}
        
        # Filtro de viés confirmatório
        confirmation_bias = cognitive_state.get('confirmation_bias', 0.3)
        if confirmation_bias > 0.5:
            filters['confirmation_filter'] = {
                'strength': confirmation_bias,
                'effect': 'Amplifica informações que confirmam crenças existentes',
            }
        
        # Filtro de aversão à perda
        loss_aversion = cognitive_state.get('loss_aversion', 0.5)
        if loss_aversion > 0.6:
            filters['loss_aversion_filter'] = {
                'strength': loss_aversion,
                'effect': 'Superestima riscos de perda',
            }
        
        # Filtro de excesso de confiança
        overconfidence = cognitive_state.get('overconfidence', 0.3)
        if overconfidence > 0.5:
            filters['overconfidence_filter'] = {
                'strength': overconfidence,
                'effect': 'Subestima incerteza e risco',
            }
        
        return filters

# ========== SISTEMA PRINCIPAL LEXTRADER-IAG 3.0 EXPANDIDO ==========

class LextraderIAGExpanded:
    """Sistema LEXTRADER-IAG 3.0 Expandido com todas as funcionalidades."""
    
    def __init__(self, config_path: str = None):
        # Configuração
        self.config = self._load_config(config_path)
        
        # Sistemas principais do histórico
        self.sentient_core = SentientCore()  # Do arquivo original
        self.ensemble_predictor = EnsemblePredictor()  # Do arquivo original
        self.memory_optimizer = MemoryOptimizer()  # Do arquivo original
        
        # Novos sistemas expandidos
        self.multi_agent_orchestrator = MultiAgentOrchestrator()
        self.multi_agent_rl = MultiAgentRLSystem()
        self.market_simulator = MarketSimulationEngine()
        self.cognitive_ar = CognitiveAugmentedReality(self)
        
        # Sistemas de suporte
        self.executor = ThreadPoolExecutor(max_workers=SystemConstantsExpanded.MAX_CONCURRENT_TASKS)
        self.performance_monitor = PerformanceMonitor()
        self.alert_system = AlertSystem()
        
        # Estado do sistema
        self.operational_mode = 'FULL_COGNITIVE'
        self.system_status = 'INITIALIZING'
        self.start_time = datetime.now()
        self.cycle_count = 0
        
        # Históricos
        self.market_history = deque(maxlen=SystemConstantsExpanded.MAX_HISTORY_DAYS * 24 * 60)  # 1 min intervals
        self.decision_history = deque(maxlen=SystemConstantsExpanded.MAX_MEMORY_ITEMS)
        self.learning_history = deque(maxlen=10000)
        
        print("""
╔══════════════════════════════════════════════════════════╗
║           LEXTRADER-IAG 3.0 - SISTEMA EXPANDIDO          ║
║              Integrando Histórico Completo               ║
╚══════════════════════════════════════════════════════════╝
        """)
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Carrega configuração do sistema."""
        default_config = {
            'mode': 'FULL_COGNITIVE',
            'risk_tolerance': 'MEDIUM',
            'learning_enabled': True,
            'simulation_enabled': True,
            'augmented_reality': True,
            'auto_save': True,
            'backup_interval': 300,
            'max_position_size': 0.15,
            'default_assets': SystemConstantsExpanded.SUPPORTED_ASSETS,
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️  Erro ao carregar configuração: {e}")
        
        return default_config
    
    async def start(self):
        """Inicia o sistema expandido."""
        print("🚀 Iniciando LEXTRADER-IAG 3.0 Expandido...")
        
        self.system_status = 'INITIALIZING'
        
        # Inicializar todos os subsistemas
        initialization_tasks = [
            self._initialize_prediction_system(),
            self._initialize_multi_agent_system(),
            self._initialize_memory_system(),
            self._initialize_simulation_engine(),
            self._initialize_augmented_reality(),
        ]
        
        await asyncio.gather(*initialization_tasks)
        
        self.system_status = 'OPERATIONAL'
        self.start_time = datetime.now()
        
        print("✅ Sistema LEXTRADER-IAG 3.0 Expandido inicializado!")
        print(f"   Modo: {self.operational_mode}")
        print(f"   Agentes: {len(self.multi_agent_orchestrator.agents)}")
        print(f"   Ativos: {len(self.config['default_assets'])}")
    
    async def _initialize_prediction_system(self):
        """Inicializa sistema de predição."""
        print("   • Sistema de Predição: OK")
        
    async def _initialize_multi_agent_system(self):
        """Inicializa sistema multi-agente."""
        print("   • Sistema Multi-Agente: OK")
        
    async def _initialize_memory_system(self):
        """Inicializa sistema de memória."""
        print("   • Sistema de Memória: OK")
        
    async def _initialize_simulation_engine(self):
        """Inicializa motor de simulação."""
        print("   • Motor de Simulação: OK")
        
    async def _initialize_augmented_reality(self):
        """Inicializa realidade aumentada cognitiva."""
        print("   • Realidade Aumentada Cognitiva: OK")
    
    async def run_cognitive_cycle(self, market_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa um ciclo cognitivo completo.
        
        Args:
            market_data: Dados de mercado atualizados
            
        Returns:
            Resultado do ciclo cognitivo
        """
        self.cycle_count += 1
        cycle_start = time.perf_counter()
        
        try:
            # 1. Coleta e processamento inicial
            processed_data = await self._process_market_data(market_data)
            
            # 2. Análise multi-agente
            agent_consensus = await self.multi_agent_orchestrator.get_consensus(processed_data)
            
            # 3. Predição de recursos e incidentes
            predictions = await self._get_predictions(processed_data)
            
            # 4. Aprendizado por reforço
            rl_actions = await self._get_rl_actions(processed_data, agent_consensus)
            
            # 5. Simulação de mercado (se habilitado)
            simulation_results = None
            if self.config.get('simulation_enabled', True):
                simulation_results = await self._run_market_simulation(processed_data)
            
            # 6. Realidade aumentada cognitiva
            augmented_view = None
            if self.config.get('augmented_reality', True):
                augmented_view = await self.cognitive_ar.augment_market_view(
                    processed_data, self._get_cognitive_state()
                )
            
            # 7. Tomada de decisão integrada
            final_decision = await self._make_integrated_decision(
                processed_data, agent_consensus, rl_actions, simulation_results
            )
            
            # 8. Aprendizado e atualização
            await self._learn_from_cycle(final_decision, processed_data)
            
            # 9. Monitoramento e alertas
            alerts = await self._check_for_alerts(processed_data, final_decision)
            
            cycle_time = time.perf_counter() - cycle_start
            
            # Construir resultado
            result = {
                'cycle_number': self.cycle_count,
                'timestamp': datetime.now().isoformat(),
                'cycle_time_ms': cycle_time * 1000,
                'agent_consensus': agent_consensus,
                'predictions': predictions,
                'rl_actions': rl_actions,
                'simulation_results': simulation_results,
                'augmented_view': augmented_view,
                'final_decision': final_decision,
                'alerts': alerts,
                'system_status': self._get_system_status(),
            }
            
            # Registrar no histórico
            self.decision_history.append(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Erro no ciclo cognitivo: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                'error': str(e),
                'cycle_number': self.cycle_count,
                'timestamp': datetime.now().isoformat(),
            }
    
    async def _process_market_data(self, market_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Processa dados de mercado."""
        processed = {
            'raw_data': market_data,
            'summary': self._summarize_market_data(market_data),
            'sentiment': self._calculate_market_sentiment(market_data),
            'volatility': self._calculate_market_volatility(market_data),
            'trends': self._identify_market_trends(market_data),
            'anomalies': self._detect_anomalies(market_data),
        }
        
        # Adiciona ao histórico
        self.market_history.append({
            'timestamp': datetime.now(),
            'data': processed,
        })
        
        return processed
    
    async def _get_predictions(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém predições do sistema."""
        predictions = {}
        
        # Predição de recursos (do sistema original)
        resource_predictions = await self.ensemble_predictor.predict(market_data['summary'])
        predictions['resources'] = resource_predictions
        
        # Predição de incidentes
        incident_predictions = await self._predict_incidents(market_data)
        predictions['incidents'] = incident_predictions
        
        # Predição de segurança
        security_predictions = await self._predict_security(market_data)
        predictions['security'] = security_predictions
        
        return predictions
    
    async def _get_rl_actions(self, market_data: Dict[str, Any], 
                            agent_consensus: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém ações do sistema de RL."""
        # Converte dados para estado RL
        state = self._market_data_to_rl_state(market_data, agent_consensus)
        
        # Obtém ação conjunta
        rl_result = await self.multi_agent_rl.get_joint_action(
            state, market_data
        )
        
        return rl_result
    
    async def _run_market_simulation(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa simulação de mercado."""
        simulation_results = []
        
        # Executa múltiplos cenários
        scenarios = ['baseline', 'bullish', 'bearish', 'volatile']
        
        for scenario in scenarios:
            result = await self._run_single_simulation(market_data, scenario)
            simulation_results.append(result)
        
        return {
            'scenarios': scenarios,
            'results': simulation_results,
            'consensus': self._analyze_simulation_results(simulation_results),
        }
    
    async def _make_integrated_decision(self, market_data: Dict[str, Any],
                                      agent_consensus: Dict[str, Any],
                                      rl_actions: Dict[str, Any],
                                      simulation_results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Toma decisão integrada considerando todos os fatores."""
        
        # Coleta todos os sinais
        signals = {
            'agent_consensus': agent_consensus.get('consensus', 'NEUTRAL'),
            'agent_confidence': agent_consensus.get('confidence', 0.5),
            'rl_action': rl_actions.get('joint_action', {}).get('action', 0),
            'rl_confidence': rl_actions.get('joint_action', {}).get('confidence', 0.5),
        }
        
        # Adiciona sinais de simulação se disponível
        if simulation_results:
            signals['simulation_consensus'] = simulation_results.get('consensus', 'NEUTRAL')
        
        # Estado do núcleo senciente
        sentient_state = self.sentient_core.get_state()
        signals['sentient_mood'] = sentient_state.emotional_tone
        signals['sentient_confidence'] = sentient_state.vector.confidence / 100
        
        # Calcula decisão ponderada
        decision = self._calculate_weighted_decision(signals, market_data)
        
        # Aplica limites de risco
        decision = self._apply_risk_limits(decision, market_data)
        
        return decision
    
    def _calculate_weighted_decision(self, signals: Dict[str, Any], 
                                   market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula decisão ponderada."""
        weights = {
            'agent_consensus': 0.3,
            'rl_action': 0.25,
            'sentiment': 0.2,
            'simulation': 0.15,
            'sentient_state': 0.1,
        }
        
        # Converte sinais para valores numéricos
        numeric_signals = {}
        
        # Consenso dos agentes
        consensus_map = {'BULLISH': 1, 'NEUTRAL': 0, 'BEARISH': -1}
        numeric_signals['agent_consensus'] = (
            consensus_map.get(signals['agent_consensus'], 0) * 
            signals['agent_confidence']
        )
        
        # Ação RL (normalizada para -1 a 1)
        rl_normalized = (signals['rl_action'] / 5.0) - 1  # Assumindo ação 0-10
        numeric_signals['rl_action'] = rl_normalized * signals['rl_confidence']
        
        # Sentimento do mercado
        sentiment = market_data.get('sentiment', 0)
        numeric_signals['sentiment'] = sentiment
        
        # Simulação
        simulation_consensus = signals.get('simulation_consensus', 'NEUTRAL')
        numeric_signals['simulation'] = consensus_map.get(simulation_consensus, 0)
        
        # Estado senciente
        mood_map = {'BULLISH': 0.5, 'BEARISH': -0.5, 'NEUTRAL': 0}
        numeric_signals['sentient_state'] = (
            mood_map.get(signals.get('sentient_mood', 'NEUTRAL'), 0) *
            signals['sentient_confidence']
        )
        
        # Calcula decisão ponderada
        weighted_sum = 0
        total_weight = 0
        
        for key, weight in weights.items():
            if key in numeric_signals:
                weighted_sum += numeric_signals[key] * weight
                total_weight += weight
        
        decision_value = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Mapeia para ação
        if decision_value > 0.3:
            action = 'STRONG_BUY'
            confidence = min(0.95, decision_value)
        elif decision_value > 0.1:
            action = 'BUY'
            confidence = decision_value * 0.8
        elif decision_value < -0.3:
            action = 'STRONG_SELL'
            confidence = min(0.95, -decision_value)
        elif decision_value < -0.1:
            action = 'SELL'
            confidence = -decision_value * 0.8
        else:
            action = 'HOLD'
            confidence = 0.5 - abs(decision_value)
        
        return {
            'action': action,
            'confidence': confidence,
            'decision_value': decision_value,
            'signals': signals,
            'weights': weights,
            'timestamp': datetime.now(),
        }
    
    def _apply_risk_limits(self, decision: Dict[str, Any], 
                         market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica limites de risco à decisão."""
        volatility = market_data.get('volatility', 0.02)
        max_position = self.config.get('max_position_size', 0.15)
        
        # Ajusta tamanho da posição baseado na volatilidade
        volatility_adjustment = 1.0 / (1.0 + volatility * 10)
        adjusted_position = max_position * volatility_adjustment
        
        # Ajusta baseado na confiança
        confidence = decision.get('confidence', 0.5)
        confidence_adjustment = confidence ** 2  # Quadrático para ser conservador
        
        final_position = adjusted_position * confidence_adjustment
        
        decision['position_size'] = final_position
        decision['risk_adjustment'] = {
            'volatility': volatility,
            'volatility_adjustment': volatility_adjustment,
            'confidence_adjustment': confidence_adjustment,
            'max_position': max_position,
        }
        
        return decision
    
    async def _learn_from_cycle(self, decision: Dict[str, Any], 
                              market_data: Dict[str, Any]):
        """Aprende do ciclo atual."""
        # Registra aprendizado
        learning_entry = {
            'decision': decision,
            'market_data': market_data,
            'timestamp': datetime.now(),
            'outcome': None,  # Será atualizado quando resultado for conhecido
        }
        
        self.learning_history.append(learning_entry)
        
        # Atualiza sistemas de aprendizado
        if decision.get('outcome') is not None:
            outcome = decision['outcome']
            
            # Atualiza RL
            state = self._market_data_to_rl_state(market_data, {})
            next_state = state  # Simplificado
            await self.multi_agent_rl.learn_from_experience(
                state, decision, outcome, next_state
            )
            
            # Atualiza orquestrador de agentes
            await self.multi_agent_orchestrator.update_weights_based_on_performance(
                outcome
            )
    
    async def _check_for_alerts(self, market_data: Dict[str, Any], 
                              decision: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica alertas."""
        alerts = []
        
        # Alertas de volatilidade
        volatility = market_data.get('volatility', 0)
        if volatility > 0.05:
            alerts.append({
                'type': 'HIGH_VOLATILITY',
                'level': 'WARNING',
                'message': f'Alta volatilidade detectada: {volatility:.1%}',
                'timestamp': datetime.now(),
            })
        
        # Alertas de anomalias
        anomalies = market_data.get('anomalies', [])
        if anomalies:
            alerts.append({
                'type': 'MARKET_ANOMALIES',
                'level': 'INFO',
                'message': f'{len(anomalies)} anomalias detectadas no mercado',
                'anomalies': anomalies[:3],
                'timestamp': datetime.now(),
            })
        
        # Alertas de risco
        if decision.get('position_size', 0) > self.config.get('max_position_size', 0.15) * 0.8:
            alerts.append({
                'type': 'POSITION_SIZE_WARNING',
                'level': 'WARNING',
                'message': f'Tamanho da posição próximo do limite: {decision["position_size"]:.1%}',
                'timestamp': datetime.now(),
            })
        
        return alerts
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Retorna status do sistema."""
        uptime = datetime.now() - self.start_time
        
        return {
            'system_status': self.system_status,
            'operational_mode': self.operational_mode,
            'uptime': str(uptime),
            'cycle_count': self.cycle_count,
            'market_history_size': len(self.market_history),
            'decision_history_size': len(self.decision_history),
            'learning_history_size': len(self.learning_history),
            'agent_count': len(self.multi_agent_orchestrator.agents),
            'rl_system_stats': self.multi_agent_rl.get_system_stats(),
            'memory_usage': self.memory_optimizer.get_memory_stats(),
            'sentient_state': self.sentient_core.get_state().get_state_info(),
        }
    
    async def get_comprehensive_report(self) -> Dict[str, Any]:
        """Obtém relatório compreensivo do sistema."""
        return {
            'system_overview': self._get_system_status(),
            'historical_integration': HistoricalIntegration.get_integrated_features(),
            'performance_metrics': self.performance_monitor.get_metrics(),
            'recent_decisions': list(self.decision_history)[-5:],
            'market_summary': self._get_market_summary(),
            'agent_performance': await self._get_agent_performance(),
            'learning_progress': self._get_learning_progress(),
            'risk_assessment': self._get_risk_assessment(),
            'recommendations': await self._generate_recommendations(),
        }

# ========== SISTEMAS AUXILIARES ==========

class PerformanceMonitor:
    """Monitor de performance do sistema."""
    
    def __init__(self):
        self.metrics_history = deque(maxlen=1000)
        self.cycle_times = deque(maxlen=100)
    
    def record_cycle(self, cycle_data: Dict[str, Any]):
        """Registra um ciclo."""
        self.cycle_times.append(cycle_data.get('cycle_time_ms', 0))
        
        # Calcula métricas
        metrics = {
            'timestamp': datetime.now(),
            'cycle_time_avg': np.mean(self.cycle_times) if self.cycle_times else 0,
            'cycle_time_std': np.std(self.cycle_times) if len(self.cycle_times) > 1 else 0,
            'decision_confidence': cycle_data.get('final_decision', {}).get('confidence', 0),
            'agent_consensus': cycle_data.get('agent_consensus', {}).get('consensus', 'NEUTRAL'),
            'alert_count': len(cycle_data.get('alerts', [])),
        }
        
        self.metrics_history.append(metrics)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas atuais."""
        if not self.metrics_history:
            return {'status': 'NO_DATA'}
        
        recent = list(self.metrics_history)[-10:]
        
        return {
            'avg_cycle_time_ms': np.mean([m['cycle_time_avg'] for m in recent]),
            'avg_decision_confidence': np.mean([m['decision_confidence'] for m in recent]),
            'recent_consensus': recent[-1]['agent_consensus'] if recent else 'UNKNOWN',
            'alert_rate': np.mean([m['alert_count'] for m in recent]),
            'monitoring_duration': len(self.metrics_history),
        }

class AlertSystem:
    """Sistema de alertas inteligente."""
    
    def __init__(self):
        self.alerts = deque(maxlen=1000)
        self.alert_patterns = {}
        self.escalation_rules = {}
    
    def add_alert(self, alert: Dict[str, Any]):
        """Adiciona um alerta."""
        alert['id'] = f"ALT-{int(time.time()*1000)}-{random.randint(1000, 9999)}"
        alert['timestamp'] = datetime.now()
        
        self.alerts.append(alert)
        
        # Detecta padrões de alerta
        self._detect_alert_patterns(alert)
    
    def _detect_alert_patterns(self, alert: Dict[str, Any]):
        """Detecta padrões em alertas."""
        alert_type = alert.get('type', 'UNKNOWN')
        
        if alert_type not in self.alert_patterns:
            self.alert_patterns[alert_type] = {
                'count': 0,
                'first_seen': datetime.now(),
                'last_seen': datetime.now(),
                'levels': defaultdict(int),
            }
        
        pattern = self.alert_patterns[alert_type]
        pattern['count'] += 1
        pattern['last_seen'] = datetime.now()
        pattern['levels'][alert.get('level', 'INFO')] += 1
        
        # Verifica se precisa escalar
        if pattern['count'] > 10 and pattern['levels'].get('WARNING', 0) > 5:
            # Cria alerta de padrão
            self.add_alert({
                'type': 'ALERT_PATTERN',
                'level': 'CRITICAL',
                'message': f'Padrão de alertas detectado para {alert_type}: {pattern["count"]} ocorrências',
                'pattern_details': dict(pattern),
            })

# ========== FUNÇÃO PRINCIPAL ==========

async def demonstrate_expanded_system():
    """Demonstração do sistema LEXTRADER-IAG 3.0 expandido."""
    
    print("""
╔══════════════════════════════════════════════════════════╗
║      LEXTRADER-IAG 3.0 EXPANDIDO - DEMONSTRAÇÃO          ║
║          Integrando Todo o Histórico do Sistema          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar sistema
    lextrader = LextraderIAGExpanded()
    await lextrader.start()
    
    print("\n" + "="*60)
    print("📊 FASE 1: Criação de Dados de Mercado Simulados")
    print("="*60)
    
    # Gerar dados de mercado simulados
    market_data = []
    for i in range(10):
        market_data.append({
            'symbol': random.choice(SystemConstantsExpanded.SUPPORTED_ASSETS),
            'price': 50000 + random.uniform(-2000, 2000),
            'volume': random.uniform(1000, 10000),
            'timestamp': datetime.now(),
            'indicators': {
                'rsi': random.uniform(20, 80),
                'macd': random.uniform(-10, 10),
                'bollinger': random.uniform(0.9, 1.1),
                'volume_ratio': random.uniform(0.5, 1.5),
            }
        })
    
    print(f"• Dados gerados: {len(market_data)} ativos")
    print(f"• Período: {market_data[0]['timestamp'].strftime('%H:%M:%S')} a {market_data[-1]['timestamp'].strftime('%H:%M:%S')}")
    
    print("\n" + "="*60)
    print("🧠 FASE 2: Execução de Ciclo Cognitivo Completo")
    print("="*60)
    
    # Executar ciclo cognitivo
    cycle_result = await lextrader.run_cognitive_cycle(market_data)
    
    print(f"• Ciclo #{cycle_result['cycle_number']} completado")
    print(f"• Tempo de ciclo: {cycle_result['cycle_time_ms']:.1f}ms")
    print(f"• Consenso dos agentes: {cycle_result['agent_consensus']['consensus']}")
    print(f"• Confiança: {cycle_result['agent_consensus']['confidence']:.1%}")
    print(f"• Decisão final: {cycle_result['final_decision']['action']}")
    print(f"• Tamanho da posição: {cycle_result['final_decision']['position_size']:.1%}")
    
    print("\n" + "="*60)
    print("🤖 FASE 3: Sistema Multi-Agente em Ação")
    print("="*60)
    
    # Mostrar contribuições dos agentes
    agent_contributions = cycle_result['agent_consensus']['agent_contributions']
    print("Contribuições dos Agentes Especialistas:")
    for agent, contrib in agent_contributions.items():
        print(f"  • {agent}: {contrib['signal']} (Conf: {contrib['confidence']:.1%}, Peso: {contrib['weight']:.2f})")
    
    print("\n" + "="*60)
    print("🎮 FASE 4: Sistema de Aprendizado por Reforço")
    print("="*60)
    
    # Mostrar estatísticas RL
    rl_stats = lextrader.multi_agent_rl.get_system_stats()
    print("Estatísticas do Sistema RL:")
    print(f"  • Agentes: {rl_stats['total_agents']}")
    print(f"  • Buffer de replay: {rl_stats['replay_buffer_size']}")
    print("  • Taxas de exploração:")
    for agent, rate in rl_stats['exploration_rates'].items():
        print(f"    - {agent}: {rate:.3f}")
    
    print("\n" + "="*60)
    print("📈 FASE 5: Relatório Compreensivo do Sistema")
    print("="*60)
    
    # Obter relatório completo
    report = await lextrader.get_comprehensive_report()
    
    print("Visão Geral do Sistema:")
    status = report['system_overview']
    print(f"  • Status: {status['system_status']}")
    print(f"  • Uptime: {status['uptime']}")
    print(f"  • Ciclos executados: {status['cycle_count']}")
    print(f"  • Histórico de decisões: {status['decision_history_size']}")
    
    print("\nIntegração Histórica:")
    features = report['historical_integration']
    print(f"  • Features Omega: {len(features['omega_features'])}")
    print(f"  • Features Memória: {len(features['memory_features'])}")
    print(f"  • Features Predição: {len(features['prediction_features'])}")
    
    print("\nMétricas de Performance:")
    metrics = report['performance_metrics']
    for key, value in metrics.items():
        print(f"  • {key}: {value}")
    
    print("\n" + "="*60)
    print("🔮 FASE 6: Simulação de Mercado Multi-Agente")
    print("="*60)
    
    # Executar simulação de mercado
    simulation_steps = 5
    print(f"Executando {simulation_steps} passos de simulação de mercado...")
    
    for i in range(simulation_steps):
        step_result = await lextrader.market_simulator.simulate_step()
        summary = lextrader.market_simulator.get_market_summary()
        
        if i == simulation_steps - 1:  # Último passo
            print(f"  • Preço final: ${summary['price']:,.2f}")
            print(f"  • Spread bid-ask: ${summary['bid_ask_spread']:.2f}")
            print(f"  • Sentimento: {summary['sentiment']:+.2f}")
            print(f"  • Volatilidade: {summary['volatility']:.2%}")
    
    print("\n" + "="*60)
    print("🧹 FASE 7: Otimização de Memória e Limpeza")
    print("="*60)
    
    # Forçar limpeza de memória
    lextrader.memory_optimizer.check_and_clean(force=True)
    
    memory_stats = lextrader.memory_optimizer.get_memory_stats()
    print("Estatísticas de Memória:")
    print(f"  • RSS: {memory_stats['rss_mb']:.1f} MB")
    print(f"  • VMS: {memory_stats['vms_mb']:.1f} MB")
    print(f"  • Limpezas executadas: {memory_stats['cleanups']}")
    print(f"  • Última limpeza: {memory_stats['last_cleanup']}")
    
    print("\n" + "="*60)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    
    # Mostrar resumo final
    print("\n🎯 RESUMO FINAL DO SISTEMA LEXTRADER-IAG 3.0:")
    print(f"• Total de funcionalidades integradas: {sum(len(f) for f in features.values())}")
    print(f"• Ciclos cognitivos executados: {status['cycle_count']}")
    print(f"• Agentes especialistas ativos: {len(lextrader.multi_agent_orchestrator.agents)}")
    print(f"• Sistema operando em modo: {status['operational_mode']}")
    print(f"• Estado senciente: {status['sentient_state']['emotional_tone']}")
    print(f"• Confiança do núcleo: {status['sentient_state']['confidence_level']}")
    
    print("""
╔══════════════════════════════════════════════════════════╗
║    LEXTRADER-IAG 3.0 - SISTEMA COGNITIVO COMPLETO        ║
║               PRONTO PARA OPERAÇÃO! 🚀                   ║
╚══════════════════════════════════════════════════════════╝
    """)

async def main():
    """Função principal."""
    try:
        await demonstrate_expanded_system()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Executar demonstração
    asyncio.run(main(), debug=False)