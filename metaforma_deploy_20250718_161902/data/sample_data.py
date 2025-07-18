import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class SampleDataGenerator:
    """
    Classe para gerar dados de exemplo para testes e demonstrações.
    Baseada nos dados reais do Instituto Metaforma.
    """
    
    def __init__(self):
        """Inicializa o gerador de dados de exemplo."""
        self.courses_mapping = {
            'FAC_17': 'Formação Analista Comportamental - Turma 17',
            'FAC_16': 'Formação Analista Comportamental - Turma 16',
            'FAC_15': 'Formação Analista Comportamental - Turma 15',
            'FAC_14': 'Formação Analista Comportamental - Turma 14'
        }
        
        self.brazilian_states = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        
        self.professions = [
            'Analista de RH',
            'Coordenador de Recursos Humanos',
            'Gestor de RH',
            'Professor',
            'Terapeuta',
            'Psicólogo',
            'Gerente',
            'Assistente de RH',
            'Consultor',
            'Coach'
        ]
    
    def generate_financial_data(self, include_budget: bool = True) -> pd.DataFrame:
        """
        Gera dados financeiros baseados nos dados reais do Instituto Metaforma.
        
        Args:
            include_budget: Se deve incluir dados de orçamento
            
        Returns:
            DataFrame com dados financeiros
        """
        # Dados realizados baseados no PDF
        realized_data = {
            'Periodo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Tipo': ['Realizado'] * 4,
            'Receita_Bruta': [3589.0, 3760.0, 7105.0, 9894.0],
            'Inadimplencia': [2910.0, 0.0, 291.0, 2328.0],
            'Receita_Liquida': [679.0, 3760.0, 6814.0, 7566.0],
            'Facebook_Anuncios': [3000.0, 2100.0, 2100.0, 3000.0],
            'Creditos_Plataforma': [1305.2, 803.2, 903.6, 1104.4],
            'Boletos': [1167.7, 159.7, 449.1, 659.9],
            'Cartao_Credito': [0.0, 0.0, 0.0, 0.0],
            'Gestor_Trafego': [600.0, 600.0, 600.0, 600.0],
            'Outras_Despesas': [0.0, 0.0, 0.0, 0.0],
            'Total_Despesas': [6072.9, 3662.9, 4052.7, 5364.3],
            'Resultado_Bruto': [-5393.9, 97.1, 2761.3, 2201.7],
            'Comissao': [-2696.9, 48.6, 1380.7, 1100.9],
            'Repasse': [0.0, 0.0, 0.0, 0.0],
            'Resultado_Liquido': [-2696.9, 48.6, 1380.7, 1100.9],
            'Data_Criacao': [datetime.now() - timedelta(days=30),
                            datetime.now() - timedelta(days=60),
                            datetime.now() - timedelta(days=90),
                            datetime.now() - timedelta(days=120)]
        }
        
        df_realized = pd.DataFrame(realized_data)
        
        if not include_budget:
            return df_realized
        
        # Dados de orçamento baseados no PDF
        budget_data = {
            'Periodo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Tipo': ['Orcamento'] * 4,
            'Receita_Bruta': [25220.0, 15400.0, 17290.0, 20370.0],
            'Inadimplencia': [0.0, 0.0, 0.0, 0.0],
            'Receita_Liquida': [25220.0, 15400.0, 17290.0, 20370.0],
            'Facebook_Anuncios': [0.0, 2100.0, 2100.0, 3000.0],
            'Creditos_Plataforma': [0.0, 803.2, 903.6, 1104.4],
            'Boletos': [0.0, 798.4, 988.0, 1099.8],
            'Cartao_Credito': [0.0, 0.0, 0.0, 0.0],
            'Gestor_Trafego': [0.0, 600.0, 600.0, 600.0],
            'Outras_Despesas': [0.0, 0.0, 0.0, 0.0],
            'Total_Despesas': [0.0, 4301.6, 4591.6, 5804.2],
            'Resultado_Bruto': [25220.0, 11098.4, 12698.4, 14565.8],
            'Comissao': [2522.0, 5549.2, 6349.2, 7282.9],
            'Repasse': [2522.0, 5549.2, 6349.2, 7282.9],
            'Resultado_Liquido': [22698.0, 5549.2, 6349.2, 7282.9],
            'Data_Criacao': [datetime.now() - timedelta(days=35),
                            datetime.now() - timedelta(days=65),
                            datetime.now() - timedelta(days=95),
                            datetime.now() - timedelta(days=125)]
        }
        
        df_budget = pd.DataFrame(budget_data)
        
        # Combinar dados realizados e orçamento
        return pd.concat([df_realized, df_budget], ignore_index=True)
    
    def generate_student_data(self, num_students: Optional[int] = None) -> pd.DataFrame:
        """
        Gera dados de alunos baseados nos dados reais do Instituto Metaforma.
        
        Args:
            num_students: Número de alunos a gerar (None para usar dados reais)
            
        Returns:
            DataFrame com dados dos alunos
        """
        # Dados reais dos alunos baseados no PDF
        real_students = {
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
            'Nome_Certificado': [
                'Fernanda Passos Silva dos Santos',
                'Nathalia da Silva Bezerra',
                'Áurea Cristina de Oliveira Aguiar',
                'Diane Machado',
                'Kathleen Sampaio Interaminsense',
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
                '719992509996',
                '11989359930',
                '91981129597',
                '55981524180',
                '81996793483',
                '61993279632',
                '38999447822',
                '73988443997'
            ],
            'CEP': [
                '42805854',
                '06045-420',
                '67130580',
                '98860000',
                '50.740-040',
                '76380-745',
                '38.602-024',
                '88220000'
            ],
            'Logradouro': [
                'rua edvard dutra, 101',
                'Via transversal sul, 200, T. 2 apto 113',
                'Avenida Vila Nova, 250, Residencial Atlanta Bloco 6 ap 104',
                'Santo Ângelo, 1953, Casa',
                'Rua Emiliano Braga, 868, Edf Portinari',
                'Avenida Goias, 250',
                'RUA JUSCELINO KUBITSCHEK, 173, CASA',
                'Rua primor, 430, Casa'
            ],
            'Bairro': [
                'Santo Antonio',
                'Novo osasco',
                'Coqueiro',
                'Centro',
                'Várzea',
                'Carrilho',
                'PRADO',
                'Santa Luzia'
            ],
            'Cidade': [
                'Camacari',
                'Osasco',
                'Ananindeua',
                'Eugênio De Castro',
                'Recife',
                'Goianésia',
                'Paracatu',
                'Tijucas'
            ],
            'Estado': ['BA', 'SP', 'PA', 'RS', 'PE', 'GO', 'MG', 'SC'],
            'Celular': [
                '71992509996',
                '11989359930',
                '91981129597',
                '55981524180',
                '81996793483',
                '61993279632',
                '38999447822',
                '73988443997'
            ],
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
                'Analista de rh',
                'Coordenadora de Recursos Humanos',
                'Professora de Gestao',
                'Terapeuta',
                'Gestora de RH',
                'Gerente',
                'ASSISTENTE DE RECURSOS HUMANOS I',
                'Analista de RH'
            ],
            'Status': ['Ativo'] * 8,
            'Valor_Pago': [350.0, 400.0, 300.0, 250.0, 450.0, 300.0, 200.0, 350.0],
            'Periodo_Curso': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14', 'FAC_15', 'FAC_16', 'FAC_17', 'FAC_14']
        }
        
        df = pd.DataFrame(real_students)
        
        # Se solicitado mais alunos, gerar dados sintéticos adicionais
        if num_students and num_students > len(df):
            additional_students = num_students - len(df)
            synthetic_data = self._generate_synthetic_students(additional_students, len(df) + 1)
            df = pd.concat([df, synthetic_data], ignore_index=True)
        
        return df
    
    def _generate_synthetic_students(self, count: int, start_id: int) -> pd.DataFrame:
        """
        Gera dados sintéticos de alunos para complementar os dados reais.
        
        Args:
            count: Número de alunos sintéticos a gerar
            start_id: ID inicial para os novos registros
            
        Returns:
            DataFrame com alunos sintéticos
        """
        synthetic_students = []
        
        first_names = ['João', 'Maria', 'José', 'Ana', 'Carlos', 'Francisca', 'Antonio', 'Antonia', 
                      'Manoel', 'Rita', 'Pedro', 'Rosa', 'Francisco', 'Raimundo', 'Daniel']
        
        last_names = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves',
                     'Pereira', 'Lima', 'Gomes', 'Costa', 'Ribeiro', 'Martins', 'Carvalho']
        
        for i in range(count):
            student_id = start_id + i
            first_name = random.choice(first_names)
            last_name = f"{random.choice(last_names)} {random.choice(last_names)}"
            full_name = f"{first_name} {last_name}"
            
            # Gerar CPF sintético (formato válido mas não real)
            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            
            # Gerar telefone sintético
            ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '27'])
            phone = f"{ddd}9{random.randint(10000000, 99999999)}"
            
            # Estado aleatório
            state = random.choice(self.brazilian_states)
            
            # Curso aleatório
            course_period = random.choice(list(self.courses_mapping.keys()))
            
            # Profissão aleatória
            profession = random.choice(self.professions)
            
            # Valor pago (baseado na distribuição real)
            value_paid = random.choice([200.0, 250.0, 300.0, 350.0, 400.0, 450.0])
            
            # Data de inscrição aleatória nos últimos 6 meses
            days_ago = random.randint(1, 180)
            inscription_date = (datetime.now() - timedelta(days=days_ago)).strftime('%d/%m/%Y')
            
            student = {
                'ID': student_id,
                'Nome': full_name,
                'Nome_Certificado': full_name,
                'Email': f"{first_name.lower()}.{last_name.split()[0].lower()}@email.com",
                'CPF': cpf,
                'Telefone': phone,
                'CEP': f"{random.randint(10000, 99999)}-{random.randint(100, 999)}",
                'Logradouro': f"Rua {random.choice(['das Flores', 'Principal', 'Central'])}, {random.randint(1, 999)}",
                'Bairro': random.choice(['Centro', 'Vila Nova', 'Jardim', 'Santa Maria']),
                'Cidade': f"Cidade {random.randint(1, 100)}",
                'Estado': state,
                'Celular': phone,
                'Curso': 'Formação Analista Comportamental',
                'Data_Inscricao': inscription_date,
                'Profissao': profession,
                'Status': random.choice(['Ativo', 'Ativo', 'Ativo', 'Concluído']),
                'Valor_Pago': value_paid,
                'Periodo_Curso': course_period
            }
            
            synthetic_students.append(student)
        
        return pd.DataFrame(synthetic_students)
    
    def generate_course_data(self) -> pd.DataFrame:
        """
        Gera dados dos cursos baseados nas informações do Instituto Metaforma.
        
        Returns:
            DataFrame com dados dos cursos
        """
        course_data = {
            'Codigo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Nome': ['Formação Analista Comportamental'] * 4,
            'Turma': [17, 16, 15, 14],
            'Data_Inicio': ['01/04/2024', '01/03/2024', '01/02/2024', '01/01/2024'],
            'Data_Fim': ['30/06/2024', '31/05/2024', '30/04/2024', '31/03/2024'],
            'Duracao_Semanas': [12, 12, 12, 12],
            'Carga_Horaria': [120, 120, 120, 120],
            'Valor_Curso': [400.0, 350.0, 400.0, 450.0],
            'Total_Alunos_Orcado': [63, 44, 43, 45],  # Baseado no orçamento
            'Total_Alunos_Realizado': [26, 16, 18, 21],  # Baseado nos dados reais
            'Status': ['Em Andamento', 'Concluído', 'Concluído', 'Concluído'],
            'Modalidade': ['Online'] * 4,
            'Instrutor': ['Instituto Metaforma'] * 4,
            'Categoria': ['Desenvolvimento Profissional'] * 4,
            'Certificacao': ['Sim'] * 4,
            'Plataforma': ['Própria'] * 4
        }
        
        return pd.DataFrame(course_data)
    
    def generate_marketing_data(self) -> pd.DataFrame:
        """
        Gera dados de marketing baseados nas despesas com Facebook Ads.
        
        Returns:
            DataFrame com dados de marketing
        """
        marketing_data = {
            'Periodo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Canal': ['Facebook'] * 4,
            'Investimento': [3000.0, 2100.0, 2100.0, 3000.0],  # Facebook Ads realizados
            'Impressoes': [150000, 120000, 110000, 140000],  # Estimativas
            'Cliques': [3000, 2400, 2200, 2800],
            'CTR': [2.0, 2.0, 2.0, 2.0],  # Taxa de clique
            'CPM': [20.0, 17.5, 19.1, 21.4],  # Custo por mil impressões
            'CPC': [1.0, 0.88, 0.95, 1.07],  # Custo por clique
            'Conversoes': [26, 16, 18, 21],  # Alunos captados
            'Taxa_Conversao': [0.87, 0.67, 0.82, 0.75],  # %
            'CAC': [115.38, 131.25, 116.67, 142.86],  # Custo de aquisição por cliente
            'ROAS': [1.20, 1.79, 3.38, 3.30]  # Return on Ad Spend
        }
        
        return pd.DataFrame(marketing_data)
    
    def generate_payment_data(self) -> pd.DataFrame:
        """
        Gera dados de pagamentos e inadimplência.
        
        Returns:
            DataFrame com dados de pagamentos
        """
        payment_data = []
        
        # Baseado nos dados reais de inadimplência
        periods_default = {
            'FAC_17': {'total': 3589.0, 'default': 2910.0},
            'FAC_16': {'total': 3760.0, 'default': 0.0},
            'FAC_15': {'total': 7105.0, 'default': 291.0},
            'FAC_14': {'total': 9894.0, 'default': 2328.0}
        }
        
        for period, data in periods_default.items():
            total_revenue = data['total']
            default_amount = data['default']
            paid_amount = total_revenue - default_amount
            
            payment_record = {
                'Periodo': period,
                'Receita_Total': total_revenue,
                'Valor_Pago': paid_amount,
                'Valor_Inadimplente': default_amount,
                'Taxa_Pagamento': (paid_amount / total_revenue * 100) if total_revenue > 0 else 0,
                'Taxa_Inadimplencia': (default_amount / total_revenue * 100) if total_revenue > 0 else 0,
                'Metodo_Pagamento_Principal': 'Boleto/PIX',
                'Prazo_Medio_Pagamento': random.randint(5, 30),
                'Status_Cobranca': 'Ativo' if default_amount > 0 else 'Não Aplicável'
            }
            
            payment_data.append(payment_record)
        
        return pd.DataFrame(payment_data)
    
    def get_complete_dataset(self) -> Dict[str, pd.DataFrame]:
        """
        Retorna um conjunto completo de dados para o sistema.
        
        Returns:
            Dicionário com todos os DataFrames
        """
        return {
            'financial': self.generate_financial_data(),
            'students': self.generate_student_data(),
            'courses': self.generate_course_data(),
            'marketing': self.generate_marketing_data(),
            'payments': self.generate_payment_data()
        }
    
    def export_sample_data(self, output_dir: str = 'data/exports/') -> Dict[str, str]:
        """
        Exporta os dados de exemplo para arquivos CSV.
        
        Args:
            output_dir: Diretório de saída
            
        Returns:
            Dicionário com caminhos dos arquivos gerados
        """
        import os
        
        # Criar diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        datasets = self.get_complete_dataset()
        file_paths = {}
        
        for name, df in datasets.items():
            file_path = os.path.join(output_dir, f'{name}_sample.csv')
            df.to_csv(file_path, index=False, encoding='utf-8')
            file_paths[name] = file_path
        
        return file_paths
