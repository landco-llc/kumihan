// Runtime observation, not a house-style mandate or an input parser.
import assert from 'node:assert/strict';
const observations = ['de-DE','de-AT','de-CH'].map(locale => ({locale,
  number: new Intl.NumberFormat(locale).format(1234.5),
  euro: new Intl.NumberFormat(locale,{style:'currency',currency:'EUR'}).format(1234.5),
  chf: new Intl.NumberFormat(locale,{style:'currency',currency:'CHF'}).format(1234.5),
  date: new Intl.DateTimeFormat(locale,{year:'numeric',month:'long',day:'numeric',timeZone:'UTC'}).format(new Date('2026-01-01T00:00:00Z'))}));
assert.equal(observations[0].number,'1.234,5');
assert.match(observations[2].number,/^1['’]234\.5$/); // ICU/CLDR versions differ in grouping glyph; record actual output.
const originals = ['1.000','01234','0.1','Straße','STRAẞE','Müller','a\u0308'];
assert.deepEqual(originals,['1.000','01234','0.1','Straße','STRAẞE','Müller','a\u0308']);
console.log(JSON.stringify({node:process.version,icu:process.versions.icu,cldr:process.versions.cldr,observations,scope:'Observed runtime only; no parsing or source conversion'},null,2));
