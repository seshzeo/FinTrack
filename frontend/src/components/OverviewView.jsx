import { Empty, PanelTitle, StatCard } from "./ui.jsx";
import TransactionTable from "./TransactionTable.jsx";

export default function OverviewView({ statistics, loadingStats, transactions, loading, topCategories, formatMoney, onChangeView, onEditTransaction, onDeleteTransaction }) {
  return (
    <>
      <section className="welcome"><span className="overline">ВАША ФИНАНСОВАЯ СВОДКА</span><h2>Деньги под контролем</h2><p>Доходы, расходы и история операций — в одном месте.</p><span className="welcome-symbol">₽</span></section>
      <section className="stat-grid">
        <StatCard title="Баланс" value={loadingStats ? "Загрузка…" : formatMoney(statistics?.balance)} hint="Доходы минус расходы" icon="◈" color="purple" />
        <StatCard title="Доходы" value={loadingStats ? "Загрузка…" : formatMoney(statistics?.total_income)} hint="Все поступления" icon="↗" color="green" />
        <StatCard title="Расходы" value={loadingStats ? "Загрузка…" : formatMoney(statistics?.total_expense)} hint="Все списания" icon="↘" color="orange" />
        <StatCard title="Операции" value={loadingStats ? "—" : String(statistics?.operations_count || 0)} hint="Всего записей" icon="▤" color="blue" />
      </section>
      <section className="overview-grid">
        <div className="panel">
          <PanelTitle title="Расходы по категориям" subtitle="Самые крупные статьи расходов" action="Категории →" onAction={() => onChangeView("categories")} />
          {loadingStats ? <p className="empty">Загрузка статистики…</p> : topCategories.length === 0 ? <Empty title="Расходов пока нет" text="Добавьте расход, чтобы увидеть аналитику." /> : <div className="category-bars">{topCategories.map((item, index) => {
            const totalExpense = Number(statistics?.total_expense || 0);
            const percent = totalExpense ? Math.min(100, Number(item.expense) / totalExpense * 100) : 0;
            return <div className="bar-row" key={item.category_id}><div className="bar-heading"><span><i className={"dot dot-" + (index % 5)} />{item.category_name}</span><b>{formatMoney(item.expense)}</b></div><div className="track"><i style={{ width: percent + "%" }} className={"bar bar-" + (index % 5)} /></div><small>{percent.toFixed(1)}% от всех расходов</small></div>;
          })}</div>}
        </div>
        <div className="panel">
          <PanelTitle title="Последние операции" subtitle="Недавно добавленные записи" action="Все операции →" onAction={() => onChangeView("transactions")} />
          <TransactionTable items={transactions.slice(0, 5)} loading={loading} onEdit={onEditTransaction} onDelete={onDeleteTransaction} compact />
        </div>
      </section>
    </>
  );
}