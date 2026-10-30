import { Empty, PanelTitle } from "./ui.jsx";

export default function CategoriesView({ categories, onAddCategory, onEditCategory, onDeleteCategory }) {
  return (
    <section className="panel">
      <PanelTitle title="Категории" subtitle="Категории помогают группировать доходы и расходы" action="＋ Добавить категорию" onAction={onAddCategory} />
      {categories.length === 0 ? <Empty title="Категорий пока нет" text="Создайте категорию для первой операции." /> : <div className="category-grid">{categories.map((category, index) => <article className="category-card" key={category.id}><span className={"category-avatar avatar-" + (index % 5)}>{category.name.slice(0, 1).toUpperCase()}</span><div className="category-card-text"><b>{category.name}</b><small>{category.is_default ? "Стандартная" : "Пользовательская"}</small></div>{category.is_default ? <span className="system-label">Системная</span> : <div className="category-actions"><button className="icon-button" title="Переименовать" onClick={() => onEditCategory(category)}>✎</button><button className="icon-button danger" title="Удалить" onClick={() => onDeleteCategory(category)}>×</button></div>}</article>)}</div>}
      <p className="info-note">Стандартные категории нельзя удалить. Категория, которая используется в операциях, также не может быть удалена.</p>
    </section>
  );
}