export function NavButton({ active, onClick, icon, children }) {
  return <button className={active ? "nav-button active" : "nav-button"} onClick={onClick}><span>{icon}</span>{children}</button>;
}

export function Notice({ kind, text, onClose }) {
  return <div className={"notice " + kind} role={kind === "error" ? "alert" : "status"}><span>{text}</span><button onClick={onClose} aria-label="Закрыть">×</button></div>;
}

export function StatCard({ title, value, hint, icon, color }) {
  return <article className="stat-card"><div className="stat-top"><span>{title}</span><i className={"stat-icon " + color}>{icon}</i></div><b>{value}</b><small>{hint}</small></article>;
}

export function PanelTitle({ title, subtitle, action, onAction, extra }) {
  return <div className="panel-title"><div><h3>{title}</h3><p>{subtitle}</p></div>{extra || (action && <button className="link-button" onClick={onAction}>{action}</button>)}</div>;
}

export function Empty({ title, text }) {
  return <div className="empty-state"><span>↗</span><b>{title}</b><p>{text}</p></div>;
}

export function Modal({ title, onClose, children }) {
  return <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}><section className="modal" role="dialog" aria-modal="true" aria-label={title}><header className="modal-header"><h2>{title}</h2><button className="modal-close" onClick={onClose} aria-label="Закрыть">×</button></header>{children}</section></div>;
}