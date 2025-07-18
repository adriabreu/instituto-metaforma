import pandas as pd
import json
import os
from typing import Dict, List, Optional, Tuple
import logging

class DataHandler:
    """
    Classe responsável por gerenciar os dados do sistema Instituto Metaforma.
    Manipula dados financeiros, de alunos e gera relatórios.
    """
    
    def __init__(self):
        """Inicializa o manipulador de dados."""
        self.financial_data = pd.DataFrame()
        self.student_data = pd.DataFrame()
        self.courses_data = pd.DataFrame()
        self.logger = self._setup_logger()
        self._load_sample_data()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o sistema de logging."""
        logger = logging.getLogger('DataHandler')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_sample_data(self):
        """Carrega dados de exemplo baseados nos PDFs fornecidos."""
        try:
            # Dados financeiros baseados no PDF
            self.financial_data = self._create_financial_data()
            
            # Dados dos alunos baseados no PDF de inscrições
            self.student_data = self._create_student_data()
            
            # Dados dos cursos
            self.courses_data = self._create_courses_data()
            
            self.logger.info("Dados de exemplo carregados com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados de exemplo: {str(e)}")
    
    def _create_financial_data(self) -> pd.DataFrame:
        """Cria DataFrame com dados financeiros baseados no PDF."""
        financial_data = {
            'Periodo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Tipo': ['Realizado', 'Realizado', 'Realizado', 'Realizado'],
            'Receita_Bruta': [3589.0, 3760.0, 7105.0, 9894.0],
            'Inadimplencia': [2910.0, 0.0, 291.0, 2328.0],
            'Receita_Liquida': [679.0, 3760.0, 6814.0, 7566.0],
            'Facebook_Anuncios': [3000.0, 2100.0, 2100.0, 3000.0],
            'Creditos_Plataforma': [1305.2, 803.2, 903.6, 1104.4],
            'Boletos': [1167.7, 159.7, 449.1, 659.9],
            'Gestor_Trafego': [600.0, 600.0, 600.0, 600.0],
            'Total_Despesas': [6072.9, 3662.9, 4052.7, 5364.3],
            'Resultado_Bruto': [-5393.9, 97.1, 2761.3, 2201.7],
            'Comissao': [-2696.9, 48.6, 1380.7, 1100.9],
            'Resultado_Liquido': [-2696.9, 48.6, 1380.7, 1100.9]
        }
        
        # Adicionar dados de orçamento
        orcamento_data = {
            'Periodo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Tipo': ['Orcamento', 'Orcamento', 'Orcamento', 'Orcamento'],
            'Receita_Bruta': [25220.0, 15400.0, 17290.0, 20370.0],
            'Inadimplencia': [0.0, 0.0, 0.0, 0.0],
            'Receita_Liquida': [25220.0, 15400.0, 17290.0, 20370.0],
            'Facebook_Anuncios': [0.0, 2100.0, 2100.0, 3000.0],
            'Creditos_Plataforma': [0.0, 803.2, 903.6, 1104.4],
            'Boletos': [0.0, 798.4, 988.0, 1099.8],
            'Gestor_Trafego': [0.0, 600.0, 600.0, 600.0],
            'Total_Despesas': [0.0, 4301.6, 4591.6, 5804.2],
            'Resultado_Bruto': [25220.0, 11098.4, 12698.4, 14565.8],
            'Comissao': [2522.0, 5549.2, 6349.2, 7282.9],
            'Resultado_Liquido': [22698.0, 5549.2, 6349.2, 7282.9]
        }
        
        # Combinar dados realizados e orçamento
        df_realizado = pd.DataFrame(financial_data)
        df_orcamento = pd.DataFrame(orcamento_data)
        
        return pd.concat([df_realizado, df_orcamento], ignore_index=True)
    
    def _create_student_data(self) -> pd.DataFrame:
        """Cria DataFrame com dados dos alunos baseados no PDF."""
        student_data = {
            'ID': range(1, 9),
            'Nome': [
                'Fernanda Passos Silva dos Santos',
                'Nathalia da Silva Bezerra',
                'Áurea Cristina de Oliveira Aguiar',
                'Diane Machado',
                'Kathleen Julianna M Sampaio Interaminsense',
                'Ruan Macedo Santana',
                'Paula Nunes Vieira Silva',
                'Lilian Jane de Menezes Farias'
            ],
            'Email': [
                'gs2fernanda@gmail.com',
                'nathalia.s.beze@gmail.com',
                'aureaaguiar30@gmail.com',
                'dihmachado81@gmail.com',
                'kathleensampa@hotmail.com',
                'ruan.macedo48@gmail.com',
                'paulanunes.adm22@gmail.com',
                'lilianjane1980@gmail.com'
            ],
            'CPF': [
                '05595210575',
                '38157732883',
                '403.323.222.20',
                '02375186001',
                '08264603483',
                '01755332106',
                '105.162.366-95',
                '00542224518'
            ],
            'Telefone': [
                '71992509996',
                '11989359930',
                '91981129597',
                '55981524180',
                '81996793483',
                '61993279632',
                '(38)99944-7822',
                '73988443997'
            ],
            'Cidade': [
                'Camaçari',
                'Osasco',
                'Ananindeua',
                'Eugênio De Castro',
                'Recife',
                'Goianésia',
                'Paracatu',
                'Tijucas'
            ],
            'Estado': ['BA', 'SP', 'PA', 'RS', 'PE', 'GO', 'MG', 'SC'],
            'Curso': ['Formação Analista Comportamental'] * 8,
            'Data_Inscricao': [
                '15/04/2024',
                '23/04/2024',
                '27/04/2024',
                '06/05/2024',
                '15/05/2024',
                '20/05/2024',
                '20/05/2024',
                '20/05/2024'
            ],
            'Profissao': [
                'Analista de RH',
                'Coordenadora de Recursos Humanos',
                'Professora de Gestão',
                'Terapeuta',
                'Gestora de RH',
                'Gerente',
                'Assistente de Recursos Humanos I',
                'Analista de RH'
            ],
            'Status': ['Ativo'] * 8,
            'Valor_Pago': [300.0, 350.0, 400.0, 250.0, 300.0, 450.0, 200.0, 300.0]
        }
        
        return pd.DataFrame(student_data)
    
    def _create_courses_data(self) -> pd.DataFrame:
        """Cria DataFrame com dados dos cursos."""
        courses_data = {
            'Codigo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Nome': ['Formação Analista Comportamental'] * 4,
            'Data_Inicio': ['01/04/2024', '01/03/2024', '01/02/2024', '01/01/2024'],
            'Data_Fim': ['30/06/2024', '31/05/2024', '30/04/2024', '31/03/2024'],
            'Valor_Curso': [400.0, 350.0, 400.0, 450.0],
            'Total_Alunos': [26, 16, 18, 21],
            'Status': ['Em Andamento', 'Concluído', 'Concluído', 'Concluído'],
            'Modalidade': ['Online'] * 4,
            'Carga_Horaria': [120, 120, 120, 120]
        }
        
        return pd.DataFrame(courses_data)
    
    def get_financial_summary(self, period: Optional[str] = None) -> Dict:
        """
        Retorna resumo financeiro para um período específico ou todos.
        
        Args:
            period: Período específico (ex: 'FAC_17') ou None para todos
            
        Returns:
            Dicionário com resumo financeiro
        """
        try:
            df = self.financial_data.copy()
            
            if period:
                df = df[df['Periodo'] == period]
            
            if df.empty:
                return {'error': 'Nenhum dado encontrado para o período especificado'}
            
            # Separar dados realizados e orçados
            realizados = df[df['Tipo'] == 'Realizado']
            orcados = df[df['Tipo'] == 'Orcamento']
            
            summary = {
                'receita_realizada': realizados['Receita_Bruta'].sum(),
                'receita_orcada': orcados['Receita_Bruta'].sum(),
                'resultado_realizado': realizados['Resultado_Liquido'].sum(),
                'resultado_orcado': orcados['Resultado_Liquido'].sum(),
                'inadimplencia_total': realizados['Inadimplencia'].sum(),
                'despesas_totais': realizados['Total_Despesas'].sum(),
                'taxa_inadimplencia': (realizados['Inadimplencia'].sum() / realizados['Receita_Bruta'].sum() * 100) if realizados['Receita_Bruta'].sum() > 0 else 0
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo financeiro: {str(e)}")
            return {'error': str(e)}
    
    def get_student_statistics(self) -> Dict:
        """
        Retorna estatísticas dos alunos cadastrados.
        
        Returns:
            Dicionário com estatísticas dos alunos
        """
        try:
            df = self.student_data.copy()
            
            if df.empty:
                return {'error': 'Nenhum dado de aluno encontrado'}
            
            stats = {
                'total_alunos': len(df),
                'estados_representados': df['Estado'].nunique(),
                'cursos_ativos': df['Curso'].nunique(),
                'ticket_medio': df['Valor_Pago'].mean(),
                'receita_total_alunos': df['Valor_Pago'].sum(),
                'distribuicao_estados': df['Estado'].value_counts().to_dict(),
                'distribuicao_profissoes': df['Profissao'].value_counts().to_dict()
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar estatísticas de alunos: {str(e)}")
            return {'error': str(e)}
    
    def get_course_performance(self) -> Dict:
        """
        Retorna performance dos cursos.
        
        Returns:
            Dicionário com performance dos cursos
        """
        try:
            # Combinar dados financeiros e de cursos
            financial_df = self.financial_data[self.financial_data['Tipo'] == 'Realizado'].copy()
            courses_df = self.courses_data.copy()
            
            performance = []
            
            for _, course in courses_df.iterrows():
                codigo = course['Codigo']
                financial_data = financial_df[financial_df['Periodo'] == codigo]
                
                if not financial_data.empty:
                    perf = {
                        'codigo': codigo,
                        'nome': course['Nome'],
                        'total_alunos': course['Total_Alunos'],
                        'receita_realizada': financial_data['Receita_Bruta'].iloc[0],
                        'resultado_liquido': financial_data['Resultado_Liquido'].iloc[0],
                        'inadimplencia': financial_data['Inadimplencia'].iloc[0],
                        'ticket_medio': financial_data['Receita_Bruta'].iloc[0] / course['Total_Alunos'] if course['Total_Alunos'] > 0 else 0,
                        'status': course['Status']
                    }
                    performance.append(perf)
            
            return {'courses': performance}
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar performance dos cursos: {str(e)}")
            return {'error': str(e)}
    
    def add_student(self, student_data: Dict) -> Dict:
        """
        Adiciona um novo aluno ao sistema.
        
        Args:
            student_data: Dicionário com dados do aluno
            
        Returns:
            Dicionário com resultado da operação
        """
        try:
            # Validar dados obrigatórios
            required_fields = ['Nome', 'Email', 'CPF', 'Telefone', 'Cidade', 'Estado', 'Curso']
            
            for field in required_fields:
                if field not in student_data or not student_data[field]:
                    return {'error': f'Campo obrigatório ausente: {field}'}
            
            # Verificar se CPF já existe
            if not self.student_data.empty and student_data['CPF'] in self.student_data['CPF'].values:
                return {'error': 'CPF já cadastrado no sistema'}
            
            # Verificar se email já existe
            if not self.student_data.empty and student_data['Email'] in self.student_data['Email'].values:
                return {'error': 'E-mail já cadastrado no sistema'}
            
            # Adicionar ID único
            new_id = self.student_data['ID'].max() + 1 if not self.student_data.empty else 1
            student_data['ID'] = new_id
            student_data['Status'] = 'Ativo'
            student_data['Data_Inscricao'] = pd.Timestamp.now().strftime('%d/%m/%Y')
            
            # Adicionar valor padrão se não fornecido
            if 'Valor_Pago' not in student_data:
                student_data['Valor_Pago'] = 300.0
            
            # Criar novo DataFrame com o aluno
            new_student_df = pd.DataFrame([student_data])
            
            # Adicionar ao DataFrame existente
            self.student_data = pd.concat([self.student_data, new_student_df], ignore_index=True)
            
            self.logger.info(f"Aluno {student_data['Nome']} adicionado com sucesso")
            
            return {'success': True, 'message': f'Aluno {student_data["Nome"]} cadastrado com sucesso', 'id': new_id}
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar aluno: {str(e)}")
            return {'error': str(e)}
    
    def export_data(self, data_type: str, format_type: str = 'csv') -> Tuple[bool, str]:
        """
        Exporta dados do sistema.
        
        Args:
            data_type: Tipo de dados ('financial', 'students', 'courses')
            format_type: Formato de exportação ('csv', 'excel', 'json')
            
        Returns:
            Tupla (sucesso, mensagem/caminho_arquivo)
        """
        try:
            # Selecionar dados para exportar
            if data_type == 'financial':
                df = self.financial_data
                filename_prefix = 'dados_financeiros'
            elif data_type == 'students':
                df = self.student_data
                filename_prefix = 'dados_alunos'
            elif data_type == 'courses':
                df = self.courses_data
                filename_prefix = 'dados_cursos'
            else:
                return False, f'Tipo de dados inválido: {data_type}'
            
            if df.empty:
                return False, f'Nenhum dado encontrado para {data_type}'
            
            # Gerar nome do arquivo
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{filename_prefix}_{timestamp}.{format_type}'
            
            # Exportar conforme o formato
            if format_type == 'csv':
                csv_data = df.to_csv(index=False)
                return True, csv_data
            elif format_type == 'excel':
                # Em um sistema real, salvaria o arquivo
                return True, f'Arquivo Excel {filename} gerado com sucesso'
            elif format_type == 'json':
                json_data = df.to_json(orient='records', indent=2)
                return True, json_data
            else:
                return False, f'Formato inválido: {format_type}'
                
        except Exception as e:
            self.logger.error(f"Erro ao exportar dados: {str(e)}")
            return False, str(e)
    
    def validate_financial_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valida dados financeiros importados.
        
        Args:
            df: DataFrame com dados financeiros
            
        Returns:
            Tupla (é_válido, lista_de_erros)
        """
        errors = []
        
        # Verificar colunas obrigatórias
        required_columns = ['Periodo', 'Receita_Bruta', 'Resultado_Liquido']
        for col in required_columns:
            if col not in df.columns:
                errors.append(f'Coluna obrigatória ausente: {col}')
        
        # Verificar valores numéricos
        numeric_columns = ['Receita_Bruta', 'Resultado_Liquido', 'Total_Despesas']
        for col in numeric_columns:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    errors.append(f'Coluna {col} deve conter apenas valores numéricos')
        
        # Verificar valores negativos em receita
        if 'Receita_Bruta' in df.columns:
            if (df['Receita_Bruta'] < 0).any():
                errors.append('Receita Bruta não pode ter valores negativos')
        
        return len(errors) == 0, errors
