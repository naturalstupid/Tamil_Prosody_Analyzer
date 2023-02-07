# coding=utf8
from yaappu.grammar import Yaappu
from yaappu import utils
""" Sandhapaa Rules """
_SANDHAPA_RULE_1 = "எல்லா அடிகளிலும் மாத்திரை அளவு ஒன்றாக இருக்க வேண்டும்\n"+ \
                      "\tகுறில்  = ஒரு மாத்திரை, (குறிலொற்று, நெடில், நெடிலொற்றுகள் ) = இரண்டு மாத்திரை\n"+ \
            "\tஇடைச்சொற்களில் (\"ய்\",\"ர்\",\"ல்\",\"வ்\",\"ழ்\",\"ள்\",) சீர் நடுவே வந்தாலோ \n"+ \
                      "\tஅல்லது (\"ய்\",\"ர்\",\"ண்\",\"ன்\",) சீர் முடிவில் வந்தாலோ மாத்திரை கிடையாது."
_SANDHAPA_RULE_2 = "எல்லா அடிகளிலும் சீர் அமைப்பு ஒன்றாக இருக்க வேண்டும்"
"""
    GLOBAL CONSTANTS
"""
GREEN_CHECK = u'\u2714  '
RED_CROSS = u'\u274C  '
GEQ = u' \u2265 '
RULE_CHECK = lambda rc : '\t' + GREEN_CHECK if rc else '\t' + RED_CROSS
PERCENT = "{:.0%}"
PERCENT_2 = "( {:.0%} " + GEQ + " {:.0%} )"
class Sandhapa(Yaappu):
    def __init__(self, text): #, treat_aaydham_as_kuril=False, treat_kutriyaligaram_as_otru=False):
        super().__init__(text)
        
    def duration(self):
        _duration = []
        for l in range(self._line_count):
            line = self.line_objects[l]
            word_count = line.word_count()
            for w in range(word_count):
                last_word = (w == word_count-1)
                _duration.append(line.word_objects[w].sandha_duration(paa_type = "Sandhapa", last_word=last_word))
        return _duration

    def sandha_kuzhippu(self):
        _sandha_kuzhippu_list = []
        for l in range(self._line_count):
            line = self.line_objects[l]
            word_count = line.word_count()
            for w in range(word_count):
                last_word = (w == word_count-1)
                _sandha_kuzhippu_list.append(line.word_objects[w].sandha_kuzhippu(paa_type = "Sandhapa", last_word=last_word))
        return _sandha_kuzhippu_list
        
    def duration_old(self):
        _duration = 0.0
        for word in range(self._words):
            _duration += word.sandha_duration()
        return _duration
    def check_for_sandhapaa(self):
        import numpy as np
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'சந்தப்பா'
        paa_str = poem_type + " இசைப்பாவியல் - சந்தப்பா விதிகள்" + '\n'
        """ _VANNAPA_RULE_1 """
        len_arr = [line.word_count() for line in self.line_objects]
        duration_2d = np.array(utils.convert_1d_list_to_2d(self.duration(),len_arr),dtype=object)
        duration_check = all(np.array_equal(duration_2d[0], duration_2d[i]) for i in range(1,len(duration_2d)))
        paa_str += RULE_CHECK(duration_check) + _SANDHAPA_RULE_1 + '\n\t'
        paa_str += np.array2string(duration_2d) + "\n"
        paa_check = duration_check
        paa_str = "சந்தப்பா விதிகள் " + ("பொருந்துகிறது." if (paa_check) else "பொருந்தவில்லை.") + "\n" + paa_str

        return [paa_check, poem_type, paa_str]
    
    def __check_for_sandhapaa_old(self):
            import numpy as np
            len_arr = [line.word_count() for line in self.line_objects]
            _duration_2d = np.array(utils.convert_1d_list_to_2d(self.duration(),len_arr),dtype=object)
            _is_sandha_paa = all(np.array_equal(_duration_2d[0], _duration_2d[i]) for i in range(1,len(_duration_2d)))
            return _is_sandha_paa

if __name__ == '__main__':
    """
    song = "விடமார் பணிபுலி வானோர் தொழவளர்\n"+ \
            "புலியூர்ச் சபையினி னடித்து நின்றன\n"+ \
            "வெறியார் நறுமலர் தேனோ டுறைதலி\n"+ \
            "னறுகாற் பறவைக ளிரைத்தெ ழுந்தன" 
    """
    """
    song = "ஊனு யர்ந்தவு ரத்தினான் \n" + \
"மேனி மிர்ந்தமி டுக்கினான் \n" + \
"தானு யர்ந்தத வத்தினான் \n" + \
"வானு யர்ந்தவ ரத்தினான்"
    """
    """
    song = "கைத்தோ டுஞ்சிறை கற்போயை \n"+ \
"வைத்தா னின்னுயிர் வாழ்வானாம் \n"+ \
"பொய்த்தோர் வில்லிகள் போவாராம் \n"+ \
"இத்தோ டொப்பது யாதுண்டே"
    """
    #"""
    song = "பொன்னி லங்கு பூங்கொ டிப்பொ லஞ்செய் கோதை வில்லிட\n" + \
"மின்னி லங்கு மேக லைகள் ஆர்ப்ப ஆர்ப்ப எங்கணும்\n" + \
"தென்ன வாழ்க வாழ்க என்று சென்று பந்த டித்துமே\n" + \
"தேவ ரார மார்பன் வாழ்க என்று பந்த டித்துமே"
    #"""
    #"""
    song ="குரக்கி னப்ப டைகொ டுகு  ரைக டலின் மீதுபோய்\n" + \
"அரக்க ரங்க ரங்க வெஞ்ச  ரந்து ரந்த வாதிநீ\n" + \
"இரக்க மண்கொ டுத்த வற்கி ரக்க மொன்று மின்றியே\n" + \
"பரக்க வைத்த ளந்து கொண்ட பற்ப பாத னல்லையே"
    #"""
    tp = Yaappu(song)
    results,_ = tp.analyze(get_individual_poem_analysis=False)
    for line in results[1:]:
        print(line)
    tp = Sandhapa(song)
    paa_check, poem_type, paa_str = tp.check_for_sandhapaa()
    print(song)
    print(paa_check,"\n", poem_type,"\n", paa_str)
    exit()
    print(utils.get_character_type_counts(tp.text()))
    has_sandha_ozhungu, sandha_ozhungu, actual_fraction = tp.has_sandha_ozhungu(1.0)
    print(has_sandha_ozhungu, sandha_ozhungu, actual_fraction)
    print(tp.check_for_sandhapaa())
    len_arr = [line.word_count() for line in tp.line_objects]     
    seergal_2d = (utils.convert_1d_list_to_2d(tp.seergaL(),len_arr))
    sandha_kuzhippu_2d = (utils.convert_1d_list_to_2d(tp.sandha_kuzhippu(),len_arr))
    duration_2d = (utils.convert_1d_list_to_2d(tp.duration(),len_arr))
    for l in range(tp.line_count()):
        line = tp.line_objects[l]
        line_duration_str = ''
        print(line.words)
        print(seergal_2d[l])
        print(sandha_kuzhippu_2d[l])
        print(duration_2d[l])
        #for word in line.word_objects:
        #    line_duration_str += word.text() +'('+str(word.sandha_duration())+') '
        #print(line_duration_str)
        