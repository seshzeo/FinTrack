import { Modal } from "./ui.jsx";

export default function TransactionForm({ editingTransaction, transactionForm, setTransactionForm, categories, saving, onSubmit, onClose }) {
  return (
    <Modal title={editingTransaction ? "Редактировать операцию" : "Новая операция"} onClose={onClose}>
      <form className="form" onSubmit={onSubmit}>
        <div className="type-switch"><button type="button" className={transactionForm.type === "expense" ? "selected expense" : ""} onClick={() => setTransactionForm((form) => ({ ...form, type: "expense" }))}>− Расход</button><button type="button" className={transactionForm.type === "income" ? "selected income" : ""} onClick={() => setTransactionForm((form) => ({ ...form, type: "income" }))}>＋ Доход</button></div>
        <label>Сумма, ₽<input autoFocus required type="number" min="0.01" step="0.01" value={transactionForm.amount} onChange={(event) => setTransactionForm((form) => ({ ...form, amount: event.target.value }))} placeholder="1500.00" /></label>
        <label>Категория<select required value={transactionForm.category_id} onChange={(event) => setTransactionForm((form) => ({ ...form, category_id: event.target.value }))}><option value="" disabled>Выберите категорию</option>{categories.map((category) => <option key={category.id} value={category.id}>{category.name}</option>)}</select></label>
        <label>Дата и время<input required type="datetime-local" value={transactionForm.date} onChange={(event) => setTransactionForm((form) => ({ ...form, date: event.target.value }))} /></label>
        <label>Описание <small>(необязательно)</small><textarea maxLength="500" rows="3" value={transactionForm.description} onChange={(event) => setTransactionForm((form) => ({ ...form, description: event.target.value }))} placeholder="Например, продукты на неделю" /></label>
        <div className="modal-actions"><button type="button" className="button secondary" onClick={onClose}>Отмена</button><button type="submit" className="button primary" disabled={saving}>{saving ? "Сохранение…" : "Сохранить"}</button></div>
      </form>
    </Modal>
  );
}