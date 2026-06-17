from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
import threading
import time
import math
import random
import html

# Registrar no NeuralBus
try:
    from neural_bus import NeuralBus
except ImportError:
    NeuralBus = None

def _escape(s: Optional[str]) -> str:
    return html.escape(s or "")

def _cn(*classes: Optional[str]) -> str:
    return " ".join(filter(None, classes))

@dataclass
class Connection:
    id: str
    from_id: str
    to_id: str
    weight: float
    strength: float
    is_active: bool
    traffic_intensity: float
    last_update: float
    adaptive_weight: float

@dataclass
class Neuron:
    id: str
    layer: int
    position: Dict[str, float]
    activation: float
    bias: float
    is_active: bool
    type: str  # 'INPUT'|'HIDDEN'|'OUTPUT'|'MEMORY'|'ATTENTION'
    connections: List[Connection] = field(default_factory=list)
    last_signal: float = field(default_factory=time.time)
    learning_rate: float = 0.001
    plasticity: float = 0.5

@dataclass
class NetworkLayer:
    id: str
    name: str
    type: str
    neurons: int
    activation: str
    learning_rate: float
    output_size: int
    parameters: int
    is_training: bool
    accuracy: float
    loss: float

@dataclass
class NetworkArchitecture:
    total_neurons: int = 0
    total_connections: int = 0
    total_layers: int = 0
    memory_usage: float = 0.0
    processing_power: float = 0.0
    parallel_streams: int = 0
    quantum_entanglements: int = 0
    synaptic_plasticity: float = 0.0
    learning_velocity: float = 0.0
    consciousness_level: float = 0.0

@dataclass
class TrainingMetrics:
    epoch: int = 0
    accuracy: float = 0.0
    loss: float = 0.0
    validation_accuracy: float = 0.0
    learning_rate: float = 0.001
    batch_size: int = 32
    training_time: float = 0.0
    convergence: float = 0.0
    overfitting: float = 0.0
    generalization: float = 0.0

class DeepNeuralNetwork:
    def __init__(self, refresh_activity_sec: float = 0.1, train_interval_sec: float = 0.2):
        self.layers: List[NetworkLayer] = []
        self.neurons: List[Neuron] = []
        self.connections: List[Connection] = []
        self.architecture = NetworkArchitecture()
        self.training_metrics = TrainingMetrics()
        self.is_training = False
        self.network_active = True
        self.visualization_mode = "ACTIVITY"
        self.network_depth = 12
        self.learning_intensity = 0.7
        self.plasticity_level = 0.85

        self._refresh_activity_sec = refresh_activity_sec
        self._train_interval_sec = train_interval_sec

        self._stop_event = threading.Event()
        self._activity_thread = threading.Thread(target=self._activity_loop, daemon=True)
        self._train_thread = threading.Thread(target=self._train_loop, daemon=True)

        # initialize network
        self.initialize_deep_network()
        self.start()
        
        # Registrar no NeuralBus para comunicação entre módulos
        if NeuralBus:
            try:
                NeuralBus.get_instance().register(
                    "deep_neural_network",
                    self,
                    {"type": "DeepNeuralNetwork", "file": "DeepNeuralNetwork.py"}
                )
            except Exception:
                pass

    # --- Initialization / reset ---
    def initialize_deep_network(self):
        new_layers = [
            NetworkLayer('input_layer', 'Entrada Multi-Modal', 'DENSE', 256, 'relu', 0.001, 256, 65536, False, 98.7, 0.023),
            NetworkLayer('conv1', 'Convolução Temporal', 'CONVOLUTION', 512, 'leaky_relu', 0.0008, 512, 131072, self.is_training, 94.2, 0.047),
            NetworkLayer('conv2', 'Convolução Espacial', 'CONVOLUTION', 1024, 'swish', 0.0006, 1024, 524288, self.is_training, 91.8, 0.062),
            NetworkLayer('lstm1', 'LSTM Temporal', 'LSTM', 768, 'tanh', 0.0004, 768, 2359296, self.is_training, 96.3, 0.031),
            NetworkLayer('transformer1', 'Multi-Head Attention', 'TRANSFORMER', 2048, 'gelu', 0.0002, 2048, 8388608, self.is_training, 97.9, 0.018),
            NetworkLayer('attention1', 'Self-Attention', 'ATTENTION', 1536, 'softmax', 0.0003, 1536, 4718592, self.is_training, 95.7, 0.038),
            NetworkLayer('dense1', 'Processamento Denso', 'DENSE', 1024, 'relu', 0.0005, 1024, 1572864, self.is_training, 93.4, 0.052),
            NetworkLayer('dropout1', 'Regularização', 'DROPOUT', 512, 'linear', 0.0007, 512, 524288, self.is_training, 94.8, 0.043),
            NetworkLayer('output_layer', 'Decisões Finais', 'DENSE', 128, 'sigmoid', 0.001, 5, 65536, False, 97.2, 0.025),
        ]

        # generate neurons
        new_neurons: List[Neuron] = []
        nid = 0
        for li, layer in enumerate(new_layers):
            for i in range(layer.neurons):
                n = Neuron(
                    id=f"neuron_{nid}",
                    layer=li,
                    position={"x": li * 100 + random.uniform(-40, 40), "y": (i * 800 / max(1, layer.neurons)) + random.uniform(-10, 10)},
                    activation=random.random() * self.learning_intensity,
                    bias=random.uniform(-0.1, 0.1),
                    is_active=random.random() > 0.1,
                    type=('INPUT' if li == 0 else 'OUTPUT' if li == len(new_layers)-1 else ('MEMORY' if layer.type=='LSTM' else ('ATTENTION' if layer.type=='ATTENTION' else 'HIDDEN'))),
                    learning_rate=layer.learning_rate,
                    plasticity=self.plasticity_level + random.uniform(-0.1, 0.1),
                )
                new_neurons.append(n)
                nid += 1

        # connect adjacent layers
        new_connections: List[Connection] = []
        cid = 0
        for li in range(len(new_layers)-1):
            from_neurons = [n for n in new_neurons if n.layer == li]
            to_neurons = [n for n in new_neurons if n.layer == li+1]
            for fn in from_neurons:
                # connect to a subset
                targets = random.sample(to_neurons, k=max(1, int(len(to_neurons)*0.2)))
                for tn in targets:
                    conn = Connection(
                        id=f"conn_{cid}",
                        from_id=fn.id,
                        to_id=tn.id,
                        weight=random.uniform(-1.0, 1.0),
                        strength=random.uniform(0.2, 1.0),
                        is_active=random.random() > 0.05,
                        traffic_intensity=random.random(),
                        last_update=time.time(),
                        adaptive_weight=random.uniform(-0.5, 0.5)
                    )
                    new_connections.append(conn)
                    fn.connections.append(conn)
                    cid += 1

        # skip connections (ResNet-like)
        for li in range(len(new_layers)-2):
            sources = [n for n in new_neurons if n.layer == li]
            targets = [n for n in new_neurons if n.layer == li+2]
            for s in sources:
                if random.random() < 0.3:
                    t = random.choice(targets)
                    conn = Connection(
                        id=f"skip_{cid}",
                        from_id=s.id,
                        to_id=t.id,
                        weight=random.uniform(-0.5, 0.5),
                        strength=random.uniform(0.1, 0.5),
                        is_active=True,
                        traffic_intensity=random.random()*0.5,
                        last_update=time.time(),
                        adaptive_weight=random.uniform(-0.3, 0.3)
                    )
                    new_connections.append(conn)
                    s.connections.append(conn)
                    cid += 1

        self.layers = new_layers
        self.neurons = new_neurons
        self.connections = new_connections

        total_params = sum(layer.parameters for layer in new_layers)
        self.architecture = NetworkArchitecture(
            total_neurons=len(new_neurons),
            total_connections=len(new_connections),
            total_layers=len(new_layers),
            memory_usage=total_params * 4 / (1024*1024),
            processing_power=len(new_neurons) * 0.001,
            parallel_streams=max(1, len(new_neurons)//256),
            quantum_entanglements=int(len(new_connections)*0.05),
            synaptic_plasticity=self.plasticity_level * 100,
            learning_velocity=self.learning_intensity * 100,
            consciousness_level=(sum(1 for n in new_neurons if n.is_active)/len(new_neurons))*100
        )

    # --- Simulation loops ---
    def _activity_loop(self):
        while not self._stop_event.wait(self._refresh_activity_sec):
            if not self.network_active:
                continue
            self._simulate_activity_step()

    def _simulate_activity_step(self):
        # update neuron activations
        id_to_neuron = {n.id: n for n in self.neurons}
        new_activations: Dict[str, float] = {}
        for n in self.neurons:
            if n.type == 'INPUT':
                val = math.sin(time.time()*0.001 + n.position['x']*0.01)*0.5 + 0.5
            else:
                incoming = 0.0
                for conn in self.connections:
                    if conn.to_id == n.id and conn.is_active:
                        src = id_to_neuron.get(conn.from_id)
                        if src:
                            incoming += src.activation * conn.weight * conn.strength
                val = math.tanh(incoming + n.bias) * n.plasticity
                val *= 0.95
            new_activations[n.id] = max(0.0, min(1.0, val))
        for n in self.neurons:
            n.activation = new_activations.get(n.id, n.activation)
            n.is_active = n.activation > 0.1
            if n.activation > 0.3:
                n.last_signal = time.time()

        # update connections traffic and slight adaptation
        for c in self.connections:
            c.traffic_intensity = max(0.0, c.traffic_intensity*0.9 + random.random()*0.3)
            c.weight += (random.random()-0.5)*0.001*self.learning_intensity
            c.last_update = time.time()

    def _train_loop(self):
        while not self._stop_event.wait(self._train_interval_sec):
            if not self.is_training:
                continue
            self._train_step()

    def _train_step(self):
        tm = self.training_metrics
        tm.epoch += 1
        base_accuracy = 0.85 + math.log(tm.epoch+1)*0.05
        noise = (random.random()-0.5)*0.02
        tm.accuracy = min(0.99, base_accuracy + noise)
        tm.loss = max(0.001, 0.5 / math.sqrt(tm.epoch+1) + abs(noise)*0.1)
        tm.validation_accuracy = min(0.98, base_accuracy*0.95 + noise*0.5)
        tm.convergence = min(100.0, (tm.epoch/1000.0)*100.0)
        tm.overfitting = max(0.0, (tm.accuracy - tm.validation_accuracy)*100.0)
        tm.generalization = max(0.0, min(100.0, tm.validation_accuracy*100.0 - tm.overfitting))
        tm.training_time += random.random()*0.5 + 0.1

        # update layers stats
        for layer in self.layers:
            layer.accuracy = min(99.0, layer.accuracy + (random.random()-0.4)*0.5)
            layer.loss = max(0.001, layer.loss * (0.999 + random.random()*0.002))
            layer.is_training = self.is_training and layer.type != 'DROPOUT'

    # --- control ---
    def start(self):
        if not self._activity_thread.is_alive():
            self._activity_thread = threading.Thread(target=self._activity_loop, daemon=True)
            self._activity_thread.start()
        if not self._train_thread.is_alive():
            self._train_thread = threading.Thread(target=self._train_loop, daemon=True)
            self._train_thread.start()

    def stop(self):
        self._stop_event.set()
        if self._activity_thread.is_alive():
            self._activity_thread.join(timeout=1.0)
        if self._train_thread.is_alive():
            self._train_thread.join(timeout=1.0)

    def toggle_training(self):
        self.is_training = not self.is_training

    def toggle_network(self):
        self.network_active = not self.network_active

    def reset(self):
        self.is_training = False
        self.training_metrics = TrainingMetrics()
        self.initialize_deep_network()

    # --- render server-side HTML (simplificado) ---
    def render_html(self) -> str:
        a = self.architecture
        tm = self.training_metrics
        html_parts: List[str] = []
        html_parts.append(f'<div class="card trading-card">')
        html_parts.append('<div class="card-header"><h3>Rede Neural Profunda</h3></div>')
        html_parts.append('<div class="card-content">')

        # architecture summary
        html_parts.append('<div class="grid grid-cols-2 md:grid-cols-4 gap-4">')
        html_parts.append(f'<div class="p-3 text-center"><div class="font-bold">{a.total_neurons:,}</div><div class="text-xs">Neurônios</div></div>')
        html_parts.append(f'<div class="p-3 text-center"><div class="font-bold">{a.total_connections:,}</div><div class="text-xs">Conexões</div></div>')
        html_parts.append(f'<div class="p-3 text-center"><div class="font-bold">{a.total_layers}</div><div class="text-xs">Camadas</div></div>')
        html_parts.append(f'<div class="p-3 text-center"><div class="font-bold">{a.memory_usage:.1f} MB</div><div class="text-xs">Memória estimada</div></div>')
        html_parts.append('</div>')

        # training metrics summary
        html_parts.append('<div class="grid grid-cols-2 gap-4 mt-4">')
        html_parts.append(f'<div class="p-3"><div class="text-xs">Época</div><div class="font-bold">{tm.epoch}</div></div>')
        html_parts.append(f'<div class="p-3"><div class="text-xs">Acurácia</div><div class="font-bold">{tm.accuracy:.3f}</div></div>')
        html_parts.append(f'<div class="p-3"><div class="text-xs">Loss</div><div class="font-bold">{tm.loss:.4f}</div></div>')
        html_parts.append(f'<div class="p-3"><div class="text-xs">Convergência</div><div class="font-bold">{tm.convergence:.1f}%</div></div>')
        html_parts.append('</div>')

        # layers list (compact)
        html_parts.append('<div class="mt-4 space-y-2">')
        for layer in self.layers:
            html_parts.append(f'<div class="border p-3 rounded"><div class="flex justify-between"><div><b>{_escape(layer.name)}</b> <small class="text-muted">({_escape(layer.type)})</small></div><div><small>{layer.neurons} neurônios</small></div></div>')
            html_parts.append(f'<div class="text-xs mt-2">Parâmetros: {layer.parameters:,} • Acurácia: {layer.accuracy:.1f}% • Loss: {layer.loss:.3f}</div></div>')
        html_parts.append('</div>')

        # simple visualization placeholder
        html_parts.append('<div class="mt-4 border rounded p-2 bg-black text-white">')
        html_parts.append('<div style="height:300px;display:flex;align-items:center;justify-content:center">')
        html_parts.append(f'<div>Visualização: {_escape(self.visualization_mode)} (render no cliente)</div>')
        html_parts.append('</div></div>')

        html_parts.append('</div></div>')
        return "\n".join(html_parts)

# Example usage
if __name__ == "__main__":
    dnn = DeepNeuralNetwork()
    try:
        time.sleep(1)
        print(dnn.render_html()[:1000])
    finally:
        dnn.stop()