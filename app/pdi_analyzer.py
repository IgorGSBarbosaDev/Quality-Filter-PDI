"""
Classe principal do analisador de PDI.
Coordena todos os serviços e fornece interface unificada.
"""
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path

from .core.config import COLUMN_MAPPING
from .services.pdi_analysis_service import PDIAnalysisService
from .services.file_service import FileService


class PDIAnalyzer:
    """
    Analisador principal de qualidade de PDI.
    
    Esta classe coordena todos os serviços necessários para análise
    de qualidade de Planos de Desenvolvimento Individual (PDI).
    """
    
    def __init__(self):
        """Inicializa o analisador com todos os serviços necessários."""
        self.analysis_service = PDIAnalysisService()
        self.file_service = FileService()
        self.column_mapping = COLUMN_MAPPING
    
    def analyze_file(
        self, 
        file_path: str, 
        output_dir: str = "output",
        sample_size: Optional[int] = None
    ) -> Tuple[str, str, Dict]:
        """
        Analisa um arquivo completo de PDIs.
        
        Args:
            file_path: Caminho para o arquivo de dados
            output_dir: Diretório para salvar resultados
            sample_size: Tamanho da amostra (None para arquivo completo)
            
        Returns:
            Tupla com (caminho_csv_resultado, caminho_json_resumo, resumo_dict)
        """
        print(f"🚀 Iniciando análise do arquivo: {Path(file_path).name}")
        
        # Carrega arquivo
        df = self._load_file(file_path)
        
        # Valida estrutura dos dados
        self._validate_data_structure(df)
        
        # Aplica amostragem se solicitado
        if sample_size and len(df) > sample_size:
            df = df.head(sample_size)
            print(f"📊 Usando amostra de {sample_size} registros")
        
        print(f"📊 Analisando {len(df)} registros...")
        
        # Executa análise
        result_df, summary = self.analysis_service.analyze_dataframe(df)
        
        # Salva resultados
        csv_path, json_path = self.file_service.save_results(
            result_df, summary, output_dir, "analise_pdi"
        )
        
        return csv_path, json_path, summary
    
    def analyze_text(self, objetivo: str, acoes: str = "", atividade: str = "") -> Dict[str, Any]:
        """
        Analisa textos individuais de PDI.
        
        Args:
            objetivo: Objetivo de desenvolvimento
            acoes: Ações planejadas
            atividade: Atividade de aprendizagem
            
        Returns:
            Resultado da análise
        """
        # Monta dados do PDI
        pdi_data = {
            self.column_mapping['objetivo_desenvolvimento']: objetivo,
            self.column_mapping['acoes_planejadas']: acoes,
            self.column_mapping.get('atividade_aprendizagem', ''): atividade
        }
        
        return self.analysis_service.analyze_single_pdi(pdi_data)
    
    def generate_report(self, results_file: str) -> Dict[str, Any]:
        """
        Gera relatório detalhado a partir de arquivo de resultados.
        
        Args:
            results_file: Caminho para arquivo CSV com resultados
            
        Returns:
            Relatório detalhado
        """
        # Carrega resultados
        df = pd.read_csv(results_file)
        
        # Gera estatísticas detalhadas
        report = self._generate_detailed_report(df)
        
        return report
    
    def get_improvement_suggestions(self, results_file: str, quality_level: str = "Baixa") -> List[Dict]:
        """
        Obtém sugestões de melhoria para PDIs de determinado nível.
        
        Args:
            results_file: Arquivo com resultados da análise
            quality_level: Nível de qualidade para filtrar
            
        Returns:
            Lista de PDIs com sugestões
        """
        df = pd.read_csv(results_file)
        
        # Filtra por nível de qualidade
        filtered_df = df[df['quality_level'] == quality_level]
        
        suggestions = []
        for _, row in filtered_df.iterrows():
            suggestions.append({
                'nome': row.get('Nome Completo', 'N/A'),
                'objetivo': row.get('Objetivo de Desenvolvimento (GAP)', 'N/A'),
                'score': row.get('overall_score', 0),
                'suggestions': row.get('suggestions', 'Sem sugestões')
            })
        
        return suggestions
    
    def _load_file(self, file_path: str) -> pd.DataFrame:
        """Carrega arquivo baseado no tipo detectado."""
        file_info = self.file_service.get_file_info(file_path)
        
        if not file_info['exists']:
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        print(f"📁 Arquivo: {file_info['name']} ({file_info['size_mb']} MB)")
        
        if file_info['type'] == 'csv':
            df, encoding = self.file_service.load_csv(file_path)
            return df
        elif file_info['type'] == 'excel':
            return self.file_service.load_excel(file_path)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_info['type']}")
    
    def _validate_data_structure(self, df: pd.DataFrame) -> None:
        """Valida se o DataFrame possui as colunas necessárias."""
        required_columns = [
            self.column_mapping['objetivo_desenvolvimento'],
            self.column_mapping['acoes_planejadas']
        ]
        
        is_valid, missing = self.file_service.validate_data_structure(df, required_columns)
        
        if not is_valid:
            print(f"⚠️ Colunas obrigatórias não encontradas: {missing}")
            print(f"📋 Colunas disponíveis: {list(df.columns)}")
            # Não levanta erro, apenas avisa - sistema é tolerante
        
        print(f"✅ Estrutura de dados validada")
    
    def _generate_detailed_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Gera relatório detalhado dos resultados."""
        total = len(df)
        
        if total == 0:
            return {'error': 'Nenhum dado para análise'}
        
        # Estatísticas de qualidade
        quality_dist = df['quality_level'].value_counts().to_dict()
        
        # Estatísticas de scores
        score_stats = {
            'clarity': {
                'mean': df['clarity_score'].mean(),
                'std': df['clarity_score'].std(),
                'min': df['clarity_score'].min(),
                'max': df['clarity_score'].max()
            },
            'specificity': {
                'mean': df['specificity_score'].mean(),
                'std': df['specificity_score'].std(),
                'min': df['specificity_score'].min(),
                'max': df['specificity_score'].max()
            },
            'completeness': {
                'mean': df['completeness_score'].mean(),
                'std': df['completeness_score'].std(),
                'min': df['completeness_score'].min(),
                'max': df['completeness_score'].max()
            },
            'structure': {
                'mean': df['structure_score'].mean(),
                'std': df['structure_score'].std(),
                'min': df['structure_score'].min(),
                'max': df['structure_score'].max()
            },
            'smart_criteria': {
                'mean': df['smart_criteria_score'].mean(),
                'std': df['smart_criteria_score'].std(),
                'min': df['smart_criteria_score'].min(),
                'max': df['smart_criteria_score'].max()
            },
            'overall': {
                'mean': df['overall_score'].mean(),
                'std': df['overall_score'].std(),
                'min': df['overall_score'].min(),
                'max': df['overall_score'].max()
            }
        }
        
        # Melhores e piores PDIs
        best_pdis = df.nlargest(5, 'overall_score')[
            ['Nome Completo', 'Objetivo de Desenvolvimento (GAP)', 'overall_score']
        ].to_dict('records')
        
        worst_pdis = df.nsmallest(5, 'overall_score')[
            ['Nome Completo', 'Objetivo de Desenvolvimento (GAP)', 'overall_score']
        ].to_dict('records')
        
        return {
            'total_analyzed': total,
            'quality_distribution': quality_dist,
            'quality_percentages': {
                level: count / total * 100 
                for level, count in quality_dist.items()
            },
            'score_statistics': score_stats,
            'best_pdis': best_pdis,
            'worst_pdis': worst_pdis,
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        }
