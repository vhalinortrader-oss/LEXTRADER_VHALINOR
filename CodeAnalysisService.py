import os
import json
import time
import random
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import re
import ast
import hashlib

# --- TIPOS & INTERFACES ---

class CodeAnalysisType(Enum):
    """Tipos de análise de código"""
    CORRECTION = "CORRECTION"
    OPTIMIZATION = "OPTIMIZATION"
    TRANSLATION = "TRANSLATION"
    DOCUMENTATION = "DOCUMENTATION"
    SECURITY = "SECURITY"
    DEBUG = "DEBUG"
    TEST_GENERATION = "TEST_GENERATION"
    ARCHITECTURE_REVIEW = "ARCHITECTURE_REVIEW"
    PERFORMANCE_ANALYSIS = "PERFORMANCE_ANALYSIS"

class ProgrammingLanguage(Enum):
    """Linguagens de programação suportadas"""
    PYTHON = "PYTHON"
    JAVASCRIPT = "JAVASCRIPT"
    TYPESCRIPT = "TYPESCRIPT"
    JAVA = "JAVA"
    CPP = "CPP"
    CSHARP = "CSHARP"
    GO = "GO"
    RUST = "RUST"
    SWIFT = "SWIFT"
    KOTLIN = "KOTLIN"

class ComplexityLevel(Enum):
    """Níveis de complexidade"""
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINE_LOG = "O(n log n)"
    QUADRATIC = "O(n²)"
    EXPONENTIAL = "O(2^n)"
    FACTORIAL = "O(n!)"

class SecurityRiskLevel(Enum):
    """Níveis de risco de segurança"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class CodeMetrics:
    """Métricas de código"""
    complexity: str = "UNKNOWN"
    performance: str = "UNKNOWN"
    security_score: float = 0.0  # 0-100
    lines_of_code: int = 0
    function_count: int = 0
    class_count: int = 0
    cyclomatic_complexity: int = 0
    maintainability_index: float = 0.0  # 0-100
    duplication_rate: float = 0.0  # 0-100
    cognitive_complexity: int = 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo das métricas"""
        return {
            'complexity': self.complexity,
            'performance': self.performance,
            'security_score': f"{self.security_score:.1f}/100",
            'lines_of_code': self.lines_of_code,
            'functions': self.function_count,
            'classes': self.class_count,
            'cyclomatic_complexity': self.cyclomatic_complexity,
            'maintainability': f"{self.maintainability_index:.1f}/100",
            'duplication': f"{self.duplication_rate:.1f}%",
            'cognitive_complexity': self.cognitive_complexity
        }

@dataclass
class CodeIssue:
    """Problema identificado no código"""
    id: str
    line: int
    column: int = 0
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    category: str = "CODE_STYLE"  # SYNTAX, LOGIC, SECURITY, PERFORMANCE, STYLE
    message: str = ""
    suggestion: str = ""
    code_snippet: str = ""
    
    def get_issue_info(self) -> Dict[str, Any]:
        """Retorna informações do problema"""
        return {
            'id': self.id,
            'location': f"L{self.line}:C{self.column}",
            'severity': self.severity,
            'category': self.category,
            'message': self.message,
            'suggestion': self.suggestion,
            'code_snippet': self.code_snippet[:100] + '...' if len(self.code_snippet) > 100 else self.code_snippet
        }

@dataclass
class CodeAnalysisResult:
    """Resultado da análise de código"""
    type: CodeAnalysisType
    original_code: str
    generated_code: str = ""
    explanation: str = ""
    issues: List[CodeIssue] = field(default_factory=list)
    metrics: CodeMetrics = field(default_factory=CodeMetrics)
    suggestions: List[str] = field(default_factory=list)
    execution_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    analysis_id: str = field(default_factory=lambda: f"ANAL-{int(time.time())}-{random.randint(1000, 9999)}")
    
    def __post_init__(self):
        # Se não houver generated_code, usa original como fallback
        if not self.generated_code:
            self.generated_code = self.original_code
    
    def get_result_summary(self) -> Dict[str, Any]:
        """Retorna resumo do resultado"""
        critical_issues = [i for i in self.issues if i.severity == "CRITICAL"]
        high_issues = [i for i in self.issues if i.severity == "HIGH"]
        
        return {
            'analysis_id': self.analysis_id,
            'type': self.type.value,
            'execution_time': f"{self.execution_time_ms:.0f}ms",
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'issues_total': len(self.issues),
            'issues_critical': len(critical_issues),
            'issues_high': len(high_issues),
            'security_score': f"{self.metrics.security_score:.1f}/100",
            'complexity': self.metrics.complexity,
            'suggestions_count': len(self.suggestions)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'type': self.type.value,
            'original_code': self.original_code,
            'generated_code': self.generated_code,
            'explanation': self.explanation,
            'issues': [issue.get_issue_info() for issue in self.issues],
            'metrics': self.metrics.get_summary(),
            'suggestions': self.suggestions,
            'execution_time_ms': self.execution_time_ms,
            'timestamp': self.timestamp.isoformat(),
            'analysis_id': self.analysis_id
        }

# --- SIMULAÇÃO DA API GOOGLE GENAI ---

class GoogleGenAI:
    """Simulação da API Google GenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "demo-key")
        self.model = "gemini-2.5-flash"
        self.request_count = 0
        self.response_cache = {}
    
    class ContentConfig:
        """Configuração de conteúdo"""
        
        def __init__(self, **kwargs):
            self.system_instruction = kwargs.get("system_instruction", "")
            self.response_mime_type = kwargs.get("response_mime_type", "text/plain")
            self.response_schema = kwargs.get("response_schema", {})
            self.temperature = kwargs.get("temperature", 0.7)
            self.max_tokens = kwargs.get("max_tokens", 2000)
    
    async def generate_content(self, contents: str, config: Optional[ContentConfig] = None) -> Dict[str, Any]:
        """
        Gera conteúdo usando IA (simulação)
        
        Args:
            contents: Conteúdo de entrada
            config: Configuração da geração
            
        Returns:
            Dict com resposta
        """
        self.request_count += 1
        
        # Verifica cache
        cache_key = hashlib.md5((contents + str(config.system_instruction if config else "")).encode()).hexdigest()
        if cache_key in self.response_cache:
            print(f"📦 Resposta em cache recuperada: {cache_key[:8]}")
            return self.response_cache[cache_key]
        
        # Simula latência de rede
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Parse do conteúdo
        task_type = self._extract_task_type(contents)
        source_code = self._extract_source_code(contents)
        
        # Gera resposta baseada no tipo de tarefa
        response = self._generate_response_based_on_task(task_type, source_code, config)
        
        # Armazena em cache
        self.response_cache[cache_key] = response
        
        # Limita cache
        if len(self.response_cache) > 100:
            # Remove item mais antigo
            oldest_key = next(iter(self.response_cache))
            del self.response_cache[oldest_key]
        
        print(f"🧠 Requisição {self.request_count}: {task_type}")
        return response
    
    def _extract_task_type(self, contents: str) -> str:
        """Extrai tipo de tarefa do prompt"""
        task_match = re.search(r'TASK:\s*(\w+)', contents, re.IGNORECASE)
        if task_match:
            return task_match.group(1).upper()
        return "UNKNOWN"
    
    def _extract_source_code(self, contents: str) -> str:
        """Extrai código fonte do prompt"""
        code_match = re.search(r'SOURCE CODE:\s*(.*?)(?:\n\n|\Z)', contents, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        return ""
    
    def _generate_response_based_on_task(self, task_type: str, source_code: str, config: Optional[ContentConfig]) -> Dict[str, Any]:
        """Gera resposta baseada no tipo de tarefa"""
        base_response = {
            "text": "",
            "candidates": [{"content": {"parts": [{"text": ""}]}}],
            "usage": {"prompt_tokens": len(source_code) // 4, "completion_tokens": 500}
        }
        
        if not source_code:
            base_response["text"] = json.dumps({
                "originalCode": "",
                "generatedCode": "",
                "explanation": "Nenhum código fornecido para análise.",
                "issues": [],
                "metrics": {},
                "suggestions": []
            })
            return base_response
        
        # Analisa código para métricas básicas
        lines = source_code.split('\n')
        issues = self._analyze_code_for_issues(source_code)
        
        if task_type == "CORRECTION":
            response_data = self._generate_correction_response(source_code, issues)
        elif task_type == "OPTIMIZATION":
            response_data = self._generate_optimization_response(source_code, issues)
        elif task_type == "TRANSLATION":
            target_lang = self._extract_target_language(source_code)
            response_data = self._generate_translation_response(source_code, target_lang)
        elif task_type == "DOCUMENTATION":
            response_data = self._generate_documentation_response(source_code)
        elif task_type == "SECURITY":
            response_data = self._generate_security_response(source_code, issues)
        elif task_type == "DEBUG":
            response_data = self._generate_debug_response(source_code, issues)
        elif task_type == "TEST_GENERATION":
            response_data = self._generate_test_response(source_code)
        else:
            response_data = self._generate_general_response(source_code)
        
        # Adiciona métricas
        response_data["metrics"] = self._calculate_metrics(source_code, issues)
        
        base_response["text"] = json.dumps(response_data)
        return base_response
    
    def _extract_target_language(self, contents: str) -> str:
        """Extrai linguagem alvo"""
        lang_match = re.search(r'TARGET LANGUAGE:\s*(\w+)', contents, re.IGNORECASE)
        return lang_match.group(1) if lang_match else "PYTHON"
    
    def _analyze_code_for_issues(self, code: str) -> List[Dict[str, Any]]:
        """Analisa código para problemas básicos"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Verifica estilo básico
            if len(line) > 100:
                issues.append({
                    "line": i,
                    "message": "Linha muito longa (>100 caracteres)",
                    "severity": "LOW",
                    "category": "STYLE"
                })
            
            # Verifica comentários TODO/FIXME
            if "TODO" in line.upper() or "FIXME" in line.upper():
                issues.append({
                    "line": i,
                    "message": "TODO/FIXME encontrado no código",
                    "severity": "MEDIUM",
                    "category": "MAINTENANCE"
                })
            
            # Verifica código comentado
            if line.startswith("#") and len(line) > 1:
                issues.append({
                    "line": i,
                    "message": "Código comentado possivelmente desnecessário",
                    "severity": "LOW",
                    "category": "CLEANUP"
                })
        
        return issues
    
    def _calculate_metrics(self, code: str, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula métricas básicas do código"""
        lines = code.split('\n')
        critical_issues = len([i for i in issues if i.get("severity") == "CRITICAL"])
        
        security_score = max(0, 100 - (critical_issues * 20))
        
        return {
            "complexity": "MEDIUM" if len(lines) > 50 else "LOW",
            "performance": "GOOD",
            "securityScore": security_score,
            "linesOfCode": len(lines),
            "issueCount": len(issues)
        }
    
    def _generate_correction_response(self, code: str, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera resposta para correção"""
        fixed_code = code
        
        # Aplica correções simples
        lines = fixed_code.split('\n')
        corrected_lines = []
        
        for line in lines:
            # Corrige espaçamento básico
            corrected = line.replace("  ", "    ")  # 2 espaços para 4
            corrected_lines.append(corrected)
        
        fixed_code = '\n'.join(corrected_lines)
        
        return {
            "originalCode": code,
            "generatedCode": fixed_code,
            "explanation": f"Corrigidos {len(issues)} problemas identificados. Ajustes aplicados para melhorar legibilidade e correção de estilo.",
            "issues": [f"{i['message']} (linha {i['line']})" for i in issues],
            "suggestions": [
                "Considere adicionar mais comentários para documentação",
                "Separe funções complexas em funções menores",
                "Use nomes de variáveis mais descritivos"
            ]
        }
    
    def _generate_optimization_response(self, code: str, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera resposta para otimização"""
        optimized_code = code
        
        # Adiciona sugestões de otimização
        suggestions = [
            "Use list comprehension para loops simples",
            "Cache resultados de funções pesadas",
            "Considere usar generators para grandes datasets",
            "Evite chamadas repetidas a mesma função",
            "Use estruturas de dados apropriadas para o caso"
        ]
        
        return {
            "originalCode": code,
            "generatedCode": optimized_code,
            "explanation": "Análise de performance completada. Sugestões de otimização fornecidas abaixo.",
            "issues": [f"{i['message']} (linha {i['line']})" for i in issues],
            "suggestions": suggestions[:3]  # Apenas 3 sugestões
        }
    
    def _generate_translation_response(self, code: str, target_lang: str) -> Dict[str, Any]:
        """Gera resposta para tradução"""
        translation_map = {
            "PYTHON": {
                "print": "console.log",
                "def ": "function ",
                "self.": "this.",
                "import ": "const ",
                "from ": "import ",
                "# ": "// ",
                "True": "true",
                "False": "false",
                "None": "null"
            },
            "JAVASCRIPT": {
                "function ": "def ",
                "this.": "self.",
                "const ": "import ",
                "let ": "",
                "var ": "",
                "console.log": "print",
                "// ": "# ",
                "true": "True",
                "false": "False",
                "null": "None"
            }
        }
        
        translated_code = code
        if target_lang in translation_map:
            for src, tgt in translation_map[target_lang].items():
                translated_code = translated_code.replace(src, tgt)
        
        return {
            "originalCode": code,
            "generatedCode": translated_code,
            "explanation": f"Código traduzido de Python para {target_lang}. Ajustes sintáticos aplicados para manter funcionalidade.",
            "issues": [],
            "suggestions": [
                f"Teste exaustivamente após tradução para {target_lang}",
                "Considere diferenças de semântica entre linguagens",
                "Adapte bibliotecas específicas da linguagem"
            ]
        }
    
    def _generate_documentation_response(self, code: str) -> Dict[str, Any]:
        """Gera resposta para documentação"""
        documented_code = code
        
        # Adiciona docstring básica se não existir
        if not re.search(r'\"\"\"[\s\S]*?\"\"\"', code) and not re.search(r"'''[\s\S]*?'''", code):
            documented_code = '"""\nDocumentação gerada automaticamente\n\nFunção: Processa dados e retorna resultado\nArgs:\n    data: Dados de entrada\nReturns:\n    Resultado processado\n"""\n' + code
        
        return {
            "originalCode": code,
            "generatedCode": documented_code,
            "explanation": "Documentação gerada com docstrings básicas. Considere expandir com exemplos e casos de uso.",
            "issues": [],
            "suggestions": [
                "Adicione exemplos de uso",
                "Documente exceções que podem ser lançadas",
                "Inclua notas sobre performance",
                "Mencione dependências importantes"
            ]
        }
    
    def _generate_security_response(self, code: str, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera resposta para análise de segurança"""
        security_issues = issues.copy()
        
        # Adiciona verificações de segurança
        if "eval(" in code:
            security_issues.append({
                "line": code.find("eval("),
                "message": "Uso de eval() detectado - vulnerabilidade de injeção de código",
                "severity": "CRITICAL",
                "category": "SECURITY"
            })
        
        if "exec(" in code:
            security_issues.append({
                "line": code.find("exec("),
                "message": "Uso de exec() detectado - alto risco de segurança",
                "severity": "CRITICAL",
                "category": "SECURITY"
            })
        
        suggestions = [
            "Nunca use eval() ou exec() com entrada do usuário",
            "Valide e sanitize todas as entradas",
            "Use prepared statements para consultas de banco de dados",
            "Implemente rate limiting para APIs",
            "Considere usar bibliotecas de segurança validadas"
        ]
        
        return {
            "originalCode": code,
            "generatedCode": code,  # Não modifica código em análise de segurança
            "explanation": f"Análise de segurança completada. {len(security_issues)} vulnerabilidades potenciais identificadas.",
            "issues": [f"[{i.get('severity', 'UNKNOWN')}] {i['message']}" for i in security_issues],
            "suggestions": suggestions
        }
    
    def _generate_debug_response(self, code: str, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera resposta para debug"""
        # Adiciona prints de debug básicos
        debugged_code = code
        
        # Adiciona try-except se não existir
        if "try:" not in code and "except" not in code:
            lines = debugged_code.split('\n')
            if lines:
                lines.insert(0, "try:")
                lines.append("except Exception as e:")
                lines.append("    print(f\"Erro: {e}\")")
                lines.append("    raise")
                debugged_code = '\n'.join(lines)
        
        return {
            "originalCode": code,
            "generatedCode": debugged_code,
            "explanation": "Código instrumentado para debug. Try-except adicionado para capturar exceções.",
            "issues": [f"{i['message']} (linha {i['line']})" for i in issues],
            "suggestions": [
                "Adicione mais logs para rastrear execução",
                "Use debugger interativo (pdb) para análise detalhada",
                "Considere adicionar métricas de performance",
                "Implemente testes unitários para isolar problemas"
            ]
        }
    
    def _generate_test_response(self, code: str) -> Dict[str, Any]:
        """Gera resposta para geração de testes"""
        # Gera teste básico
        test_code = f'''
import unittest

class TestGeneratedCode(unittest.TestCase):
    """Testes gerados automaticamente para o código"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        pass
    
    def test_basic_functionality(self):
        """Testa funcionalidade básica"""
        # TODO: Implementar testes específicos
        self.assertTrue(True)
    
    def test_edge_cases(self):
        """Testa casos de borda"""
        # TODO: Testar valores limites
        pass
    
    def test_error_handling(self):
        """Testa tratamento de erros"""
        # TODO: Testar exceções
        pass

if __name__ == '__main__':
    unittest.main()
'''
        
        return {
            "originalCode": code,
            "generatedCode": test_code.strip(),
            "explanation": "Estrutura de testes unitários gerada. Implemente os métodos TODO com casos de teste específicos.",
            "issues": [],
            "suggestions": [
                "Implemente testes para casos de uso reais",
                "Adicione testes de integração",
                "Considere usar fixtures para dados de teste",
                "Teste tanto casos válidos quanto inválidos",
                "Meça cobertura de código"
            ]
        }
    
    def _generate_general_response(self, code: str) -> Dict[str, Any]:
        """Gera resposta geral"""
        return {
            "originalCode": code,
            "generatedCode": code,
            "explanation": "Análise geral completada. Consulte sugestões para melhorias.",
            "issues": [],
            "suggestions": [
                "Revise a estrutura do código",
                "Considere padrões de design apropriados",
                "Documente decisões arquiteturais",
                "Planeje para escalabilidade"
            ]
        }

# --- SERVIÇO DE ANÁLISE DE CÓDIGO ---

class CodeAnalysisService:
    """Serviço de Análise de Código"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.ai = GoogleGenAI(api_key=api_key)
        self.analysis_history = []
        self.cache_enabled = True
        self.max_history = 100
        
        print("🧠 CyberArchitect: Serviço de Análise de Código inicializado")
        print("   Recursos: Correção, Otimização, Tradução, Documentação, Segurança, Debug, Testes")
    
    def _get_system_instruction(self, analysis_type: CodeAnalysisType, 
                               language: ProgrammingLanguage, 
                               target_lang: Optional[ProgrammingLanguage] = None) -> str:
        """
        Gera instrução de sistema baseada no tipo de análise
        
        Args:
            analysis_type: Tipo de análise
            language: Linguagem do código
            target_lang: Linguagem alvo (para tradução)
            
        Returns:
            Instrução de sistema formatada
        """
        base = (
            f"Você é uma IA Arquitetônica Avançada chamada 'CyberArchitect'. "
            f"Seu objetivo é analisar, corrigir e otimizar código com extrema precisão. "
            f"Linguagem: {language.value}. "
        )
        
        instructions = {
            CodeAnalysisType.CORRECTION: (
                "Identifique erros de sintaxe e lógica. "
                "Forneça código corrigido e liste erros encontrados."
            ),
            CodeAnalysisType.OPTIMIZATION: (
                "Otimize para performance (Big O) e legibilidade. "
                "Sugira melhorias de estrutura."
            ),
            CodeAnalysisType.TRANSLATION: (
                f"Converta código de {language.value} para {target_lang.value if target_lang else 'LINGUAGEM_ALVO'}. "
                "Mantenha lógica e funcionalidade."
            ),
            CodeAnalysisType.DOCUMENTATION: (
                "Gere documentação profissional (docstrings), "
                "explique funcionalidade, parâmetros e retornos."
            ),
            CodeAnalysisType.SECURITY: (
                "Analise vulnerabilidades de segurança (injeção, overflow, vazamentos). "
                "Forneça correções e avaliação de risco."
            ),
            CodeAnalysisType.DEBUG: (
                "Debug o código fornecido. Assuma que tem erros. "
                "Encontre causas raiz e corrija."
            ),
            CodeAnalysisType.TEST_GENERATION: (
                "Gere testes unitários abrangentes "
                "(casos de borda, entradas válidas/inválidas)."
            ),
            CodeAnalysisType.ARCHITECTURE_REVIEW: (
                "Analise a arquitetura do código. "
                "Sugira melhorias de design e padrões."
            ),
            CodeAnalysisType.PERFORMANCE_ANALYSIS: (
                "Analise performance e gargalos. "
                "Sugira otimizações específicas."
            )
        }
        
        return base + instructions.get(analysis_type, "Analise o código fornecendo feedback construtivo.")
    
    def _get_response_schema(self) -> Dict[str, Any]:
        """Retorna schema para resposta JSON"""
        return {
            "type": "object",
            "properties": {
                "originalCode": {"type": "string"},
                "generatedCode": {"type": "string"},
                "explanation": {"type": "string"},
                "issues": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "metrics": {
                    "type": "object",
                    "properties": {
                        "complexity": {"type": "string"},
                        "performance": {"type": "string"},
                        "securityScore": {"type": "number"}
                    }
                },
                "suggestions": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["generatedCode", "explanation"]
        }
    
    def _create_prompt(self, code: str, analysis_type: CodeAnalysisType, 
                      target_lang: Optional[ProgrammingLanguage] = None) -> str:
        """Cria prompt para análise"""
        prompt = f"""
TASK: {analysis_type.value}

SOURCE CODE:
{code}

{('TARGET LANGUAGE: ' + target_lang.value) if analysis_type == CodeAnalysisType.TRANSLATION and target_lang else ''}

Analise o código estritamente de acordo com a tarefa. Retorne formato JSON.
        """
        
        return prompt.strip()
    
    def _parse_ai_response(self, response_text: str, original_code: str, 
                          analysis_type: CodeAnalysisType) -> CodeAnalysisResult:
        """Parseia resposta da IA para objeto estruturado"""
        try:
            response_data = json.loads(response_text)
            
            # Converte issues para objetos CodeIssue
            issues = []
            if "issues" in response_data:
                for i, issue_text in enumerate(response_data["issues"]):
                    issues.append(CodeIssue(
                        id=f"ISSUE-{i+1}",
                        line=1,
                        message=issue_text,
                        severity="MEDIUM",
                        category="GENERAL"
                    ))
            
            # Cria métricas
            metrics = CodeMetrics()
            if "metrics" in response_data:
                metrics_data = response_data["metrics"]
                metrics.complexity = metrics_data.get("complexity", "UNKNOWN")
                metrics.performance = metrics_data.get("performance", "UNKNOWN")
                metrics.security_score = metrics_data.get("securityScore", 0.0)
            
            return CodeAnalysisResult(
                type=analysis_type,
                original_code=original_code,
                generated_code=response_data.get("generatedCode", original_code),
                explanation=response_data.get("explanation", ""),
                issues=issues,
                metrics=metrics,
                suggestions=response_data.get("suggestions", []),
                execution_time_ms=0.0  # Será preenchido após execução
            )
            
        except json.JSONDecodeError:
            # Fallback em caso de erro no JSON
            return CodeAnalysisResult(
                type=analysis_type,
                original_code=original_code,
                generated_code=original_code,
                explanation="Erro ao parsear resposta da IA. Código retornado sem modificações.",
                issues=[
                    CodeIssue(
                        id="PARSE-ERROR",
                        line=0,
                        message="Falha ao decodificar resposta JSON da IA",
                        severity="MEDIUM",
                        category="SYSTEM"
                    )
                ],
                suggestions=["Verifique o formato da resposta da IA"]
            )
    
    async def analyze_code(self, code: str, analysis_type: CodeAnalysisType, 
                          language: ProgrammingLanguage = ProgrammingLanguage.PYTHON,
                          target_lang: Optional[ProgrammingLanguage] = None) -> CodeAnalysisResult:
        """
        Analisa código usando IA
        
        Args:
            code: Código fonte para análise
            analysis_type: Tipo de análise
            language: Linguagem do código
            target_lang: Linguagem alvo (para tradução)
            
        Returns:
            CodeAnalysisResult: Resultado da análise
        """
        start_time = time.time()
        
        try:
            # Cria prompt
            prompt = self._create_prompt(code, analysis_type, target_lang)
            
            # Configuração da IA
            config = self.ai.ContentConfig(
                system_instruction=self._get_system_instruction(analysis_type, language, target_lang),
                response_mime_type="application/json",
                response_schema=self._get_response_schema(),
                temperature=0.2,  # Baixa temperatura para análise precisa
                max_tokens=4000
            )
            
            # Chama IA
            print(f"🔍 Analisando código ({analysis_type.value})...")
            response = await self.ai.generate_content(prompt, config)
            
            # Parseia resposta
            execution_time = (time.time() - start_time) * 1000  # ms
            
            result = self._parse_ai_response(response.get("text", "{}"), code, analysis_type)
            result.execution_time_ms = execution_time
            
            # Armazena no histórico
            self._add_to_history(result)
            
            print(f"✅ Análise completada em {execution_time:.0f}ms")
            
            return result
            
        except Exception as error:
            execution_time = (time.time() - start_time) * 1000
            
            print(f"❌ Falha na análise: {str(error)}")
            
            # Resultado de fallback
            return CodeAnalysisResult(
                type=analysis_type,
                original_code=code,
                generated_code=code,
                explanation=f"Falha na análise neural. Erro: {str(error)}",
                issues=[
                    CodeIssue(
                        id="SYSTEM-ERROR",
                        line=0,
                        message=f"Erro no sistema de análise: {str(error)}",
                        severity="HIGH",
                        category="SYSTEM"
                    )
                ],
                execution_time_ms=execution_time
            )
    
    def _add_to_history(self, result: CodeAnalysisResult):
        """Adiciona resultado ao histórico"""
        self.analysis_history.append(result)
        
        # Limita histórico
        if len(self.analysis_history) > self.max_history:
            self.analysis_history = self.analysis_history[-self.max_history:]
    
    def get_history(self, limit: int = 10, 
                    analysis_type: Optional[CodeAnalysisType] = None) -> List[CodeAnalysisResult]:
        """Retorna histórico de análises"""
        filtered = self.analysis_history
        
        if analysis_type:
            filtered = [r for r in filtered if r.type == analysis_type]
        
        return filtered[-limit:] if filtered else []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do serviço"""
        total_analyses = len(self.analysis_history)
        
        if total_analyses == 0:
            return {"status": "No analyses performed yet"}
        
        # Contagem por tipo
        type_counts = {}
        for analysis in self.analysis_history:
            type_name = analysis.type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        # Tempo médio de execução
        avg_time = sum(a.execution_time_ms for a in self.analysis_history) / total_analyses
        
        # Issues totais
        total_issues = sum(len(a.issues) for a in self.analysis_history)
        
        return {
            "total_analyses": total_analyses,
            "analysis_by_type": type_counts,
            "avg_execution_time_ms": f"{avg_time:.1f}",
            "total_issues_found": total_issues,
            "cache_hit_rate": f"{self.ai.request_count - len(self.ai.response_cache)}/{self.ai.request_count}"
        }

# --- INSTÂNCIA GLOBAL ---

code_architect = CodeAnalysisService()

# --- FUNÇÃO DE DEMONSTRAÇÃO ---

async def demonstrate_code_analysis():
    """Demonstra o serviço de análise de código"""
    
    print("=" * 60)
    print("CYBERARCHITECT - SERVIÇO DE ANÁLISE DE CÓDIGO")
    print("=" * 60)
    
    # Código de exemplo para análise
    sample_code = '''
def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def process_data(data):
    result = []
    for item in data:
        if item > 10:
            result.append(item * 2)
    return result

print(calculate_fibonacci(10))
'''
    
    print("\n📝 CÓDIGO DE EXEMPLO:")
    print(sample_code)
    
    # Testa diferentes tipos de análise
    test_analyses = [
        (CodeAnalysisType.CORRECTION, "Correção"),
        (CodeAnalysisType.OPTIMIZATION, "Otimização"),
        (CodeAnalysisType.DOCUMENTATION, "Documentação"),
        (CodeAnalysisType.SECURITY, "Segurança"),
        (CodeAnalysisType.TEST_GENERATION, "Geração de Testes")
    ]
    
    results = []
    
    for analysis_type, description in test_analyses:
        print(f"\n🔍 EXECUTANDO {description.upper()}...")
        
        result = await code_architect.analyze_code(
            code=sample_code,
            analysis_type=analysis_type,
            language=ProgrammingLanguage.PYTHON
        )
        
        results.append(result)
        
        # Mostra resumo
        summary = result.get_result_summary()
        print(f"✅ {description} completada:")
        print(f"   Tempo: {summary['execution_time']}")
        print(f"   Issues: {summary['issues_total']} total, {summary['issues_critical']} críticos")
        print(f"   Score segurança: {summary['security_score']}")
        print(f"   Sugestões: {summary['suggestions_count']}")
        
        # Mostra explicação resumida
        if result.explanation:
            explanation_preview = result.explanation[:150] + "..." if len(result.explanation) > 150 else result.explanation
            print(f"   Explicação: {explanation_preview}")
        
        # Pequena pausa entre análises
        await asyncio.sleep(0.5)
    
    # Demonstra tradução
    print("\n🌐 TESTANDO TRADUÇÃO (Python → JavaScript)...")
    
    translation_result = await code_architect.analyze_code(
        code=sample_code,
        analysis_type=CodeAnalysisType.TRANSLATION,
        language=ProgrammingLanguage.PYTHON,
        target_lang=ProgrammingLanguage.JAVASCRIPT
    )
    
    print(f"✅ Tradução completada:")
    translation_preview = translation_result.generated_code[:200] + "..." if len(translation_result.generated_code) > 200 else translation_result.generated_code
    print(f"   Preview: {translation_preview}")
    
    # Estatísticas do serviço
    print("\n📊 ESTATÍSTICAS DO SERVIÇO:")
    stats = code_architect.get_statistics()
    
    for key, value in stats.items():
        if key == "analysis_by_type":
            print(f"  Análises por tipo:")
            for type_name, count in value.items():
                print(f"    {type_name}: {count}")
        else:
            print(f"  {key}: {value}")
    
    # Histórico recente
    print(f"\n📋 HISTÓRICO RECENTE:")
    recent = code_architect.get_history(limit=3)
    
    for i, analysis in enumerate(recent, 1):
        summary = analysis.get_result_summary()
        print(f"  {i}. {summary['type']}: {summary['issues_total']} issues, {summary['execution_time']}")
    
    print("\n" + "=" * 60)
    print("✅ Demonstração do CyberArchitect completa!")
    print("=" * 60)

if __name__ == "__main__":
    # Executa demonstração
    asyncio.run(demonstrate_code_analysis())