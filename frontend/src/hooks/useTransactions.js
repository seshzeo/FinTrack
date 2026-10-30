import { useEffect, useState } from "react";
import { api } from "../api.js";
import { localDateTime } from "../utils/formatters.js";

const PAGE_SIZE = 10;

export default function useTransactions(categories, { onError, onMessage, loadStatistics, dataRevision, onDataChanged }) {
  const [transactions, setTransactions] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [filters, setFilters] = useState({ search: "", type: "", category_id: "", date_from: "", date_to: "" });
  const [transactionOpen, setTransactionOpen] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [transactionForm, setTransactionForm] = useState({ type: "expense", amount: "", category_id: "", date: localDateTime(), description: "" });

  useEffect(() => {
    let current = true;
    setLoading(true);
    api.getTransactions({ ...filters, limit: PAGE_SIZE, offset: page * PAGE_SIZE })
      .then((data) => {
        if (!current) return;
        setTransactions(data.items || []);
        setTotal(data.total || 0);
      })
      .catch((error) => {
        if (current) onError(error.message);
      })
      .finally(() => {
        if (current) setLoading(false);
      });
    return () => {
      current = false;
    };
  }, [filters, page, dataRevision, onError]);

  function changeFilter(name, value) {
    setFilters((old) => ({ ...old, [name]: value }));
    setPage(0);
  }

  function resetFilters() {
    setFilters({ search: "", type: "", category_id: "", date_from: "", date_to: "" });
    setPage(0);
  }

  function startTransaction(transaction = null) {
    onError("");
    onMessage("");
    if (!transaction && categories.length === 0) {
      onError("Сначала создайте категорию, затем добавьте операцию.");
      return false;
    }

    setEditingTransaction(transaction);
    setTransactionForm(transaction ? {
      type: transaction.type,
      amount: transaction.amount,
      category_id: transaction.category_id,
      date: localDateTime(transaction.date),
      description: transaction.description || "",
    } : {
      type: "expense",
      amount: "",
      category_id: categories[0]?.id || "",
      date: localDateTime(),
      description: "",
    });
    setTransactionOpen(true);
    return true;
  }

  async function submitTransaction(event) {
    event.preventDefault();
    setSaving(true);
    onError("");
    try {
      const payload = {
        type: transactionForm.type,
        amount: transactionForm.amount,
        category_id: transactionForm.category_id,
        date: new Date(transactionForm.date).toISOString(),
        description: transactionForm.description.trim() || null,
      };
      if (editingTransaction) {
        await api.updateTransaction(editingTransaction.id, payload);
        onMessage("Операция обновлена.");
      } else {
        await api.createTransaction(payload);
        onMessage("Операция добавлена.");
      }
      setTransactionOpen(false);
      onDataChanged();
      await loadStatistics();
    } catch (error) {
      onError(error.message);
    } finally {
      setSaving(false);
    }
  }

  async function removeTransaction(transaction) {
    if (!window.confirm("Удалить эту операцию?")) return;
    onError("");
    try {
      await api.deleteTransaction(transaction.id);
      onMessage("Операция удалена.");
      onDataChanged();
      await loadStatistics();
    } catch (error) {
      onError(error.message);
    }
  }

  return {
    transactions,
    total,
    page,
    setPage,
    loading,
    saving,
    filters,
    changeFilter,
    resetFilters,
    transactionOpen,
    setTransactionOpen,
    editingTransaction,
    transactionForm,
    setTransactionForm,
    startTransaction,
    submitTransaction,
    removeTransaction,
  };
}