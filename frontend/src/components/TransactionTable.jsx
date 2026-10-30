import { formatDate, formatMoney } from "../utils/formatters.js";
import { Empty } from "./ui.jsx";

export default function TransactionTable({ items, loading, onEdit, onDelete, compact = false }) {
  if (loading) return <div className="empty">Загружаем операции…</div>;
  if (items.length === 0) return <Empty title="Операций пока нет" text="Добавьте операцию или измените параметры фильтра." />;

  return (
    <div className="table-wrap">
      <table className={compact ? "compact" : ""}>
        <thead><tr><th>Операция</th>{!compact && <th>Описание</th>}<th>Дата</th><th className="align-right">Сумма</th><th /></tr></thead>
        <tbody>{items.map((item) => (
          <tr key={item.id}>
            <td><div className="operation-cell"><span className={item.type === "income" ? "operation-icon income-bg" : "operation-icon expense-bg"}>{item.type === "income" ? "↗" : "↘"}</span><span><b>{item.category_name}</b>{compact && <small>{item.description || (item.type === "income" ? "Доход" : "Расход")}</small>}</span></div></td>
            {!compact && <td className="description">{item.description || "—"}</td>}
            <td className="date-cell">{formatDate(item.date)}</td>
            <td className={"amount " + (item.type === "income" ? "income-text" : "expense-text")}>{item.type === "income" ? "+" : "−"}{formatMoney(item.amount)}</td>
            <td><div className="row-actions"><button className="icon-button" title="Редактировать" aria-label="Редактировать" onClick={() => onEdit(item)}>✎</button><button className="icon-button danger" title="Удалить" aria-label="Удалить" onClick={() => onDelete(item)}>×</button></div></td>
          </tr>
        ))}</tbody>
      </table>
    </div>
  );
}