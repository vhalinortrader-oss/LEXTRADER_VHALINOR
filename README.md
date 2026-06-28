# LEXTRADER-IAG 5.0  
**Sistema Cerebral Artificial para o Mercado Financeiro VHALINOR**

O **LEXTRADER-IAG 5.0** é uma plataforma de inteligência artificial modular que integra análise técnica avançada, aprendizado de máquina, processamento de linguagem natural e execução autônoma para operar nos mercados financeiros globais. Sua arquitetura é inspirada em redes neurais especializadas, combinando dezenas de indicadores, modelos preditivos e um sistema de memória contínua para tomar decisões de trading com gestão de risco adaptativa.

---

## 1. ANÁLISE MULTIDIMENSIONAL & GERAÇÃO DE SINAIS (Percepção)

**Objetivo:** Transformar dados brutos do mercado em uma representação unificada que alimenta as decisões.

### 1.1 Análise Técnica Clássica & Indicadores  
- Cálculo de mais de **60 indicadores** (tendência, momentum, volatilidade, volume, ciclos, padrões candlestick) via `pandas_ta` e implementações customizadas.  
- Exemplos: Ichimoku Cloud, SuperTrend, ADX, Stochastic RSI, OBV, reconhecimento de Doji, Engolfo, Martelo etc.

### 1.2 Análise de Ativos & Histórica  
- Coleta de dados OHLCV **multi-timeframe** (1m, 5m, 15m, 1h, 4h, 1d) a partir de Yahoo Finance, Google Finance, Binance, Bybit, Pionex e WebSocket em tempo real.  
- Armazenamento otimizado para séries temporais (InfluxDB, TimescaleDB) garantindo consultas rápidas e treinamento contínuo.

### 1.3 Análise de Mercado & Contexto Macroeconômico  
- Integração com dados **on-chain** (criptomoedas: fluxo de stablecoins, taxas de financiamento) e APIs de mercado tradicional (Índice de Medo e Ganância, VIX).  
- Matriz de correlação dinâmica para identificação automática de regimes de risco.

### 1.4 Análise de Padrões Gráficos & Candlestick  
- Reconhecimento automatizado de **padrões harmônicos** (Gartley, Borboleta), gráficos clássicos (cabeça-ombro, bandeiras, triângulos) e microestruturas de volume (Volume Profile, clusters).  
- Uso de algoritmos geométricos e **redes neurais convolucionais (CNN)** sobre imagens de velas ou diretamente sobre dados de preço/volume.

### 1.5 Análise de Notícias & Sentimento (NLP)  
- Coleta em tempo real de feeds (Reuters, CryptoPanic, Twitter/X) via APIs.  
- Processamento com **FinBERT** e modelos de linguagem financeira para classificação de sentimento (positivo/negativo/neutro) e extração de entidades (tickers, eventos).  
- Geração de um **score de sentimento** por ativo, ponderado por janela temporal e relevância da fonte.

### 1.6 Revisão e Seleção dos Melhores Ativos (Top-Down Screening)  
- Módulo de ranking que pontua ativos combinando: força da tendência, volatilidade relativa, volume, sentimento de notícias, correlação e momentum.  
- Algoritmo adaptado de *Relative Strength Rotation Graph* (RRG) para selecionar os **5 a 10 ativos com maior potencial** no horizonte de operação.

### 1.7 Neurônios Sensores Especializados  
- Cada grupo de análise (técnico, volume, sentimento, padrões) é encapsulado em um **neurônio sensor**, que gera uma saída padronizada (vetor de características) e uma medida de confiança.  
- **Exemplos:**  
  - *Neurônio de Momentum* → score entre -1 e +1 baseado em RSI, Stoch, CCI e Fisher Transform.  
  - *Neurônio de Sentimento* → score entre -1 e +1 a partir da análise NLP.  
  - *Neurônio de Volume* → score combinando OBV, CMF e Volume Profile.

---

## 2. APRENDIZADO DE MÁQUINA, EVOLUÇÃO E MEMÓRIA (Cognição)

**Objetivo:** Tomar decisões de trading a partir dos dados, aprender com os erros e evoluir as estratégias ao longo do tempo.

### 2.1 Modelos Preditivos Base (Núcleo de Previsão)  
- **LSTM/GRU com atenção** e **Transformers temporais** (Informer, Autoformer) para previsão de direção e volatilidade em múltiplos horizontes (15min, 1h, 4h).  
- **Gradient Boosting** (XGBoost, LightGBM) como baseline robusto, treinado com features técnicas + sentimento.  
- **Modelos probabilísticos** (DeepAR, Mixture Density Networks) para estimar a distribuição completa dos retornos.  
- **AutoML integrado** – seleção automática de arquitetura e hiperparâmetros via *Optuna* ou *Bayesian Optimization*, mantendo um histórico de versões dos modelos (versionamento).

### 2.2 Ensemble e Votação Inteligente  
- **Stacking** (meta‑modelo) que combina LSTM, XGBoost, Random Forest e Transformer com uma camada final de regressão logística ou rede neural rasa.  
- **Votação ponderada dinâmica** – o peso de cada modelo é atualizado a cada hora com base na acurácia direcional recente (janela móvel do índice de Sharpe ou taxa de acerto).

### 2.3 Aprendizado Contínuo & Adaptação Online  
- **Online Learning** com modelos incrementais (*Hoeffding Trees*, biblioteca `River`) que se atualizam a cada novo candle sem necessidade de retreinamento completo.  
- **Retreino agendado** (diário/semanal) com dados automaticamente rotulados: um sinal de compra que resultou em lucro > 2% em 24h recebe rótulo positivo.  
- **Decaimento de relevância** – amostras antigas têm peso exponencialmente menor, permitindo rápida adaptação a mudanças de regime.

### 2.4 Evolução de Estratégias (Reinforcement Learning & Algoritmos Genéticos)  
- **Reinforcement Learning (PPO, SAC, TD3)** – agente treinado em ambiente de simulação (backtest) para maximizar retorno ajustado ao risco; ações: comprar, vender, manter.  
- **Algoritmos Genéticos** – população de estratégias (combinações de regras, indicadores e parâmetros) que evoluem via crossover e mutação, selecionadas por métricas de risco/retorno.  
- Bibliotecas: `gym` customizado, `stable-baselines3`, `FinRL`, `DEAP`.

### 2.5 Aprendizagem de Estratégia por Imitação (Transfer Learning)  
- Extração de conhecimento a partir de **logs de traders experientes** – treinamento de um classificador que recomenda a ação ideal em cada estado.  
- Suporte a *Reinforcement Learning from Demonstrations (RLfD)* para acelerar o aprendizado do agente.

### 2.6 Memória de Longo Prazo (Córtex de Experiência)  
- Armazenamento de estados passados (vetor de indicadores + ação + resultado) em um **banco vetorial** de alta performance (FAISS / Annoy).  
- Durante a operação, o sistema consulta os **k vizinhos mais similares** e recupera as ações historicamente bem‑sucedidas naquele contexto.  
- **Poda inteligente** – a memória mantém apenas eventos de alta informação (grandes ganhos, perdas severas, reversões de tendência) para evitar sobrecarga e manter a relevância.

### 2.7 Autoavaliação e Confiança do Sistema  
- Cada sinal gerado recebe um **score de confiança** (0–100%) baseado na concordância dos modelos, na clareza do regime atual e na força dos neurônios sensores.  
- Sinais com baixa confiança podem ser ignorados ou executados com capital reduzido, conforme o perfil de risco selecionado.

---

## 3. EXECUÇÃO AUTÔNOMA EM PLATAFORMAS DE TRADING (Ação)

**Objetivo:** Converter sinais em ordens reais (ou simuladas) com baixa latência e rastreamento completo do estado.

### 3.1 Conectores Multi‑Exchange  
- Módulo padronizado para **Binance, Bybit, Pionex** e outras corretoras via APIs REST e WebSocket.  
- Suporte a ordens: market, limit, stop‑limit, OCO.  
- Reconexão automática e gerenciamento de sessão.

### 3.2 Fila de Sinais e Orquestração  
- Sinais são enfileirados com timestamp e validados por um **orquestrador** que verifica:  
  - Conflito com posição existente.  
  - Limite máximo de exposição.  
  - Intervalo mínimo entre operações (cooldown).  

### 3.3 Simulação e Paper Trading  
- Ambiente de **backtest realista** e trading simulado, usando dados históricos e latência simulada.  
- Métricas detalhadas (Sharpe, Sortino, Drawdown Máximo, Win Rate, Fator de Lucro) geradas automaticamente.

### 3.4 Gerenciamento de Estado de Posição  
- **Máquina de estados finita** para cada ativo: `IDLE → ENTRY → ACTIVE → PARTIAL_TP → EXIT`.  
- Atualização em tempo real via WebSocket, garantindo conhecimento exato do preço médio, tamanho e PnL de cada posição.

---

## 4. GESTÃO DE RISCO AUTÔNOMA (Preservação)

**Objetivo:** Proteger o capital e dimensionar operações de forma inteligente, adaptando-se à volatilidade do mercado.

### 4.1 Stop‑Loss e Take‑Profit Dinâmicos  
- Cálculo baseado em **ATR** (ex.: stop a 2× ATR, take a 3× ATR) ou em níveis de suporte/resistência extraídos do ZigZag e Volume Profile.  
- **Trailing stop** adaptativo que utiliza Parabolic SAR, SuperTrend ou uma fração da volatilidade recente.

### 4.2 Dimensionamento de Posição Adaptativo (Risk Sizing)  
- Fórmula baseada no **Critério de Kelly** fracionário ou risco fixo por trade (ex.: 1% do capital).  
- Ajuste conforme a **confiança do sinal** e a **volatilidade corrente** – em regimes de alta volatilidade, o tamanho da posição é automaticamente reduzido.  
- Consideração da correlação entre ativos para evitar superexposição a um único setor ou fator de risco.

### 4.3 Circuit Breakers e Filtros de Exposição  
- Limites rígidos: máximo de **5 posições simultâneas** e drawdown diário de -5%.  
- Bloqueio automático de novas entradas e redução parcial de posições ao atingir os limites.  
- **Detecção de eventos de alto impacto** (decisões de juros, anúncios macroeconômicos) e suspensão de operações 30 minutos antes/depois.

### 4.4 Perfis de Risco Selecionáveis  
- **Três modos pré‑configurados:** Conservador, Moderado, Agressivo.  
- Cada modo ajusta alavancagem máxima, percentual de risco por trade, proporção de ativos voláteis e trailing stop.  
- Um **meta‑gestor** pode alternar automaticamente entre perfis com base na volatilidade global (VIX, ATR médio do portfólio).

### 4.5 Relatórios de Risco em Tempo Real  
- Cálculo contínuo de **Value at Risk (VaR)**, **Conditional VaR (CVaR)** e testes de estresse (queda instantânea de 20%).  
- Exibição no dashboard e registro em logs para auditoria.

---

## 5. DASHBOARD INTERATIVO EM TEMPO REAL (Interface Humano‑Máquina)

**Objetivo:** Oferecer transparência total sobre o “cérebro” e permitir supervisão e intervenção manual.

### 5.1 Camada de Visualização  
- Interface gráfica modular com opções **Tkinter** (leve, local) e **Web (FastAPI + React)** para acesso remoto.  
- Abas: Visão Geral, Gráficos Interativos (Plotly), Histórico de Trades, Previsões ao Vivo, Mapa de Ativação Neural.  
- Gráficos de velas com indicadores sobrepostos (Ichimoku, Bandas de Bollinger), zonas de suporte/resistência e marcação de entradas/saídas.

### 5.2 Aba “Cérebro Neural”  
- Diagrama dinâmico que exibe a **ativação de cada neurônio especializado** (Tendência, Volume, Sentimento, Padrões) e o output combinado.  
- **Justificativa textual** gerada automaticamente: ex.: *“Compra sinalizada com 87% de confiança – RSI < 30, SuperTrend subiu e sentimento positivo no Twitter”*.

### 5.3 Monitor de Execução  
- Status em tempo real: ordens ativas, posições abertas, P&L por trade, log de eventos com alertas visuais (stop‑loss atingido, erro de conexão).

### 5.4 Controle Manual e Override  
- Botões para **encerrar posição**, **pausar execução autônoma** ou **alterar perfil de risco** com um clique.  
- Sliders para ajuste de parâmetros críticos (alavancagem máxima, trailing stop) sem necessidade de alterar código.

### 5.5 Painel de Performance  
- Curva de capital (equity curve), drawdown, retorno mensal, matriz de confusão dos modelos.  
- **Modo replay** – reconstrução visual do mercado passado para depuração de decisões (debugging temporal).

---

## 🔁 FLUXO DE DADOS RESUMIDO DA ARQUITETURA DE IA

1. **Ingestão:** Dados de mercado + notícias + on‑chain → streams em tempo real.  
2. **Processamento Sensorial:** Neurônios especializados calculam indicadores, sentimento e padrões.  
3. **Memória & Similaridade:** Busca por configurações históricas semelhantes.  
4. **Inferência Preditiva:** Ensemble de modelos (LSTM, XGBoost, Transformer) gera previsão de direção e volatilidade.  
5. **Decisão Estratégica:** RL + votação definem ação (comprar/vender/manter) e tamanho da posição.  
6. **Gestão de Risco:** Ajuste de stops, dimensionamento e verificação de limites de exposição.  
7. **Execução:** Ordem enviada à exchange; estado monitorado até a conclusão.  
8. **Feedback:** Resultado registrado na memória e utilizado para atualização contínua dos modelos e evolução das estratégias.

---

## 📊 PRINCIPAIS INDICADORES TÉCNICOS DISPONÍVEIS

*(Implementados com `pandas_ta` e funções customizadas – mais de 60 indicadores)*

### Tendência
| Indicador | Descrição | Código `pandas_ta` |
|-----------|-----------|-------------------|
| SMA | Média Móvel Simples | `sma()` |
| EMA | Média Móvel Exponencial | `ema()` |
| WMA | Média Móvel Ponderada | `wma()` |
| HMA | Hull Moving Average | `hma()` |
| MACD | Convergência/Divergência de Médias | `macd()` |
| ADX | Força da tendência | `adx()` |
| +DI / -DI | Direção da tendência | `adx()` (retorna DMP/DMN) |
| Parabolic SAR | Pontos de reversão | `psar()` |
| SuperTrend | Tendência baseada em ATR | `supertrend()` |
| Ichimoku Cloud | Suporte, resistência e momentum | `ichimoku()` |
| VWAP | Preço médio ponderado por volume | `vwap()` |
| KAMA | Média adaptativa (Kaufman) | `kama()` |
| TEMA | Triple EMA – suavização avançada | `tema()` |

### Momentum / Osciladores
| Indicador | Descrição | Código `pandas_ta` |
|-----------|-----------|-------------------|
| RSI | Índice de Força Relativa | `rsi()` |
| Stochastic (%K, %D) | Posição do fechamento | `stoch()` |
| Stochastic RSI | RSI do Stochastic | `stochrsi()` |
| Williams %R | Semelhante ao Stoch invertido | `willr()` |
| CCI | Commodity Channel Index | `cci()` |
| MFI | Índice de Fluxo de Dinheiro | `mfi()` |
| Ultimate Oscillator | Oscilador de três períodos | `uo()` |
| TSI | True Strength Index | `tsi()` |
| Awesome Oscillator | Diferença de duas médias | `ao()` |
| KST | Know Sure Thing | `kst()` |
| Fisher Transform | Identificação de extremos | `fisher()` |

### Volatilidade
| Indicador | Descrição | Código `pandas_ta` |
|-----------|-----------|-------------------|
| ATR | Average True Range | `atr()` |
| Bandas de Bollinger | Envoltória de volatilidade | `bbands()` |
| Keltner Channel | Canal baseado em ATR | `kc()` |
| Donchian Channel | Canal de breakout (máx./mín.) | `donchian()` |
| Bollinger %B / Width | Posição relativa e largura | `bbands()` (retorna `%b`, `width`) |
| Ulcer Index | Profundidade de drawdowns | `ui()` |
| Volatilidade Histórica | Desvio padrão anualizado | (customizado) |
| Garman‑Klass | Volatilidade usando OHLC | `pandas_ta.misc.garman_klass()` |

### Volume
| Indicador | Descrição | Código `pandas_ta` |
|-----------|-----------|-------------------|
| OBV | On‑Balance Volume | `obv()` |
| Volume Profile | Distribuição de volume por preço | (implementação customizada) |
| CMF | Chaikin Money Flow | `cmf()` |
| EOM | Ease of Movement | `eom()` |
| Force Index | Força combinando preço/volume | `efi()` |
| A/D Line | Acumulação/Distribuição | `ad()` |
| Volume RSI | RSI aplicado ao volume | `vrsi()` |

### Suporte / Resistência & Candlestick
| Indicador | Descrição | Implementação |
|-----------|-----------|----------------|
| Pivot Points (Clássico, Fibonacci, Camarilla) | Níveis baseados em OHLC anterior | Customizado |
| Padrões de Candlestick (Doji, Martelo, Engolfo, Estrela etc.) | Reconhecimento automático | `pandas_ta.cdl_pattern()` |
| ZigZag | Reversões significativas | `zigzag()` |
| Suporte/Resistência por clusters de volume | Zonas de interesse | Customizado (clusterização) |

### Estatísticos e Ciclos
| Indicador | Descrição | Código `pandas_ta` |
|-----------|-----------|-------------------|
| Z‑Score | Normalização do preço | `zscore()` |
| Skewness / Kurtosis | Assimetria e achatamento | `skew()`, `kurtosis()` |
| Regressão Linear | Inclinação e intercepto | `linreg()` |
| DPO | Detrended Price Oscillator | `dpo()` |
| Hilbert Sine Wave | Indicador de ciclo | `ht_sine()` |
| Mesa Sine Wave | Detecção de ciclos dominantes | `mesa()` |

---

## 🚀 FUNCIONALIDADES PRINCIPAIS (RESUMO)

- **Coleta de dados** – Yahoo Finance, Google Finance, Binance, Bybit, Pionex; criptomoedas, ações, forex, índices.  
- **+60 indicadores técnicos** – Cálculo otimizado com `pandas_ta` e ampla cobertura (tendência, momentum, volatilidade, volume, padrões).  
- **Modelos de previsão** – LSTM, Transformers temporais, XGBoost, Random Forest, modelos probabilísticos.  
- **Ensemble inteligente** – Stacking com votação ponderada dinâmica e autoavaliação de confiança.  
- **Aprendizado contínuo** – Online learning, retreino agendado, decaimento de relevância e memória vetorial.  
- **Evolução de estratégias** – Reinforcement Learning (PPO, SAC) e algoritmos genéticos.  
- **Execução autônoma** – Integração multi‑exchange com gerenciamento de estado e ordens avançadas.  
- **Gestão de risco adaptativa** – Stops dinâmicos, dimensionamento por Kelly, circuit breakers e perfis de risco.  
- **Dashboard interativo** – Interface Tkinter/Web, monitoramento do “cérebro”, gráficos e controles manuais.  
- **Arquitetura modular** – Componentes desacoplados facilitam customização, testes e expansão.

---

## 📋 REQUISITOS

### Principais
- Python 3.8+
- NumPy, Pandas, Matplotlib
- scikit-learn, joblib
- yfinance, pandas_ta
- PyYAML

### Opcionais (para funcionalidades avançadas)
- **TensorFlow** ou **PyTorch** – modelos LSTM/Transformers
- **Optuna** – para AutoML e tuning automático
- **Qiskit** – experimentos quânticos (funcionalidade experimental)
- **NetworkX** – visualização avançada da rede neural
- **Tkinter** – dashboard gráfico (geralmente incluso no Python; se ausente, sistema roda em modo console)

### Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/lextrader-iag.git
cd lextrader-iag

# Dependências obrigatórias
pip install numpy pandas matplotlib scikit-learn joblib yfinance pandas_ta pyyaml

# Para redes neurais profundas (escolha um)
pip install tensorflow
# ou
pip install torch

# Para otimização automática de hiperparâmetros
pip install optuna

# (Opcional) Para a interface web
pip install fastapi uvicorn jinja2
