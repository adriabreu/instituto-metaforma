import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
import re

@dataclass
class BankTransaction:
    """Representa uma transação bancária."""
    date: datetime
    amount: float
    description: str
    document: str
    account: str
    type: str  # 'credit' or 'debit'

@dataclass
class StudentPayment:
    """Representa um pagamento esperado de aluno."""
    student_id: str
    student_name: str
    installment_number: int
    due_date: datetime
    amount: float
    payment_method: str
    status: str  # 'pending', 'paid', 'overdue'

class BankReconciliation:
    """
    Sistema de conciliação bancária para validar adimplência e inadimplência.
    """
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.tolerance_amount = 5.0  # Tolerância de R$ 5,00 para diferenças
        self.tolerance_days = 3  # Tolerância de 3 dias para datas
        
        # Padrões para identificar pagamentos
        self.payment_patterns = [
            r'PIX.*?(\d{3}\.\d{3}\.\d{3}-\d{2})',  # PIX com CPF
            r'TED.*?(\d+)',  # TED
            r'BOLETO.*?(\d+)',  # Boleto
            r'CARTAO.*?(\d+)',  # Cartão
            r'TRANSFERENCIA.*?(\d+)',  # Transferência
        ]
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o sistema de logging."""
        logger = logging.getLogger('BankReconciliation')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_bank_extract(self, file_path: str = None, data: pd.DataFrame = None) -> List[BankTransaction]:
        """
        Carrega extrato bancário de arquivo ou DataFrame.
        
        Args:
            file_path: Caminho para arquivo CSV/Excel do extrato
            data: DataFrame com dados do extrato
            
        Returns:
            Lista de transações bancárias
        """
        try:
            if file_path:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
            elif data is not None:
                df = data.copy()
            else:
                # Gerar dados de exemplo para demonstração
                df = self._generate_sample_bank_data()
            
            transactions = []
            
            for _, row in df.iterrows():
                try:
                    # Mapear colunas (ajustar conforme formato do banco)
                    date = pd.to_datetime(row.get('data', row.get('Data', row.get('date'))))
                    valor_raw = str(row.get('valor', row.get('Valor', row.get('amount', 0))))
                    amount = float(valor_raw.replace('R$', '').replace(',', '.').strip())
                    description = str(row.get('descricao', row.get('Descricao', row.get('description', ''))))
                    document = str(row.get('documento', row.get('Documento', row.get('document', ''))))
                    account = str(row.get('conta', row.get('Conta', row.get('account', ''))))
                    tx_type = 'credit' if amount > 0 else 'debit'
                    
                    transaction = BankTransaction(
                        date=date,
                        amount=abs(amount),
                        description=description,
                        document=document,
                        account=account,
                        type=tx_type
                    )
                    
                    transactions.append(transaction)
                    
                except Exception as e:
                    self.logger.warning(f"Erro ao processar linha do extrato: {e}")
                    continue
            
            self.logger.info(f"Carregadas {len(transactions)} transações bancárias")
            return transactions
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar extrato bancário: {e}")
            return []
    
    def _generate_sample_bank_data(self) -> pd.DataFrame:
        """Gera dados bancários de exemplo para demonstração."""
        np.random.seed(42)
        
        # Datas dos últimos 30 dias
        base_date = datetime.now() - timedelta(days=30)
        dates = [base_date + timedelta(days=i) for i in range(30)]
        
        transactions = []
        
        for i, date in enumerate(dates):
            # Simular alguns pagamentos de alunos
            if np.random.random() > 0.7:  # 30% chance de pagamento por dia
                # Pagamento por PIX
                transactions.append({
                    'data': date.strftime('%Y-%m-%d'),
                    'valor': f"R$ {np.random.choice([400, 500, 600, 350]):.2f}",
                    'descricao': f'PIX RECEBIDO - {np.random.choice(["FERNANDA SILVA", "JOAO SANTOS", "MARIA OLIVEIRA", "PEDRO COSTA"])}',
                    'documento': f'{np.random.randint(100000, 999999)}',
                    'conta': 'Conta Corrente',
                    'tipo': 'credit'
                })
            
            # Simular boletos
            if np.random.random() > 0.8:  # 20% chance de boleto por dia
                transactions.append({
                    'data': date.strftime('%Y-%m-%d'),
                    'valor': f"R$ {np.random.choice([400, 500]):.2f}",
                    'descricao': f'BOLETO PAGO - FAC {np.random.choice([17, 18, 19])}',
                    'documento': f'BOL{np.random.randint(10000, 99999)}',
                    'conta': 'Conta Corrente',
                    'tipo': 'credit'
                })
            
            # Simular despesas
            if np.random.random() > 0.85:  # 15% chance de despesa por dia
                transactions.append({
                    'data': date.strftime('%Y-%m-%d'),
                    'valor': f"R$ -{np.random.choice([150, 200, 300, 500]):.2f}",
                    'descricao': f'{np.random.choice(["FORNECEDOR", "MARKETING", "INFRAESTRUTURA", "SALARIOS"])}',
                    'documento': f'DEB{np.random.randint(1000, 9999)}',
                    'conta': 'Conta Corrente',
                    'tipo': 'debit'
                })
        
        return pd.DataFrame(transactions)
    
    def generate_expected_payments(self, students_data: pd.DataFrame) -> List[StudentPayment]:
        """
        Gera lista de pagamentos esperados baseado nos dados dos alunos.
        
        Args:
            students_data: DataFrame com dados dos alunos
            
        Returns:
            Lista de pagamentos esperados
        """
        expected_payments = []
        
        try:
            for _, student in students_data.iterrows():
                student_id = str(student.get('id', ''))
                student_name = student.get('fullName', student.get('name', ''))
                payment_method = student.get('paymentMethod', 'BOLETO')
                course_fee = float(student.get('courseFee', 400))
                total_installments = int(student.get('totalInstallments', 10))
                boleto_due_date = int(student.get('boletoDueDate', 10))
                
                # Gerar parcelas esperadas
                enrollment_date = datetime.now() - timedelta(days=np.random.randint(1, 90))
                
                for i in range(total_installments):
                    # Calcular data de vencimento
                    due_date = enrollment_date + timedelta(days=30*i)
                    due_date = due_date.replace(day=boleto_due_date)
                    
                    # Determinar status baseado na data
                    if due_date < datetime.now() - timedelta(days=5):
                        status = 'overdue'
                    elif due_date < datetime.now():
                        status = 'paid' if np.random.random() > 0.3 else 'overdue'
                    else:
                        status = 'pending'
                    
                    payment = StudentPayment(
                        student_id=student_id,
                        student_name=student_name,
                        installment_number=i + 1,
                        due_date=due_date,
                        amount=course_fee / total_installments,
                        payment_method=payment_method,
                        status=status
                    )
                    
                    expected_payments.append(payment)
            
            self.logger.info(f"Gerados {len(expected_payments)} pagamentos esperados")
            return expected_payments
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar pagamentos esperados: {e}")
            return []
    
    def reconcile_payments(self, bank_transactions: List[BankTransaction], 
                          expected_payments: List[StudentPayment]) -> Dict:
        """
        Executa conciliação entre transações bancárias e pagamentos esperados.
        
        Args:
            bank_transactions: Lista de transações bancárias
            expected_payments: Lista de pagamentos esperados
            
        Returns:
            Resultado da conciliação
        """
        try:
            # Filtrar apenas créditos (recebimentos)
            credits = [tx for tx in bank_transactions if tx.type == 'credit']
            
            matched_payments = []
            unmatched_transactions = []
            unpaid_installments = []
            
            # Tentar fazer correspondência de cada transação
            for transaction in credits:
                best_match = None
                best_score = 0
                
                for payment in expected_payments:
                    if payment.status == 'paid':
                        continue
                    
                    score = self._calculate_match_score(transaction, payment)
                    
                    if score > best_score and score > 0.6:  # Threshold de 60%
                        best_score = score
                        best_match = payment
                
                if best_match:
                    matched_payments.append({
                        'transaction': transaction,
                        'payment': best_match,
                        'match_score': best_score
                    })
                    best_match.status = 'paid'
                else:
                    unmatched_transactions.append(transaction)
            
            # Identificar pagamentos não quitados
            for payment in expected_payments:
                if payment.status in ['pending', 'overdue']:
                    unpaid_installments.append(payment)
            
            # Calcular métricas
            total_expected = len(expected_payments)
            total_paid = len(matched_payments)
            total_overdue = len([p for p in expected_payments if p.status == 'overdue'])
            
            adimplencia_rate = (total_paid / total_expected * 100) if total_expected > 0 else 0
            inadimplencia_rate = (total_overdue / total_expected * 100) if total_expected > 0 else 0
            
            self.logger.info(f"Conciliação concluída: {total_paid}/{total_expected} pagamentos identificados")
            
            return {
                'matched_payments': matched_payments,
                'unmatched_transactions': unmatched_transactions,
                'unpaid_installments': unpaid_installments,
                'metrics': {
                    'total_expected': total_expected,
                    'total_paid': total_paid,
                    'total_overdue': total_overdue,
                    'adimplencia_rate': adimplencia_rate,
                    'inadimplencia_rate': inadimplencia_rate,
                    'unmatched_transactions_count': len(unmatched_transactions),
                    'total_amount_received': sum(tx.amount for tx in credits),
                    'total_amount_expected': sum(p.amount for p in expected_payments),
                    'total_amount_overdue': sum(p.amount for p in unpaid_installments if p.status == 'overdue')
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erro na conciliação: {e}")
            return {}
    
    def _calculate_match_score(self, transaction: BankTransaction, payment: StudentPayment) -> float:
        """
        Calcula score de correspondência entre transação e pagamento.
        
        Returns:
            Score de 0 a 1
        """
        score = 0.0
        
        # Score por valor (40% do peso)
        amount_diff = abs(transaction.amount - payment.amount)
        if amount_diff <= self.tolerance_amount:
            score += 0.4 * (1 - amount_diff / self.tolerance_amount)
        
        # Score por data (30% do peso)
        date_diff = abs((transaction.date - payment.due_date).days)
        if date_diff <= self.tolerance_days:
            score += 0.3 * (1 - date_diff / self.tolerance_days)
        
        # Score por nome/descrição (30% do peso)
        name_words = payment.student_name.upper().split()
        description_upper = transaction.description.upper()
        
        name_matches = sum(1 for word in name_words if word in description_upper)
        if name_matches > 0:
            score += 0.3 * (name_matches / len(name_words))
        
        return min(score, 1.0)
    
    def generate_reconciliation_report(self, reconciliation_result: Dict) -> pd.DataFrame:
        """
        Gera relatório detalhado da conciliação.
        
        Args:
            reconciliation_result: Resultado da conciliação
            
        Returns:
            DataFrame com relatório
        """
        try:
            report_data = []
            
            # Pagamentos identificados
            for match in reconciliation_result.get('matched_payments', []):
                transaction = match['transaction']
                payment = match['payment']
                
                report_data.append({
                    'Tipo': 'Pagamento Identificado',
                    'Aluno': payment.student_name,
                    'Parcela': f"{payment.installment_number}/{payment.amount:.2f}",
                    'Data_Vencimento': payment.due_date.strftime('%d/%m/%Y'),
                    'Data_Pagamento': transaction.date.strftime('%d/%m/%Y'),
                    'Valor_Esperado': payment.amount,
                    'Valor_Recebido': transaction.amount,
                    'Diferenca': transaction.amount - payment.amount,
                    'Score_Match': f"{match['match_score']:.2%}",
                    'Status': '✅ Pago',
                    'Observacoes': transaction.description[:50]
                })
            
            # Pagamentos em atraso
            for payment in reconciliation_result.get('unpaid_installments', []):
                if payment.status == 'overdue':
                    days_overdue = (datetime.now() - payment.due_date).days
                    
                    report_data.append({
                        'Tipo': 'Inadimplência',
                        'Aluno': payment.student_name,
                        'Parcela': f"{payment.installment_number}/{payment.amount:.2f}",
                        'Data_Vencimento': payment.due_date.strftime('%d/%m/%Y'),
                        'Data_Pagamento': '',
                        'Valor_Esperado': payment.amount,
                        'Valor_Recebido': 0,
                        'Diferenca': -payment.amount,
                        'Score_Match': '',
                        'Status': f'❌ Atraso ({days_overdue}d)',
                        'Observacoes': f'Vencido há {days_overdue} dias'
                    })
            
            # Transações não identificadas
            for transaction in reconciliation_result.get('unmatched_transactions', []):
                report_data.append({
                    'Tipo': 'Recebimento Não Identificado',
                    'Aluno': 'Não Identificado',
                    'Parcela': '',
                    'Data_Vencimento': '',
                    'Data_Pagamento': transaction.date.strftime('%d/%m/%Y'),
                    'Valor_Esperado': 0,
                    'Valor_Recebido': transaction.amount,
                    'Diferenca': transaction.amount,
                    'Score_Match': '',
                    'Status': '⚠️ Não Identificado',
                    'Observacoes': transaction.description[:50]
                })
            
            return pd.DataFrame(report_data)
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            return pd.DataFrame()
    
    def generate_dashboard_metrics(self, reconciliation_result: Dict) -> Dict:
        """
        Gera métricas para dashboard de adimplência.
        
        Args:
            reconciliation_result: Resultado da conciliação
            
        Returns:
            Dicionário com métricas
        """
        try:
            metrics = reconciliation_result.get('metrics', {})
            
            return {
                'adimplencia': {
                    'rate': metrics.get('adimplencia_rate', 0),
                    'count': metrics.get('total_paid', 0),
                    'amount': sum(match['transaction'].amount for match in reconciliation_result.get('matched_payments', []))
                },
                'inadimplencia': {
                    'rate': metrics.get('inadimplencia_rate', 0),
                    'count': metrics.get('total_overdue', 0),
                    'amount': metrics.get('total_amount_overdue', 0)
                },
                'conciliacao': {
                    'total_transacoes': len(reconciliation_result.get('unmatched_transactions', [])) + len(reconciliation_result.get('matched_payments', [])),
                    'transacoes_identificadas': len(reconciliation_result.get('matched_payments', [])),
                    'transacoes_nao_identificadas': len(reconciliation_result.get('unmatched_transactions', [])),
                    'taxa_identificacao': (len(reconciliation_result.get('matched_payments', [])) / max(1, len(reconciliation_result.get('unmatched_transactions', [])) + len(reconciliation_result.get('matched_payments', [])))) * 100
                },
                'financeiro': {
                    'total_recebido': metrics.get('total_amount_received', 0),
                    'total_esperado': metrics.get('total_amount_expected', 0),
                    'total_em_atraso': metrics.get('total_amount_overdue', 0),
                    'eficiencia_cobranca': ((metrics.get('total_amount_received', 0) / max(1, metrics.get('total_amount_expected', 1))) * 100)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar métricas: {e}")
            return {}