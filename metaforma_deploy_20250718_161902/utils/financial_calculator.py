import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import logging
from datetime import datetime, timedelta

class FinancialCalculator:
    """
    Classe responsável por cálculos financeiros do Instituto Metaforma.
    Processa dados financeiros e gera métricas de performance.
    """
    
    def __init__(self, data_handler=None):
        """
        Inicializa o calculador financeiro.
        
        Args:
            data_handler: Instância do DataHandler para acesso aos dados
        """
        self.data_handler = data_handler
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o sistema de logging."""
        logger = logging.getLogger('FinancialCalculator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def calculate_roi(self, revenue: float, investment: float) -> float:
        """
        Calcula o Return on Investment (ROI).
        
        Args:
            revenue: Receita obtida
            investment: Investimento realizado
            
        Returns:
            ROI em percentual
        """
        try:
            if investment == 0:
                return 0.0
            
            roi = ((revenue - investment) / investment) * 100
            return round(roi, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular ROI: {str(e)}")
            return 0.0
    
    def calculate_conversion_rate(self, realized_revenue: float, budgeted_revenue: float) -> float:
        """
        Calcula a taxa de conversão (receita realizada vs orçada).
        
        Args:
            realized_revenue: Receita realizada
            budgeted_revenue: Receita orçada
            
        Returns:
            Taxa de conversão em percentual
        """
        try:
            if budgeted_revenue == 0:
                return 0.0
            
            conversion_rate = (realized_revenue / budgeted_revenue) * 100
            return round(conversion_rate, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular taxa de conversão: {str(e)}")
            return 0.0
    
    def calculate_default_rate(self, default_amount: float, gross_revenue: float) -> float:
        """
        Calcula a taxa de inadimplência.
        
        Args:
            default_amount: Valor da inadimplência
            gross_revenue: Receita bruta
            
        Returns:
            Taxa de inadimplência em percentual
        """
        try:
            if gross_revenue == 0:
                return 0.0
            
            default_rate = (default_amount / gross_revenue) * 100
            return round(default_rate, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular taxa de inadimplência: {str(e)}")
            return 0.0
    
    def calculate_operational_efficiency(self, net_revenue: float, total_expenses: float) -> float:
        """
        Calcula a eficiência operacional.
        
        Args:
            net_revenue: Receita líquida
            total_expenses: Total de despesas
            
        Returns:
            Eficiência operacional em percentual
        """
        try:
            if net_revenue == 0:
                return 0.0
            
            efficiency = (1 - (total_expenses / net_revenue)) * 100
            return round(efficiency, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular eficiência operacional: {str(e)}")
            return 0.0
    
    def calculate_average_ticket(self, total_revenue: float, total_students: int) -> float:
        """
        Calcula o ticket médio por aluno.
        
        Args:
            total_revenue: Receita total
            total_students: Total de alunos
            
        Returns:
            Ticket médio
        """
        try:
            if total_students == 0:
                return 0.0
            
            average_ticket = total_revenue / total_students
            return round(average_ticket, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular ticket médio: {str(e)}")
            return 0.0
    
    def calculate_profit_margin(self, net_result: float, gross_revenue: float) -> float:
        """
        Calcula a margem de lucro.
        
        Args:
            net_result: Resultado líquido
            gross_revenue: Receita bruta
            
        Returns:
            Margem de lucro em percentual
        """
        try:
            if gross_revenue == 0:
                return 0.0
            
            profit_margin = (net_result / gross_revenue) * 100
            return round(profit_margin, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular margem de lucro: {str(e)}")
            return 0.0
    
    def analyze_expense_distribution(self, expenses_dict: Dict[str, float]) -> Dict[str, float]:
        """
        Analisa a distribuição de despesas.
        
        Args:
            expenses_dict: Dicionário com categorias e valores de despesas
            
        Returns:
            Dicionário com percentual de cada categoria
        """
        try:
            total_expenses = sum(expenses_dict.values())
            
            if total_expenses == 0:
                return {category: 0.0 for category in expenses_dict.keys()}
            
            distribution = {}
            for category, amount in expenses_dict.items():
                percentage = (amount / total_expenses) * 100
                distribution[category] = round(percentage, 2)
            
            return distribution
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar distribuição de despesas: {str(e)}")
            return {}
    
    def calculate_growth_rate(self, current_value: float, previous_value: float) -> float:
        """
        Calcula a taxa de crescimento entre dois períodos.
        
        Args:
            current_value: Valor atual
            previous_value: Valor anterior
            
        Returns:
            Taxa de crescimento em percentual
        """
        try:
            if previous_value == 0:
                return 0.0 if current_value == 0 else 100.0
            
            growth_rate = ((current_value - previous_value) / previous_value) * 100
            return round(growth_rate, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular taxa de crescimento: {str(e)}")
            return 0.0
    
    def calculate_cash_flow(self, revenue: float, expenses: float, defaults: float = 0.0) -> float:
        """
        Calcula o fluxo de caixa.
        
        Args:
            revenue: Receita
            expenses: Despesas
            defaults: Inadimplência
            
        Returns:
            Fluxo de caixa
        """
        try:
            cash_flow = revenue - expenses - defaults
            return round(cash_flow, 2)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular fluxo de caixa: {str(e)}")
            return 0.0
    
    def calculate_break_even_point(self, fixed_costs: float, variable_cost_per_unit: float, price_per_unit: float) -> int:
        """
        Calcula o ponto de equilíbrio.
        
        Args:
            fixed_costs: Custos fixos
            variable_cost_per_unit: Custo variável por unidade
            price_per_unit: Preço por unidade
            
        Returns:
            Quantidade de unidades no ponto de equilíbrio
        """
        try:
            if price_per_unit <= variable_cost_per_unit:
                return 0
            
            break_even = fixed_costs / (price_per_unit - variable_cost_per_unit)
            return int(np.ceil(break_even))
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular ponto de equilíbrio: {str(e)}")
            return 0
    
    def generate_financial_summary(self, period: Optional[str] = None) -> Dict:
        """
        Gera um resumo financeiro completo.
        
        Args:
            period: Período específico ou None para todos
            
        Returns:
            Dicionário com resumo financeiro detalhado
        """
        try:
            if not self.data_handler:
                return {'error': 'DataHandler não configurado'}
            
            # Obter dados básicos
            basic_summary = self.data_handler.get_financial_summary(period)
            
            if 'error' in basic_summary:
                return basic_summary
            
            # Calcular métricas adicionais
            summary = basic_summary.copy()
            
            # Taxa de conversão
            summary['taxa_conversao'] = self.calculate_conversion_rate(
                summary['receita_realizada'],
                summary['receita_orcada']
            )
            
            # ROI
            summary['roi'] = self.calculate_roi(
                summary['resultado_realizado'],
                summary['despesas_totais']
            )
            
            # Margem de lucro
            summary['margem_lucro'] = self.calculate_profit_margin(
                summary['resultado_realizado'],
                summary['receita_realizada']
            )
            
            # Eficiência operacional
            summary['eficiencia_operacional'] = self.calculate_operational_efficiency(
                summary['receita_realizada'],
                summary['despesas_totais']
            )
            
            # Fluxo de caixa
            summary['fluxo_caixa'] = self.calculate_cash_flow(
                summary['receita_realizada'],
                summary['despesas_totais'],
                summary['inadimplencia_total']
            )
            
            # Análise de variação
            summary['variacao_receita'] = summary['receita_realizada'] - summary['receita_orcada']
            summary['variacao_resultado'] = summary['resultado_realizado'] - summary['resultado_orcado']
            
            # Percentual de variação
            if summary['receita_orcada'] != 0:
                summary['percentual_variacao_receita'] = (summary['variacao_receita'] / summary['receita_orcada']) * 100
            else:
                summary['percentual_variacao_receita'] = 0.0
            
            if summary['resultado_orcado'] != 0:
                summary['percentual_variacao_resultado'] = (summary['variacao_resultado'] / abs(summary['resultado_orcado'])) * 100
            else:
                summary['percentual_variacao_resultado'] = 0.0
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo financeiro: {str(e)}")
            return {'error': str(e)}
    
    def analyze_trend(self, values: List[float]) -> Dict[str, Union[str, float]]:
        """
        Analisa a tendência de uma série de valores.
        
        Args:
            values: Lista de valores ordenados cronologicamente
            
        Returns:
            Dicionário com análise de tendência
        """
        try:
            if len(values) < 2:
                return {'trend': 'Dados insuficientes', 'slope': 0.0, 'direction': 'Neutro'}
            
            # Calcular tendência usando regressão linear simples
            x = np.arange(len(values))
            y = np.array(values)
            
            # Remover valores NaN
            mask = ~np.isnan(y)
            if np.sum(mask) < 2:
                return {'trend': 'Dados insuficientes', 'slope': 0.0, 'direction': 'Neutro'}
            
            x_clean = x[mask]
            y_clean = y[mask]
            
            # Calcular coeficiente angular
            slope = np.polyfit(x_clean, y_clean, 1)[0]
            
            # Determinar direção da tendência
            if slope > 0.1:
                direction = 'Crescente'
                trend_emoji = '📈'
            elif slope < -0.1:
                direction = 'Declinante'
                trend_emoji = '📉'
            else:
                direction = 'Estável'
                trend_emoji = '➡️'
            
            # Calcular variação percentual total
            if y_clean[0] != 0:
                total_variation = ((y_clean[-1] - y_clean[0]) / abs(y_clean[0])) * 100
            else:
                total_variation = 0.0
            
            return {
                'trend': f'{trend_emoji} {direction}',
                'slope': round(slope, 4),
                'direction': direction,
                'total_variation': round(total_variation, 2),
                'average_value': round(np.mean(y_clean), 2)
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar tendência: {str(e)}")
            return {'trend': 'Erro na análise', 'slope': 0.0, 'direction': 'Neutro'}
    
    def calculate_customer_metrics(self) -> Dict:
        """
        Calcula métricas relacionadas aos clientes/alunos.
        
        Returns:
            Dicionário com métricas de clientes
        """
        try:
            if not self.data_handler:
                return {'error': 'DataHandler não configurado'}
            
            student_stats = self.data_handler.get_student_statistics()
            
            if 'error' in student_stats:
                return student_stats
            
            financial_summary = self.data_handler.get_financial_summary()
            
            metrics = {
                'total_clientes': student_stats['total_alunos'],
                'ticket_medio': student_stats['ticket_medio'],
                'receita_por_cliente': student_stats['receita_total_alunos'] / student_stats['total_alunos'] if student_stats['total_alunos'] > 0 else 0,
                'diversificacao_geografica': student_stats['estados_representados'],
                'concentracao_cursos': student_stats['cursos_ativos']
            }
            
            # Calcular LTV (Lifetime Value) estimado
            # Assumindo duração média de curso de 4 meses
            metrics['ltv_estimado'] = metrics['ticket_medio'] * 4
            
            # Calcular CAC (Customer Acquisition Cost) baseado em marketing
            if 'error' not in financial_summary:
                # Estimar CAC baseado nos gastos com Facebook Ads
                marketing_spend = 10200.0  # Total gasto com Facebook Ads (realizado)
                if student_stats['total_alunos'] > 0:
                    metrics['cac_estimado'] = marketing_spend / student_stats['total_alunos']
                else:
                    metrics['cac_estimado'] = 0.0
                
                # Ratio LTV/CAC
                if metrics['cac_estimado'] > 0:
                    metrics['ltv_cac_ratio'] = metrics['ltv_estimado'] / metrics['cac_estimado']
                else:
                    metrics['ltv_cac_ratio'] = 0.0
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular métricas de clientes: {str(e)}")
            return {'error': str(e)}
    
    def generate_performance_score(self, period: Optional[str] = None) -> Dict:
        """
        Gera um score de performance geral.
        
        Args:
            period: Período específico ou None para todos
            
        Returns:
            Dicionário com score de performance
        """
        try:
            summary = self.generate_financial_summary(period)
            
            if 'error' in summary:
                return summary
            
            # Calcular scores individuais (0-100)
            scores = {}
            
            # Score de receita (baseado na taxa de conversão)
            conversion_rate = summary.get('taxa_conversao', 0)
            scores['receita'] = min(conversion_rate, 100)
            
            # Score de lucratividade (baseado na margem de lucro)
            profit_margin = summary.get('margem_lucro', 0)
            if profit_margin >= 20:
                scores['lucratividade'] = 100
            elif profit_margin >= 10:
                scores['lucratividade'] = 70
            elif profit_margin >= 0:
                scores['lucratividade'] = 50
            else:
                scores['lucratividade'] = max(0, 50 + profit_margin * 2)  # Penalidade para prejuízo
            
            # Score de inadimplência (inverso da taxa)
            default_rate = summary.get('taxa_inadimplencia', 0)
            scores['cobranca'] = max(0, 100 - default_rate * 2)
            
            # Score de eficiência (baseado na eficiência operacional)
            efficiency = summary.get('eficiencia_operacional', 0)
            if efficiency >= 0:
                scores['eficiencia'] = min(efficiency, 100)
            else:
                scores['eficiencia'] = 0
            
            # Score geral (média ponderada)
            weights = {
                'receita': 0.3,
                'lucratividade': 0.3,
                'cobranca': 0.2,
                'eficiencia': 0.2
            }
            
            overall_score = sum(scores[key] * weights[key] for key in scores.keys())
            
            # Classificação do score
            if overall_score >= 80:
                classification = 'Excelente'
                color = '🟢'
            elif overall_score >= 60:
                classification = 'Bom'
                color = '🟡'
            elif overall_score >= 40:
                classification = 'Regular'
                color = '🟠'
            else:
                classification = 'Crítico'
                color = '🔴'
            
            return {
                'score_geral': round(overall_score, 1),
                'classificacao': f'{color} {classification}',
                'scores_individuais': {k: round(v, 1) for k, v in scores.items()},
                'pesos': weights,
                'recomendacoes': self._generate_recommendations(scores)
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar score de performance: {str(e)}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """
        Gera recomendações baseadas nos scores.
        
        Args:
            scores: Dicionário com scores individuais
            
        Returns:
            Lista de recomendações
        """
        recommendations = []
        
        if scores.get('receita', 0) < 50:
            recommendations.append("📈 Revisar estratégia de vendas e marketing")
        
        if scores.get('lucratividade', 0) < 50:
            recommendations.append("💰 Analisar estrutura de custos e precificação")
        
        if scores.get('cobranca', 0) < 70:
            recommendations.append("📞 Implementar sistema de cobrança mais eficiente")
        
        if scores.get('eficiencia', 0) < 60:
            recommendations.append("⚡ Otimizar processos operacionais")
        
        if not recommendations:
            recommendations.append("✅ Performance geral satisfatória - manter estratégia atual")
        
        return recommendations
