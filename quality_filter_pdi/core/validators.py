"""
✅ Sistema de Validação Padronizado
Validações consistentes para dados e parâmetros
"""

from typing import Any, Dict, List, Optional, Union, Callable
import pandas as pd
import re
from .exceptions import DataValidationError
from .logging_config import get_logger

logger = get_logger('validator')


class ValidationRule:
    """Regra de validação individual"""
    
    def __init__(self, 
                 name: str, 
                 validator: Callable[[Any], bool], 
                 error_message: str,
                 severity: str = 'error'):
        self.name = name
        self.validator = validator
        self.error_message = error_message
        self.severity = severity  # 'error', 'warning', 'info'
    
    def validate(self, value: Any) -> bool:
        """Executa validação"""
        try:
            return self.validator(value)
        except Exception as e:
            logger.warning(f"Erro na validação '{self.name}': {e}")
            return False


class ValidationResult:
    """Resultado de validação"""
    
    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
    
    def add_error(self, message: str):
        """Adiciona erro"""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Adiciona aviso"""
        self.warnings.append(message)
    
    def add_info(self, message: str):
        """Adiciona informação"""
        self.info.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'is_valid': self.is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }


class Validator:
    """Validador principal"""
    
    def __init__(self):
        self.rules: List[ValidationRule] = []
    
    def add_rule(self, rule: ValidationRule) -> None:
        """Adiciona regra de validação"""
        self.rules.append(rule)
    
    def validate(self, value: Any) -> ValidationResult:
        """Executa todas as validações"""
        result = ValidationResult()
        
        for rule in self.rules:
            if not rule.validate(value):
                if rule.severity == 'error':
                    result.add_error(rule.error_message)
                elif rule.severity == 'warning':
                    result.add_warning(rule.error_message)
                else:
                    result.add_info(rule.error_message)
        
        return result


class PDIDataValidator:
    """Validador específico para dados de PDI"""
    
    def __init__(self):
        self._setup_text_validators()
        self._setup_dataframe_validators()
    
    def _setup_text_validators(self):
        """Configura validadores de texto"""
        self.text_validator = Validator()
        
        # Texto não vazio
        self.text_validator.add_rule(ValidationRule(
            'not_empty',
            lambda x: x and str(x).strip(),
            'Texto não pode estar vazio'
        ))
        
        # Comprimento mínimo
        self.text_validator.add_rule(ValidationRule(
            'min_length',
            lambda x: len(str(x).strip()) >= 5,
            'Texto muito curto (mínimo 5 caracteres)',
            'warning'
        ))
        
        # Comprimento máximo
        self.text_validator.add_rule(ValidationRule(
            'max_length',
            lambda x: len(str(x)) <= 1000,
            'Texto muito longo (máximo 1000 caracteres)',
            'warning'
        ))
        
        # Contém caracteres alfabéticos
        self.text_validator.add_rule(ValidationRule(
            'has_letters',
            lambda x: re.search(r'[a-záêçõãéàíóú]', str(x).lower()),
            'Texto deve conter pelo menos uma letra',
            'warning'
        ))
    
    def _setup_dataframe_validators(self):
        """Configura validadores de DataFrame"""
        self.dataframe_validator = Validator()
        
        # DataFrame não vazio
        self.dataframe_validator.add_rule(ValidationRule(
            'not_empty',
            lambda df: not df.empty,
            'DataFrame não pode estar vazio'
        ))
        
        # Tem colunas obrigatórias
        self.dataframe_validator.add_rule(ValidationRule(
            'required_columns',
            self._has_required_columns,
            'DataFrame deve ter pelo menos uma coluna de objetivo ou ações'
        ))
    
    def _has_required_columns(self, df: pd.DataFrame) -> bool:
        """Verifica se tem colunas obrigatórias"""
        if df.empty:
            return False
        
        required_patterns = [
            r'objetivo.*desenvolvimento',
            r'açã(o|õ)es.*realiz',
            r'atividade.*aprendizagem'
        ]
        
        columns_lower = [col.lower() for col in df.columns]
        
        for pattern in required_patterns:
            if any(re.search(pattern, col) for col in columns_lower):
                return True
        
        return False
    
    def validate_text(self, text: str, field_name: str = 'texto') -> ValidationResult:
        """Valida texto individual"""
        result = self.text_validator.validate(text)
        
        # Adicionar contexto do campo
        if not result.is_valid:
            result.errors = [f"{field_name}: {error}" for error in result.errors]
        if result.warnings:
            result.warnings = [f"{field_name}: {warning}" for warning in result.warnings]
        
        return result
    
    def validate_pdi_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Valida dados completos de PDI"""
        result = ValidationResult()
        
        # Validar campos obrigatórios
        required_fields = ['objetivo_desenvolvimento']
        
        for field in required_fields:
            if field not in data or not data[field]:
                result.add_error(f"Campo obrigatório ausente: {field}")
        
        # Validar textos individuais
        text_fields = [
            'objetivo_desenvolvimento',
            'acoes_planejadas', 
            'atividade_aprendizagem'
        ]
        
        for field in text_fields:
            if field in data and data[field]:
                text_result = self.validate_text(data[field], field)
                result.errors.extend(text_result.errors)
                result.warnings.extend(text_result.warnings)
                if not text_result.is_valid:
                    result.is_valid = False
        
        # Validar pelo menos um campo de ações
        has_actions = any(
            data.get(field) and str(data[field]).strip()
            for field in ['acoes_planejadas', 'atividade_aprendizagem']
        )
        
        if not has_actions:
            result.add_warning("Recomendado ter pelo menos ações ou atividades definidas")
        
        return result
    
    def validate_dataframe(self, df: pd.DataFrame) -> ValidationResult:
        """Valida DataFrame completo"""
        result = self.dataframe_validator.validate(df)
        
        if result.is_valid and not df.empty:
            # Validar qualidade dos dados
            empty_ratio = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
            
            if empty_ratio > 0.5:
                result.add_warning(f"DataFrame com muitos valores vazios ({empty_ratio:.1%})")
            
            # Verificar duplicatas
            if df.duplicated().any():
                duplicates = df.duplicated().sum()
                result.add_warning(f"Encontradas {duplicates} linhas duplicadas")
        
        return result


class ConfigValidator:
    """Validador para configurações"""
    
    @staticmethod
    def validate_metric_weights(weights: Dict[str, float]) -> ValidationResult:
        """Valida pesos das métricas"""
        result = ValidationResult()
        
        # Verificar se somam 1.0
        total = sum(weights.values())
        if abs(total - 1.0) > 0.001:
            result.add_error(f"Pesos devem somar 1.0, atual: {total:.3f}")
        
        # Verificar valores válidos
        for name, weight in weights.items():
            if not 0 <= weight <= 1:
                result.add_error(f"Peso '{name}' deve estar entre 0 e 1, atual: {weight}")
        
        return result
    
    @staticmethod
    def validate_thresholds(thresholds: Dict[str, float]) -> ValidationResult:
        """Valida limites de qualidade"""
        result = ValidationResult()
        
        # Verificar ordem crescente
        values = list(thresholds.values())
        if values != sorted(values):
            result.add_error("Limites devem estar em ordem crescente")
        
        # Verificar intervalo válido
        for name, threshold in thresholds.items():
            if not 0 <= threshold <= 1:
                result.add_error(f"Limite '{name}' deve estar entre 0 e 1, atual: {threshold}")
        
        return result


# Instâncias globais
pdi_validator = PDIDataValidator()
config_validator = ConfigValidator()

# Funções de conveniência
def validate_text(text: str, field_name: str = 'texto') -> ValidationResult:
    """Função de conveniência para validar texto"""
    return pdi_validator.validate_text(text, field_name)

def validate_pdi_data(data: Dict[str, Any]) -> ValidationResult:
    """Função de conveniência para validar dados PDI"""
    return pdi_validator.validate_pdi_data(data)

def validate_dataframe(df: pd.DataFrame) -> ValidationResult:
    """Função de conveniência para validar DataFrame"""
    return pdi_validator.validate_dataframe(df)
