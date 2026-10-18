// Observed ICU behavior only: no claim of semantic correctness or custom dictionary.
import assert from 'node:assert/strict';
const samples = ['เก', 'น้ำ', 'ก่ํ', '😀ไทย', 'ภาษาไทยอ่านได้โดยไม่ต้องแทรกช่องว่าง', 'ราคา 1,250 บาท ๆ ฯ'];
if (typeof Intl.Segmenter !== 'function') {
  console.log(JSON.stringify({status:'unsupported', engine:process.version}));
} else {
  const results = samples.map(text => {
    const graphemes = [...new Intl.Segmenter('th', {granularity:'grapheme'}).segment(text)];
    const words = [...new Intl.Segmenter('th', {granularity:'word'}).segment(text)];
    assert.equal(graphemes.map(x => x.segment).join(''), text);
    assert.equal(words.map(x => x.segment).join(''), text);
    for (const x of [...graphemes, ...words]) assert.equal(text.slice(x.index, x.index+x.segment.length), x.segment);
    return {text, graphemes, words};
  });
  const emoji = results.find(x => x.text === '😀ไทย');
  assert.equal(emoji.graphemes[0].index, 0);
  assert.equal(emoji.graphemes[1].index, 2);
  console.log(JSON.stringify({status:'passed',engine:process.version,icu:process.versions.icu,scope:'ICU Thai word/grapheme sample reconstruction and UTF-16 offsets; semantic quality needs-review',results},null,2));
}
