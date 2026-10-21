Estos son los pasos para usar {{brand}} con Claude Code y el chat de Claude.

> **Acerca de la v{{version}}**
> Esta versión es para que pruebes la instalación en tu propio entorno. Su funcionamiento en cada herramienta aún no se ha comprobado lo suficiente, por lo que es posible que algo no funcione como se espera.

## 1. Elige un método de instalación

| Dónde quieres usarlo | Método recomendado |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Instalar desde GitHub](#a) (fácil de actualizar) |
{{/if}}
| Claude Code (si prefieres instalarlo desde un ZIP) | [{{L_zip}}. Instalar desde un ZIP](#{{l_zip}}) |
| Chat de Claude (claude.ai y apps) | [{{L_chat}}. Subir las skills](#{{l_chat}}) |

Claude Code y el chat de Claude se instalan de forma distinta.

{{#if marketplace}}
## A. Claude Code: instalar desde GitHub

1. En un terminal, registra la fuente de distribución de KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. En una conversación de Claude Code, escribe lo siguiente:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Revisa la información, elige el alcance (solo para ti, solo para este proyecto, etc.) e instálalo.

Una vez instalado, podrás usar los siguientes comandos.

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: instalar desde un ZIP

1. Descarga el [ZIP del plugin para Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Al extraer el ZIP se crea la carpeta `{{plugin_folder}}`.
{{else}}
2. Crea una carpeta `{{plugin}}` vacía y extrae el ZIP dentro de ella.
{{/if}}
3. Inicia Claude Code indicando esa carpeta.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Ten en cuenta**

- Usa el contenido de la carpeta tal como está. No elimines archivos ni añadas otros.
- Con este método no hay actualizaciones automáticas. Cuando salga una versión nueva, sustitúyela por el nuevo ZIP.

## {{L_chat}}. Chat de Claude: subir las skills

Este método es para claude.ai y las apps de Claude.

1. Descarga los ZIP de las skills que quieras usar.
{{skills_list_indented}}
2. En Claude, abre **Customize → Skills** y elige **Upload a skill** con el botón de añadir.
3. Sube los ZIP uno por uno y activa cada skill.

**Ten en cuenta**

- El ZIP del plugin para Claude Code no sirve aquí. Usa los ZIP de las skills.
- Sube los ZIP sin cambiarles el nombre.
- Para usar skills, la ejecución de código debe estar activada en la configuración. Para más información, consulta la [guía oficial de Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- En las cuentas de organización, puede que no esté disponible según la configuración del administrador.
- Las skills subidas no se actualizan automáticamente. Cuando salga una versión nueva, vuelve a subirlas.

## 2. Pruébalo

Para empezar, te recomendamos una petición que no modifique ningún archivo.

> Voy a crear una página web en español. ¿Qué aspectos debo tener en cuenta? No modifiques ningún archivo.

## Comprueba que los archivos son correctos (opcional)

Si quieres comprobar que los archivos descargados no están dañados, usa [SHA256SUMS.txt]({{sums}}).

Coloca SHA256SUMS.txt en la misma carpeta que los archivos ZIP descargados y ejecuta el siguiente comando en un terminal. Si tu entorno no tiene `shasum`, verifica el SHA-256 con otra herramienta, como `Get-FileHash` de Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Si en las líneas de los archivos descargados aparece `OK`, todo está en orden.

---

Otras herramientas: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Las pantallas y las condiciones del servicio pueden cambiar. Consulta la información oficial de cada servicio para obtener los datos más recientes (fecha de revisión de esta página: 14 de octubre de 2026).
