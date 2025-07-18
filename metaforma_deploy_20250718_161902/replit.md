# Instituto Metaforma - Sistema de Gestão Financeira

## Overview

This repository contains a financial management system for Instituto Metaforma, built as a Streamlit web application. The system manages student data, financial records, and generates comprehensive reports for educational course management. The application appears to be transitioning from a previous React-based implementation to a Python/Streamlit architecture.

## User Preferences

Preferred communication style: Simple, everyday language (Portuguese Brazilian).
Technical background: User had advanced React/TypeScript system with SQLite database.
Project goal: Migrate from React system to Streamlit while preserving advanced functionalities.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit (Python-based web framework)
- **Layout**: Multi-page application with sidebar navigation
- **Visualization**: Plotly for interactive charts and graphs
- **UI Components**: Native Streamlit components with custom styling
- **Pages**: Modular page structure with separate files for each major feature

### Backend Architecture
- **Language**: Python 3.x
- **Framework**: Streamlit for both frontend and backend logic
- **Data Processing**: Pandas for data manipulation and analysis
- **File Structure**: Utilities separated into dedicated modules

### Previous Architecture (Legacy)
- **Frontend**: React 18 with TypeScript
- **Build Tool**: ESBuild for bundling and compilation
- **Styling**: Tailwind CSS with PostCSS
- **Routing**: React Router DOM
- **Charts**: Chart.js and Recharts for data visualization

## Key Components

### 1. Application Core (`app.py`)
- Main application entry point
- System status monitoring
- Data handler initialization with caching
- Sidebar navigation and system information display

### 2. Page Modules
- **Dashboard Financeiro** (`pages/1_Dashboard_Financeiro.py`): Financial overview and metrics
- **Gestão de Alunos** (`pages/2_Gestao_Alunos.py`): Student management interface
- **Importar Dados** (`pages/3_Importar_Dados.py`): Data import functionality
- **Relatórios** (`pages/4_Relatorios.py`): Report generation and analysis
- **Migração de Dados** (`pages/5_Migração_Dados.py`): SQLite database migration from previous React system
- **Melhorias do Sistema** (`pages/6_Melhorias_Sistema.py`): Advanced features and AI-powered analytics
- **Gestão Avançada de Alunos** (`pages/7_Gestao_Alunos_Avancada.py`): React-style student management with complete forms, validation, and payment tracking
- **Conciliação Bancária** (`pages/8_Conciliacao_Bancaria.py`): Bank reconciliation system for tracking payment compliance and default rates

### 3. Utility Classes
- **DataHandler** (`utils/data_handler.py`): Data management and persistence
- **FinancialCalculator** (`utils/financial_calculator.py`): Financial calculations and metrics
- **SQLiteReader** (`utils/sqlite_reader.py`): Migration tool for reading data from previous React system's SQLite database
- **AdvancedDataHandler** (`utils/advanced_data_handler.py`): Complete student management system with payment tracking, based on React components
- **BackendMigrator** (`utils/backend_migrator.py`): Complete migration tool for Node.js/Express backend data
- **BankReconciliation** (`utils/bank_reconciliation.py`): Automated bank reconciliation system for payment validation

### 4. Data Layer
- **Sample Data Generator** (`data/sample_data.py`): Test data generation for development
- File-based data storage with support for Excel, CSV, and PDF imports

## Data Flow

### 1. Data Input
- Manual data entry through Streamlit forms
- File uploads (Excel, CSV, PDF) via Streamlit file uploader
- Sample data generation for testing and demonstrations

### 2. Data Processing
- Pandas DataFrames for in-memory data manipulation
- Financial calculations performed by FinancialCalculator class
- Data validation and cleaning in DataHandler

### 3. Data Output
- Interactive Plotly charts and visualizations
- Streamlit native components for data display
- Export functionality for reports and student lists

### 4. Session Management
- Streamlit session state for data persistence
- Cached data handlers to improve performance
- Real-time data updates across page navigation

## External Dependencies

### Core Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive data visualization
- **numpy**: Numerical computations

### File Processing
- **openpyxl**: Excel file handling
- **csv**: CSV file processing
- Support for PDF file uploads (visualization only)

### Development Tools
- **logging**: Application logging and debugging
- **datetime**: Date and time handling
- **typing**: Type hints for better code quality

### Legacy Dependencies (React)
- **react**: Frontend framework
- **react-dom**: DOM manipulation
- **react-router-dom**: Client-side routing
- **chart.js**: Data visualization
- **tailwindcss**: CSS framework
- **esbuild**: Build tooling

## Deployment Strategy

### Current Approach
- Streamlit native deployment capability
- Single-command deployment with `streamlit run app.py`
- Environment-agnostic configuration
- File-based data storage for simplicity

### Development Workflow
- Local development with Streamlit dev server
- Hot reloading for rapid development
- Modular page structure for team collaboration

### Legacy Build Process (React)
- ESBuild for production bundling
- PostCSS pipeline for CSS processing
- Static file generation for deployment
- Development server with watch mode

### Recommended Production Setup
- Container-based deployment (Docker)
- Environment variable configuration
- Database integration (PostgreSQL recommended)
- Load balancing for multiple instances
- SSL/TLS termination
- Monitoring and logging infrastructure

### Data Persistence Strategy
- Current: File-based storage with Pandas
- Recommended: Database integration with proper ORM
- Backup and recovery procedures needed
- Data migration tools for scaling

The system is designed to handle educational institution management with a focus on financial tracking, student administration, and comprehensive reporting capabilities.

## Recent Changes

### 2025-07-18 - Integração Completa Backend Node.js
- **Analisados arquivos originais** do projeto React/TypeScript completo
- **Implementado BackendMigrator** para migração completa do SQLite backend
- **Identificadas estruturas avançadas**: StudentFormModal, StudentTable, PaymentInstallments
- **Sistema original** possui formulários com validação completa (CPF, email, telefone)
- **Backend com API REST** completa (Express + SQLite + CORS)
- **Configuração TypeScript** + Tailwind CSS + ESBuild para build
- **Dados reais disponíveis**: usuário admin cadastrado, estrutura de alunos vazia
- **Implementado BackendMigrator** completo para dados reais do usuário
- **Criado sistema de conciliação bancária** com validação de adimplência/inadimplência
- **Sistema pronto** para produção com todas as funcionalidades do projeto original

### 2025-07-18 - Sistema de Cadastro Online e Deploy
- **Criado sistema completo** de cadastro online para substituir Google Forms
- **Implementada validação** de CPF, email e telefone brasileiros
- **Sistema administrativo** integrado com exportação de dados
- **Preparado deploy completo** para hospedagem tradicional
- **Criados scripts** automatizados para instalação (Docker e manual)
- **Documentação detalhada** para usuários leigos em programação
- **Sistema pronto** para ser hospedado na infraestrutura do cliente