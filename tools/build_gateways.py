#!/usr/bin/env python3
"""Build the KUMIHAN language gateway (index.html in English, top-*.html); --check verifies.

Page copy that already existed lives in assets/gateway-copy.json; shared styles
in assets/gateway.css. Language order everywhere is by language code, with
the page's own language first (and English second in the language menu).
"""
from seo_adapter import seo_outputs
import argparse
import hashlib
import json
import re
import sys
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)
FOOTER = WEB_FONTS.FOOTER
BASE = "https://landco-llc.github.io/kumihan/"
VISIBLE, STEP = 6, 6

# Gateway pages: key -> (file, html lang, menu label, native name)
GATEWAYS = {
    "ar": ("top-ar.html", "ar", "AR", "العربية"),
    "bn": ("top-bn.html", "bn", "BN", "বাংলা"),
    "de": ("top-de.html", "de", "DE", "Deutsch"),
    "en": ("index.html", "en", "EN", "English"),
    "es": ("top-es.html", "es", "ES", "Español"),
    "fr": ("top-fr.html", "fr", "FR", "Français"),
    "hi": ("top-hi.html", "hi", "HI", "हिंदी"),
    "id": ("top-id.html", "id", "ID", "Bahasa Indonesia"),
    "it": ("top-it.html", "it", "IT", "Italiano"),
    "ja": ("top-ja.html", "ja", "JA", "日本語"),
    "ko": ("top-ko.html", "ko-KR", "KO", "한국어"),
    "pl": ("top-pl.html", "pl", "PL", "Polski"),
    "pt": ("top-pt.html", "pt", "PT", "Português"),
    "sw": ("top-sw.html", "sw", "SW", "Kiswahili"),
    "zu": ("top-zu.html", "zu", "ZU", "isiZulu"),
    "ru": ("top-ru.html", "ru", "RU", "Русский"),
    "th": ("top-th.html", "th-TH", "TH", "ไทย"),
    "vi": ("top-vi.html", "vi", "VI", "Tiếng Việt"),
    "zh-hans": ("top-zh-cn.html", "zh-Hans-CN", "ZH-HANS", "简体中文"),
    "zh-hant": ("top-zh-han.html", "zh-Hant-TW", "ZH-HANT", "繁體中文"),
}

# Language editions: code -> data. "pages" maps a reader language to the
# edition page in that language; the first entry is the edition's own page.
PRODUCTS = {
    "zu": dict(name="isiZulu", lang="zu", brand="KUMIHAN｜Hlela", glyph="Aa", label="ZU · ISIZULU", version="v0.1.0", pages={"zu":"kumihan-zu.html","en":"kumihan-zu.en.html","ja":"kumihan-zu.ja.html"}),
    "sw": dict(name="Kiswahili", lang="sw", brand="KUMIHAN｜Mizani", glyph="ng’", label="SW · SWAHILI", version="v0.1.0", pages={"sw":"kumihan-sw.html","en":"kumihan-sw.en.html","ja":"kumihan-sw.ja.html"}),
    "de": dict(name="Deutsch", lang="de", brand="KUMIHAN｜Satzbild", glyph="Ä", label="DE · GERMAN", version="v0.1.0", pages={"de":"kumihan-de.html", "en":"kumihan-de.en.html", "ja":"kumihan-de.ja.html"}),
    "hi": dict(name="हिंदी", lang="hi", brand="KUMIHAN｜अक्षर-संगति", glyph="अ", label="HI · HINDI", version="v0.1.0", pages={"hi":"kumihan-hi.html", "en":"kumihan-hi.en.html", "ja":"kumihan-hi.ja.html"}),
    "id": dict(name="Bahasa Indonesia", lang="id", brand="KUMIHAN｜Laras", glyph="Ng", label="ID · INDONESIAN", version="v0.1.0",
               pages={"id": "kumihan-id.html", "en": "kumihan-id.en.html", "ja": "kumihan-id.ja.html"}),
    "ar": dict(name="العربية", lang="ar", brand="KUMIHAN｜نضيد", glyph="ع", label="AR · ARABIC", version="v0.1.0",
               pages={"ar": "kumihan-ar.html", "en": "kumihan-ar.en.html", "ja": "kumihan-ar.ja.html"}),
    "es": dict(name="Español", lang="es", brand="KUMIHAN｜Grafía", glyph="Ñ", label="ES · SPANISH", version="v0.1.0",
               pages={"es": "kumihan-es.html", "en": "kumihan-es.en.html", "ja": "kumihan-es.ja.html"}),
    "fr": dict(name="Français", lang="fr", brand="KUMIHAN｜Accord", glyph="Ç", label="FR · FRENCH", version="v0.1.1",
               pages={"fr": "kumihan-fr.html", "en": "kumihan-fr.en.html", "ja": "kumihan-fr.ja.html"}),
    "ja": dict(name="日本語", lang="ja", brand="KUMIHAN", glyph="あ", label="JA · JAPANESE", version="v0.1.6 preview",
               pages={"ja": "kumihan.html", "en": "en.html", "zh-hant": "zh-tw.html"}),
    "ko": dict(name="한국어", lang="ko", brand="KUMIHAN｜글짜임", glyph="한", label="KO · KOREAN", version="v0.1.0",
               pages={"ko": "kumihan-ko.html", "en": "kumihan-ko.en.html", "ja": "kumihan-ko.ja.html"}),
    "pt": dict(name="Português", lang="pt", brand="KUMIHAN｜Compasso", glyph="Ã", label="PT · PORTUGUESE", version="v0.1.0",
               pages={"pt": "kumihan-pt.html", "en": "kumihan-pt.en.html", "ja": "kumihan-pt.ja.html"}),
    "th": dict(name="ไทย", lang="th", brand="KUMIHAN｜ดุลอักษร", glyph="ก", label="TH · THAI", version="v0.1.1",
               pages={"th": "kumihan-th.html", "en": "kumihan-th-en.html", "ja": "kumihan-th-ja.html"}),
    "vi": dict(name="Tiếng Việt", lang="vi", brand="KUMIHAN｜Nhịp Chữ", glyph="Ắ", label="VI · VIETNAMESE", version="v0.1.0",
               pages={"vi": "kumihan-vi.html", "en": "kumihan-vi.en.html", "ja": "kumihan-vi.ja.html"}),
    "zh-hans": dict(name="简体中文", lang="zh-Hans-CN", brand="KUMIHAN｜字律", glyph="汉", label="ZH-HANS · SIMP.", version="v0.1.0",
                    pages={"zh-hans": "kumihan-zh-cn.html", "en": "kumihan-zh-cn.en.html", "ja": "kumihan-zh-cn.ja.html"}),
    "zh-hant": dict(name="繁體中文", lang="zh-Hant-TW", brand="KUMIHAN｜字衡", glyph="漢", label="ZH-HANT · TRAD.", version="v0.1.0 preview",
                    pages={"zh-hant": "kumihan-zh-han.html", "en": "kumihan-zh-han.en.html", "ja": "kumihan-zh-han.ja.html"}),
}

# Right-to-left gateway languages.
RTL = {"ar", "fa"}

# Card text per gateway language: code -> (description, action label)
CARDS = {
    "id": {
        "ar": ("Tipografi Arab yang menangani tulisan dari kanan ke kiri dan campuran aksara, tanpa mengubah naskah asli.", "Lihat edisi bahasa Arab"),
        "de": ("Tipografi Jerman yang menghormati kata majemuk panjang, tanda kutip, ß dan ẞ, serta perbedaan DE, AT, dan CH sambil menjaga naskah asli.", "Lihat edisi bahasa Jerman"),
        "es": ("Tipografi Spanyol yang menghormati penggunaan regional, menjaga naskah asli, dan memisahkan bukti terverifikasi dari pertimbangan editorial.", "Lihat edisi bahasa Spanyol"),
        "fr": ("Tipografi Prancis yang membedakan spasi tak terputus, tanda kutip, dan gaya penulisan regional atau kelembagaan.", "Lihat edisi bahasa Prancis"),
        "hi": ("Tipografi dan desain bahasa Hindi yang menjaga naskah asli, gugus konsonan, dan matra.", "Lihat edisi bahasa Hindi"),
        "id": ("Tipografi bahasa Indonesia yang menimbang kata depan, imbuhan, kata ulang, tanda baca, dan nominal rupiah sesuai konteks, sambil menjaga naskah asli.", "Lihat edisi bahasa Indonesia"),
        "ja": ("Dari aturan pemenggalan baris Jepang (kinsoku) dan pergantian baris yang alami hingga struktur informasi, ruang kosong, dan alur baca.", "Lihat edisi bahasa Jepang"),
        "ko": ("Pergantian baris di antara eojeol (satuan spasi bahasa Korea), ritme teks, dan struktur informasi yang jelas.", "Lihat edisi bahasa Korea"),
        "pl": ("Tipografi Polandia yang cermat pada diakritik, kata satu huruf di akhir baris, angka, dan tanda kutip, tanpa mengubah naskah asli.", "Lihat edisi bahasa Polandia"),
        "pt": ("Tipografi Portugis dan desain berbasis makna yang menghormati konvensi Brasil dan Portugal serta maksud penulis.", "Lihat edisi bahasa Portugis"),
        "th": ("Menghormati batas kata dan karakter gabung bahasa Thai, untuk desain bahasa Thai yang nyaman dibaca.", "Lihat edisi bahasa Thai"),
        "vi": ("Tipografi Vietnam yang menghormati tanda nada, pergantian baris yang alami, dan konten asli.", "Lihat edisi bahasa Vietnam"),
        "zh-hans": ("Tanda baca, pergantian baris, dan campuran teks Tionghoa–Latin untuk bahasa Tionghoa Sederhana, tanpa menulis ulang naskah asli.", "Lihat edisi bahasa Tionghoa Sederhana"),
        "zh-hant": ("Memperhatikan kebiasaan tanda baca dan penataan huruf yang berbeda di Taiwan dan Hong Kong.", "Lihat edisi bahasa Tionghoa Tradisional"),
    },
    "de": {
        "ar": ("Arabische Typografie für rechtsläufige Schrift und gemischte Schriftsysteme, die das Original unverändert lässt.", "Arabische Version ansehen"),
        "de": ("Deutsche Typografie, die lange Komposita, Anführungszeichen, ß und ẞ sowie die Unterschiede zwischen DE, AT und CH respektiert und das Original schützt.", "Deutsche Version ansehen"),
        "es": ("Spanische Typografie, die regionalen Sprachgebrauch respektiert, das Original bewahrt und geprüfte Belege von redaktionellem Urteil trennt.", "Spanische Version ansehen"),
        "fr": ("Französische Typografie, die geschützte Leerzeichen, Anführungszeichen und regionale oder institutionelle Hausstile unterscheidet.", "Französische Version ansehen"),
        "hi": ("Hindi-Typografie und -Design, die das Original, Konsonantenverbindungen und Matras bewahren.", "Hindi-Version ansehen"),
        "ja": ("Von japanischen Umbruchregeln (Kinsoku) und natürlichen Zeilenumbrüchen bis zu Informationsstruktur, Weißraum und Lesefluss.", "Japanische Version ansehen"),
        "ko": ("Umbrüche zwischen Eojeol (koreanischen Leerzeicheneinheiten), Textrhythmus und klare Informationsstruktur.", "Koreanische Version ansehen"),
        "pl": ("Polnische Typografie mit korrekten diakritischen Zeichen, Einzelbuchstaben am Zeilenende, Zahlen und Anführungszeichen – ohne das Original zu verändern.", "Polnische Version ansehen"),
        "pt": ("Portugiesische Typografie und sinnorientiertes Design, das brasilianische und europäische Konventionen sowie die Absicht des Autors respektiert.", "Portugiesische Version ansehen"),
        "th": ("Respektiert thailändische Wortgrenzen und kombinierende Zeichen für thailändisches Design, das sich natürlich liest.", "Thailändische Version ansehen"),
        "vi": ("Vietnamesische Typografie, die Tonzeichen, natürliche Zeilenumbrüche und den Originalinhalt respektiert.", "Vietnamesische Version ansehen"),
        "zh-hans": ("Interpunktion, Zeilenumbrüche und gemischter chinesisch-lateinischer Text für vereinfachtes Chinesisch, ohne das Original umzuschreiben.", "Version in vereinfachtem Chinesisch ansehen"),
        "zh-hant": ("Berücksichtigt die unterschiedlichen Interpunktions- und Satzkonventionen Taiwans und Hongkongs.", "Version in traditionellem Chinesisch ansehen"),
    },
    "pl": {
        "ar": ("Typografia arabska obsługująca pismo od prawej do lewej i mieszane systemy pisma, bez zmieniania oryginału.", "Zobacz wersję arabską"),
        "de": ("Typografia niemiecka uwzględniająca długie złożenia, cudzysłowy, ß i ẞ oraz różnice między DE, AT i CH, chroniąca oryginał.", "Zobacz wersję niemiecką"),
        "es": ("Typografia hiszpańska szanująca regionalne zwyczaje językowe, chroniąca oryginał i oddzielająca sprawdzone dowody od oceny redakcyjnej.", "Zobacz wersję hiszpańską"),
        "fr": ("Typografia francuska rozróżniająca spacje niełamliwe, cudzysłowy oraz regionalne i instytucjonalne zasady redakcyjne.", "Zobacz wersję francuską"),
        "hi": ("Typografia i projektowanie w hindi, zachowujące oryginał, ligatury spółgłoskowe i matry.", "Zobacz wersję w hindi"),
        "ja": ("Od japońskich zasad łamania wierszy (kinsoku) i naturalnego podziału wierszy po strukturę informacji, światło i rytm czytania.", "Zobacz wersję japońską"),
        "ko": ("Podział wierszy między eojeol (koreańskimi jednostkami odstępu), rytm tekstu i przejrzysta struktura informacji.", "Zobacz wersję koreańską"),
        "pl": ("Typografia polska dbająca o znaki diakrytyczne, jednoliterowe wyrazy na końcu wiersza, liczby i cudzysłowy, chroniąca oryginał i jego sens.", "Zobacz wersję polską"),
        "pt": ("Typografia portugalska i projektowanie oparte na znaczeniu, szanujące konwencje Brazylii i Portugalii oraz intencję autora.", "Zobacz wersję portugalską"),
        "th": ("Szacunek dla granic wyrazów i znaków łączących w języku tajskim, dla tajskiego projektu, który czyta się naturalnie.", "Zobacz wersję tajską"),
        "vi": ("Typografia wietnamska szanująca znaki tonów, naturalny podział wierszy i oryginalną treść.", "Zobacz wersję wietnamską"),
        "zh-hans": ("Interpunkcja, podział wierszy i tekst mieszany chińsko-łaciński dla chińskiego uproszczonego, bez przepisywania oryginału.", "Zobacz wersję w chińskim uproszczonym"),
        "zh-hant": ("Uwzględnia odmienne zwyczaje interpunkcyjne i składu Tajwanu oraz Hongkongu.", "Zobacz wersję w chińskim tradycyjnym"),
    },
    "ar": {
        "ar": ("تنضيد عربي يراعي الكتابة من اليمين إلى اليسار وتداخل اللغات، ويحافظ على النص الأصلي.", "عرض النسخة العربية"),
        "es": ("تنضيد إسباني يحترم الاستخدام الإقليمي ويحافظ على الأصل، ويفصل بين الأدلة المتحقق منها والقرار التحريري.", "عرض النسخة الإسبانية"),
        "fr": ("تنضيد فرنسي يميّز المسافات غير القابلة للكسر وعلامات الاقتباس وأدلة الأسلوب الإقليمية والمؤسسية.", "عرض النسخة الفرنسية"),
        "ja": ("من قواعد كسر الأسطر اليابانية (كينسوكو) والفواصل الطبيعية إلى بنية المعلومات والمسافات ومسار القراءة.", "عرض النسخة اليابانية"),
        "ko": ("كسر الأسطر بين وحدات الكلام الكورية (أوجول)، مع العناية بإيقاع النص ووضوح بنية المعلومات.", "عرض النسخة الكورية"),
        "pt": ("تنضيد برتغالي وتصميم يقوده المعنى، يحترم أعراف البرازيل والبرتغال وقصد الكاتب.", "عرض النسخة البرتغالية"),
        "th": ("يحترم حدود الكلمات التايلاندية والحروف المركّبة، لتصميم تايلاندي سهل القراءة.", "عرض النسخة التايلاندية"),
        "zh-hans": ("علامات الترقيم وكسر الأسطر والمزج بين الصينية واللاتينية للصينية المبسطة، دون إعادة كتابة الأصل.", "عرض نسخة الصينية المبسطة"),
        "zh-hant": ("يراعي أعراف الترقيم والتنضيد المختلفة في تايوان وهونغ كونغ.", "عرض نسخة الصينية التقليدية"),
        "hi": ("تنضيد وتصميم هندي يحافظ على الأصل والحروف المركّبة وعلامات الحركات.", "عرض النسخة الهندية"),
        "vi": ("تنضيد فيتنامي يحافظ على علامات النغمة وفواصل الأسطر الطبيعية والمحتوى الأصلي.", "عرض النسخة الفيتنامية"),
    },
    "es": {
        "ar": ("Tipografía árabe que gestiona la escritura de derecha a izquierda y la mezcla de alfabetos, sin alterar el original.", "Ver la edición en árabe"),
        "es": ("Tipografía en español que respeta el uso regional, conserva el original y separa la evidencia comprobada del criterio editorial.", "Ver la edición en español"),
        "fr": ("Tipografía francesa que distingue los espacios de no separación, las comillas y los libros de estilo regionales o institucionales.", "Ver la edición en francés"),
        "ja": ("De las reglas japonesas de división de líneas (kinsoku) y los saltos naturales a la estructura de la información, los espacios y el recorrido de lectura.", "Ver la edición en japonés"),
        "ko": ("Saltos de línea entre eojeol (unidades de espaciado coreanas), ritmo del texto y una estructura de información clara.", "Ver la edición en coreano"),
        "pt": ("Tipografía portuguesa y diseño guiado por el sentido, que respeta las convenciones de Brasil y Portugal y la intención del autor.", "Ver la edición en portugués"),
        "th": ("Respeta los límites de palabra y los caracteres combinados del tailandés, para un diseño que se lee con naturalidad.", "Ver la edición en tailandés"),
        "zh-hans": ("Puntuación, saltos de línea y mezcla de chino y alfabeto latino para el chino simplificado, sin reescribir el original.", "Ver la edición en chino simplificado"),
        "zh-hant": ("Atiende las convenciones de puntuación y composición propias de Taiwán y Hong Kong.", "Ver la edición en chino tradicional"),
        "hi": ("Tipografía y diseño en hindi que conservan el original, los conjuntos consonánticos y las matras.", "Ver la edición en hindi"),
        "vi": ("Tipografía vietnamita que respeta los signos de tono, los saltos de línea naturales y el contenido original.", "Ver la edición en vietnamita"),
    },
    "fr": {
        "ar": ("Typographie arabe qui gère l’écriture de droite à gauche et le mélange des écritures, sans toucher au texte d’origine.", "Voir l’édition arabe"),
        "es": ("Typographie espagnole qui respecte les usages régionaux, préserve la source et distingue les preuves vérifiées du jugement éditorial.", "Voir l’édition espagnole"),
        "fr": ("Typographie française qui distingue espaces insécables, guillemets et styles maison régionaux ou institutionnels.", "Voir l’édition française"),
        "ja": ("Des règles japonaises de coupure (kinsoku) et des retours à la ligne naturels à la structure de l’information, aux blancs et au parcours de lecture.", "Voir l’édition japonaise"),
        "ko": ("Coupures entre eojeol (unités d’espacement coréennes), rythme du texte et structure de l’information lisible.", "Voir l’édition coréenne"),
        "pt": ("Typographie portugaise et design guidé par le sens, qui respectent les usages du Brésil et du Portugal et l’intention de l’auteur.", "Voir l’édition portugaise"),
        "th": ("Respect des limites de mots et des caractères combinatoires du thaï, pour un design thaï qui se lit naturellement.", "Voir l’édition thaïe"),
        "zh-hans": ("Ponctuation, coupures et mélange chinois–latin pour le chinois simplifié, sans réécrire la source.", "Voir l’édition en chinois simplifié"),
        "zh-hant": ("Prend en compte les usages de ponctuation et de composition propres à Taïwan et à Hong Kong.", "Voir l’édition en chinois traditionnel"),
        "hi": ("Typographie et design en hindi qui préservent la source, les ligatures consonantiques et les matras.", "Voir l’édition hindie"),
        "vi": ("Typographie vietnamienne qui respecte les signes de ton, les coupures naturelles et le contenu d’origine.", "Voir l’édition vietnamienne"),
    },
    "pt": {
        "ar": ("Tipografia árabe que trata a escrita da direita para a esquerda e a mistura de alfabetos, sem alterar o original.", "Ver a edição em árabe"),
        "es": ("Tipografia espanhola que respeita o uso regional, preserva o original e separa a evidência verificada do critério editorial.", "Ver a edição em espanhol"),
        "fr": ("Tipografia francesa que distingue espaços inseparáveis, aspas e normas editoriais regionais ou institucionais.", "Ver a edição em francês"),
        "ja": ("Das regras japonesas de quebra de linha (kinsoku) e das quebras naturais à estrutura da informação, aos espaços e ao percurso de leitura.", "Ver a edição em japonês"),
        "ko": ("Quebras de linha entre eojeol (unidades de espaçamento coreanas), ritmo do texto e uma estrutura de informação clara.", "Ver a edição em coreano"),
        "pt": ("Tipografia portuguesa e design orientado pelo sentido, que respeita as convenções do Brasil e de Portugal e a intenção do autor.", "Ver a edição em português"),
        "th": ("Respeita os limites de palavra e os caracteres combinados do tailandês, para um design que se lê com naturalidade.", "Ver a edição em tailandês"),
        "zh-hans": ("Pontuação, quebras de linha e mistura de chinês e alfabeto latino para o chinês simplificado, sem reescrever o original.", "Ver a edição em chinês simplificado"),
        "zh-hant": ("Atende às convenções de pontuação e composição próprias de Taiwan e Hong Kong.", "Ver a edição em chinês tradicional"),
        "hi": ("Tipografia e design em hindi que preservam o original, os conjuntos consonânticos e as matras.", "Ver a edição em hindi"),
        "vi": ("Tipografia vietnamita que respeita os sinais de tom, as quebras de linha naturais e o conteúdo original.", "Ver a edição em vietnamita"),
    },
    "hi": {
        "ar": ("दाएँ से बाएँ लिखावट और मिश्रित लिपियों को सँभालने वाली, मूल को सुरक्षित रखने वाली अरबी टाइपोग्राफ़ी।", "अरबी संस्करण देखें"),
        "es": ("क्षेत्रीय प्रयोग का सम्मान करने वाली, मूल को सुरक्षित रखने और जाँचे गए प्रमाण को संपादकीय निर्णय से अलग रखने वाली स्पेनिश टाइपोग्राफ़ी।", "स्पेनिश संस्करण देखें"),
        "fr": ("न टूटने वाली खाली जगह, उद्धरण चिह्न और क्षेत्रीय या संस्थागत शैली नियमों में भेद करने वाली फ़्रेंच टाइपोग्राफ़ी।", "फ़्रेंच संस्करण देखें"),
        "hi": ("मूल पाठ, संयुक्ताक्षर और मात्राओं को सुरक्षित रखने वाली हिंदी टाइपोग्राफ़ी और डिज़ाइन।", "हिंदी संस्करण देखें"),
        "ja": ("जापानी लाइन-ब्रेक नियमों (किनसोकु) और स्वाभाविक लाइन ब्रेक से लेकर जानकारी की संरचना, खाली जगह और पढ़ने के क्रम तक।", "जापानी संस्करण देखें"),
        "ko": ("कोरियाई ओजोल (शब्द-इकाइयों) के बीच लाइन ब्रेक, पाठ की लय और स्पष्ट जानकारी की संरचना।", "कोरियाई संस्करण देखें"),
        "pt": ("ब्राज़ील और पुर्तगाल की परंपराओं और लेखक के आशय का सम्मान करने वाली पुर्तगाली टाइपोग्राफ़ी और अर्थ-आधारित डिज़ाइन।", "पुर्तगाली संस्करण देखें"),
        "th": ("थाई शब्द-सीमाओं और संयुक्त वर्णों का सम्मान करते हुए, सहज पढ़ने वाला थाई डिज़ाइन।", "थाई संस्करण देखें"),
        "vi": ("स्वर-चिह्नों, स्वाभाविक लाइन ब्रेक और मूल सामग्री का सम्मान करने वाली वियतनामी टाइपोग्राफ़ी।", "वियतनामी संस्करण देखें"),
        "zh-hans": ("सरलीकृत चीनी के लिए विराम चिह्न, लाइन ब्रेक और चीनी–लैटिन मिश्रित पाठ, मूल को बदले बिना।", "सरलीकृत चीनी संस्करण देखें"),
        "zh-hant": ("ताइवान और हांगकांग की अलग-अलग विराम चिह्न और टाइपसेटिंग परंपराओं का ध्यान रखती है।", "पारंपरिक चीनी संस्करण देखें"),
    },
    "vi": {
        "ar": ("Typography tiếng Ả Rập xử lý chữ viết từ phải sang trái và văn bản đa hệ chữ, giữ nguyên bản gốc.", "Xem phiên bản tiếng Ả Rập"),
        "es": ("Typography tiếng Tây Ban Nha tôn trọng cách dùng theo vùng, giữ nguyên bản gốc và tách bằng chứng đã kiểm chứng khỏi nhận định biên tập.", "Xem phiên bản tiếng Tây Ban Nha"),
        "fr": ("Typography tiếng Pháp phân biệt khoảng trắng không ngắt, dấu ngoặc kép và quy chuẩn biên tập theo vùng hoặc tổ chức.", "Xem phiên bản tiếng Pháp"),
        "hi": ("Typography và thiết kế tiếng Hindi giữ nguyên bản gốc, các phụ âm ghép và dấu nguyên âm (matra).", "Xem phiên bản tiếng Hindi"),
        "ja": ("Từ quy tắc ngắt dòng tiếng Nhật (kinsoku) và chỗ ngắt dòng tự nhiên đến cấu trúc thông tin, khoảng trắng và luồng đọc.", "Xem phiên bản tiếng Nhật"),
        "ko": ("Ngắt dòng giữa các eojeol (đơn vị cách chữ tiếng Hàn), nhịp điệu văn bản và cấu trúc thông tin rõ ràng.", "Xem phiên bản tiếng Hàn"),
        "pt": ("Typography tiếng Bồ Đào Nha và thiết kế dựa trên ý nghĩa, tôn trọng quy ước của Brasil và Bồ Đào Nha cùng ý định của tác giả.", "Xem phiên bản tiếng Bồ Đào Nha"),
        "th": ("Tôn trọng ranh giới từ và ký tự kết hợp của tiếng Thái, cho thiết kế tiếng Thái dễ đọc.", "Xem phiên bản tiếng Thái"),
        "vi": ("Giữ dấu thanh và chỗ ngắt dòng tự nhiên, sắp xếp thông tin và khoảng trắng cho typography tiếng Việt.", "Xem phiên bản tiếng Việt"),
        "zh-hans": ("Dấu câu, ngắt dòng và văn bản pha trộn Hán–Latin cho tiếng Trung giản thể, không viết lại bản gốc.", "Xem phiên bản tiếng Trung giản thể"),
        "zh-hant": ("Chú ý đến quy ước dấu câu và dàn chữ riêng của Đài Loan và Hồng Kông.", "Xem phiên bản tiếng Trung phồn thể"),
    },
    "ja": {
        "ar": ("RTLと多言語混植を扱い、原文を守るアラビア語の文字組。", "アラビア語版を見る"),
        "es": ("スペイン語の文字組と原稿保全。地域の表現を尊重し、確認できた根拠と編集判断を分けて伝えます。", "スペイン語版を見る"),
        "fr": ("不改行空白、引用符、地域と組織の編集規約を区別するフランス語文字組。", "フランス語版を見る"),
        "ja": ("日本語の禁則・自然な改行、情報構造、余白や視線の流れまで考えます。", "日本語版を見る"),
        "ko": ("어절単位の改行や文字のリズム、伝わる情報構造に配慮します。", "韓国語版を見る"),
        "pt": ("ポルトガル語の文字組と意味に沿ったデザイン。ブラジルとポルトガルの表記差を尊重し、原稿の意図を守ります。", "ポルトガル語版を見る"),
        "th": ("単語境界・結合文字を尊重し、読みやすいタイ語デザインへ。", "タイ語版を見る"),
        "vi": ("声調記号と自然な改行を守り、情報と余白を整えるベトナム語の文字組とデザイン。", "ベトナム語版を見る"),
        "zh-hans": ("標点・禁則と中英混植、原稿の保全を大切にするKUMIHAN｜字律。", "簡体中国語版を見る"),
        "zh-hant": ("臺灣・香港それぞれの約物と文字組に向き合うKUMIHAN｜字衡。", "繁体中国語版を見る"),
    },
    "en": {
        "ar": ("Arabic typography that handles right-to-left text and mixed scripts while keeping the original intact.", "View the Arabic edition"),
        "es": ("Spanish typography that respects regional usage, preserves the source and separates verified evidence from editorial judgment.", "View the Spanish edition"),
        "fr": ("French typography that distinguishes no-break spaces, quotation marks and regional or institutional house styles.", "View the French edition"),
        "ja": ("From Japanese line-breaking rules (kinsoku) and natural line breaks to information structure, whitespace and reading flow.", "View the Japanese edition"),
        "ko": ("Line breaks between eojeol (Korean spacing units), textual rhythm and information structure that communicates clearly.", "View the Korean edition"),
        "pt": ("Portuguese typography and meaning-led design that respects Brazilian and European conventions and the author’s intent.", "View the Portuguese edition"),
        "th": ("Respecting Thai word boundaries and combining characters, for Thai design that reads naturally.", "View the Thai edition"),
        "vi": ("Vietnamese typography that respects tone marks, meaningful line breaks and original content.", "View the Vietnamese edition"),
        "zh-hans": ("Punctuation, line breaks and mixed Chinese–Latin text for mainland China, without rewriting your source.", "View the Simplified Chinese edition"),
        "zh-hant": ("Addresses the distinct punctuation and typesetting conventions of Taiwan and Hong Kong.", "View the Traditional Chinese edition"),
    },
    "zh-hant": {
        "ar": ("處理由右至左書寫與多語混排，並保留原文的阿拉伯文排版。", "前往阿拉伯文版"),
        "es": ("尊重各地區用法、保留原稿，並區分已確認依據與編輯判斷的西班牙文排版。", "前往西班牙文版"),
        "fr": ("區分不斷行空格、引號，以及地區與機構編輯規範的法文排版。", "前往法文版"),
        "ja": ("從日文的禁則處理與自然換行，到資訊架構、留白與閱讀動線。", "前往日文版"),
        "ko": ("以韓文的語節（어절）為單位換行，兼顧文字節奏與清楚的資訊架構。", "前往韓文版"),
        "pt": ("尊重巴西與葡萄牙的書寫差異，依意義設計並守護原稿意圖的葡萄牙文排版。", "前往葡萄牙文版"),
        "th": ("尊重泰文的斷詞與組合字元，打造易讀的泰文設計。", "前往泰文版"),
        "vi": ("保護越南文聲調符號，兼顧自然換行、資訊層次與原稿完整性。", "前往越南文版"),
        "zh-hans": ("面向中國大陸簡體中文，重視標點、換行與中英混排，並保留原稿。", "前往簡體中文版"),
        "zh-hant": ("分別對應臺灣與香港的標點符號與排版習慣。", "前往繁體中文版"),
        "hi": ("保留原稿、連字與母音符號的印地文排版與設計。", "前往印地文版"),
    },
    "zh-hans": {
        "ar": ("处理从右到左书写与多语混排，并保留原文的阿拉伯文排版。", "前往阿拉伯文版"),
        "es": ("尊重各地区用法、保留原稿，并区分已确认依据与编辑判断的西班牙文排版。", "前往西班牙文版"),
        "fr": ("区分不换行空格、引号，以及地区与机构编辑规范的法文排版。", "前往法文版"),
        "ja": ("从日文的避头尾处理与自然换行，到信息结构、留白与阅读动线。", "前往日文版"),
        "ko": ("以韩文的语节（어절）为单位换行，兼顾文字节奏与清晰的信息结构。", "前往韩文版"),
        "pt": ("尊重巴西与葡萄牙的书写差异，按意义设计并守护原稿意图的葡萄牙文排版。", "前往葡萄牙文版"),
        "th": ("尊重泰文的分词与组合字符，打造易读的泰文设计。", "前往泰文版"),
        "vi": ("保护越南语声调符号，兼顾自然换行、信息层次和原文完整性。", "前往越南语版"),
        "zh-hans": ("面向中国大陆简体中文，重视标点、换行与中英混排，并保留原稿。", "前往简体中文版"),
        "zh-hant": ("分别对应台湾与香港的标点符号与排版习惯。", "前往繁体中文版"),
        "hi": ("保留原稿、连字与元音符号的印地语排版与设计。", "前往印地语版"),
    },
    "ko": {
        "ar": ("오른쪽에서 왼쪽으로 쓰는 글과 다국어 혼용을 다루며 원문을 지키는 아랍어 글짜임.", "아랍어 버전 보기"),
        "es": ("지역별 표현을 존중하고 원고를 지키며, 확인한 근거와 편집 판단을 구분하는 스페인어 글짜임.", "스페인어 버전 보기"),
        "fr": ("줄바꿈하지 않는 공백, 인용 부호, 지역과 기관의 편집 규정을 구분하는 프랑스어 글짜임.", "프랑스어 버전 보기"),
        "ja": ("일본어의 금칙 처리와 자연스러운 줄바꿈, 정보 구조, 여백과 시선의 흐름까지 고려합니다.", "일본어 버전 보기"),
        "ko": ("어절 단위 줄바꿈과 글의 리듬, 잘 전달되는 정보 구조를 고려한 KUMIHAN｜글짜임.", "한국어 버전 보기"),
        "pt": ("브라질과 포르투갈의 표기 차이를 존중하고 원고의 의도를 지키는 포르투갈어 글짜임.", "포르투갈어 버전 보기"),
        "th": ("단어 경계와 결합 문자를 존중해, 읽기 쉬운 태국어 디자인으로.", "태국어 버전 보기"),
        "vi": ("성조 부호와 자연스러운 줄바꿈을 지키고 원고를 보존하는 베트남어 글짜임.", "베트남어 버전 보기"),
        "zh-hans": ("중국 본토 간체 중국어의 문장 부호와 줄바꿈, 중영 혼용 조판을 다룹니다.", "간체 중국어 버전 보기"),
        "zh-hant": ("대만과 홍콩, 각 지역의 문장 부호와 조판에 맞춥니다.", "번체 중국어 버전 보기"),
        "hi": ("원고와 결합 자음, 모음 기호를 지키는 힌디어 글짜임과 디자인.", "힌디어 버전 보기"),
    },
    "th": {
        "ar": ("การจัดวางตัวอักษรอาหรับที่รองรับการเขียนจากขวาไปซ้ายและการผสมหลายภาษา โดยรักษาต้นฉบับไว้", "ดูเวอร์ชันภาษาอาหรับ"),
        "es": ("การจัดวางตัวอักษรสเปนที่เคารพการใช้ภาษาตามภูมิภาค รักษาต้นฉบับ และแยกหลักฐานที่ตรวจแล้วออกจากการตัดสินใจทางบรรณาธิการ", "ดูเวอร์ชันภาษาสเปน"),
        "fr": ("การจัดวางตัวอักษรฝรั่งเศสที่แยกแยะช่องว่างไม่ตัดบรรทัด เครื่องหมายอัญประกาศ และแนวทางบรรณาธิการของแต่ละภูมิภาคและองค์กร", "ดูเวอร์ชันภาษาฝรั่งเศส"),
        "ja": ("คำนึงถึงกฎการตัดบรรทัดของภาษาญี่ปุ่น โครงสร้างข้อมูล พื้นที่ว่าง และลำดับสายตา", "ดูเวอร์ชันภาษาญี่ปุ่น"),
        "ko": ("ตัดบรรทัดตามหน่วยคำของภาษาเกาหลี พร้อมใส่ใจจังหวะของตัวอักษรและโครงสร้างข้อมูลที่สื่อสารได้ชัด", "ดูเวอร์ชันภาษาเกาหลี"),
        "pt": ("การจัดวางตัวอักษรโปรตุเกสที่เคารพความต่างของบราซิลและโปรตุเกส และรักษาเจตนาของต้นฉบับ", "ดูเวอร์ชันภาษาโปรตุเกส"),
        "th": ("เคารพการแบ่งคำและตำแหน่งสระ–วรรณยุกต์ เพื่องานออกแบบภาษาไทยที่อ่านง่าย", "ดูเวอร์ชันภาษาไทย"),
        "vi": ("การจัดวางตัวอักษรเวียดนามที่รักษาเครื่องหมายวรรณยุกต์ การตัดบรรทัดที่เป็นธรรมชาติ และเนื้อหาต้นฉบับ", "ดูเวอร์ชันภาษาเวียดนาม"),
        "zh-hans": ("ใส่ใจเครื่องหมายวรรคตอน การตัดบรรทัด และการผสมอักษรจีนกับละตินของภาษาจีนตัวย่อ", "ดูเวอร์ชันภาษาจีนตัวย่อ"),
        "zh-hant": ("ใส่ใจเครื่องหมายวรรคตอนและการจัดวางตัวอักษรของไต้หวันและฮ่องกง", "ดูเวอร์ชันภาษาจีนตัวเต็ม"),
        "hi": ("การจัดวางตัวอักษรและการออกแบบภาษาฮินดีที่รักษาต้นฉบับ พยัญชนะควบ และสระ", "ดูเวอร์ชันภาษาฮินดี"),
    },
}

UI = {
    "bn": dict(heading="KUMIHAN-এর ভাষা সংস্করণ", more="পরের {n}টি দেখুন", menu="ভাষা"),
    "it": dict(heading="Le edizioni linguistiche di KUMIHAN", more="Mostra le prossime {n}", menu="Lingua"),
    "ru": dict(heading="Языковые версии KUMIHAN", more="Показать ещё {n}", menu="Язык"),
    "id": dict(heading="Edisi bahasa KUMIHAN", more="Tampilkan {n} berikutnya", menu="Bahasa"),
    "de": dict(heading="Die Sprachversionen von KUMIHAN", more="Die nächsten {n} anzeigen", menu="Sprache"),
    "pl": dict(heading="Wersje językowe KUMIHAN", more="Pokaż kolejne {n}", menu="Język"),
    "ar": dict(heading="نسخ KUMIHAN اللغوية", more="عرض {n} أخرى", menu="اللغة"),
    "es": dict(heading="Ediciones de KUMIHAN por idioma", more="Mostrar {n} más", menu="Idioma"),
    "fr": dict(heading="Les éditions de KUMIHAN", more="Afficher les {n} suivantes", menu="Langue"),
    "pt": dict(heading="Edições do KUMIHAN por língua", more="Mostrar mais {n}", menu="Língua"),
    "hi": dict(heading="KUMIHAN के भाषा संस्करण", more="अगले {n} देखें", menu="भाषा"),
    "vi": dict(heading="Các phiên bản ngôn ngữ của KUMIHAN", more="Hiển thị {n} mục tiếp theo", menu="Ngôn ngữ"),
    "ja": dict(heading="KUMIHANの各言語版", more="次の{n}つを表示", menu="表示言語"),
    "en": dict(heading="KUMIHAN language editions", more="Show the next {n}", menu="Language"),
    "zh-hant": dict(heading="KUMIHAN 各語言版本", more="顯示接下來的 {n} 個", menu="語言"),
    "zh-hans": dict(heading="KUMIHAN 各语言版本", more="显示接下来的 {n} 个", menu="语言"),
    "ko": dict(heading="KUMIHAN 언어별 버전", more="다음 {n}개 보기", menu="언어"),
    "zu": dict(heading="Izinguqulo zezilimi ze-KUMIHAN", more="Bonisa ezilandelayo ezi-{n}", menu="Ulimi"),
    "sw": dict(heading="Matoleo ya lugha ya KUMIHAN", more="Onyesha {n} zinazofuata", menu="Lugha"),
    "th": dict(heading="KUMIHAN ในแต่ละภาษา", more="แสดงอีก {n} รายการ", menu="ภาษา"),
}

# Hindi edition: same card dimensions and navigation behavior as existing editions.
for _lang, _cards in CARDS.items():
    _cards.setdefault("hi", ("結合文字・母音記号・原稿を守るヒンディー語の文字組とデザイン。", "ヒンディー語版を見る") if _lang == "ja" else ("Hindi typography and design with source fidelity, conjuncts and matras.", "View the Hindi edition"))


# Satzbild card copy; preserve every existing edition and gateway.
CARDS['ja']["de"] = ('長い複合語、引用符、ß・ẞとDE・AT・CHの違いを尊重し、原稿を守るドイツ語組版。', 'ドイツ語版を見る')
CARDS['en']["de"] = ('German typography with long compounds, quotation marks and distinct DE/AT/CH conventions, preserving the original.', 'View the German edition')
CARDS['ko']["de"] = ('긴 합성어, 인용 부호, DE·AT·CH의 차이를 존중하고 원고를 지키는 독일어 글짜임.', '독일어 버전 보기')
CARDS['zh-hans']["de"] = ('尊重长复合词、引号及德国、奥地利、瑞士差异，保护原稿的德语排版。', '查看德语版')
CARDS['zh-hant']["de"] = ('尊重長複合詞、引號及德國、奧地利、瑞士差異，保護原稿的德語排版。', '查看德語版')
CARDS['es']["de"] = ('Tipografía alemana que respeta los compuestos largos, las comillas y las variantes DE/AT/CH, sin alterar el original.', 'Ver la edición en alemán')
CARDS['fr']["de"] = ('Typographie allemande respectant les mots composés, les guillemets et les variantes DE/AT/CH, sans modifier l’original.', 'Voir l’édition allemande')
CARDS['pt']["de"] = ('Tipografia alemã que respeita palavras compostas, aspas e variantes DE/AT/CH, preservando o original.', 'Ver a edição em alemão')
CARDS['ar']["de"] = ('تنضيد ألماني يحترم الكلمات المركبة وعلامات الاقتباس والاختلافات الإقليمية ويحافظ على الأصل.', 'عرض النسخة الألمانية')
CARDS['hi']["de"] = ('मूल पाठ को सुरक्षित रखते हुए जर्मन संयुक्त शब्दों, उद्धरण चिह्नों और क्षेत्रीय भिन्नताओं का ध्यान रखने वाली टाइपोग्राफी।', 'जर्मन संस्करण देखें')
CARDS['vi']["de"] = ('Kiểu chữ tiếng Đức tôn trọng từ ghép dài, dấu ngoặc kép và khác biệt DE/AT/CH, giữ nguyên bản gốc.', 'Xem phiên bản tiếng Đức')
CARDS['th']["de"] = ('การจัดวางตัวอักษรเยอรมันที่เคารพคำประสม เครื่องหมายอัญประกาศ และความต่างระหว่างภูมิภาค โดยรักษาต้นฉบับ', 'ดูเวอร์ชันภาษาเยอรมัน')


# KUMIHAN｜Szyk — Polish v0.1.0 language edition; all gateway cards are generated
# from this single registry instead of manually changing index/top pages.
PRODUCTS["pl"] = dict(
    name="Polski", lang="pl", brand="KUMIHAN｜Szyk", glyph="Ł",
    label="PL · POLISH", version="v0.1.0",
    pages={"pl":"kumihan-pl.html", "en":"kumihan-pl.en.html", "ja":"kumihan-pl.ja.html"})
PL_CARD_COPY = {
    "ja": ("ポーランド語の特殊文字、一文字語の行末、数値・引用符を扱い、原稿と意味を守る文字組みとデザイン。","ポーランド語版を見る"),
    "en": ("Polish typography with accurate diacritics, meaningful wrapping and source-preserving design.","View the Polish edition"),
    "zh-hant": ("尊重波蘭文特殊字母、換行與數字格式，兼顧原稿完整性的排版與設計。","前往波蘭文版"),
    "zh-hans": ("尊重波兰语特殊字母、换行和数字格式，维护原稿完整性的排版与设计。","前往波兰语版"),
    "ko": ("폴란드어 특수문자, 줄바꿈, 숫자 표기를 존중하고 원문을 지키는 타이포그래피와 디자인.","폴란드어 버전 보기"),
    "th": ("การจัดวางตัวอักษรโปแลนด์ที่ใส่ใจเครื่องหมายกำกับ การตัดบรรทัดและตัวเลข โดยรักษาต้นฉบับ","ดูเวอร์ชันภาษาโปแลนด์"),
    "ar": ("تنضيد بولندي يراعي الحروف المميزة وفواصل الأسطر وتنسيق الأرقام مع الحفاظ على النص الأصلي.","عرض النسخة البولندية"),
    "es": ("Tipografía polaca que respeta los signos diacríticos, los saltos de línea y el contenido original.","Ver la edición en polaco"),
    "fr": ("Typographie polonaise respectueuse des signes diacritiques, des retours à la ligne et du texte source.","Voir la version polonaise"),
    "hi": ("पोलिश टाइपोग्राफी में विशेष अक्षरों, पंक्ति-विभाजन और मूल पाठ की अखंडता का ध्यान रखा जाता है।","पोलिश संस्करण देखें"),
    "pt": ("Tipografia polonesa que respeita diacríticos, quebras de linha e o texto original.","Ver a edição em polonês"),
    "vi": ("Thiết kế chữ tiếng Ba Lan chú trọng dấu phụ, ngắt dòng và giữ nguyên nội dung gốc.","Xem phiên bản tiếng Ba Lan"),
}
for _lang, _cards in CARDS.items():
    if _lang in PL_CARD_COPY:
        _cards.setdefault("pl", PL_CARD_COPY[_lang])

# Indonesian edition (KUMIHAN｜Laras) for every reader language.
ID_CARD_COPY = {
    "de": (
        "Indonesische Typografie, die Präpositionen, Affixe, Reduplikationen, Satzzeichen und Rupiah-Beträge im Kontext behandelt und das Original schützt.",
        "Indonesische Version ansehen"
    ),
    "pl": (
        "Typografia indonezyjska uwzględniająca przyimki, afiksy, reduplikację, interpunkcję i kwoty w rupiach, chroniąca oryginał.",
        "Zobacz wersję indonezyjską"
    ),
    "ar": (
        "تنضيد إندونيسي يراعي حروف الجر واللواحق والتكرار وعلامات الترقيم ومبالغ الروبية، ويحافظ على النص الأصلي.",
        "عرض النسخة الإندونيسية"
    ),
    "es": (
        "Tipografía indonesia que atiende preposiciones, afijos, reduplicación, puntuación e importes en rupias, sin alterar el original.",
        "Ver la edición en indonesio"
    ),
    "fr": (
        "Typographie indonésienne attentive aux prépositions, affixes, redoublements, à la ponctuation et aux montants en roupies, sans toucher au texte d’origine.",
        "Voir l’édition indonésienne"
    ),
    "pt": (
        "Tipografia indonésia atenta a preposições, afixos, reduplicação, pontuação e valores em rupias, sem alterar o original.",
        "Ver a edição em indonésio"
    ),
    "hi": (
        "पूर्वसर्ग, प्रत्यय, पुनरुक्ति, विराम चिह्न और रुपिया राशियों का ध्यान रखने वाली, मूल को सुरक्षित रखने वाली इंडोनेशियाई टाइपोग्राफ़ी।",
        "इंडोनेशियाई संस्करण देखें"
    ),
    "vi": (
        "Typography tiếng Indonesia chú ý giới từ, phụ tố, từ láy, dấu câu và số tiền rupiah, giữ nguyên bản gốc.",
        "Xem phiên bản tiếng Indonesia"
    ),
    "ja": (
        "前置詞と接辞、重複語、句読点、ルピアの金額を文脈に合わせて扱い、原稿を守るインドネシア語の文字組とデザイン。",
        "インドネシア語版を見る"
    ),
    "en": (
        "Indonesian typography that respects prepositions, affixes, reduplication, punctuation and rupiah values while keeping the source intact.",
        "View the Indonesian edition"
    ),
    "zh-hant": (
        "依語境處理介詞、詞綴、重疊詞、標點與印尼盾金額，並保留原稿的印尼文排版與設計。",
        "前往印尼文版"
    ),
    "zh-hans": (
        "按语境处理介词、词缀、重叠词、标点与印尼盾金额，并保留原稿的印尼语排版与设计。",
        "前往印尼语版"
    ),
    "ko": (
        "전치사와 접사, 중첩어, 문장 부호, 루피아 금액을 맥락에 맞게 다루고 원고를 지키는 인도네시아어 글짜임.",
        "인도네시아어 버전 보기"
    ),
    "th": (
        "การจัดวางตัวอักษรอินโดนีเซียที่ใส่ใจคำบุพบท หน่วยคำเติม คำซ้ำ เครื่องหมายวรรคตอน และจำนวนเงินรูเปียห์ โดยรักษาต้นฉบับ",
        "ดูเวอร์ชันภาษาอินโดนีเซีย"
    )
}
for _lang, _cards in CARDS.items():
    if _lang in ID_CARD_COPY:
        _cards.setdefault("id", tuple(ID_CARD_COPY[_lang]))

# Bangla edition (KUMIHAN｜অক্ষরসজ্জা): its card for every reader language and the
# Bangla reader's table of all editions.
PRODUCTS["bn"] = dict(name="বাংলা", lang="bn", brand="KUMIHAN｜অক্ষরসজ্জা", glyph="অ", label="BN · BANGLA", version="v0.1.0",
                      pages={"bn": "kumihan-bn.html", "en": "kumihan-bn.en.html", "ja": "kumihan-bn.ja.html"})
BN_CARD_COPY = {
    "ja": ("母音記号・結合文字と原稿を守り、bn-BD／bn-INを区別するベンガル語の文字組みとデザイン。", "ベンガル語版を見る"),
    "en": ("Bangla typography and design with safe vowel signs, conjuncts, source fidelity and distinct bn-BD/bn-IN guidance.", "View the Bangla edition"),
    "zh-hant": ("保護母音符號、連字與原稿，並區分 bn-BD／bn-IN 的孟加拉文排版與設計。", "前往孟加拉文版"),
    "zh-hans": ("保护元音符号、连字与原稿，并区分 bn-BD／bn-IN 的孟加拉语排版与设计。", "前往孟加拉语版"),
    "ko": ("모음 기호와 결합 문자, 원고를 지키고 bn-BD·bn-IN을 구분하는 벵골어 글짜임과 디자인.", "벵골어 버전 보기"),
    "th": ("การจัดวางตัวอักษรและการออกแบบภาษาเบงกาลีที่รักษาสระ ตัวอักษรควบ และต้นฉบับ พร้อมแยก bn-BD กับ bn-IN", "ดูเวอร์ชันภาษาเบงกาลี"),
    "fr": ("Typographie et design en bengali qui préservent les signes vocaliques, les ligatures et la source, en distinguant bn-BD et bn-IN.", "Voir l’édition bengalie"),
    "es": ("Tipografía y diseño en bengalí que conservan los signos vocálicos, las ligaduras y el original, y distinguen bn-BD y bn-IN.", "Ver la edición en bengalí"),
    "pt": ("Tipografia e design em bengali que preservam sinais vocálicos, ligaduras e o original, distinguindo bn-BD e bn-IN.", "Ver a edição em bengali"),
    "ar": ("تنضيد وتصميم بنغالي يحافظ على علامات الحركات والحروف المركّبة والنص الأصلي، ويميّز بين bn-BD وbn-IN.", "عرض النسخة البنغالية"),
    "hi": ("मात्राओं, संयुक्ताक्षरों और मूल पाठ को सुरक्षित रखने वाली, bn-BD और bn-IN में भेद करने वाली बांग्ला टाइपोग्राफ़ी और डिज़ाइन।", "बांग्ला संस्करण देखें"),
    "vi": ("Typography và thiết kế tiếng Bengal giữ nguyên dấu nguyên âm, chữ ghép và bản gốc, phân biệt bn-BD và bn-IN.", "Xem phiên bản tiếng Bengal"),
    "de": ("Bengalische Typografie und Gestaltung, die Vokalzeichen, Ligaturen und das Original bewahren und bn-BD von bn-IN unterscheiden.", "Bengalische Version ansehen"),
    "pl": ("Typografia i projektowanie w języku bengalskim, chroniące znaki samogłoskowe, ligatury i oryginał oraz rozróżniające bn-BD i bn-IN.", "Zobacz wersję bengalską"),
    "id": ("Tipografi dan desain bahasa Bengali yang menjaga tanda vokal, huruf gabung, dan naskah asli, serta membedakan bn-BD dan bn-IN.", "Lihat edisi bahasa Bengali"),
}
for _lang, _cards in CARDS.items():
    if _lang in BN_CARD_COPY:
        _cards.setdefault("bn", BN_CARD_COPY[_lang])
CARDS["bn"] = {
    "ar": ("ডান থেকে বাঁয়ে লেখা ও মিশ্র লিপি সামলে মূল লেখা অক্ষুণ্ণ রাখা আরবি টাইপোগ্রাফি।", "আরবি সংস্করণ দেখুন"),
    "bn": ("কার-চিহ্ন, যুক্তাক্ষর ও মূল লেখা সুরক্ষিত রেখে bn-BD ও bn-IN-এর পার্থক্য মেনে চলা বাংলা টাইপোগ্রাফি ও ডিজাইন।", "বাংলা সংস্করণ দেখুন"),
    "de": ("দীর্ঘ যৌগিক শব্দ, উদ্ধৃতিচিহ্ন এবং DE/AT/CH-এর ভিন্ন রীতি মেনে মূল লেখা রক্ষা করা জার্মান টাইপোগ্রাফি।", "জার্মান সংস্করণ দেখুন"),
    "es": ("আঞ্চলিক ব্যবহারকে সম্মান করে, মূল লেখা রক্ষা করে এবং যাচাই-করা তথ্যকে সম্পাদকীয় বিচার থেকে আলাদা রাখা স্প্যানিশ টাইপোগ্রাফি।", "স্প্যানিশ সংস্করণ দেখুন"),
    "fr": ("নন-ব্রেকিং স্পেস, উদ্ধৃতিচিহ্ন এবং আঞ্চলিক বা প্রাতিষ্ঠানিক রচনারীতি আলাদা করে দেখা ফরাসি টাইপোগ্রাফি।", "ফরাসি সংস্করণ দেখুন"),
    "hi": ("মূল লেখা, যুক্তাক্ষর ও মাত্রা সুরক্ষিত রাখা হিন্দি টাইপোগ্রাফি ও ডিজাইন।", "হিন্দি সংস্করণ দেখুন"),
    "id": ("অব্যয়, প্রত্যয়, দ্বিরুক্ত শব্দ, যতিচিহ্ন ও রুপিয়ার অঙ্ক প্রসঙ্গ বুঝে সামলানো, মূল লেখা রক্ষা করা ইন্দোনেশীয় টাইপোগ্রাফি।", "ইন্দোনেশীয় সংস্করণ দেখুন"),
    "ja": ("জাপানি লাইন ভাঙার নিয়ম (কিনসোকু) ও স্বাভাবিক লাইন বিরতি থেকে তথ্যের কাঠামো, ফাঁকা জায়গা ও পড়ার প্রবাহ পর্যন্ত।", "জাপানি সংস্করণ দেখুন"),
    "ko": ("এওজল (কোরীয় শব্দ-একক) অনুযায়ী লাইন ভাঙা, লেখার ছন্দ এবং স্পষ্টভাবে বোঝানোর মতো তথ্যের কাঠামো।", "কোরীয় সংস্করণ দেখুন"),
    "pl": ("নির্ভুল বিশেষ চিহ্ন, অর্থপূর্ণ লাইন ভাঙা এবং মূল লেখা রক্ষা করা পোলিশ টাইপোগ্রাফি ও ডিজাইন।", "পোলিশ সংস্করণ দেখুন"),
    "pt": ("ব্রাজিল ও ইউরোপের রীতি এবং লেখকের অভিপ্রায় মেনে চলা পর্তুগিজ টাইপোগ্রাফি ও অর্থনির্ভর ডিজাইন।", "পর্তুগিজ সংস্করণ দেখুন"),
    "th": ("থাই শব্দসীমা ও সংযুক্ত চিহ্ন মেনে স্বাভাবিকভাবে পড়া যায় এমন থাই ডিজাইন।", "থাই সংস্করণ দেখুন"),
    "vi": ("স্বরচিহ্ন, অর্থপূর্ণ লাইন ভাঙা ও মূল বিষয়বস্তু মেনে চলা ভিয়েতনামি টাইপোগ্রাফি।", "ভিয়েতনামি সংস্করণ দেখুন"),
    "zh-hans": ("মূল লেখা না বদলে মূল ভূখণ্ড চীনের যতিচিহ্ন, লাইন ভাঙা ও চীনা-লাতিন মিশ্র লেখা সামলায়।", "সরলীকৃত চীনা সংস্করণ দেখুন"),
    "zh-hant": ("তাইওয়ান ও হংকংয়ের ভিন্ন যতিচিহ্ন ও অক্ষরবিন্যাসের রীতি সামলায়।", "প্রথাগত চীনা সংস্করণ দেখুন"),
}

# Italian (KUMIHAN｜Equilibrio) and Russian (KUMIHAN｜Лад) editions: their card for every
# reader language and each reader's table of all editions.
PRODUCTS["it"] = dict(name="Italiano", lang="it", brand="KUMIHAN｜Equilibrio", glyph="È", label="IT · ITALIAN", version="v0.1.0",
                      pages={"it": "kumihan-it.html", "en": "kumihan-it.en.html", "ja": "kumihan-it.ja.html"})
PRODUCTS["ru"] = dict(name="Русский", lang="ru", brand="KUMIHAN｜Лад", glyph="Ж", label="RU · RUSSIAN", version="v0.1.0",
                      pages={"ru": "kumihan-ru.html", "en": "kumihan-ru.en.html", "ja": "kumihan-ru.ja.html"})
IT_CARD_COPY = {
    "ja": ("アクセント・引用・地域差を尊重し、原稿と意味を守るイタリア語の文字組みとデザイン。", "イタリア語版を見る"),
    "en": ("Italian typography respecting accents, quotations and regional choices while preserving the original.", "View the Italian edition"),
    "zh-hant": ("尊重重音、引號與地區差異，保護原稿的義大利文排版與設計。", "查看義大利文版"),
    "zh-hans": ("尊重重音、引号和地区差异，保护原稿的意大利语排版与设计。", "查看意大利语版"),
    "ko": ("악센트, 인용 부호와 지역 차이를 존중하고 원문을 지키는 이탈리아어 글짜임.", "이탈리아어 버전 보기"),
    "th": ("การจัดวางตัวอักษรอิตาลีที่ใส่ใจเครื่องหมายกำกับ คำอ้างอิงและความต่างระหว่างภูมิภาค โดยรักษาต้นฉบับ", "ดูเวอร์ชันภาษาอิตาลี"),
    "fr": ("Typographie italienne respectant les accents, les citations et les variantes régionales, sans modifier l’original.", "Voir la version italienne"),
    "es": ("Tipografía italiana que respeta acentos, citas y variantes regionales, preservando el original.", "Ver la edición en italiano"),
    "pt": ("Tipografia italiana que respeita acentos, citações e variantes regionais, preservando o original.", "Ver a edição em italiano"),
    "ar": ("تنضيد إيطالي يراعي علامات النبر والاقتباس والاختلافات الإقليمية مع الحفاظ على الأصل.", "عرض النسخة الإيطالية"),
    "hi": ("मूल पाठ सुरक्षित रखते हुए इतालवी उच्चारण चिह्नों, उद्धरणों और क्षेत्रीय भिन्नताओं का ध्यान रखने वाली टाइपोग्राफी।", "इतालवी संस्करण देखें"),
    "vi": ("Thiết kế chữ tiếng Ý tôn trọng dấu, trích dẫn và khác biệt vùng miền, giữ nguyên bản gốc.", "Xem phiên bản tiếng Ý"),
    "de": ("Italienische Typografie, die Akzente, Zitate und regionale Varianten respektiert und das Original bewahrt.", "Italienische Version ansehen"),
    "pl": ("Typografia włoska uwzględniająca akcenty, cytaty i warianty regionalne, chroniąca oryginał.", "Zobacz wersję włoską"),
    "id": ("Tipografi Italia yang menghormati aksen, kutipan, dan variasi regional sambil menjaga naskah asli.", "Lihat edisi bahasa Italia"),
    "bn": ("অ্যাকসেন্ট, উদ্ধৃতি ও আঞ্চলিক ভিন্নতা মেনে মূল লেখা রক্ষা করা ইতালীয় টাইপোগ্রাফি।", "ইতালীয় সংস্করণ দেখুন"),
    "ru": ("Итальянская типографика с вниманием к акцентам, цитатам и региональным вариантам, сохраняющая оригинал.", "Открыть итальянскую версию"),
    "it": ("Tipografia italiana attenta ad accenti, citazioni e varianti regionali, nel rispetto del testo originale.", "Vai all’edizione italiana"),
}
RU_CARD_COPY = {
    "ja": ("ё・й、引用符、ダッシュ、改行を文脈に合わせて扱い、原稿を守るロシア語の文字組みとデザイン。", "ロシア語版を見る"),
    "en": ("Russian typography that handles ё and й, quotation marks, dashes and line breaks in context while preserving the source.", "View the Russian edition"),
    "zh-hant": ("依語境處理 ё 與 й、引號、破折號與換行，並保留原稿的俄文排版與設計。", "前往俄文版"),
    "zh-hans": ("按语境处理 ё 与 й、引号、破折号与换行，并保留原稿的俄语排版与设计。", "前往俄语版"),
    "ko": ("ё와 й, 인용 부호, 대시, 줄바꿈을 맥락에 맞게 다루고 원고를 지키는 러시아어 글짜임.", "러시아어 버전 보기"),
    "th": ("การจัดวางตัวอักษรรัสเซียที่ใส่ใจ ё และ й เครื่องหมายอัญประกาศ ขีดยาว และการตัดบรรทัดตามบริบท โดยรักษาต้นฉบับ", "ดูเวอร์ชันภาษารัสเซีย"),
    "fr": ("Typographie russe qui traite ё et й, les guillemets, les tirets et les retours à la ligne selon le contexte, sans modifier la source.", "Voir l’édition russe"),
    "es": ("Tipografía rusa que trata ё y й, las comillas, las rayas y los saltos de línea según el contexto, sin alterar el original.", "Ver la edición en ruso"),
    "pt": ("Tipografia russa que trata ё e й, aspas, travessões e quebras de linha conforme o contexto, preservando o original.", "Ver a edição em russo"),
    "ar": ("تنضيد روسي يعالج ё وй وعلامات الاقتباس والشرطات وفواصل الأسطر حسب السياق، مع الحفاظ على النص الأصلي.", "عرض النسخة الروسية"),
    "hi": ("ё और й, उद्धरण चिह्नों, डैश और पंक्ति-विभाजन को संदर्भ के अनुसार संभालने वाली, मूल पाठ सुरक्षित रखने वाली रूसी टाइपोग्राफ़ी।", "रूसी संस्करण देखें"),
    "vi": ("Typography tiếng Nga xử lý ё và й, dấu ngoặc kép, gạch ngang và ngắt dòng theo ngữ cảnh, giữ nguyên bản gốc.", "Xem phiên bản tiếng Nga"),
    "de": ("Russische Typografie, die ё und й, Anführungszeichen, Gedankenstriche und Zeilenumbrüche im Kontext behandelt und das Original bewahrt.", "Russische Version ansehen"),
    "pl": ("Typografia rosyjska, która uwzględnia ё i й, cudzysłowy, myślniki i podziały wierszy zależnie od kontekstu, chroniąc oryginał.", "Zobacz wersję rosyjską"),
    "id": ("Tipografi Rusia yang menangani ё dan й, tanda kutip, tanda pisah, dan pergantian baris sesuai konteks sambil menjaga naskah asli.", "Lihat edisi bahasa Rusia"),
    "bn": ("প্রসঙ্গ বুঝে ё ও й, উদ্ধৃতিচিহ্ন, ড্যাশ ও লাইন ভাঙা সামলানো, মূল লেখা রক্ষা করা রুশ টাইপোগ্রাফি।", "রুশ সংস্করণ দেখুন"),
    "it": ("Tipografia russa che tratta ё e й, virgolette, trattini e a capo secondo il contesto, nel rispetto dell’originale.", "Vai all’edizione russa"),
    "ru": ("Русская типографика: ё и й, кавычки, тире и переносы строк с учётом контекста — без изменения оригинала.", "Открыть русскую версию"),
}
CARDS["it"] = {
    "ar": ("Tipografia araba che gestisce la scrittura da destra a sinistra e i testi in più alfabeti, senza alterare l’originale.", "Vai all’edizione araba"),
    "bn": ("Tipografia e design in bengalese che preservano segni vocalici, legature e testo originale, distinguendo bn-BD e bn-IN.", "Vai all’edizione bengalese"),
    "de": ("Tipografia tedesca attenta ai composti lunghi, alle virgolette e alle convenzioni DE/AT/CH, nel rispetto dell’originale.", "Vai all’edizione tedesca"),
    "es": ("Tipografia spagnola che rispetta l’uso regionale, preserva il testo e distingue le prove verificate dal giudizio editoriale.", "Vai all’edizione spagnola"),
    "fr": ("Tipografia francese che distingue spazi indivisibili, virgolette e stili redazionali regionali o istituzionali.", "Vai all’edizione francese"),
    "hi": ("Tipografia e design in hindi che preservano il testo originale, i nessi consonantici e le matra.", "Vai all’edizione hindi"),
    "id": ("Tipografia indonesiana attenta a preposizioni, affissi, raddoppiamenti, punteggiatura e importi in rupie, nel rispetto dell’originale.", "Vai all’edizione indonesiana"),
    "ja": ("Dalle regole giapponesi di a capo (kinsoku) agli a capo naturali, fino a struttura delle informazioni, spazi bianchi e flusso di lettura.", "Vai all’edizione giapponese"),
    "ko": ("A capo tra gli eojeol (unità di spaziatura coreane), ritmo del testo e una struttura delle informazioni chiara.", "Vai all’edizione coreana"),
    "pl": ("Tipografia polacca con diacritici accurati, a capo sensati e un design che preserva il testo originale.", "Vai all’edizione polacca"),
    "pt": ("Tipografia portoghese e design guidato dal significato, nel rispetto delle convenzioni brasiliane ed europee e delle intenzioni dell’autore.", "Vai all’edizione portoghese"),
    "th": ("Rispetta i confini di parola e i caratteri combinanti del thai, per un design che si legge in modo naturale.", "Vai all’edizione thai"),
    "vi": ("Tipografia vietnamita che rispetta i segni tonali, gli a capo sensati e il contenuto originale.", "Vai all’edizione vietnamita"),
    "zh-hans": ("Punteggiatura, a capo e testi misti cinese-latino per la Cina continentale, senza riscrivere l’originale.", "Vai all’edizione in cinese semplificato"),
    "zh-hant": ("Tiene conto delle diverse convenzioni di punteggiatura e composizione di Taiwan e Hong Kong.", "Vai all’edizione in cinese tradizionale"),
}
CARDS["ru"] = {
    "ar": ("Арабская типографика: письмо справа налево и смешение письменностей без изменения оригинала.", "Открыть арабскую версию"),
    "bn": ("Бенгальская типографика и дизайн: огласовки, лигатуры и оригинал под защитой, с различием bn-BD и bn-IN.", "Открыть бенгальскую версию"),
    "de": ("Немецкая типографика: длинные сложные слова, кавычки и нормы DE/AT/CH без изменения оригинала.", "Открыть немецкую версию"),
    "es": ("Испанская типографика: региональные нормы, сохранность текста и разделение проверенных фактов и редакторских решений.", "Открыть испанскую версию"),
    "fr": ("Французская типографика: неразрывные пробелы, кавычки и региональные или институциональные редакционные стили.", "Открыть французскую версию"),
    "hi": ("Типографика и дизайн на хинди с сохранением оригинала, лигатур согласных и матр.", "Открыть версию на хинди"),
    "id": ("Индонезийская типографика: предлоги, аффиксы, повторы, пунктуация и суммы в рупиях с учётом контекста и без изменения оригинала.", "Открыть индонезийскую версию"),
    "ja": ("От японских правил переноса (кинсоку) и естественных разрывов строк до структуры информации, пустого пространства и ритма чтения.", "Открыть японскую версию"),
    "ko": ("Переносы по эоджолям (корейским единицам пробела), ритм текста и ясная структура информации.", "Открыть корейскую версию"),
    "pl": ("Польская типографика: точные диакритические знаки, осмысленные переносы и сохранность оригинала.", "Открыть польскую версию"),
    "pt": ("Португальская типографика и дизайн от смысла с учётом бразильских и европейских норм и замысла автора.", "Открыть португальскую версию"),
    "th": ("Тайская типографика с учётом границ слов и комбинируемых знаков — для естественного чтения.", "Открыть тайскую версию"),
    "vi": ("Вьетнамская типографика: тоновые знаки, осмысленные переносы строк и сохранность оригинала.", "Открыть вьетнамскую версию"),
    "zh-hans": ("Пунктуация, переносы строк и смешанный китайско-латинский текст для материкового Китая без переписывания оригинала.", "Открыть версию на упрощённом китайском"),
    "zh-hant": ("Учитывает различия в пунктуации и наборе Тайваня и Гонконга.", "Открыть версию на традиционном китайском"),
}
for _lang, _cards in CARDS.items():
    _cards.setdefault("it", IT_CARD_COPY[_lang])
    _cards.setdefault("ru", RU_CARD_COPY[_lang])

# Swahili edition (KUMIHAN｜Mizani): its card for every reader language and the Swahili
# reader's table of all editions.
SW_CARD_COPY = {
    "ja": ("ng’とアポストロフィ、長い語を守り、sw-TZ・sw-KE・sw-CDの書式を明示して選ぶスワヒリ語の文字組みとデザイン。", "スワヒリ語版を見る"),
    "en": ("Swahili typography protecting ng’, original wording and regional formatting choices.", "View the Swahili edition"),
    "zh-hant": ("保護 ng’ 與撇號、尊重長詞，並明確選擇 sw-TZ／sw-KE／sw-CD 格式的史瓦希利文排版與設計。", "前往史瓦希利文版"),
    "zh-hans": ("保护 ng’ 与撇号、尊重长词，并明确选择 sw-TZ／sw-KE／sw-CD 格式的斯瓦希里语排版与设计。", "前往斯瓦希里语版"),
    "ko": ("ng’와 아포스트로피, 긴 단어를 지키고 sw-TZ·sw-KE·sw-CD 서식을 명시적으로 고르는 스와힐리어 글짜임.", "스와힐리어 버전 보기"),
    "th": ("การจัดวางตัวอักษรสวาฮีลีที่รักษา ng’ และอะพอสทรอฟี เคารพคำยาว และเลือกรูปแบบ sw-TZ sw-KE หรือ sw-CD อย่างชัดเจน", "ดูเวอร์ชันภาษาสวาฮีลี"),
    "fr": ("Typographie swahilie qui protège ng’ et les apostrophes, respecte les mots longs et choisit explicitement les formats sw-TZ, sw-KE ou sw-CD.", "Voir l’édition swahilie"),
    "es": ("Tipografía suajili que protege ng’ y los apóstrofos, respeta las palabras largas y elige de forma explícita los formatos sw-TZ, sw-KE o sw-CD.", "Ver la edición en suajili"),
    "pt": ("Tipografia suaíli que protege ng’ e os apóstrofos, respeita palavras longas e escolhe explicitamente os formatos sw-TZ, sw-KE ou sw-CD.", "Ver a edição em suaíli"),
    "ar": ("تنضيد سواحيلي يحمي ng’ والفواصل العليا ويراعي الكلمات الطويلة ويختار صراحةً تنسيقات sw-TZ أو sw-KE أو sw-CD.", "عرض النسخة السواحيلية"),
    "hi": ("ng’ और एपॉस्ट्रॉफ़ी को सुरक्षित रखने वाली, लंबे शब्दों का ध्यान रखने वाली और sw-TZ, sw-KE या sw-CD प्रारूप स्पष्ट रूप से चुनने वाली स्वाहिली टाइपोग्राफ़ी।", "स्वाहिली संस्करण देखें"),
    "vi": ("Typography tiếng Swahili bảo vệ ng’ và dấu nháy, tôn trọng từ dài và chọn rõ định dạng sw-TZ, sw-KE hoặc sw-CD.", "Xem phiên bản tiếng Swahili"),
    "de": ("Suaheli-Typografie, die ng’ und Apostrophe schützt, lange Wörter respektiert und die Formate sw-TZ, sw-KE oder sw-CD ausdrücklich wählt.", "Suaheli-Version ansehen"),
    "pl": ("Typografia suahili chroniąca ng’ i apostrofy, szanująca długie wyrazy i wyraźnie wybierająca formaty sw-TZ, sw-KE lub sw-CD.", "Zobacz wersję suahili"),
    "id": ("Tipografi Swahili yang menjaga ng’ dan apostrof, menghormati kata panjang, serta memilih format sw-TZ, sw-KE, atau sw-CD secara eksplisit.", "Lihat edisi bahasa Swahili"),
    "bn": ("ng’ ও অ্যাপোস্ট্রফি রক্ষা করে, দীর্ঘ শব্দ মেনে এবং sw-TZ, sw-KE বা sw-CD বিন্যাস স্পষ্টভাবে বেছে নেওয়া সোয়াহিলি টাইপোগ্রাফি।", "সোয়াহিলি সংস্করণ দেখুন"),
    "it": ("Tipografia swahili che protegge ng’ e gli apostrofi, rispetta le parole lunghe e sceglie esplicitamente i formati sw-TZ, sw-KE o sw-CD.", "Vai all’edizione swahili"),
    "ru": ("Типографика суахили: защита ng’ и апострофов, внимание к длинным словам и явный выбор форматов sw-TZ, sw-KE или sw-CD.", "Открыть версию на суахили"),
}
CARDS["sw"] = {
    "ar": ("Uchapaji wa Kiarabu unaoshughulikia maandishi ya kulia kwenda kushoto na mchanganyiko wa hati, bila kubadilisha maandishi asilia.", "Tazama toleo la Kiarabu"),
    "bn": ("Uchapaji na usanifu wa Kibengali unaolinda alama za irabu, herufi ambatani na maandishi asilia, ukitofautisha bn-BD na bn-IN.", "Tazama toleo la Kibengali"),
    "de": ("Uchapaji wa Kijerumani unaozingatia maneno marefu ambatani, alama za nukuu na tofauti za DE/AT/CH, ukihifadhi maandishi asilia.", "Tazama toleo la Kijerumani"),
    "es": ("Uchapaji wa Kihispania unaoheshimu matumizi ya kimaeneo, kuhifadhi maandishi asilia na kutenganisha ushahidi uliothibitishwa na maamuzi ya kihariri.", "Tazama toleo la Kihispania"),
    "fr": ("Uchapaji wa Kifaransa unaotofautisha nafasi zisizokatika, alama za nukuu na mitindo ya uhariri ya kimaeneo au ya kitaasisi.", "Tazama toleo la Kifaransa"),
    "hi": ("Uchapaji na usanifu wa Kihindi unaolinda maandishi asilia, herufi ambatani na alama za irabu (matra).", "Tazama toleo la Kihindi"),
    "id": ("Uchapaji wa Kiindonesia unaozingatia vihusishi, viambishi, maneno yanayorudiwa, uakifishaji na kiasi cha rupia kulingana na muktadha, ukihifadhi maandishi asilia.", "Tazama toleo la Kiindonesia"),
    "it": ("Uchapaji wa Kiitaliano unaozingatia lafudhi, nukuu na tofauti za kimaeneo, ukihifadhi maandishi asilia.", "Tazama toleo la Kiitaliano"),
    "ja": ("Kuanzia kanuni za Kijapani za kukata mistari (kinsoku) na mikato ya kawaida ya mistari hadi muundo wa taarifa, nafasi tupu na mtiririko wa usomaji.", "Tazama toleo la Kijapani"),
    "ko": ("Mikato ya mistari kati ya eojeol (vipashio vya nafasi vya Kikorea), mdundo wa maandishi na muundo wa taarifa ulio wazi.", "Tazama toleo la Kikorea"),
    "pl": ("Uchapaji wa Kipolandi wenye alama sahihi za herufi, mikato yenye maana na usanifu unaohifadhi maandishi asilia.", "Tazama toleo la Kipolandi"),
    "pt": ("Uchapaji wa Kireno na usanifu unaoongozwa na maana, ukiheshimu desturi za Brazili na Ulaya pamoja na nia ya mwandishi.", "Tazama toleo la Kireno"),
    "ru": ("Uchapaji wa Kirusi unaoshughulikia ё na й, alama za nukuu, vistari na mikato ya mistari kulingana na muktadha, ukihifadhi maandishi asilia.", "Tazama toleo la Kirusi"),
    "sw": ("Uchapaji wa Kiswahili unaolinda ng’ na alama za ritifaa, unaoheshimu maneno marefu na kuchagua waziwazi miundo ya sw-TZ, sw-KE au sw-CD.", "Tazama toleo la Kiswahili"),
    "th": ("Kuheshimu mipaka ya maneno ya Kithai na herufi ambatanishi, kwa usanifu wa Kithai unaosomeka kwa urahisi.", "Tazama toleo la Kithai"),
    "vi": ("Uchapaji wa Kivietinamu unaoheshimu alama za toni, mikato yenye maana ya mistari na maudhui asilia.", "Tazama toleo la Kivietinamu"),
    "zh-hans": ("Uakifishaji, mikato ya mistari na maandishi mchanganyiko ya Kichina na Kilatini kwa China Bara, bila kuandika upya maandishi asilia.", "Tazama toleo la Kichina Kilichorahisishwa"),
    "zh-hant": ("Hushughulikia desturi tofauti za uakifishaji na upangaji wa herufi za Taiwan na Hong Kong.", "Tazama toleo la Kichina cha Jadi"),
}
for _lang, _cards in CARDS.items():
    if "sw" not in _cards:
        _cards["sw"] = SW_CARD_COPY[_lang]

# isiZulu edition (KUMIHAN｜Hlela): its card for every reader language.
ZU_CARD_COPY = {
    "ja": ("接合語と語中の大文字（isiZulu など）を守り、原稿を変えずに組むズールー語の文字組みとデザイン。", "ズールー語版を見る"),
    "en": ("isiZulu typography that protects conjunctive words and internal capitals, keeping the source intact.", "View the isiZulu edition"),
    "zh-hant": ("保護黏著詞與詞中大寫（如 isiZulu），不改動原稿的祖魯文排版與設計。", "前往祖魯文版"),
    "zh-hans": ("保护黏着词与词中大写（如 isiZulu），不改动原稿的祖鲁语排版与设计。", "前往祖鲁语版"),
    "ko": ("결합어와 단어 안의 대문자(isiZulu 등)를 지키고 원고를 바꾸지 않는 줄루어 글짜임.", "줄루어 버전 보기"),
    "th": ("การจัดวางตัวอักษรภาษาซูลูที่รักษาคำเชื่อมและตัวพิมพ์ใหญ่กลางคำ (เช่น isiZulu) โดยไม่เปลี่ยนต้นฉบับ", "ดูเวอร์ชันภาษาซูลู"),
    "fr": ("Typographie zouloue qui protège les mots agglutinés et les majuscules internes (isiZulu), sans modifier la source.", "Voir l’édition zouloue"),
    "es": ("Tipografía zulú que protege las palabras aglutinadas y las mayúsculas internas (isiZulu) sin alterar el original.", "Ver la edición en zulú"),
    "pt": ("Tipografia zulu que protege palavras aglutinadas e maiúsculas internas (isiZulu), preservando o original.", "Ver a edição em zulu"),
    "ar": ("تنضيد زولو يحمي الكلمات الملتصقة والأحرف الكبيرة داخل الكلمة (مثل isiZulu) دون تغيير النص الأصلي.", "عرض نسخة الزولو"),
    "hi": ("संयोजी शब्दों और शब्द के भीतर बड़े अक्षरों (जैसे isiZulu) को सुरक्षित रखने वाली, मूल पाठ न बदलने वाली ज़ुलु टाइपोग्राफ़ी।", "ज़ुलु संस्करण देखें"),
    "vi": ("Typography tiếng Zulu giữ nguyên từ ghép dính liền và chữ hoa giữa từ (như isiZulu), không thay đổi bản gốc.", "Xem phiên bản tiếng Zulu"),
    "de": ("Zulu-Typografie, die zusammengeschriebene Wörter und Großbuchstaben im Wortinneren (isiZulu) schützt und das Original bewahrt.", "Zulu-Version ansehen"),
    "pl": ("Typografia zulu chroniąca wyrazy łączne i wielkie litery wewnątrz słów (isiZulu), bez zmiany oryginału.", "Zobacz wersję zulu"),
    "id": ("Tipografi Zulu yang menjaga kata gabung dan huruf kapital di tengah kata (seperti isiZulu) tanpa mengubah naskah asli.", "Lihat edisi bahasa Zulu"),
    "bn": ("সংযুক্ত শব্দ ও শব্দের মাঝের বড় হাতের অক্ষর (যেমন isiZulu) রক্ষা করে, মূল লেখা না বদলানো জুলু টাইপোগ্রাফি।", "জুলু সংস্করণ দেখুন"),
    "it": ("Tipografia zulu che protegge le parole agglutinate e le maiuscole interne (isiZulu), nel rispetto dell’originale.", "Vai all’edizione zulu"),
    "ru": ("Типографика зулу: слитные слова и заглавные буквы внутри слова (isiZulu) без изменения оригинала.", "Открыть версию на зулу"),
    "sw": ("Uchapaji wa Kizulu unaolinda maneno yaliyounganishwa na herufi kubwa ndani ya neno (kama isiZulu) bila kubadilisha maandishi asilia.", "Tazama toleo la Kizulu"),
}
CARDS["zu"] = {
    "ar": ("Ukuhlelwa kombhalo kwesi-Arabic osuka kwesokudla uye kwesobunxele nokuxutshwa kwemibhalo, ngaphandle kokushintsha umbhalo wokuqala.", "Buka isi-Arabic"),
    "bn": ("Ukuhlelwa kombhalo nedizayini yesi-Bengali evikela izimpawu zonkamisa, izinhlamvu ezihlanganisiwe nombhalo wokuqala, ihlukanise i-bn-BD ne-bn-IN.", "Buka isi-Bengali"),
    "de": ("Ukuhlelwa kombhalo kwesi-German okuhlonipha amagama amade ahlanganisiwe, izimpawu zokucaphuna nemithetho ye-DE/AT/CH, kugcine umbhalo wokuqala.", "Buka isi-German"),
    "es": ("Ukuhlelwa kombhalo kwesi-Spanish okuhlonipha ukusetshenziswa kwezifunda, kugcine umbhalo wokuqala futhi kuhlukanise ubufakazi obuqinisekisiwe nezinqumo zokuhlela.", "Buka isi-Spanish"),
    "fr": ("Ukuhlelwa kombhalo kwesi-French okuhlukanisa izikhala ezingahlukani, izimpawu zokucaphuna nezitayela zokuhlela zezifunda noma zezikhungo.", "Buka isi-French"),
    "hi": ("Ukuhlelwa kombhalo nedizayini yesi-Hindi evikela umbhalo wokuqala, ongwaqa abahlanganisiwe nezimpawu zonkamisa (matra).", "Buka isi-Hindi"),
    "id": ("Ukuhlelwa kombhalo kwesi-Indonesian okunaka izandiso, iziqalo, amagama aphindwayo, izimpawu zokubhala nezimali ze-rupiah ngokomongo, kugcine umbhalo wokuqala.", "Buka isi-Indonesian"),
    "it": ("Ukuhlelwa kombhalo kwesi-Italian okunaka izimpawu zokuphimisa, izingcaphuno nokwehluka kwezifunda, kugcine umbhalo wokuqala.", "Buka isi-Italian"),
    "ja": ("Kusukela emithethweni yesi-Japanese yokwehlukanisa imigqa (kinsoku) nokwehlukaniswa kwemigqa okungokwemvelo kuya esakhiweni solwazi, isikhala esingenalutho nokugeleza kokufunda.", "Buka isi-Japanese"),
    "ko": ("Ukwehlukaniswa kwemigqa phakathi kwama-eojeol (amayunithi esikhala esi-Korean), isigqi sombhalo nesakhiwo solwazi esicacile.", "Buka isi-Korean"),
    "pl": ("Ukuhlelwa kombhalo kwesi-Polish okunezimpawu ezinembile, ukwehlukaniswa kwemigqa okunomqondo nedizayini egcina umbhalo wokuqala.", "Buka isi-Polish"),
    "pt": ("Ukuhlelwa kombhalo kwesi-Portuguese nedizayini eqondiswa yincazelo, kuhlonipha imithetho yaseBrazil neYurophu kanye nenhloso yombhali.", "Buka isi-Portuguese"),
    "ru": ("Ukuhlelwa kombhalo kwesi-Russian okuphatha u-ё no-й, izimpawu zokucaphuna, amadeshi nokwehlukaniswa kwemigqa ngokomongo, kugcine umbhalo wokuqala.", "Buka isi-Russian"),
    "sw": ("Ukuhlelwa kombhalo kwesiSwahili okuvikela u-ng’ nama-apostrophe, kuhlonipha amagama amade futhi kukhethe ngokucacile amafomethi e-sw-TZ, sw-KE noma sw-CD.", "Buka isiSwahili"),
    "th": ("Ukuhlonipha imingcele yamagama yesi-Thai nezinhlamvu ezihlanganayo, ukuze idizayini yesi-Thai ifundeke kalula.", "Buka isi-Thai"),
    "vi": ("Ukuhlelwa kombhalo kwesi-Vietnamese okuhlonipha izimpawu zethoni, ukwehlukaniswa kwemigqa okunomqondo nokuqukethwe kwangempela.", "Buka isi-Vietnamese"),
    "zh-hans": ("Izimpawu zokubhala, ukwehlukaniswa kwemigqa nombhalo oxubile wesi-Chinese nesiLatini wase-China, ngaphandle kokubhala kabusha umbhalo wokuqala.", "Buka isi-Chinese (esenziwe-lula)"),
    "zh-hant": ("Kuphatha imithetho ehlukile yezimpawu zokubhala nokuhlelwa kombhalo yase-Taiwan nase-Hong Kong.", "Buka isi-Chinese (Sasendulo)"),
    "zu": ("Ukuhlelwa kombhalo kwesiZulu okuvikela amagama ahlanganisiwe nezinhlamvu ezinkulu ngaphakathi kwegama, kugcine umbhalo wokuqala.", "Buka isiZulu"),
}
for _lang, _cards in CARDS.items():
    if _lang != "zu":
        _cards["zu"] = ZU_CARD_COPY[_lang]

# Polish readers: one-letter words (a, i, o, u, w, z) stay with the next word (kumihan-szyk-web).
_PL_ONE_LETTER = re.compile(r"(?<![\w/=-])([AaIiOoUuWwZz]) (?=\S)")
CARDS["pl"] = {code: tuple(_PL_ONE_LETTER.sub("\\1\u00a0", s) for s in pair) for code, pair in CARDS["pl"].items()}




# Language-edition names in each page language, for the edition menu (CLDR names, first letter
# capitalized; adjusted to the names used on the cards).
EDITION_NAMES = {
    "ar": {"ar": "العربية", "bn": "البنغالية", "de": "الألمانية", "es": "الإسبانية", "fr": "الفرنسية", "hi": "الهندية", "id": "الإندونيسية", "it": "الإيطالية", "ja": "اليابانية", "ko": "الكورية", "pl": "البولندية", "pt": "البرتغالية", "ru": "الروسية", "th": "التايلاندية", "vi": "الفيتنامية", "zh-hans": "الصينية المبسطة", "zh-hant": "الصينية التقليدية"},
    "bn": {"ar": "আরবি", "bn": "বাংলা", "de": "জার্মান", "es": "স্প্যানিশ", "fr": "ফরাসি", "hi": "হিন্দি", "id": "ইন্দোনেশীয়", "it": "ইতালীয়", "ja": "জাপানি", "ko": "কোরীয়", "pl": "পোলিশ", "pt": "পর্তুগিজ", "ru": "রুশ", "th": "থাই", "vi": "ভিয়েতনামি", "zh-hans": "সরলীকৃত চীনা", "zh-hant": "প্রথাগত চীনা"},
    "de": {"ar": "Arabisch", "bn": "Bengalisch", "de": "Deutsch", "es": "Spanisch", "fr": "Französisch", "hi": "Hindi", "id": "Indonesisch", "it": "Italienisch", "ja": "Japanisch", "ko": "Koreanisch", "pl": "Polnisch", "pt": "Portugiesisch", "ru": "Russisch", "th": "Thailändisch", "vi": "Vietnamesisch", "zh-hans": "Chinesisch (vereinfacht)", "zh-hant": "Chinesisch (traditionell)"},
    "en": {"ar": "Arabic", "bn": "Bangla", "de": "German", "es": "Spanish", "fr": "French", "hi": "Hindi", "id": "Indonesian", "it": "Italian", "ja": "Japanese", "ko": "Korean", "pl": "Polish", "pt": "Portuguese", "ru": "Russian", "th": "Thai", "vi": "Vietnamese", "zh-hans": "Simplified Chinese", "zh-hant": "Traditional Chinese"},
    "es": {"ar": "Árabe", "bn": "Bengalí", "de": "Alemán", "es": "Español", "fr": "Francés", "hi": "Hindi", "id": "Indonesio", "it": "Italiano", "ja": "Japonés", "ko": "Coreano", "pl": "Polaco", "pt": "Portugués", "ru": "Ruso", "th": "Tailandés", "vi": "Vietnamita", "zh-hans": "Chino simplificado", "zh-hant": "Chino tradicional"},
    "fr": {"ar": "Arabe", "bn": "Bengali", "de": "Allemand", "es": "Espagnol", "fr": "Français", "hi": "Hindi", "id": "Indonésien", "it": "Italien", "ja": "Japonais", "ko": "Coréen", "pl": "Polonais", "pt": "Portugais", "ru": "Russe", "th": "Thaï", "vi": "Vietnamien", "zh-hans": "Chinois simplifié", "zh-hant": "Chinois traditionnel"},
    "hi": {"ar": "अरबी", "bn": "बंगाली", "de": "जर्मन", "es": "स्पेनिश", "fr": "फ़्रेंच", "hi": "हिंदी", "id": "इंडोनेशियाई", "it": "इतालवी", "ja": "जापानी", "ko": "कोरियाई", "pl": "पोलिश", "pt": "पुर्तगाली", "ru": "रूसी", "th": "थाई", "vi": "वियतनामी", "zh-hans": "सरलीकृत चीनी", "zh-hant": "पारंपरिक चीनी"},
    "id": {"ar": "Arab", "bn": "Bengali", "de": "Jerman", "es": "Spanyol", "fr": "Prancis", "hi": "Hindi", "id": "Indonesia", "it": "Italia", "ja": "Jepang", "ko": "Korea", "pl": "Polandia", "pt": "Portugis", "ru": "Rusia", "th": "Thai", "vi": "Vietnam", "zh-hans": "Tionghoa Sederhana", "zh-hant": "Tionghoa Tradisional"},
    "it": {"ar": "Arabo", "bn": "Bengalese", "de": "Tedesco", "es": "Spagnolo", "fr": "Francese", "hi": "Hindi", "id": "Indonesiano", "it": "Italiano", "ja": "Giapponese", "ko": "Coreano", "pl": "Polacco", "pt": "Portoghese", "ru": "Russo", "th": "Thailandese", "vi": "Vietnamita", "zh-hans": "Cinese semplificato", "zh-hant": "Cinese tradizionale"},
    "ja": {"ar": "アラビア語", "bn": "ベンガル語", "de": "ドイツ語", "es": "スペイン語", "fr": "フランス語", "hi": "ヒンディー語", "id": "インドネシア語", "it": "イタリア語", "ja": "日本語", "ko": "韓国語", "pl": "ポーランド語", "pt": "ポルトガル語", "ru": "ロシア語", "th": "タイ語", "vi": "ベトナム語", "zh-hans": "簡体中国語", "zh-hant": "繁体中国語"},
    "ko": {"ar": "아랍어", "bn": "벵골어", "de": "독일어", "es": "스페인어", "fr": "프랑스어", "hi": "힌디어", "id": "인도네시아어", "it": "이탈리아어", "ja": "일본어", "ko": "한국어", "pl": "폴란드어", "pt": "포르투갈어", "ru": "러시아어", "th": "태국어", "vi": "베트남어", "zh-hans": "중국어(간체)", "zh-hant": "중국어(번체)"},
    "pl": {"ar": "Arabski", "bn": "Bengalski", "de": "Niemiecki", "es": "Hiszpański", "fr": "Francuski", "hi": "Hindi", "id": "Indonezyjski", "it": "Włoski", "ja": "Japoński", "ko": "Koreański", "pl": "Polski", "pt": "Portugalski", "ru": "Rosyjski", "th": "Tajski", "vi": "Wietnamski", "zh-hans": "Chiński uproszczony", "zh-hant": "Chiński tradycyjny"},
    "pt": {"ar": "Árabe", "bn": "Bengali", "de": "Alemão", "es": "Espanhol", "fr": "Francês", "hi": "Híndi", "id": "Indonésio", "it": "Italiano", "ja": "Japonês", "ko": "Coreano", "pl": "Polonês", "pt": "Português", "ru": "Russo", "th": "Tailandês", "vi": "Vietnamita", "zh-hans": "Chinês simplificado", "zh-hant": "Chinês tradicional"},
    "ru": {"ar": "Арабский", "bn": "Бенгальский", "de": "Немецкий", "es": "Испанский", "fr": "Французский", "hi": "Хинди", "id": "Индонезийский", "it": "Итальянский", "ja": "Японский", "ko": "Корейский", "pl": "Польский", "pt": "Португальский", "ru": "Русский", "th": "Тайский", "vi": "Вьетнамский", "zh-hans": "Китайский (упрощённый)", "zh-hant": "Китайский (традиционный)"},
    "th": {"ar": "อาหรับ", "bn": "เบงกาลี", "de": "เยอรมัน", "es": "สเปน", "fr": "ฝรั่งเศส", "hi": "ฮินดี", "id": "อินโดนีเซีย", "it": "อิตาลี", "ja": "ญี่ปุ่น", "ko": "เกาหลี", "pl": "โปแลนด์", "pt": "โปรตุเกส", "ru": "รัสเซีย", "th": "ไทย", "vi": "เวียดนาม", "zh-hans": "จีนตัวย่อ", "zh-hant": "จีนตัวเต็ม"},
    "vi": {"ar": "Tiếng Ả Rập", "bn": "Tiếng Bengal", "de": "Tiếng Đức", "es": "Tiếng Tây Ban Nha", "fr": "Tiếng Pháp", "hi": "Tiếng Hindi", "id": "Tiếng Indonesia", "it": "Tiếng Ý", "ja": "Tiếng Nhật", "ko": "Tiếng Hàn", "pl": "Tiếng Ba Lan", "pt": "Tiếng Bồ Đào Nha", "ru": "Tiếng Nga", "th": "Tiếng Thái", "vi": "Tiếng Việt", "zh-hans": "Tiếng Trung (Giản thể)", "zh-hant": "Tiếng Trung (Phồn thể)"},
    "zh-hans": {"ar": "阿拉伯语", "bn": "孟加拉语", "de": "德语", "es": "西班牙语", "fr": "法语", "hi": "印地语", "id": "印度尼西亚语", "it": "意大利语", "ja": "日语", "ko": "韩语", "pl": "波兰语", "pt": "葡萄牙语", "ru": "俄语", "th": "泰语", "vi": "越南语", "zh-hans": "简体中文", "zh-hant": "繁体中文"},
    "zh-hant": {"ar": "阿拉伯文", "bn": "孟加拉文", "de": "德文", "es": "西班牙文", "fr": "法文", "hi": "印地文", "id": "印尼文", "it": "義大利文", "ja": "日文", "ko": "韓文", "pl": "波蘭文", "pt": "葡萄牙文", "ru": "俄文", "th": "泰文", "vi": "越南文", "zh-hans": "簡體中文", "zh-hant": "繁體中文"},
}
# Placeholder of the edition menu, in each page language.
PICK = {"zu": "Khetha ulimi", "sw": "Chagua lugha", "ja": "言語を選ぶ", "en": "Choose a language", "ar": "اختر لغة", "bn": "ভাষা বেছে নিন", "de": "Sprache wählen", "es": "Elige un idioma", "fr": "Choisir une langue", "hi": "भाषा चुनें", "id": "Pilih bahasa", "it": "Scegli una lingua", "ko": "언어 선택", "pl": "Wybierz język", "pt": "Escolha uma língua", "ru": "Выберите язык", "th": "เลือกภาษา", "vi": "Chọn ngôn ngữ", "zh-hans": "选择语言", "zh-hant": "選擇語言"}

def css_version():
    """Short content hash of the stylesheet, so a new page never meets a cached old stylesheet."""
    return hashlib.sha256((ROOT / "assets" / "gateway.css").read_bytes()).hexdigest()[:10]


def x(value):
    return escape(str(value), quote=True)


def menu(key):
    others = sorted(k for k in GATEWAYS if k not in (key, "en"))
    order = [key] + (["en"] if key != "en" else []) + others
    file, _, code, name = GATEWAYS[key]
    lang_attr = lambda k: GATEWAYS[k][1].split("-")[0] if GATEWAYS[k][1] in ("ko-KR", "th-TH") else GATEWAYS[k][1]
    items = "".join(
        f'<li><a href="{GATEWAYS[k][0]}" hreflang="{GATEWAYS[k][1]}"' + (' aria-current="page"' if k == key else "")
        + f'><span class="code">{GATEWAYS[k][2]}</span> - <span lang="{lang_attr(k)}">{x(GATEWAYS[k][3])}</span></a></li>'
        for k in order)
    return (f'<details class="lang-menu"><summary aria-label="{x(UI[key]["menu"])}: {code} - {x(name)}">'
            f'<span>{code} - <span lang="{lang_attr(key)}">{x(name)}</span></span></summary><ul>{items}</ul></details>')


# Mizani: append the new edition name in each existing gateway language.
EDITION_NAMES["sw"] = {"ar": "Kiarabu", "bn": "Kibengali", "de": "Kijerumani", "es": "Kihispania", "fr": "Kifaransa", "hi": "Kihindi", "id": "Kiindonesia", "it": "Kiitaliano", "ja": "Kijapani", "ko": "Kikorea", "pl": "Kipolandi", "pt": "Kireno", "ru": "Kirusi", "th": "Kithai", "vi": "Kivietinamu", "zh-hans": "Kichina Kilichorahisishwa", "zh-hant": "Kichina cha Jadi"}
_SW_EDITION_NAMES = {"sw":"Kiswahili","ar":"السواحيلية","bn":"সোয়াহিলি","de":"Suaheli","en":"Swahili","es":"Suajili","fr":"Swahili","hi":"स्वाहिली","id":"Swahili","it":"Swahili","ja":"スワヒリ語","ko":"스와힐리어","pl":"Suahili","pt":"Suaíli","ru":"Суахили","th":"ภาษาสวาฮีลี","vi":"Tiếng Swahili","zh-hans":"斯瓦希里语","zh-hant":"史瓦希利語"}
for _lang, _names in EDITION_NAMES.items():
    _names["sw"] = _SW_EDITION_NAMES[_lang]


EDITION_NAMES["zu"] = {"ar": "isi-Arabic", "bn": "isi-Bengali", "de": "isi-German", "es": "isi-Spanish", "fr": "isi-French", "hi": "isi-Hindi", "id": "isi-Indonesian", "it": "isi-Italian", "ja": "isi-Japanese", "ko": "isi-Korean", "pl": "isi-Polish", "pt": "isi-Portuguese", "ru": "isi-Russian", "sw": "isiSwahili", "th": "isi-Thai", "vi": "isi-Vietnamese", "zh-hans": "isi-Chinese (esenziwe-lula)", "zh-hant": "isi-Chinese (Sasendulo)"}
_ZU_EDITION_NAMES = {"zu":"isiZulu","sw":"Kizulu","ar":"الزولو","bn":"জুলু","de":"Zulu","en":"isiZulu","es":"Zulú","fr":"Zoulou","hi":"ज़ुलू","id":"Zulu","it":"Zulu","ja":"ズールー語","ko":"줄루어","pl":"Zuluski","pt":"Zulu","ru":"Зулу","th":"ภาษาซูลู","vi":"Tiếng Zulu","zh-hans":"祖鲁语","zh-hant":"祖魯語"}
for _lang, _names in EDITION_NAMES.items():
    _names["zu"] = _ZU_EDITION_NAMES[_lang]


# Khmer edition (KUMIHAN｜លំនឹង): registry, the Khmer top, its card for every reader
# language and the Khmer reader's table of all editions; names from CLDR.
GATEWAYS["km"] = ("top-km.html", "km", "KM", "ភាសាខ្មែរ")
PRODUCTS["km"] = dict(name="ភាសាខ្មែរ", lang="km", brand="KUMIHAN｜លំនឹង",
    glyph="ក", label="KM · KHMER", version="v0.1.0",
    pages={"km":"kumihan-km.html","en":"kumihan-km.en.html","ja":"kumihan-km.ja.html"})
UI["km"] = dict(heading="កំណែភាសារបស់ KUMIHAN", more="បង្ហាញ {n} បន្ថែម", menu="ភាសា")
PICK["km"] = "ជ្រើសភាសា"
_KM_EDITION_NAMES = {
    'ar': 'الخميرية',
    'bn': 'খমের',
    'de': 'Khmer',
    'en': 'Khmer',
    'es': 'Jemer',
    'fr': 'Khmer',
    'hi': 'खमेर',
    'id': 'Khmer',
    'it': 'Khmer',
    'ja': 'クメール語',
    'ko': '크메르어',
    'pl': 'Khmerski',
    'pt': 'Khmer',
    'ru': 'Кхмерский',
    'sw': 'Kikambodia',
    'th': 'เขมร',
    'vi': 'Tiếng Khmer',
    'zh-hans': '高棉语',
    'zh-hant': '高棉文',
    'zu': 'isi-Khmer',
}
for _reader, _names in EDITION_NAMES.items():
    _names["km"] = _KM_EDITION_NAMES[_reader]
EDITION_NAMES["km"] = {
    'ar': 'អារ៉ាប់',
    'bn': 'បង់ក្លាដែស',
    'de': 'អាល្លឺម៉ង់',
    'es': 'អេស្ប៉ាញ',
    'fr': 'បារាំង',
    'hi': 'ហិណ្ឌី',
    'id': 'ឥណ្ឌូណេស៊ី',
    'it': 'អ៊ីតាលី',
    'ja': 'ជប៉ុន',
    'ko': 'កូរ៉េ',
    'pl': 'ប៉ូឡូញ',
    'pt': 'ព័រទុយហ្គាល់',
    'ru': 'រុស្ស៊ី',
    'sw': 'ស្វាហ៊ីលី',
    'th': 'ថៃ',
    'vi': 'វៀតណាម',
    'zh-hans': 'ចិន\u200bអក្សរ\u200bកាត់',
    'zh-hant': 'ចិន\u200bអក្សរ\u200bពេញ',
    'zu': 'ហ្សូលូ',
    'km': 'ខ្មែរ',
}
_KM_DESC = {
    'ar': 'ការរៀបចំអក្សរអារ៉ាប់ ដែលគ្រប់គ្រងការសរសេរពីស្ដាំទៅឆ្វេង និងការលាយអក្សរច្រើនប្រភេទ ដោយមិនកែប្រែអត្ថបទដើម។',
    'bn': 'ការរៀបចំអក្សរ និងការរចនាបង់ក្លាដែស ដែលរក្សាសញ្ញាស្រៈ អក្សរផ្សំ និងអត្ថបទដើម ហើយបែងចែក bn-BD និង bn-IN។',
    'de': 'ការរៀបចំអក្សរអាល្លឺម៉ង់ ដែលគោរពពាក្យផ្សំវែងៗ សញ្ញាសម្រង់ និងវិធាន DE/AT/CH ដោយរក្សាអត្ថបទដើម។',
    'es': 'ការរៀបចំអក្សរអេស្ប៉ាញ ដែលគោរពការប្រើប្រាស់តាមតំបន់ រក្សាអត្ថបទដើម និងបែងចែកភស្តុតាងដែលបានផ្ទៀងផ្ទាត់ពីការសម្រេចចិត្តផ្នែកនិពន្ធ។',
    'fr': 'ការរៀបចំអក្សរបារាំង ដែលបែងចែកដកឃ្លាមិនបំបែក សញ្ញាសម្រង់ និងរចនាប័ទ្មនិពន្ធតាមតំបន់ ឬស្ថាប័ន។',
    'hi': 'ការរៀបចំអក្សរ និងការរចនាហិណ្ឌី ដែលរក្សាអត្ថបទដើម អក្សរផ្សំ និងសញ្ញាស្រៈ (matra)។',
    'id': 'ការរៀបចំអក្សរឥណ្ឌូណេស៊ី ដែលយកចិត្តទុកដាក់លើធ្នាក់ បុព្វបទ ពាក្យស្ទួន វណ្ណយុត្តិ និងចំនួនទឹកប្រាក់រូពី តាមបរិបទ ដោយរក្សាអត្ថបទដើម។',
    'it': 'ការរៀបចំអក្សរអ៊ីតាលី ដែលយកចិត្តទុកដាក់លើសញ្ញាសំឡេង ការដកស្រង់ និងភាពខុសគ្នាតាមតំបន់ ដោយរក្សាអត្ថបទដើម។',
    'ja': 'ចាប់ពីវិធានបំបែកបន្ទាត់ជប៉ុន (kinsoku) និងការចុះបន្ទាត់ធម្មជាតិ រហូតដល់រចនាសម្ព័ន្ធព័ត៌មាន ចន្លោះទទេ និងលំហូរនៃការអាន។',
    'ko': 'ការបំបែកបន្ទាត់រវាង eojeol (ឯកតាដកឃ្លាកូរ៉េ) ចង្វាក់អត្ថបទ និងរចនាសម្ព័ន្ធព័ត៌មានដែលច្បាស់លាស់។',
    'pl': 'ការរៀបចំអក្សរប៉ូឡូញ ដែលមានសញ្ញាអក្សរត្រឹមត្រូវ ការចុះបន្ទាត់មានន័យ និងការរចនាដែលរក្សាអត្ថបទដើម។',
    'pt': 'ការរៀបចំអក្សរ និងការរចនាព័រទុយហ្គាល់តាមអត្ថន័យ ដែលគោរពវិធានប្រេស៊ីល និងអឺរ៉ុប ព្រមទាំងបំណងរបស់អ្នកនិពន្ធ។',
    'ru': 'ការរៀបចំអក្សររុស្ស៊ី ដែលគ្រប់គ្រង ё និង й សញ្ញាសម្រង់ សញ្ញាដាច់ និងការចុះបន្ទាត់តាមបរិបទ ដោយរក្សាអត្ថបទដើម។',
    'sw': 'ការរៀបចំអក្សរស្វាហ៊ីលី ដែលរក្សា ng’ និងសញ្ញាអាប៉ូស្ត្រូហ្វ គោរពពាក្យវែងៗ និងជ្រើសទម្រង់ sw-TZ, sw-KE ឬ sw-CD ឲ្យច្បាស់លាស់។',
    'th': 'គោរពព្រំដែនពាក្យថៃ និងតួអក្សរផ្សំ ដើម្បីឲ្យការរចនាថៃអានបានដោយធម្មជាតិ។',
    'vi': 'ការរៀបចំអក្សរវៀតណាម ដែលគោរពសញ្ញាសំនៀង ការចុះបន្ទាត់មានន័យ និងខ្លឹមសារដើម។',
    'zh-hans': 'វណ្ណយុត្តិ ការចុះបន្ទាត់ និងអត្ថបទលាយចិន-ឡាតាំងសម្រាប់ចិនដីគោក ដោយមិនសរសេរអត្ថបទដើមឡើងវិញ។',
    'zh-hant': 'គ្រប់គ្រងវិធានវណ្ណយុត្តិ និងការរៀបចំអក្សរខុសៗគ្នារបស់តៃវ៉ាន់ និងហុងកុង។',
    'zu': 'ការរៀបចំអក្សរហ្សូលូ ដែលរក្សាពាក្យភ្ជាប់ និងអក្សរធំនៅកណ្ដាលពាក្យ (ដូចជា isiZulu) ដោយរក្សាអត្ថបទដើម។',
    'km': 'ការរៀបចំអក្សរខ្មែរ ដោយរក្សាអក្សរផ្សំ ការបំបែកបន្ទាត់ និងអត្ថបទដើម។',
}
CARDS["km"] = {code: (text, "មើលកំណែ" + EDITION_NAMES["km"][code]) for code, text in _KM_DESC.items()}
KM_CARD_COPY = {
    'ja': ('結合文字・語のまとまり・原稿を守るクメール語の文字組みとデザイン。', 'クメール語版を見る'),
    'en': ('Khmer typography protecting conjuncts, source text and purposeful line breaks.', 'View the Khmer edition'),
    'zh-hant': ('保護疊寫子音、詞的完整與原稿，並依語意換行的高棉文排版與設計。', '前往高棉文版'),
    'zh-hans': ('保护叠写辅音、词的完整与原稿，并按语意换行的高棉语排版与设计。', '前往高棉语版'),
    'ko': ('결합 자음과 원고를 지키고 의미에 맞게 줄을 바꾸는 크메르어 글짜임.', '크메르어 버전 보기'),
    'th': ('การจัดวางตัวอักษรเขมรที่รักษาพยัญชนะซ้อน ต้นฉบับ และการตัดบรรทัดตามความหมาย', 'ดูเวอร์ชันภาษาเขมร'),
    'fr': ('Typographie khmère qui protège les consonnes souscrites, le texte source et des retours à la ligne réfléchis.', 'Voir l’édition khmère'),
    'es': ('Tipografía jemer que protege las consonantes subíndices, el original y los saltos de línea con sentido.', 'Ver la edición en jemer'),
    'pt': ('Tipografia khmer que protege as consoantes subscritas, o original e quebras de linha com sentido.', 'Ver a edição em khmer'),
    'ar': ('تنضيد خميري يحمي الحروف المركّبة والنص الأصلي وفواصل الأسطر ذات المعنى.', 'عرض النسخة الخميرية'),
    'hi': ('संयुक्त व्यंजनों, मूल पाठ और अर्थपूर्ण पंक्ति-विभाजन को सुरक्षित रखने वाली ख्मेर टाइपोग्राफ़ी।', 'ख्मेर संस्करण देखें'),
    'vi': ('Typography tiếng Khmer giữ nguyên phụ âm chồng, bản gốc và ngắt dòng có chủ đích.', 'Xem phiên bản tiếng Khmer'),
    'de': ('Khmer-Typografie, die Konsonantenligaturen, das Original und sinnvolle Zeilenumbrüche bewahrt.', 'Khmer-Version ansehen'),
    'pl': ('Typografia khmerska chroniąca spółgłoski podpisane, oryginał i przemyślane podziały wierszy.', 'Zobacz wersję khmerską'),
    'id': ('Tipografi Khmer yang menjaga konsonan bertumpuk, naskah asli, dan pergantian baris yang bermakna.', 'Lihat edisi bahasa Khmer'),
    'bn': ('যুক্তব্যঞ্জন, মূল লেখা ও অর্থপূর্ণ লাইন ভাঙা রক্ষা করা খমের টাইপোগ্রাফি।', 'খমের সংস্করণ দেখুন'),
    'it': ('Tipografia khmer che protegge le consonanti sottoscritte, il testo originale e gli a capo ragionati.', 'Vai all’edizione khmer'),
    'ru': ('Кхмерская типографика: подстрочные согласные, сохранность оригинала и осмысленные переносы строк.', 'Открыть кхмерскую версию'),
    'sw': ('Uchapaji wa Kikambodia unaolinda konsonanti zilizopangwa chini, maandishi asilia na mikato ya mistari yenye maana.', 'Tazama toleo la Kikambodia'),
    'zu': ('Ukuhlelwa kombhalo kwesi-Khmer okuvikela ongwaqa abahlanganisiwe, umbhalo wokuqala nokwehlukaniswa kwemigqa okunomqondo.', 'Buka isi-Khmer'),
}
for _reader, _cards in CARDS.items():
    if _reader != "km":
        _cards["km"] = KM_CARD_COPY[_reader]
CARDS["pl"] = {code: tuple(_PL_ONE_LETTER.sub("\\1\u00a0", s) for s in pair) for code, pair in CARDS["pl"].items()}


# Persian edition (KUMIHAN｜تراز): the Persian top, its card and name for every reader language.
PRODUCTS["fa"] = dict(name="فارسی", lang="fa", brand="KUMIHAN｜تراز", glyph="ژ", label="FA · PERSIAN", version="v0.1.0",
                      pages={"fa": "kumihan-fa.html", "en": "kumihan-fa.en.html", "ja": "kumihan-fa.ja.html"})
GATEWAYS["fa"] = ("top-fa.html", "fa", "FA", "فارسی")
UI["fa"] = dict(heading="نسخه‌های زبانی KUMIHAN", more="نمایش {n} مورد بعدی", menu="زبان")
PICK["fa"] = "انتخاب زبان"
EDITION_NAMES["fa"] = {
    'ar': 'عربی',
    'bn': 'بنگالی',
    'de': 'آلمانی',
    'es': 'اسپانیایی',
    'fr': 'فرانسوی',
    'hi': 'هندی',
    'id': 'اندونزیایی',
    'it': 'ایتالیایی',
    'ja': 'ژاپنی',
    'ko': 'کره\u200cای',
    'pl': 'لهستانی',
    'pt': 'پرتغالی',
    'ru': 'روسی',
    'sw': 'سواحیلی',
    'th': 'تایلندی',
    'vi': 'ویتنامی',
    'zh-hans': 'چینی ساده\u200cشده',
    'zh-hant': 'چینی سنتی',
    'zu': 'زولویی',
    'km': 'خمری',
    'fa': 'فارسی',
}
_FA_DESC = {
    'ar': 'حروف\u200cچینی عربی که نوشتار راست\u200cبه\u200cچپ و آمیختگی خط\u200cها را مدیریت می\u200cکند، بی\u200cآنکه متن اصلی تغییر کند.',
    'bn': 'حروف\u200cچینی و طراحی بنگالی که نشانه\u200cهای مصوت، حروف ترکیبی و متن اصلی را حفظ می\u200cکند و bn-BD و bn-IN را از هم جدا می\u200cداند.',
    'de': 'حروف\u200cچینی آلمانی که واژه\u200cهای مرکب بلند، گیومه\u200cها و قواعد DE/AT/CH را رعایت می\u200cکند و متن اصلی را نگه می\u200cدارد.',
    'es': 'حروف\u200cچینی اسپانیایی که کاربرد منطقه\u200cای را محترم می\u200cشمارد، متن اصلی را حفظ می\u200cکند و شواهد تأییدشده را از داوری ویرایشی جدا می\u200cکند.',
    'fr': 'حروف\u200cچینی فرانسوی که فاصله\u200cهای نشکن، گیومه\u200cها و سبک\u200cهای ویرایشی منطقه\u200cای یا سازمانی را از هم تمیز می\u200cدهد.',
    'hi': 'حروف\u200cچینی و طراحی هندی که متن اصلی، هم\u200cخوان\u200cهای ترکیبی و نشانه\u200cهای مصوت (ماترا) را حفظ می\u200cکند.',
    'id': 'حروف\u200cچینی اندونزیایی که حروف اضافه، وندها، واژه\u200cهای تکراری، نشانه\u200cگذاری و مبالغ روپیه را بر پایهٔ بافت در نظر می\u200cگیرد و متن اصلی را حفظ می\u200cکند.',
    'it': 'حروف\u200cچینی ایتالیایی که به نشانه\u200cهای تکیه، نقل\u200cقول\u200cها و تفاوت\u200cهای منطقه\u200cای توجه دارد و متن اصلی را حفظ می\u200cکند.',
    'ja': 'از قواعد ژاپنی شکستن سطر (کینسوکو) و سطربندی طبیعی تا ساختار اطلاعات، فضای خالی و جریان خواندن.',
    'ko': 'شکستن سطر میان اوجول\u200cها (واحدهای فاصله\u200cگذاری کره\u200cای)، ریتم متن و ساختار روشن اطلاعات.',
    'pl': 'حروف\u200cچینی لهستانی با نشانه\u200cهای دقیق، شکستن سطر معنادار و طراحی\u200cای که متن اصلی را حفظ می\u200cکند.',
    'pt': 'حروف\u200cچینی پرتغالی و طراحی معنامحور که قراردادهای برزیلی و اروپایی و نیت نویسنده را رعایت می\u200cکند.',
    'ru': 'حروف\u200cچینی روسی که ё و й، گیومه\u200cها، خط تیره\u200cها و شکستن سطرها را بر پایهٔ بافت مدیریت می\u200cکند و متن اصلی را حفظ می\u200cکند.',
    'sw': 'حروف\u200cچینی سواحیلی که ng’ و آپوستروف\u200cها را حفظ می\u200cکند، واژه\u200cهای بلند را رعایت می\u200cکند و قالب\u200cهای sw-TZ، sw-KE یا sw-CD را آشکارا برمی\u200cگزیند.',
    'th': 'رعایت مرز واژه\u200cها و نویسه\u200cهای ترکیبی تایلندی، برای طراحی تایلندی\u200cای که روان خوانده شود.',
    'vi': 'حروف\u200cچینی ویتنامی که نشانه\u200cهای آهنگ، شکستن سطر معنادار و محتوای اصلی را رعایت می\u200cکند.',
    'zh-hans': 'نشانه\u200cگذاری، شکستن سطر و متن آمیختهٔ چینی و لاتین برای چین اصلی، بی\u200cآنکه متن اصلی بازنویسی شود.',
    'zh-hant': 'قراردادهای متفاوت نشانه\u200cگذاری و حروف\u200cچینی تایوان و هنگ\u200cکنگ را در نظر می\u200cگیرد.',
    'zu': 'حروف\u200cچینی زولو که واژه\u200cهای پیوسته و حروف بزرگ میان واژه (مانند isiZulu) را حفظ می\u200cکند و متن اصلی را نگه می\u200cدارد.',
    'km': 'حروف\u200cچینی خمری که هم\u200cخوان\u200cهای زیرنویس، متن اصلی و شکستن سطر معنادار را حفظ می\u200cکند.',
    'fa': 'حروف\u200cچینی فارسی که جهت راست\u200cبه\u200cچپ را روشن نگه می\u200cدارد، نیم\u200cفاصله (ZWNJ) را حفظ می\u200cکند و نشانی\u200cها و شمارهٔ نسخه\u200cهای لاتین را جدا می\u200cکند.',
}
CARDS["fa"] = {code: (text, "دیدن نسخهٔ " + EDITION_NAMES["fa"][code]) for code, text in _FA_DESC.items()}
_FA_EDITION_NAMES = {
    'ar': 'الفارسية',
    'bn': 'ফার্সি',
    'de': 'Persisch',
    'en': 'Persian',
    'es': 'Persa',
    'fr': 'Persan',
    'hi': 'फ़ारसी',
    'id': 'Persia',
    'it': 'Persiano',
    'ja': 'ペルシア語',
    'ko': '페르시아어',
    'pl': 'Perski',
    'pt': 'Persa',
    'ru': 'Персидский',
    'sw': 'Kiajemi',
    'th': 'เปอร์เซีย',
    'vi': 'Tiếng Ba Tư',
    'zh-hans': '波斯语',
    'zh-hant': '波斯文',
    'zu': 'isi-Persian',
    'km': 'ភឺសៀន',
}
for _reader, _names in EDITION_NAMES.items():
    if _reader != "fa":
        _names["fa"] = _FA_EDITION_NAMES[_reader]
FA_CARD_COPY = {
    'ja': ('右から左の方向とZWNJ（ゼロ幅非接合子）を守り、ラテン文字のURLや版番号を正しく分離するペルシア語の文字組みとデザイン。', 'ペルシア語版を見る'),
    'en': ('Persian typography that keeps right-to-left direction clear, preserves ZWNJ and isolates Latin URLs and version labels.', 'View the Persian edition'),
    'zh-hant': ('保持由右至左的方向、保留 ZWNJ，並正確隔離拉丁網址與版本號的波斯文排版與設計。', '前往波斯文版'),
    'zh-hans': ('保持从右到左的方向、保留 ZWNJ，并正确隔离拉丁网址与版本号的波斯语排版与设计。', '前往波斯语版'),
    'ko': ('오른쪽에서 왼쪽 방향과 ZWNJ를 지키고 라틴 URL과 버전 표기를 바르게 분리하는 페르시아어 글짜임.', '페르시아어 버전 보기'),
    'th': ('การจัดวางตัวอักษรเปอร์เซียที่รักษาทิศทางจากขวาไปซ้ายและ ZWNJ พร้อมแยก URL ภาษาละตินและเลขเวอร์ชันอย่างถูกต้อง', 'ดูเวอร์ชันภาษาเปอร์เซีย'),
    'fr': ('Typographie persane qui garde clair le sens de droite à gauche, préserve le ZWNJ et isole les URL et numéros de version latins.', 'Voir l’édition persane'),
    'es': ('Tipografía persa que mantiene clara la dirección de derecha a izquierda, conserva el ZWNJ y aísla URL y versiones latinas.', 'Ver la edición en persa'),
    'pt': ('Tipografia persa que mantém clara a direção da direita para a esquerda, preserva o ZWNJ e isola URLs e versões latinas.', 'Ver a edição em persa'),
    'ar': ('تنضيد فارسي يحافظ على اتجاه الكتابة من اليمين إلى اليسار وعلى ZWNJ، ويعزل الروابط وأرقام الإصدارات اللاتينية.', 'عرض النسخة الفارسية'),
    'hi': ('दाएँ से बाएँ दिशा और ZWNJ को सुरक्षित रखने वाली, लैटिन URL और संस्करण संख्याओं को सही ढंग से अलग करने वाली फ़ारसी टाइपोग्राफ़ी।', 'फ़ारसी संस्करण देखें'),
    'vi': ('Typography tiếng Ba Tư giữ rõ hướng phải sang trái, bảo toàn ZWNJ và tách riêng URL, số phiên bản Latinh.', 'Xem phiên bản tiếng Ba Tư'),
    'de': ('Persische Typografie, die die Schreibrichtung von rechts nach links klar hält, ZWNJ bewahrt und lateinische URLs und Versionsangaben isoliert.', 'Persische Version ansehen'),
    'pl': ('Typografia perska zachowująca kierunek od prawej do lewej i ZWNJ oraz poprawnie wydzielająca łacińskie adresy URL i numery wersji.', 'Zobacz wersję perską'),
    'id': ('Tipografi Persia yang menjaga arah kanan ke kiri, mempertahankan ZWNJ, serta memisahkan URL dan nomor versi Latin dengan tepat.', 'Lihat edisi bahasa Persia'),
    'bn': ('ডান থেকে বাঁ দিক ও ZWNJ রক্ষা করে এবং লাতিন URL ও সংস্করণ নম্বর ঠিকভাবে আলাদা রাখা ফারসি টাইপোগ্রাফি।', 'ফারসি সংস্করণ দেখুন'),
    'it': ('Tipografia persiana che mantiene chiara la direzione da destra a sinistra, preserva lo ZWNJ e isola URL e numeri di versione latini.', 'Vai all’edizione persiana'),
    'ru': ('Персидская типографика: направление справа налево, сохранение ZWNJ и изоляция латинских URL и номеров версий.', 'Открыть персидскую версию'),
    'sw': ('Uchapaji wa Kiajemi unaodumisha mwelekeo wa kulia kwenda kushoto, kuhifadhi ZWNJ na kutenganisha URL na nambari za matoleo za Kilatini.', 'Tazama toleo la Kiajemi'),
    'zu': ('Ukuhlelwa kombhalo kwesi-Persian okugcina isiqondiso sokusuka kwesokudla kuya kwesobunxele, kugcine i-ZWNJ futhi kuhlukanise ama-URL nezinombolo zezinguqulo zesiLatini.', 'Buka isi-Persian'),
    'km': ('ការរៀបចំអក្សរពែរ្ស ដែលរក្សាទិសដៅពីស្ដាំទៅឆ្វេង និង ZWNJ ហើយញែក URL និងលេខកំណែឡាតាំងឲ្យត្រឹមត្រូវ។', 'មើលកំណែភឺសៀន'),
}
for _reader, _cards in CARDS.items():
    if _reader != "fa":
        _cards["fa"] = FA_CARD_COPY[_reader]
CARDS["pl"] = {code: tuple(_PL_ONE_LETTER.sub("\\1\u00a0", s) for s in pair) for code, pair in CARDS["pl"].items()}



def edition_menu(key):
    """Language-edition menu under the section title: the page's language first, then by code."""
    order = ([key] if key in PRODUCTS else []) + sorted(c for c in PRODUCTS if c != key)
    items = "".join(
        f'<li><a href="{PRODUCTS[c]["pages"].get(key) or PRODUCTS[c]["pages"]["en"]}"'
        + (' class="current"' if c == key else "")
        + f'><span class="code">{c.upper()}</span> - {x(EDITION_NAMES[key][c])}</a></li>'
        for c in order)
    return (f'<details class="lang-menu edition-menu"><summary>{x(PICK[key])}</summary>'
            f'<ul>{items}</ul></details>')


def marquee():
    codes = sorted(PRODUCTS)
    half = (len(codes) + 1) // 2
    rows = [codes[:half], codes[half:]]

    def glyph(code):
        p = PRODUCTS[code]
        return (f'<div class="glyph"><span class="character" lang="{p["lang"]}">{p["glyph"]}</span>'
                f'<span class="glyph-label">{p["label"]}</span></div>')
    out = ""
    for i, row in enumerate(rows):
        cells = "".join(glyph(c) for c in row)
        out += f'<div class="glyph-row{" reverse" if i else ""}" style="--duration:{30 + 6 * i}s">{cells}{cells}</div>'
    return f'<div aria-hidden="true" class="glyph-marquee">{out}</div>'


def cards(key):
    order = ([key] if key in PRODUCTS else []) + sorted(c for c in PRODUCTS if c != key)
    out = ""
    for i, code in enumerate(order):
        p = PRODUCTS[code]
        desc, action = CARDS[key][code]
        href = p["pages"].get(key) or p["pages"].get("en") or next(iter(p["pages"].values()))
        direction = ' dir="rtl"' if code in ("ar", "fa") else ""
        current = code == key
        out += (f'<article class="lang-card{" current" if current else ""}" aria-labelledby="language-{code}"'
                + (" data-extra" if i >= VISIBLE else "") + ">"
                f'<div class="lang-card-head"><span class="lang-index">{code.upper()}</span><span class="state">{x(p["version"])}</span></div>'
                f'<h3 class="lang-title" id="language-{code}" lang="{p["lang"]}"{direction}>{x(p["name"])}</h3>'
                f'<p class="lang-sub"><bdi dir="ltr">{x(p["brand"])}</bdi></p>'
                f'<p class="lang-desc">{x(desc)}</p>'
                f'<a class="lang-action" href="{href}"><span>{x(action)}</span><span aria-hidden="true" class="action-arrow">↗</span></a>'
                "</article>\n")
    return out, len(order)


SCRIPT = """<script>
(() => {
  'use strict';
  const grid = document.querySelector('.language-grid');
  const button = document.querySelector('.more-languages');
  if (!grid || !button) return;
  const step = %d;
  const extra = () => [...grid.querySelectorAll('[data-extra][hidden]')];
  grid.querySelectorAll('[data-extra]').forEach(card => { card.hidden = true; });
  const update = () => {
    const rest = extra().length;
    button.parentElement.hidden = rest === 0;
    button.textContent = button.dataset.label.replace('{n}', Math.min(step, rest));
  };
  button.addEventListener('click', () => {
    const shown = extra().slice(0, step);
    shown.forEach(card => { card.hidden = false; });
    update();
    if (shown[0]) shown[0].querySelector('a').focus();
  });
  update();
  document.querySelectorAll('.lang-menu').forEach(menu => {
    document.addEventListener('click', event => { if (!menu.contains(event.target)) menu.open = false; });
    menu.addEventListener('keydown', event => { if (event.key === 'Escape') { menu.open = false; menu.querySelector('summary').focus(); } });
  });
})();
</script>""" % STEP


def page(key, c):
    file, html_lang, _, _ = GATEWAYS[key]
    alternates = "".join(f'<link href="{f}" hreflang="{l}" rel="alternate"/>' for k, (f, l, _, _) in GATEWAYS.items())
    alternates += '<link href="index.html" hreflang="x-default" rel="alternate"/>'
    card_html, count = cards(key)
    more = (f'<div class="more-row"><button type="button" class="more-languages" data-label="{x(UI[key]["more"])}">'
            f'{x(UI[key]["more"].replace("{n}", str(min(STEP, count - VISIBLE))))}</button></div>' if count > VISIBLE else "")
    return f"""<!doctype html>
<html lang="{html_lang}"{' dir="rtl"' if key in RTL else ""}>
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<meta content="#f4f1e9" name="theme-color"/>
<meta content="{x(c['description'])}" name="description"/>
<title>{c['title']}</title>
<link href="assets/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="assets/gateway.css?v={css_version()}" rel="stylesheet"/>
{alternates}<link href="{BASE}{file}" rel="canonical"/>
{WEB_FONTS.head(html_lang)}

</head>
<body>
<a class="skip-link" href="#main">{c['skip']}</a>
<header class="site-header">
<div class="shell header-inner">
<a aria-label="KUMIHAN" class="brand" href="{file}">
<img alt="" height="56" src="assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png" width="56"/>
<span><span class="brand-word">KUMIHAN</span><span class="brand-caption">LANGUAGE &amp; DESIGN</span></span>
</a>
<div class="header-side"><span aria-hidden="true" class="red-line"></span><span>LANGUAGE GATEWAY<br/>CONCEPT / 01</span></div>
<nav aria-label="{x(c['nav_label'])}">{menu(key)}</nav>
</div>
</header>
<main id="main">
<section aria-labelledby="page-title" class="intro">
<div class="shell intro-grid">
<div>
<p class="eyebrow">{c['eyebrow']}</p>
<h1 id="page-title">{c['h1']}</h1>
<p class="intro-lead">{c['lead']}</p>
<div class="intro-actions">
<a class="primary-action" href="#languages"><span>{c['primary']}</span><span aria-hidden="true">↘</span></a>
<a class="minor-action" href="#about">{c['minor']}</a>
</div>
</div>
<div aria-label="{x(c['art_label'])}" class="type-art">
<div class="type-art-top"><span>SCRIPT STUDIES / EDITIONS</span><strong>KUMIHAN / TYPE</strong></div>
{marquee()}
<div class="art-bottom"><span>KUMIHAN / TYPE STUDIES</span><span>LANGUAGE BY LANGUAGE</span></div>
</div>
</div>
</section>
<section aria-labelledby="language-title" class="language-section" id="languages">
<div class="shell">
<div class="section-heading">
<div><p class="eyebrow">CHOOSE YOUR LANGUAGE</p><h2 id="language-title">{x(UI[key]['heading'])}</h2>{edition_menu(key)}</div>
<p class="section-note">{c['section_note']}</p>
</div>
<div class="language-grid">
{card_html}</div>
{more}
</div>
</section>
{c['about']}
</main>
{FOOTER.footer(html_lang, '', sys.modules[__name__])}
{SCRIPT}
</body>
</html>
"""


# Former gateway addresses, kept so existing links still arrive: old file -> current page.
REDIRECTS = {"top-en.html": "index.html"}


def redirect(target):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>KUMIHAN</title>
<meta content="noindex" name="robots"/>
<link href="{BASE}{target}" rel="canonical"/>
<meta content="0; url={target}" http-equiv="refresh"/>
</head>
<body><p><a href="{target}">KUMIHAN</a></p></body>
</html>
"""


@seo_outputs
def outputs():
    copy = json.loads((ROOT / "assets" / "gateway-copy.json").read_text(encoding="utf-8"))
    files = {GATEWAYS[k][0]: WEB_FONTS.SHARE.apply(page(k, copy[k])) for k in GATEWAYS}
    files.update({old: redirect(new) for old, new in REDIRECTS.items()})
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for name, content in outputs().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale gateway pages: " + ", ".join(stale))
    print(f"Gateway: {len(GATEWAYS)} pages " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
