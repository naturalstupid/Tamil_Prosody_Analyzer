# coding=utf8
from yaappu.grammar import (
    Yaappu,
    VENPA_SEER_FRACTION,
    VENPA_THALAI_FRACTION,
    VENPA_OSAI_FRACTION,
    ASIRIYAPA_SEER_FRACTION,
    ASIRIYAPA_THALAI_FRACTION,
    ASIRIYAPA_OSAI_FRACTION,
)
from yaappu import utils

"""
    Marutpaa Rules
"""
MARUTPA_MIN_LINES = 4
MARUTPA_DEFAULT_FRACTION = 0.50

_MARUTPA_RULE_1 = "அடி இலக்கணம் (சிறுமை): குறைந்தது 4 அடிகளைக் கொண்டிருத்தல் வேண்டும் (வெண்பா பகுதி + ஆசிரியப்பா பகுதி)."
_MARUTPA_RULE_2 = "முற்பகுதி (வெண்பா இலக்கணம்): தொடக்க அடிகளில் வெண்டளை / செப்பலோசை / நாற்சீர் அமைப்பு மிகுந்து வருதல்."
_MARUTPA_RULE_3 = "பிற்பகுதி (ஆசிரியப்பா இலக்கணம்): இறுதி அடிகளில் ஆசிரியத் தளை / அகவலோசை / ஈரசைச் சீர்கள் மிகுந்து வருதல்."
_MARUTPA_RULE_4 = "வஞ்சியுரிச் சீர் விலக்கு: பிற்பகுதியில் வஞ்சியுரிச் சீர்கள் (கருவிளங்கனி, கூவிளங்கனி) வாராமை."
_MARUTPA_RULE_5 = "ஈற்றுச் சீர் இலக்கணம்: இறுதிச் சீர் ஆசிரியப்பா ஈற்று எழுத்துகளில் (ஏ, என், ஓ, ஈ, ஆய், ஐ) முடிதல்."
_MARUTPA_RULE_6 = "ஈற்றயலடி அமைப்பு: சில மருட்பாக்களில் ஈற்றயலடி சிந்தடியாக (3 சீர்) வருதல்."

"""
    GLOBAL CONSTANTS
"""
GREEN_CHECK = u'\u2714  '
RED_CROSS = u'\u274C  '
GEQ = u' \u2265 '
RULE_CHECK = lambda rc: '\t' + GREEN_CHECK if rc else '\t' + RED_CROSS
PERCENT = "{:.0%}"
PERCENT_2 = "( {:.0%} " + GEQ + " {:.0%} )"


class Marutpa(Yaappu):
    def __init__(
        self,
        text,
        poem_check_fraction=MARUTPA_DEFAULT_FRACTION,
        treat_aaydham_as_kuril=False,
        treat_kutriyaligaram_as_otru=False,
        venpa_line_count = 0,
        asiriyapa_line_count = 0,
    ):
        super().__init__(
            text,
            treat_aaydham_as_kuril=treat_aaydham_as_kuril,
            treat_kutriyaligaram_as_otru=treat_kutriyaligaram_as_otru,
        )
        self.poem_check_fraction = poem_check_fraction

    def _split_portions(self):
        """
        Split lines into (venpaa_lines, asiriyapaa_lines).
        By default, the first half (at least 2 lines) is treated as Venpaa
        and the remaining lines (at least 2 lines) as Asiriyapaa.
        """
        total = self.line_count()
        if total < MARUTPA_MIN_LINES:
            self.venpa_line_count = 0
            self.asiriyapa_line_count = 0
            return [], []

        split_idx = max(2, total // 2)
        if total - split_idx < 2:
            split_idx = total - 2

        self.venpa_line_count = split_idx
        self.asiriyapa_line_count = total - split_idx
        return self.line_objects[:split_idx], self.line_objects[split_idx:]

    @staticmethod
    def _lines_words(lines):
        return [w for line in lines for w in line.words]

    @staticmethod
    def _lines_word_objects(lines):
        return [w for line in lines for w in line.word_objects]

    def _lines_seergal(self, lines, check_eetrucheer_for_venpaa=False):
        word_objs = self._lines_word_objects(lines)
        if not word_objs:
            return []
        seers = [w.seer_type() for w in word_objs]
        if check_eetrucheer_for_venpaa:
            seers[-1] = word_objs[-1].venpaa_seer()
        return seers

    def _lines_thalaigal(self, lines, include_sub_type=True):
        word_objs = self._lines_word_objects(lines)
        if len(word_objs) < 2:
            return []
        return [
            word_objs[i].thaLai_type(word_objs[i + 1].text(), include_sub_type)
            for i in range(len(word_objs) - 1)
        ]

    def _lines_osaigal(self, lines, include_sub_type=True):
        thalaigal = self._lines_thalaigal(lines, include_sub_type=include_sub_type)
        osai_arr = utils.OSAI_TYPES if include_sub_type else utils.OSAI_TYPES_SHORT
        return [osai_arr.get(t) for t in thalaigal if t]

    def _check_venpaa_portion(self, venpaa_lines, expected_fraction=None):
        """
        Checks the opening Venpaa portion of a Marutpaa.
        Returns (portion_ok, details_str).
        """
        if expected_fraction is None:
            expected_fraction = min(self.poem_check_fraction, VENPA_THALAI_FRACTION)

        if not venpaa_lines:
            return False, RULE_CHECK(False) + _MARUTPA_RULE_2 + " (அடிகள் இல்லை)\n"

        seers = self._lines_seergal(venpaa_lines, check_eetrucheer_for_venpaa=False)
        thalaigal = self._lines_thalaigal(venpaa_lines)
        osaigal = self._lines_osaigal(venpaa_lines)

        seer_ok, seer_frac = utils.has_required_percentage_of_occurrence(
            seers, utils.VENPA_ALLOWED_SEERS, expected_fraction
        )
        thalai_ok, thalai_frac = utils.has_required_percentage_of_occurrence(
            thalaigal, utils.VENPA_ALLOWED_THALAI, expected_fraction
        )
        osai_ok, osai_frac = utils.has_required_percentage_of_occurrence(
            osaigal,
            ["தூங்கிசைச் செப்பலோசை", "ஏந்திசைச் செப்பலோசை"],
            expected_fraction,
        )
        line_seer_ok = all(line.word_count() == 4 for line in venpaa_lines)

        portion_ok = seer_ok and thalai_ok and osai_ok and line_seer_ok

        details = ""
        details += (
            RULE_CHECK(portion_ok)
            + _MARUTPA_RULE_2
            + f" [சீர்: {PERCENT_2.format(seer_frac, expected_fraction)}, "
            + f"தளை: {PERCENT_2.format(thalai_frac, expected_fraction)}, "
            + f"ஓசை: {PERCENT_2.format(osai_frac, expected_fraction)}]\n"
        )
        return portion_ok, details

    def _check_asiriyapa_portion(self, asiriyapa_lines, expected_fraction=None):
        """
        Checks the closing Asiriyapaa portion of a Marutpaa.
        Returns (portion_ok, eetru_ok, details_str).
        """
        if expected_fraction is None:
            expected_fraction = self.poem_check_fraction

        if not asiriyapa_lines:
            return False, False, RULE_CHECK(False) + _MARUTPA_RULE_3 + " (அடிகள் இல்லை)\n"

        seers = self._lines_seergal(asiriyapa_lines, check_eetrucheer_for_venpaa=True)
        thalaigal = self._lines_thalaigal(asiriyapa_lines)
        osaigal = self._lines_osaigal(asiriyapa_lines)
        words = self._lines_words(asiriyapa_lines)

        seer_ok, seer_frac = utils.has_required_percentage_of_occurrence(
            seers, utils.ASIRIYAPPA_ALLOWED_SEERS, expected_fraction
        )
        thalai_ok, thalai_frac = utils.has_required_percentage_of_occurrence(
            thalaigal,
            ["நேரொன்றிய ஆசிரியத்தளை", "நிரையொன்றிய ஆசிரியத்தளை"],
            expected_fraction,
        )
        osai_ok, osai_frac = utils.has_required_percentage_of_occurrence(
            osaigal,
            ["ஏந்திசை அகவலோசை", "தூங்கிசை அகவலோசை"],
            expected_fraction,
        )
        has_disallowed_seer, disallowed_frac = utils.has_required_percentage_of_occurrence(
            seers, utils.ASIRIYAPPA_DISALLOWED_SEERS, 0.01
        )
        disallowed_ok = not has_disallowed_seer

        last_word = words[-1] if words else ""
        last_char = last_word[-1] if last_word else ""
        eetru_ok = utils.list_has_element(utils.ASIRIYAPPA_EETRUCHEER_LETTERS, last_char)

        portion_ok = seer_ok and thalai_ok and osai_ok and disallowed_ok

        details = ""
        details += (
            RULE_CHECK(portion_ok)
            + _MARUTPA_RULE_3
            + f" [சீர்: {PERCENT_2.format(seer_frac, expected_fraction)}, "
            + f"தளை: {PERCENT_2.format(thalai_frac, expected_fraction)}, "
            + f"ஓசை: {PERCENT_2.format(osai_frac, expected_fraction)}]\n"
        )
        details += (
            RULE_CHECK(disallowed_ok)
            + _MARUTPA_RULE_4
            + PERCENT_2.format(disallowed_frac, 0.0)
            + "\n"
        )
        details += (
            RULE_CHECK(eetru_ok)
            + _MARUTPA_RULE_5
            + (f" ({last_word})" if last_word else "")
            + "\n"
        )
        return portion_ok, eetru_ok, details

    def check_for_marutpaa(
        self,
        expected_seer_fraction=None,
        expected_thaLai_fraction=None,
        expected_osai_fraction=None,
    ):
        """
        Return arguments:
            [paa_check, poem_type, paa_str]
        """
        paa_check = True
        poem_type = "மருட்பா"
        header = poem_type + " யாப்பிலக்கண விதிகள்\n"
        body = ""

        fraction = (
            expected_thaLai_fraction
            if expected_thaLai_fraction is not None
            else (
                expected_seer_fraction
                if expected_seer_fraction is not None
                else (
                    expected_osai_fraction
                    if expected_osai_fraction is not None
                    else self.poem_check_fraction
                )
            )
        )

        try:
            min_lines_ok = self.line_count() >= MARUTPA_MIN_LINES
            paa_check = paa_check and min_lines_ok
            body += (
                RULE_CHECK(min_lines_ok)
                + _MARUTPA_RULE_1
                + f" ({self.line_count()} அடிகள்)\n"
            )

            venpaa_lines, asiriyapa_lines = self._split_portions()

            venpaa_ok, venpaa_details = self._check_venpaa_portion(
                venpaa_lines, expected_fraction=fraction
            )
            paa_check = paa_check and venpaa_ok
            body += venpaa_details

            asiriyapa_ok, eetru_ok, asiriyapa_details = self._check_asiriyapa_portion(
                asiriyapa_lines, expected_fraction=fraction
            )
            paa_check = paa_check and asiriyapa_ok and eetru_ok
            body += asiriyapa_details

            if self.line_count() >= 2:
                penultimate_sindhadi = self.line_objects[-2].word_count() == 3
                body += RULE_CHECK(penultimate_sindhadi) + _MARUTPA_RULE_6 + "\n"
                if paa_check and penultimate_sindhadi:
                    poem_type = "சிந்தடி ஈற்றயலடி மருட்பா"
                if self.asiriyapa_line_count > self.venpa_line_count:
                    poem_type += " (வியனிலை மருட்பா)"
                else:
                    poem_type += " (சமநிலை மருட்பா)"
            status_line = (
                "மருட்பா விதிகள் "
                + ("பொருந்துகிறது." if paa_check else "பொருந்தவில்லை.")
                + "\n"
                + f"வெண்பா அடிகள் = {self.venpa_line_count} ஆசிரியப்பா அடிகள் = {self.asiriyapa_line_count}\n"
            )
            paa_str = status_line + header + body
            return [paa_check, poem_type, paa_str]
        except Exception:
            status_line = "மருட்பா விதிகள் பொருந்தவில்லை.\n"
            return [False, poem_type, status_line + header + body]


if __name__ == "__main__":
    sample_poem = """திருநுதல் வேர்அரும்பும் தேங்கோதை வாடும்
இருநிலனும் சேவடி எய்தும் - அரிபரந்த
போகுஇதழ் உண்கண் இமைக்கும்
ஆகும் மற்றிவள் அகலிடத்து அணங்கே."""
    sample_potem = """பருந்தளிக்கு முத்தலைவேல் பண்ணவற்கே அன்றி
விருந்தளிக்கும் விண்ணோர் பிறர்க்கும் - திருந்த
வலனுயர் சிறப்பின் மன்ற வாணனக்
குலமுனி புதல்வனுக் கீந்த
அலைகட லாகுமிவ் வாயிழை நோக்கே"""
    ty = Yaappu(sample_poem)
    results, _ = ty.analyze(get_individual_poem_analysis=False)
    for item in results[1:]:
        print(item)

    mp = Marutpa(sample_poem)
    paa_check, poem_type, paa_str = mp.check_for_marutpaa()
    print(sample_poem)
    print(paa_check, "\n", poem_type, "\n", paa_str)