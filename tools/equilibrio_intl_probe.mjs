// Observe this runtime, not institutional style; never parse source strings.
import assert from 'node:assert/strict';
const observations=['it-IT','it-CH'].map(locale=>({locale,
  numbers:[0,-1234.56,1234.56,12345.67].map(value=>({value,display:new Intl.NumberFormat(locale).format(value)})),
  currencies:['EUR','CHF'].map(currency=>({currency,value:12345.67,display:new Intl.NumberFormat(locale,{style:'currency',currency}).format(12345.67)})),
  percent:new Intl.NumberFormat(locale,{style:'percent',maximumFractionDigits:1}).format(0.125),
  date:new Intl.DateTimeFormat(locale,{dateStyle:'long',timeZone:'Europe/Rome'}).format(new Date('2026-10-19T12:00:00Z'))}));
for(const o of observations){assert.equal(Intl.NumberFormat.supportedLocalesOf([o.locale]).length,1);assert.equal(o.numbers[1].value,-1234.56);assert.ok(o.numbers[1].display.includes('-'));assert.notEqual(o.numbers[2].display,o.numbers[3].display);}
assert.notEqual(observations[0].numbers[3].display,observations[1].numbers[3].display);
console.log(JSON.stringify({node:process.version,icu:process.versions.icu,cldr:process.versions.cldr,options:'default number; explicit EUR/CHF; percent maxFractionDigits=1; dateStyle long, Europe/Rome',observations,scope:'Runtime observations only; no source parsing, no institutional house-style validation'},null,2));
