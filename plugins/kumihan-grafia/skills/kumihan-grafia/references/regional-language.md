# Región, sentido y conservación / Regional context and preservation

Esta guía desarrolla ES-L01–L09, ES-T07 y ES-DQ01/DQ03–DQ05. Es orientación para revisar contexto, no un detector de dialecto ni un motor de reescritura. `locales/regional/context-policy.json` contiene el modelo opcional; los perfiles de locale conservan los campos planos existentes. No exigir claves internas al usuario: resolver el contexto disponible y preguntar solo por datos que cambian una decisión necesaria.

## Herencia con alcance

Separar idioma del texto y de sus fragmentos, mercado, lector, medio, papel de texto, estilo de marca, pronombre, paradigma verbal, plural, sentido léxico, locale de formato, moneda, zona, redondeo y tipo de fecha. La instrucción explícita para un componente precede al estilo aprobado para ese medio y al estilo del proyecto. Sin política, conservar el original y `inherit`/`null`. Si dos valores explícitos discrepan, registrar el conflicto y su ámbito; no rellenar uno silenciosamente a partir del país. Los campos planos y anidados incompatibles requieren revisión. El nombre de un idioma no decide mercado, moneda, zona ni tratamiento.

## Tratamiento y vocabulario

No transformar Colombia en una obligación de usted, Guatemala en vos ni España en vosotros. Un texto aprobado con tú conserva esa elección. Vos puede coexistir con te, tu y tuyo; el voseo verbal y el pronominal son dimensiones distintas. El paradigma rioplatense no invalida el chileno ni una combinación regional aprobada de tú y voseo verbal. Diferencias entre web, SNS, contratos o mensajes de servicio pueden ser políticas legítimas del mismo proyecto.

Registrar término, sentido, lector, mercado, medio, edición de la fuente y estilo adoptado. Guagua, palta o coger requieren comprobar sentido y riesgo; una etiqueta geográfica del diccionario no prohíbe la palabra en el resto del mundo. En las etiquetas del Diccionario de americanismos, ES puede significar El Salvador: no tratarla como el código ISO de España.

El DPD de segunda edición reconoce usos americanos de aplicar en solicitudes/candidaturas y no aplica. Solicitar puede ser una elección editorial, pero aplicar no es un error automático. Ahorita, ahora y ya no garantizan fecha, duración ni dirección temporal. En una entrega, devolución o contrato, indicar el plazo no confirmado y conservarlo; cambiar ahorita por ahora no determina el dato que falta.

## Texto, formato y mercado

Es-US es español para un público concreto; no es en-US ni exige traducción literal. Declarar el idioma de fragmentos, mantener nombres oficiales en inglés y no importar Title Case o puntuación inglesa globalmente. Es-419 puede servir al texto compartido mientras distintos nodos usan formatos regionales explícitos. Su herencia CLDR no elimina las sobrescrituras por locale. Es-419 es válido como idioma, pero no se convierte mecánicamente en hreflang de Google ni justifica páginas alternantes inexistentes.

Distinguir prosa editorial y nodos Intl: espacios de porcentajes o agrupaciones editoriales no son una orden de normalizar la salida del formatter. Conservar valor original, código de moneda explícito, precisión y redondeo por separado; $ no identifica USD. Conservar formatToParts y resolvedOptions con entrada, locale solicitado y versiones del entorno. Un resultado de Node no certifica Office, PDF, todos los navegadores o todos los mercados. Mantener date-only como fecha de calendario; no convertirla implícitamente a instante UTC. La zona de un instante y un orden de fecha ambiguo no se deducen de es-US.

## Citas, marcas y cambios

Elegir comillas según medio y house style. Recomendaciones editoriales, guías institucionales y delimitadores CLDR pueden diferir; no fijar España=«» y América=“”. Mantener citas literales, código, identificadores y marcas. Comparaciones de marca deben separar producto, canal, campaña, fecha y condiciones jurídicas: una diferencia observada no demuestra una preferencia nacional. No redistribuir publicidad ajena como texto original propio.

La revisión no escribe el original. Cualquier edición autorizada conserva el original y muestra un diff de propuestas, incluidos cambios de significado, promesas o público objetivo. Preservar nombres, URLs, IDs, cantidades, precios, fechas, acentos, secuencias Unicode descompuestas y espacios especiales. No completar unidades ausentes ni resolver contradicciones de fuentes con conjeturas; dejar CONFLICTED_SOURCE/NEEDS_HUMAN_EDITORIAL y continuar las verificaciones independientes.

## Fuentes y límites / Sources and limits

La recuperación de estas fuentes se registró el 2026-10-22; no constituye una nueva consulta ni una certificación del entorno del usuario. La investigación base del 2026-10-18 permanece separada. Solo se incluyen síntesis propias y enlaces, sin copy comercial, imágenes ni investigación interna completa.

- [RAE/ASALE, DPD segunda edición: voseo](https://www.rae.es/dpd/voseo) y [aplicar](https://www.rae.es/dpd/aplicar): norma y variantes con contexto; no preferencias nacionales universales.
- [ASALE: ahorita](https://www.asale.org/damer/ahorita), [DEM: ahorita](https://dem.colmex.mx/ver/ahorita), [DLE: ahora](https://dle.rae.es/ahora) y [ya](https://dle.rae.es/ya): sentidos temporales, no compromisos operativos.
- [Head Start, guía de traducción](https://headstart.gov/culture-language/article/style-guide-translations-spanish): política de esa organización por medio, no norma obligatoria de otras marcas.
- [gub.uy: cómo habla el sitio](https://www.gub.uy/ayuda/comunicacion/noticias/habla-nuestro-sitio): lector, momento e importancia del trámite; no estilo obligatorio de todo Uruguay.
- [W3C: language tags](https://www.w3.org/International/articles/language-tags/), [CLDR release-48 supplementalData](https://github.com/unicode-org/cldr/blob/release-48/common/supplemental/supplementalData.xml) y [resumen español CLDR 48](https://www.unicode.org/cldr/charts/48/summary/es.html): etiqueta, herencia y datos estáticos; no comportamiento verificado de cada runtime.
- [RAE/ASALE: comillas](https://www.rae.es/dpd/comillas): distinguir recomendación editorial y política de cada producto.

English: inherit only scoped, approved context. Keep language, audience, market, address and numeric formatting independent. Record uncertainty, provenance and source edition. Regional observations are review evidence, never authority to replace source text, invent transaction facts or claim untested native rendering.
