#!/usr/bin/env python3
"""Build the KUMIHAN language gateway (index.html, top-*.html); --check verifies.

Page copy that already existed lives in assets/gateway-copy.json; shared styles
in assets/gateway.css. Language order everywhere is by language code, with
the page's own language first (and English second in the language menu).
"""
import argparse
import json
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)
BASE = "https://landco-llc.github.io/kumihan/"
VISIBLE, STEP = 9, 6

# Gateway pages: key -> (file, html lang, menu label, native name)
GATEWAYS = {
    "ar": ("top-ar.html", "ar", "AR", "العربية"),
    "en": ("top-en.html", "en", "EN", "English"),
    "es": ("top-es.html", "es", "ES", "Español"),
    "fr": ("top-fr.html", "fr", "FR", "Français"),
    "hi": ("top-hi.html", "hi", "HI", "हिंदी"),
    "ja": ("index.html", "ja", "JA", "日本語"),
    "ko": ("top-ko.html", "ko-KR", "KO", "한국어"),
    "pt": ("top-pt.html", "pt", "PT", "Português"),
    "th": ("top-th.html", "th-TH", "TH", "ไทย"),
    "vi": ("top-vi.html", "vi", "VI", "Tiếng Việt"),
    "zh-hans": ("top-zh-cn.html", "zh-Hans-CN", "ZH-HANS", "简体中文"),
    "zh-hant": ("top-zh-han.html", "zh-Hant-TW", "ZH-HANT", "繁體中文"),
}

# Language editions: code -> data. "pages" maps a reader language to the
# edition page in that language; the first entry is the edition's own page.
PRODUCTS = {
    "de": dict(name="Deutsch", lang="de", brand="KUMIHAN｜Satzbild", glyph="Ä", label="DE · GERMAN", version="v0.1.0", pages={"de":"kumihan-de.html", "en":"kumihan-de.en.html", "ja":"kumihan-de.ja.html"}),
    "hi": dict(name="हिंदी", lang="hi", brand="KUMIHAN｜अक्षर-संगति", glyph="अ", label="HI · HINDI", version="v0.1.0", pages={"hi":"kumihan-hi.html", "en":"kumihan-hi.en.html", "ja":"kumihan-hi.ja.html"}),
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
RTL = {"ar"}

# Card text per gateway language: code -> (description, action label)
CARDS = {
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
        direction = ' dir="rtl"' if code == "ar" else ""
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
<link href="assets/gateway.css" rel="stylesheet"/>
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
<div><p class="eyebrow">CHOOSE YOUR LANGUAGE</p><h2 id="language-title">{x(UI[key]['heading'])}</h2></div>
<p class="section-note">{c['section_note']}</p>
</div>
<div class="language-grid">
{card_html}</div>
{more}
</div>
</section>
{c['about']}
</main>
{c['footer']}
{SCRIPT}
</body>
</html>
"""


def outputs():
    copy = json.loads((ROOT / "assets" / "gateway-copy.json").read_text(encoding="utf-8"))
    return {GATEWAYS[k][0]: page(k, copy[k]) for k in GATEWAYS}


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
