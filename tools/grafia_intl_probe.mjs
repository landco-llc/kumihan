// Environment observations only. Currency/timezone are explicit test inputs, never inferred.
import assert from 'node:assert/strict';
const observations=[];
for(const [locale,currency] of [['es-ES','EUR'],['es-MX','MXN'],['es-AR','ARS'],['es-CO','COP'],['es-CL','CLP'],['es-PE','PEN'],['es-419','USD']]){
 const value=1234.56;const f=new Intl.NumberFormat(locale,{style:'currency',currency});
 assert.equal(value,1234.56);assert.equal(f.resolvedOptions().currency,currency);
 assert.equal(Intl.NumberFormat.supportedLocalesOf([locale]).length,1);
 observations.push({locale,currency,original:value,display:f.format(value),parts:f.formatToParts(value),resolved:f.resolvedOptions(),status:'passed',scope:'explicit format observation; original value preserved'});
}
const instant=new Date('2026-10-19T01:30:00Z');
for(const timeZone of ['Europe/Madrid','America/Mexico_City']){
 const f=new Intl.DateTimeFormat('es',{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',timeZone});
 observations.push({timeZone,original:instant.toISOString(),display:f.format(instant),parts:f.formatToParts(instant),resolved:f.resolvedOptions(),status:'passed',scope:'explicit instant format observation'});
}
assert.equal(instant.toISOString(),'2026-10-19T01:30:00.000Z');
console.log(JSON.stringify({versions:process.versions,observations,date_only:'not converted; no formatter API supplied for civil date',native_proofreading:'not-checked'},null,2));
