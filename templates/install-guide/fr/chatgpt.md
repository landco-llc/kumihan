Voici comment utiliser {{brand}} avec ChatGPT et Codex.

> **À propos de la v{{version}}**
> Cette version vous permet d’essayer l’installation dans votre propre environnement. Son fonctionnement dans chaque outil n’a pas encore été suffisamment vérifié : il se peut que certaines étapes ne fonctionnent pas comme prévu.

## 1. Choisir une méthode d’installation

| Où l’utiliser | Méthode recommandée |
| --- | --- |
| ChatGPT (si l’envoi de skills est disponible) | [A. Ajouter les skills un par un](#a) |
| ChatGPT (pour l’enregistrer comme votre plugin personnel) | [B. Tout enregistrer comme plugin](#b) |
| Codex (sur votre ordinateur) | [C. Copier les dossiers](#c) |

Un **skill** correspond à une seule fonction ; le **plugin** est un paquet qui regroupe les quatre skills.

## 2. Télécharger les fichiers

Les fichiers se trouvent sur la [page de la version]({{release}}). Cliquez sur un lien pour télécharger le fichier ZIP.

**Plugin (les quatre skills regroupés)**

- {{plugin_link}}

**Skills (un par un)**

{{skills_list}}

## A. Ajouter des skills à ChatGPT

Cette méthode est possible si l’écran de ChatGPT affiche « Skills » avec une option d’envoi.

1. Choisissez un fichier ZIP de skill et envoyez-le.
2. Vérifiez les informations affichées, puis ajoutez-le.
3. Répétez ces étapes pour chaque skill dont vous avez besoin.

**Attention**

- Le ZIP du plugin ne fonctionne pas avec cette méthode. Utilisez les ZIP des skills.
- Joindre un fichier à une conversation ne l’ajoute pas comme skill.
- Si l’option n’apparaît pas, elle n’est peut-être pas encore proposée pour votre abonnement ou votre application. Consultez le [guide officiel d’OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Enregistrer un plugin dans ChatGPT

Cette méthode regroupe les quatre skills et les enregistre comme votre plugin personnel.

1. Ouvrez une nouvelle conversation dans ChatGPT et sélectionnez `@plugin-creator`.
2. Joignez le fichier ZIP du plugin.
3. Formulez la demande suivante :

   > Enregistre ce paquet comme mon plugin privé. Ne le soumets pas au répertoire public.

4. Une fois l’enregistrement terminé, **{{display}}** apparaît dans Plugins, sous « Personal » ou « Created by me ».
5. Installez-le si nécessaire, puis activez-le dans une nouvelle conversation.

**Attention**

- Le plugin peut être enregistré dans l’espace de travail de votre équipe. Si vous voulez qu’il reste personnel, vérifiez la destination avant de l’enregistrer.
- Selon votre abonnement ou les paramètres de votre espace de travail, cette fonction peut ne pas être disponible. Pour en savoir plus, consultez [Build plugins](https://learn.chatgpt.com/docs/build-plugins) et [Plugins](https://learn.chatgpt.com/docs/plugins).
- Un plugin enregistré ainsi n’est utilisable que par votre compte. Il n’est pas publié dans le répertoire public.

## C. Copier les dossiers dans Codex

Une fois le ZIP d’un skill décompressé, vous obtenez un dossier tel que `{{first}}`. Copiez ce dossier à l’emplacement que Codex lit.

| Portée | Destination |
| --- | --- |
| Un seul projet | `.agents/skills/` dans le projet |
| Tous les projets | `~/.agents/skills/` dans votre dossier personnel |

Par exemple, pour ajouter `{{first}}` à un projet :

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Attention**

- Copiez le dossier entier, avec tout son contenu. Avec seulement une partie des fichiers, le skill ne fonctionnera pas correctement.
- Si un dossier du même nom existe déjà, vérifiez son contenu avant de l’écraser.

## 3. Essayer

Une fois l’installation terminée, ouvrez une nouvelle conversation et appelez un skill.

| Outil | Comment l’appeler |
| --- | --- |
| ChatGPT | Choisissez-le depuis `@` |
| Codex | Choisissez-le depuis `$` ou `/skills` |

Pour commencer, nous vous conseillons une demande qui ne modifie aucun fichier.

> Je prévois de rédiger un rapport en français. À quoi dois-je faire attention ? Ne modifie aucun fichier.

## Vérifier les fichiers (facultatif)

Pour vous assurer que les fichiers téléchargés ne sont pas endommagés, utilisez [SHA256SUMS.txt]({{sums}}).

Placez SHA256SUMS.txt dans le même dossier que les fichiers ZIP téléchargés, puis exécutez la commande suivante dans un terminal. Si `shasum` n’est pas disponible, comparez l’empreinte SHA-256 avec un outil équivalent, par exemple `Get-FileHash` dans Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Si `OK` s’affiche sur les lignes des fichiers téléchargés, tout est en ordre.

---

Autres outils : [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Les écrans et les conditions d’accès peuvent changer. Pour les informations les plus récentes, consultez la documentation officielle de chaque service (dernière vérification de cette page : 14 octobre 2026).
