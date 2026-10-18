---
name: kumihan-compasso-documents
description: "Organiza texto, tipografia e design em português sem alterar o original. | Structure Portuguese typography and content design while preserving original text."
---

# KUMIHAN｜Compasso

Skill independente v0.1.0 / Standalone Portuguese skill.

1. Defina explicitamente pt-BR, pt-PT ou outro mercado, meio, leitor, intenção e manual de estilo. O mercado não determina automaticamente aspas, moeda, pronome ou separadores.
2. Preserve sempre os bytes UTF-8 do original, marcas, números, nomes, citações, URL e significado. Revisão é não destrutiva; alterações exigem autorização e diff.
3. Consulte rules/catalog.json (36 regras), locales/house-styles.json e sources.json. Para documents, escolha prioridades de composição conforme a intenção e a função do texto.
4. Rejeite padrões genéricos de aparência «AI-generated»: gradientes decorativos, cartões repetidos sem hierarquia, espaçamento artificial, títulos excessivos e CTA sem contexto. Componha conteúdo, legibilidade e identidade de marca.
5. Trate hifenização, quebras de linha, glifos, diacríticos, PDF, 320px, 200% e implementação real apenas com evidência de renderização. Sem observação, informe NOT_CHECKED.
6. O verificador local `python runtime/checks.py original.txt --locale pt-BR` apenas sugere verificações. Não edita arquivos, não corrige português nem certifica design.
7. Devolva contexto, regras acionadas, trechos originais, sugestões com fundamento, impacto, testes realizados e não realizados.

EN: Select region and house style explicitly, preserve originals, favor content-led typographic design, and distinguish static candidates from real render observations.
