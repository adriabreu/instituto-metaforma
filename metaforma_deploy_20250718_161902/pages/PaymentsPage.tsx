
import React, { useState, useMemo } from 'react';
import { useAppContext } from '../context/AppContext';
import { PaymentInstallment, Student, PaymentStatus } from '../types';
import { CheckCircle, XCircle, Clock, Edit3 } from 'lucide-react';

const PaymentsPage: React.FC = () => {
  const { students, facs, updatePaymentInstallment } = useAppContext();
  const [selectedFac, setSelectedFac] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [editingInstallment, setEditingInstallment] = useState<PaymentInstallment | null>(null);
  const [editStatus, setEditStatus] = useState<PaymentStatus>(PaymentStatus.PENDING);
  const [editPaymentDate, setEditPaymentDate] = useState<string>('');
  const [editNotes, setEditNotes] = useState<string>('');


  const filteredStudents = useMemo(() => {
    return students.filter(student => 
      (selectedFac === '' || student.facCode === selectedFac) &&
      (searchTerm === '' || student.fullName.toLowerCase().includes(searchTerm.toLowerCase()) || student.email.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  }, [students, selectedFac, searchTerm]);

  const allInstallments = useMemo(() => {
    return filteredStudents.flatMap(student => 
      student.paymentInstallments.map(inst => ({ ...inst, studentName: student.fullName, studentEmail: student.email, facCode: student.facCode }))
    ).sort((a,b) => new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime());
  }, [filteredStudents]);

  const openEditModal = (installment: PaymentInstallment) => {
    setEditingInstallment(installment);
    setEditStatus(installment.status);
    setEditPaymentDate(installment.paymentDate || '');
    setEditNotes(installment.notes || '');
  };

  const closeEditModal = () => {
    setEditingInstallment(null);
  };

  const handleSaveEdit = () => {
    if (editingInstallment) {
      updatePaymentInstallment(editingInstallment.studentId, editingInstallment.id, {
        status: editStatus,
        paymentDate: editStatus === PaymentStatus.PAID && editPaymentDate ? editPaymentDate : undefined,
        notes: editNotes,
      });
      closeEditModal();
    }
  };
  
  const getStatusIconAndColor = (status: PaymentStatus) => {
    switch (status) {
      case PaymentStatus.PAID: return { icon: <CheckCircle className="text-green-500" size={18}/>, color: "text-green-600 bg-green-100" };
      case PaymentStatus.OVERDUE: return { icon: <XCircle className="text-red-500" size={18}/>, color: "text-red-600 bg-red-100" };
      case PaymentStatus.CANCELED: return { icon: <XCircle className="text-gray-500" size={18}/>, color: "text-gray-600 bg-gray-100" };
      default: return { icon: <Clock className="text-yellow-500" size={18}/>, color: "text-yellow-600 bg-yellow-100" };
    }
  };


  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold text-gray-800">Gerenciamento de Pagamentos</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 p-4 bg-white rounded-lg shadow">
        <div>
          <label htmlFor="facFilter" className="block text-sm font-medium text-gray-700">Filtrar por Turma (FAC):</label>
          <select 
            id="facFilter" 
            value={selectedFac} 
            onChange={e => setSelectedFac(e.target.value)}
            className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-sky-500 focus:border-sky-500 sm:text-sm"
          >
            <option value="">Todas as Turmas</option>
            {facs.map(fac => <option key={fac.code} value={fac.code}>{fac.name} ({fac.code})</option>)}
          </select>
        </div>
        <div>
          <label htmlFor="searchTerm" className="block text-sm font-medium text-gray-700">Buscar Aluno (Nome/Email):</label>
          <input 
            type="text" 
            id="searchTerm"
            placeholder="Digite nome ou email..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-sky-500 focus:border-sky-500 sm:text-sm"
          />
        </div>
      </div>

      {allInstallments.length === 0 ? (
         <p className="text-center text-gray-500 py-8">Nenhuma parcela encontrada para os filtros selecionados.</p>
      ) : (
      <div className="bg-white shadow-xl rounded-lg overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="th-cell">Aluno</th>
              <th className="th-cell">Turma</th>
              <th className="th-cell">Parcela</th>
              <th className="th-cell">Vencimento</th>
              <th className="th-cell">Valor (R$)</th>
              <th className="th-cell">Status</th>
              <th className="th-cell">Data Pagto.</th>
              <th className="th-cell">Ações</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {allInstallments.map(inst => {
              const {icon, color} = getStatusIconAndColor(inst.status);
              return (
                <tr key={inst.id} className="hover:bg-gray-50">
                  <td className="td-cell">{inst.studentName}<br/><span className="text-xs text-gray-500">{inst.studentEmail}</span></td>
                  <td className="td-cell">{inst.facCode}</td>
                  <td className="td-cell text-center">{inst.installmentNumber}</td>
                  <td className="td-cell">{new Date(inst.dueDate).toLocaleDateString()}</td>
                  <td className="td-cell text-right">{inst.amount.toFixed(2)}</td>
                  <td className="td-cell">
                    <span className={`px-2 py-1 inline-flex text-xs leading-tight font-semibold rounded-full ${color}`}>
                      {icon} <span className="ml-1">{inst.status}</span>
                    </span>
                  </td>
                  <td className="td-cell">{inst.paymentDate ? new Date(inst.paymentDate).toLocaleDateString() : '-'}</td>
                  <td className="td-cell">
                    <button onClick={() => openEditModal(inst)} className="text-sky-600 hover:text-sky-800" title="Editar Parcela">
                      <Edit3 size={18} />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      )}

      {editingInstallment && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">Editar Parcela</h3>
            <p className="mb-1 text-sm">Aluno: <span className="font-medium">{students.find(s=>s.id === editingInstallment.studentId)?.fullName}</span></p>
            <p className="mb-1 text-sm">Parcela: <span className="font-medium">{editingInstallment.installmentNumber}</span> | Valor: <span className="font-medium">R$ {editingInstallment.amount.toFixed(2)}</span></p>
            <p className="mb-4 text-sm">Vencimento: <span className="font-medium">{new Date(editingInstallment.dueDate).toLocaleDateString()}</span></p>
            
            <div className="mb-4">
              <label htmlFor="editStatus" className="block text-sm font-medium text-gray-700">Status</label>
              <select id="editStatus" value={editStatus} onChange={e => setEditStatus(e.target.value as PaymentStatus)} className="mt-1 block w-full input-field">
                {Object.values(PaymentStatus).map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            {editStatus === PaymentStatus.PAID && (
              <div className="mb-4">
                <label htmlFor="editPaymentDate" className="block text-sm font-medium text-gray-700">Data do Pagamento</label>
                <input type="date" id="editPaymentDate" value={editPaymentDate} onChange={e => setEditPaymentDate(e.target.value)} className="mt-1 block w-full input-field" />
              </div>
            )}
             <div className="mb-4">
                <label htmlFor="editNotes" className="block text-sm font-medium text-gray-700">Observações</label>
                <textarea id="editNotes" value={editNotes} onChange={e => setEditNotes(e.target.value)} rows={2} className="mt-1 block w-full input-field"></textarea>
            </div>
            <div className="flex justify-end space-x-2">
              <button onClick={closeEditModal} className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300">Cancelar</button>
              <button onClick={handleSaveEdit} className="px-4 py-2 text-white bg-sky-600 rounded-md hover:bg-sky-700">Salvar</button>
            </div>
          </div>
        </div>
      )}
      <style>{`
        .th-cell { padding: 0.75rem 1rem; text-align: left; font-size: 0.75rem; font-weight: 500; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; }
        .td-cell { padding: 0.75rem 1rem; font-size: 0.875rem; color: #374151; white-space: nowrap; }
        .input-field { py: 0.5rem; px: 0.75rem; border: 1px solid #D1D5DB; border-radius: 0.375rem; box-shadow: sm; focus:outline-none focus:ring-sky-500 focus:border-sky-500; font-size: 0.875rem; }
      `}</style>
    </div>
  );
};

export default PaymentsPage;

