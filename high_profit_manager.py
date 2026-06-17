from typing import Dict, List
import pandas as pd
import numpy as np
from dataclasses import dataclass
import logging
from enum import Enum

class NivelGanho(Enum):
    INICIAL = "80%"
    INTERMEDIARIO = "200%"
    AVANCADO = "500%"
    EXCEPCIONAL = "1000%"

@dataclass
class ConfiguracaoGanhos:
    # Níveis de saída em porcentagem
    nivel_1: float = 80.0
    nivel_2: float = 200.0
    nivel_3: float = 500.0
    nivel_4: float = 1000.0
    # Total de volume de saída
    total_volume: float = 1.0
    # Número de ações a serem compradas por saída
    volume_1: float = 0.25
    volume_2: float = 0.25
    volume_3: float = 0.25
    volume_4: float = 0.25
    def __post_init__(self):
        self.total_volume = self.volume_1 + self.volume_2 + self.volume_3 + self.volume_4 
        if self.total_volume != 1.0:
            raise ValueError("Volumes de saída devem somar 1.0")

class GerenciadorGanhos:
    def __init__(self, config: ConfiguracaoGanhos = None):
        self.config = config or ConfiguracaoGanhos()
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def calcular_ganho_percentual(self, posicao: Dict) -> float:
        """Calcula ganho percentual atual"""
        return ((posicao['preco_atual'] - posicao['preco_entrada']) 
                / posicao['preco_entrada']) * 100
    
    def gerenciar_posicao(self, posicao: Dict) -> Dict:
        """Gerencia saídas baseadas em níveis de ganho"""
        ganho_atual = self.calcular_ganho_percentual(posicao)
        resultado = {
            'acao': None,
            'nivel': None,
            'volume': 0,
            'preco': 0,
            'ganho_percentual': ganho_atual
        }
        
        # Verifica cada nível de ganho
    
    # Volume de saída por nível
    volume_1: float = 0.25  # 25% da posição
    volume_2: float = 0.25  # 25% da posição
    volume_3: float = 0.25  # 25% da posição
    volume_4: float = 0.25  # 25% restante
    # Níveis de ganho em porcentagem
    nivel_1: float = 80.0
    nivel_2: float = 200.0
    nivel_3: float = 500.0
    nivel_4: float = 1000.0
    # Total de volume de saída
    total_volume: float = 1.0
    
    def __post_init__(self):
        self.total_volume = self.volume_1 + self.volume_2 + self.volume_3 + self.volume_4 
        if self.total_volume != 1.0:
            raise ValueError("Volumes de saída devem somar 1.0")
        
        if self.nivel_1 + self.nivel_2 + self.nivel_3 + self.nivel_4 != 100.0:
            raise ValueError("Níveis de ganho devem somar 100.0")
    
    def gerenciar_posicao(self, posicao: Dict) -> Dict:
        """Gerencia saídas baseadas em níveis de ganho"""
        # Verifica cada nível de ganho
        ganho_atual = self.calcular_ganho_percentual(posicao)
        if ganho_atual >= self.nivel_1:
            return {
                'acao': 'comprar',
                'nivel': 'nivel_1',
                'volume': self.volume_1,
                'preco': posicao['preco_entrada'] * (1 + self.nivel_1 / 100),
                'ganho_percentual': self.nivel_1
            }
        elif ganho_atual >= self.nivel_2:
            return {
                'acao': 'comprar',
                'nivel': 'nivel_2',
                'volume': self.volume_2,
                'preco': posicao['preco_entrada'] * (1 + self.nivel_2 / 100),
                'ganho_percentual': self.nivel_2
            }
        elif ganho_atual >= self.nivel_3:
            return {
                'acao': 'comprar',
                'nivel': 'nivel_3',
                'volume': self.volume_3,
                'preco': posicao['preco_entrada'] * (1 + self.nivel_3 / 100),
                'ganho_percentual': self.nivel_3
            }
        elif ganho_atual >= self.nivel_4:
            return {
                'acao': 'comprar',
                'nivel': 'nivel_4',
                'volume': self.volume_4,
                'preco': posicao['preco_entrada'] * (1 + self.nivel_4 / 100),
                'ganho_percentual': self.nivel_4
            }
        else:
            return None
        def calcular_ganho_percentual(self, posicao: Dict) -> float:
        """Calcula ganho percentual atual"""
        return ((posicao['preco_atual'] - posicao['preco_entrada']) 
                 / posicao['preco_entrada']) * 100
    
    def gerenciar_posicao(self, posicao: Dict) -> Dict:
        """Gerencia saídas baseadas em níveis de ganho"""
        ganho_atual = self.calcular_ganho_percentual(posicao)
        resultado = {
            'acao': None,
            'nivel': None,
            'volume': 0,
            'preco': 0,
            'ganho_percentual': ganho_atual
        }
        
        # Verifica cada nível de ganho
        if ganho_atual >= self.config.nivel_1:
            self.executar_saida_nivel_1(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_2:
            self.executar_saida_nivel_2(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_3:
            self.executar_saida_nivel_3(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_4:
            self.executar_saida_nivel_4(posicao, resultado)
        
        return resultado
    def executar_saida_nivel_1(self, posicao: Dict, resultado: Dict):
        """Executa saída do primeiro nível (80%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.INICIAL,
            'volume': posicao['volume'] * self.config.volume_1,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 1 (80%) acionada: {resultado['volume']} unidades")
    
    def executar_saida_nivel_2(self, posicao: Dict, resultado: Dict):
        """Executa saída do segundo nível (200%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.INTERMEDIARIO,
            'volume': posicao['volume'] * self.config.volume_2,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 2 (200%) acionada: {resultado['volume']} unidades")
        def executar_saida_nivel_3(self, posicao: Dict, resultado: Dict):
        """Executa saída do terceiro nível (500%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.AVANCADO,
            'volume': posicao['volume'] * self.config.volume_3,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 3 (500%) acionada: {resultado['volume']} unidades")
    
    def executar_saida_nivel_4(self, posicao: Dict, resultado: Dict):
        """Executa saída do quarto nível (1000%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.EXCEPCIONAL,
            'volume': posicao['volume'] * self.config.volume_4,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 4 (1000%) acionada: {resultado['volume']} unidades")
        def gerenciar_posicao(self, posicao: Dict) -> Dict:
        """Gerencia saídas baseadas em níveis de ganho"""
        ganho_atual = self.calcular_ganho_percentual(posicao)
        resultado = {
            'acao': None,
            'nivel': None,
            'volume': 0,
            'preco': 0,
            'ganho_percentual': ganho_atual
        }
        
        # Verifica cada nível de ganho
        if ganho_atual >= self.config.nivel_1:
            self.executar_saida_nivel_1(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_2:
            self.executar_saida_nivel_2(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_3:
            self.executar_saida_nivel_3(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_4:
            self.executar_saida_nivel_4(posicao, resultado)
        
        return resultado
    
    def executar_saida_nivel_1(self, posicao: Dict, resultado: Dict):
        """Executa saída do primeiro nível (80%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.INICIAL,
            'volume': posicao['volume'] * self.config.volume_1,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 1 (80%) acionada: {resultado['volume']} unidades")
        def executar_saida_nivel_2(self, posicao: Dict, resultado: Dict):
        """Executa saída do segundo nível (200%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.INTERMEDIARIO,
            'volume': posicao['volume'] * self.config.volume_2,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 2 (200%) acionada: {resultado['volume']} unidades")
        def executar_saida_nivel_3(self, posicao: Dict, resultado: Dict):
        """Executa saída do terceiro nível (500%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.AVANCADO,
            'volume': posicao['volume'] * self.config.volume_3,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 3 (500%) acionada: {resultado['volume']} unidades")
        def executar_saida_nivel_4(self, posicao: Dict, resultado: Dict):
        """Executa saída do quarto nível (1000%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.EXCEPCIONAL,
            'volume': posicao['volume'] * self.config.volume_4,
            'preco': posicao['preco_atual']
        })
        logging.info(f"Saída Nível 4 (1000%) acionada: {resultado['volume']} unidades")
        def gerenciar_posicao(self, posicao: Dict) -> Dict:
        """Gerencia saídas baseadas em níveis de ganho"""
        ganho_atual = self.calcular_ganho_percentual(posicao)
        resultado = {
            'acao': None,
            'nivel': None,
            'volume': 0,
            'preco': 0,
            'ganho_percentual': ganho_atual
        }
        
        # Verifica cada nível de ganho
        if ganho_atual >= self.config.nivel_1:
            self.executar_saida_nivel_1(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_2:
            self.executar_saida_nivel_2(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_3:
            self.executar_saida_nivel_3(posicao, resultado)
            
        elif ganho_atual >= self.config.nivel_4:
            self.executar_saida_nivel_4(posicao, resultado)
        
        return resultado
    
    @property
    def volumes(self):
        return [self.volume_1, self.volume_2, self.volume_3, self.volume_4]
    
    def __post_init__(self):
        self.total_volume = self.volume_1 + self.volume_2 + self.volume_3 + self.volume_4 
        if self.total_volume != 1.0:
            raise ValueError("Volumes de saída devem somar 1.0")
        
class GerenciadorGanhosElevados:
    def __init__(self, config: ConfiguracaoGanhos = None):
        self.config = config or ConfiguracaoGanhos()
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def calcular_ganho_percentual(self, posicao: Dict) -> float:
        """Calcula ganho percentual atual"""
        return ((posicao['preco_atual'] - posicao['preco_entrada']) 
                / posicao['preco_entrada']) * 100
    
    def gerenciar_posicao(self, posicao: Dict) -> Dict:
        """Gerencia saídas baseadas em níveis de ganho"""
        ganho_atual = self.calcular_ganho_percentual(posicao)
        resultado = {
            'acao': None,
            'nivel': None,
            'volume': 0,
            'preco': 0,
            'ganho_percentual': ganho_atual
        }
        
        # Verifica cada nível de ganho
        if not posicao.get('nivel_1_executado', False) and ganho_atual >= self.config.nivel_1:
            self.executar_saida_nivel_1(posicao, resultado)
            
        elif not posicao.get('nivel_2_executado', False) and ganho_atual >= self.config.nivel_2:
            self.executar_saida_nivel_2(posicao, resultado)
            
        elif not posicao.get('nivel_3_executado', False) and ganho_atual >= self.config.nivel_3:
            self.executar_saida_nivel_3(posicao, resultado)
            
        elif not posicao.get('nivel_4_executado', False) and ganho_atual >= self.config.nivel_4:
            self.executar_saida_nivel_4(posicao, resultado)
        
        return resultado
    
    def executar_saida_nivel_1(self, posicao: Dict, resultado: Dict):
        """Executa saída do primeiro nível (80%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.INICIAL,
            'volume': posicao['volume'] * self.config.volume_1,
            'preco': posicao['preco_atual']
        })
        posicao['nivel_1_executado'] = True
        logging.info(f"Saída Nível 1 (80%) acionada: {resultado['volume']} unidades")
    
    def executar_saida_nivel_2(self, posicao: Dict, resultado: Dict):
        """Executa saída do segundo nível (200%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.INTERMEDIARIO,
            'volume': posicao['volume'] * self.config.volume_2,
            'preco': posicao['preco_atual']
        })
        posicao['nivel_2_executado'] = True
        logging.info(f"Saída Nível 2 (200%) acionada: {resultado['volume']} unidades")
    
    def executar_saida_nivel_3(self, posicao: Dict, resultado: Dict):
        """Executa saída do terceiro nível (500%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.AVANCADO,
            'volume': posicao['volume'] * self.config.volume_3,
            'preco': posicao['preco_atual']
        })
        posicao['nivel_3_executado'] = True
        logging.info(f"Saída Nível 3 (500%) acionada: {resultado['volume']} unidades")
    
    def executar_saida_nivel_4(self, posicao: Dict, resultado: Dict):
        """Executa saída do quarto nível (1000%)"""
        resultado.update({
            'acao': 'VENDER',
            'nivel': NivelGanho.EXCEPCIONAL,
            'volume': posicao['volume'] * self.config.volume_4,
            'preco': posicao['preco_atual']
        })
        posicao['nivel_4_executado'] = True
        logging.info(f"Saída Nível 4 (1000%) acionada: {resultado['volume']} unidades")

class MonitorGanhosElevados:
    def __init__(self):
        self.gerenciador = GerenciadorGanhosElevados()
        self.posicoes = {}
        self.historico_saidas = []
    
    def adicionar_posicao(self, posicao: Dict):
        """Adiciona nova posição para monitoramento"""
        self.posicoes[posicao['id']] = {
            **posicao,
            'nivel_1_executado': False,
            'nivel_2_executado': False,
            'nivel_3_executado': False,
            'nivel_4_executado': False
        }
    
    def atualizar_posicao(self, id_posicao: str, dados: Dict):
        """Atualiza posição e verifica níveis de ganho"""
        if id_posicao not in self.posicoes:
            return
        
        posicao = self.posicoes[id_posicao]
        posicao.update(dados)
        
        resultado = self.gerenciador.gerenciar_posicao(posicao)
        
        if resultado['acao'] == 'VENDER':
            self.registrar_saida(id_posicao, resultado)
    
    def registrar_saida(self, id_posicao: str, resultado: Dict):
        """Registra saída realizada"""
        self.historico_saidas.append({
            'id_posicao': id_posicao,
            'nivel': resultado['nivel'].value,
            'volume': resultado['volume'],
            'preco': resultado['preco'],
            'ganho_percentual': resultado['ganho_percentual'],
            'timestamp': pd.Timestamp.now()
        })
    
    def gerar_relatorio_performance(self) -> Dict:
        """Gera relatório de performance das saídas"""
        df_historico = pd.DataFrame(self.historico_saidas)
        
        if df_historico.empty:
            return {}
        
        return {
            'saidas_por_nivel': df_historico['nivel'].value_counts().to_dict(),
            'ganho_medio': df_historico['ganho_percentual'].mean(),
            'ganho_maximo': df_historico['ganho_percentual'].max(),
            'volume_total': df_historico['volume'].sum(),
            'distribuicao_ganhos': self.calcular_distribuicao_ganhos(df_historico)
        }
    
    def calcular_distribuicao_ganhos(self, df: pd.DataFrame) -> Dict:
        """Calcula distribuição dos ganhos por nível"""
        return df.groupby('nivel').agg({
            'ganho_percentual': ['mean', 'min', 'max', 'count'],
            'volume': 'sum'
        }).to_dict()

def main():
    # Exemplo de uso
    monitor = MonitorGanhosElevados()
    
    # Adiciona posição exemplo
    posicao_exemplo = {
        'id': 'CRIPTO-001',
        'preco_entrada': 100.00,
        'volume': 1000,
        'preco_atual': 100.00
    }
    
    monitor.adicionar_posicao(posicao_exemplo)
    
    # Simula atualizações de preço com ganhos elevados
    precos_teste = [
        180.00,  # +80%
        300.00,  # +200%
        600.00,  # +500%
        1100.00  # +1000%
    ]
    
    for preco in precos_teste:
        monitor.atualizar_posicao('CRIPTO-001', {
            'preco_atual': preco
        })
    
    # Gera relatório
    relatorio = monitor.gerar_relatorio_performance()
    print("\nRelatório de Ganhos Elevados:")
    print(f"Saídas por nível: {relatorio.get('saidas_por_nivel', {})}")
    print(f"Ganho médio: {relatorio.get('ganho_medio', 0):.2f}%")
    print(f"Ganho máximo: {relatorio.get('ganho_maximo', 0):.2f}%")

if __name__ == "__main__":
    main() 
    