import React, { useState, useMemo, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import { FAC, Expense, FacFinancialSummary, PaymentStatus } from '../types';
import { PlusCircle, Edit2, Trash2, DollarSign, Users, TrendingUp, TrendingDown, Eye } from 'lucide-react';

// Simplified FAC Form Modal
const FacFormModal: React.FC<{ isOpen: boolean; onClose: () => void; facCode?: string | null; }> = ({ isOpen, onClose, facCode }) => {
  const { addFac, updateFac, getFacByCode, courses, facs } = useAppContext(); // Destructure facs here
  
  const [courseId, setCourseId] = useState('');
  const [name, setName] = useState('');
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [status, setStatus] = useState<'Planejada' | 'Em andamento' | 'Finalizada' | 'Cancelada'>('Planejada');
  const [description, setDescription] = useState('');
  
  // Initialize customCodeSuffix using 'facs' from context
  const [customCodeSuffix, setCustomCodeSuffix] = useState<string>(() => (facs.length + 18).toString());

  useEffect(() => {
    if (facCode) {
      const facItem = getFacByCode(facCode); 
      if (facItem) {
        setCourseId(facItem.courseId);
        setName(facItem.name);
        setStartDate(facItem.startDate);
        setStatus(facItem.status);
        setDescription(facItem.description || '');
        // When editing, the code/suffix is fixed, so no need to setCustomCodeSuffix.
      }
    } else {
        // Reset form for new FAC
        setCourseId(courses.length > 0 ? courses[0].id : '');
        setName('');
        setStartDate(new Date().toISOString().split('T')[0]);
        setStatus('Planejada');
        setDescription('');
        // Update suffix based on current number of facs
        setCustomCodeSuffix((facs.length + 18).toString());
    }
  }, [facCode, getFacByCode, courses, isOpen, facs]); // Added facs to dependency array

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedSuffix = customCodeSuffix.trim();
    if (!courseId || !name || !startDate || !status || (!facCode && !trimmedSuffix) ) {
        alert("Por favor, preencha todos os campos obrigatórios da turma, incluindo o sufixo do código para novas turmas.");
        return;
    }
    const facData = { courseId, name, startDate, status, description };
    if (facCode) {
      updateFac(facCode, facData);
    } else {
      addFac(facData, trimmedSuffix); 
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg">
        <h2 className="text-xl font-semibold mb-4">{facCode ? 'Editar Turma (FAC)' : 'Adicionar Nova Turma (FAC)'}</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="courseId" className="block text-sm font-medium text-gray-700">Curso Base*</label>
            <select id="courseId" value={courseId} onChange={(e) => setCourseId(e.target.value)} required className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-sky-500 focus:border-sky-500 sm:text-sm">
              <option value="">Selecione um Curso</option>
              {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>
          {!facCode && (
            <div>
                <label htmlFor="customCodeSuffix" className="block text-sm font-medium text-gray-700">Sufixo do Código da Turma (Ex: 18 para FAC_C1_T18)*</label>
                <input type="text" id="customCodeSuffix" value={customCodeSuffix} onChange={(e) => setCustomCodeSuffix(e.target.value)} required className="mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm"/>
            </div>
          )}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">Nome da Turma*</label>
            <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required className="mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm"/>
          </div>
          <div>
            <label htmlFor="startDate" className="block text-sm font-medium text-gray-700">Data de Início*</label>
            <input type="date" id="startDate" value={startDate} onChange={(e) => setStartDate(e.target.value)} required className="mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm"/>
          </div>
          <div>
            <label htmlFor="status" className="block text-sm font-medium text-gray-700">Status*</label>
            <select id="status" value={status} onChange={(e) => setStatus(e.target.value as FAC['status'])} required className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm">
              <option value="Planejada">Planejada</option>
              <option value="Em andamento">Em andamento</option>
              <option value="Finalizada">Finalizada</option>
              <option value="Cancelada">Cancelada</option>
            </select>
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">Descrição</label>
            <textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} rows={3} className="mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm"></textarea>
          </div>
          <div className="flex justify-end space-x-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300">Cancelar</button>
            <button type="submit" className="px-4 py-2 text-white bg-sky-600 rounded-md hover:bg-sky-700">Salvar</button>
          </div>
        </form>
      </div>
    </div>
  );
};

const FacCard: React.FC<{ summary: FacFinancialSummary, onManageExpenses: (facCode: string) => void, fac: FAC }> = ({ summary, onManageExpenses, fac }) => {
  const { getCourseById } = useAppContext();
  const course = getCourseById(fac.courseId);
  
  return (
    <div className="bg-white shadow-xl rounded-lg p-6 space-y-4 transform hover:scale-105 transition-transform duration-300">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-xl font-bold text-sky-700">{summary.facCode} - {fac.name}</h2>
          <p className="text-sm text-gray-500">{course?.name} | Início: {new Date(fac.startDate).toLocaleDateString()}</p>
          <span className={`px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full ${
              fac.status === 'Em andamento' ? 'bg-blue-100 text-blue-800' :
              fac.status === 'Finalizada' ? 'bg-green-100 text-green-800' :
              fac.status === 'Planejada' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800' // Cancelada
            }`}>{fac.status}</span>
        </div>
        {/* Actions like Edit FAC could go here */}
      </div>
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="flex items-center space-x-2 text-gray-700">
          <Users size={18} className="text-sky-500" /> 
          <span>Alunos: <span className="font-semibold">{summary.totalStudents}</span></span>
        </div>
        <div className="flex items-center space-x-2 text-gray-700">
          <DollarSign size={18} className="text-green-500" />
          <span>Receita Realizada: <span className="font-semibold">R$ {summary.grossRevenueRealized.toFixed(2)}</span></span>
        </div>
        <div className="flex items-center space-x-2 text-gray-700">
          <TrendingUp size={18} className="text-blue-500" />
          <span>Receita Orçada: <span className="font-semibold">R$ {summary.grossRevenueBudgeted.toFixed(2)}</span></span>
        </div>
        <div className="flex items-center space-x-2 text-gray-700">
          <TrendingDown size={18} className="text-red-500" />
          <span>Inadimplência: <span className="font-semibold">R$ {summary.delinquency.toFixed(2)}</span></span>
        </div>
         <div className="flex items-center space-x-2 text-gray-700">
          <DollarSign size={18} className="text-orange-500" />
          <span>Despesas: <span className="font-semibold">R$ {summary.totalExpenses.toFixed(2)}</span></span>
        </div>
        <div className="flex items-center space-x-2 text-gray-700">
          <Eye size={18} className="text-purple-500" />
          <span>Resultado Líquido: <span className="font-semibold">R$ {summary.netResultRealized.toFixed(2)}</span></span>
        </div>
      </div>
       <button 
        onClick={() => onManageExpenses(summary.facCode)}
        className="mt-2 w-full text-sm text-sky-600 hover:text-sky-800 font-medium py-2 px-3 rounded-md border border-sky-600 hover:bg-sky-50 transition-colors"
      >
        Gerenciar Despesas
      </button>
    </div>
  );
};


const ExpenseModal: React.FC<{ isOpen: boolean; onClose: () => void; facCode: string; }> = ({ isOpen, onClose, facCode }) => {
    const { expenses, addExpense } = useAppContext();
    const facExpenses = expenses.filter(e => e.facCode === facCode);
    
    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState<number>(0);
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [category, setCategory] = useState<Expense['category']>('Other');

    const handleAddExpense = () => {
        if (!description || amount <= 0) {
            alert("Preencha descrição e valor da despesa.");
            return;
        }
        addExpense({ facCode, description, amount, date, category });
        setDescription('');
        setAmount(0);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <h2 className="text-xl font-semibold mb-4">Despesas da Turma: {facCode}</h2>
                <div className="space-y-3 mb-4">
                    {renderExpenseField('Descrição', <input type="text" value={description} onChange={e => setDescription(e.target.value)} />)}
                    {renderExpenseField('Valor (R$)', <input type="number" value={amount} onChange={e => setAmount(parseFloat(e.target.value))} />)}
                    {renderExpenseField('Data', <input type="date" value={date} onChange={e => setDate(e.target.value)} />)}
                    {renderExpenseField('Categoria', 
                        <select value={category} onChange={e => setCategory(e.target.value as Expense['category'])}>
                            {(['Facebook Ads', 'Platform Credits', 'Boletos Fees', 'Credit Card Fees', 'Traffic Manager', 'Other'] as Expense['category'][]).map(cat => <option key={cat} value={cat}>{cat}</option>)}
                        </select>
                    )}
                    <button onClick={handleAddExpense} className="w-full bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-md">Adicionar Despesa</button>
                </div>
                <h3 className="text-lg font-medium mt-6 mb-2">Despesas Lançadas</h3>
                {facExpenses.length > 0 ? (
                    <ul className="divide-y divide-gray-200">
                        {facExpenses.map(exp => (
                            <li key={exp.id} className="py-3">
                                <div className="flex justify-between items-center">
                                    <span>{exp.description} ({exp.category})</span>
                                    <span className="font-semibold">R$ {exp.amount.toFixed(2)}</span>
                                </div>
                                <p className="text-xs text-gray-500">{new Date(exp.date).toLocaleDateString()}</p>
                            </li>
                        ))}
                    </ul>
                ) : <p className="text-gray-500">Nenhuma despesa lançada para esta turma.</p>}
                <button onClick={onClose} className="mt-6 w-full bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 px-4 rounded-md">Fechar</button>
            </div>
        </div>
    );
};
const renderExpenseField = (label: string, field: React.ReactElement<React.HTMLAttributes<HTMLElement>>) => (
    <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
        {React.cloneElement(field, { className: "mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-sky-500 focus:border-sky-500 sm:text-sm" })}
    </div>
);


const FacManagementPage: React.FC = () => {
  const { facs, students, expenses } = useAppContext();
  const [isFacModalOpen, setIsFacModalOpen] = useState(false);
  const [editingFacCode, setEditingFacCode] = useState<string | null>(null);

  const [isExpenseModalOpen, setIsExpenseModalOpen] = useState(false);
  const [managingExpensesForFac, setManagingExpensesForFac] = useState<string | null>(null);


  const financialSummaries = useMemo<FacFinancialSummary[]>(() => {
    return facs.map(fac => {
      const facStudents = students.filter(s => s.facCode === fac.code);
      const grossRevenueRealized = facStudents.reduce((sum, student) => 
          sum + student.paymentInstallments.filter(p => p.status === PaymentStatus.PAID).reduce((s, p) => s + p.amount, 0), 0);
      const grossRevenueBudgeted = facStudents.reduce((sum, student) => sum + student.courseFee, 0);
      const now = new Date();
      const delinquency = facStudents.reduce((sum, student) =>
        sum + student.paymentInstallments.filter(p => p.status === PaymentStatus.PENDING && new Date(p.dueDate) < now).reduce((s, p) => s + p.amount, 0), 0);
      const totalExpenses = expenses.filter(e => e.facCode === fac.code).reduce((sum, e) => sum + e.amount, 0);
      
      return {
        facCode: fac.code,
        totalStudents: facStudents.length,
        grossRevenueBudgeted,
        grossRevenueRealized,
        delinquency,
        totalExpenses,
        netResultRealized: grossRevenueRealized - totalExpenses - delinquency, // Simplified
      };
    });
  }, [students, facs, expenses]);

  const openAddFacModal = () => {
    setEditingFacCode(null);
    setIsFacModalOpen(true);
  };

  const openEditFacModal = (facCode: string) => {
    setEditingFacCode(facCode);
    setIsFacModalOpen(true);
  };
  
  const handleManageExpenses = (facCode: string) => {
    setManagingExpensesForFac(facCode);
    setIsExpenseModalOpen(true);
  };


  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-semibold text-gray-800">Gerenciamento de Turmas (FACs)</h1>
        <button
          onClick={openAddFacModal}
          className="bg-sky-600 hover:bg-sky-700 text-white font-medium py-2 px-4 rounded-lg flex items-center space-x-2"
        >
          <PlusCircle size={20} />
          <span>Adicionar Turma</span>
        </button>
      </div>

      {facs.length === 0 ? (
        <p className="text-center text-gray-500 py-8">Nenhuma turma (FAC) cadastrada ainda.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {financialSummaries.map(summary => {
            const facDetail = facs.find(f => f.code === summary.facCode);
            return facDetail ? <FacCard key={summary.facCode} summary={summary} fac={facDetail} onManageExpenses={handleManageExpenses} /> : null;
          })}
        </div>
      )}

      <FacFormModal isOpen={isFacModalOpen} onClose={() => setIsFacModalOpen(false)} facCode={editingFacCode} />
      {managingExpensesForFac && (
        <ExpenseModal 
            isOpen={isExpenseModalOpen} 
            onClose={() => { setIsExpenseModalOpen(false); setManagingExpensesForFac(null); }} 
            facCode={managingExpensesForFac} 
        />
      )}
    </div>
  );
};

export default FacManagementPage;