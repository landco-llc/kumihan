Estos son los pasos para usar {{brand}} con ChatGPT y Codex.

> **Acerca de la v{{version}}**
> Esta versión es para que pruebes la instalación en tu propio entorno. Su funcionamiento en cada herramienta aún no se ha comprobado lo suficiente, por lo que es posible que algo no funcione como se espera.

## 1. Elige un método de instalación

| Dónde quieres usarlo | Método recomendado |
| --- | --- |
| ChatGPT (si puedes subir skills) | [A. Añadir las skills una por una](#a) |
| ChatGPT (si quieres registrarlo como tu plugin personal) | [B. Registrar todo como plugin](#b) |
| Codex (en tu ordenador) | [C. Copiar las carpetas](#c) |

Una **skill** equivale a una función; el **plugin** es un paquete que reúne las cuatro skills.

## 2. Descarga los archivos

Los archivos están en la [página de la versión]({{release}}). Al pulsar un enlace se descarga el archivo ZIP.

**Plugin (las cuatro skills juntas)**

- {{plugin_link}}

**Skills (una por una)**

{{skills_list}}

## A. Añadir skills a ChatGPT

Este método sirve si en la pantalla de ChatGPT aparece «Skills» con una opción para subir archivos.

1. Elige un archivo ZIP de una skill y súbelo.
2. Revisa la información que se muestra y añádela.
3. Repite los mismos pasos con cada skill que necesites.

**Ten en cuenta**

- El ZIP del plugin no sirve para este método. Usa los ZIP de las skills.
- Adjuntar un archivo a una conversación no lo añade como skill.
- Si no ves la opción, es posible que todavía no esté disponible en tu plan o en tu aplicación. Consulta la [guía oficial de OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Registrar un plugin en ChatGPT

Con este método, las cuatro skills se registran juntas como tu plugin personal.

1. Abre una conversación nueva en ChatGPT y selecciona `@plugin-creator`.
2. Adjunta el archivo ZIP del plugin.
3. Pídelo de esta forma:

   > Registra este paquete como mi plugin privado. No lo envíes al directorio público.

4. Cuando se haya registrado, **{{display}}** aparecerá en Plugins, dentro de «Personal» o «Created by me».
5. Instálalo si hace falta y actívalo en una conversación nueva.

**Ten en cuenta**

- Es posible que se registre en el espacio de trabajo de tu equipo. Si quieres que sea solo para ti, comprueba el destino antes de registrarlo.
- Según tu plan o la configuración del espacio de trabajo, puede que esta función no esté disponible. Para más información, consulta [Build plugins](https://learn.chatgpt.com/docs/build-plugins) y [Plugins](https://learn.chatgpt.com/docs/plugins).
- Un plugin registrado de esta forma solo puede usarse con tu cuenta. No aparece en el directorio público.

## C. Copiar las carpetas a Codex

Al extraer el ZIP de una skill obtienes una carpeta como `{{first}}`. Copia esa carpeta en la ubicación que lee Codex.

| Alcance | Destino |
| --- | --- |
| Solo un proyecto concreto | `.agents/skills/` dentro del proyecto |
| Todos los proyectos | `~/.agents/skills/` en tu carpeta personal |

Por ejemplo, para añadir `{{first}}` a un proyecto:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Ten en cuenta**

- Copia la carpeta entera, con todo su contenido. Con solo algunos archivos no funcionará correctamente.
- Si ya existe una carpeta con el mismo nombre, revisa su contenido antes de sobrescribirla.

## 3. Pruébalo

Una vez instalado, abre una conversación nueva y llama a la skill.

| Herramienta | Cómo llamarla |
| --- | --- |
| ChatGPT | Elígela desde `@` |
| Codex | Elígela desde `$` o `/skills` |

Para empezar, te recomendamos una petición que no modifique ningún archivo.

> Voy a preparar un informe en español. ¿Qué aspectos debo tener en cuenta? No modifiques ningún archivo.

## Comprueba que los archivos son correctos (opcional)

Si quieres comprobar que los archivos descargados no están dañados, usa [SHA256SUMS.txt]({{sums}}).

Coloca SHA256SUMS.txt en la misma carpeta que los archivos ZIP descargados y ejecuta el siguiente comando en un terminal. Si tu entorno no tiene `shasum`, verifica el SHA-256 con otra herramienta, como `Get-FileHash` de Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Si en las líneas de los archivos descargados aparece `OK`, todo está en orden.

---

Otras herramientas: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Las pantallas y las condiciones del servicio pueden cambiar. Consulta la información oficial de cada servicio para obtener los datos más recientes (fecha de revisión de esta página: 14 de octubre de 2026).
