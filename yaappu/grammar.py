import utils
import string
"""
    TODO: Treat Aaydham as Kuril
    TODO: Handle Kutriyaligaram (e.g. அருளல்ல (தியா)தெனிற்  - treat or ignore "தி"
"""
"""
    VenPaa Rules 
"""
    
VENPA_RULE_FAC = 1.00
_VENPA_RULE_1 = "சீர் இலக்கணம் - ஈற்றடியின் ஈற்றுச்சீரைத் தவிர்த்து ஈரசைச்சீர்களும் காய்ச்சீர்களும் மட்டுமே பயின்று வருதல் வேண்டும்."
_VENPA_RULE_2 = "தளை இலக்கணம் - வெண்டளைகள் மட்டுமே பயின்று வருதல் வேண்டும்."
_VENPA_RULE_3 = "அடி இலக்கணம் - ஈற்றடி மூன்று சீர்களும் ஏனைய அடிகள் நான்கு சீர்களும் கொண்டிருத்தல் வேண்டும்."
_VENPA_RULE_4 = "ஓசை இலக்கணம் - செப்பலோசை மிகுந்து வரும்."
_VENPA_RULE_5 = "ஈற்றுச் சீர் இலக்கணம்  - ஈற்றடியின் ஈற்றுச்சீர் நாள், மலர், காசு, பிறப்பு ஆகியவற்றுள் இருத்தல் வேண்டும்."
_VENPA_KURAL_RULE_1 = "\t\tகுறள் வெண்பா - இரண்டடிகளால்     வரும். அதாவது, முதலடி அளவடியாகவும் இரண்டாமடி சிந்தடியாகவும் அமையும்."
_VENPA_NERISAI_RULE_1 = "\t\tநேரிசை வெண்பா -இரண்டாவது அடியில் தனிச்சொல் எதுகை அமைவது "
_VENPA_INNISAI_RULE_1 = "\t\tஇன்னிசை வெண்பா-இரண்டாவது அடியில் தனிச்சொல் எதுகை அமைந்திராது."
_VENPA_PAHRODAI_RULE_1 = "\t\tபஃறொடை வெண்பா - நான்கடிக்கு மேற்பட்ட பல அடிகளால் வரும்."
_VENPA_SINDHIYAL_RULE_1 = "\t\tசிந்தியல் வெண்பா - மூன்றடியால் வருவது"
"""
    Asiryappaa rules
"""
ASIRIYAPA_RULE_FRACTION = 0.45
ASIRIYAPA_SANDHA_OZHUNGU_FRACTION = 0.50
_ASIRIYAPA_RULE_1 = "சீர் இலக்கணம் -   ஈரசைச் சீர்கள் மிகுந்து வரும். (தேமா புளிமா கூவிளம் கருவிளம்) "
_ASIRIYAPA_RULE_2 = "சீர் இலக்கணம் - வஞ்சியுரிச் சீர்கள் (கருவிளங்கனி, கூவிளங்கனி) வராது."
_ASIRIYAPA_RULE_3 = "ஈற்றுச் சீர் - இலக்கணம்  - ஏ, என், ஓ, ஈ, ஆய், ஐ   - என முடியும்"
_ASIRIYAPA_RULE_4 = "தளை இலக்கணம் - ஆசிரியத் தளைகள் மிகுந்து வரும்."
_ASIRIYAPA_RULE_5 =  "ஓசை இலக்கணம் - அகவலோசை மிகுந்து வரும்."
_ASIRIYAPA_RULE_6 = "அடி - இலக்கணம்  - அடியின் வரையரை  (அதிகபட்சம்) - அளவடி"
_ASIRIYAPA_RULE_INAIKURAL_1 = "    இணைக்குறள் ஆசிரியப்பா - முதலடியும் கடைசி அடியும் அளவடிகளாகவே வரும். \n" \
                            + "             இடையே அளவடிகளோடு குறளடிகளும் சிந்தடிகளும் கலந்து வரும்."
_ASIRIYAPA_RULE_NERISAI_1 = "    நேரிசை ஆசிரியப்பா - ஈற்றயலடி சிந்தடியாய, ஏனைய அடிகள் அளவடிகளாய் வரும்"
_ASIRIYAPA_RULE_NILAMANDILA_1 = "    நிலை மண்டில ஆசிரியப்பா - எல்லா அடிகளும் அளவடிகளாக வருவது."
"""
    Kalipaa Rules
"""
KALIPA_RULE_FRACTION = 0.35 #0.45
KALIPA_SANDHA_OZHUNGU_FRACTION = 0.50
KALIPA_THALAI_FRACTION = 0.50
_KALIPA_RULE_1="சீர் இலக்கணம் -   நிறை முதல் சீர் (தேமாங்காய், புளிமாங்காய், கூவிளங்காய், கருவிளங்காய் மிகுந்து வரும்."
_KALIPA_RULE_2="சீர் இலக்கணம் - நேர் ஈற்றுச் சீர் (தேமா, புளிமா) வராது. நிறை நடுச் சீர் (கருவிளங்கனி, கூவிளங்கனி) வராது."
_KALIPA_RULE_3="தளை இலக்கணம் - கலித்தளைகள் மிகுந்து வரும்."
_KALIPA_RULE_4="ஓசை இலக்கணம் - துள்ளலோசை மிகுந்து வரும்.";
_KALIPA_RULE_5="அடி - இலக்கணம்  - அடியின் வரையரை  அளவடி. ஈற்றடி சிந்தடி வரலாம்."

"""
    VANJIPAA Rules
"""
VANJIPA_RULE_FRACTION = 0.25
_VANJIPA_RULE_1 = "சீர் இலக்கணம் - பெரும்பான்மை கனிச் சீர்கள்.  சிறுபான்மை காய்ச் சீர்கள் "
_VANJIPA_RULE_2 = "தனிச்சொற்கள் தேமா, புளிமா, கூவிளம், கருவிளம் (ஆசிரியச் சுரிதகம்) அசைகளில் அமையும்."
_VANJIPA_RULE_3 = "தளை இலக்கணம் - ஒன்றிய வஞ்சித் தளையும் ஒன்றாத வஞ்சித்  தளையும்  பெரும்பான்மை. "
_VANJIPA_RULE_4 = "ஓசை இலக்கணம் - தூங்கலோசை மிகுந்து வரும்."
_VANJIPA_RULE_5 = "தனிச்சொல்லை அடுத்து இரண்டு அடிகளே வரும் (சுரிதகம்)."
_VANJIPA_RULE_6 = "அடி - இலக்கணம் - முழுமையும் குறளடி அல்லது முழுமையும் சிந்தடி, தனிச்சொல் வரை பெற்றிருக்கும்."
_VANJIPA_KURALADI = "\t\tதனிச்சொல் முன்பு வரை இரண்டடிகள் இருந்ததால் குறளடி."
_VANJIPA_SINDHADI = "\t\tதனிச்சொல் முன்பு வரை மூன்றடிகள் இருந்ததால் சிந்தடி."

_VENPAVINAM_KURAL_THAZHISAI = "குறள்  தாழிசை:\n\t\tஇரண்டடியாய் வரும்.  முதலடி நான்கிற்கும் அதிக சீர்களை பெற்று ஈற்றடி அதைவிட சில சீர்கள் குறைவாக பெற்றிருக்கும். "
_VENPAVINAM_KURAL_THURAI = "குறள் துறை:\n\t\tஇரண்டடி பெற்று இரண்டும் சம சீர்களைப் பெற்றிருக்கும்."
_VENPAVINAM_VEN_THURAI = "வெண்டுறை :\n\t\tமூன்றடி முதல் ஏழடி வரை பெற்றிருக்கும்.\n" + \
                         "\t\tமுதலில் வரும் அடிகளை விட பின்னர் வரும் அடிகள் சீர்கள் குறைவாகக் கொண்டிருக்கும்."                         
_VENPAVINAM_VEN_THAZHISAI = "வெண் தாழிசை:\n\t\tமூன்றடிகள் பெற்று, முதல் இரண்டு அடிகளும் அளவடி ஆகவும் ஈற்றடி சிந்தடி ஆகவும் இருக்கும்."
_VENPAVINAM_VELI_VIRUTHAM = "வெளி விருத்தம்:\n\t\tமூன்று அல்லது நான்கு அடிகளாய் வரும்.\n" + \
                            "\t\tஒவ்வோர் அடி இறுதியிலும் நான்கு சீர்களைத் தாண்டி ஒரு தனிச்சொல் வரும்."
_ASIRIYAPA_THAZHISAI = "ஆசிரியத் தாழிசை:\n\t\tமூன்றடியாய் வந்து சீர் எண்ணிக்கையால் ஒத்து வரும்."
_ASIRIYAPA_THURAI = "ஆசிரியத் துறை:\n\t\tநான்கடியாய் ஈற்றயலடி குறைந்து வரும்\n" + \
                    "\t\tஇடையே வரும் அடிகள் இடைமடக்காகவும் (வந்த அடியே திரும்பவும் அடுத்த அடியில் வருதல்) வரும்.\n" + \
                    "\t\tநான்கடியாய் இடையிடை குறைந்து வருவதும் உண்டு\n" + \
                    "\t\tநான்கடியாய் இடையிடை குறைந்து இடைமடக்காக வருவதும் உண்டு."
_ASIRIYAPA_VIRUTHAM = "ஆசிரிய விருத்தம்:\n\t\tநான்கு கழி நெடிலடிகளால் ஆகி, நான்கடியும் அளவொத்து வரும்.\n" + \
                        "\t\tகழி நெடிலடிகள் என்பதனால் ஐந்துக்கும் மேற்பட்ட எத்தனை சீர்களும் வரலாம்.\n" + \
                        "\t\tநான்கடியும் ஒரே எதுகை அமைப்பைப் பெற்றிருக்க வேண்டும் (ஒரே சீர் அமைப்பைப் பெற்றிருப்பது).\n" + \
                        "\t\tநான்கடியும் ஒரே சந்த ஒழுங்கைப்  பெற்றிருக்க வேண்டும்."
                
_KALIPA_THAZHISAI = "கலித்தாழிசை:\n\t\tஇரண்டு அல்லது மேற்பட்ட அடிகளால் வரும்.\n" + \
                "\t\tஈற்றடி சற்று நீண்டு ஏனைய அடிகள் சீர் எண்ணிக்கையில் ஒத்து/ஒவ்வாது வரும்."
_KALIPA_KATTALAI_THURAI = "கட்டளைக் கலித்துறை:\n\t\tநெடிலடி நான்காய் வரும்.\n" + \
                "\t\tமுதல் நான்கு சீர்களும் வெண்டளை அமைந்து வரும்.\n" + \
                "\t\tஈற்றடியின் ஈற்றுச் சீர் ஏகாரத்தில் முடியும்"
_KALIPA_KALI_THURAI = "கலித்துறை:\n\t\tநெடிலடி நான்காய் வரும்.\n" + \
                "\t\tநான்கடிகளும் எதுகை அமைப்பில் ஒன்றியிருக்கும்."
_KALIPA_VIRUTHAM = "கலி விருத்தம்:\n\t\tநான்கு அளவடிகளால் ஆகி, நான்கடியும்  நாற்சீராய் அளவொத்து வரும்.\n" + \
                "\t\tநான்கடியும் ஒரே எதுகை அமைப்பைப் பெற்றிருக்க வேண்டும் (ஒரே சீர் அமைப்பைப் பெற்றிருப்பது).\n" + \
                "\t\tநான்கடியும் ஒரே சந்த ஒழுங்கைப்  பெற்றிருக்க வேண்டும்."

_VANJIPA_THAZHISAI = "வஞ்சித் தாழிசை:\n\t\tகுறளடி நான்காய் வரும்.\n" + \
                "\t\tவஞ்சித்  தாழிசை ஒரு பொருள் மேல் மூன்றடுக்கி  மட்டுமே வரும். தனியே வராது.\n" \
                + "\t\tதனியே வரின் வஞ்சித் துறையாகி விடும்.\n" \
                + "\t\tஅடுக்கி வருதல்: 4, 8, 12 ஆம் அடிகளின் இறுதிச்சீர்  ஒன்றாய் இருக்கும்."
_VANJIPA_THURAI = "வஞ்சித்  துறை:\n\t\tகுறளடி நான்கு தனித்து வருவது வஞ்சித்துறை.\n" + \
                "\t\tபல்வேறு ஓசை அமைப்புகளில் வரும்."
_VANJIPA_VIRUTHAM = "வஞ்சி விருத்தம்:\n\t\tசிந்தடி நான்கு தனித்து வருவது வஞ்சி விருத்தம்.\n"+ \
                "\t\tபல்வேறு ஓசை அமைப்புகளில் வரும்."
GREEN_CHECK = u'\u2714  '
RED_CROSS = u'\u274C  '
GEQ = u' \u2265 '
RULE_CHECK = lambda rc : '\t' + GREEN_CHECK if rc else '\t' + RED_CROSS
PERCENT = "{:.0%}"
class Ezhuthu(object):
    """ 
        Class for Tamil Character
        Methods: 
            is_kuril() - to check whether ezhuthu is kuril
            is_nedil() - to check whether ezhuthu is nedil
            is_otru() - to check whether ezhuthu is otru
            is_aaytham() - to check whether ezhuthu is aaydham
            is_aikaaram() - to check whether ezhuthu is aikaaram
            is_aukaaram() - to check whether ezhuthu is aukaaram
    """
    def __init__(self, tamil_char):
        self.set_text(tamil_char)
        self._index = 0
        self.set_duration(0.0)
        self._is_kuril = utils.list_has_element(utils.KURILGAL, self._text)
        self._is_nedil = utils.list_has_element(utils.NEDILGAL, self._text)
        self._is_otru = utils.list_has_element(utils.MEYGAL, self._text)
        self._is_kutriyalugaram = False
        self._is_kutriyaligaram = False
        self._is_magarakurukkam = False
        self._is_aaydham = self.is_aaydham()
        if self._is_nedil:
            self._duration = 2.0
        elif self._is_kuril:
            self._duration = 1.0
        elif (self.is_aikaaram() or self.is_aukaaram()):
            self._duration = 1.5
        elif self._is_otru or self.is_aaydham():
            self._duration = 0.5
            
    def set_text(self, text):
        self._text = text
    
    def text(self):
        return self._text
    
    def set_index(self, index):
        self._index = index
    
    def index(self):
        return self._index
    
    def set_duration(self, duration):
        self._duration = duration
    
    def duration(self):
        return self._duration
    
    def is_aikaaram(self):
        return utils.list_has_element(utils.AIKAARAM, self._text)
    
    def is_aukaaram(self):
        return utils.list_has_element(utils.AUKAARAM, self._text)

    def set_kuril(self, b):
        self._is_kuril = b
        
    def is_kuril(self):
        return self._is_kuril  
    
    def set_nedil(self, b):
        self._is_nedil = b
        #print(self._text,'is nediil',self._is_nedil)
        
    def is_nedil(self):
        return self._is_nedil
    
    def is_otru(self):
        return self._is_otru
    
    def set_otru(self, b):
        self._is_otru = b
        
    def is_kutriyalugaram(self):
        return self._is_kutriyalugaram
    
    def set_kutriyalugaram(self, b):
        self._is_kutriyalugaram = b
        if self._is_kutriyalugaram :
            self.set_duration(0.5)
    
    def is_kutriyaligaram(self):
        return self._is_kutriyaligaram
    
    def set_kutriyaligaram(self, b):
        self._is_kutriyaligaram = b
        if self._is_kutriyaligaram :
            self.set_duration(0.5)
            if utils._TREAT_KUTRIYALIGARAM_AS_OTRU:
                self.set_otru(True)
                self.set_kuril(False) 

    def is_aaydham(self):
        self._is_aaydham = self._text == utils.AYDHAM
        if self._is_aaydham:
            self.set_kuril(utils._TREAT_AAYDHAM_AS_KURIL)
        return self._is_aaydham
    
    def is_vada_ezhuthu(self):
        return utils.list_has_element(utils.VADA_EZHUTHUKKAL, self._text)
    
    def is_vallinam(self):
        return utils.list_has_element(utils.VALLINAM, self._text)
    
    def is_mellinam(self):
        return utils.list_has_element(utils.MELLINAM, self._text)
    
    def is_yidaiyinam(self):
        return utils.list_has_element(utils.YIDAIYINAM, self._text)
    
    def is_uyir_ezhuthu(self):
        return utils.list_has_element(utils.UYIRGAL, self._text)
    
    def is_mey_ezhuthu(self):
        return utils.list_has_element(utils.MEYGAL, self._text)
    
    def is_uyir_mey_ezhuthu(self):
        return utils.list_has_element(utils.UYIR_MEY_LETTERS, self._text)

    def is_magarakurukkam(self):
        return self._is_magarakurukkam
    
    def set_magarakurukkam(self, b):
        self._is_magarakurukkam = True

"""
    class for Tamil Word
"""
class Sol(object):
    SEPARATOR = '/'
    def __init__(self,tamil_word):
        self.original_text = tamil_word
        self._text=''
        self._asai_word = ""
        self.characters = []
        self.tamil_char_objects = []
        self._asaigaL = ''
        self._seer_count = 0
        self._seer_type = ""
        self._thaLai_type = ""
        self._osai_type = ""
        if tamil_word != '' or tamil_word != "":
            self.set_text(tamil_word)
        #print('tamil word',tamil_word)
    
    def duration(self):
        _duration = 0.0
        for c in range(self.character_count):
            tc = self.tamil_char_objects[c]
            tChar = self.characters[c]
            if c == 0 and (tc.is_aikaaram() or tc.is_aukaaram()):  ## AIKAARAM and AUKAARAM
                tc.set_duration(1.5)
                tc.set_nedil(True)
                tc.set_kuril(False)
            if c == self.character_count-1 and utils.list_has_element(utils.KUTRIYALUGARAM, tChar): # Kutriyalugaram
                tc.set_kutriyalugaram(True)
            if c >= 0 and c < self.character_count-1 and utils.list_has_element(utils.KUTRIYALIGARAM, tChar) \
                and utils.list_has_element(utils.YAGARA_VARISAI, self.characters[c+1]): # Kutriyaligaram
                #and self.characters[c+1] == "யா": # Kutriyaligaram
                #print('setting kutriyaligaram',tChar,self.characters[c+1])
                tc.set_kutriyaligaram(True)
            if tChar == 'ம்': # Magarakurukkam
                if c < self.character_count - 1 and utils.list_has_element(utils.VAGARA_VARISAI, self.characters[c+1]):
                    tc.set_magarakurukkam(True)
                    tc.set_duration(0.25)
                elif c > 0  and  utils.list_has_element({'ன்', 'ண்'},self.characters[c-1]):
                    tc.set_magarakurukkam(True)
                    tc.set_duration(0.25)
            _duration += tc.duration()
        if ''.join(self.characters[:3])=='நுந்தை': #special kutriyalugara word from tholkaapiyam
            self.tamil_char_objects[0].set_kutriyalugaram(True)   
        return _duration
        
    def text(self):
        return self._text
    
    def set_text(self, tamil_word):
        if ' ' in tamil_word:
            for word in tamil_word.split(' ') : self.set_text(word) 
        else:
            self._text = tamil_word
            import regex
            tamil_word = regex.sub('\{P}','',tamil_word)
            #print('word',tamil_word)
            self.characters = utils.get_unicode_characters(tamil_word)
            self.character_count = len(self.characters)
            for tc in self.characters:
                tamil_char  = Ezhuthu(tc)
                index = self.characters.index(tc)
                tamil_char.set_index(index)
                self.tamil_char_objects.append(tamil_char)
            if ''.join(self.characters[:3])=='நுந்தை': #special kutriyalugara word from tholkaapiyam
                self.tamil_char_objects[0].set_kutriyalugaram(True)   
            self.duration()
            self._asaigaL = self.asaigaL()
            self._seer_type= self.seer_type()
    
    def _get_nko_string(self):
        self._nko_str = ''
        for tc in self.tamil_char_objects:
            if tc.is_nedil():
                self._nko_str += 'N'
            elif tc.is_kuril():
                self._nko_str += 'K'
            elif tc.is_otru():
                self._nko_str += 'O'
            else:
                self._nko_str += ''
        return self._nko_str
            
    
    def asaigaL(self, separator=SEPARATOR):
        if (self._asaigaL):
            return self._asaigaL
        nko = self._get_nko_string()
        s = 0
        self._asaigaL = ''
        self._asai_word = ''
        #print('len(nko)',len(nko))
        while s <= len(nko):
            #print('s=',s)
            for i in range(len(utils.ASAI_DICT),0,-1):
                key = nko[s:s+i]
                #print('i=',i,key)
                if len(nko) < (s+i):
                    #print('len(nko) < (s+i) - continue')
                    continue
                if key in utils.ASAI_DICT[i-1].keys():
                    self._asaigaL += utils.ASAI_DICT[i-1].get(key)+separator
                    aw = ''.join(self.characters[s:s+i])
                    self._asai_word += aw + separator
                    #print('asaiword',aw, self._asai_word)
                    #print('self._asaigal',self._asaigaL)
                    s = s + i-1
                    break
            s = s + 1
        if self._asaigaL:
            if (self._asai_word[-1] == separator):
                self._asai_word = self._asai_word[:-1]
            if (self._asaigaL[-1] == separator):
                self._asaigaL = self._asaigaL[:-1]
        return self._asaigaL
    
    def set_asai_word(self, asai_word):
        self._asai_word = asai_word
           
    def asai_word(self):
        #print('self._asai_word before',self._asai_word)
        if self._asai_word:
            return self._asai_word
        #print(' calling asaigal')
        self._asaigaL = self.asaigaL()
        #print('self._asai_word after',self._asai_word)
        return self._asai_word
    
    def seer_type(self,separator=SEPARATOR):
        if not self._asaigaL:
            self.asaigaL(separator)
        self._seer_count = self._asaigaL.count(separator)+1
        asai_str = self._asaigaL.replace(separator,' ')
        self._seer_type = utils.SEER_TYPES[self._seer_count-1].get(asai_str)
        #print('seer_count',seer_count,'asai_str',asai_str,'self.seer_type',self._seer_type)
        return self._seer_type
    
    def venpaa_seer(self, separator=SEPARATOR):
        if not self._asaigaL:
            self.asaigaL(separator)
        venpaa_seer = self._asaigaL
        if (self._seer_count > 2):
            return venpaa_seer
        elif (self._seer_count==1):
            if self._asaigaL == 'நிரை':
                venpaa_seer = 'மலர்'
            elif self._asaigaL == 'நேர்':
                venpaa_seer = 'நாள்'
        elif (self._seer_count==2):
            first_seer = self._asaigaL.split(separator)[0]
            if first_seer == 'நிரை':
                venpaa_seer = 'பிறப்பு'
            elif first_seer == 'நேர்':
                venpaa_seer = 'காசு'
        return venpaa_seer
    
    def thaLai_type(self, word_text, include_sub_type=True,neighbor='next'):
        self._thaLai_type = ''
        if not self._text.strip() or not word_text.strip():
            return self._thaLai_type
        seer1 = self.seer_type()
        asai1 = self.asaigaL()
        neighbor_word = Sol(word_text)
        seer2 = neighbor_word.seer_type()
        asai2 = neighbor_word.asaigaL()
        if neighbor == 'next':
            combined_seer = seer1 + ' ' + asai2
        else:
            combined_seer = seer2 + ' ' + asai1
        thaLai_arr = utils.THALAI_TYPES
        if include_sub_type==False:
            thaLai_arr = utils.THALAI_TYPES_SHORT
        self._thaLai_type = utils.get_keys_containing_string(thaLai_arr, combined_seer)
        if self._thaLai_type:
            self._thaLai_type = self._thaLai_type[0]
        else:
            self._thaLai_type = ''
            
        return self._thaLai_type
    
    def osai_type(self, word_text, include_sub_type=True, neighbor='next'):
        if not self._thaLai_type:
            self.thaLai_type(word_text, neighbor)
        osai_arr = utils.OSAI_TYPES
        if include_sub_type==False:
            osai_arr = utils.OSAI_TYPES_SHORT
        self._osai_type =  osai_arr.get(self._thaLai_type)
        return self._osai_type

    " check whether thodai matches betwee two words. thodai index monai(=0), edhugai (=1), yiyaibu (=-1)"
    def thodai_matches(self, neighbor_word_text, thodai_index=0):
        word1 = self.tamil_char_objects
        word2 = Sol(neighbor_word_text).tamil_char_objects
        """ TODO return FALSE if either are single letter words thodai_index <> 0 """
        if thodai_index != 0 and (len(word1) == 1 or len(word2) == 1):
            return False 
        thodai_char1 = word1[thodai_index]
        thodai_char2 = word2[thodai_index]
        char1 = thodai_char1.text()
        char2 = thodai_char2.text()
        if char1==char2: # if characters match exactly
            if thodai_index==0:
                #print('monai exact match', char2)
                return True # covered
            elif len(word1) > 1 and len(word2) > 1:
                return ( word1[thodai_index-1].is_kuril() and word2[thodai_index-1].is_kuril() ) or \
                               ( word1[thodai_index-1].is_nedil() and word2[thodai_index-1].is_nedil() ) or \
                               len(word1) > 2 and len(word2) > 2 and ( word1[thodai_index-2].is_nedil() and word2[thodai_index-2].is_nedil() ) and \
                               ( word1[thodai_index-1].is_otru() and word2[thodai_index-1].is_otru() ) #:
        elif (thodai_index == -1): # Check if atleast morphnese are identical example "டே","ணே","தே","நே","னே"
            has_same_last_morpheme = (char1[-1]==char2[-1])
            return has_same_last_morpheme
        " Construct possible matching characters to thodai_char1 and check against thodai_char2"
        thodai_matches = char2 in utils.get_thodai_characters(char1, thodai_index)
        #print(char1,'edhugai match', char2,thodai_matches)
        return thodai_matches
        
    def sandha_seer(self):
        if not self._seer_type:
            self.seer_type(separator=SEPARATOR)
        return [s for s in utils.SANDHA_SEERGAL if self._seer_type.endswith(s)][0]
            
"""
    class for Tamil Sentence
"""
class Adi(object):
    def __init__(self,sentence):
        sentence = ' '.join(sentence.split()) # remove multiple spaces
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        self.original_text = sentence
        self._text=''
        self._line_type = ''
        self._word_count = 0
        self.seer_thodai_types = ['','','']
        self.words = []
        self.word_objects = []
        self._seer_monai_words = []
        self._seer_edhugai_words = []
        self._seer_yiyaibu_words = []
        self.set_text(sentence)
        self._seer_monai_words = self.seer_thodai_words(0, '()')
        self._seer_edhugai_words = self.seer_thodai_words(1, '()')
        self._seer_yiyaibu_words = self.seer_thodai_words(-1, '()')
        
    def set_text(self, sentence):
        #print('sentence',sentence)
        end_of_line = '\n'
        if end_of_line in sentence:
            for line in sentence.splitlines() : self.set_text(line)
        else:
            self._text = sentence.translate(str.maketrans('', '', string.punctuation))
            blank = ' '
            self.words = self._text.strip().split(blank)
            #print('Line Words',self.words)
            self._word_count = len(self.words)
            self.word_objects = [Sol(wrd) for wrd in self.words]        
            #print('inside line',self._text)
    def text(self):
        return self._text
    
    def word_count(self):
        return self._word_count
        
    def line_type(self):
        #print('word count',self.word_count)
        if self.word_count() > 11:
            self._line_type = utils.LINE_TYPES[11]
        else:
            self._line_type = utils.LINE_TYPES[self.word_count()]
        return self._line_type
    
    def sandha_ozhungu(self):
        #self._sandha_ozhungu = ' '.join([wrd.sandha_seer() for wrd in self.word_objects])
        self._sandha_ozhungu = [wrd.sandha_seer() for wrd in self.word_objects]
        #print(utils.most_common_frequencies(self._sandha_ozhungu))
        return self._sandha_ozhungu

    def seer_thodai_words(self, thodai_index,thodai_separator='()'):
        thodai_words = []
        thodai_type_prefix = 'சீர் ' + utils.THODAI_TYPES[thodai_index]+ ': '
        wc = self.word_count()
        start = 0
        end = wc - 1
        step = 1
        if thodai_index == -1:
            start = wc-1
            end = 0
            step = -1
        word1 = self.word_objects[start]
        word1_chars = utils.get_unicode_characters(word1.text())
        end_char =''.join(word1_chars[thodai_index+1:])
        if (thodai_index == -1):
            end_char = ''
        thodai_word = utils.insert_string_at_index(word1_chars,thodai_separator,thodai_index)
        #thodai_word = ''.join(word1_chars[:thodai_index])+thodai_separator[0]+word1_chars[thodai_index]+thodai_separator[1]+end_char
        thodai_words.append(thodai_word)
        thodai_counter = 1
        thodai_type = str(thodai_counter)
        if wc == 1:
            thodai_type_pattern = 'இல்லை'
            if ('-' in thodai_type):
                thodai_type_pattern = ' (' + thodai_type + ')'
            self.seer_thodai_types[thodai_index] = thodai_type_prefix + utils.SEER_THODAI_TYPES.get(thodai_type) + thodai_type_pattern    
            return thodai_words
        for w in range(start+step,end+step,step):
            thodai_counter += 1 
            word2_text = self.word_objects[w].text()
            word2_chars = utils.get_unicode_characters(word2_text)
            if word1.thodai_matches(word2_text,thodai_index):
                if thodai_counter <= 4:
                    thodai_type += '-' + str(thodai_counter)
                end_char =''.join(word2_chars[thodai_index+1:])
                if (thodai_index == -1):
                    end_char = ''
                thodai_word = utils.insert_string_at_index(word2_chars,thodai_separator,thodai_index)
                #thodai_word = ''.join(word2_chars[:thodai_index])+thodai_separator[0]+word2_chars[thodai_index]+thodai_separator[1]+end_char
                thodai_words.append(thodai_word)
            else:
                #print(' no thodai',thodai_index,word2_text)
                thodai_words.append(word2_text)
        thodai_type_pattern = 'இல்லை'
        if ('-' in thodai_type):
            thodai_type_pattern = ' (' + thodai_type + ')'
        self.seer_thodai_types[thodai_index] = thodai_type_prefix + utils.SEER_THODAI_TYPES.get(thodai_type) + thodai_type_pattern
        if (thodai_index == -1):
            thodai_words = list(reversed(thodai_words)) 
        return thodai_words
        
                
class Yiyarpa(object):
    def __init__(self, text):
        self._text = ''
        self._line_count = 0
        self._words = []
        self._word_objects = []
        self.lines = []
        self.line_objects = []
        self._seergaL = []
        self._sandha_seergaL = []
        self._thaLaigaL = []
        self._osaigaL = []
        self.set_text(text)
        
    def text(self):
        return self._text
    
    def set_text(self, text):
        self.original_text = text
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.replace('\r','')
        self._text = text
        #print('self-text',self._text)
        self.lines = self._text.splitlines()
        self._line_count = len(self.lines)
        #print('line count',self._line_count)
        self.line_objects = [Adi(line) for line in self.lines] 
        #print('line objects',self.line_objects)
        
    def line_count(self):
        return self._line_count
    
    def words(self):
        self._words = [word.text() for line in self.line_objects for word in line.word_objects ]
        return self._words

    def asai_words(self):
        self._asai_words = [word.asai_word() for line in self.line_objects for word in line.word_objects ]
        return self._asai_words
        
    def asaigaL(self):
        self._asaigaL = [word.asaigaL() for line in self.line_objects for word in line.word_objects ]
        return self._asaigaL
        
    def word_objects(self):
        self._word_objects = [word for line in self.line_objects for word in line.word_objects ]
        return self._word_objects

    def seergaL(self, check_eetrucheer_for_venpaa=False):
        if not self._word_objects:
            self._word_objects = self.word_objects()
        self._seergaL = [word_object.seer_type() for word_object in self._word_objects ]
        if check_eetrucheer_for_venpaa:
            self._seergaL[-1] = self._word_objects[-1].venpaa_seer()
        return self._seergaL
    
    def sandha_seergaL(self):
        if not self._word_objects:
            self._word_objects = self.word_objects()
        self._sandha_seergaL = [word_object.sandha_seer() for word_object in self._word_objects ]
        return self._sandha_seergaL

    def thaLaigaL(self, include_sub_type=True):
        if not self._word_objects:
            self._word_objects = self.word_objects()
        if not self._words:
            self._words = self.words()
        self._thaLaigaL = [self._word_objects[w].thaLai_type(self._words[w+1], include_sub_type) for w in range(len(self._word_objects)-1) ]
        #print(self._thaLaigaL)
        return self._thaLaigaL
        
    def osaigaL(self,include_sub_type=True):
        if not self._thaLaigaL:
            self._thaLaigaL = self.thaLaigaL(include_sub_type)
        self._osaigaL = []
        osai_arr = utils.OSAI_TYPES
        if include_sub_type==False:
            osai_arr = utils.OSAI_TYPES_SHORT
        for thaLai in self._thaLaigaL:
            self._osaigaL.append(osai_arr.get(thaLai))
        return self._osaigaL

    def adi_thodai_lines(self, thodai_index,thodai_separator='()'):
        vikarpa_count = 0
        wi = 0
        thodai_lines = ''
        thodai_line_prefix = 'அடி ' + utils.THODAI_TYPES[thodai_index]
        if thodai_index == -1:
            wi = -1
        for l in range(self.line_count()-1):
            line1 = self.line_objects[l]
            line2 = self.line_objects[l+1]
            line1_text = line1.text()
            line2_text = line2.text()
            word1_obj = line1.word_objects[wi]
            word2_txt = line2.word_objects[wi].text()
            thodai_matches = word1_obj.thodai_matches(word2_txt,thodai_index)
            if (thodai_matches):
                line1_text = utils.insert_string_at_index(utils.get_unicode_characters(line1_text),thodai_separator,thodai_index)
                thodai_lines += line1_text + '\n'
                line2_text = utils.insert_string_at_index(utils.get_unicode_characters(line2_text),thodai_separator,thodai_index)
                thodai_lines += line2_text + '\n\n'
        if (thodai_lines==''):
            thodai_lines = thodai_line_prefix + ' இல்லை \n'
        else:
            thodai_lines = thodai_line_prefix + "\n" + thodai_lines
        return thodai_lines
    
    def vikarpam_count(self):
        vikarpa_count = 0
        w1 = 0
        for l in range(self.line_count()-1):
            word1_obj = self.word_objects()[w1]
            w2 = w1+self.line_objects[l].word_count()
            word2_txt = self.word_objects()[w2].text()
            if not word1_obj.thodai_matches(word2_txt,thodai_index=1):
                vikarpa_count += 1
            w1 = w2
        return vikarpa_count
    
    def vikarpam(self):
        vikarpa_count = self.vikarpam_count()
        return utils.VIKARPAM_LIST[vikarpa_count] if vikarpa_count < len(utils.VIKARPAM_LIST) else utils.VIKARPAM_LIST[-1]

    def thani_sorkaL(self):
        thani_sol_indices =[]
        for l in range(self.line_count()-1): ##No thani sol on last line
            line = self.line_objects[l]
            word_count = line.word_count()
            #print(line.text(),'word count',word_count)
            word1 = line.word_objects[0]
            word2 = line.word_objects[-1]
            if word_count==1:
                thani_sol_indices.append((l,0,word2.text()))
                continue
            #print(word1.text(), word2.text())
            if word1.thodai_matches(word2.text(),thodai_index=1):
                thani_sol_indices.append((l,word_count-1,word2.text()))
                continue
        return thani_sol_indices

    def seer_thodai_words(self, thodai_index,thodai_separator='()'):
        thodai_words = []
        for line in self.line_objects:
            line_seer_thodai = line.seer_thodai_words(thodai_index, thodai_separator)
            #print(line_seer_thodai, line.seer_thodai_types[thodai_index])
            thodai_words.append(line_seer_thodai)
        
        return thodai_words
        
class Yaappu(Yiyarpa):    
    
    def __init__(self, text, treat_aaydham_as_kuril=False, treat_kutriyaligaram_as_otru=False):
        super().__init__(text)
        self.treat_aaydham_as_kuril(treat_aaydham_as_kuril)
        self.treat_kutriyaligaram_as_otru(treat_kutriyaligaram_as_otru)
        #print(self.text())
        
    def treat_aaydham_as_kuril(self,b):
        utils._TREAT_AAYDHAM_AS_KURIL = b

    def treat_kutriyaligaram_as_otru(self, b):
        utils._TREAT_KUTRIYALIGARAM_AS_OTRU = b
            
    def check_for_venpaa(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'வெண்பா'
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:            
            rule_str = _VENPA_RULE_1
            poem_has_allowed_seers, actual_fraction = utils.has_required_percentage_of_occurrence(self.seergaL(True),utils.VENPA_ALLOWED_SEERS)
            paa_check = paa_check and poem_has_allowed_seers
            paa_str += RULE_CHECK(poem_has_allowed_seers) + rule_str +' (' + PERCENT.format(actual_fraction) + ')' +'\n'
            
            rule_str = _VENPA_RULE_2
            poem_has_allowed_thaLai, actual_fraction = utils.has_required_percentage_of_occurrence(self.thaLaigaL(),['வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை'])
            paa_check = paa_check and poem_has_allowed_thaLai
            paa_str += RULE_CHECK(poem_has_allowed_thaLai) + rule_str +' (' + PERCENT.format(actual_fraction) + ')' +'\n'
            
            rule_str = _VENPA_RULE_3
            has_allowed_seer_count = self.line_objects[-1].word_count() == 3 and all( self.line_objects[l].word_count()==4 for l in range(self.line_count()-1) )
            paa_check = paa_check and has_allowed_seer_count
            paa_str += RULE_CHECK(has_allowed_seer_count) + rule_str + '\n'
            
            rule_str = _VENPA_RULE_4
            poem_has_allowed_osai, actual_fraction = utils.has_required_percentage_of_occurrence(self.osaigaL(),["தூங்கிசைச் செப்பலோசை","ஏந்திசைச் செப்பலோசை"])
            paa_check = paa_check and poem_has_allowed_osai
            paa_str +=  RULE_CHECK(poem_has_allowed_osai) + rule_str +' (' + PERCENT.format(actual_fraction) + ')'+ '\n'
            
            rule_str = _VENPA_RULE_5
            poem_has_allowed_eetru_seer = utils.list_has_element(utils.VENPA_EETRU_SEERS,self.word_objects()[-1].venpaa_seer())
            paa_check = paa_check and poem_has_allowed_eetru_seer
            paa_str += RULE_CHECK(poem_has_allowed_eetru_seer) + rule_str+ '\n'
            
            if paa_check:
                #rule_str = _VENPA_KURAL_RULE_1
                kural_check = self.line_count() == 2 and self.line_objects[0].word_count()==4 and self.line_objects[1].word_count() == 3
                sindhiyal_check = self.line_count() == 3
                pahorodai_check = self.line_count() > 4
                #rule_str = _VENPA_NERISAI_RULE_1
                word1_pos = self.line_objects[0].word_count() # second line first word
                word2_pos =word1_pos + self.line_objects[1].word_count() - 1 # second line last word
                word1_obj = self.word_objects()[word1_pos]
                word2_txt = self.words()[word2_pos]
                poem_has_secondline_edhugai_with_last_word = word1_obj.thodai_matches(word2_txt,thodai_index = 1) #thodai_index = 1 >> Edhugai
                poem_has_secondline_edhugai_with_last_word
                #paa_str +=  RULE_CHECK(poem_has_secondline_edhugai_with_last_word) + rule_str+ '\n'
                if kural_check:
                    poem_sub_type = 'குறள்'
                    paa_str += RULE_CHECK(kural_check) + _VENPA_KURAL_RULE_1 + '\n'
                elif sindhiyal_check:
                    poem_sub_type = 'சிந்தியல்'
                    paa_str += RULE_CHECK(sindhiyal_check) + _VENPA_SINDHIYAL_RULE_1 + '\n'
                elif pahorodai_check:
                    poem_sub_type = 'பஃறொடை'
                    paa_str += RULE_CHECK(pahorodai_check) + _VENPA_PAHRODAI_RULE_1 + '\n'
                elif poem_has_secondline_edhugai_with_last_word :
                    poem_sub_type = 'நேரிசை' 
                    paa_str += RULE_CHECK(poem_has_secondline_edhugai_with_last_word) + _VENPA_NERISAI_RULE_1 + '\n'
                else:
                    poem_sub_type = 'இன்னிசை' 
                    paa_str += RULE_CHECK(not poem_has_secondline_edhugai_with_last_word) + _VENPA_INNISAI_RULE_1 + '\n'
                #poem_sub_type = 'நேரிசை' if poem_has_secondline_edhugai_with_last_word else 'இன்னிசை'
                poem_type = poem_sub_type + ' ' + poem_type
                
                poem_sub_type = self.vikarpam()
                poem_type = poem_sub_type + ' ' + poem_type
                paa_str += '\n' + poem_type+ '\n'
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
        
    def check_for_asiriyapaa(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'ஆசிரியப்பா'
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:
            rule_str = _ASIRIYAPA_RULE_1
            expected_fraction = ASIRIYAPA_RULE_FRACTION
            poem_has_allowed_seers, actual_fraction = utils.has_required_percentage_of_occurrence(self.seergaL(True),utils.ASIRIYAPPA_ALLOWED_SEERS,expected_fraction)
            paa_check = paa_check and poem_has_allowed_seers
            paa_str += RULE_CHECK(poem_has_allowed_seers) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
            
            rule_str = _ASIRIYAPA_RULE_2
            poem_has_disallowed_seers, actual_fraction = utils.has_required_percentage_of_occurrence(self.seergaL(),utils.ASIRIYAPPA_DISALLOWED_SEERS)
            paa_check = paa_check and not poem_has_disallowed_seers
            paa_str += RULE_CHECK(not poem_has_disallowed_seers) + rule_str +' (' + PERCENT.format(actual_fraction) + ')' +'\n'
    
            rule_str = _ASIRIYAPA_RULE_3
            lastChar = self.words()[-1][-1]
            #print('lastchar',lastChar)
            poem_has_allowed_ending = utils.list_has_element(utils.ASIRIYAPPA_EETRUCHEER_LETTERS,lastChar)
            paa_check = paa_check and poem_has_allowed_ending
            paa_str += RULE_CHECK(poem_has_allowed_ending) + rule_str +'\n'
    
            rule_str = _ASIRIYAPA_RULE_4
            expected_fraction = ASIRIYAPA_RULE_FRACTION
            poem_has_allowed_thaLaigaL, actual_fraction = utils.has_required_percentage_of_occurrence(self.thaLaigaL(),["நேரொன்றிய ஆசிரியத்தளை","நிரையொன்றிய ஆசிரியத்தளை"],expected_fraction)
            paa_check = paa_check and poem_has_allowed_thaLaigaL
            paa_str += RULE_CHECK(poem_has_allowed_thaLaigaL) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
    
            rule_str = _ASIRIYAPA_RULE_5
            expected_fraction = ASIRIYAPA_RULE_FRACTION
            poem_has_allowed_osai, actual_fraction = utils.has_required_percentage_of_occurrence(self.osaigaL(),["ஏந்திசை அகவலோசை","தூங்கிசை அகவலோசை"],expected_fraction)
            paa_check = paa_check and poem_has_allowed_osai
            paa_str += RULE_CHECK(poem_has_allowed_osai) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
    
            rule_str = _ASIRIYAPA_RULE_6
            has_allowed_seer_count = all(self.line_objects[l].word_count()<=4 for l in range(self.line_count()))       
            paa_check = paa_check and has_allowed_seer_count
            paa_str += RULE_CHECK(has_allowed_seer_count) + rule_str + '\n'
    
            nilaimandila_check = all(self.line_objects[l].word_count()==4 for l in range(self.line_count()))
            kuraLadi_check =  all(self.line_objects[l].word_count()<4 for l in range(1,self.line_count()-1)) and self.line_objects[0].word_count()==4 and self.line_objects[-1].word_count()==4
            nerisai_check = has_allowed_seer_count and self.line_objects[-2].word_count()==3
            poem_sub_type = ""
            if paa_check:
                if nilaimandila_check:
                    poem_sub_type = "நிலை மண்டில"
                elif kuraLadi_check:
                    poem_sub_type = "இணைக்குறள்"
                elif nerisai_check:
                    poem_sub_type = "நேரிசை"
            poem_type = poem_sub_type +' '+ poem_type
                
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
        
    def check_for_kalipaa(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'கலிப்பா'
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:
            rule_str = _KALIPA_RULE_1
            expected_fraction = KALIPA_RULE_FRACTION
            poem_has_allowed_seers, actual_fraction = utils.has_required_percentage_of_occurrence(self.seergaL(True),utils.KALIPPA_ALLOWED_SEERS,expected_fraction)
            paa_check = paa_check and poem_has_allowed_seers
            paa_str += RULE_CHECK(poem_has_allowed_seers) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
            
            rule_str = _KALIPA_RULE_2
            poem_has_disallowed_seers, actual_fraction = utils.has_required_percentage_of_occurrence(self.seergaL(),utils.KALIPPA_DISALLOWED_SEERS)
            paa_check = paa_check and not poem_has_disallowed_seers
            paa_str += RULE_CHECK(not poem_has_disallowed_seers) + rule_str +' (' + PERCENT.format(actual_fraction) + ')' +'\n'
    
            rule_str = _KALIPA_RULE_3
            expected_fraction = KALIPA_RULE_FRACTION
            poem_has_allowed_thaLaigaL, actual_fraction = utils.has_required_percentage_of_occurrence(self.thaLaigaL(),["கலித்தளை"],expected_fraction)
            paa_check = paa_check and poem_has_allowed_thaLaigaL
            paa_str += RULE_CHECK(poem_has_allowed_thaLaigaL) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
    
            rule_str = _KALIPA_RULE_4
            expected_fraction = KALIPA_RULE_FRACTION
            poem_has_allowed_osai, actual_fraction = utils.has_required_percentage_of_occurrence(self.osaigaL(),["ஏந்திசைத் துள்ளலோசை"],expected_fraction)
            paa_check = paa_check and poem_has_allowed_osai
            paa_str += RULE_CHECK(poem_has_allowed_osai) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
    
            rule_str = _KALIPA_RULE_5
            has_allowed_seer_count = all(self.line_objects[l].word_count()==4 for l in range(self.line_count()-1))       
            paa_check = paa_check and has_allowed_seer_count
            paa_str += RULE_CHECK(has_allowed_seer_count) + rule_str + '\n'
            last_line_count = self.line_objects[-1].word_count()
            if paa_check:
                if last_line_count == 3:
                    poem_sub_type = 'வெண்'
                else:
                    poem_sub_type = 'தரவு கொச்சகக்'
                poem_type = poem_sub_type + ' ' + poem_type
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
        
    def check_for_vanjipaa(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'வஞ்சிப்பா'
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:
            rule_str = _VANJIPA_RULE_1
            expected_fraction = VANJIPA_RULE_FRACTION
            poem_has_allowed_seers, actual_fraction = utils.has_required_percentage_of_occurrence(self.seergaL(),utils.VANJPA_ALLOWED_SEERS,expected_fraction)
            paa_check = paa_check and poem_has_allowed_seers
            paa_str += RULE_CHECK(poem_has_allowed_seers) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
            
            rule_str = _VANJIPA_RULE_2
            expected_fraction = VANJIPA_RULE_FRACTION
            thani_seers = [Sol(thani[2]).seer_type() for thani in self.thani_sorkaL() ]
            poem_has_allowed_seers, actual_fraction = utils.has_required_percentage_of_occurrence(thani_seers,utils.VANJPA_THANISOL_ALLOWED_SEERS,expected_fraction)
            paa_check = paa_check and poem_has_allowed_seers
            paa_str += RULE_CHECK(poem_has_allowed_seers) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
            
            rule_str = _VANJIPA_RULE_3
            expected_fraction = VANJIPA_RULE_FRACTION
            poem_has_allowed_thaLaigaL, actual_fraction = utils.has_required_percentage_of_occurrence(self.thaLaigaL(),["ஒன்றிய வஞ்சித்தளை","ஒன்றா வஞ்சித்தளை"],expected_fraction)
            paa_check = paa_check and poem_has_allowed_thaLaigaL
            paa_str += RULE_CHECK(poem_has_allowed_thaLaigaL) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
    
            rule_str = _VANJIPA_RULE_4
            expected_fraction = VANJIPA_RULE_FRACTION
            poem_has_allowed_osai, actual_fraction = utils.has_required_percentage_of_occurrence(self.osaigaL(),["ஏந்திசைத் தூங்கலோசை","அகவல் தூங்கலோசை"],expected_fraction)
            paa_check = paa_check and poem_has_allowed_osai
            paa_str += RULE_CHECK(poem_has_allowed_osai) + rule_str +' (' + PERCENT.format(actual_fraction) + GEQ + PERCENT.format(expected_fraction) + ')' +'\n'
    
            rule_str = _VANJIPA_RULE_5
            thani_line = self.thani_sorkaL()[-1][0]
            #print(thani[-1][0],'==',self.line_count()-3)
            surithagam_check = thani_line and (thani_line == self.line_count()-3)
            paa_check = paa_check and surithagam_check
            paa_str += RULE_CHECK(surithagam_check) + rule_str +'\n'
    
            rule_str = _VANJIPA_RULE_6
            kuraladi_check = all(self.line_objects[l].word_count()==2 for l in range(thani_line-1) )
            sindhadi_check = all(self.line_objects[l].word_count()==3 for l in range(thani_line-1) )
            line_count_check = (kuraladi_check or sindhadi_check)
            paa_check = paa_check and line_count_check
            paa_str += RULE_CHECK(line_count_check) + rule_str +'\n'
    
            if paa_check:
                if kuraladi_check:
                    poem_sub_type = 'குறளடி'
                    paa_str += RULE_CHECK(kuraladi_check) + _VANJIPA_KURALADI +'\n'
                elif sindhadi_check:
                    poem_sub_type = 'சிந்தடி'
                    paa_str += RULE_CHECK(sindhadi_check) + _VANJIPA_SINDHADI +'\n'
                poem_type = poem_sub_type + ' ' + poem_type
                    
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
            
    def check_for_venpaavinam(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'வெண்பாவினம் '
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:
            kuRaL_thaazhisai_check = self.line_count() == 2 and self.line_objects[0].word_count() >= 4 and self.line_objects[1].word_count() < self.line_objects[0].word_count()
            kuRal_thuRai_check = self.line_count() == 2 and self.line_objects[0].word_count() == self.line_objects[1].word_count()
            ven_thaazhisai_check = self.line_count() == 3 and self.line_objects[0].word_count() == 4 and self.line_objects[1].word_count() == 4 and self.line_objects[2].word_count() ==3
            #thani_check = all(thani[0]==l for l in range(self.line_count() for thani in thani_sol))
            thani_check = all(self.line_objects[0].words[-1] == self.line_objects[l].words[-1] for l in range(self.line_count()))
            #print('thani_check',thani_check,self.line_objects[0].words[-1],self.line_objects[-1].words[-1])
            ven_thurai_check = self.line_count() >= 3 and  self.line_count()<=7 and (self.line_objects[-1].word_count() < self.line_objects[0].word_count())
            veLi_virutham_check = self.line_count() == 3 or self.line_count() ==4 and thani_check
            #print('kuRaL_thaazhisai_check',kuRaL_thaazhisai_check,'kuRal_thuRai_check',kuRal_thuRai_check,'ven_thaazhisai_check',ven_thaazhisai_check,'ven_thurai_check',ven_thurai_check,'veLi_virutham_check',veLi_virutham_check)
            poem_sub_type = ''
            paa_str += RULE_CHECK(kuRaL_thaazhisai_check) + _VENPAVINAM_KURAL_THAZHISAI + '\n'
            paa_str += RULE_CHECK(kuRal_thuRai_check) + _VENPAVINAM_KURAL_THURAI + '\n'
            paa_str += RULE_CHECK(ven_thaazhisai_check) + _VENPAVINAM_VEN_THAZHISAI + '\n'
            paa_str += RULE_CHECK(ven_thurai_check) + _VENPAVINAM_VEN_THURAI  + '\n'
            paa_str += RULE_CHECK(veLi_virutham_check) + _VENPAVINAM_VELI_VIRUTHAM + '\n'
            paa_check = paa_check and (kuRaL_thaazhisai_check or kuRal_thuRai_check or ven_thaazhisai_check or ven_thurai_check or veLi_virutham_check)
            if kuRaL_thaazhisai_check:
                poem_sub_type = 'குறள்  தாழிசை' 
            elif kuRal_thuRai_check:
                poem_sub_type = 'குறள் துறை' 
            elif ven_thaazhisai_check:
                poem_sub_type = 'வெண் தாழிசை' 
            elif ven_thurai_check:
                poem_sub_type = 'வெண்டுறை' 
            elif veLi_virutham_check:
                poem_sub_type = 'வெளி விருத்தம்' 
            poem_type = poem_sub_type + ' ' + poem_type
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
                
    def check_for_asiriyapaavinam(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'ஆசிரியப்பாவினம்'
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:
            word_count = self.line_objects[-1].word_count()
            thazhisai_check = self.line_count() == 3 and all(self.line_objects[l].word_count() == word_count for l in range(self.line_count()-1))
            thuRai_check = ( (self.line_objects[1].word_count() > self.line_objects[0].word_count()) and \
                           (self.line_objects[1].word_count() > self.line_objects[2].word_count()) ) or \
                           ( (self.line_objects[2].word_count() < self.line_objects[1].word_count()) and \
                           (self.line_objects[2].word_count() < self.line_objects[3].word_count()) )
            thuRai_check = thuRai_check and ( self.line_objects[1].words[0] == self.line_objects[2].words[0]) and \
                                            ( self.line_objects[1].words[1] == self.line_objects[2].words[1])
            virutham_check = self.line_count() == 4 and word_count > 5 and \
                            all(self.line_objects[l].word_count() == word_count for l in range(self.line_count()-1))
            sandha_ozhungu = self.line_objects[0].sandha_ozhungu()
            has_sandha_ozhungu, actual_fraction = utils.has_required_percentage_of_occurrence(self.sandha_seergaL(),sandha_ozhungu,ASIRIYAPA_SANDHA_OZHUNGU_FRACTION)
            #has_sandha_ozhungu = all(self.line_objects[l].sandha_ozhungu() == sandha_ozhungu for l in range(self.line_count()))
            virutham_check = virutham_check and has_sandha_ozhungu
            paa_check = paa_check and (thazhisai_check or thuRai_check or virutham_check)
            paa_str += RULE_CHECK(thazhisai_check) + _ASIRIYAPA_THAZHISAI + '\n'
            paa_str += RULE_CHECK(thuRai_check) + _ASIRIYAPA_THURAI + '\n'
            paa_str += RULE_CHECK(virutham_check) + _ASIRIYAPA_VIRUTHAM + '(' + ' '.join(sandha_ozhungu) + ') (' + PERCENT.format(actual_fraction) + ')'+ '\n'
            poem_sub_type = ''
            if thazhisai_check:
                poem_sub_type = "ஆசிரியத் தாழிசை" 
            elif thuRai_check:
                poem_sub_type = "ஆசிரியத் துறை" 
            elif virutham_check:
                poem_sub_type = "ஆசிரிய/வெளி விருத்தம்" 
            poem_type = poem_sub_type + ' ' + poem_type
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
        
    def check_for_kalipaavinam(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'கலிப்பாவினம்'
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:
            word_count = self.line_objects[-1].word_count()
            thazhisai_check = self.line_count() >=2  and all(self.line_objects[l].word_count() < word_count for l in range(self.line_count()-1))
            thuRai_check = self.line_count() == 4 and word_count ==5 and all(self.line_objects[l].word_count() == word_count for l in range(self.line_count()-1))
            thuRai_check = thuRai_check and self.vikarpam_count() == 0
            kattaLai_check = self.line_count() == 4
            poem_has_allowed_thaLai, kattaLai_fraction = utils.has_required_percentage_of_occurrence(self.thaLaigaL(),['வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை'],KALIPA_THALAI_FRACTION)
            eetru_seer_check = self.words()[-1][-1]==utils.KALIPPA_EETRUCHEER_LETTERS[0]
            kattaLai_check = kattaLai_check and poem_has_allowed_thaLai and eetru_seer_check
            virutham_check = self.line_count() == 4 and word_count == 4 and \
                            all(self.line_objects[l].word_count() == word_count for l in range(self.line_count()-1))
            sandha_ozhungu = self.line_objects[0].sandha_ozhungu()
            has_sandha_ozhungu, virutham_fraction = utils.has_required_percentage_of_occurrence(self.sandha_seergaL(),sandha_ozhungu,KALIPA_SANDHA_OZHUNGU_FRACTION)
            #has_sandha_ozhungu = all(self.line_objects[l].sandha_ozhungu() == sandha_ozhungu for l in range(self.line_count()))
            virutham_check = virutham_check and has_sandha_ozhungu
            paa_check = paa_check and (thazhisai_check or thuRai_check or kattaLai_check or virutham_check)
            paa_str += RULE_CHECK(thazhisai_check) + _KALIPA_THAZHISAI + '\n'
            paa_str += RULE_CHECK(kattaLai_check) + _KALIPA_KATTALAI_THURAI + ' (' + PERCENT.format(kattaLai_fraction) + ')'+ '\n'
            paa_str += RULE_CHECK(thuRai_check) + _KALIPA_KALI_THURAI + '\n'
            paa_str += RULE_CHECK(virutham_check) + _KALIPA_VIRUTHAM + '(' + ' '.join(sandha_ozhungu) + ') (' + PERCENT.format(virutham_fraction) + ')'+ '\n'
            poem_sub_type = ''
            if thazhisai_check:
                poem_sub_type = "கலித் தாழிசை" 
            elif kattaLai_check:
                poem_sub_type = "கட்டளைக் கலித்துறை" 
            elif thuRai_check:
                poem_sub_type = "கலித்துறை" 
            elif virutham_check:
                poem_sub_type = "கலி விருத்தம்"
            poem_type = poem_sub_type + ' ' + poem_type
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
        
    def check_for_vanjipaavinam(self):
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'வஞ்சிப்பாவினம்'
        paa_str = poem_type + " யாப்பிலக்கண விதிகள்" + '\n'
        try:
            word_count = self.line_objects[-1].word_count()
            thazhisai_check = self.line_count() > 4 and self.line_count() % 4 ==0 and all(self.line_objects[l].word_count() == 2 for l in range(self.line_count()))
            thuRai_check = self.line_count() == 4 and all(self.line_objects[l].word_count() == 2 for l in range(self.line_count()))
            virutham_check = self.line_count() == 4 and all(self.line_objects[l].word_count() == 3 for l in range(self.line_count()))
            paa_check = paa_check and (thazhisai_check or thuRai_check or virutham_check)
            paa_str += RULE_CHECK(thazhisai_check) + _VANJIPA_THAZHISAI + '\n'
            paa_str += RULE_CHECK(thuRai_check) + _VANJIPA_THURAI + '\n'
            paa_str += RULE_CHECK(virutham_check) + _VANJIPA_VIRUTHAM + '\n'
            poem_sub_type = ''
            if thazhisai_check:
                poem_sub_type = "வஞ்சித் தாழிசை" 
            elif thuRai_check:
                poem_sub_type = "வஞ்சித்  துறை" 
            elif virutham_check:
                poem_sub_type = "வஞ்சி விருத்தம்"
            poem_type = poem_sub_type + ' ' + poem_type
            return [paa_check, poem_type, paa_str]
        except:
            return [False, poem_type, paa_str]
        
    def analyze(self,poem_type=None,get_individual_poem_analysis=False):
        """
        arguments:
            poem_type: integer 1 to 8, 1= VENPA and 5=VENPAVINAM and 8 - VANJIPAVINAM
                if None - all poem text will be analyzed for all poem types and sub types
            get_individual_poem_analysis: True or False (default)
                True: will return poem analysis for all poem types until matching poem type is found
        return:
            result, poem_analysis
            result: [True/False matching poem_type, poem_type name, poem type matching details]
            poem_analysis = analysis of all poem types until matching poem type found
        """
        poem_analysis = ''
        result=[False,'','']
        for poem_type_enum in utils.POEM_TYPES:
            #print(poem_type,poem_type_enum,not result[0],poem_type==None, poem_type==poem_type_enum)
            if not result[0] and (poem_type==None or poem_type==poem_type_enum or get_individual_poem_analysis):
                #print(poem_type_enum,POEM_CHECK_FUNCTIONS.get(poem_type_enum))
                result = getattr(self,utils.POEM_CHECK_FUNCTIONS.get(poem_type_enum))()
                if get_individual_poem_analysis:
                    poem_analysis += result[2]
        return result, poem_analysis    
    
    def _analyze_thirukural(self):
        kuralgal = open('thirukural.txt', "r", encoding="utf-8").readlines()
        outFile = open('output.txt', "w", encoding="utf-8")
        start_kural_id = 0
        end_kural_id = start_kural_id + 10
        id = start_kural_id
        kural_types = []
        venpaavinam_kuralgal = []
        kuralgal_with_incompatible_seer_count = []
        TREAT_AAYDHAM_AS_KURIL_KURALGAL = [226, 363, 414, 943, 1166]
        TREAT_KUTRIYALIGARAM_AS_OTRU_KURALGAL = [178, 254, 291, 324, 541, 585, 801, 831, 844, 895, 1041]
        for kural in kuralgal:#[start_kural_id:end_kural_id]:
            id += 1
            kural = kural.replace('$','\n')
            if id in TREAT_AAYDHAM_AS_KURIL_KURALGAL:
                ty = Yaappu(kural,treat_aaydham_as_kuril=True)
            elif id in TREAT_KUTRIYALIGARAM_AS_OTRU_KURALGAL:
                ty = Yaappu(kural,treat_kutriyaligaram_as_otru=True)
            else:
                ty = Yaappu(kural)
                #utils._TREAT_AAYDHAM_AS_KURIL = False
            paa_check,poem_analysis = ty.analyze()#utils.POEM_TYPES.VENPA,get_individual_poem_analysis=False)
            print('============================================')
            print(id,kural)
            outFile.write('\n'+str(id)+' '+kural)
            kural_types.append(paa_check[1])
            print('POEM Results:',paa_check[1] + RULE_CHECK(paa_check[0]))
            outFile.write(paa_check[1])
            if 'வெண்பாவினம்' in paa_check[1]:
                venpaavinam_kuralgal.append(id)
                if ty.line_objects[0].word_count() != 4 or ty.line_objects[1].word_count() != 3:
                    kuralgal_with_incompatible_seer_count.append(id)
            #print('POEM Results:',paa_check[2])
        outFile.close()
        print(utils.frequency_of_occurrence(kural_types))
        print(venpaavinam_kuralgal)
        print('kuralgal_with_incompatible_seer_count',kuralgal_with_incompatible_seer_count)
            
if __name__ == '__main__':
    tp = Yiyarpa("இருவினையின் மதிமயங்கித் திரியாதே\n"+
"எழுநரகி லுழலுநெஞ்சத் தலையாலே\n"+
"பரமகுரு வருணினைந்திட் டுணர்வாலே\n"+
"கரவுதரி சனையையென்றற் கருள்வாயே\n"+
"தெரிதமிழை யுதவுசங்கப் புலவோனே\n"+
"சிவனருளு முருகசெம்பொற் கழலோனே\n"+
"கருணைநெறி புரியுமன்பர்க் கெளியோனே\n"+
"கனகசபை மருவுகந்தப் பெருமாளே!")
    #print(tp.text())
    for line in tp.line_objects:
        nko_str = ''
        for word in line.word_objects:
            nko_str += Sol(word.text())._get_nko_string()+' '
        print(line.text(),'\n', line.sandha_ozhungu(),nko_str)
    exit()
    #"""
    kural = "அணியன்றோ நாணுடைமை சான்றோர்க்கஃ தின்றேல்\nபிணியன்றோ பீடு நடை"
    #utils._TREAT_AAYDHAM_AS_KURIL = True
    print(kural)
    ty = Yaappu(kural)
    paa_check,poem_analysis = ty.analyze(utils.POEM_TYPES.VENPA)#VINAM)
    print('POEM Results:',paa_check[1] + RULE_CHECK(paa_check[0]))
    print('POEM Results:',paa_check[2])
    print(ty.thaLaigaL())
    print(ty.seergaL(True))
    print(ty.asaigaL())
    print(ty.asai_words())
    exit()
    #"""
    _analyze_thirukural()
    exit()
    #"""
    wrd = Sol('நுந்தை')
    print(wrd.text(),wrd.tamil_char_objects[0].is_magarakurukkam(),wrd.tamil_char_objects[0].duration())
    print('total duration',wrd.duration())
    exit()
    file = 'input/Kalipaavinam_KattaLaiThuRai.txt'
    poem = open(file, "r", encoding="utf-8").read()
    ty = Yaappu(poem)
    paa_check,poem_analysis = ty.analyze(utils.POEM_TYPES.KALIPAVINAM,get_individual_poem_analysis=False)
    print(poem_analysis)
    print('============================================')
    print(poem)
    print('POEM Results:',paa_check[1] + RULE_CHECK(paa_check[0]))
    print('POEM Results:',paa_check[2])
    exit()
    tp = Yiyarpa("தனந்தரும் கல்வி தருமொரு நாளும் தளர்வறியா\n"+\
"மனந்தரும் தெய்வ வடிவும் தரும்நெஞ்சில் வஞ்சமில்லா\n"+ \
"இனந்தரும் நல்லன எல்லாம் தருமன்பர் என்பவர்க்கே\n" + \
"கனந்தரும் பூங்குழ லாளபி ராமி கடைக்கண்களே")
    len_arr = [line.word_count() for line in tp.line_objects]
    thodai_type_2d = []
    for t in [0,1,-1]:
        print('todai_index = ', t)
        thodai_type_2d.append(tp.seer_thodai_words(t))
        for l in range(tp.line_count()):
            print(thodai_type_2d[t][l], tp.line_objects[l].seer_thodai_types[t])
    #exit()
    len_arr = [line.word_count() for line in tp.line_objects]     
    words_2d = (utils.convert_1d_list_to_2d(tp.words(),len_arr))
    asai_words_2d = (utils.convert_1d_list_to_2d(tp.asai_words(),len_arr))
    asaigal_2d = (utils.convert_1d_list_to_2d(tp.asaigaL(),len_arr))
    seergal_2d = (utils.convert_1d_list_to_2d(tp.seergaL(),len_arr))
    sandha_seergal_2d = (utils.convert_1d_list_to_2d(tp.sandha_seergaL(),len_arr))
    thaLaigaL_2d = (utils.convert_1d_list_to_2d(tp.thaLaigaL(include_sub_type=False),len_arr))
    osaigaL_2d = (utils.convert_1d_list_to_2d(tp.osaigaL(include_sub_type=False),len_arr))
    separator = '\t\t'
    separator_2 = separator+separator
    for l in range(tp.line_count()):
        print(separator.join(asai_words_2d[l]))
        print(separator.join(asaigal_2d[l]))
        print(separator.join(seergal_2d[l]))
        print(separator_2.join(sandha_seergal_2d[l]))
        print('\t\t\t\t\t', tp.line_objects[l].line_type())
        print('<->'.join(thaLaigaL_2d[l]))
        print('<->'.join(osaigaL_2d[l]))
        print('\n')
    for t in [0,1,-1]:
        #print('adi todai_index = ', t)
        print(tp.adi_thodai_lines(t,'<>'))