# LEXTRADER-IAG 5.0  
## Sistema Cerebral Artificial para o Mercado Financeiro VHALINOR 

**LEXTRADER-IAG 5.0** é um sistema avançado baseado em inteligência artificial, projetado para **análise**, **previsão** e **execução autônoma de operações** nos mercados financeiros. Ele integra múltiplas técnicas de machine learning, indicadores técnicos e uma arquitetura inspirada em redes neurais (neurônios especializados) para fornecer sinais de trading, gestão de risco e um dashboard interativo em tempo real.

---

## 🚀 Funcionalidades Principais  

- **Coleta de dados financeiros** – Integração com Yahoo Finance (yfinance) para cotações históricas e em tempo real de ações, criptomoedas, índices, forex e commodities.  
- **Indicadores técnicos** – Cálculo de RSI, MACD, Bandas de Bollinger, Médias Móveis (SMA/EMA), Estocástico, ATR e muito mais (com `pandas_ta` e implementações customizadas).  
- **Modelos de previsão** – Treinamento e inferência com:
  - LSTM (via PyTorch ou TensorFlow)  
  - Random Forest (scikit-learn)  
  Suporte extensível para ARIMA e Prophet (planejado).  
- **Estratégias de trading** – Combinação de sinais baseados em regras (cruzamento de médias, RSI+MACD) com votação para decisões automáticas.  
- **Execução autônoma de trades** – Módulo de trading simulado com gestão de risco adaptável (conservador, moderado, agressivo), stop-loss, take-profit e dimensionamento de posição.  
- **Dashboard interativo (GUI)** – Interface Tkinter com abas para visão geral do portfólio, gráficos de candlestick, histórico de trades, previsões em tempo real e monitoramento do “cérebro” neural.  
- **Memória e aprendizado contínuo** – Os “neurônios financeiros” armazenam estados, padrões e resultados para refinar futuras decisões.  
- **Arquitetura modular** – Componentes desacoplados (coleta, indicadores, previsão, estratégia, execução) facilitam customizações e expansões.  

---

## 📋 Requisitos  

### Principais  
- Python 3.8 ou superior  
- NumPy, Pandas, Matplotlib  
- scikit-learn, joblib  
- yfinance  
- pandas_ta  
- PyYAML  

### Opcionais (para funcionalidades avançadas)  
- **TensorFlow** ou **PyTorch** – Para modelos LSTM (se nenhum estiver presente, apenas Random Forest estará disponível).  
- **Qiskit** – Para experimentos quânticos (funcionalidade experimental).  
- **NetworkX** – Para visualização expandida da rede neural (não obrigatório para o núcleo).  
- **Tkinter** – Necessário para o dashboard gráfico (já incluso na maioria das instalações Python; caso contrário, o sistema roda apenas em modo console).  

### Instalação  
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/lextrader-iag.git
cd lextrader-iag

# Instale as dependências obrigatórias
pip install numpy pandas matplotlib scikit-learn joblib yfinance pandas_ta pyyaml

# (Opcional) Para redes neurais profundas:
pip install tensorflow        # ou pip install torch

# (Opcional) Para a interface gráfica completa:
# Tkinter geralmente já vem com o Python; caso contrário, instale conforme seu sistema.
