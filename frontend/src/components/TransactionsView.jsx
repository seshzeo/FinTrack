import { PanelTitle } from "./ui.jsx";
import TransactionTable from "./TransactionTable.jsx";

export default function TransactionsView({ total, filters, categories, transactions, loading, page, pageSize, onChangeFilter, onResetFilters, onPageChange, onEditTransaction, onDeleteTransaction }) {
  return (
    <section className="panel">
      <PanelTitle title="История операций" subtitle="Поиск и фильтрация записей" extra={<span className="badge">{total} записей</span>} />
      <div className="filters">
        <input aria-label="Поиск" type="search" placeholder="Поиск по описанию…" value={filters.search} onChange={(event) => onChangeFilter("search", event.target.value)} />
        <select aria-label="Тип" value={filters.type} onChange={(event) => onChangeFilter("type", event.target.value)}><option value="">Все типы</option><option value="income">Доходы</option><option value="expense">Расходы</option></select>
        <select aria-label="Категория" value={filters.category_id} onChange={(event) => onChangeFilter("category_id", event.target.value)}><option value="">Все категории</option>{categories.map((category) => <option key={category.id} value={category.id}>{category.name}</option>)}</select>
        <label>С <input aria-label="Дата с" type="date" value={filters.date_from} onChange={(event) => onChangeFilter("date_from", event.target.value)} /></label>
        <label>По <input aria-label="Дата по" type="date" value={filters.date_to} onChange={(event) => onChangeFilter("date_to", event.target.value)} /></label>
        <button className="button secondary" onClick={onResetFilters}>Сбросить</button>
      </div>
      <TransactionTable items={transactions} loading={loading} onEdit={onEditTransaction} onDelete={onDeleteTransaction} />
      <div className="pagination"><span>Показано {total ? page * pageSize + 1 : 0}–{Math.min((page + 1) * pageSize, total)} из {total}</span><div><button className="button secondary" disabled={page === 0} onClick={() => onPageChange((current) => current - 1)}>← Назад</button><span> Страница {page + 1} из {Math.max(1, Math.ceil(total / pageSize))} </span><button className="button secondary" disabled={(page + 1) * pageSize >= total} onClick={() => onPageChange((current) => current + 1)}>Далее →</button></div></div>
    </section>
  );
}