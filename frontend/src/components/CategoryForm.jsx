import { Modal } from "./ui.jsx";

export default function CategoryForm({ editingCategory, categoryName, setCategoryName, saving, onSubmit, onClose }) {
  return (
    <Modal title={editingCategory ? "Переименовать категорию" : "Новая категория"} onClose={onClose}>
      <form className="form" onSubmit={onSubmit}>
        <label>Название<input autoFocus required minLength="1" maxLength="100" value={categoryName} onChange={(event) => setCategoryName(event.target.value)} placeholder="Например, Кафе" /></label>
        <p className="form-help">Название должно быть уникальным, длина — до 100 символов.</p>
        <div className="modal-actions"><button type="button" className="button secondary" onClick={onClose}>Отмена</button><button type="submit" className="button primary" disabled={saving || !categoryName.trim()}>{saving ? "Сохранение…" : "Сохранить"}</button></div>
      </form>
    </Modal>
  );
}