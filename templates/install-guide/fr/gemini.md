Voici comment utiliser {{brand}} avec Gemini CLI et l’application Gemini.

> **À propos de la v{{version}}**
> Cette version vous permet d’essayer l’installation dans votre propre environnement. Son fonctionnement dans chaque outil n’a pas encore été suffisamment vérifié : il se peut que certaines étapes ne fonctionnent pas comme prévu.

## 1. Choisir une méthode d’installation

| Où l’utiliser | Méthode recommandée |
| --- | --- |
| Gemini CLI (les quatre ensemble) | [A. Installer comme extension](#a) |
| Gemini CLI (seulement ceux dont vous avez besoin) | [B. Choisir et installer des skills](#b) |
| Application Gemini (web, Mac, smartphone) | [C. Envoyer les skills](#c) |

## A. Gemini CLI : installer comme extension

Cette méthode installe les quatre skills en une seule fois.

1. Téléchargez le [ZIP de l’extension]({{plugin_url}}).
{{#if plugin_folder}}
2. Décompressez le ZIP : vous obtenez un dossier `{{plugin_folder}}`.
{{else}}
2. Créez un dossier `{{plugin}}` vide et décompressez le ZIP à l’intérieur.
{{/if}}
3. Installez l’extension en indiquant ce dossier.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Si un écran de confirmation s’affiche, vérifiez son contenu avant de continuer. Une fois installée, l’extension est active dans tous les projets.

Une extension installée depuis un ZIP ne se met pas à jour automatiquement. Lorsqu’une nouvelle version sort, remplacez-la par le nouveau ZIP.

## B. Gemini CLI : choisir et installer des skills

Cette méthode installe uniquement les skills dont vous avez besoin, projet par projet. Si vous avez suivi la méthode A, cette étape est inutile.

Par exemple, pour installer `{{first}}`, exécutez la commande suivante dans le projet concerné :

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Pour installer un autre skill, modifiez `--path` comme suit :

{{gemini_paths}}

`--scope workspace` limite l’utilisation à « ce projet uniquement ». Sans cette option, le skill est disponible dans tous vos projets.

**Pour mettre à jour**

Exécutez de nouveau la même commande. Le skill installé est remplacé : si vous l’avez modifié vous-même, enregistrez d’abord vos changements.

## C. Application Gemini : envoyer les skills

1. Téléchargez les ZIP des skills que vous voulez utiliser.
{{skills_list_indented}}
2. Dans Gemini, ouvrez **Customize** (ou **More** si vous ne le voyez pas) → **Skills** → **Upload**.
3. Choisissez les ZIP un par un, vérifiez les informations et appuyez sur **Create**.

**Attention**

- Cette fonction est réservée aux comptes Google personnels de personnes âgées de 18 ans ou plus. Les comptes professionnels et scolaires ne sont pas pris en charge pour le moment.
- L’option « Keep Activity » (enregistrement de l’activité) doit être activée.
- La fonction est déployée progressivement et peut ne pas encore s’afficher. Pour en savoir plus, consultez l’[aide officielle de Gemini](https://support.google.com/gemini/answer/17094296?hl=fr).
- Le ZIP de l’extension (pour Gemini CLI) ne fonctionne pas ici.
- Les skills envoyés ne se mettent pas à jour automatiquement. Lorsqu’une nouvelle version sort, envoyez-les à nouveau.

## 2. Essayer

Pour commencer, nous vous conseillons une demande qui ne modifie aucun fichier.

> Je prévois de préparer une présentation en français. À quoi dois-je faire attention ? Ne modifie aucun fichier.

## Vérifier les fichiers (facultatif)

Pour vous assurer que les fichiers téléchargés ne sont pas endommagés, utilisez [SHA256SUMS.txt]({{sums}}).

Placez SHA256SUMS.txt dans le même dossier que les fichiers ZIP téléchargés, puis exécutez la commande suivante dans un terminal. Si `shasum` n’est pas disponible, comparez l’empreinte SHA-256 avec un outil équivalent, par exemple `Get-FileHash` dans Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Si `OK` s’affiche sur les lignes des fichiers téléchargés, tout est en ordre.

---

Autres outils : [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Les écrans et les conditions d’accès peuvent changer. Pour les informations les plus récentes, consultez la documentation officielle de chaque service (dernière vérification de cette page : 14 octobre 2026).
