import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid

class AdvancedDataHandler:
    """
    Versão avançada do manipulador de dados baseada no sistema React original.
    Inclui funcionalidades completas de gestão de alunos, cursos e pagamentos.
    """
    
    def __init__(self):
        """Inicializa o manipulador avançado de dados."""
        self.logger = self._setup_logger()
        
        # DataFrames principais
        self.students_df = pd.DataFrame()
        self.courses_df = pd.DataFrame()
        self.facs_df = pd.DataFrame()
        self.payments_df = pd.DataFrame()
        self.users_df = pd.DataFrame()
        
        # Constantes baseadas no sistema React
        self.HOW_FOUND_OPTIONS = [
            'Facebook', 'Instagram', 'Google', 'Indicação', 'YouTube', 
            'LinkedIn', 'WhatsApp', 'Site', 'Outros'
        ]
        
        self.ENROLLMENT_STATUS_OPTIONS = [
            'Matriculado', 'Aguardando Pagamento', 'Em Análise', 
            'Cancelado', 'Concluído', 'Trancado'
        ]
        
        self.PAYMENT_METHOD_OPTIONS = [
            'BOLETO', 'PIX', 'CARTAO_CREDITO', 'CARTAO_DEBITO', 'TRANSFERENCIA'
        ]
        
        self.BOLETO_DUE_DATE_OPTIONS = [
            '05', '10', '15', '20', '25', '30'
        ]
        
        self.STATES_BR = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        
        # Inicializar dados
        self._initialize_data()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o sistema de logging."""
        logger = logging.getLogger('AdvancedDataHandler')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_data(self):
        """Inicializa os dados básicos do sistema."""
        try:
            # Inicializar cursos
            self._create_courses_data()
            
            # Inicializar FACs (turmas)
            self._create_facs_data()
            
            # Inicializar alguns alunos de exemplo
            self._create_sample_students()
            
            self.logger.info("Dados inicializados com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao inicializar dados: {str(e)}")
    
    def _create_courses_data(self):
        """Cria dados dos cursos disponíveis."""
        courses_data = [
            {
                'id': 'COURSE_001',
                'name': 'Formação Analista Comportamental',
                'description': 'Curso completo de análise comportamental aplicada',
                'defaultFee': 400.0,
                'defaultInstallments': 10,
                'duration': 120,  # horas
                'modality': 'Online',
                'status': 'Ativo'
            },
            {
                'id': 'COURSE_002', 
                'name': 'Gestão de Pessoas',
                'description': 'Curso de gestão e desenvolvimento de pessoas',
                'defaultFee': 350.0,
                'defaultInstallments': 8,
                'duration': 80,
                'modality': 'Online',
                'status': 'Ativo'
            }
        ]
        
        self.courses_df = pd.DataFrame(courses_data)
    
    def _create_facs_data(self):
        """Cria dados das turmas (FACs)."""
        facs_data = [
            {
                'code': 'FAC_17',
                'name': 'Turma 17 - Analista Comportamental',
                'startDate': '2024-04-01',
                'endDate': '2024-06-30',
                'status': 'Em Andamento',
                'maxStudents': 30,
                'currentStudents': 26
            },
            {
                'code': 'FAC_16',
                'name': 'Turma 16 - Analista Comportamental', 
                'startDate': '2024-03-01',
                'endDate': '2024-05-31',
                'status': 'Concluído',
                'maxStudents': 25,
                'currentStudents': 16
            },
            {
                'code': 'FAC_15',
                'name': 'Turma 15 - Analista Comportamental',
                'startDate': '2024-02-01', 
                'endDate': '2024-04-30',
                'status': 'Concluído',
                'maxStudents': 25,
                'currentStudents': 18
            }
        ]
        
        self.facs_df = pd.DataFrame(facs_data)
    
    def _create_sample_students(self):
        """Cria alguns alunos de exemplo baseados nos dados reais do PDF."""
        sample_students = [
            {
                'id': self._generate_student_id(),
                'fullName': 'Fernanda Passos Silva dos Santos',
                'email': 'gs2fernanda@gmail.com',
                'cpfCnpj': '05595210575',
                'certificateName': 'Fernanda Passos Silva dos Santos',
                'profession': 'Analista de RH',
                'phone': '71992509996',
                'whatsapp': '71992509996',
                'cep': '42800-000',
                'address': 'Rua das Flores',
                'addressNumber': '123',
                'addressComplement': 'Apt 101',
                'neighborhood': 'Centro',
                'city': 'Camaçari',
                'state': 'BA',
                'chosenCourseName': 'Formação Analista Comportamental',
                'facCode': 'FAC_17',
                'paymentMethod': 'BOLETO',
                'totalInstallments': 10,
                'courseFee': 400.0,
                'boletoDueDate': '10',
                'howFound': 'Facebook',
                'enrollmentStatus': 'Matriculado',
                'timestamp': datetime.now().isoformat(),
                'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'id': self._generate_student_id(),
                'fullName': 'Nathalia da Silva Bezerra', 
                'email': 'nathalia.s.beze@gmail.com',
                'cpfCnpj': '38157732883',
                'certificateName': 'Nathalia da Silva Bezerra',
                'profession': 'Coordenadora de Recursos Humanos',
                'phone': '11989359930',
                'whatsapp': '11989359930',
                'cep': '06010-000',
                'address': 'Avenida das Palmeiras',
                'addressNumber': '456',
                'addressComplement': '',
                'neighborhood': 'Vila Nova',
                'city': 'Osasco',
                'state': 'SP',
                'chosenCourseName': 'Formação Analista Comportamental',
                'facCode': 'FAC_17',
                'paymentMethod': 'PIX',
                'totalInstallments': 8,
                'courseFee': 400.0,
                'boletoDueDate': '15',
                'howFound': 'Instagram',
                'enrollmentStatus': 'Matriculado',
                'timestamp': datetime.now().isoformat(),
                'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        
        self.students_df = pd.DataFrame(sample_students)
        
        # Gerar parcelas para os alunos de exemplo
        for student in sample_students:
            self._generate_payment_installments(student)
    
    def _generate_student_id(self) -> str:
        """Gera um ID único para o aluno."""
        return f"STU_{str(uuid.uuid4())[:8].upper()}"
    
    def _generate_payment_installments(self, student_data: Dict) -> List[Dict]:
        """
        Gera as parcelas de pagamento para um aluno.
        
        Args:
            student_data: Dados do aluno
            
        Returns:
            Lista de parcelas geradas
        """
        try:
            installments = []
            student_id = student_data['id']
            total_fee = student_data['courseFee']
            num_installments = student_data['totalInstallments']
            due_day = int(student_data['boletoDueDate'])
            
            # Calcular valor da parcela
            installment_value = total_fee / num_installments
            
            # Data base para primeira parcela (próximo dia de vencimento)
            today = datetime.now()
            if today.day <= due_day:
                first_due = today.replace(day=due_day)
            else:
                if today.month == 12:
                    first_due = today.replace(year=today.year + 1, month=1, day=due_day)
                else:
                    first_due = today.replace(month=today.month + 1, day=due_day)
            
            # Gerar cada parcela
            for i in range(num_installments):
                due_date = first_due + timedelta(days=30 * i)
                
                installment = {
                    'id': f"PAY_{student_id}_{i+1:02d}",
                    'student_id': student_id,
                    'installment_number': i + 1,
                    'total_installments': num_installments,
                    'amount': round(installment_value, 2),
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'payment_date': None,
                    'status': 'Pendente',  # Pendente, Pago, Atrasado, Cancelado
                    'payment_method': student_data['paymentMethod'],
                    'barcode': None,  # Para boletos
                    'transaction_id': None,
                    'created_at': datetime.now().isoformat()
                }
                
                installments.append(installment)
            
            # Adicionar ao DataFrame de pagamentos
            new_payments = pd.DataFrame(installments)
            self.payments_df = pd.concat([self.payments_df, new_payments], ignore_index=True)
            
            self.logger.info(f"Geradas {len(installments)} parcelas para {student_data['fullName']}")
            return installments
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar parcelas: {str(e)}")
            return []
    
    def create_student(self, student_data: Dict) -> bool:
        """
        Cria um novo aluno com dados do formulário online.
        
        Args:
            student_data: Dados do aluno do formulário
            
        Returns:
            True se criado com sucesso
        """
        try:
            # Mapear dados do formulário para formato interno
            internal_data = {
                'fullName': student_data.get('fullName', ''),
                'email': student_data.get('email', ''),
                'phone': student_data.get('phone', ''),
                'cpfCnpj': student_data.get('cpf', ''),
                'certificateName': student_data.get('fullName', ''),
                'profession': 'Não informado',
                'whatsapp': student_data.get('phone', ''),
                'cep': student_data.get('zipCode', ''),
                'address': student_data.get('address', ''),
                'addressNumber': '',
                'addressComplement': '',
                'neighborhood': '',
                'city': student_data.get('city', ''),
                'state': student_data.get('state', ''),
                'chosenCourseName': student_data.get('courseName', ''),
                'facCode': f"FAC_{student_data.get('courseName', '')[:3].upper()}",
                'paymentMethod': student_data.get('paymentMethod', 'BOLETO'),
                'totalInstallments': int(student_data.get('installments', 1)),
                'courseFee': float(student_data.get('courseFee', 0)),
                'boletoDueDate': '10',
                'howFound': student_data.get('howFound', 'Internet'),
                'enrollmentStatus': 'Matriculado'
            }
            
            return self.add_student(internal_data)
            
        except Exception as e:
            self.logger.error(f"Erro ao criar aluno: {str(e)}")
            return False

    def add_student(self, student_data: Dict) -> bool:
        """
        Adiciona um novo aluno com dados completos.
        
        Args:
            student_data: Dicionário com dados do aluno
            
        Returns:
            True se adicionado com sucesso
        """
        try:
            # Validar dados obrigatórios
            required_fields = ['fullName', 'email', 'phone']
            for field in required_fields:
                if not student_data.get(field):
                    raise ValueError(f"Campo obrigatório '{field}' não fornecido")
            
            # Gerar ID único
            student_id = self._generate_student_id()
            
            # Dados completos do aluno
            complete_student = {
                'id': student_id,
                'fullName': student_data.get('fullName', ''),
                'email': student_data.get('email', ''),
                'cpfCnpj': student_data.get('cpfCnpj', ''),
                'certificateName': student_data.get('certificateName', student_data.get('fullName', '')),
                'profession': student_data.get('profession', ''),
                'phone': student_data.get('phone', ''),
                'whatsapp': student_data.get('whatsapp', student_data.get('phone', '')),
                'cep': student_data.get('cep', ''),
                'address': student_data.get('address', ''),
                'addressNumber': student_data.get('addressNumber', ''),
                'addressComplement': student_data.get('addressComplement', ''),
                'neighborhood': student_data.get('neighborhood', ''),
                'city': student_data.get('city', ''),
                'state': student_data.get('state', 'SP'),
                'chosenCourseName': student_data.get('chosenCourseName', ''),
                'facCode': student_data.get('facCode', ''),
                'paymentMethod': student_data.get('paymentMethod', 'BOLETO'),
                'totalInstallments': int(student_data.get('totalInstallments', 10)),
                'courseFee': float(student_data.get('courseFee', 0)),
                'boletoDueDate': student_data.get('boletoDueDate', '10'),
                'howFound': student_data.get('howFound', 'Internet'),
                'enrollmentStatus': student_data.get('enrollmentStatus', 'Matriculado'),
                'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': datetime.now().isoformat()
            }
            
            # Adicionar ao DataFrame
            new_student = pd.DataFrame([complete_student])
            self.students_df = pd.concat([self.students_df, new_student], ignore_index=True)
            
            # Gerar parcelas de pagamento
            self._generate_payment_installments(complete_student)
            
            self.logger.info(f"Aluno {complete_student['fullName']} adicionado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar aluno: {str(e)}")
            return False
    
    def update_student(self, student_id: str, updated_data: Dict) -> bool:
        """
        Atualiza dados de um aluno existente.
        
        Args:
            student_id: ID do aluno
            updated_data: Dados atualizados
            
        Returns:
            True se atualizado com sucesso
        """
        try:
            # Verificar se aluno existe
            student_idx = self.students_df[self.students_df['id'] == student_id].index
            
            if len(student_idx) == 0:
                raise ValueError(f"Aluno com ID {student_id} não encontrado")
            
            # Atualizar dados
            for field, value in updated_data.items():
                if field in self.students_df.columns:
                    self.students_df.loc[student_idx[0], field] = value
            
            # Atualizar timestamp
            self.students_df.loc[student_idx[0], 'timestamp'] = datetime.now().isoformat()
            
            self.logger.info(f"Aluno {student_id} atualizado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao atualizar aluno: {str(e)}")
            return False
    
    def delete_student(self, student_id: str) -> bool:
        """
        Remove um aluno do sistema.
        
        Args:
            student_id: ID do aluno
            
        Returns:
            True se removido com sucesso
        """
        try:
            # Verificar se aluno existe
            student_exists = self.students_df['id'] == student_id
            
            if not student_exists.any():
                raise ValueError(f"Aluno com ID {student_id} não encontrado")
            
            # Remover aluno
            self.students_df = self.students_df[~student_exists]
            
            # Remover parcelas relacionadas
            self.payments_df = self.payments_df[self.payments_df['student_id'] != student_id]
            
            self.logger.info(f"Aluno {student_id} removido com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao remover aluno: {str(e)}")
            return False
    
    def get_student_by_id(self, student_id: str) -> Optional[Dict]:
        """
        Obtém dados de um aluno específico.
        
        Args:
            student_id: ID do aluno
            
        Returns:
            Dicionário com dados do aluno ou None
        """
        try:
            student_data = self.students_df[self.students_df['id'] == student_id]
            
            if student_data.empty:
                return None
            
            return student_data.iloc[0].to_dict()
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar aluno: {str(e)}")
            return None
    
    def get_all_students(self) -> pd.DataFrame:
        """Retorna todos os alunos."""
        return self.students_df.copy()
    
    def get_students_by_fac(self, fac_code: str) -> pd.DataFrame:
        """
        Retorna alunos de uma turma específica.
        
        Args:
            fac_code: Código da turma
            
        Returns:
            DataFrame com alunos da turma
        """
        return self.students_df[self.students_df['facCode'] == fac_code].copy()
    
    def get_payment_installments(self, student_id: str) -> pd.DataFrame:
        """
        Retorna parcelas de pagamento de um aluno.
        
        Args:
            student_id: ID do aluno
            
        Returns:
            DataFrame com parcelas
        """
        return self.payments_df[self.payments_df['student_id'] == student_id].copy()
    
    def update_payment_status(self, payment_id: str, status: str, payment_date: Optional[str] = None) -> bool:
        """
        Atualiza status de um pagamento.
        
        Args:
            payment_id: ID do pagamento
            status: Novo status
            payment_date: Data do pagamento (se pago)
            
        Returns:
            True se atualizado com sucesso
        """
        try:
            payment_idx = self.payments_df[self.payments_df['id'] == payment_id].index
            
            if len(payment_idx) == 0:
                raise ValueError(f"Pagamento {payment_id} não encontrado")
            
            self.payments_df.loc[payment_idx[0], 'status'] = status
            
            if payment_date:
                self.payments_df.loc[payment_idx[0], 'payment_date'] = payment_date
            
            self.logger.info(f"Status do pagamento {payment_id} atualizado para {status}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao atualizar pagamento: {str(e)}")
            return False
    
    def get_financial_summary(self) -> Dict:
        """Retorna resumo financeiro geral."""
        try:
            total_students = len(self.students_df)
            total_revenue = self.payments_df['amount'].sum()
            paid_payments = self.payments_df[self.payments_df['status'] == 'Pago']
            total_paid = paid_payments['amount'].sum()
            pending_payments = self.payments_df[self.payments_df['status'] == 'Pendente']
            total_pending = pending_payments['amount'].sum()
            
            # Calcular inadimplência (pagamentos em atraso)
            today = datetime.now().strftime('%Y-%m-%d')
            overdue_payments = self.payments_df[
                (self.payments_df['status'] == 'Pendente') & 
                (self.payments_df['due_date'] < today)
            ]
            total_overdue = overdue_payments['amount'].sum()
            
            return {
                'total_students': total_students,
                'total_revenue': total_revenue,
                'total_paid': total_paid,
                'total_pending': total_pending,
                'total_overdue': total_overdue,
                'payment_rate': (total_paid / total_revenue * 100) if total_revenue > 0 else 0,
                'overdue_rate': (total_overdue / total_revenue * 100) if total_revenue > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo financeiro: {str(e)}")
            return {}
    
    def get_courses(self) -> pd.DataFrame:
        """Retorna lista de cursos."""
        return self.courses_df.copy()
    
    def get_facs(self) -> pd.DataFrame:
        """Retorna lista de turmas (FACs)."""
        return self.facs_df.copy()
    
    def export_students_to_excel(self, file_path: str) -> bool:
        """
        Exporta dados dos alunos para Excel.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se exportado com sucesso
        """
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                self.students_df.to_excel(writer, sheet_name='Alunos', index=False)
                self.payments_df.to_excel(writer, sheet_name='Pagamentos', index=False)
                self.facs_df.to_excel(writer, sheet_name='Turmas', index=False)
                self.courses_df.to_excel(writer, sheet_name='Cursos', index=False)
            
            self.logger.info(f"Dados exportados para {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar dados: {str(e)}")
            return False