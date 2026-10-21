Voici comment utiliser {{brand}} avec Claude Code et le chat Claude.

> **À propos de la v{{version}}**
> Cette version vous permet d’essayer l’installation dans votre propre environnement. Son fonctionnement dans chaque outil n’a pas encore été suffisamment vérifié : il se peut que certaines étapes ne fonctionnent pas comme prévu.

## 1. Choisir une méthode d’installation

| Où l’utiliser | Méthode recommandée |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Installer depuis GitHub](#a) (mises à jour faciles) |
{{/if}}
| Claude Code (installation depuis un ZIP) | [{{L_zip}}. Installer depuis un ZIP](#{{l_zip}}) |
| Chat Claude (claude.ai et applications) | [{{L_chat}}. Envoyer les skills](#{{l_chat}}) |

Claude Code et le chat Claude ne s’installent pas de la même manière.

{{#if marketplace}}
## A. Claude Code : installer depuis GitHub

1. Dans un terminal, ajoutez la source de distribution de KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Dans une conversation Claude Code, saisissez :

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Vérifiez les informations, choisissez la portée (vous seul, ce projet uniquement, etc.) et lancez l’installation.

Une fois l’installation terminée, les commandes suivantes sont disponibles.

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code : installer depuis un ZIP

1. Téléchargez le [ZIP du plugin pour Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Décompressez le ZIP : vous obtenez un dossier `{{plugin_folder}}`.
{{else}}
2. Créez un dossier `{{plugin}}` vide et décompressez le ZIP à l’intérieur.
{{/if}}
3. Lancez Claude Code en indiquant ce dossier.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Attention**

- Utilisez le contenu du dossier tel quel. Ne supprimez aucun fichier et n’en ajoutez pas d’autres.
- Cette méthode ne se met pas à jour automatiquement. Lorsqu’une nouvelle version sort, remplacez le dossier par le nouveau ZIP.

## {{L_chat}}. Chat Claude : envoyer les skills

Cette méthode s’applique à claude.ai et aux applications Claude.

1. Téléchargez les ZIP des skills que vous voulez utiliser.
{{skills_list_indented}}
2. Dans Claude, ouvrez **Customize → Skills**, puis choisissez **Upload a skill** depuis le bouton d’ajout.
3. Envoyez les ZIP un par un et activez chaque skill.

**Attention**

- Le ZIP du plugin pour Claude Code ne fonctionne pas ici. Utilisez les ZIP des skills.
- Envoyez les ZIP sans modifier leur nom de fichier.
- Pour utiliser les skills, l’exécution de code doit être activée dans les paramètres. Pour en savoir plus, consultez le [guide officiel de Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Sur un compte d’organisation, cette fonction peut être indisponible selon les paramètres de l’administrateur.
- Les skills envoyés ne se mettent pas à jour automatiquement. Lorsqu’une nouvelle version sort, envoyez-les à nouveau.

## 2. Essayer

Pour commencer, nous vous conseillons une demande qui ne modifie aucun fichier.

> Je prévois de créer une page web en français. À quoi dois-je faire attention ? Ne modifie aucun fichier.

## Vérifier les fichiers (facultatif)

Pour vous assurer que les fichiers téléchargés ne sont pas endommagés, utilisez [SHA256SUMS.txt]({{sums}}).

Placez SHA256SUMS.txt dans le même dossier que les fichiers ZIP téléchargés, puis exécutez la commande suivante dans un terminal. Si `shasum` n’est pas disponible, comparez l’empreinte SHA-256 avec un outil équivalent, par exemple `Get-FileHash` dans Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Si `OK` s’affiche sur les lignes des fichiers téléchargés, tout est en ordre.

---

Autres outils : [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Les écrans et les conditions d’accès peuvent changer. Pour les informations les plus récentes, consultez la documentation officielle de chaque service (dernière vérification de cette page : 14 octobre 2026).
