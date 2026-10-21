Lo mhlahlandlela uchaza indlela yokusebenzisa i-{{brand}} ku-Claude Code nakwingxoxo ye-Claude.

> **Mayelana ne-v{{version}}**
> Lolu hlobo lwenzelwe ukuthi uzame ukufaka ohlelweni lwakho. Ukusebenza kulo lonke ithuluzi akukaqinisekiswa ngokugcwele, ngakho ezinye izinyathelo zingase zingasebenzi njengoba kulindelekile.

## 1. Khetha indlela yokufaka

| Lapho ufuna ukuyisebenzisa khona | Indlela enconyiwe |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Faka kusuka ku-GitHub](#a) (kulula ukubuyekeza) |
{{/if}}
| Claude Code (uma ufuna ukufaka kusuka ku-ZIP) | [{{L_zip}}. Faka kusuka ku-ZIP](#{{l_zip}}) |
| Ingxoxo ye-Claude (claude.ai nama-app) | [{{L_chat}}. Layisha ama-skill](#{{l_chat}}) |

I-Claude Code nengxoxo ye-Claude zinezindlela ezahlukene zokufaka.

{{#if marketplace}}
## A. Claude Code: faka kusuka ku-GitHub

1. Ku-terminal, bhalisa umthombo wokusabalalisa we-KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Engxoxweni ye-Claude Code, faka lokhu okulandelayo:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Hlola imininingwane, khetha ububanzi bokusetshenziswa (wena wedwa, le phrojekthi kuphela, njalo njalo), bese uyafaka.

Uma isifakiwe, le miyalo elandelayo izotholakala:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: faka kusuka ku-ZIP

1. Landa [ifayela le-ZIP le-plugin ye-Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Uma ukhipha ifayela le-ZIP, uzothola ifolda ethi `{{plugin_folder}}`.
{{else}}
2. Dala ifolda engenalutho ethi `{{plugin}}`, bese ukhiphela ifayela le-ZIP ngaphakathi kwayo.
{{/if}}
3. Qalisa i-Claude Code ucacise leyo folda.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Qaphela**

- Sebenzisa okuqukethwe kufolda njengoba kunjalo. Ungasusi amafayela noma uxube amanye amafayela kuyo.
- Le ndlela ayibuyekezi ngokuzenzakalelayo. Uma kukhishwa uhlobo olusha, shintsha ufake ifayela le-ZIP elisha.

## {{L_chat}}. Ingxoxo ye-Claude: layisha ama-skill

Le ndlela eyokusebenzisa ku-claude.ai nakuma-app e-Claude.

1. Landa amafayela e-ZIP ama-skill ofuna ukuwasebenzisa.
{{skills_list_indented}}
2. Ku-Claude, vula **Customize → Skills**, bese ukhetha **Upload a skill** enkinobheni yokwengeza.
3. Layisha amafayela e-ZIP elilodwa ngelilodwa, bese uvula i-skill ngayinye.

**Qaphela**

- Ifayela le-ZIP le-plugin ye-Claude Code alisebenzi lapha. Sebenzisa amafayela e-ZIP ama-skill.
- Layisha amafayela e-ZIP ngaphandle kokushintsha amagama awo.
- Ukuze usebenzise ama-skill, “ukusebenzisa ikhodi” (code execution) kufanele kuvulwe ezilungiselelweni. Ukuze uthole imininingwane, bona [umhlahlandlela osemthethweni we-Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Kuma-akhawunti ezinhlangano, kungenzeka kungatholakali kuye ngezilungiselelo zomphathi.
- Ama-skill alayishiwe awabuyekezwa ngokuzenzakalelayo. Uma kukhishwa uhlobo olusha, phinda uwalayishe.

## 2. Zama

Sincoma ukuthi uqale ngesicelo esingashintshi noma yiliphi ifayela.

> Ngihlela ukwenza ikhasi lewebhu ngesiZulu. Yini okufanele ngiyiqaphele? Sicela ungashintshi noma yiliphi ifayela.

## Qinisekisa ukuthi amafayela alungile (akuphoqelekile)

Uma ufuna ukuhlola ukuthi amafayela owalandile awonakalanga, sebenzisa i-[SHA256SUMS.txt]({{sums}}).

Beka i-SHA256SUMS.txt kufolda efanayo namafayela e-ZIP owalandile, bese usebenzisa lo myalo ku-terminal. Uma i-`shasum` ingatholakali, qhathanisa i-SHA-256 ngomunye umyalo ofana ne-`Get-FileHash` ye-Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Uma imigqa yamafayela owalandile ibonisa `OK`, ayikho inkinga.

---

Amanye amathuluzi: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Izikrini nemibandela yokutholakala kungashintsha. Sicela uhlole umhlahlandlela osemthethweni wesevisi ngayinye ukuze uthole ulwazi lwakamuva (leli khasi lagcina ukuhlolwa ngomhla ziyi-14 kuOkthoba 2026).
