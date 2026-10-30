import { useMemo, useState } from "react";
import CategoriesView from "./components/CategoriesView.jsx";
import CategoryForm from "./components/CategoryForm.jsx";
import OverviewView from "./components/OverviewView.jsx";
import Sidebar from "./components/Sidebar.jsx";
import TransactionForm from "./components/TransactionForm.jsx";
import TransactionsView from "./components/TransactionsView.jsx";
import { Notice } from "./components/ui.jsx";
import useCategories from "./hooks/useCategories.js";
import useStatistics from "./hooks/useStatistics.js";
import useTransactions from "./hooks/useTransactions.js";
import { formatDate, formatMoney } from "./utils/formatters.js";

const PAGE_SIZE = 10;

export default function App() {
  const [view, setView] = useState("overview");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const { statistics, loadingStats, loadStatistics } = useStatistics(setError);
  const [dataRevision, setDataRevision] = useState(0);

  function refreshData() {
    setDataRevision((revision) => revision + 1);
  }

  const categoryState = useCategories({
    onError: setError,
    onMessage: setMessage,
    loadStatistics,
    onDataChanged: refreshData,
  });
  const {
    categories,
    saving: categorySaving,
    categoryOpen,
    setCategoryOpen,
    editingCategory,
    categoryName,
    setCategoryName,
    startCategory,
    submitCategory,
    removeCategory,
  } = categoryState;

  const transactionState = useTransactions(categories, {
    onError: setError,
    onMessage: setMessage,
    loadStatistics,
    dataRevision,
    onDataChanged: refreshData,
  });
  const {
    transactions,
    total,
    page,
    setPage,
    loading,
    saving: transactionSaving,
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
  } = transactionState;

  function openTransaction(transaction = null) {
    const started = startTransaction(transaction);
    if (!started) setView("categories");
  }

  const topCategories = useMemo(
    () => (statistics?.categories || []).filter((item) => Number(item.expense) > 0).slice(0, 5),
    [statistics],
  );
  const title = { overview: "Обзор", transactions: "Операции", categories: "Категории" }[view];

  return (
    <div className="app-shell">
      <Sidebar view={view} onChangeView={setView} />
      <main className="main-content">
        <header className="topbar">
          <div><p className="eyebrow">УПРАВЛЕНИЕ ФИНАНСАМИ</p><h1>{title}</h1></div>
          <div className="top-actions"><span className="today">{formatDate(new Date(), false)}</span><button className="button primary" onClick={() => openTransaction()}>＋ Новая операция</button></div>
        </header>

        {error && <Notice kind="error" text={error} onClose={() => setError("")} />}
        {message && <Notice kind="success" text={message} onClose={() => setMessage("")} />}

        {view === "overview" && <OverviewView
          statistics={statistics}
          loadingStats={loadingStats}
          transactions={transactions}
          loading={loading}
          topCategories={topCategories}
          formatMoney={formatMoney}
          onChangeView={setView}
          onEditTransaction={openTransaction}
          onDeleteTransaction={removeTransaction}
        />}
        {view === "transactions" && <TransactionsView
          total={total}
          filters={filters}
          categories={categories}
          transactions={transactions}
          loading={loading}
          page={page}
          pageSize={PAGE_SIZE}
          onChangeFilter={changeFilter}
          onResetFilters={resetFilters}
          onPageChange={setPage}
          onEditTransaction={openTransaction}
          onDeleteTransaction={removeTransaction}
        />}
        {view === "categories" && <CategoriesView
          categories={categories}
          onAddCategory={() => startCategory()}
          onEditCategory={startCategory}
          onDeleteCategory={removeCategory}
        />}

        <footer><b>FinTrack</b><span>Учебный проект · React + FastAPI</span></footer>
      </main>

      {transactionOpen && <TransactionForm
        editingTransaction={editingTransaction}
        transactionForm={transactionForm}
        setTransactionForm={setTransactionForm}
        categories={categories}
        saving={transactionSaving}
        onSubmit={submitTransaction}
        onClose={() => setTransactionOpen(false)}
      />}
      {categoryOpen && <CategoryForm
        editingCategory={editingCategory}
        categoryName={categoryName}
        setCategoryName={setCategoryName}
        saving={categorySaving}
        onSubmit={submitCategory}
        onClose={() => setCategoryOpen(false)}
      />}
    </div>
  );
}