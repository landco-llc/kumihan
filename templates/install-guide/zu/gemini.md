Lo mhlahlandlela uchaza indlela yokusebenzisa i-{{brand}} ku-Gemini CLI naku-app ye-Gemini.

> **Mayelana ne-v{{version}}**
> Lolu hlobo lwenzelwe ukuthi uzame ukufaka ohlelweni lwakho. Ukusebenza kulo lonke ithuluzi akukaqinisekiswa ngokugcwele, ngakho ezinye izinyathelo zingase zingasebenzi njengoba kulindelekile.

## 1. Khetha indlela yokufaka

| Lapho ufuna ukuyisebenzisa khona | Indlela enconyiwe |
| --- | --- |
| Gemini CLI (womane ndawonye) | [A. Faka njengesandiso](#a) |
| Gemini CLI (lawo owadingayo kuphela) | [B. Khetha bese ufaka ama-skill](#b) |
| I-app ye-Gemini (iwebhu, i-Mac, ifoni ehlakaniphile) | [C. Layisha ama-skill](#c) |

## A. Gemini CLI: faka njengesandiso

Le ndlela ifaka wonke ama-skill amane ndawonye.

1. Landa [ifayela le-ZIP lesandiso]({{plugin_url}}).
{{#if plugin_folder}}
2. Uma ukhipha ifayela le-ZIP, uzothola ifolda ethi `{{plugin_folder}}`.
{{else}}
2. Dala ifolda engenalutho ethi `{{plugin}}`, bese ukhiphela ifayela le-ZIP ngaphakathi kwayo.
{{/if}}
3. Faka ucacise leyo folda.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Uma kuvela isikrini sokuqinisekisa, hlola imininingwane ngaphambi kokuqhubeka. Uma sesifakiwe, isandiso sisebenza kuwo wonke amaphrojekthi.

Uma usifake kusuka ku-ZIP, ngeke sibuyekezwe ngokuzenzakalelayo. Uma kukhishwa uhlobo olusha, shintsha ufake ifayela le-ZIP elisha.

## B. Gemini CLI: khetha bese ufaka ama-skill

Le ndlela ifaka kuphela ama-skill owadingayo, ngephrojekthi ngayinye. Uma usufake ngendlela A, awudingi lesi sinyathelo.

Isibonelo, ukuze ufake i-`{{first}}`, sebenzisa lo myalo kuphrojekthi ofuna ukuyifaka kuyo:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Ukuze ufake amanye ama-skill, shintsha i-`--path` kanje:

{{gemini_paths}}

I-`--scope workspace` iyisilungiselelo sokusebenzisa “kule phrojekthi kuphela”. Uma uyishiya, i-skill izotholakala kuwo wonke amaphrojekthi akho.

**Ukubuyekeza**

Phinda usebenzise umyalo ofanayo. I-skill efakiwe izoshintshwa, ngakho uma wenze izinguquko zakho, zigcine kuqala.

## C. I-app ye-Gemini: layisha ama-skill

1. Landa amafayela e-ZIP ama-skill ofuna ukuwasebenzisa.
{{skills_list_indented}}
2. Ku-Gemini, vula **Customize** (noma **More** uma ungayiboni) → **Skills** → **Upload**.
3. Khetha ifayela le-ZIP elilodwa ngesikhathi, hlola imininingwane, bese uchofoza **Create**.

**Qaphela**

- Itholakala kuma-akhawunti e-Google omuntu siqu abantu abaneminyaka eyi-18 nangaphezulu. Ama-akhawunti omsebenzi nawesikole awasekelwa okwamanje.
- I-“Keep Activity (Gcina Umsebenzi)” kufanele ivulwe.
- Lesi sici sikhishwa kancane kancane, ngakho kungenzeka singakaveli kuwe. Ukuze uthole imininingwane, bona [usizo olusemthethweni lwe-Gemini](https://support.google.com/gemini/answer/17094296?hl=zu).
- Ifayela le-ZIP lesandiso (le-Gemini CLI) alisebenzi lapha.
- Ama-skill alayishiwe awabuyekezwa ngokuzenzakalelayo. Uma kukhishwa uhlobo olusha, phinda uwalayishe.

## 2. Zama

Sincoma ukuthi uqale ngesicelo esingashintshi noma yiliphi ifayela.

> Ngihlela ukwenza amaslayidi okwethula ngesiZulu. Yini okufanele ngiyiqaphele? Sicela ungashintshi noma yiliphi ifayela.

## Qinisekisa ukuthi amafayela alungile (akuphoqelekile)

Uma ufuna ukuhlola ukuthi amafayela owalandile awonakalanga, sebenzisa i-[SHA256SUMS.txt]({{sums}}).

Beka i-SHA256SUMS.txt kufolda efanayo namafayela e-ZIP owalandile, bese usebenzisa lo myalo ku-terminal. Uma i-`shasum` ingatholakali, qhathanisa i-SHA-256 ngomunye umyalo ofana ne-`Get-FileHash` ye-Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Uma imigqa yamafayela owalandile ibonisa `OK`, ayikho inkinga.

---

Amanye amathuluzi: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Izikrini nemibandela yokutholakala kungashintsha. Sicela uhlole umhlahlandlela osemthethweni wesevisi ngayinye ukuze uthole ulwazi lwakamuva (leli khasi lagcina ukuhlolwa ngomhla ziyi-14 kuOkthoba 2026).
