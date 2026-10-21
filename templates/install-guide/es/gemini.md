Estos son los pasos para usar {{brand}} con Gemini CLI y la app de Gemini.

> **Acerca de la v{{version}}**
> Esta versión es para que pruebes la instalación en tu propio entorno. Su funcionamiento en cada herramienta aún no se ha comprobado lo suficiente, por lo que es posible que algo no funcione como se espera.

## 1. Elige un método de instalación

| Dónde quieres usarlo | Método recomendado |
| --- | --- |
| Gemini CLI (las cuatro juntas) | [A. Instalar como extensión](#a) |
| Gemini CLI (solo las que necesites) | [B. Elegir e instalar skills](#b) |
| App de Gemini (web, Mac, smartphone) | [C. Subir las skills](#c) |

## A. Gemini CLI: instalar como extensión

Con este método se instalan las cuatro skills a la vez.

1. Descarga el [ZIP de la extensión]({{plugin_url}}).
{{#if plugin_folder}}
2. Al extraer el ZIP se crea la carpeta `{{plugin_folder}}`.
{{else}}
2. Crea una carpeta `{{plugin}}` vacía y extrae el ZIP dentro de ella.
{{/if}}
3. Instálala indicando esa carpeta.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Si aparece una pantalla de confirmación, revisa su contenido antes de continuar. Una vez instalada, la extensión queda activa en todos los proyectos.

Si la instalaste desde un ZIP, no se actualiza automáticamente. Cuando salga una versión nueva, sustitúyela por el nuevo ZIP.

## B. Gemini CLI: elegir e instalar skills

Con este método instalas solo las skills que necesitas, proyecto por proyecto. Si usaste el método A, no hace falta este paso.

Por ejemplo, para instalar `{{first}}`, ejecuta lo siguiente en el proyecto correspondiente:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Para instalar otras skills, cambia `--path` de esta forma:

{{gemini_paths}}

`--scope workspace` limita el uso a «solo este proyecto». Si lo omites, la skill estará disponible en todos tus proyectos.

**Para actualizar**

Vuelve a ejecutar el mismo comando. La skill instalada se sustituye, así que, si la has modificado, guarda antes tus cambios.

## C. App de Gemini: subir las skills

1. Descarga los ZIP de las skills que quieras usar.
{{skills_list_indented}}
2. En Gemini, abre **Customize** (o **More** si no lo ves) → **Skills** → **Upload**.
3. Elige los ZIP uno por uno, revisa la información y pulsa **Create**.

**Ten en cuenta**

- Solo pueden usarlo las cuentas personales de Google de personas mayores de 18 años. Por ahora no funciona con cuentas de trabajo ni de centros educativos.
- Debes tener activada la opción «Keep Activity» (guardar actividad).
- La función se está ofreciendo de forma gradual, así que es posible que todavía no te aparezca. Para más información, consulta la [ayuda oficial de Gemini](https://support.google.com/gemini/answer/17094296?hl=es).
- El ZIP de la extensión (para Gemini CLI) no sirve aquí.
- Las skills subidas no se actualizan automáticamente. Cuando salga una versión nueva, vuelve a subirlas.

## 2. Pruébalo

Para empezar, te recomendamos una petición que no modifique ningún archivo.

> Voy a preparar una presentación en español. ¿Qué aspectos debo tener en cuenta? No modifiques ningún archivo.

## Comprueba que los archivos son correctos (opcional)

Si quieres comprobar que los archivos descargados no están dañados, usa [SHA256SUMS.txt]({{sums}}).

Coloca SHA256SUMS.txt en la misma carpeta que los archivos ZIP descargados y ejecuta el siguiente comando en un terminal. Si tu entorno no tiene `shasum`, verifica el SHA-256 con otra herramienta, como `Get-FileHash` de Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Si en las líneas de los archivos descargados aparece `OK`, todo está en orden.

---

Otras herramientas: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Las pantallas y las condiciones del servicio pueden cambiar. Consulta la información oficial de cada servicio para obtener los datos más recientes (fecha de revisión de esta página: 14 de octubre de 2026).
