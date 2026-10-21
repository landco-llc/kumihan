Lo mhlahlandlela uchaza indlela yokusebenzisa i-{{brand}} ku-ChatGPT naku-Codex.

> **Mayelana ne-v{{version}}**
> Lolu hlobo lwenzelwe ukuthi uzame ukufaka ohlelweni lwakho. Ukusebenza kulo lonke ithuluzi akukaqinisekiswa ngokugcwele, ngakho ezinye izinyathelo zingase zingasebenzi njengoba kulindelekile.

## 1. Khetha indlela yokufaka

| Lapho ufuna ukuyisebenzisa khona | Indlela enconyiwe |
| --- | --- |
| ChatGPT (uma ungakwazi ukulayisha ama-skill) | [A. Engeza ama-skill elilodwa ngelilodwa](#a) |
| ChatGPT (uma ufuna ukuyibhalisa njenge-plugin yakho yangasese) | [B. Bhalisa wonke ndawonye njenge-plugin](#b) |
| Codex (kukhompyutha yakho) | [C. Kopisha amafolda](#c) |

I-**skill** iwumsebenzi owodwa, kanti i-**plugin** iyiphakheji ehlanganisa wonke ama-skill amane.

## 2. Landa amafayela

Amafayela atholakala [ekhasini lokukhishwa]({{release}}). Uma uchofoza isixhumanisi, ifayela le-ZIP lizolandwa.

**I-plugin (ama-skill amane ahlanganisiwe)**

- {{plugin_link}}

**Ama-skill (elilodwa ngelilodwa)**

{{skills_list}}

## A. Engeza ama-skill ku-ChatGPT

Sebenzisa le ndlela uma isikrini sakho se-ChatGPT sine-**Skills** kanye nenketho yokulayisha.

1. Khetha ifayela le-ZIP le-skill elilodwa bese ulilayisha.
2. Hlola imininingwane eboniswayo, bese uyengeza.
3. Phinda lezi zinyathelo ku-skill ngasinye osidingayo.

**Qaphela**

- Ifayela le-ZIP le-plugin alisebenzi ngale ndlela. Sebenzisa amafayela e-ZIP ama-skill.
- Ukunamathisela ifayela engxoxweni kuphela akuyengezi njenge-skill.
- Uma ungayiboni inketho, kungenzeka ukuthi ayikatholakali ohlelweni lokubhaliselwa noma ku-app oyisebenzisayo. Bona [umhlahlandlela osemthethweni we-OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Bhalisa njenge-plugin ku-ChatGPT

Le ndlela ihlanganisa wonke ama-skill amane futhi iwabhalise njenge-plugin yakho yangasese.

1. Vula ingxoxo entsha ku-ChatGPT bese ukhetha `@plugin-creator`.
2. Namathisela ifayela le-ZIP le-plugin.
3. Cela kanje:

   > Sicela ubhalise le phakheji njenge-plugin yami yangasese. Ungayithumeli ohlwini lomphakathi.

4. Uma isibhalisiwe, i-**{{display}}** izovela ngaphansi kwe-Plugins, ku-“Personal” noma ku-“Created by me”.
5. Yifake uma kudingeka, bese uyivula engxoxweni entsha.

**Qaphela**

- I-plugin ingase igcinwe endaweni yokusebenza (workspace) yethimba lakho. Uma ufuna ibe ngeyakho wedwa, hlola lapho izogcinwa khona ngaphambi kokubhalisa.
- Lesi sici singase singatholakali kuye ngohlelo lwakho lokubhaliselwa noma izilungiselelo ze-workspace. Ukuze uthole imininingwane, bona [Build plugins](https://learn.chatgpt.com/docs/build-plugins) kanye ne-[Plugins](https://learn.chatgpt.com/docs/plugins).
- I-plugin ebhaliswe ngale ndlela itholakala ku-akhawunti yakho kuphela. Ayifakwa ohlwini lomphakathi.

## C. Kopisha amafolda e-Codex

Uma ukhipha ifayela le-ZIP le-skill, uzothola ifolda efana ne-`{{first}}`. Kopisha leyo folda endaweni lapho i-Codex ifunda khona ama-skill.

| Ububanzi bokusetshenziswa | Lapho kukopishelwa khona |
| --- | --- |
| Iphrojekthi eyodwa kuphela | `.agents/skills/` ngaphakathi kwephrojekthi |
| Wonke amaphrojekthi | `~/.agents/skills/` kufolda yasekhaya (home) |

Isibonelo, ukuze wengeze i-`{{first}}` kuphrojekthi:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Qaphela**

- Kopisha yonke ifolda kanye nakho konke okuqukethwe yiyo. I-skill ngeke isebenze kahle uma kunamafayela athile kuphela.
- Uma sekukhona ifolda enegama elifanayo, hlola okuqukethwe yiyo ngaphambi kokuyibhala phezulu.

## 3. Zama

Ngemuva kokufaka, vula ingxoxo entsha bese ubiza i-skill.

| Ithuluzi | Indlela yokubiza |
| --- | --- |
| ChatGPT | Khetha ku-`@` |
| Codex | Khetha ku-`$` noma ku-`/skills` |

Sincoma ukuthi uqale ngesicelo esingashintshi noma yiliphi ifayela.

> Ngihlela ukubhala umbiko ngesiZulu. Yini okufanele ngiyiqaphele? Sicela ungashintshi noma yiliphi ifayela.

## Qinisekisa ukuthi amafayela alungile (akuphoqelekile)

Uma ufuna ukuhlola ukuthi amafayela owalandile awonakalanga, sebenzisa i-[SHA256SUMS.txt]({{sums}}).

Beka i-SHA256SUMS.txt kufolda efanayo namafayela e-ZIP owalandile, bese usebenzisa lo myalo ku-terminal. Uma i-`shasum` ingatholakali, qhathanisa i-SHA-256 ngomunye umyalo ofana ne-`Get-FileHash` ye-Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Uma imigqa yamafayela owalandile ibonisa `OK`, ayikho inkinga.

---

Amanye amathuluzi: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Izikrini nemibandela yokutholakala kungashintsha. Sicela uhlole umhlahlandlela osemthethweni wesevisi ngayinye ukuze uthole ulwazi lwakamuva (leli khasi lagcina ukuhlolwa ngomhla ziyi-14 kuOkthoba 2026).
