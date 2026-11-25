import os
from pathlib import Path
from nicegui import ui
from yaappu import grammar, utils, Sandhapa, Vannapa, Marutpaa
import re


def get_app_version() -> str:
    setup_file = BASE_DIR / 'setup.py'
    if setup_file.exists():
        match = re.search(r'''version\s*=\s*['"]([^'"]+)['"]''', setup_file.read_text(encoding='utf-8'))
        if match:
            return f"V{match.group(1)}"
    return 'V1.7.8'


_APP_VERSION = get_app_version()

BASE_DIR = Path(__file__).resolve().parent
TEST_INPUT_DIR = BASE_DIR / 'yaappu' / 'test_input'
VANNAPPA_DIR = TEST_INPUT_DIR / 'vannappa_examples'
SANDHAPPA_DIR = TEST_INPUT_DIR / 'sandhappa_examples'
MARUTPA_DIR = TEST_INPUT_DIR / 'marutppa_examples'

UYIR_KEYS = ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ', 'ஃ']
BASE_CONSONANTS = [
    'க', 'ங', 'ச', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ன',
    'ப', 'ம', 'ய', 'ர', 'ற', 'ல', 'ள', 'ழ', 'வ',
    'ஜ', 'ஷ', 'ஸ', 'ஹ',
]
VOWEL_SIGNS = {
    '': 'அடிப்படை',
    '்': '்',
    'ா': 'ா',
    'ி': 'ி',
    'ீ': 'ீ',
    'ு': 'ு',
    'ூ': 'ூ',
    'ெ': 'ெ',
    'ே': 'ே',
    'ை': 'ை',
    'ொ': 'ொ',
    'ோ': 'ோ',
    'ௌ': 'ௌ',
}


def load_files_for_selection(check_sandhapa: bool, check_vannapa: bool,
                             check_marutpa: bool) -> dict[str, Path]:
    """Return a {dropdown_label: Path} mapping while preserving each file's source folder."""
    files_map: dict[str, Path] = {}

    def add_from_folder(folder: Path, prefix: str = '') -> None:
        if not folder.exists() or not folder.is_dir():
            return
        for p in sorted((f for f in folder.glob('*.txt') if f.is_file()), key=lambda f: f.name.lower()):
            label = f'{prefix}{p.name}'
            files_map[label] = p

    if check_marutpa:
        add_from_folder(MARUTPA_DIR, prefix='மருட்பா: ')
    if check_vannapa and check_sandhapa:
        add_from_folder(VANNAPPA_DIR, prefix='வண்ணப்பா: ')
        add_from_folder(SANDHAPPA_DIR, prefix='சந்தப்பா: ')
        add_from_folder(VANNAPPA_DIR)
    elif check_sandhapa:
        add_from_folder(SANDHAPPA_DIR)
    elif not check_marutpa:
        add_from_folder(TEST_INPUT_DIR)

    return files_map

def build_analysis(poem_text: str, check_sandhapa: bool, check_vannapa: bool,
                   check_marutpa: bool) -> dict[str, str]:
    tp = grammar.Yaappu(poem_text)
    paa_check, poem_analysis = tp.analyze(get_individual_poem_analysis=True)

    char_stats = '\n'.join(
        f'{name} : {count}'
        for name, count in utils.get_character_type_counts(
            tp.text(), show_by_character_type_keys=False, include_zero_counts=False
        )
    )

    asai_seer_lines = []
    for line in tp.line_objects:
        r1 = '    '.join(w.asai_word() for w in line.word_objects)
        r2 = '    '.join(w.asaigaL() for w in line.word_objects)
        r3 = '    '.join(w.seer_type() or '' for w in line.word_objects)
        r4 = '    '.join(w.sandha_seer() or '' for w in line.word_objects)
        asai_seer_lines.append('\n'.join([r1, r2, r3, r4, line.line_type()]))
    asai_seer_adi = '\n\n'.join(asai_seer_lines)

    thalai_osai_rows = []
    lines = tp.line_objects
    for l_idx in range(tp.line_count()):
        wc = lines[l_idx].word_count()
        for w_idx in range(wc):
            if l_idx == tp.line_count() - 1 and w_idx == wc - 1:
                continue
            n_l, n_w = (l_idx + 1, 0) if w_idx + 1 == wc else (l_idx, w_idx + 1)
            w1 = lines[l_idx].word_objects[w_idx]
            w2 = lines[n_l].word_objects[n_w]
            thalai = w1.thaLai_type(w2.text())
            osai = w1.osai_type(w2.text())
            thalai_osai_rows.append(
                f'{w1.text()} - {w2.text()}  |  {w1.seer_type()} - {thalai}  |  {osai}'
            )

    seer_thodai_parts = []
    for label, idx in [('சீர் மோனை', 0), ('சீர் எதுகை', 1), ('சீர் இயைபு', -1)]:
        words_2d = tp.seer_thodai_words(idx)
        block = [f'=== {label} ===']
        for l_idx in range(tp.line_count()):
            block.append(f"{' '.join(words_2d[l_idx])}    {lines[l_idx].seer_thodai_types[idx]}")
        seer_thodai_parts.append('\n'.join(block))

    adi_thodai_parts = []
    for label, idx in [('அடி மோனை', 0), ('அடி எதுகை', 1), ('அடி இயைபு', -1)]:
        adi_thodai_parts.append(f'=== {label} ===\n{tp.adi_thodai_lines(idx, "<>")}')

    isaipaa_out = []
    if check_sandhapa:
        s_check, s_type, s_str = Sandhapa.Sandhapa(poem_text).check_for_sandhapaa()
        isaipaa_out.append(f'{s_check}\n{s_type}\n{s_str}')
    if check_vannapa:
        v_check, v_type, v_str = Vannapa.Vannapa(poem_text).check_for_vannapaa()
        isaipaa_out.append(f'{v_check}\n{v_type}\n{v_str}')
    if check_marutpa:
        m_check, m_type, m_str = Marutpaa.Marutpa(poem_text).check_for_marutpaa()
        isaipaa_out.append(f'{m_check}\n{m_type}\n{m_str}')

    return {
        'ezhuthu': char_stats,
        'asai': asai_seer_adi,
        'thalai': '\n'.join(thalai_osai_rows),
        'seer_thodai': '\n\n'.join(seer_thodai_parts),
        'adi_thodai': '\n\n'.join(adi_thodai_parts),
        'yaappu': f"{paa_check[1]} {grammar.RULE_CHECK(paa_check[0])}\n{paa_check[2]}",
        'details': poem_analysis,
        'isaipaa': '\n\n'.join(isaipaa_out),
    }


@ui.page('/')
def index():
    ui.add_head_html('''
    <style>
        .tamil-font { font-family: "Noto Sans Tamil", "Latha", "Nirmala UI", sans-serif; }
        .mono-out { white-space: pre-wrap; font-family: "Noto Sans Tamil", monospace; font-size: 0.9rem; }
    </style>
    ''')

    current_files: dict[str, Path] = load_files_for_selection(False, False, False)
    selected_base = {'char': 'க'}
    sign_buttons: dict[str, ui.button] = {}
    tab_panels_map: dict[str, ui.label] = {}

    def on_file_selected(e):
        selected_label = e.value
        if not selected_label or selected_label not in current_files:
            return
        file_path = current_files[selected_label]
        try:
            textarea.set_value(file_path.read_text(encoding='utf-8'))
        except Exception as exc:
            ui.notify(f'கோப்பைப் படிக்க முடியவில்லை ({selected_label}): {exc}', type='negative')

    with ui.header().classes('bg-indigo-800 text-white items-center justify-between px-4'):
        ui.label(f"Tamil Prosody Analyzer — யாப்பறி செயலி ({_APP_VERSION})").classes('text-lg font-bold tamil-font')
        file_select = ui.select(
            options=list(current_files.keys()),
            label='செய்யுள் கோப்பு (test_input)',
            on_change=on_file_selected,
        ).props('clearable').classes('w-80 bg-white text-black rounded px-2')

    with ui.column().classes('w-full max-w-6xl mx-auto p-4 gap-4 tamil-font'):
        with ui.row().classes('items-center gap-4'):
            ui.label('இசைப்பாவை ஆராயவும்:').classes('font-semibold')
            sandhapa_cb = ui.checkbox('சந்தப்பா')
            vannapa_cb = ui.checkbox('வண்ணப்பா')
            marutpa_cb = ui.checkbox('மருட்பா')

        textarea = ui.textarea(
            label='தமிழ்ச் செய்யுளை உள்ளிடவும்',
            placeholder='இங்கு செய்யுளைத் தட்டச்சு செய்யவும், கோப்பைத் தேர்ந்தெடுக்கவும் அல்லது விசைப்பலகையைப் பயன்படுத்தவும்...',
        ).props('id=poem-input rows=5 outlined').classes('w-full text-lg')

        async def get_cursor_pos() -> tuple[int, int]:
            pos = await ui.run_javascript('''
                const root = document.getElementById('poem-input');
                const el = root ? (root.tagName === 'TEXTAREA' ? root : root.querySelector('textarea')) : null;
                if (!el) return [null, null];
                return [el.selectionStart ?? el.value.length, el.selectionEnd ?? el.value.length];
            ''')
            if not pos or pos[0] is None:
                current = textarea.value or ''
                return len(current), len(current)
            return int(pos[0]), int(pos[1])

        async def set_cursor_pos(pos: int) -> None:
            await ui.run_javascript(f'''
                const root = document.getElementById('poem-input');
                const el = root ? (root.tagName === 'TEXTAREA' ? root : root.querySelector('textarea')) : null;
                if (el) {{
                    el.focus();
                    el.setSelectionRange({pos}, {pos});
                }}
            ''')

        async def insert_text(text_to_insert: str) -> None:
            current = textarea.value or ''
            start, end = await get_cursor_pos()
            start = max(0, min(start, len(current)))
            end = max(start, min(end, len(current)))

            updated = current[:start] + text_to_insert + current[end:]
            textarea.value = updated
            await set_cursor_pos(start + len(text_to_insert))

        async def backspace_text() -> None:
            current = textarea.value or ''
            if not current:
                return
            start, end = await get_cursor_pos()
            start = max(0, min(start, len(current)))
            end = max(start, min(end, len(current)))

            if start != end:
                remove_start, remove_end = start, end
            elif start > 0:
                remove_end = start
                remove_start = start - 1
                while remove_start > 0 and 0x0BBE <= ord(current[remove_start]) <= 0x0BCD:
                    remove_start -= 1
            else:
                return

            textarea.value = current[:remove_start] + current[remove_end:]
            await set_cursor_pos(remove_start)

        def update_sign_button_labels() -> None:
            base = selected_base['char']
            for sign, btn in sign_buttons.items():
                btn.set_text(f'{base}{sign}' if sign else base)

        async def handle_consonant(c: str) -> None:
            selected_base['char'] = c
            update_sign_button_labels()
            await insert_text(c)

        # Virtual Tamil Keyboard
        with ui.expansion('தமிழ் மெய்நிகர் விசைப்பலகை (Virtual Tamil Keyboard)', value=False).classes('w-full border rounded'):
            with ui.column().classes('p-3 gap-2'):
                ui.label('உயிர் எழுத்துக்கள்').classes('text-xs text-gray-600')
                with ui.row().classes('flex-wrap gap-1'):
                    for ch in UYIR_KEYS:
                        ui.button(ch, on_click=lambda _, c=ch: insert_text(c)).props('dense outline size=sm')

                ui.label('மெய் / உயிர்மெய் அடிப்படை எழுத்துக்கள்').classes('text-xs text-gray-600 mt-1')
                with ui.row().classes('flex-wrap gap-1'):
                    for ch in BASE_CONSONANTS:
                        ui.button(
                            ch,
                            on_click=lambda _, c=ch: handle_consonant(c),
                        ).props('dense unelevated color=indigo-1 text-color=indigo-9 size=sm')

                ui.label('மாத்திரை / குறியீடுகள் (தேர்ந்தெடுத்த எழுத்துடன்)').classes('text-xs text-gray-600 mt-1')
                with ui.row().classes('flex-wrap gap-1'):
                    for sign in VOWEL_SIGNS:
                        label = f"{selected_base['char']}{sign}" if sign else selected_base['char']
                        btn = ui.button(
                            label,
                            on_click=lambda _, s=sign: insert_text(s),
                        ).props('dense outline color=teal size=sm')
                        sign_buttons[sign] = btn
                    ui.button('Space', on_click=lambda: insert_text(' ')).props('dense flat size=sm')
                    ui.button('Enter', on_click=lambda: insert_text('\n')).props('dense flat size=sm')
                    ui.button('⌫', on_click=backspace_text).props('dense color=negative outline size=sm')

        def sync_file_dropdown_for_mode(check_sandhapa: bool, check_vannapa: bool,
                                        check_marutpa: bool) -> None:
            nonlocal current_files
            current_files = load_files_for_selection(check_sandhapa, check_vannapa, check_marutpa)
            file_select.options = list(current_files.keys())
            if file_select.value not in current_files:
                file_select.value = None
            file_select.update()

        def on_isaipaa_toggle():
            s_checked = bool(sandhapa_cb.value)
            v_checked = bool(vannapa_cb.value)
            m_checked = bool(marutpa_cb.value)
            sync_file_dropdown_for_mode(s_checked, v_checked, m_checked)

            show_isa = s_checked or v_checked or m_checked
            isaipaa_tab.set_visibility(show_isa)
            if show_isa:
                tabs.set_value(isaipaa_tab)
            elif tabs.value == isaipaa_tab:
                tabs.set_value(yaappu_tab)
        
        sandhapa_cb.on_value_change(lambda _: on_isaipaa_toggle())
        vannapa_cb.on_value_change(lambda _: on_isaipaa_toggle())
        marutpa_cb.on_value_change(lambda _: on_isaipaa_toggle())

        def run_analysis():
            text = (textarea.value or '').strip()
            if not text:
                ui.notify('தயவுசெய்து செய்யுளை உள்ளிடவும்.', type='warning')
                return
            any_isaipaa = bool(sandhapa_cb.value or vannapa_cb.value or marutpa_cb.value)
            res = build_analysis(
                text,
                bool(sandhapa_cb.value),
                bool(vannapa_cb.value),
                bool(marutpa_cb.value),
            )
            for key, lbl in tab_panels_map.items():
                lbl.set_text(res.get(key, ''))
            if any_isaipaa:
                isaipaa_tab.set_visibility(True)
                tabs.set_value(isaipaa_tab)
            else:
                tabs.set_value(yaappu_tab)

        def clear_all():
            textarea.set_value('')
            for lbl in tab_panels_map.values():
                lbl.set_text('')

        with ui.row().classes('gap-2'):
            ui.button('யாப்பறி', on_click=run_analysis).props('color=primary')
            ui.button('மீட்டமை', on_click=clear_all).props('outline color=secondary')
            ui.button(
                'வெளியீட்டை சேமி (.txt)',
                on_click=lambda: ui.download(
                    '\n\n'.join(f'--- {k} ---\n{v.text}' for k, v in tab_panels_map.items()).encode('utf-8'),
                    'yaappu_analysis.txt',
                ),
            ).props('outline')

        tab_defs = [
            ('ezhuthu', 'எழுத்து', False),
            ('asai', 'அசை-சீர்-அடி', False),
            ('thalai', 'தளை-ஓசை', False),
            ('seer_thodai', 'சீர்-தொடை', False),
            ('adi_thodai', 'அடி-தொடை', False),
            ('yaappu', 'யாப்பு', True),
            ('details', 'ஆய்வு விவரங்கள்', False),
        ]

        with ui.tabs().classes('w-full') as tabs:
            created_tabs = {}
            for key, title, _ in tab_defs:
                created_tabs[key] = ui.tab(title)
            isaipaa_tab = ui.tab('இசைப்பா')
            isaipaa_tab.set_visibility(False)

        yaappu_tab = created_tabs['yaappu']

        with ui.tab_panels(tabs, value=yaappu_tab).classes('w-full border rounded p-3 min-h-64'):
            for key, _, _ in tab_defs:
                with ui.tab_panel(created_tabs[key]):
                    tab_panels_map[key] = ui.label('').classes('mono-out')
            with ui.tab_panel(isaipaa_tab):
                tab_panels_map['isaipaa'] = ui.label('').classes('mono-out')


port = int(os.environ.get('PORT', 8080))
ui.run(host='0.0.0.0', port=port, reload=False)