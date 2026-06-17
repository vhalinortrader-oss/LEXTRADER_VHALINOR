import asyncio
import random
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor

# --- TIPOS & INTERFACES ---

class ConnectionStatus(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    ERROR = "ERROR"

class SystemStatus(Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"

class RecoveryResult(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"

class IssueType(Enum):
    CONNECTION_EXCHANGE = "conexao_corretora"
    SYSTEM_RESOURCES = "recursos_sistema"
    MEMORY_LEAK = "vazamento_memoria"
    CPU_OVERLOAD = "sobrecarga_cpu"
    NETWORK_LATENCY = "latencia_rede"
    API_LIMIT = "limite_api"
    UNKNOWN = "desconhecido"

@dataclass
class HealthStatus:
    """Status de saúde do sistema"""
    connection: ConnectionStatus = ConnectionStatus.DISCONNECTED
    memory_usage: float = 0.0  # 0-100%
    cpu_load: float = 0.0  # 0-100%
    last_check: datetime = field(default_factory=datetime.now)
    error_count: Dict[str, int] = field(default_factory=dict)
    status: SystemStatus = SystemStatus.HEALTHY
    network_latency: float = 0.0  # ms
    active_threads: int = 0
    uptime: float = 0.0  # segundos
    prediction_score: float = 0.0  # 0-1 probabilidade de falha
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo do status"""
        total_errors = sum(self.error_count.values())
        
        return {
            'status': self.status.value,
            'connection': self.connection.value,
            'cpu_load': f"{self.cpu_load:.1f}%",
            'memory_usage': f"{self.memory_usage:.1f}%",
            'network_latency': f"{self.network_latency:.1f}ms",
            'total_errors': total_errors,
            'last_check': self.last_check.strftime('%H:%M:%S'),
            'uptime': f"{self.uptime:.0f}s",
            'prediction_score': f"{self.prediction_score:.1%}"
        }

@dataclass
class RecoveryLog:
    """Log de recuperação"""
    id: str
    timestamp: datetime
    issue: str
    action: str
    result: RecoveryResult
    agi_intervention: bool = False
    details: Optional[Dict[str, Any]] = None
    recovery_time: Optional[float] = None  # segundos
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}
    
    def get_log_info(self) -> Dict[str, Any]:
        """Retorna informações do log"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'issue': self.issue,
            'action': self.action,
            'result': self.result.value,
            'agi_intervention': self.agi_intervention,
            'recovery_time': f"{self.recovery_time:.2f}s" if self.recovery_time else "N/A",
            'details': self.details
        }

# --- SIMULAÇÃO DAS DEPENDÊNCIAS ---

class SentimentVector:
    """Vetor de sentimentos (simulação)"""
    
    def __init__(self):
        self.joy = random.uniform(40, 80)
        self.fear = random.uniform(10, 40)
        self.greed = random.uniform(10, 30)
        self.confidence = random.uniform(60, 90)
        self.urgency = random.uniform(20, 60)
        self.stability = random.uniform(60, 90)
        self.aggression = random.uniform(10, 40)
        self.creativity = random.uniform(50, 90)
        self.timestamp = datetime.now()
    
    def update(self):
        """Atualiza sentimentos com variação aleatória"""
        for attr in ['confidence', 'stability', 'fear', 'urgency']:
            current = getattr(self, attr)
            change = random.uniform(-5, 5)
            setattr(self, attr, max(0.0, min(100.0, current + change)))
        self.timestamp = datetime.now()

class SentientCore:
    """Núcleo Senciente (simulação)"""
    
    def __init__(self):
        self.vector = SentimentVector()
        self.thoughts = []
        self.reality_perceptions = []
        self.start_time = datetime.now()
    
    def get_vector(self) -> SentimentVector:
        """Retorna vetor de sentimentos"""
        self.vector.update()  # Atualiza com variação aleatória
        return self.vector
    
    def add_thought(self, thought: str):
        """Adiciona pensamento"""
        thought_record = {
            'timestamp': datetime.now(),
            'thought': thought,
            'vector': {
                'confidence': self.vector.confidence,
                'stability': self.vector.stability,
                'fear': self.vector.fear
            }
        }
        
        self.thoughts.append(thought_record)
        print(f"💭 {thought}")
        
        # Mantém histórico limitado
        if len(self.thoughts) > 100:
            self.thoughts = self.thoughts[-100:]
    
    def perceive_reality(self, volatility: float, outcome: float):
        """Percepção da realidade"""
        perception = {
            'timestamp': datetime.now(),
            'volatility': volatility,
            'outcome': outcome,
            'system_impact': abs(outcome) * volatility
        }
        
        self.reality_perceptions.append(perception)
        
        # Ajusta sentimentos baseado no resultado
        if outcome > 0:
            # Sucesso aumenta confiança
            self.vector.confidence = min(100.0, self.vector.confidence + 2.0)
            self.vector.stability = min(100.0, self.vector.stability + 1.0)
        else:
            # Falha aumenta medo e diminui confiança
            self.vector.fear = min(100.0, self.vector.fear + 3.0)
            self.vector.confidence = max(0.0, self.vector.confidence - 2.0)
            self.vector.stability = max(0.0, self.vector.stability - 1.5)
        
        print(f"🌍 Percepção: volatilidade={volatility:.1f}, resultado={outcome:+.1f}")
        
        # Mantém histórico limitado
        if len(self.reality_perceptions) > 50:
            self.reality_perceptions = self.reality_perceptions[-50:]

class QuantumNeuralNetwork:
    """Rede Neural Quântica (simulação)"""
    
    def __init__(self):
        self.initialized = False
        self.prediction_history = []
        self.training_data = []
    
    async def initialize(self):
        """Inicializa a rede"""
        await asyncio.sleep(0.3)  # Simula inicialização
        self.initialized = True
        print("⚛️ Rede Neural Preditiva inicializada")
    
    async def predict(self, metrics: List[float]) -> Dict[str, Any]:
        """
        Prediz probabilidade de falha
        
        Args:
            metrics: [cpu_load, mem_usage, error_rate] normalizados 0-1
            
        Returns:
            Dict com predição e confiança
        """
        if not self.initialized:
            await self.initialize()
        
        # Valida entrada
        if len(metrics) < 3:
            metrics = metrics + [0.0] * (3 - len(metrics))
        
        # Normaliza para 0-1
        metrics = [max(0.0, min(1.0, m)) for m in metrics[:3]]
        
        # Simulação de predição neural
        # Pesos: CPU: 0.4, Memória: 0.3, Erros: 0.3
        weights = [0.4, 0.3, 0.3]
        weighted_sum = sum(m * w for m, w in zip(metrics, weights))
        
        # Adiciona ruído quântico
        quantum_noise = random.uniform(-0.1, 0.1)
        prediction = max(0.0, min(1.0, weighted_sum + quantum_noise))
        
        # Calcula confiança baseada na coerência
        feature_std = sum(abs(m - 0.5) for m in metrics) / len(metrics)
        coherence = 1.0 - (feature_std * 0.8)
        confidence = 0.6 + (coherence * 0.4)
        
        result = {
            'prediction': prediction,
            'confidence': confidence,
            'features': {
                'cpu_load': metrics[0],
                'memory_usage': metrics[1],
                'error_rate': metrics[2]
            },
            'quantum_state': 'SUPERPOSITION_ANALYZED'
        }
        
        # Registra no histórico
        self.prediction_history.append({
            'timestamp': datetime.now(),
            'result': result,
            'metrics': metrics
        })
        
        if len(self.prediction_history) > 1000:
            self.prediction_history = self.prediction_history[-1000:]
        
        return result
    
    def train(self, metrics: List[float], target: float):
        """Treina a rede com novos dados"""
        if len(metrics) < 3:
            return
        
        training_point = {
            'timestamp': datetime.now(),
            'metrics': metrics[:3],
            'target': target
        }
        
        self.training_data.append(training_point)
        
        # Limita dados de treinamento
        if len(self.training_data) > 5000:
            self.training_data = self.training_data[-5000:]
        
        print(f"🎓 Rede treinada: target={target:.2f}, amostras={len(self.training_data)}")

# --- REDE NEURAL LEVE PARA PREVISÃO DE FALHAS ---

class PredictiveMaintenanceNet:
    """Rede Neural leve para previsão de falhas de sistema"""
    
    def __init__(self):
        self.net = QuantumNeuralNetwork()
        self.failure_history = []
        self.initialized = False
    
    async def initialize(self):
        """Inicializa a rede"""
        await self.net.initialize()
        self.initialized = True
        print("🔮 Sistema Preditivo de Manutenção inicializado")
    
    async def predict_failure(self, metrics: List[float]) -> float:
        """
        Prediz probabilidade de falha
        
        Args:
            metrics: [cpu_load, mem_usage, error_rate] normalizados 0-1
            
        Returns:
            float: Probabilidade de falha 0-1
        """
        if not self.initialized:
            await self.initialize()
        
        result = await self.net.predict(metrics)
        prediction = result['prediction']
        
        # Registra no histórico
        self.failure_history.append({
            'timestamp': datetime.now(),
            'prediction': prediction,
            'metrics': metrics,
            'confidence': result['confidence']
        })
        
        if len(self.failure_history) > 500:
            self.failure_history = self.failure_history[-500:]
        
        return prediction
    
    def get_prediction_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de predição"""
        if not self.failure_history:
            return {'status': 'No predictions yet'}
        
        recent = self.failure_history[-100:] if len(self.failure_history) > 100 else self.failure_history
        avg_prediction = sum(p['prediction'] for p in recent) / len(recent)
        avg_confidence = sum(p['confidence'] for p in recent) / len(recent)
        
        high_risk = [p for p in recent if p['prediction'] > 0.7]
        low_risk = [p for p in recent if p['prediction'] < 0.3]
        
        return {
            'total_predictions': len(self.failure_history),
            'recent_predictions': len(recent),
            'avg_prediction': f"{avg_prediction:.1%}",
            'avg_confidence': f"{avg_confidence:.1%}",
            'high_risk_count': len(high_risk),
            'low_risk_count': len(low_risk),
            'alarm_rate': f"{len(high_risk) / len(recent):.1%}" if recent else "0%"
        }

# --- SERVIÇO DE VALIDAÇÃO AUTÔNOMA ---

class AutonomousValidationService:
    """Serviço de Validação Autônoma"""
    
    def __init__(self):
        self.status = HealthStatus()
        self.recovery_logs: List[RecoveryLog] = []
        self.active = False
        self.max_retries = 3
        self.monitor_interval = None
        self.predictor = PredictiveMaintenanceNet()
        self.start_time = datetime.now()
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Estatísticas
        self.stats = {
            'total_checks': 0,
            'successful_recoveries': 0,
            'failed_recoveries': 0,
            'predictive_actions': 0,
            'critical_escalations': 0,
            'average_recovery_time': 0.0
        }
        
        # Instâncias das dependências
        self.sentient_core = SentientCore()
        
        print("🩺 Sistema de Validação Autônoma Inicializado")
        print(f"   Configuração: Máximo de retries={self.max_retries}")
    
    async def start(self):
        """Inicia o serviço"""
        if self.active:
            print("⚠️ Serviço já está ativo")
            return
        
        self.active = True
        self.start_time = datetime.now()
        
        # Inicializa preditor
        await self.predictor.initialize()
        
        # Inicia loop de monitoramento em thread separada
        self.monitor_interval = threading.Thread(
            target=self._run_monitor_loop,
            daemon=True
        )
        self.monitor_interval.start()
        
        print("✅ Sistema de Validação Autônoma ATIVADO")
        self._log_recovery(
            issue="SYSTEM_START",
            action="Inicialização do Sistema de Validação",
            result=RecoveryResult.SUCCESS,
            agi_intervention=False
        )
    
    def stop(self):
        """Para o serviço"""
        if not self.active:
            return
        
        self.active = False
        
        if self.monitor_interval and self.monitor_interval.is_alive():
            self.monitor_interval.join(timeout=2.0)
        
        self.executor.shutdown(wait=False)
        
        print("⏹️ Sistema de Validação Autônoma DESATIVADO")
        self._log_recovery(
            issue="SYSTEM_STOP",
            action="Parada do Sistema de Validação",
            result=RecoveryResult.SUCCESS,
            agi_intervention=False
        )
    
    # --- LOOP PRINCIPAL ---
    
    def _run_monitor_loop(self):
        """Loop de monitoramento (executado em thread separada)"""
        last_check = time.time()
        
        while self.active:
            try:
                current_time = time.time()
                elapsed = current_time - last_check
                
                # Executa ciclo a cada 5 segundos
                if elapsed >= 5:
                    # Executa em thread separada para não bloquear
                    self.executor.submit(self._execute_monitor_cycle)
                    last_check = current_time
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"⚠️ Erro no loop de monitoramento: {str(e)}")
                time.sleep(1)  # Espera antes de tentar novamente
    
    async def _execute_monitor_cycle(self):
        """Executa um ciclo completo de monitoramento"""
        if not self.active:
            return
        
        try:
            self.stats['total_checks'] += 1
            
            # Atualiza tempo de atividade
            self.status.uptime = (datetime.now() - self.start_time).total_seconds()
            
            # 1. Verifica saúde do sistema
            await self._check_system_health()
            
            # 2. Realiza análise preditiva
            await self._perform_predictive_analysis()
            
            # 3. Tenta recuperação automática
            await self._auto_recover()
            
        except Exception as e:
            print(f"❌ Erro crítico no validador: {str(e)}")
            self._log_recovery(
                issue="MONITOR_ERROR",
                action=f"Erro no ciclo de monitoramento: {str(e)}",
                result=RecoveryResult.FAILURE,
                agi_intervention=True
            )
    
    # --- VERIFICAÇÕES DE SAÚDE ---
    
    async def _check_system_health(self):
        """Verifica saúde do sistema"""
        issues: List[str] = []
        
        # 1. Verificação de Conexão
        is_connected = await self._validate_connection()
        if not is_connected:
            issues.append(IssueType.CONNECTION_EXCHANGE.value)
        self.status.connection = (
            ConnectionStatus.CONNECTED if is_connected 
            else ConnectionStatus.DISCONNECTED
        )
        
        # 2. Verificação de Recursos
        resources_ok = self._check_resources()
        if not resources_ok:
            issues.append(IssueType.SYSTEM_RESOURCES.value)
        
        # 3. Verificação de Latência de Rede
        latency_ok = self._check_network_latency()
        if not latency_ok:
            issues.append(IssueType.NETWORK_LATENCY.value)
        
        # Atualiza Status Global
        self.status.last_check = datetime.now()
        
        if issues:
            self.status.status = SystemStatus.WARNING
            if len(issues) >= 3:
                self.status.status = SystemStatus.CRITICAL
        else:
            self.status.status = SystemStatus.HEALTHY
        
        # Registra erros
        for issue in issues:
            self.status.error_count[issue] = self.status.error_count.get(issue, 0) + 1
        
        # Log de verificação
        if issues:
            print(f"⚠️ Issues detectadas: {', '.join(issues)}")
    
    async def _validate_connection(self) -> bool:
        """
        Valida conexão com serviços externos
        
        Returns:
            bool: True se conectado, False caso contrário
        """
        # Simula verificação de conexão
        # Em produção, faria um ping real na API da exchange
        connection_success_rate = 0.99  # 99% de sucesso
        
        # Chance de falha aumenta com erros acumulados
        error_penalty = min(0.3, self.status.error_count.get(IssueType.CONNECTION_EXCHANGE.value, 0) * 0.05)
        success_probability = connection_success_rate - error_penalty
        
        is_connected = random.random() < success_probability
        
        # Atualiza latência baseada no estado da conexão
        if is_connected:
            # Latência normal
            self.status.network_latency = random.uniform(10, 50)
        else:
            # Alta latência quando desconectado
            self.status.network_latency = random.uniform(200, 1000)
        
        return is_connected
    
    def _check_resources(self) -> bool:
        """
        Verifica recursos do sistema
        
        Returns:
            bool: True se recursos OK, False caso contrário
        """
        # Simula métricas de sistema
        base_cpu = random.uniform(10, 40)
        base_memory = random.uniform(20, 60)
        
        # Penalidades por erros acumulados
        resource_errors = self.status.error_count.get(IssueType.SYSTEM_RESOURCES.value, 0)
        memory_leak_errors = self.status.error_count.get(IssueType.MEMORY_LEAK.value, 0)
        
        cpu_penalty = min(30, resource_errors * 3)
        memory_penalty = min(40, (resource_errors + memory_leak_errors) * 5)
        
        self.status.cpu_load = min(100, base_cpu + cpu_penalty)
        self.status.memory_usage = min(100, base_memory + memory_penalty)
        
        # Verifica thresholds
        cpu_ok = self.status.cpu_load < 80
        memory_ok = self.status.memory_usage < 85
        
        # Simula vazamento de memória se erro acumular
        if resource_errors > 5:
            self.status.memory_usage = min(100, self.status.memory_usage + 15)
            memory_ok = False
        
        return cpu_ok and memory_ok
    
    def _check_network_latency(self) -> bool:
        """Verifica latência de rede"""
        # Penalidade por erros de latência
        latency_errors = self.status.error_count.get(IssueType.NETWORK_LATENCY.value, 0)
        latency_penalty = min(500, latency_errors * 50)
        
        # Latência base + penalidade
        base_latency = random.uniform(20, 100)
        self.status.network_latency = base_latency + latency_penalty
        
        return self.status.network_latency < 200  # Threshold de 200ms
    
    # --- IA & PREDIÇÃO ---
    
    async def _perform_predictive_analysis(self):
        """Realiza análise preditiva"""
        # Calcula taxa de erro
        total_errors = sum(self.status.error_count.values())
        error_rate = min(1.0, total_errors / 20.0)  # Normaliza para 0-1
        
        # Predição de falha baseada no estado atual
        metrics = [
            self.status.cpu_load / 100.0,
            self.status.memory_usage / 100.0,
            error_rate
        ]
        
        try:
            failure_probability = await self.predictor.predict_failure(metrics)
            self.status.prediction_score = failure_probability
            
            if failure_probability > 0.8:
                self.stats['predictive_actions'] += 1
                self._log_recovery(
                    issue="PREDICTIVE_MAINTENANCE",
                    action="Limpando caches preventivamente",
                    result=RecoveryResult.SUCCESS,
                    agi_intervention=True,
                    details={'probability': failure_probability}
                )
                
                # Simula ação preventiva
                self.status.memory_usage = max(20, self.status.memory_usage * 0.7)
                self.status.cpu_load = max(10, self.status.cpu_load * 0.8)
                
                # Limpa alguns erros
                for issue in list(self.status.error_count.keys()):
                    if random.random() > 0.5:
                        self.status.error_count[issue] = max(0, self.status.error_count[issue] - 1)
                
                print(f"🔮 Ação preditiva: probabilidade de falha {failure_probability:.1%}")
        
        except Exception as e:
            print(f"⚠️ Erro na análise preditiva: {str(e)}")
    
    # --- RECUPERAÇÃO AUTOMÁTICA ---
    
    async def _auto_recover(self):
        """Tenta recuperação automática"""
        issues = [k for k, v in self.status.error_count.items() if v > 0]
        
        if not issues:
            return
        
        # Influência da AGI na paciência
        agi_state = self.sentient_core.get_vector()
        
        # Se AGI está calma/estável, tenta mais vezes antes de desistir
        agi_bonus_retries = int(agi_state.stability / 20)
        current_max_retries = self.max_retries + agi_bonus_retries
        
        for issue in issues:
            count = self.status.error_count[issue]
            
            if count <= current_max_retries:
                start_time = time.time()
                success = await self._apply_fix(issue)
                recovery_time = time.time() - start_time
                
                # Atualiza tempo médio de recuperação
                alpha = 0.1
                self.stats['average_recovery_time'] = (
                    (1 - alpha) * self.stats['average_recovery_time'] + 
                    alpha * recovery_time
                )
                
                if success:
                    self.stats['successful_recoveries'] += 1
                    # Reset contador se fix assumido bem sucedido
                    if random.random() > 0.2:  # 80% de chance de sucesso
                        self.status.error_count[issue] = 0
                else:
                    self.stats['failed_recoveries'] += 1
            
            else:
                # Escalação crítica
                self.stats['critical_escalations'] += 1
                self.sentient_core.add_thought(
                    f"Problema crítico persistente: {issue}. Solicitando intervenção."
                )
                
                self._log_recovery(
                    issue=issue,
                    action="Notificação ao Admin (Simulada)",
                    result=RecoveryResult.FAILURE,
                    agi_intervention=False,
                    details={
                        'retry_count': count,
                        'max_retries': current_max_retries,
                        'agi_stability': agi_state.stability
                    }
                )
                
                self.status.status = SystemStatus.CRITICAL
    
    async def _apply_fix(self, issue: str) -> bool:
        """
        Aplica correção para um problema específico
        
        Args:
            issue: Tipo de problema
            
        Returns:
            bool: True se correção aplicada com sucesso
        """
        action = ""
        success = True
        details = {}
        
        try:
            if issue == IssueType.CONNECTION_EXCHANGE.value:
                action = "Reiniciando Adaptador de Rede Neural"
                details = {'method': 'soft_reset', 'retry_delay': '2s'}
                
                # Lógica de reconexão
                await asyncio.sleep(0.5)  # Simula tempo de reconexão
                success = random.random() > 0.3  # 70% de sucesso
            
            elif issue == IssueType.SYSTEM_RESOURCES.value:
                action = "Garbage Collection Forçado & Flush de Tensores"
                details = {'method': 'gc_collect', 'aggressiveness': 'high'}
                
                # Lógica de limpeza
                self.status.memory_usage = max(20, self.status.memory_usage * 0.5)
                self.status.cpu_load = max(10, self.status.cpu_load * 0.6)
                success = True
            
            elif issue == IssueType.MEMORY_LEAK.value:
                action = "Identificação e Correção de Vazamento de Memória"
                details = {'method': 'heap_analysis', 'cleanup': 'full'}
                
                # Limpa memória
                self.status.memory_usage = 30
                success = random.random() > 0.4  # 60% de sucesso
            
            elif issue == IssueType.NETWORK_LATENCY.value:
                action = "Otimização de Rota de Rede"
                details = {'method': 'route_optimization', 'protocol': 'UDP/TCP'}
                
                # Reduz latência
                self.status.network_latency = max(10, self.status.network_latency * 0.7)
                success = random.random() > 0.2  # 80% de sucesso
            
            else:
                action = "Diagnóstico Genérico e Correção"
                details = {'method': 'generic_fix', 'scope': 'system_wide'}
                success = random.random() > 0.5  # 50% de sucesso
            
            # Log da recuperação
            self._log_recovery(
                issue=issue,
                action=action,
                result=RecoveryResult.SUCCESS if success else RecoveryResult.FAILURE,
                agi_intervention=True,
                details=details
            )
            
            # Feedback para AGI
            self.sentient_core.perceive_reality(
                volatility=0.5,
                outcome=1.0 if success else -1.0
            )
            
            return success
            
        except Exception as e:
            print(f"❌ Erro ao aplicar correção para {issue}: {str(e)}")
            return False
    
    def _log_recovery(self, issue: str, action: str, result: RecoveryResult, 
                     agi_intervention: bool, details: Optional[Dict[str, Any]] = None):
        """Registra log de recuperação"""
        log = RecoveryLog(
            id=f"REC-{int(time.time()*1000)}-{random.randint(1000, 9999)}",
            timestamp=datetime.now(),
            issue=issue,
            action=action,
            result=result,
            agi_intervention=agi_intervention,
            details=details or {}
        )
        
        self.recovery_logs.insert(0, log)
        
        # Limita histórico
        if len(self.recovery_logs) > 50:
            self.recovery_logs = self.recovery_logs[:50]
        
        # Exibe log
        print(f"📋 Recuperação: {issue} -> {action} [{result.value}]")
    
    # --- MÉTODOS PÚBLICOS ---
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do sistema"""
        recent_logs = [log.get_log_info() for log in self.recovery_logs[:5]]
        
        return {
            'active': self.active,
            'health': self.status.get_summary(),
            'statistics': {
                'total_checks': self.stats['total_checks'],
                'successful_recoveries': self.stats['successful_recoveries'],
                'failed_recoveries': self.stats['failed_recoveries'],
                'success_rate': (
                    self.stats['successful_recoveries'] / 
                    max(1, self.stats['successful_recoveries'] + self.stats['failed_recoveries'])
                ),
                'predictive_actions': self.stats['predictive_actions'],
                'critical_escalations': self.stats['critical_escalations'],
                'avg_recovery_time_s': f"{self.stats['average_recovery_time']:.2f}"
            },
            'error_distribution': self.status.error_count.copy(),
            'recent_recovery_logs': recent_logs,
            'prediction_stats': self.predictor.get_prediction_stats(),
            'agi_state': {
                'confidence': self.sentient_core.vector.confidence,
                'stability': self.sentient_core.vector.stability,
                'thoughts_count': len(self.sentient_core.thoughts)
            }
        }
    
    def get_recovery_history(self, limit: int = 10, 
                            issue_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna histórico de recuperação"""
        filtered_logs = self.recovery_logs
        
        if issue_filter:
            filtered_logs = [log for log in filtered_logs if log.issue == issue_filter]
        
        return [log.get_log_info() for log in filtered_logs[:limit]]
    
    def force_recovery(self, issue: str):
        """Força tentativa de recuperação para um problema específico"""
        if not self.active:
            print("⚠️ Sistema não está ativo")
            return
        
        print(f"🔄 Forçando recuperação para: {issue}")
        
        # Executa em thread separada
        self.executor.submit(
            lambda: asyncio.run(self._apply_fix(issue))
        )

# --- INSTÂNCIA GLOBAL ---

auto_validator = AutonomousValidationService()

# --- FUNÇÃO DE DEMONSTRAÇÃO ---

async def demonstrate_validation_service():
    """Demonstra o serviço de validação autônoma"""
    
    print("=" * 60)
    print("SERVIÇO DE VALIDAÇÃO AUTÔNOMA - DEMONSTRAÇÃO")
    print("=" * 60)
    
    # Status inicial
    print("\n📊 STATUS INICIAL:")
    initial_status = auto_validator.get_status()
    print(f"  Ativo: {'✅' if initial_status['active'] else '❌'}")
    print(f"  Status: {initial_status['health']['status']}")
    print(f"  Conexão: {initial_status['health']['connection']}")
    
    # Inicia serviço
    print("\n🚀 INICIANDO SERVIÇO...")
    await auto_validator.start()
    
    # Aguarda alguns ciclos
    print("\n⏳ EXECUTANDO MONITORAMENTO (aguarde 15 segundos)...")
    await asyncio.sleep(15)
    
    # Obtém status atualizado
    print("\n📈 STATUS ATUALIZADO:")
    current_status = auto_validator.get_status()
    
    print(f"\n  SAÚDE DO SISTEMA:")
    for key, value in current_status['health'].items():
        print(f"    {key}: {value}")
    
    print(f"\n  ESTATÍSTICAS:")
    stats = current_status['statistics']
    print(f"    Total de verificações: {stats['total_checks']}")
    print(f"    Recuperações bem-sucedidas: {stats['successful_recoveries']}")
    print(f"    Recuperações falhas: {stats['failed_recoveries']}")
    print(f"    Taxa de sucesso: {stats['success_rate']:.1%}")
    print(f"    Ações preditivas: {stats['predictive_actions']}")
    print(f"    Tempo médio de recuperação: {stats['avg_recovery_time_s']}s")
    
    print(f"\n  DISTRIBUIÇÃO DE ERROS:")
    for issue, count in current_status['error_distribution'].items():
        print(f"    {issue}: {count}")
    
    print(f"\n  ESTADO DA AGI:")
    agi_state = current_status['agi_state']
    print(f"    Confiança: {agi_state['confidence']:.1f}")
    print(f"    Estabilidade: {agi_state['stability']:.1f}")
    print(f"    Pensamentos registrados: {agi_state['thoughts_count']}")
    
    # Histórico de recuperação
    print(f"\n  ÚLTIMAS RECUPERAÇÕES:")
    recovery_history = auto_validator.get_recovery_history(limit=3)
    for log in recovery_history:
        print(f"    [{log['timestamp'][11:]}] {log['issue']}: {log['action']} [{log['result']}]")
    
    # Força uma recuperação
    print("\n🔄 FORÇANDO RECUPERAÇÃO DE TESTE...")
    auto_validator.force_recovery(IssueType.SYSTEM_RESOURCES.value)
    await asyncio.sleep(2)
    
    # Para o serviço
    print("\n🛑 PARANDO SERVIÇO...")
    auto_validator.stop()
    
    print("\n📋 RELATÓRIO FINAL:")
    final_status = auto_validator.get_status()
    
    print(f"  Total de ciclos executados: {final_status['statistics']['total_checks']}")
    print(f"  Taxa geral de sucesso: {final_status['statistics']['success_rate']:.1%}")
    print(f"  Status final: {final_status['health']['status']}")
    
    print("\n" + "=" * 60)
    print("✅ Demonstração do Serviço de Validação completa!")
    print("=" * 60)

if __name__ == "__main__":
    # Executa demonstração
    asyncio.run(demonstrate_validation_service())