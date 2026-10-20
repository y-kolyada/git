#!/usr/bin/env python3
"""Stamp the pages of a new site of the series, once, from the seed shells.

    python3 tools/new-site.py

Reads site.conf, writes 17 pages per language into ru/ en/ uk/ de/ and stops.
Russian pages are skeletons with placeholder titles: the section names and the
text are the work of the site's own first task. The other three languages are
stubs that point at the Russian page, exactly the shape the structure check
already understands.

WHY A STAMP AND NOT A HAND-WRITTEN SHELL. The shell carries the brand, the
utility tray, the font scaler, the language switcher, the sticky navigation,
the in-page navigator and the accessibility markup. Hand-copied, it loses one
of them silently; stamped from a live page of the reference site, it cannot.

Run build-nav.py, build-meta.py and build-search.py after this, in that order:
they fill in the icons, the switcher, the version, the head block, the size and
the neighbouring topics.
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import siteconf

LANGS = ('ru', 'en', 'uk', 'de')
SOURCE = 'ru'
CHAIN = ['index'] + ['%02d' % n for n in range(1, 16)] + ['glossary']
SHELLS = {'index': 'pages/shell-index.html', 'glossary': 'pages/shell-glossary.html',
          'topic': 'pages/shell-topic.html', 'stub': 'pages/shell-stub.html',
          'door': 'pages/shell-door.html'}

# Что в оболочке названо именем эталонного сайта - то и заменяется.
BRAND = re.compile(r'(<span class="sub-brand">)[^<]*(</span>)')
SLOGAN = re.compile(r'(<div class="three" aria-hidden="true">).*?(</div>)', re.S)
TITLE = re.compile(r'<title>.*?</title>', re.S)
HTML = re.compile(r'<html lang="(\w+)"[^>]*>')
HEAD_BLOCK = re.compile(r'\n?<!-- meta:.*?<!-- /meta -->', re.S)
MAIN = re.compile(r'(<main id="main">).*?(</main>)', re.S)
NAV_ITEM = re.compile(r'(<a href="(\d\d)\.html"[^>]*>)(.*?)(</a>)', re.S)
INLINE = re.compile(r'<script>\s*\(function\(\).*?\)\(\);\s*</script>', re.S)
# У корневой двери свой <main>, без идентификатора: она не страница темы.
DOOR_MAIN = re.compile(r'(<main>).*?(</main>)', re.S)
# Переключатель языков ведёт на ту же страницу в другом языке, а оболочка
# скопирована с одной страницы: ссылки надо переставить на каждой.
SWITCH = re.compile(r'(<a href=")(?:\.\./(?:en|uk|de|ru)/)?[\w-]+\.html(" lang=")(\w\w)')

EARLY = """<script>
  (function() {
    var s = document.documentElement.dataset.site || 'swa';
    var t = localStorage.getItem('swa-' + s + '-theme');
    if (t) document.documentElement.setAttribute('data-theme', t);
    var f = localStorage.getItem('swa-' + s + '-font');
    if (f) document.documentElement.setAttribute('data-font', f);
  })();
</script>"""

SAY = {
    'ru': {'section': 'Раздел', 'glossary': 'Словарь понятий', 'landing': 'Посадочная страница',
           'lead': 'Лид страницы: о чём она и кому нужна. Одно предложение, не длиннее 160 знаков.',
           'key': 'Главная мысль страницы', 'artifacts': 'Артефакты: что у вас есть после этой страницы',
           'todo': 'Текст этого раздела ещё не написан.'},
    'en': {'wait': 'The English version is in preparation', 'open': 'Open the full version:',
           'where': 'The full working version of this page is published in Russian.'},
    'uk': {'wait': 'Українська версія готується', 'open': 'Відкрити повну версію:',
           'where': 'Повна робоча версія цієї сторінки опублікована російською.'},
    'de': {'wait': 'Die deutsche Fassung ist in Vorbereitung', 'open': 'Vollständige Fassung öffnen:',
           'where': 'Die vollständige Arbeitsfassung dieser Seite ist auf Russisch veröffentlicht.'},
}


def read(path):
    return pathlib.Path(path).read_text(encoding='utf-8')


def heading(name, conf):
    if name == 'index':
        return '%s: %s' % (conf['topic'], SAY['ru']['landing'])
    if name == 'glossary':
        return SAY['ru']['glossary']
    return '%s %d' % (SAY['ru']['section'], int(name))


def shell_for(name):
    if name in SHELLS:
        return read(SHELLS[name])
    return read(SHELLS['topic'])


def dress(text, lang, name, conf):
    """Общая часть: бренд, слоган, заголовок окна, имя сайта для хранилища."""
    # data-site ставит build-nav.py, здесь только язык страницы.
    text = HTML.sub('<html lang="%s">' % lang, text, count=1)
    text = TITLE.sub('<title>%s · %s · ai|</title>' % (heading(name, conf), conf['name']), text, count=1)
    text = BRAND.sub(lambda m: m.group(1) + conf['name'] + m.group(2), text)
    text = SLOGAN.sub(lambda m: m.group(1) + conf['slogan'] + m.group(2), text)
    text = HEAD_BLOCK.sub('', text)
    text = INLINE.sub(EARLY, text, count=1)
    text = NAV_ITEM.sub(lambda m: m.group(1) + '%s %d' % (SAY['ru']['section'], int(m.group(2))) + m.group(4), text)

    def switch(found):
        other = found.group(3)
        href = '%s.html' % name if other == lang else '../%s/%s.html' % (other, name)
        return found.group(1) + href + found.group(2) + other
    text = SWITCH.sub(switch, text)
    return text


def skeleton(name, conf):
    head = heading(name, conf)
    if name == 'glossary':
        return ('\n    <h1>%s</h1>\n    <p class="lead">%s</p>\n\n'
                '    <p>%s</p>\n  ' % (head, SAY['ru']['lead'], SAY['ru']['todo']))
    body = ['\n    <h1>%s</h1>' % head,
            '    <p class="lead">%s</p>' % SAY['ru']['lead'],
            '',
            '    <div class="box key" id="key-idea">',
            '      <h2>%s <a class="anchor-link" href="#key-idea" aria-label="ссылка на этот блок">#</a></h2>'
            % SAY['ru']['key'],
            '      <p>%s</p>' % SAY['ru']['todo'],
            '    </div>', '']
    if name != 'index':
        body += ['    <h2 id="first">1 · %s 1 <a class="anchor-link" href="#first">#</a></h2>' % SAY['ru']['section'],
                 '    <p>%s</p>' % SAY['ru']['todo'], '']
    body += ['    <div class="box key" id="artifacts">',
             '      <h2>%s <a class="anchor-link" href="#artifacts">#</a></h2>' % SAY['ru']['artifacts'],
             '      <p>%s</p>' % SAY['ru']['todo'],
             '    </div>', '  ']
    return '\n'.join(body)


def stub(lang, name, conf):
    head = heading(name, conf)
    say = SAY[lang]
    return ('\n    <h1>%s</h1>\n\n'
            '    <div class="stub-card">\n'
            '      <h2>%s</h2>\n'
            '      <p>%s</p>\n'
            '      <p>%s</p>\n'
            '      <div class="stub-actions">\n'
            '        <a href="../%s/%s.html" class="btn-primary">%s →</a>\n'
            '      </div>\n'
            '    </div>\n  ' % (head, say['wait'], say['where'], say['open'], SOURCE, name, head))


def doorway(conf):
    """Содержимое корневой двери: выбор языка и честная строка о состоянии."""
    return """
  <h1>Выберите язык</h1>

  <p>Справочник-ассессмент по %s. Текст сайта пишется: русский язык - источник,
  остальные три пока ведут на него.</p>

  <ul>
    <li><a href="ru/index.html"><strong>Русский</strong></a> - полный текст сайта</li>
    <li><a href="en/index.html"><strong>English</strong></a> - translation in preparation</li>
    <li><a href="uk/index.html"><strong>Українська</strong></a> - переклад готується</li>
    <li><a href="de/index.html"><strong>Deutsch</strong></a> - Übersetzung in Vorbereitung</li>
  </ul>

  <div class="box key">
    <h2>Что здесь честно сказано</h2>
    <p>Русский язык - источник, с него идут остальные три. Английский, украинский и немецкий
    пока заглушки со ссылкой на русскую страницу: это решение, а не недоработка. Страница,
    которой нет, не обещается.</p>
  </div>
""" % conf['topic']


def main():
    conf = siteconf.conf()
    conf.setdefault('slogan', 'инструменты · <span class="topic">%s</span> · практика · 150 вопросов'
                    % conf['topic'])
    made = 0
    for lang in LANGS:
        pathlib.Path(lang).mkdir(exist_ok=True)
        for name in CHAIN:
            page = pathlib.Path('%s/%s.html' % (lang, name))
            if page.exists():
                continue
            text = dress(shell_for(name if lang == SOURCE else 'stub'), lang, name, conf)
            inner = skeleton(name, conf) if lang == SOURCE else stub(lang, name, conf)
            text = MAIN.sub(lambda m: m.group(1) + inner + m.group(2), text, count=1)
            page.write_text(text, encoding='utf-8')
            made += 1
    # Корневая дверь: без неё адрес сайта отдаёт 404, а внутренние страницы
    # живут в папках языков. Правятся в ней только бренд, слоган и заголовок.
    door = pathlib.Path('index.html')
    if not door.exists():
        text = dress(read(SHELLS['door']), SOURCE, 'index', conf)
        text = DOOR_MAIN.sub(lambda m: m.group(1) + doorway(conf) + m.group(2), text, count=1)
        door.write_text(text, encoding='utf-8')
        made += 1

    print()
    print('  Страницы нового сайта')
    print('  ' + '-' * 46)
    print('  создано: %d из %d' % (made, len(LANGS) * len(CHAIN) + 1))
    print('  дальше: build-nav.py, build-meta.py, build-search.py, ./check.sh')
    print('  ' + '-' * 46)
    print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
