#!/usr/bin/env python3
"""Собирает 6 сайтов из data/raw/*.json. Запуск: python3 build.py"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
RAW = ROOT / "data" / "raw"
e = html.escape

CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 var(--fb);-webkit-text-size-adjust:100%}
a{color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.hero{background:var(--hbg);color:var(--hink);padding:64px 0 48px}
.hero h1{font:700 clamp(2.4rem,7vw,4.6rem)/1.02 var(--fh);margin:.2em 0 .3em;letter-spacing:-.01em}
.cat{margin:0;opacity:.8;font-size:.95rem}
.lead{max-width:34em;font-size:1.2rem;margin:0 0 1.6em}
.cta{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;padding:14px 22px;border-radius:var(--r);background:var(--accent);color:var(--aink);font-weight:700;text-decoration:none}
.btn.alt{background:transparent;color:inherit;border:2px solid currentColor}
.score{display:flex;flex-wrap:wrap;gap:6px 22px;margin-top:2em;align-items:baseline}
.score b{font:700 2.6rem/1 var(--fh)}
section{padding:52px 0;border-bottom:1px solid var(--line)}
h2{font:700 clamp(1.6rem,4vw,2.2rem)/1.15 var(--fh);margin:0 0 .8em}
dl.prices{margin:0}
.row{display:grid;grid-template-columns:1fr auto;gap:4px 24px;padding:16px 0;border-top:1px solid var(--line)}
.row:last-child{border-bottom:1px solid var(--line)}
.row dt{font-weight:700}.row dd{margin:0}
.row .d{grid-column:1;color:var(--mute);max-width:38em;font-size:.97rem}
.row .p{grid-row:1;grid-column:2;font:700 1.3rem var(--fh);white-space:nowrap;text-align:right}
.promo{background:var(--accent);color:var(--aink);padding:14px 18px;border-radius:var(--r);font-weight:700;margin:0 0 1.2em}
.chips{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none;margin:0}
.chips li{background:var(--panel);border:1px solid var(--line);padding:6px 12px;border-radius:var(--r);font-size:.92rem}
.aspects{display:grid;gap:12px;margin:0 0 2em;padding:0;list-style:none}
.aspects li{display:grid;grid-template-columns:minmax(120px,200px) 1fr auto;gap:14px;align-items:center;font-size:.95rem}
.bar{height:10px;background:var(--line);border-radius:99px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--accent)}
.aspects small{color:var(--mute)}
blockquote{margin:0 0 18px;padding:16px 20px;background:var(--panel);border-left:5px solid var(--accent);border-radius:0 var(--r) var(--r) 0;max-width:46em}
blockquote footer{margin-top:8px;color:var(--mute);font-size:.9rem}
.note{color:var(--mute);font-size:.92rem;max-width:46em}
.contacts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:28px}
.contacts h3{margin:0 0 .3em;font:700 1.05rem var(--fb)}
.contacts p{margin:0 0 .3em}
footer.site{padding:28px 0 48px;color:var(--mute);font-size:.88rem}
@media(max-width:560px){.aspects li{grid-template-columns:1fr auto}.aspects .bar{grid-column:1/-1;grid-row:2}.row{grid-template-columns:1fr}.row .p{grid-row:auto;grid-column:1;text-align:left}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

PHOTOS = {
 "lida-drive-plus": "https://avatars.mds.yandex.net/get-altay/16634215/2a00000198fbffdbf388baf7f14404493c77/L_height",
 "avtomasters": "https://avatars.mds.yandex.net/get-tycoon/17969377/2a0000019a06de3ba079703ef6df36ac2929/priority-headline-background",
 "yudzhin-avto": "https://avatars.mds.yandex.net/get-tycoon/18019403/2a000001a1f2b13c10c55b357220d7b7ab98/priority-headline-background",
 "detroyt": "https://avatars.mds.yandex.net/get-altay/4398559/2a000001875c2a3341cb310177a13c73aa99/L_height",
 "kvn": "https://avatars.mds.yandex.net/get-altay/15223968/2a000001975f559c095c66862691a618ce92/L_height",
 "interavto": "https://avatars.mds.yandex.net/get-altay/11300692/2a0000019159b4f9216632f167c550519e34/L_height",
}

EXTRA = """
.top{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 20px}
.top b{font:700 1.1rem var(--fh)}.top .btn{padding:9px 16px}
.glass{background:color-mix(in srgb,var(--hbg) 62%,transparent);-webkit-backdrop-filter:blur(16px) saturate(1.3);backdrop-filter:blur(16px) saturate(1.3);border:1px solid rgba(255,255,255,.22);color:var(--hink)}
.hero,.band{position:relative;overflow:hidden;isolation:isolate}
.hero::before,.band::before{content:"";position:absolute;inset:-60px;z-index:-2;background:var(--photo) center/cover no-repeat,radial-gradient(circle at 15% 25%,var(--accent),transparent 45%),radial-gradient(circle at 85% 70%,color-mix(in srgb,var(--accent) 55%,var(--hbg)),transparent 50%),var(--hbg);filter:blur(26px) saturate(1.2)}
.hero::after,.band::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,color-mix(in srgb,var(--hbg) 50%,transparent),color-mix(in srgb,var(--hbg) 82%,transparent))}
.hero{padding:72px 0 64px}
.hgrid{display:flex;flex-wrap:wrap;gap:36px;align-items:center}.htext{flex:1 1 420px}
.shot{flex:0 1 400px;margin:0;border-radius:calc(var(--r)*3);overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.3)}
.shot img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.score{display:inline-flex;padding:14px 20px;border-radius:calc(var(--r)*2);background:rgba(255,255,255,.12);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.22)}
.band{padding:80px 0;border:0}.band .card{max-width:560px;padding:32px;border-radius:calc(var(--r)*3)}.band h2{margin-top:0}
section{border-bottom:0}
.row{background:var(--panel);padding:16px 20px;border:1px solid var(--line);border-radius:calc(var(--r)*2);margin-bottom:10px}.row:last-child{border-bottom:1px solid var(--line)}
"""

DATA = [
 dict(slug="lida-drive-plus", name="Лида драйв плюс", category="Гостиница", city="Лида",
  address="Лида, пер. Фомичёва, 1", phone="+375 44 555-56-32", phone_note="Бронирование гостиничных номеров",
  rating="5,0", rating_count=476, reviews_count=155, hours="Круглосуточно",
  lead="Гостиница в Лиде: номер от 75 бел.руб. за ночь, парковка, кондиционер в номере и баня на дровах для гостей.",
  cta="Забронировать номер", links=[["Instagram", "https://www.instagram.com/sport_club_lida_drive_plus/"]],
  prices=[["Баня", "Для гостей отеля: русская баня на дровах, бассейн, терраса, зона барбекю", "150 Br за 2 ч"],
          ["Завтраки (по договорённости)", "Организация завтраков по предварительному запросу гостей отеля.", "32 Br за 1 шт."],
          ["Проживание с кошкой или собакой", "Сообщить о питомце нужно строго до бронирования.", "20 Br за 1 шт."]],
  promo="", features=["Парковка", "Кондиционер в номере", "Оплата картой", "Номер от 75 бел.руб. за ночь"], works=[],
  aspects=[["Персонал", 98, 42], ["Территория", 100, 17], ["Интерьер", 100, 15], ["Еда", 94, 37], ["Расположение", 94, 19],
           ["Атмосфера", 89, 46], ["Чистота", 88, 26], ["Номера", 71, 56], ["Тишина в номере", 47, 20]],
  quotes=[], stop=["Улица Фомичёва", "310 м"], yandex="https://yandex.by/maps/org/lida_drayv_plyus/183856233649/",
  note="Реже всего гости хвалят тишину в номере: 47% положительных отзывов из 20.",
  theme=dict(bg="#eef3f0", ink="#14302a", mute="#4b635c", accent="#b8892b", aink="#14302a", panel="#ffffff", line="#cfdcd6",
             hbg="#14302a", hink="#f1f5f2", r="2px", fh="Georgia,'Times New Roman',serif", fb="Georgia,'Times New Roman',serif")),
 dict(slug="avtomasters", name="АвтоМастерС", category="Автосервис, автотехцентр, магазин автозапчастей", city="Гомель",
  address="Гомель, Шоссейная ул., 8А", phone="+375 44 575-76-55", phone_note="Консультация и запись на ремонт",
  rating="5,0", rating_count=95, reviews_count=59, hours="",
  lead="Ремонт и обслуживание Mercedes-Benz, Land Rover и Jaguar в Гомеле. Бесплатная диагностика подвески.",
  cta="Записаться на ремонт",
  links=[["WhatsApp", "https://wa.me/375445757655"], ["Viber", "https://viber.click/375445757655"],
         ["Telegram", "https://t.me/375445757655"], ["Instagram", "https://www.instagram.com/automasters_gomel/"]],
  prices=[["Замена сцепления на VW T5/T6", "", "520 BYN"]],
  promo="Бесплатная диагностика подвески в Гомеле",
  features=["Оплата картой", "Базовое сервисное обслуживание", "Кузовной ремонт"],
  works=["Ремонт двигателя", "Замена двигателя", "Замена сцепления", "Ремонт подвески и тормозной системы", "Замена ремня ГРМ",
         "Замена цепи ГРМ", "Замена радиатора печки", "Ремонт и замена турбины", "Автоэлектрика", "Компьютерная диагностика",
         "Ремонт АКПП", "Ремонт КПП", "Покраска автомобиля", "Установка парктроника"],
  aspects=[["Время ожидания", 100, 23], ["Запчасти", 92, 14], ["Ремонт", 91, 32], ["Персонал", 90, 48]],
  quotes=[["Присылают фото и видео, а по окончании работ выдают заказ-наряд с гарантией.", "Виктор Р.", "15 июня"],
          ["Мне наглядно рассказали и показали, что, где и от какого производителя лучше поставить по приемлемой цене.", "Дмитрий К.", "15 июня"]],
  stop=["Никольская церковь", "800 м"], yandex="https://yandex.by/maps/org/avtomasters/158395784301/",
  note="В карточке указан только один прайс-пункт. Остальные цены сообщают по телефону.",
  theme=dict(bg="#eaeef2", ink="#13202c", mute="#52606d", accent="#0b5fd6", aink="#ffffff", panel="#ffffff", line="#cdd6df",
             hbg="#1b2a38", hink="#f3f6f9", r="6px", fh="'Arial Narrow','Helvetica Neue',Arial,sans-serif", fb="system-ui,-apple-system,'Segoe UI',Roboto,sans-serif")),
 dict(slug="yudzhin-avto", name="Юджин авто", category="Автосервис, автотехцентр", city="Гомель",
  address="Гомель, просп. Октября, 27/4", phone="+375 29 527-15-05", phone_note="",
  rating="4,4", rating_count=6, reviews_count=5, hours="",
  lead="Диагностика и ремонт в Гомеле с прозрачными ценами: компьютерная диагностика 40 BYN, ремонт тормозов 50 BYN.",
  cta="Позвонить в сервис",
  links=[["WhatsApp", "https://wa.me/375295271505"], ["Viber", "https://viber.click/+375295271505"],
         ["Запись в Instagram", "https://www.instagram.com/shakhlenkov_evgeny9928"]],
  prices=[["Компьютерная диагностика", "", "40 BYN"], ["Обслуживание и ремонт тормозных систем", "", "50 BYN"],
          ["Диагностика и ремонт дизельных и бензиновых топливных систем", "", "40 BYN"],
          ["Ремонт ходовой части автомобиля", "", "60 BYN"], ["Капитальный ремонт бензиновых и дизельных ДВС", "", "100 BYN"]],
  promo="", features=["Оплата картой", "Базовое сервисное обслуживание", "Кузовной ремонт", "Шиномонтаж"],
  works=["Ремонт АКПП", "Ремонт КПП", "Ремонт сцепления", "Замена ГРМ", "Ремонт турбокомпрессора", "Ремонт генераторов",
         "Ремонт стартеров", "Ремонт рулевых реек", "Ремонт фар", "Шумоизоляция", "Эндоскопия двигателя"],
  aspects=[], quotes=[["Сделали всё хорошо, по доступной цене и в кротчайшие сроки.", "Иван Моденков", "23 августа"],
          ["Редкое сочетание, когда руководитель лично контролирует весь процесс.", "Галина Запецкая", "8 октября"]],
  stop=["Мотороремонтный завод", "400 м"], yandex="https://yandex.by/maps/org/yudzhin_avto/5907564066/",
  note="Оценка 4,4 основана на 6 оценках, а отзывов в карточке 5. Выборка небольшая.",
  theme=dict(bg="#fbf6e6", ink="#241f10", mute="#6a5f3c", accent="#1f1a0c", aink="#f6c52b", panel="#ffffff", line="#e6dcae",
             hbg="#f6c52b", hink="#241f10", r="0px", fh="Impact,'Arial Narrow Bold','Helvetica Neue',sans-serif", fb="system-ui,-apple-system,'Segoe UI',Roboto,sans-serif")),
 dict(slug="detroyt", name="Детройт", category="Автосервис, автомойка, шиномонтаж", city="Барановичи",
  address="Барановичи, ул. 50 лет ВЛКСМ, 45", phone="+375 33 669-90-89", phone_note="",
  rating="4,4", rating_count=223, reviews_count=75, hours="",
  lead="Автосервис, автомойка и шиномонтаж в одном месте в Барановичах. Пока машину моют, можно подождать в зале ожидания.",
  cta="Позвонить",
  links=[["Instagram", "http://instagram.com/detroitautocenter"], ["ВКонтакте", "https://vk.ru/club114827625"]],
  prices=[], promo="", features=["Оплата картой", "Базовое сервисное обслуживание", "Развал-схождение", "Шиномонтаж"],
  works=["Общий ремонт и обслуживание", "Замена коробки передач", "Замена воздушных и салонных фильтров", "Мойка", "Шиномонтаж", "Развал-схождение"],
  aspects=[["Персонал", 74, 32], ["Мойка", 71, 55], ["Время ожидания", 58, 23]],
  quotes=[["Обслуживают быстро и качественно, персонал вежливый, в зале ожидания есть удобные кресла и питьевая вода.", "Валентина Хорунжая", "19 февраля"],
          ["Удобно, что рядом мойка и по просьбе ребята отогнали авто на мойку.", "Максим Якшук", "21 августа"]],
  stop=["Спецавтобаза", "259 м"], yandex="https://yandex.by/maps/org/detroyt/51220960303/",
  note="Цены в карточке не указаны (стоят условные 1 Br), поэтому прайс не публикуем. Гости упоминают очередь на мойку: положительных отзывов о времени ожидания 58%.",
  theme=dict(bg="#f4f4f2", ink="#22262c", mute="#5d636b", accent="#c4262e", aink="#ffffff", panel="#ffffff", line="#d9d9d4",
             hbg="#2b2f36", hink="#f6f6f4", r="3px", fh="'Arial Black','Helvetica Neue',Arial,sans-serif", fb="system-ui,-apple-system,'Segoe UI',Roboto,sans-serif")),
 dict(slug="kvn", name="КВН", category="Автосервис, ремонт двигателей, шиномонтаж", city="Барановичи",
  address="Барановичи, ул. Вильчковского, 81В", phone="+375 29 721-01-56", phone_note="МТС",
  rating="5,0", rating_count=54, reviews_count=19, hours="",
  lead="Автосервис для легковых автомобилей в Барановичах. Замена масла и масляного фильтра от 40 Br, диагностика, ремонт двигателя и ходовой.",
  cta="Позвонить",
  links=[["Viber", "https://viber.click/+375297210156"], ["Instagram", "https://www.instagram.com/autoservice_kvn_baranovichi"]],
  prices=[["Сервисное обслуживание: замена масла, фильтра масляного", "", "40 Br за 1 шт."]],
  promo="", features=["Оплата картой", "Базовое сервисное обслуживание", "Шиномонтаж"],
  works=["Компьютерная диагностика", "Ремонт двигателя", "Ремонт ходовой части", "Ремонт тормозной системы", "Замена ГРМ",
         "Ремонт КПП", "Ремонт генераторов", "Ремонт стартеров", "Промывка инжектора", "Проточка тормозных дисков", "Установка парктроника"],
  aspects=[], quotes=[["Быстро провели диагностику, нашли реальную причину поломки и всё чётко устранили без лишних переплат.", "Сергей Глебчук", "29 октября"],
          ["Понятный сервис. Понятные механики. Без тайн за закрытыми дверями.", "Алексей Пинчук", "16 июня 2025"]],
  stop=["Метеостанция", "550 м"], yandex="https://yandex.by/maps/org/kvn/94281552340/",
  note="Из прайса в карточке опубликована одна позиция. Остальное уточняйте по телефону.",
  theme=dict(bg="#edf3ee", ink="#16261d", mute="#4f6256", accent="#1f7a4d", aink="#ffffff", panel="#ffffff", line="#cddcd2",
             hbg="#1f7a4d", hink="#ffffff", r="10px", fh="'Trebuchet MS','Segoe UI',sans-serif", fb="system-ui,-apple-system,'Segoe UI',Roboto,sans-serif")),
 dict(slug="interavto", name="Интеравто", category="Автосервис, ремонт выхлопных систем", city="Мозырь",
  address="Мозырь, Интернациональная ул., 63В", phone="+375 29 247-09-00", phone_note="",
  rating="4,9", rating_count=62, reviews_count=30, hours="",
  lead="Автосервис в Мозыре: диагностика, ремонт ходовой, выхлопной и топливной систем. В отзывах хвалят скорость и цены.",
  cta="Позвонить в сервис", links=[["Instagram", "https://www.instagram.com/interavto63/"]],
  prices=[["Промывка радиатора системы отопления салона", "Альтернатива замене радиатора: промывка на специальной установке.", "150 Br"]],
  promo="", features=["Оплата картой", "Базовое сервисное обслуживание", "Развал-схождение", "Шиномонтаж"],
  works=["Ремонт выхлопной системы", "Ремонт тормозной системы", "Ремонт двигателя", "Замена ГРМ", "Ремонт ходовой части",
         "Компьютерная диагностика", "Ремонт сцепления", "Ремонт турбокомпрессора", "Ремонт системы охлаждения", "Ремонт топливной системы"],
  aspects=[["Ремонт", 100, 17], ["Время ожидания", 100, 15], ["Персонал", 94, 20]],
  quotes=[["За день заменили всю подвеску, рулевую рейку и барабаны сзади.", "Руслан Казмирчук", "10 сентября 2025"],
          ["Мастера оперативно провели диагностику и быстро определили необходимые работы.", "валера м.", "2 февраля"]],
  stop=["Школа № 8", "257 м"], yandex="https://yandex.by/maps/org/interavto/6662825271/",
  note="Из прайса в карточке опубликована одна позиция. Остальное уточняйте по телефону.",
  theme=dict(bg="#f3f5f9", ink="#14284b", mute="#51607c", accent="#e8761c", aink="#1a1206", panel="#ffffff", line="#d3d9e5",
             hbg="#14284b", hink="#f3f5f9", r="4px", fh="'Segoe UI Semibold','Helvetica Neue',Arial,sans-serif", fb="system-ui,-apple-system,'Segoe UI',Roboto,sans-serif")),
]


def ntext(n, forms):
    n10, n100 = n % 10, n % 100
    return forms[0] if n10 == 1 and n100 != 11 else forms[1] if 2 <= n10 <= 4 and not 12 <= n100 <= 14 else forms[2]


def page(d):
    t = d["theme"]
    loc = ROOT / "assets" / "photos" / d["slug"] / "hero.jpg"
    photo = f"../assets/photos/{d['slug']}/hero.jpg" if loc.exists() else PHOTOS[d["slug"]]
    tel = "tel:" + "".join(c for c in d["phone"] if c.isdigit() or c == "+")
    var = ";".join(f"--{k}:{v}" for k, v in dict(bg=t["bg"], ink=t["ink"], mute=t["mute"], accent=t["accent"], aink=t["aink"],
              panel=t["panel"], line=t["line"], hbg=t["hbg"], hink=t["hink"], r=t["r"], fh=t["fh"], fb=t["fb"], photo=f"url('{photo}')").items())
    btns = f'<a class="btn" href="{tel}">{e(d["cta"])}: {e(d["phone"])}</a>' + "".join(
        f'<a class="btn alt" href="{e(u)}" rel="noopener">{e(n)}</a>' for n, u in d["links"])
    out = [f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{e(d["name"])}, {e(d["city"])}</title><meta name="description" content="{e(d["lead"])}">'
           f'<style>:root{{{var}}}{CSS}{EXTRA}</style></head><body>',
           f'<nav class="top glass"><b>{e(d["name"])}</b><a class="btn" href="{tel}">Позвонить</a></nav><header class="hero"><div class="wrap hgrid"><div class="htext"><p class="cat">{e(d["category"])}, {e(d["city"])}</p><h1>{e(d["name"])}</h1>'
           f'<p class="lead">{e(d["lead"])}</p><div class="cta">{btns}</div>'
           f'<div class="score"><b>{d["rating"]}</b><span>рейтинг на Яндекс Картах</span><span>{d["rating_count"]} '
           f'{ntext(d["rating_count"], ["оценка","оценки","оценок"])}</span><span>{d["reviews_count"]} '
           f'{ntext(d["reviews_count"], ["отзыв","отзыва","отзывов"])}</span></div></div><figure class="shot"><img src="{photo}" alt="Фото: {e(d["name"])}" onerror="this.parentNode.remove()"></figure></div></header><main>']
    if d["prices"] or d["promo"]:
        rows = "".join(f'<div class="row"><dt>{e(n)}</dt><dd class="p">{e(p)}</dd>' + (f'<dd class="d">{e(ds)}</dd>' if ds else "") + '</div>'
                       for n, ds, p in d["prices"])
        out.append('<section id="prices"><div class="wrap"><h2>Услуги и цены</h2>'
                   + (f'<p class="promo">{e(d["promo"])}</p>' if d["promo"] else "")
                   + (f'<dl class="prices">{rows}</dl>' if rows else "") + f'<p class="note">{e(d["note"])}</p></div></section>')
    if d["works"] or d["features"]:
        chips = "".join(f"<li>{e(x)}</li>" for x in d["features"] + d["works"])
        out.append(f'<section><div class="wrap"><h2>Что здесь делают</h2><ul class="chips">{chips}</ul>'
                   + ('' if d["prices"] or d["promo"] else f'<p class="note" style="margin-top:1.2em">{e(d["note"])}</p>') + '</div></section>')
    asp = "".join(f'<li><span>{e(a)}</span><span class="bar" role="img" aria-label="{p}% положительных"><i style="width:{p}%"></i></span>'
                  f'<span>{p}% <small>({n})</small></span></li>' for a, p, n in d["aspects"])
    qs = "".join(f'<blockquote><p>«{e(q)}»</p><footer>{e(a)}, {e(dt)}</footer></blockquote>' for q, a, dt in d["quotes"])
    if asp or qs:
        out.append('<section id="reviews"><div class="wrap"><h2>Что пишут клиенты</h2>'
                   + (f'<ul class="aspects">{asp}</ul>' if asp else "") + qs
                   + f'<p class="note">Оценки и отзывы из карточки на Яндекс Картах. <a href="{e(d["yandex"])}reviews/" rel="noopener">Все отзывы</a>.</p></div></section>')
    out.append(f'<section id="contacts"><div class="wrap"><h2>Как найти</h2><div class="contacts"><div><h3>Адрес</h3><p>{e(d["address"])}</p>'
               f'<p>Остановка «{e(d["stop"][0])}», {e(d["stop"][1])}</p><p><a href="{e(d["yandex"])}" rel="noopener">Маршрут в Яндекс Картах</a></p></div>'
               f'<div><h3>Телефон</h3><p><a href="{tel}">{e(d["phone"])}</a></p>' + (f'<p>{e(d["phone_note"])}</p>' if d["phone_note"] else "") + '</div>'
               f'<div><h3>Режим работы</h3><p>' + (e(d["hours"]) if d["hours"] else "График смотрите в карточке на Яндекс Картах или уточняйте по телефону.") + '</p></div></div></div></section>')
    out.append(f'<section class="band"><div class="wrap"><div class="glass card"><h2>{e(d["name"])}, {e(d["city"])}</h2><p>{e(d["address"])}</p><div class="cta">{btns}</div></div></div></section></main><footer class="site"><div class="wrap">Данные: Яндекс Карты. Прототип сайта, не официальный ресурс организации. '
               f'<a href="../index.html">Все прототипы</a></div></footer></body></html>')
    return "".join(out)


def hub():
    cards = "".join(f'<li><a href="{d["slug"]}/"><b>{e(d["name"])}</b><span>{e(d["category"].split(",")[0])}, {e(d["city"])}</span>'
                    f'<span>Рейтинг {d["rating"]}, {d["rating_count"]} {ntext(d["rating_count"], ["оценка","оценки","оценок"])}</span></a></li>' for d in DATA)
    return ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Прототипы сайтов для местного бизнеса</title><style>body{margin:0;font:18px/1.5 system-ui,sans-serif;background:#f5f5f3;color:#1d1d1b}'
            'main{max-width:860px;margin:0 auto;padding:48px 20px}h1{font-size:2.2rem;line-height:1.1;margin:0 0 .4em}'
            'ul{list-style:none;padding:0;display:grid;gap:12px}a{display:grid;gap:2px;padding:18px 20px;background:#fff;border:1px solid #d8d8d2;border-radius:8px;text-decoration:none;color:inherit}'
            'a:hover,a:focus-visible{border-color:#1d1d1b;outline:none}b{font-size:1.25rem}span{color:#5a5a54;font-size:.95rem}</style></head><body><main>'
            f'<h1>Прототипы сайтов для местного бизнеса</h1><p>Шесть одностраничных сайтов по данным карточек Яндекс Карт. Это демо-версии: по первой просьбе владельца мы удалим сайт.</p><ul>{cards}</ul></main></body></html>')


if __name__ == "__main__":
    from layout import page
    RAW.mkdir(parents=True, exist_ok=True)
    for d in DATA:
        (RAW / f"{d['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        (ROOT / d["slug"]).mkdir(exist_ok=True)
        (ROOT / d["slug"] / "index.html").write_text(page(d), encoding="utf-8")
    (ROOT / "index.html").write_text(hub(), encoding="utf-8")
    print("Готово:", len(DATA), "сайтов")
