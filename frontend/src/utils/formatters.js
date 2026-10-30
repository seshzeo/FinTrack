const money = new Intl.NumberFormat("ru-RU", { style: "currency", currency: "RUB", maximumFractionDigits: 2 });
const dateTime = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
const dateOnly = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "short", year: "numeric" });

export function formatMoney(value) {
  return money.format(Number(value || 0));
}

function parseApiDate(value) {
  if (value instanceof Date) return value;
  if (!value) return new Date(NaN);

  const text = String(value).trim();
  const hasTimezone = /(?:Z|[+-]\d{2}:?\d{2})$/i.test(text);
  return new Date(hasTimezone ? text : `${text}Z`);
}

export function formatDate(value, includeTime = true) {
  const date = parseApiDate(value);
  return Number.isNaN(date.getTime())
    ? "—"
    : (includeTime ? dateTime : dateOnly).format(date);
}

export function localDateTime(value = new Date()) {
  const date = parseApiDate(value);
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000)
    .toISOString()
    .slice(0, 16);
}