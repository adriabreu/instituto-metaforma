import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Student, Course, Fac, Payment, Expense } from '../types';

export type AppContextType = {
  students: Student[];
  courses: Course[];
  facs: Fac[];
  payments: Payment[];
  expenses: Expense[];
  addStudent: (student: Student) => void;
  updateStudent: (student: Student) => void;
  deleteStudent: (id: string) => void;
  addCourse: (course: Course) => void;
  updateCourse: (course: Course) => void;
  deleteCourse: (id: string) => void;
  addFac: (fac: Fac) => void;
  updateFac: (fac: Fac) => void;
  deleteFac: (id: string) => void;
  addPayment: (payment: Payment) => void;
  updatePayment: (payment: Payment) => void;
  deletePayment: (id: string) => void;
  addExpense: (expense: Expense) => void;
  updateExpense: (expense: Expense) => void;
  deleteExpense: (id: string) => void;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

const LOCAL_STORAGE_KEY = 'metaforma_app_data';

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [facs, setFacs] = useState<Fac[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [expenses, setExpenses] = useState<Expense[]>([]);

  // Load data from localStorage on initial render
  useEffect(() => {
    try {
      const storedData = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (storedData) {
        const data = JSON.parse(storedData);
        setStudents(data.students || []);
        setCourses(data.courses || []);
        setFacs(data.facs || []);
        setPayments(data.payments || []);
        setExpenses(data.expenses || []);
      }
    } catch (error) {
      console.error("Failed to parse data from localStorage", error);
    }
  }, []);

  // Persist data to localStorage whenever state changes
  useEffect(() => {
    const dataToStore = {
      students,
      courses,
      facs,
      payments,
      expenses,
    };
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(dataToStore));
  }, [students, courses, facs, payments, expenses]);

  // Student functions
  const addStudent = (student: Student) => setStudents((prev: Student[]) => [...prev, student]);
  const updateStudent = (updatedStudent: Student) =>
    setStudents((prev: Student[]) =>
      prev.map((student: Student) => (student.id === updatedStudent.id ? updatedStudent : student))
    );
  const deleteStudent = (id: string) => setStudents((prev: Student[]) => prev.filter((student: Student) => student.id !== id));

  // Course functions
  const addCourse = (course: Course) => setCourses((prev: Course[]) => [...prev, course]);
  const updateCourse = (updatedCourse: Course) =>
    setCourses((prev: Course[]) =>
      prev.map((course: Course) => (course.id === updatedCourse.id ? updatedCourse : course))
    );
  const deleteCourse = (id: string) => setCourses((prev: Course[]) => prev.filter((course: Course) => course.id !== id));

  // Fac functions
  const addFac = (fac: Fac) => setFacs((prev: Fac[]) => [...prev, fac]);
  const updateFac = (updatedFac: Fac) =>
    setFacs((prev: Fac[]) => prev.map((fac: Fac) => (fac.id === updatedFac.id ? updatedFac : fac)));
  const deleteFac = (id: string) => setFacs((prev: Fac[]) => prev.filter((fac: Fac) => fac.id !== id));

  // Payment functions
  const addPayment = (payment: Payment) => setPayments((prev: Payment[]) => [...prev, payment]);
  const updatePayment = (updatedPayment: Payment) =>
    setPayments((prev: Payment[]) =>
      prev.map((payment: Payment) => (payment.id === updatedPayment.id ? updatedPayment : payment))
    );
  const deletePayment = (id: string) => setPayments((prev: Payment[]) => prev.filter((payment: Payment) => payment.id !== id));

  // Expense functions
  const addExpense = (expense: Expense) => setExpenses((prev: Expense[]) => [...prev, expense]);
  const updateExpense = (updatedExpense: Expense) =>
    setExpenses((prev: Expense[]) =>
      prev.map((expense: Expense) => (expense.id === updatedExpense.id ? updatedExpense : expense))
    );
  const deleteExpense = (id: string) => setExpenses((prev: Expense[]) => prev.filter((expense: Expense) => expense.id !== id));

  const contextValue: AppContextType = {
    test: "hello",
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};