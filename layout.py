"""Макет в стиле iOS: матовая шапка, группированные списки, скругления, одна кнопка «Позвонить»."""
import html
from build import PHOTOS, ROOT, ntext

e = html.escape

HEAD = {
    "lida-drive-plus": "Гостиница в Лиде с баней на дровах",
    "avtomasters": "Автосервис в Гомеле: Mercedes-Benz, Land Rover, Jaguar",
    "yudzhin-avto": "Диагностика и ремонт в Гомеле, цены на сайте",
    "detroyt": "Автосервис, мойка и шиномонтаж в Барановичах",
    "kvn": "Автосервис для легковых авто в Барановичах",
    "interavto": "Автосервис в Мозыре: диагностика и ремонт",
}
TINT = {"lida-drive-plus": "#1f9d55", "avtomasters": "#0a6cff", "yudzhin-avto": "#c76a00",
        "detroyt": "#d62b25", "kvn": "#0a7ea8", "interavto": "#5348d6"}
DEMO = "Это демо-версия сайта. По первой просьбе владельца мы удалим сайт."

CSS = """
:root{--bg:#f2f2f7;--card:#fff;--ink:#1c1c1e;--mute:#6e6e73;--sep:#e5e5ea;--chip:#f2f2f7}
@media(prefers-color-scheme:dark){:root{--bg:#000;--card:#1c1c1e;--ink:#f5f5f7;--mute:#98989f;--sep:#38383a;--chip:#2c2c2e}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.45 -apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue","Segoe UI",Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--tint);text-decoration:none}a:hover{text-decoration:underline}
:focus-visible{outline:3px solid var(--tint);outline-offset:2px;border-radius:8px}
.wrap{max-width:1040px;margin:0 auto;padding:0 16px}
.demo{background:color-mix(in srgb,var(--tint) 16%,var(--bg));color:var(--ink);text-align:center;padding:10px 16px;font-size:.92rem;font-weight:600}
.nav{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--bg) 72%,transparent);-webkit-backdrop-filter:saturate(180%) blur(22px);backdrop-filter:saturate(180%) blur(22px);border-bottom:.5px solid var(--sep);text-align:center;padding:14px 16px;font-weight:600}
.hero{position:relative;isolation:isolate;overflow:hidden;margin:12px auto 0;max-width:1012px;border-radius:30px;color:#fff;padding:56px 28px 40px}
@media(max-width:1040px){.hero{margin:12px 12px 0;padding:44px 20px 28px}}
.hero::before{content:"";position:absolute;inset:-60px;z-index:-2;background:var(--photo) center/cover no-repeat,radial-gradient(circle at 18% 22%,var(--tint),transparent 55%),radial-gradient(circle at 88% 80%,color-mix(in srgb,var(--tint) 50%,#1c1c1e),transparent 55%),#1c1c1e;filter:blur(24px) saturate(1.25)}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,0,0,.28),rgba(0,0,0,.55))}
.hg{display:flex;flex-wrap:wrap;gap:30px;align-items:center}.ht{flex:1 1 380px}
.cat{margin:0 0 .5em;opacity:.85;font-size:.98rem;font-weight:500}
h1{font-weight:700;font-size:clamp(2.1rem,6vw,3.7rem);line-height:1.05;letter-spacing:-.025em;margin:0 0 .35em;text-wrap:balance}
.lead{margin:0 0 1.4em;font-size:1.15rem;max-width:32em;opacity:.95}
.cta{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;padding:13px 24px;border-radius:999px;background:var(--tint);color:#fff;font-weight:600;font-size:1rem}
.btn:hover{text-decoration:none;filter:brightness(1.08)}
.btn.g{background:rgba(255,255,255,.22);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.shot{flex:0 1 380px;margin:0;border-radius:24px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.4)}
.shot img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.pill{display:inline-flex;flex-wrap:wrap;gap:4px 18px;align-items:baseline;margin-top:1.6em;padding:12px 20px;border-radius:22px;background:rgba(255,255,255,.16);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.pill b{font-size:2rem;line-height:1}
h2{font-size:1.75rem;line-height:1.15;letter-spacing:-.02em;margin:44px 6px 12px}
.group{background:var(--card);border-radius:20px;overflow:hidden}
.item{display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding:14px 18px;border-top:.5px solid var(--sep)}
.item:first-child{border-top:0}
.item small{display:block;color:var(--mute);font-size:.9rem;margin-top:2px}
.v{text-align:right;font-weight:600}.item .v{color:var(--tint)}.item .v.plain{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.tile{background:var(--card);border-radius:20px;padding:20px}
.tile b{display:block;font-size:2.1rem;line-height:1.1;letter-spacing:-.02em;color:var(--tint);overflow-wrap:anywhere}
.tile span{color:var(--mute);font-size:.93rem}
details{border-top:.5px solid var(--sep)}details:first-child{border-top:0}
summary{cursor:pointer;list-style:none;padding:15px 18px;font-weight:600;display:flex;justify-content:space-between}
summary::-webkit-details-marker{display:none}
summary::after{content:"\\203A";color:var(--mute);font-size:1.5rem;line-height:1;transition:transform .2s}
details[open] summary::after{transform:rotate(90deg)}
details>div{padding:0 0 12px}
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:0;padding:4px 18px 8px}
.chips li{background:var(--chip);padding:7px 14px;border-radius:999px;font-size:.92rem}
.promo{margin:0 18px 8px;padding:12px 16px;border-radius:14px;background:color-mix(in srgb,var(--tint) 14%,var(--card));font-weight:600}
.note{color:var(--mute);font-size:.9rem;padding:4px 18px 8px;margin:0}
.asp{display:grid;grid-template-columns:minmax(110px,190px) 1fr auto;gap:14px;align-items:center;padding:12px 18px;border-top:.5px solid var(--sep);font-size:.95rem}
.asp:first-child{border-top:0}
.bar{height:8px;border-radius:99px;background:var(--sep);overflow:hidden}.bar i{display:block;height:100%;background:var(--tint);border-radius:99px}
.asp small{color:var(--mute)}
@media(max-width:560px){.asp{grid-template-columns:1fr auto}.asp .bar{grid-column:1/-1;grid-row:2}}
.rv{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:12px;margin-top:12px}
blockquote{margin:0;background:var(--card);border-radius:20px;padding:18px 20px}
blockquote p{margin:0 0 8px}blockquote footer{color:var(--mute);font-size:.9rem}
.foot{padding:36px 16px 48px;text-align:center;color:var(--mute);font-size:.88rem}
.foot p{margin:.3em 0}
"""


def page(d):
    slug = d["slug"]
    photo = (f"../assets/photos/{slug}/hero.jpg" if (ROOT / "assets/photos" / slug / "hero.jpg").exists() else PHOTOS[slug])
    tel = "tel:" + "".join(c for c in d["phone"] if c.isdigit() or c == "+")
    hotel = "Гостиница" in d["category"]
    hours = d["hours"] or "График смотрите в карточке на Яндекс Картах"
    rc = d["rating_count"]

    # факты
    facts = [(d["rating"], f'рейтинг на Яндекс Картах, {rc} {ntext(rc, ["оценка", "оценки", "оценок"])}'), (str(d["reviews_count"]), "отзывов в карточке")]
    if d["aspects"]:
        a, p, n = max(d["aspects"], key=lambda x: (x[1], x[2]))
        facts.append((f"{p}%", f"положительных отзывов о теме «{a}», всего {n}"))
    else:
        facts.append((d["features"][0], "указано в карточке организации"))
    facts.append((d["stop"][1], f'до остановки «{d["stop"][0]}»'))
    ft = "".join(f'<div class="tile"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in facts)

    # услуги
    items = [(n, ds, p) for n, ds, p in d["prices"]] + [(w, "", "") for w in d["works"]]
    if len(items) < 4:
        items += [(f, "", "") for f in d["features"]]
    sv = "".join(f'<div class="item"><span>{e(n)}' + (f"<small>{e(ds)}</small>" if ds else "") + "</span>" + (f'<span class="v">{e(p)}</span>' if p else "") + "</div>"
                 for n, ds, p in items[:6])

    # цены
    rows = "".join(f'<div class="item"><span>{e(n)}' + (f"<small>{e(ds)}</small>" if ds else "") + f'</span><span class="v">{e(p)}</span></div>' for n, ds, p in d["prices"])
    chips = lambda xs: '<ul class="chips">' + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"
    acc = ('<details open><summary>Цены из карточки</summary><div>' + (f'<p class="promo">{e(d["promo"])}</p>' if d["promo"] else "") + rows
           + f'<p class="note">{e(d["note"])}</p></div></details>')
    if d["works"]:
        acc += f'<details><summary>Все виды работ</summary><div>{chips(d["works"])}</div></details>'
    acc += f'<details><summary>Особенности</summary><div>{chips(d["features"])}</div></details>'

    # отзывы
    asp = "".join(f'<div class="asp"><span>{e(a)}</span><span class="bar" role="img" aria-label="{p}% положительных"><i style="width:{p}%"></i></span><span>{p}% <small>({n})</small></span></div>' for a, p, n in d["aspects"])
    qs = "".join(f'<blockquote><p>«{e(q)}»</p><footer>{e(a)}, {e(dt)}</footer></blockquote>' for q, a, dt in d["quotes"])
    rev = ""
    if asp or qs:
        rev = ("<h2>Отзывы</h2>" + (f'<div class="group">{asp}</div>' if asp else "") + (f'<div class="rv">{qs}</div>' if qs else "")
               + f'<p class="note">Оценки и отзывы из карточки на Яндекс Картах. <a href="{e(d["yandex"])}reviews/" rel="noopener">Все отзывы</a>.</p>')

    # контакты
    soc = " ".join(f'<a href="{e(u)}" rel="noopener">{e(n)}</a>' for n, u in d["links"])
    contacts = (f'<div class="item"><span>Адрес</span><span class="v plain">{e(d["address"])}</span></div>'
                f'<div class="item"><span>Телефон</span><span class="v"><a href="{tel}">{e(d["phone"])}</a></span></div>'
                + (f'<div class="item"><span>Для чего</span><span class="v plain">{e(d["phone_note"])}</span></div>' if d["phone_note"] else "")
                + f'<div class="item"><span>Режим работы</span><span class="v plain">{e(hours)}</span></div>'
                f'<div class="item"><span>Остановка</span><span class="v plain">«{e(d["stop"][0])}», {e(d["stop"][1])}</span></div>'
                f'<div class="item"><span>Мессенджеры и соцсети</span><span class="v">{soc}</span></div>'
                f'<div class="item"><span>Маршрут</span><span class="v"><a href="{e(d["yandex"])}" rel="noopener">Яндекс Карты</a></span></div>')

    body = (
        f'<div class="demo">{DEMO}</div><div class="nav">{e(d["name"])}</div>'
        f'<header class="hero"><div class="hg"><div class="ht"><p class="cat">{e(d["category"])}, {e(d["city"])}</p><h1>{e(HEAD[slug])}</h1>'
        f'<p class="lead">{e(d["lead"])}</p><div class="cta"><a class="btn" href="{tel}">Позвонить</a>'
        f'<a class="btn g" href="{e(d["yandex"])}" rel="noopener">Маршрут</a></div></div>'
        f'<figure class="shot"><img src="{photo}" alt="Фото: {e(d["name"])}" onerror="this.parentNode.remove()"></figure></div></header>'
        f'<main class="wrap"><h2>Коротко</h2><div class="grid">{ft}</div>'
        f'<h2>Услуги</h2><div class="group">{sv}</div>'
        f'<h2>Цены</h2><div class="group">{acc}</div>{rev}'
        f'<h2>Контакты</h2><div class="group">{contacts}</div></main>'
        f'<footer class="foot"><p>{DEMO}</p><p>Данные: Яндекс Карты. Прототип, не официальный ресурс организации.</p>'
        f'<p><a href="../index.html">Все прототипы</a></p></footer>')
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<meta name="color-scheme" content="light dark"><title>{e(d["name"])}, {e(d["city"])}</title><meta name="description" content="{e(d["lead"])}">'
            f'<style>:root{{--tint:{TINT[slug]};--photo:url(\'{photo}\')}}{CSS}</style></head><body>{body}</body></html>')
