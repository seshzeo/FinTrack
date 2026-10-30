import { NavButton } from "./ui.jsx";

export default function Sidebar({ view, onChangeView }) {
  return (
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">F</span><span><b>FinTrack</b><small>личные финансы</small></span></div>
      <p className="nav-label">МЕНЮ</p>
      <nav>
        <NavButton active={view === "overview"} onClick={() => onChangeView("overview")} icon="▦">Обзор</NavButton>
        <NavButton active={view === "transactions"} onClick={() => onChangeView("transactions")} icon="↕">Операции</NavButton>
        <NavButton active={view === "categories"} onClick={() => onChangeView("categories")} icon="◫">Категории</NavButton>
      </nav>
      <div className="sidebar-bottom"><span className="online-dot" /> API-подключение<br /><small>Учебный проект FinTrack</small></div>
    </aside>
  );
}