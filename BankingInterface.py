import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time
from enum import Enum

# ==================== CLASSES DE DADOS ====================
class TransferType(Enum):
    PROFIT_WITHDRAWAL = "PROFIT_WITHDRAWAL"
    DEPOSIT = "DEPOSIT"
    INTERNAL = "INTERNAL"

@dataclass
class BankAccount:
    id: str
    bankName: str
    agency: str
    accountNumber: str
    holderName: str
    pixKey: str = ""
    isDefault: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'bankName': self.bankName,
            'agency': self.agency,
            'accountNumber': self.accountNumber,
            'holderName': self.holderName,
            'pixKey': self.pixKey,
            'isDefault': self.isDefault,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

@dataclass
class BankTransfer:
    id: str
    amount: float
    type: TransferType
    date: datetime
    status: str
    description: str = ""
    source: str = "Corretora"
    destination: str = "Banco Pessoal"
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'type': self.type.value,
            'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
            'status': self.status,
            'description': self.description,
            'source': self.source,
            'destination': self.destination
        }

@dataclass
class FinancialSnapshot:
    totalApplications: float
    totalRealizedBank: float
    pendingTransfers: float
    availableWithdrawal: float
    lastUpdated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'totalApplications': self.totalApplications,
            'totalRealizedBank': self.totalRealizedBank,
            'pendingTransfers': self.pendingTransfers,
            'availableWithdrawal': self.availableWithdrawal,
            'lastUpdated': self.lastUpdated.strftime("%Y-%m-%d %H:%M:%S")
        }

@dataclass
class BankingConfig:
    autoTransferEnabled: bool = True
    profitThreshold: float = 1000.0
    transferPercentage: float = 50.0
    safetyCushion: float = 5000.0
    riskIntegration: bool = True
    maxDailyWithdrawal: float = 10000.0
    minTransferAmount: float = 100.0
    
    def to_dict(self):
        return {
            'autoTransferEnabled': self.autoTransferEnabled,
            'profitThreshold': self.profitThreshold,
            'transferPercentage': self.transferPercentage,
            'safetyCushion': self.safetyCushion,
            'riskIntegration': self.riskIntegration,
            'maxDailyWithdrawal': self.maxDailyWithdrawal,
            'minTransferAmount': self.minTransferAmount
        }

# ==================== SERVIÇO BANCÁRIO ====================
class BankingService:
    def __init__(self):
        self.accounts: List[BankAccount] = []
        self.transfer_history: List[BankTransfer] = []
        self.config = BankingConfig()
        self._initialize_data()
    
    def _initialize_data(self):
        """Inicializa com dados de exemplo"""
        if not self.accounts:
            self.accounts = [
                BankAccount(
                    id="acc1",
                    bankName="Nubank",
                    agency="0001",
                    accountNumber="12345-6",
                    holderName="João Silva",
                    pixKey="joao@email.com",
                    isDefault=True
                ),
                BankAccount(
                    id="acc2",
                    bankName="Itaú",
                    agency="1234",
                    accountNumber="987654-0",
                    holderName="João Silva",
                    isDefault=False
                )
            ]
        
        if not self.transfer_history:
            for i in range(10):
                self.transfer_history.append(
                    BankTransfer(
                        id=f"trans{i+1}",
                        amount=500 + random.random() * 2000,
                        type=TransferType.PROFIT_WITHDRAWAL,
                        date=datetime.now() - timedelta(days=random.randint(1, 30)),
                        status="COMPLETED",
                        description=f"Saque de lucro {i+1}"
                    )
                )
    
    def get_financial_snapshot(self) -> FinancialSnapshot:
        """Retorna snapshot financeiro atual"""
        total_apps = 125000 + random.random() * 25000  # Simula variação
        total_bank = 45000 + random.random() * 15000
        pending = sum(t.amount for t in self.transfer_history if t.status == "PENDING")
        
        return FinancialSnapshot(
            totalApplications=round(total_apps, 2),
            totalRealizedBank=round(total_bank, 2),
            pendingTransfers=round(pending, 2),
            availableWithdrawal=round(total_apps * 0.3, 2)  # 30% disponível para saque
        )
    
    def get_accounts(self) -> List[BankAccount]:
        """Retorna lista de contas"""
        return self.accounts
    
    def add_account(self, account_data: Dict[str, Any]) -> None:
        """Adiciona nova conta bancária"""
        if any(acc.isDefault for acc in self.accounts):
            # Desmarca conta padrão anterior se necessário
            for acc in self.accounts:
                if acc.isDefault:
                    acc.isDefault = False
        
        new_account = BankAccount(
            id=f"acc{len(self.accounts) + 1}",
            bankName=account_data['bankName'],
            agency=account_data.get('agency', ''),
            accountNumber=account_data['accountNumber'],
            holderName=account_data['holderName'],
            pixKey=account_data.get('pixKey', ''),
            isDefault=account_data.get('isDefault', True)
        )
        
        self.accounts.append(new_account)
    
    def request_transfer(self, amount: float, transfer_type: TransferType) -> bool:
        """Solicita transferência bancária"""
        if amount <= 0:
            raise ValueError("Valor deve ser positivo")
        
        # Verifica limite diário
        today = datetime.now().date()
        today_transfers = [
            t for t in self.transfer_history 
            if t.date.date() == today and t.status == "COMPLETED"
        ]
        today_total = sum(t.amount for t in today_transfers)
        
        if today_total + amount > self.config.maxDailyWithdrawal:
            raise ValueError(f"Limite diário excedido. Disponível: R$ {self.config.maxDailyWithdrawal - today_total:.2f}")
        
        # Cria transferência
        new_transfer = BankTransfer(
            id=f"trans{len(self.transfer_history) + 1}",
            amount=amount,
            type=transfer_type,
            date=datetime.now(),
            status="PENDING",
            description=f"Saque solicitado via sistema"
        )
        
        self.transfer_history.append(new_transfer)
        return True
    
    def simulate_profit(self, amount: float) -> None:
        """Simula lucro para testes"""
        # Adiciona ao histórico como transferência completa
        profit_transfer = BankTransfer(
            id=f"profit{len(self.transfer_history) + 1}",
            amount=amount,
            type=TransferType.PROFIT_WITHDRAWAL,
            date=datetime.now(),
            status="COMPLETED",
            description=f"Simulação de lucro: R$ {amount:.2f}"
        )
        self.transfer_history.append(profit_transfer)
    
    def update_config(self, config_data: Dict[str, Any]) -> None:
        """Atualiza configurações"""
        for key, value in config_data.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    @property
    def transferHistory(self) -> List[BankTransfer]:
        """Histórico de transferências ordenado por data"""
        return sorted(self.transfer_history, key=lambda x: x.date, reverse=True)

# ==================== APLICAÇÃO STREAMLIT ====================
def main():
    # Configuração da página
    st.set_page_config(
        page_title="Sistema Bancário Integrado",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Estilos CSS personalizados
    st.markdown("""
        <style>
        .main {
            background-color: #0a0a0a;
            color: #e5e5e5;
        }
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #111827 100%);
        }
        .balance-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .balance-card:hover {
            border-color: rgba(16, 185, 129, 0.3);
            transform: translateY(-2px);
        }
        .transfer-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1.5rem;
        }
        .account-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        .default-account {
            background-color: rgba(6, 78, 59, 0.2);
            border-color: rgba(16, 185, 129, 0.5);
        }
        .tab-button {
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: bold;
            font-size: 0.8rem;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .active-tab {
            background-color: #059669;
            color: white;
        }
        .inactive-tab {
            background-color: transparent;
            color: #9ca3af;
        }
        .inactive-tab:hover {
            color: white;
            background-color: rgba(255, 255, 255, 0.1);
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 48px;
            height: 24px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #374151;
            transition: .4s;
            border-radius: 24px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #059669;
        }
        input:checked + .slider:before {
            transform: translateX(24px);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar serviço bancário no estado da sessão
    if 'banking_service' not in st.session_state:
        st.session_state.banking_service = BankingService()
    
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'DASHBOARD'
    
    # Estado dos formulários
    if 'transfer_amount' not in st.session_state:
        st.session_state.transfer_amount = ''
    
    if 'new_account' not in st.session_state:
        st.session_state.new_account = {
            'bankName': '',
            'agency': '',
            'accountNumber': '',
            'holderName': '',
            'pixKey': ''
        }
    
    service = st.session_state.banking_service
    snapshot = service.get_financial_snapshot()
    accounts = service.get_accounts()
    history = service.transferHistory
    
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="padding: 0.5rem; background-color: rgba(6, 78, 59, 0.2); 
                         border-radius: 0.5rem; border: 1px solid rgba(16, 185, 129, 0.5);">
                    <span style="color: #10b981; font-size: 1.5rem;">🏦</span>
                </div>
                <div>
                    <h1 style="color: white; margin: 0; font-size: 1.5rem;">SISTEMA BANCÁRIO INTEGRADO</h1>
                    <p style="color: #10b981; font-family: monospace; font-size: 0.8rem; margin: 0;">
                        GESTÃO DE PATRIMÔNIO • TRANSFERÊNCIAS • RISCO
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Tabs de navegação
        tabs_html = """
        <div style="display: flex; background-color: black; border: 1px solid #374151; 
                    border-radius: 0.25rem; padding: 0.25rem; margin-top: 1rem;">
        """
        
        for tab in ['DASHBOARD', 'ACCOUNTS', 'SETTINGS']:
            is_active = st.session_state.active_tab == tab
            tabs_html += f"""
                <button onclick="window.parent.postMessage({{'type': 'streamlit:setComponentValue', 
                'value': '{tab}'}}, '*')" 
                class="tab-button {'active-tab' if is_active else 'inactive-tab'}" 
                style="flex: 1; margin: 0 0.125rem;">
                    {tab}
                </button>
            """
        
        tabs_html += "</div>"
        st.markdown(tabs_html, unsafe_allow_html=True)
        
        # JavaScript para comunicação com Streamlit
        st.markdown("""
            <script>
            window.addEventListener('message', function(event) {
                if (event.data.type === 'streamlit:setComponentValue') {
                    Streamlit.setComponentValue(event.data.value);
                }
            });
            </script>
        """, unsafe_allow_html=True)
        
        # Criar um placeholder para capturar os cliques
        tab_clicked = st.empty()
        if tab_clicked.button("", key="tab_trigger", label_visibility="collapsed"):
            pass
    
    st.divider()
    
    # Conteúdo baseado na tab ativa
    if st.session_state.active_tab == 'DASHBOARD':
        render_dashboard(snapshot, accounts, history, service)
    elif st.session_state.active_tab == 'ACCOUNTS':
        render_accounts_tab(accounts, service)
    elif st.session_state.active_tab == 'SETTINGS':
        render_settings_tab(service)
    
    # Atualização automática
    time.sleep(5)
    st.rerun()

def render_dashboard(snapshot: FinancialSnapshot, accounts: List[BankAccount], 
                     history: List[BankTransfer], service: BankingService):
    """Renderiza a tab Dashboard"""
    
    # Cards de saldo
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="balance-card">
                <div style="position: absolute; top: 0; right: 0; padding: 1rem; opacity: 0.1;">
                    <span style="font-size: 3rem;">📈</span>
                </div>
                <div style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; 
                          font-weight: bold; margin-bottom: 0.5rem;">
                    Saldo Total (Aplicações)
                </div>
                <div style="font-family: monospace; font-size: 2rem; font-weight: bold; color: white;
                          transition: color 0.3s ease;">
                    R$ {snapshot.totalApplications:,.2f}
                </div>
                <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 0.5rem; display: flex; align-items: center; gap: 0.25rem;">
                    <span style="color: #10b981;">✓</span> Capital em Risco na Corretora
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="balance-card">
                <div style="position: absolute; top: 0; right: 0; padding: 1rem; opacity: 0.1;">
                    <span style="font-size: 3rem;">🏦</span>
                </div>
                <div style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; 
                          font-weight: bold; margin-bottom: 0.5rem;">
                    Saldo Real (Banco Pessoal)
                </div>
                <div style="font-family: monospace; font-size: 2rem; font-weight: bold; color: #10b981;
                          transition: color 0.3s ease;">
                    R$ {snapshot.totalRealizedBank:,.2f}
                </div>
                <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 0.5rem; display: flex; align-items: center; gap: 0.25rem;">
                    <span style="color: #10b981;">✓</span> Lucro Realizado e Seguro
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="balance-card">
                <div style="position: absolute; top: 0; right: 0; padding: 1rem; opacity: 0.1;">
                    <span style="font-size: 3rem;">⏳</span>
                </div>
                <div style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; 
                          font-weight: bold; margin-bottom: 0.5rem;">
                    Transferências Pendentes
                </div>
                <div style="font-family: monospace; font-size: 2rem; font-weight: bold; color: #fbbf24;">
                    R$ {snapshot.pendingTransfers:,.2f}
                </div>
                <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 0.5rem;">
                    Processamento em andamento...
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Transferência rápida e gráfico
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
            <div class="transfer-card">
                <h3 style="color: white; font-size: 0.9rem; font-weight: bold; margin-bottom: 1rem; 
                          display: flex; align-items: center; gap: 0.5rem;">
                    <span>↔️</span> TRANSFERÊNCIA RÁPIDA
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulário de transferência
        transfer_amount = st.text_input(
            "Valor (R$)",
            value=st.session_state.transfer_amount,
            key="transfer_input",
            placeholder="0.00"
        )
        
        default_account = next((acc for acc in accounts if acc.isDefault), None)
        if default_account:
            st.markdown(f"""
                <div style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.5rem;">
                    Destino: <span style="color: white; font-weight: bold;">{default_account.bankName}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("💳 SOLICITAR SAQUE", use_container_width=True, type="primary"):
            if transfer_amount:
                try:
                    amount = float(transfer_amount)
                    if amount > 0:
                        service.request_transfer(amount, TransferType.PROFIT_WITHDRAWAL)
                        st.success("Transferência solicitada com sucesso!")
                        st.session_state.transfer_amount = ''
                        st.rerun()
                    else:
                        st.error("Valor deve ser positivo")
                except ValueError as e:
                    st.error(f"Erro: {e}")
            else:
                st.warning("Digite um valor para transferência")
        
        st.markdown("""
            <div style="font-size: 0.7rem; color: #fbbf24; margin-top: 1rem; padding: 0.5rem;
                      background-color: rgba(251, 191, 36, 0.1); border-radius: 0.25rem;
                      display: flex; align-items: start; gap: 0.5rem;">
                <span style="font-size: 0.8rem;">⚠️</span>
                Sujeito à aprovação do Gerenciador de Risco Autônomo.
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="transfer-card" style="height: 100%;">
                <h3 style="color: white; font-size: 0.9rem; font-weight: bold; margin-bottom: 1rem; 
                          display: flex; align-items: center; gap: 0.5rem;">
                    <span>📈</span> HISTÓRICO DE SAQUES
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Gráfico de histórico
        chart_data = []
        for transfer in history[:10]:  # Últimas 10 transferências
            chart_data.append({
                'date': transfer.date.strftime('%d/%m'),
                'amount': transfer.amount,
                'type': transfer.type.value
            })
        
        if chart_data:
            df = pd.DataFrame(chart_data)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=df['date'],
                    y=df['amount'],
                    marker_color='#10b981',
                    text=df['amount'].apply(lambda x: f'R$ {x:,.0f}'),
                    textposition='auto',
                    name='Valor'
                )
            ])
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis_title="Data",
                yaxis_title="Valor (R$)",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma transferência registrada ainda.")
    
    # Botão de debug (simular lucro)
    if st.button("[DEBUG] Simular Lucro (+R$500)", type="secondary", use_container_width=False):
        service.simulate_profit(500)
        st.success("Lucro simulado com sucesso!")
        st.rerun()

def render_accounts_tab(accounts: List[BankAccount], service: BankingService):
    """Renderiza a tab de Contas"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Contas Cadastradas")
        
        if not accounts:
            st.info("Nenhuma conta cadastrada.")
        else:
            for acc in accounts:
                card_class = "account-card default-account" if acc.isDefault else "account-card"
                
                st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="padding: 0.5rem; background-color: #374151; border-radius: 50%;">
                                    <span style="color: white;">🏦</span>
                                </div>
                                <div>
                                    <h4 style="color: white; margin: 0; font-weight: bold;">{acc.bankName}</h4>
                                    <p style="font-size: 0.8rem; color: #9ca3af; margin: 0.25rem 0; font-family: monospace;">
                                        AG: {acc.agency} | CC: {acc.accountNumber}
                                    </p>
                                    <p style="font-size: 0.8rem; color: #9ca3af; margin: 0;">{acc.holderName}</p>
                                </div>
                            </div>
                            {f'<span style="font-size: 0.7rem; background-color: #10b981; color: black; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-weight: bold;">PADRÃO</span>' if acc.isDefault else ''}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botões para cada conta
                cols = st.columns(2)
                with cols[0]:
                    if st.button(f"Tornar Padrão", key=f"default_{acc.id}", use_container_width=True):
                        for a in accounts:
                            a.isDefault = False
                        acc.isDefault = True
                        st.rerun()
                
                with cols[1]:
                    if st.button(f"Remover", key=f"remove_{acc.id}", type="secondary", use_container_width=True):
                        if len(accounts) > 1 or not acc.isDefault:
                            service.accounts.remove(acc)
                            st.rerun()
                        else:
                            st.error("Não é possível remover a única conta padrão")
    
    with col2:
        st.subheader("➕ Cadastrar Nova Conta")
        
        with st.form("new_account_form"):
            new_bank = st.text_input("Nome do Banco*", 
                                    value=st.session_state.new_account['bankName'],
                                    placeholder="Ex: Nubank, Itaú...")
            
            col1, col2 = st.columns(2)
            with col1:
                new_agency = st.text_input("Agência*", 
                                         value=st.session_state.new_account['agency'],
                                         placeholder="0001")
            
            with col2:
                new_account_num = st.text_input("Conta*", 
                                              value=st.session_state.new_account['accountNumber'],
                                              placeholder="12345-6")
            
            new_holder = st.text_input("Nome do Titular*", 
                                     value=st.session_state.new_account['holderName'],
                                     placeholder="João Silva")
            
            new_pix = st.text_input("Chave PIX (Opcional)", 
                                  value=st.session_state.new_account['pixKey'],
                                  placeholder="joao@email.com ou telefone")
            
            set_default = st.checkbox("Definir como conta padrão", value=len(accounts) == 0)
            
            if st.form_submit_button("💾 SALVAR CONTA", type="primary", use_container_width=True):
                if new_bank and new_account_num and new_holder:
                    account_data = {
                        'bankName': new_bank,
                        'agency': new_agency,
                        'accountNumber': new_account_num,
                        'holderName': new_holder,
                        'pixKey': new_pix,
                        'isDefault': set_default
                    }
                    
                    service.add_account(account_data)
                    
                    # Limpar formulário
                    st.session_state.new_account = {
                        'bankName': '',
                        'agency': '',
                        'accountNumber': '',
                        'holderName': '',
                        'pixKey': ''
                    }
                    
                    st.success("Conta cadastrada com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha os campos obrigatórios (*)")

def render_settings_tab(service: BankingService):
    """Renderiza a tab de Configurações"""
    
    st.subheader("⚙️ Automação de Risco & Transferência")
    
    with st.container():
        # Switch para transferência automática
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
                <div style="padding: 1rem; background-color: rgba(0,0,0,0.4); 
                          border-radius: 0.5rem; border: 1px solid #374151;">
                    <div style="font-size: 0.9rem; font-weight: bold; color: white;">
                        Transferência Automática
                    </div>
                    <div style="font-size: 0.8rem; color: #9ca3af;">
                        Enviar lucros automaticamente para o banco
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            auto_transfer = st.toggle("", 
                                     value=service.config.autoTransferEnabled,
                                     key="auto_transfer_toggle",
                                     label_visibility="collapsed")
            
            if auto_transfer != service.config.autoTransferEnabled:
                service.config.autoTransferEnabled = auto_transfer
        
        st.divider()
        
        # Configurações numéricas
        col1, col2 = st.columns(2)
        
        with col1:
            profit_threshold = st.number_input(
                "Gatilho de Lucro (R$)*",
                min_value=0.0,
                value=float(service.config.profitThreshold),
                step=100.0,
                help="Transfere quando o lucro atingir este valor."
            )
            
            if profit_threshold != service.config.profitThreshold:
                service.config.profitThreshold = profit_threshold
        
        with col2:
            transfer_percentage = st.number_input(
                "% a Transferir*",
                min_value=0.0,
                max_value=100.0,
                value=float(service.config.transferPercentage),
                step=5.0,
                help="Porcentagem do lucro a ser enviada."
            )
            
            if transfer_percentage != service.config.transferPercentage:
                service.config.transferPercentage = transfer_percentage
        
        # Margem de segurança
        safety_cushion = st.number_input(
            "Margem de Segurança (R$)*",
            min_value=0.0,
            value=float(service.config.safetyCushion),
            step=500.0,
            help="Valor mínimo a manter na corretora para operações."
        )
        
        if safety_cushion != service.config.safetyCushion:
            service.config.safetyCushion = safety_cushion
        
        # Integração com gerenciador de risco
        risk_integration = st.checkbox(
            "Integração com Gerenciador de Risco AGI",
            value=service.config.riskIntegration,
            help="Bloqueia saques em alta volatilidade"
        )
        
        if risk_integration != service.config.riskIntegration:
            service.config.riskIntegration = risk_integration
        
        # Botão salvar
        if st.button("💾 SALVAR PREFERÊNCIAS", type="primary", use_container_width=True):
            # As alterações já foram salvas em tempo real
            st.success("Configurações salvas com sucesso!")

# Handler para troca de tabs
def handle_tab_change():
    """Manipula mudança de tabs via JavaScript"""
    try:
        # Tentar capturar valor do JavaScript
        return st.session_state.get('tab_change', 'DASHBOARD')
    except:
        return 'DASHBOARD'

if __name__ == "__main__":
    main()