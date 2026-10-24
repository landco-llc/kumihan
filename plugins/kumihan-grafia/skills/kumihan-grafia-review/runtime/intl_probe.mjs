// Offline environment observation. Explicit fixture choices never infer market or currency.
const inputs = [
 ['es','EUR'], ['es-ES','EUR'], ['es-MX','MXN'], ['es-AR','ARS'],
 ['es-CO','COP'], ['es-CL','CLP'], ['es-PE','PEN'], ['es-419','COP'], ['es-US','MXN']
];
const rawDecimal = '1234567.89123';
const numbers = inputs.map(([requested_locale, explicit_currency]) => {
 const formatter = new Intl.NumberFormat(requested_locale, {
  style: 'currency', currency: explicit_currency,
  minimumFractionDigits: 2, maximumFractionDigits: 2
 });
 return {requested_locale, explicit_currency, raw_decimal: rawDecimal,
  original_after_format: rawDecimal, supported: Intl.NumberFormat.supportedLocalesOf([requested_locale]),
  resolved: formatter.resolvedOptions(), display: formatter.format(rawDecimal),
  parts: formatter.formatToParts(rawDecimal), observation_status: 'observed',
  currency_scope: 'explicit test fixture; not a market default'};
});
const rawInstant = '2026-10-25T00:30:00Z';
const instant = new Date(rawInstant);
const instants = ['UTC', 'Europe/Madrid', 'America/Mexico_City', 'America/Argentina/Buenos_Aires'].map(explicit_timeZone => {
 const epoch_before = instant.getTime();
 const formatter = new Intl.DateTimeFormat('es', {
  year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit',
  timeZone: explicit_timeZone
 });
 const display = formatter.format(instant);
 const parts = formatter.formatToParts(instant);
 return {raw_instant: rawInstant, epoch_before, epoch_after: instant.getTime(), explicit_timeZone,
  resolved: formatter.resolvedOptions(), display, parts, observation_status: 'observed'};
});
console.log(JSON.stringify({versions: process.versions, numbers, instants,
 date_only: {raw: '2026-10-25', value_kind: 'date-only', conversion: 'not-performed'},
 native_host: 'not-checked', editorial_acceptance: 'not-checked',
 limitations: ['Runtime output only; no editorial or legal standard.',
 'No parsing of money, currency inference, civil-date conversion, copy rewrite or native rendering.']
}, null, 2));
