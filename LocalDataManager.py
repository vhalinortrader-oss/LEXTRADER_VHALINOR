import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import time
import threading
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass

@dataclass
class DataComponent:
    """Estrutura para componentes de dados"""
    name: str
    size: float  # MB
    description: str
    icon: str

class LocalDataManagerApp:
    """Aplicação principal que replica a funcionalidade do componente React LocalDataManager"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("💾 Gerenciador de Dados Local")
        self.root.geometry("800x700")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação (equivalente aos useState hooks)
        self.selected_path = ""
        self.is_saving = False
        self.save_progress = 0
        self.last_backup: Optional[datetime] = None
        
        # Dados simulados (equivalente aos dataSize e dataComponents)
        self.data_size = {
            'trading': 125.4,
            'neural': 89.7,
            'settings': 2.1,
            'logs': 45.8,
            'total': 262.9
        }
        
        self.data_components = [
            DataComponent(
                name='Dados de Trading',
                size=self.data_size['trading'],
                description='Histórico de operações, posições e análises',
                icon='📈'
            ),
            DataComponent(
                name='Modelos Neural',
                size=self.data_size['neural'],
                description='Redes neurais treinadas e algoritmos de IA',
                icon='🗄️'
            ),
            DataComponent(
                name='Configurações',
                size=self.data_size['settings'],
                description='Preferências pessoais e parâmetros do sistema',
                icon='⚙️'
            ),
            DataComponent(
                name='Logs e Relatórios',
                size=self.data_size['logs'],
                description='Histórico de atividades e relatórios de performance',
                icon='📄'
            )
        ]
        
        # Widgets que precisam ser atualizados
        self.path_display_frame = None
        self.save_button = None
        self.progress_frame = None
        self.progress_bar = None
        self.progress_label = None
        self.backup_info_frame = None
        
        # Configurar estilos
        self.setup_styles()
        
        # Configurar interface
        self.setup_ui()
    
    def setup_styles(self) -> None:
        """Configurar estilos customizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Primary.TButton', 
                       background='#3b82f6', 
                       foreground='white',
                       focuscolor='none')
        
        style.configure('Success.TLabel', foreground='#10b981')
        style.configure('Warning.TLabel', foreground='#f59e0b')
        style.configure('Error.TLabel', foreground='#ef4444')
        style.configure('Muted.TLabel', foreground='#6b7280')
        
        style.configure('Card.TFrame', 
                       background='white', 
                       relief='solid',
                       borderwidth=1)
    
    # Função principal de seleção de pasta (equivalente a handleSelectFolder)
    def handle_select_folder(self) -> None:
        """Selecionar pasta para backup (equivalente a handleSelectFolder)"""
        try:
            # Usar filedialog para seleção de pasta
            folder_path = filedialog.askdirectory(
                title='Selecionar pasta para salvar dados do LEXTRADER ASI',
                initialdir=os.path.expanduser('~')
            )
            
            if folder_path:
                # Criar subpasta específica para o backup
                backup_folder = os.path.join(folder_path, 'LEXTRADER-ASI-Backup')
                self.selected_path = backup_folder
                
                self.update_path_display()
                self.show_toast("Pasta selecionada", f"Dados serão salvos em: {backup_folder}")
            
        except Exception as e:
            self.show_toast("Erro", "Não foi possível selecionar a pasta", "error")
    
    # Função principal de salvamento (equivalente a handleSaveData)
    def handle_save_data(self) -> None:
        """Salvar dados com progresso (equivalente a handleSaveData)"""
        if not self.selected_path:
            self.show_toast("Erro", "Selecione uma pasta primeiro", "error")
            return
        
        self.is_saving = True
        self.save_progress = 0
        self.update_save_button()
        self.show_progress_frame()
        
        # Executar salvamento em thread separada
        save_thread = threading.Thread(target=self._save_worker, daemon=True)
        save_thread.start()
    
    def _save_worker(self) -> None:
        """Worker thread para simulação de salvamento"""
        try:
            # Etapas do salvamento (equivalente ao array steps)
            steps = [
                {'name': 'Configurações do sistema', 'progress': 10},
                {'name': 'Dados de trading históricos', 'progress': 30},
                {'name': 'Modelos de IA neural', 'progress': 60},
                {'name': 'Logs e relatórios', 'progress': 80},
                {'name': 'Compactando arquivos', 'progress': 95},
                {'name': 'Finalizando backup', 'progress': 100}
            ]
            
            for step in steps:
                time.sleep(0.8)  # Simular tempo de processamento
                self.save_progress = step['progress']
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_progress_display)
                self.root.after(0, lambda s=step['name']: self.show_toast("Salvando...", s))
            
            # Criar estrutura de dados de backup
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'dataSize': self.data_size['total'],
                'path': self.selected_path,
                'components': {
                    'tradingData': 'Histórico de operações e posições',
                    'neuralModels': 'Modelos treinados de IA',
                    'settings': 'Configurações personalizadas',
                    'logs': 'Logs do sistema e análises'
                }
            }
            
            # Criar pasta se não existir
            os.makedirs(self.selected_path, exist_ok=True)
            
            # Salvar arquivo de backup (simulado)
            backup_file = os.path.join(self.selected_path, 'backup_info.json')
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            # Finalizar backup
            self.last_backup = datetime.now()
            self.root.after(0, self.finish_save_success)
            
        except Exception as e:
            self.root.after(0, lambda: self.finish_save_error(str(e)))
    
    def finish_save_success(self) -> None:
        """Finalizar salvamento com sucesso"""
        self.is_saving = False
        self.save_progress = 0
        self.update_save_button()
        self.hide_progress_frame()
        self.update_backup_info()
        
        self.show_toast("Backup concluído!", 
                       f"{self.data_size['total']}MB salvos com sucesso")
    
    def finish_save_error(self, error: str) -> None:
        """Finalizar salvamento com erro"""
        self.is_saving = False
        self.save_progress = 0
        self.update_save_button()
        self.hide_progress_frame()
        
        self.show_toast("Erro no backup", f"Não foi possível completar o backup: {error}", "error")
    
    def handle_restore_data(self) -> None:
        """Restaurar dados de backup"""
        try:
            backup_file = filedialog.askopenfilename(
                title='Selecionar arquivo de backup',
                filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
            )
            
            if backup_file:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                
                self.show_toast("Restore simulado", 
                               f"Dados de {backup_data.get('timestamp', 'data desconhecida')} carregados")
        
        except Exception as e:
            self.show_toast("Erro na restauração", f"Não foi possível restaurar: {e}", "error")
    
    # Configuração da interface gráfica
    def setup_ui(self) -> None:
        """Configurar interface principal"""
        # Frame principal com scroll
        main_canvas = tk.Canvas(self.root, bg='#f8fafc')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Container principal
        container = ttk.Frame(scrollable_frame, padding="20", style='Card.TFrame')
        container.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=20, pady=20)
        
        # Cabeçalho
        self.setup_header(container)
        
        # Seleção de pasta
        self.setup_folder_selection(container)
        
        # Visão geral dos dados
        self.setup_data_overview(container)
        
        # Frame de progresso (inicialmente oculto)
        self.setup_progress_section(container)
        
        # Botões de ação
        self.setup_action_buttons(container)
        
        # Informações de backup
        self.setup_backup_info(container)
        
        # Notas importantes
        self.setup_important_notes(container)
        
        # Configurar scroll
        main_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        scrollable_frame.columnconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
    
    def setup_header(self, parent: ttk.Frame) -> None:
        """Configurar cabeçalho"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Título com ícone
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(title_frame, text="💾", font=("Arial", 18)).grid(row=0, column=0, padx=(0, 8))
        ttk.Label(title_frame, text="Gerenciador de Dados Local", 
                 font=("Arial", 18, "bold")).grid(row=0, column=1)
        
        # Descrição
        desc_label = tk.Label(header_frame, 
                             text="Salve todos os dados do LEXTRADER ASI em uma pasta no seu computador",
                             font=("Arial", 10), fg="#6b7280", bg="white")
        desc_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        header_frame.columnconfigure(0, weight=1)
    
    def setup_folder_selection(self, parent: ttk.Frame) -> None:
        """Configurar seção de seleção de pasta"""
        folder_section = ttk.Frame(parent)
        folder_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Título da seção
        ttk.Label(folder_section, text="Pasta de Destino", 
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Botão de seleção
        select_button = tk.Button(folder_section, 
                                 text="📁 Selecionar Pasta",
                                 bg="white", fg="#6b7280",
                                 font=("Arial", 10, "bold"),
                                 relief='solid', borderwidth=1,
                                 padx=15, pady=8,
                                 cursor="hand2",
                                 command=self.handle_select_folder)
        select_button.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Frame para exibir pasta selecionada
        self.path_display_frame = ttk.Frame(folder_section)
        
        folder_section.columnconfigure(0, weight=1)
    
    def setup_data_overview(self, parent: ttk.Frame) -> None:
        """Configurar visão geral dos dados"""
        data_section = ttk.Frame(parent)
        data_section.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Header da seção
        header_frame = ttk.Frame(data_section)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(header_frame, text="Dados para Backup", 
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W)
        
        total_badge = tk.Label(header_frame, text=f"Total: {self.data_size['total']}MB",
                              bg="#f1f5f9", fg="#6b7280", font=("Arial", 8, "bold"),
                              padx=6, pady=2)
        total_badge.grid(row=0, column=1, sticky=tk.E)
        
        header_frame.columnconfigure(0, weight=1)
        
        # Grid de componentes
        components_grid = ttk.Frame(data_section)
        components_grid.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        for i, component in enumerate(self.data_components):
            row = i // 2
            col = i % 2
            
            self.create_component_card(components_grid, component, row, col)
        
        # Configurar grid
        components_grid.columnconfigure(0, weight=1)
        components_grid.columnconfigure(1, weight=1)
        
        data_section.columnconfigure(0, weight=1)
    
    def create_component_card(self, parent: ttk.Frame, component: DataComponent, 
                            row: int, col: int) -> None:
        """Criar card de componente de dados"""
        card = tk.Frame(parent, bg="#f8fafc", relief='solid', borderwidth=1)
        card.grid(row=row, column=col, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        card_content = tk.Frame(card, bg="#f8fafc")
        card_content.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        # Header com ícone e info
        header_frame = tk.Frame(card_content, bg="#f8fafc")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Ícone
        ttk.Label(header_frame, text=component.icon, font=("Arial", 14)).grid(row=0, column=0, padx=(0, 8))
        
        # Info frame
        info_frame = tk.Frame(header_frame, bg="#f8fafc")
        info_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Nome e tamanho
        name_size_frame = tk.Frame(info_frame, bg="#f8fafc")
        name_size_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(name_size_frame, text=component.name, 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        
        size_label = tk.Label(name_size_frame, text=f"{component.size}MB",
                             bg="#f8fafc", fg="#6b7280", font=("Arial", 8))
        size_label.grid(row=0, column=1, sticky=tk.E)
        
        name_size_frame.columnconfigure(0, weight=1)
        
        # Descrição
        desc_label = tk.Label(info_frame, text=component.description,
                             bg="#f8fafc", fg="#6b7280", font=("Arial", 8),
                             wraplength=200, justify=tk.LEFT)
        desc_label.grid(row=1, column=0, sticky=tk.W)
        
        info_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        card_content.columnconfigure(0, weight=1)
        card.columnconfigure(0, weight=1)
    
    def setup_progress_section(self, parent: ttk.Frame) -> None:
        """Configurar seção de progresso"""
        self.progress_frame = ttk.Frame(parent)
        
        # Título do progresso
        progress_header = ttk.Frame(self.progress_frame)
        progress_header.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        self.progress_label = tk.Label(progress_header, text="Salvando dados...",
                                      font=("Arial", 10, "bold"), bg="white")
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_percentage = tk.Label(progress_header, text="0%",
                                           bg="white", fg="#6b7280", font=("Arial", 10))
        self.progress_percentage.grid(row=0, column=1, sticky=tk.E)
        
        progress_header.columnconfigure(0, weight=1)
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=600, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.progress_frame.columnconfigure(0, weight=1)
    
    def setup_action_buttons(self, parent: ttk.Frame) -> None:
        """Configurar botões de ação"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Botão salvar
        self.save_button = tk.Button(buttons_frame, 
                                    text="💾 Salvar Dados",
                                    bg="#3b82f6", fg="white",
                                    font=("Arial", 12, "bold"),
                                    padx=20, pady=10,
                                    cursor="hand2",
                                    command=self.handle_save_data)
        self.save_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botão restaurar
        restore_button = tk.Button(buttons_frame, 
                                  text="📤 Restaurar",
                                  bg="white", fg="#6b7280",
                                  font=("Arial", 12, "bold"),
                                  relief='solid', borderwidth=1,
                                  padx=20, pady=10,
                                  cursor="hand2",
                                  command=self.handle_restore_data)
        restore_button.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
    
    def setup_backup_info(self, parent: ttk.Frame) -> None:
        """Configurar informações de backup"""
        self.backup_info_frame = ttk.Frame(parent)
    
    def setup_important_notes(self, parent: ttk.Frame) -> None:
        """Configurar notas importantes"""
        notes_frame = tk.Frame(parent, bg="#fef3c7", relief='solid', borderwidth=1)
        notes_frame.grid(row=6, column=0, sticky=(tk.W, tk.E))
        
        notes_content = tk.Frame(notes_frame, bg="#fef3c7")
        notes_content.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=15, pady=12)
        
        # Header
        header_frame = tk.Frame(notes_content, bg="#fef3c7")
        header_frame.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        ttk.Label(header_frame, text="⚠️", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 8))
        notes_title = tk.Label(header_frame, text="Importante:",
                              bg="#fef3c7", fg="#92400e", font=("Arial", 10, "bold"))
        notes_title.grid(row=0, column=1)
        
        # Lista de notas
        notes_list = [
            "• Os dados salvos incluem configurações pessoais e modelos de IA treinados",
            "• Mantenha o backup em local seguro - contém informações sensíveis",
            "• Para transferir para outro computador, use a função 'Restaurar'",
            "• Recomendamos backup semanal para preservar o progresso do sistema"
        ]
        
        for note in notes_list:
            note_label = tk.Label(notes_content, text=note, bg="#fef3c7", 
                                 fg="#78350f", font=("Arial", 9), justify=tk.LEFT)
            note_label.grid(row=len(notes_list) + 1, column=0, sticky=tk.W, pady=1)
        
        notes_content.columnconfigure(0, weight=1)
        notes_frame.columnconfigure(0, weight=1)
    
    # Funções de atualização da UI
    def update_path_display(self) -> None:
        """Atualizar display da pasta selecionada"""
        if self.path_display_frame:
            self.path_display_frame.destroy()
        
        if self.selected_path:
            self.path_display_frame = tk.Frame(self.path_display_frame.master, 
                                              bg="#dbeafe", relief='solid', borderwidth=1)
            self.path_display_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
            
            content = tk.Frame(self.path_display_frame, bg="#dbeafe")
            content.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=12, pady=10)
            
            # Header
            header = tk.Frame(content, bg="#dbeafe")
            header.grid(row=0, column=0, sticky=tk.W)
            
            ttk.Label(header, text="✅", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
            header_text = tk.Label(header, text="Pasta selecionada:",
                                  bg="#dbeafe", font=("Arial", 10, "bold"))
            header_text.grid(row=0, column=1)
            
            # Caminho
            path_label = tk.Label(content, text=self.selected_path,
                                 bg="#dbeafe", fg="#1e40af", font=("Consolas", 9))
            path_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
            
            content.columnconfigure(0, weight=1)
            self.path_display_frame.columnconfigure(0, weight=1)
    
    def update_save_button(self) -> None:
        """Atualizar botão de salvamento"""
        if self.save_button:
            if self.is_saving:
                self.save_button.config(text="💾 Salvando...", state="disabled", bg="#9ca3af")
            else:
                enabled = bool(self.selected_path)
                self.save_button.config(text="💾 Salvar Dados", 
                                       state="normal" if enabled else "disabled",
                                       bg="#3b82f6" if enabled else "#9ca3af")
    
    def show_progress_frame(self) -> None:
        """Mostrar frame de progresso"""
        if self.progress_frame:
            self.progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
    
    def hide_progress_frame(self) -> None:
        """Ocultar frame de progresso"""
        if self.progress_frame:
            self.progress_frame.grid_remove()
    
    def update_progress_display(self) -> None:
        """Atualizar display de progresso"""
        if self.progress_bar and self.progress_percentage:
            self.progress_bar['value'] = self.save_progress
            self.progress_percentage.config(text=f"{self.save_progress}%")
    
    def update_backup_info(self) -> None:
        """Atualizar informações de backup"""
        if self.backup_info_frame:
            self.backup_info_frame.destroy()
        
        if self.last_backup:
            parent = self.backup_info_frame.master
            self.backup_info_frame = tk.Frame(parent, bg="#dcfce7", relief='solid', borderwidth=1)
            self.backup_info_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
            
            content = tk.Frame(self.backup_info_frame, bg="#dcfce7")
            content.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=12, pady=10)
            
            # Header
            header = tk.Frame(content, bg="#dcfce7")
            header.grid(row=0, column=0, sticky=tk.W)
            
            ttk.Label(header, text="✅", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
            header_text = tk.Label(header, text="Último backup:",
                                  bg="#dcfce7", fg="#15803d", font=("Arial", 10, "bold"))
            header_text.grid(row=0, column=1)
            
            # Informações
            backup_text = f"{self.last_backup.strftime('%d/%m/%Y %H:%M:%S')} - {self.data_size['total']}MB salvos"
            info_label = tk.Label(content, text=backup_text,
                                 bg="#dcfce7", fg="#166534", font=("Arial", 9))
            info_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
            
            content.columnconfigure(0, weight=1)
            self.backup_info_frame.columnconfigure(0, weight=1)
    
    def show_toast(self, title: str, message: str, type: str = "info") -> None:
        """Mostrar notificação toast (equivalente ao toast do React)"""
        if type == "error":
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

def main() -> None:
    """Função principal para executar a aplicação"""
    root = tk.Tk()
    app = LocalDataManagerApp(root)
    
    # Tornar a janela responsiva
    root.minsize(700, 600)
    
    # Centralizar janela
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()
