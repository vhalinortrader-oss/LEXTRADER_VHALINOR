LEXTRADER-IAG 5.0  
Sistema Cerebral Artificial para o Mercado Financeiro VHALINOR 

**1. ANÁLISE MULTIDIMENSIONAL & GERAÇÃO DE SINAIS (Percepção)
Objetivo: Transformar dados brutos do mercado em uma representação unificada que alimenta as decisões.

1.1 Análise Técnica Clássica & Indicadores

Cálculo de mais de 60 indicadores (tendência, momentum, volatilidade, volume, ciclos, candlestick patterns) usando pandas_ta e funções customizadas.

Ex: Ichimoku Cloud, SuperTrend, ADX, Stochastic RSI, OBV, padrões de vela (Doji, Engolfo).

1.2 Análise de Ativos & Histórica

Coleta de dados OHLCV multi-timeframe (1m, 5m, 15m, 1h, 4h, 1d) via Yahoo Finance, APIs de corretoras (Binance, Bybit) e WebSocket em tempo real.

Armazenamento em banco de dados otimizado para séries temporais (InfluxDB, TimescaleDB) para consultas rápidas e treino contínuo.

1.3 Análise de Mercado & Contexto Macroeconômico

Integração com fontes de dados on-chain (para criptomoedas: fluxo de stablecoins, taxas de financiamento) e APIs de mercado tradicional (índices de medo/ganância, VIX).

Correlação entre ativos (matriz de correlação dinâmica) para identificar regimes de risco.

1.4 Análise de Padrões Gráficos & Candlestick

Reconhecimento automatizado de padrões harmônicos (Gartley, Borboleta), gráficos (cabeça-ombro, bandeiras, triângulos) e microestruturas de volume (Volume Profile, clusters).

Uso de algoritmos geométricos e redes neurais convolucionais (CNN) sobre imagens de velas ou diretamente sobre dados de preço/volume.

1.5 Análise de Notícias & Sentimento (NLP)

Coleta em tempo real de feeds de notícias (Reuters, CryptoPanic, Twitter/X) via APIs.

Processamento com modelos de linguagem (BERT financeiro, FinBERT) para classificação de sentimento (positivo/negativo/neutro) e extração de entidades (tickers, pessoas, eventos).

Geração de score de sentimento por ativo com janela temporal.

1.6 Revisão e Seleção dos Melhores Ativos (Top-Down Screening)

Módulo de ranking que pontua ativos com base em: força de tendência, volatilidade relativa, volume, sentimento, correlação e notícias.

Algoritmo de filtragem (como “Relative Strength Rotation Graph” adaptado) para elencar os 5–10 ativos com maior potencial para o dia/semana.

1.7 Neurônios Sensores Especializados

Cada grupo de análise (técnico, volume, sentimento, padrões) é encapsulado em um “neurônio sensor”, que gera uma saída padronizada (vetor de características) e uma medida de confiança.

Ex: Neurônio de Momentum produz score -1 a +1 baseado na combinação de RSI, Stoch, CCI; Neurônio de Sentimento retorna score de -1 a +1 com NLP.

2. APRENDIZADO DE MÁQUINA, EVOLUÇÃO E MEMÓRIA (Cognição)
Objetivo: Tomar decisões de trading a partir dos dados, aprender com erros e evoluir estratégias ao longo do tempo.

2.1 Modelos Preditivos Base (Núcleo de Previsão)

LSTM/GRU com atenção para previsão de direção do preço e volatilidade futura (horizontes: 15min, 1h, 4h).

Transformers temporais (Informer, Autoformer) para séries longas e captura de dependências complexas.

Gradient Boosting (XGBoost, LightGBM) como baseline robusto, treinado com features técnicas + sentimento.

Modelos probabilísticos (DeepAR, Gaussian Mixture Networks) para estimar distribuição de retornos.

2.2 Ensemble e Votação Inteligente

Stacking (meta-modelo) que combina previsões de LSTM, XGBoost e Random Forest usando uma camada final de regressão logística ou rede rasa.

Votação ponderada por desempenho recente (janela móvel de acurácia direcional ou Sharpe) para dar mais peso aos modelos que acertam mais no regime atual.

2.3 Aprendizado Contínuo & Adaptação Online

Online Learning: Modelos incrementais (Hoeffding Trees, River library) que se atualizam a cada novo candle sem retreino completo.

Retreino agendado (diário/semanal) em batch com dados rotulados automaticamente (ex: se um sinal de compra gerou lucro > 2% em 24h, rótulo positivo).

Decaimento de relevância: Amostras antigas recebem peso menor, para o sistema se adaptar rapidamente a mudanças de regime.

2.4 Evolução de Estratégias (Reinforcement Learning & Algoritmos Genéticos)

Reinforcement Learning (PPO, SAC): Agente treinado em ambiente simulado (backtest) para maximizar retorno ajustado ao risco; ações: comprar, vender, manter; estado: vetor de features + posição atual.

Algoritmos Genéticos: População de “indivíduos” (combinações de regras de entrada/saída, indicadores e parâmetros) que evoluem via crossover e mutação, selecionando os melhores por métricas de risco/retorno.

Bibliotecas: gym customizado, stable-baselines3, FinRL, DEAP para AG.

2.5 Aprendizagem de Estratégia por Imitação (Transfer Learning)

Extração de conhecimento de traders experientes: se disponível, logs de operações bem-sucedidas são usados para treinar um modelo de classificação que recomenda quando agir.

Uso de aprendizado por reforço a partir de demonstrações (RLfD).

2.6 Memória de Longo Prazo (Experiência)

“Córtex de memória” armazena estados de mercado passados (vetor de indicadores + resultado) para consulta por similaridade.

Ao enfrentar uma configuração atual, busca k-vizinhos mais próximos (usando FAISS ou Annoy) e recupera quais ações funcionaram naquele contexto.

A memória é podada periodicamente para evitar sobrecarga, mantendo apenas eventos de alta informação (grandes ganhos, perdas, reversões).

3. EXECUÇÃO AUTÔNOMA EM PLATAFORMAS DE TRADING (Ação)
Objetivo: Converter sinais em ordens reais (ou simuladas) com baixa latência e gerenciamento de estado.

3.1 Conectores para Exchanges (Binance, Bybit, Pionex, etc.)

Módulo padronizado de API REST e WebSocket para executar ordens, consultar saldo e posições.

Suporte a múltiplos tipos de ordem: limit, market, stop-limit, OCO (quando disponível).

Gerenciamento de sessão e reconexão automática.

3.2 Fila de Sinais e Orquestração

Todo sinal (ex: “compra BTC/USDT com 3% de capital”) é colocado em uma fila interna com timestamp.

Validador de consistência: verifica se não há conflito com posição atual, exposição máxima, intervalo mínimo entre trades.

3.3 Simulação e Paper Trading

Ambiente de backtest e trading simulado integrado, que usa dados reais e latência simulada para validar estratégias antes do deploy em real.

Métricas detalhadas (Sharpe, Max Drawdown, Win Rate) são computadas automaticamente.

3.4 Gerenciamento de Estado de Posição

Máquina de estados finita para cada ativo: IDLE → ENTRY → ACTIVE → PARTIAL_TP → EXIT.

Atualização em tempo real via WebSocket de ordens preenchidas, garantindo que o sistema sempre saiba o tamanho exato da posição, preço médio e PnL.

4. GESTÃO DE RISCO AUTÔNOMA (Preservação)
Objetivo: Proteger o capital e otimizar o dimensionamento das operações.

4.1 Stop-Loss e Take-Profit Dinâmicos

Cálculo baseado em ATR (ex: stop a 2x ATR, take a 3x ATR) ou em suporte/resistência identificados pelo ZigZag/Perfil de Volume.

Ajuste dinâmico ao longo da trade (trailing stop) usando Parabolic SAR, SuperTrend ou uma fração da volatilidade recente.

4.2 Dimensionamento de Posição Adaptativo (Risk Sizing)

Fórmula baseada no Critério de Kelly (fração ótima) ou em risco fixo por trade (ex: 1% do capital).

Ajusta o tamanho de acordo com a confiança do sinal (output do ensemble) e a volatilidade atual (regime de alta volatilidade = posição menor).

Considera correlação total do portfólio para evitar superexposição a um mesmo setor.

4.3 Circuit Breakers e Filtros de Exposição

Limite máximo de posições simultâneas (ex: 5).

Limite de drawdown diário/semanal: ao atingir -5% no dia, o sistema bloqueia novas entradas e reduz posições.

Detecção de notícias de alto impacto (ex: decisões de juros): bloqueio automático 30 min antes e depois.

4.4 Perfil de Risco Adaptável

O sistema opera em três modos selecionáveis (Conservador, Moderado, Agressivo), alterando parâmetros como % de risco, alavancagem máxima e proporção de ativos arriscados.

Um meta-gestor pode comutar dinamicamente entre perfis com base na volatilidade do mercado (VIX, ATR médio do portfólio).

4.5 Relatórios de Risco em Tempo Real

Cálculo contínuo de Value at Risk (VaR), Expected Shortfall (CVaR) e stress tests por cenário (queda repentina de 20%).

Exibição no dashboard para supervisão humana.

5. DASHBOARD INTERATIVO EM TEMPO REAL (Interface Humano-Máquina)
Objetivo: Fornecer transparência total sobre o “cérebro” e permitir monitoramento e intervenção manual.

5.1 Camada de Visualização (Tkinter / PyQt / Web via FastAPI+React)

Estrutura modular com abas: Visão Geral, Gráficos de Velas, Histórico de Trades, Previsões ao Vivo, Mapa de Calor do Cérebro.

Gráficos interativos com Plotly/Matplotlib: indicadores, nuvens de Ichimoku, zonas de suporte/resistência, e marcação dos pontos de entrada/saída.

5.2 Aba “Cérebro Neural”

Diagrama dinâmico que mostra a ativação dos neurônios especializados (Tendência, Volume, Sentimento) e o output combinado.

Barras de confiança e justificativa textual resumida (ex: “Compra sinalizada porque RSI < 30, Supertrend subiu e sentimento positivo”).

5.3 Monitor de Execução

Status em tempo real de todas as ordens ativas, posições abertas, P&L atualizado por trade.

Log de eventos com timestamp e alertas visuais (ex: stop-loss atingido, conexão com exchange perdida).

5.4 Controle Manual e Override

Botões para forçar encerramento de posição, pausar execução autônoma, ou mudar perfil de risco instantaneamente.

Slider para ajustar parâmetros como alavancagem máxima sem precisar alterar código.

5.5 Painel de Performance e Backtesting

Curvas de capital (equity curve), drawdown, retorno mensal, matriz de confusão dos modelos.

Funcionalidade de “replay” de mercado para depurar decisões em modo offline.

🔁 FLUXO DE DADOS RESUMIDO DA ARQUITETURA DE IA
Ingestão: Dados de mercado + notícias + on-chain → streams em tempo real.

Processamento Sensorial: Neurônios especializados calculam indicadores, sentimento, padrões.

Memória & Similaridade: Busca configurações históricas parecidas para contexto adicional.

Inferência Preditiva: Ensemble de modelos (LSTM, XGBoost, Transformer) gera previsão de direção e volatilidade.

Decisão Estratégica: RL + regras votam ação (comprar/vender/manter) e definem tamanho da posição.

Gestão de Risco: Ajusta tamanho, define stop/take dinâmicos, verifica limites de exposição.

Execução: Ordem é enviada à exchange via API; status monitorado até conclusão.

Feedback: Resultado é registrado na memória e usado para atualizar modelos (aprendizado contínuo) e para evolução das estratégias.


## 🚀 Funcionalidades Principais  

- **Coleta de dados financeiros** – Integração com Yahoo Finance (yfinance, Google Finance ) para cotações históricas e em tempo real de ações, criptomoedas, índices, forex e commodities.  
- ** Indicadores de Tendência
Indicador	Descrição	Código pandas_ta
SMA (Média Móvel Simples)	Já incluso – média de preços em N períodos.	sma()
EMA (Média Móvel Exponencial)	Já incluso – peso maior para preços recentes.	ema()
WMA (Média Móvel Ponderada)	Peso linear decrescente.	wma()
HMA (Hull Moving Average)	Extremamente suave, reduz atraso.	hma()
MACD	Já incluso – convergência/divergência de médias.	macd()
ADX (Average Directional Index)	Força da tendência (não direção).	adx()
+DI / -DI (Directional Indicators)	Direção da tendência.	adx() retorna DMP/DMN
Parabolic SAR	Pontos de reversão de tendência.	psar()
SuperTrend	Indicador de tendência baseado em ATR.	supertrend()
Ichimoku Cloud (Kumo)	Suporte/resistência, tendência e momentum.	ichimoku()
VWAP (Volume Weighted Avg Price)	Preço médio ponderado por volume (intradiário).	vwap()
KAMA (Kaufman Adaptive Moving Avg)	Adapta-se à volatilidade.	kama()
Triple EMA (TEMA)	Reduz ainda mais o atraso.	tema()
2. Indicadores de Momentum / Osciladores
Indicador	Descrição	Código pandas_ta
RSI (Relative Strength Index)	Já incluso – sobrecompra/venda.	rsi()
Stochastic ( %K, %D )	Já incluso – posição do fechamento em relação à máxima/mínima.	stoch()
Stochastic RSI	RSI do Stochastic, sinal mais rápido.	stochrsi()
Williams %R	Semelhante ao Stoch, mas invertido.	willr()
CCI (Commodity Channel Index)	Desvio do preço em relação à sua média.	cci()
MFI (Money Flow Index)	RSI ponderado por volume.	mfi()
Ultimate Oscillator	Combina três períodos para evitar divergências falsas.	uo()
TSI (True Strength Index)	Suaviza variações de preço para identificar tendências e reversões.	tsi()
Awesome Oscillator	Diferença entre duas médias móveis (pode usar ao()).	ao()
KST (Know Sure Thing)	Oscilador composto por várias taxas de variação suavizadas.	kst()
Fisher Transform	Transforma preços em uma curva gaussiana para identificar extremos.	fisher()
3. Indicadores de Volatilidade
Indicador	Descrição	Código pandas_ta
ATR (Average True Range)	Já incluso – volatilidade absoluta.	atr()
Bandas de Bollinger	Já incluso – envoltória de volatilidade.	bbands()
Keltner Channel	Canal baseado em ATR, semelhante a Bollinger.	kc()
Donchian Channel	Canal de máxima/mínima em N períodos (para breakout).	donchian()
Bollinger %B / Width	Posição relativa dentro das bandas e largura do canal.	bbands() retorna %b, width
Ulcer Index	Mede a profundidade e duração de drawdowns.	ui()
Historical Volatility (desvio padrão)	Volatilidade anualizada.	(customizado com std())
Garman-Klass Volatility	Estimativa de volatilidade usando OHLC.	(pode ser calculado via pandas_ta.misc.garman_klass())
4. Indicadores de Volume
Indicador	Descrição	Código pandas_ta
OBV (On-Balance Volume)	Soma/subtrai volume conforme direção do preço.	obv()
Volume Profile (não nativo, mas possível)	Distribuição de volume por preço.	(implementação customizada ou via volume_profile)
Chaikin Money Flow (CMF)	Fluxo de dinheiro em N períodos.	cmf()
Ease of Movement (EOM)	Facilidade de movimento do preço com base no volume.	eom()
Force Index	Combina preço e volume para medir força.	efi()
Accumulation/Distribution Line	Linha que relaciona fechamento e volume.	ad()
Volume RSI	RSI aplicado ao volume, não ao preço.	vrsi()
5. Indicadores de Suporte e Resistência / Candlestick
Indicador	Descrição	Implementação
Pivot Points (Clássico, Fibonacci, Camarilla)	Níveis calculados a partir de OHLC anterior.	Customizado ou bibliotecas como pivot_points
Padrões de Candlestick (Doji, Martelo, Engolfo, etc.)	Reconhecimento de padrões.	pandas_ta.cdl_pattern() (ex: cdl_doji()) – suporta dezenas de padrões.
ZigZag	Filtra movimentos menores, mostrando apenas reversões significativas.	zigzag()
Suporte/Resistência por clusters de volume	Identificação de zonas de interesse.	Customizado (agrupamento de perfil de volume)
6. Indicadores Estatísticos e de Ciclo
Indicador	Descrição	Código pandas_ta
Z-Score	Normalização do preço.	zscore()
Skewness / Kurtosis	Assimetria e achatamento da distribuição.	skew(), kurtosis()
Linear Regression	Inclinação e intercepto da regressão linear.	linreg()
Detrended Price Oscillator (DPO)	Remove tendência para identificar ciclos.	dpo()
Hilbert Transform (Sine Wave)	Indicador de ciclo – identifica fase e tendência.	ht_sine()
Cycles (Mesa Sine Wave, etc.)	Detecção de ciclos dominantes.	mesa()).  
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
