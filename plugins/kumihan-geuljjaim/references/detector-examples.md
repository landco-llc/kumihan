# Static candidate examples

| Rule | Positive candidate | Negative | Exception |
|---|---|---|---|
| KO-ORTH-001 | 서울 에서 출발 | 서울에서 출발 | Name, code, URL, quotation or protected copy |
| KO-ORTH-002 | 할수 있다 | 할 수 있다 | A protected product name or intentional poetic form |
| KO-TYPE-010 | 13,000 followed by newline then 원 | 13,000원 | Table cell boundary, protected text |
| KO-TYPE-001 | ᄒ followed by newline then ᅡᆫ | 한 | Educational decomposition, protected text |

Every candidate returns needs-review. Caller must classify segments and can withhold protected content from prose recognition. 3개 and 3 개 are both negative examples; there is no unconditional unit-spacing rewrite. Runtime does not analyze raw HTML, perform full grapheme segmentation or simulate rendered wraps. Positive/negative/protected-role cases are executable in tests/geuljjaim/test_product.py.
