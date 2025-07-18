
import React, { useState } from 'react';
import StudentTable from '../components/StudentTable';
import StudentFormModal from '../components/StudentFormModal';
import { useAppContext } from '../context/AppContext';
import { PlusCircle } from 'lucide-react';

const StudentsPage: React.FC = () => {
  const { students, addStudent, updateStudent, deleteStudent } = useAppContext();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingStudentId, setEditingStudentId] = useState<string | null>(null);

  const openAddModal = () => {
    setEditingStudentId(null);
    setIsModalOpen(true);
  };

  const openEditModal = (studentId: string) => {
    setEditingStudentId(studentId);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingStudentId(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-semibold text-gray-800">Gerenciamento de Alunos</h1>
        <button
          onClick={openAddModal}
          className="bg-sky-600 hover:bg-sky-700 text-white font-medium py-2 px-4 rounded-lg flex items-center space-x-2 transition-colors"
        >
          <PlusCircle size={20} />
          <span>Adicionar Aluno</span>
        </button>
      </div>

      <StudentTable students={students} onEdit={openEditModal} onDelete={deleteStudent} />

      {isModalOpen && (
        <StudentFormModal
          isOpen={isModalOpen}
          onClose={closeModal}
          studentId={editingStudentId}
        />
      )}
    </div>
  );
};

export default StudentsPage;
