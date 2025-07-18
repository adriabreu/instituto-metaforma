import React from 'react';
import { Student } from '../types';
import { Edit, Trash2, Eye } from 'lucide-react'; // Eye for view details later

interface StudentTableProps {
  students: Student[];
  onEdit: (studentId: string) => void;
  onDelete: (studentId: string) => void;
}

const StudentTable: React.FC<StudentTableProps> = ({ students, onEdit, onDelete }) => {
  if (students.length === 0) {
    return <p className="text-center text-gray-500 py-8">Nenhum aluno cadastrado ainda.</p>;
  }

  return (
    <div className="bg-white shadow-xl rounded-lg overflow-x-auto" role="region" aria-label="Students Table">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome Completo</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turma (FAC)</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Telefone</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status Matrícula</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {students.map((student) => (
            <tr key={student.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{student.fullName}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{student.email}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{student.facCode}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{student.phone}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  student.enrollmentStatus === 'Matriculado' ? 'bg-green-100 text-green-800' : 
                  student.enrollmentStatus === 'Cancelado' ? 'bg-red-100 text-red-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {student.enrollmentStatus || 'N/A'}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button onClick={() => onEdit(student.id)} className="text-sky-600 hover:text-sky-800 transition-colors" title="Editar">
                  <Edit size={18} />
                </button>
                <button onClick={() => onDelete(student.id)} className="text-red-600 hover:text-red-800 transition-colors" title="Excluir">
                  <Trash2 size={18} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentTable;