# Tipografía regional por función / Regional typography by role

Elegir por contenido, marca, medio y función; un mercado no determina una fuente, tamaño, interletraje o interlineado. Conservar el original, incluidos acentos, secuencias Unicode y espacios. Las pautas siguientes amplían la revisión editorial y de salida; no son comprobaciones automáticas ni resultados de pruebas del proyecto.

## Contexto y decisiones / Context and decisions

Heredar idioma real, mercado, audiencia, medio, función del componente y estilo de marca ya aprobados. Un dato desconocido queda pendiente: no completar decisiones a partir de ES, MX, AR, CO, CL, PE, US o es-419. No pedir al usuario que rellene claves técnicas para poder continuar comprobaciones independientes. Separar titular expresivo, texto de lectura, etiqueta o botón, transacción, cita y pie de imagen. En cada rol registrar la fuente realmente utilizada, archivo y versión, peso o ejes, ancho disponible, tamaño y condiciones de lectura.

Para comillas, seguir el estilo editorial adoptado y su jerarquía de anidación, preservando la cita literal. Una preferencia de imprenta, una guía institucional y los datos de locale son fuentes distintas; no equivalen a «España usa siempre angulares» o «América usa siempre inglesas». Código, entrada literal, identificadores y citas contractuales quedan intactos. Relacionar los signos con el alcance de la cita y de la oración exterior, no sólo con su país.

## Signos, mayúsculas y Unicode / Marks, capitals and Unicode

**ES-T01/T02/T04/T05/T06/T10/T25:** Las mayúsculas de palabras conservan las tildes y diéresis necesarias; las siglas, marcas y títulos oficiales necesitan contexto. No quitar ¿¡ de una pregunta ordinaria por influencia del inglés. Determinar el tramo interrogativo o exclamativo: una pregunta dentro de una oración, un título y una cita no comparten necesariamente sus límites. Un candidato estático no convierte todas las preguntas de un titular en errores. Revisar 1.º/2.ª, ñ, á, ü y sus secuencias combinadas en el glifo real; no normalizar Unicode ni cambiar un logotipo aprobado para uniformar su apariencia.

## Saltos, cifras y fuentes / Wrapping, numbers and fonts

**ES-T14/T15/X03:** La división depende del idioma efectivo, el diccionario disponible, el motor y la salida. `lang="es-AR"` y `hyphens:auto` declaran una intención; no demuestran un diccionario argentino ni una división correcta. Registrar navegador o aplicación y versión, diccionario si es identificable y las palabras realmente divididas. No reducir toda diferencia de división a España frente a Latinoamérica. Revisar repeticiones y finales de línea por rol; no imponer división de prosa a titulares breves o botones. Conservar URLs, códigos y nombres protegidos.

**ES-T16/T17/X03/X04:** Conservar la mínima unidad semántica de cifra y símbolo, por ejemplo `35 %` o `24 °C`, cuando lo pida la política editorial adoptada; no imponer este formato a una salida Intl con otro contrato. Registrar U+0020, U+00A0 y U+202F tal como aparecen. La muestra ilustra una agrupación, no autoriza su sustitución. Medir con el CSS o exportación reales: ni un espacio inseparable garantiza ausencia de desbordamiento ni un gran `nowrap` conserva una buena lectura. Separar valor almacenado, moneda, precisión y presentación; no reducir cifras, condiciones o texto autorizado para ajustar el ancho.

**ES-X01/X02/T01/T25:** El nombre de una familia o su anuncio de idiomas no acredita cobertura. Inspeccionar archivo suministrado, versión, licencia, cmap, subset y CSS `unicode-range`; distinguir prueba, edición comercial y versión publicada. Observar pesos, cursivas y ejes utilizados con ÁÉÍÓÚÜÑ áéíóúüñ ¿¡ ºª°, marcas combinantes, recorte, sustitución y fallback. Comprobar además nombres e idiomas que realmente aparecen: el repertorio español no certifica todas las lenguas de un mercado. Conservar por separado evidencia de metadatos y de glifos dibujados. Sin el archivo o sin renderer, dejar la parte correspondiente como `not-checked`.

## Expresión, lectura y fuentes contradictorias / Roles and conflicting sources

**ES-DQ02/DQ06/X02/X03:** El uso de letras expresivas o históricas puede explicar una identidad; no prueba una preferencia nacional ni una mejora de legibilidad o conversión. Un ejemplo histórico de MetLife México de 2021 reserva su tratamiento con sombra a grandes titulares y excluye cuerpo, botones y otros UI. Su condición de tamaño pertenece a ese tratamiento, marca y edición; no es el tamaño mínimo de un titular mexicano. No copiar anuncios ni gráficos de terceros como propuesta propia. En packaging, vídeo o diapositivas comprobar tamaño físico, duración y distancia reales; una tarjeta estática no demuestra lectura en movimiento.

**ES-DQ04/DQ05/DQ06:** Registrar publicación, recuperación, edición, página o sección, rol, medio, unidad y alcance de cada especificación. No convertir texto extraído en saltos de pantalla, ni una especificación en estilo computado. La inspección de una imagen acredita sólo esa imagen y esa escala; una afirmación del autor sobre resultados no es validación independiente. Separar `source-text`, `specification`, `image-observation`, `rendered-measurement` y `editorial-proposal` en la evidencia.

Si una tabla y una muestra discrepan, conservar ambas y marcar `needs-review` (conflicto de fuente pendiente de decisión editorial); no elegir silenciosamente. Ejemplos documentados: GOV.CO UI Kit v6.1 muestra Body1 16/22px y 16/24px; Gob.pe incluye 18px y 1.25rem que no se igualan bajo una raíz supuesta de 16px; un ejemplo impreso de Chile presenta tracking 10–20 sin unidad declarada. No adivinar raíz CSS ni convertir tracking sin unidad a px o em. Confirmar con el responsable cuál edición y medio gobiernan; continuar otras comprobaciones independientes. Una guía más reciente no sustituye automáticamente todas las anteriores en todos los medios.

## Evidencia de accesibilidad y salida / Accessibility and output evidence

**ES-X04/X05/X06/T25:** En Web/UI observar reflujo a 320 CSS px, ampliación de texto al 200% y ajustes de espaciado (interlineado 1.5, párrafos 2em, letras .12em y palabras .16em). Son condiciones de prueba de adaptación, no recomendaciones de diseño por país. Comprobar pérdida de información y acciones, etiquetas largas, orden de lectura, foco y mezcla inglés/español con idioma por fragmento. No ocultar overflow ni encerrar información esencial sólo en imagen; proporcionar alternativas pertinentes. Estas comprobaciones acotadas no certifican por sí mismas toda WCAG.

En documentos y slides revisar el archivo exportado en la aplicación destino: paginación, extracción/búsqueda/copia, acentos, ordinales, espacios inseparables, fuentes y orden de lectura. Registrar aplicación, versión, archivo y tamaño observados. Intl en Node, JSON válido, una captura o PDF parseable no prueban importación nativa, Office, lector de pantalla ni todos los navegadores. Cada comprobación conserva su estado `passed`, `failed`, `needs-review`, `not-checked`, `unsupported`, `waived` o `not-applicable`; sólo una afirmación ejecutada puede ser `passed`. Una observación en un entorno no se extiende a otro sin evidencia.

## Referencias públicas / Public references

Consultadas en la investigación del 22-10-2026; estas referencias no implican una nueva visita ni pruebas nativas del proyecto. Las guías de marca y los ejemplos históricos se usan dentro de su edición y alcance, sin redistribuir gráficos ni originales.

- RAE/ASALE, [signos de interrogación y exclamación](https://www.rae.es/dpd/signos%20de%20interrogaci%C3%B3n%20y%20exclamaci%C3%B3n), [tilde en las mayúsculas](https://www.rae.es/espanol-al-dia/tilde-en-las-mayusculas) y [guion](https://www.rae.es/dpd/guion).
- W3C, [CSS Text: Hyphenation](https://www.w3.org/TR/css-text-3/#hyphenation), [WCAG Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) y [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
- MetLife, [Mexico Typography](https://design.metlife.com/foundations/standards/typography/mexico/), caso histórico de 2021; comprobar la edición aplicable antes de usarla en un proyecto actual.
- GOV.CO, [UI Kit v6.1](https://beta.www.gov.co/uploads/KIT_UI_V6_1.pdf), 26-11-2020, p. física 13; [Gob.pe Tipografía](https://guias.servicios.gob.pe/creacion-servicios-digitales/estilos/tipografia); Gobierno de Chile, [Manual Comunicación Visual 2025](https://kitdigital.gob.cl/archivos/insumos/2025/Manual-Comunicacio%CC%81n-Visual-2025_vf.pdf), ejemplo de libro de 2023. Son especificaciones institucionales, no valores nacionales universales.
