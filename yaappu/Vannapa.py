# coding=utf8
from yaappu.grammar import Ezhuthu, Sol, Adi,Yiyarpa
from yaappu import utils
import string
""" Vannappa Rules """
_VANNAPA_RULE_1 = "எல்லா அடிகளிலும் சந்த ஒழுங்கு ஒன்றாக இருக்க வேண்டும்."
_VANNAPA_RULE_2 = "எல்லா அடிகளிலும் சந்தக் குழிப்பு ஒன்றாக இருக்க வேண்டும்." +"\n"\
                    "\tசந்தக் குழிப்புகள் ஒரே இனத்தைச் சார்ந்ததாக இருக்க வேண்டும்."
_VANNAPA_RULE_3 = "எல்லா அடிகளும் ஒரே எதுகை அமைப்பைப் பெற்றிருக்க வேண்டும்.\n"
_VANNAPA_RULE_4 = "கலைகள் மோனையால் இணைந்து அடியாகும்.\n"
                    
"""
    GLOBAL CONSTANTS
"""
GREEN_CHECK = u'\u2714  '
RED_CROSS = u'\u274C  '
GEQ = u' \u2265 '
RULE_CHECK = lambda rc : '\t' + GREEN_CHECK if rc else '\t' + RED_CROSS
PERCENT = "{:.0%}"
PERCENT_2 = "( {:.0%} " + GEQ + " {:.0%} )"
class Vannapa(Yiyarpa):
    " TODO: Vannappa/Sandhappa is_aikaaram should be treated as KuRil ALSO for edhugai/monai"
    def __init__(self, text, poem_check_fraction = 0.9): #, treat_aaydham_as_kuril=False, treat_kutriyaligaram_as_otru=False):
        super().__init__(text)
        self.poem_check_fraction = poem_check_fraction
        self.kalaiCount = 0
        self.thuLLalCount = 0
        self.kalai_monai_words = ""
        self.adi_edhugai_words = ""
        self._sandha_kuzhippu_list = self.sandha_kuzhippu()
        self.kalaiCount = self._kalai_count()
    def _kalai_count(self):
        first_line_sandha_kuzhippu = self.sandha_kuzhippu()[0:self.line_objects[0].word_count()]
        last_word_index = len(first_line_sandha_kuzhippu)-1
        " Get kalai count "
        kalaiCount = 0
        for k in range(5,0,-1):
            div = int((last_word_index+1)/k)
            if ( (div*k==last_word_index+1) and 
                    (first_line_sandha_kuzhippu[0]==(first_line_sandha_kuzhippu[div]) )):
                kalaiCount = k
                #print("last_word_index "+str(last_word_index+1)+" div"+str(div)+" Found kalaiCount="+str(kalaiCount)+"=>"+first_line_sandha_kuzhippu[div])
                break
        return kalaiCount
    def sandha_kuzhippu(self):
        _sandha_kuzhippu_list = []
        for l in range(self._line_count):
            line = self.line_objects[l]
            word_count = line.word_count()
            for w in range(word_count):
                "TODO Middle Word option should be set at poem level"
                middle_word = (w == (word_count/2)-1) # False #
                #if middle_word:
                #    print('middle_word',line.word_objects[w].text()) 
                last_word = (w == word_count-1)
                _sandha_kuzhippu_list.append(line.word_objects[w].sandha_kuzhippu(paa_type = "Vannapa", last_word=last_word, middle_word=middle_word))
        return _sandha_kuzhippu_list

    def has_sandha_kuzhippu(self, required_percent_of_occurrence=0.99):
        if not self._sandha_kuzhippu_list:
            self._sandha_kuzhippu_list = self.sandha_kuzhippu()
        #print(self._sandha_kuzhippu_list)
        len_arr = [line.word_count() for line in self.line_objects]
        sandha_kuzhippu_2d = (utils.convert_1d_list_to_2d(self._sandha_kuzhippu_list,len_arr))
        _sandha_kuzhippu = sandha_kuzhippu_2d[0] 
        #print(_sandha_kuzhippu)
        _has_sandha_kuzhippu, _actual_fraction = utils.has_required_percentage_of_occurrence(self._sandha_kuzhippu_list,_sandha_kuzhippu,required_percent_of_occurrence)
        return _has_sandha_kuzhippu, _sandha_kuzhippu, _actual_fraction        
    
    def get_kuzhippu_thongal_kalai(self):
        result = ""
        first_line_sandha_kuzhippu = self.sandha_kuzhippu()[0:self.line_objects[0].word_count()]
        last_word_index = len(first_line_sandha_kuzhippu)-1
        kalaiCount = self.kalaiCount
        middle_word_index = int((last_word_index+1)/kalaiCount-1)
        result += first_line_sandha_kuzhippu[0]+" "
        i=1
        while (not first_line_sandha_kuzhippu[i]==(first_line_sandha_kuzhippu[0])):
            result += first_line_sandha_kuzhippu[i] +" "
            i+=1
        thuLLalCount = int(middle_word_index / i)
        result = ("துள்ளல் ("+str(thuLLalCount)+")=>"+ result.strip()+", தொங்கல்=>"+first_line_sandha_kuzhippu[middle_word_index]+
                  ", துள்ளல்+தொங்கல்=கலை ("+str(kalaiCount)+")")
        return result.strip();
        
    def has_adi_edhugai(self):
        edhugai_check = (self.vikarpam_count() ==0)
        self.adi_edhugai_words = ""
        if edhugai_check:
            lineCount = self.line_count()
            kalai_word1 = self.line_objects[0].word_objects[0]
            for l in range(1,lineCount):
                kalai_word2 = self.line_objects[l].word_objects[0]
                edhugai_check = kalai_word1.thodai_matches(kalai_word2.text(),1)
                if not edhugai_check:
                    return edhugai_check
                else:
                    kalai_word1_new = utils.insert_string_at_index(utils.get_unicode_characters(kalai_word1.text()),"()",1)
                    kalai_word2_new = utils.insert_string_at_index(utils.get_unicode_characters(kalai_word2.text()),"()",1)
                    self.adi_edhugai_words += "["+kalai_word1_new+","+kalai_word2_new+"] ";                    
        return edhugai_check
    def has_kalai_monai(self):
        monai_check = True
        self.kalai_monai_words = ""
        lineCount = self.line_count()
        for l in range(lineCount):
            line = self.line_objects[l]
            div = int(line.word_count()/self.kalaiCount)
            kalai_word1 = line.word_objects[0]
            for k in range(1,self.kalaiCount):
                kalai_word2 = line.word_objects[k*div]
                monai_check = kalai_word1.thodai_matches(kalai_word2.text(),0)
                if not monai_check:
                    return monai_check
                else:
                    kalai_word1_new = utils.insert_string_at_index(utils.get_unicode_characters(kalai_word1.text()),"()",0)
                    kalai_word2_new = utils.insert_string_at_index(utils.get_unicode_characters(kalai_word2.text()),"()",0)
                    self.kalai_monai_words += "["+kalai_word1_new+","+kalai_word2_new+"] ";                    
        return monai_check

    def check_for_vannapaa(self):
        import numpy as np
        """
        return arguments - tuple
        poem type True or False
        rule check description
        """    
        paa_check = True
        poem_type = 'வண்ணப்பா'
        paa_str = poem_type + " இசைப்பாவியல் - வண்ணப்பா விதிகள்" + '\n'
        len_arr = [line.word_count() for line in self.line_objects]
        
        """ _VANNAPA_RULE_1 """
        expected_sandha_fraction = self.poem_check_fraction
        has_sandha_ozhungu, sandha_ozhungu, actual_fraction = self.has_sandha_ozhungu(expected_sandha_fraction)
        paa_str += RULE_CHECK(has_sandha_ozhungu) + _VANNAPA_RULE_1 + '\n\t (' + ' '.join(sandha_ozhungu) + ')' + PERCENT_2.format(actual_fraction, expected_sandha_fraction) +'\n'
        """ _VANNAPA_RULE_2 """
        expected_kuzhippu_fraction = self.poem_check_fraction
        has_sandha_kuzhippu, sandha_kuzhippu, actual_fraction = self.has_sandha_kuzhippu(expected_kuzhippu_fraction)
        paa_str += RULE_CHECK(has_sandha_kuzhippu) + _VANNAPA_RULE_2 + '\n\t (' + ' '.join(sandha_kuzhippu) + ')' + PERCENT_2.format(actual_fraction, expected_kuzhippu_fraction) +'\n'
        """ _VANNAPA_RULE_3 """
        adi_edhugai_check = self.has_adi_edhugai()
        paa_str += RULE_CHECK(adi_edhugai_check) + _VANNAPA_RULE_3+"\t"+self.adi_edhugai_words+"\n"
        """ _VANNAPA_RULE_4 """
        kalai_monai_check = self.has_kalai_monai()
        paa_str += RULE_CHECK(kalai_monai_check) + _VANNAPA_RULE_4+"\t"+self.kalai_monai_words+"\n"
        paa_check = has_sandha_ozhungu and has_sandha_kuzhippu and adi_edhugai_check and kalai_monai_check 
        paa_str = "வண்ணப்பா விதிகள் " + ("பொருந்துகிறது." if (paa_check) else "பொருந்தவில்லை.") + "\n" + paa_str
        if paa_check:
            paa_str += "\t"+self.get_kuzhippu_thongal_kalai()
        return [paa_check, poem_type, paa_str]
    def __check_for_vannapaa_old(self):
        return self.has_sandha_kuzhippu()

        

if __name__ == '__main__':
    """
    song = "முத்து, வற்றல், விட்டம், மொய்த்த, மெய்ச்சொல், கர்த்தன்\n"+ \
"அக்கா, முட்டாள், விட்டான், பொய்க்கோ, நெய்க்கோல், மெய்க்கோன்\n"+ ]
"பாட்டு, பாட்டன், கூத்தன், வார்ப்பு, தூர்த்தன், வாழ்த்தல்\n"+ \
"தாத்தா, மூச்சால், சாத்தான், வேய்ப்பூ, மாய்த்தோர், வார்த்தோன்\n"+ \
"பந்து, உம்பர், சுண்டல், மொய்ம்பு, மொய்ம்பர், மொய்ம்பன்\n"+ \
"அந்தோ, வந்தார், தந்தேன், மொய்ம்பா, மொய்ம்போர், மொய்ம்போன்\n"+ \
"வேந்து, வேந்தர், பாங்கன், பாய்ந்து, சார்ங்கர், சார்ங்கம்\n"+ \
"சேந்தா, வாங்கார், நான்றான், நேர்ந்தோ, சார்ந்தார், மாய்ந்தான்"
    """
    #"""
    song = "பஞ்சியொளி(ர்) விஞ்சுகுளிர் பல்லவம னுங்க\n"+ \
"செஞ்செவிய கஞ்சநிகர் சீறடியள் ஆகி\n"+ \
"அஞ்சலிள மஞ்ஞையென அன்னமென மின்னும்\n"+ \
"வஞ்சியென நஞ்சமென வஞ்சமகள் வந்தாள்"
    #"""
    """
    song = "விடமார் பணிபுலி வானோர் தொழவளர்\n"+ \
"புலியூர்ச் சபையினி னடித்து நின்றன\n"+ \
"வெறியார் நறுமலர் தேனோ டுறைதலி\n"+ \
"னறுகாற் பறவைக ளிரைத்தெ ழுந்தன"
    """
    """
    song = "பொன்னி லங்கு பூங்கொ டிப்பொ லஞ்செய் கோதை வில்லிட\n"+ \
"மின்னி லங்கு மேக லைகள் ஆர்ப்ப ஆர்ப்ப எங்கணும்\n"+ \
"தென்னன் வாழ்க வாழ்க என்று சென்று பந்த டித்துமே\n"+ \
"தேவ ரார மார்பன் வாழ்க என்று பந்த டித்துமே"
    """
    from timeit import default_timer as timer
    start = timer()
    #"""
    song = "கைத்தல நிறைகனி யப்பமொ டவல்பொரி கப்பிய கரிமுக  னடிபேணிக்  கற்றிடு மடியவர் புத்தியி லுறைபவ  கற்பக மெனவினை கடிதேகும் \n" + \
    "மத்தமு மதியமும் வைத்திடு மரன்மகன்  மற்பொரு திரள்புய  மதயானை  மத்தள வயிறனை உத்தமி புதல்வனை  மட்டவிழ் மலர்கொடு  பணிவேனே\n" + \
    "முத்தமி ழடைவினை முற்படு கிரிதனில்  முற்பட எழுதிய முதல்வோனே  முப்புர மெரிசெய்த அச்சிவ னுறைரதம்  அச்சது பொடிசெய்த அதிதீரா\n"+ \
    "அத்துய ரதுகொடு சுப்பிர மணிபடும் அப்புன மதனிடை இபமாகி  அக்குற மகளுட னச்சிறு முருகனை அக்கண மணமருள் பெருமாளே"
    #"""
    """
    song = "சருவியி கழ்ந்தும ருண்டுவெ குண்டுறு  சமயமு மொன்றிலை யென்றவ ரும்பறி  தலையரு நின்றுக லங்கவி ரும்பிய - தமிழ்கூறுஞ்  சலிகையு நன்றியும் வென்றியு மங்கள  பெருமைக ளுங்கன முங்குண மும்பயில் சரவண மும்பொறை யும்புக ழுந்திகழ் - தனிவேலும் \n" + \
"விருதுது லங்கசி கண்டியி லண்டரு முருகிவ ணங்கவ ரும்பத மும்பல விதரண முந்திற முந்தர முந்தினை - புனமானின்  ம்ருகமத குங்கும கொங்கையில் நொந்தடி  வருடிம ணந்துபு ணர்ந்தது வும்பல  விஜயமு மன்பின்மொ ழிந்துமொ ழிந்தியல் - மறவேனே \n" + \
"கருதியி லங்கைய ழிந்துவி டும்படி அவுணர டங்கம டிந்துவி ழும்படி  கதிரவ னிந்துவி ளங்கிவ ரும்படி - விடுமாயன்  கடகரி யஞ்சிந டுங்கிவ ருந்திடு மடுவினில் வந்துத வும்புய லிந்திரை கணவன ரங்கமு குந்தன்வ ருஞ்சக - டறமோதி \n" + \
"மருதுகு லுங்கிந லங்கமு னிந்திடு வரதன லங்கல்பு னைந்தரு ளுங்குறள் வடிவனெ டுங்கடல் மங்கவொ ரம்புகை - தொடுமீளி மருகபு ரந்தர னுந்தவ மொன்றிய பிரமபு ரந்தனி லுங்குக னென்பவர் மனதினி லும்பரி வொன்றிய மர்ந்தருள் - பெருமாளே"
    """
    """
    song = "தினமணி சார்ங்கபாணி யெனமதிள் நீண்டுசால  தினகர னேய்ந்தமாளி - கையிலாரஞ்  செழுமணி சேர்ந்தபீடி கையிலிசை வாய்ந்தபாடல்  வயிரியர் சேர்ந்துபாட - இருபாலும் \n" + \
"இனவளை பூண்கையார்க வரியிட வேய்ந்துமாலை புழுககில் சாந்துபூசி - யரசாகி  இனிதிறு மாந்துவாழு மிருவினை நீண்டகாய மொருபிடி சாம்பலாகி - விடலாமோ \n" + \
"வனசர ரேங்கவான முகடுற வோங்கிஆசை மயிலொடு பாங்கிமார்க - ளருகாக  மயிலொடு மான்கள்சூழ வளவரி வேங்கையாகி மலைமிசை தோன்றுமாய - வடிவோனே \n" + \
"கனசமண் மூங்கர்கோடி கழுமிசை தூங்கநீறு கருணைகொள் பாண்டிநாடு - பெறவேதக்  கவிதரு காந்தபால கழுமல பூந்தராய கவுணியர் வேந்ததேவர் - பெருமாளே"
    """
    """
    song = "கனகந்திரள் கின்றபெ ருங்கிரி தனில்வந்துத கன்தகன் என்றிடு கதிர்மிஞ்சிய செண்டைஎ றிந்திடு  - கதியோனே கடமிஞ்சிஅ நந்தவி தம்புணர் கவளந்தனை உண்டுவ ளர்ந்திடு கரியின்றுணை என்றுபி றந்திடு - முருகோனே\n"+\
    "பனகந்துயில் கின்றதி றம்புனை கடல்முன்புக டைந்தப ரம்பரர் படரும்புயல் என்றவர் அன்புகொள் - மருகோனே பலதுன்பம் உழன்றுக லங்கிய சிறியன்புலை யன்கொலை யன்புரி பவமின்றுக ழிந்திட வந்தருள் - புரிவாயே\n"+\
    "அனகன்பெயர் நின்றுரு ளுந்திரி புரமுந்திரி வென்றிட இன்புடன் அழலுந்தந குந்திறல் கொண்டவர் - புதல்வோனே அடல்வந்துமு ழங்கியி டும்பறை டுடுடுண்டுடு டுண்டுடு டுண்டென அதிர்கின்றிட அண்டநெ ரிந்திட - வருசூரர்\n"+\
    "மனமுந்தழல் சென்றிட அன்றவர் உடலுங்குட லுங்கிழி கொண்டிட மயில்வென்றனில் வந்தரு ளுங்கன - பெரியோனே மதியுங்கதி ருந்தட வும்படி உயர்கின்றவ னங்கள்பொ ருந்திய வளமொன்றுப ரங்கிரி வந்தருள் - பெருமாளே"
    """
    """
    song = "மதப்பட்டவி சாலக போலமு முகப்பிற்சன வாடையு மோடையு மருக்கற்புர லேபல லாடமு  - மஞ்சையாரி வயிற்றுக்கிடு சீகர பாணியு மிதற்செக்கர்வி லோசன வேகமு மணிச்சத்தக டோரபு ரோசமு - மொன்றுகோல\n"+\
"விதப்பட்டவெ ளானையி லேறியு நிறைக்கற்பக நீழலி லாறியும் விஷத்துர்க்கன சூளிகை மாளிகை - யிந்திலோகம் விளக்கச்சுரர் சூழ்தர வாழ்தரு பிரப்புத்வகு மாரசொ ரூபக வெளிப்பட்டெனை யாள்வய லூரிலி - ருந்தவாழ்வே\n"+\
"இதப்பட்டிட வேகம லாலய வொருத்திக்கிசை வானபொ னாயிர மியற்றப்பதி தோறுமு லாவிய - தொண்டர்தாள இசைக்கொக்கவி ராசத பாவனை யுளப்பெற்றொடு பாடிட வேடையி லிளைப்புக்கிட வார்மறை யோனென - வந்துகானிற்\n"+\
"றிதப்பட்டெதி ரேபொதி சோறினை யவிழ்த்திட்டவி நாசியி லேவரு திசைக்குற்றச காயனு மாகிம - றைந்துபோமுன் செறிப்பித்த கராவதின் வாய்மக வழைப்பித்தபு ராணக்ரு பாகர திருப்புக்கொளி யூருடை யார்புகழ் - தம்பிரானே"
    """
    """
    song = "முத்தைத்தரு பத்தித் திருநகை  அத்திக்கிறை சத்திச் சரவண முத்திக்கொரு வித்துக் குருபர - எனவோதும் முக்கட்பர மற்குச் சுருதியின் முற்பட்டது கற்பித் திருவரும் முப்பத்துமு வர்க்கத் தமரரும் - அடிபேணப்\n"+\
    "பத்துத்தலை தத்தக் கணைதொடு ஒற்றைக்கிரி மத்தைப் பொருதொரு பட்டப்பகல் வட்டத் திகிரியில் - இரவாகப் பத்தற்கிர தத்தைக் கடவிய பச்சைப்புயல் மெச்சத் தகுபொருள் பட்சத்தொடு ரட்சித் தருள்வதும் - ஒருநாளே\n"+\
    "தித்தித்தெய ஒத்தப் பரிபுர நிர்த்தப்பதம் வைத்துப் பயிரவி திக்கொட்கந டிக்கக் கழுகொடு - கழுதாடத் திக்குப்பரி அட்டப் பயிரவர் தொக்குத்தொகு தொக்குத் தொகுதொகு சித்ரப்பவு ரிக்குத் த்ரிகடக - எனவோதக்\n"+\
    "கொத்துப்பறை கொட்டக் களமிசை குக்குக்குகு குக்குக் குகுகுகு குத்திப்புதை புக்குப் பிடியென - முதுகூகை கொட்புற்றெழ நட்பற் றவுணரை வெட்டிப்பலி யிட்டுக் குலகிரி குத்துப்பட ஒத்துப் பொரவல - பெருமாளே\n"
    """
    """
    song = "ஐம்புலன் இச்சைகள் மூட, வஞ்சம னத்தினன் ஆகி  அஞ்சனம் இட்டழ கேறும் .. விழிமாதர் அங்கசு கத்தினை நாடி, வெந்துயர் உற்றிட வாடி  அஞ்சுபி றப்பொரு கோடி .. பெறலாமோ\n"+\
"வம்புவ னப்புல வாத வண்டமிழ் நித்தலும் ஓதி மன்றினில் நர்த்தனம் ஆடும் .. உனதாளை மங்கலம் உற்றிடு மாறு, வெம்பவம் அற்றிடு மாறு வந்துவ ழுத்திடு மாறு .. வரமீயாய்\n"+\
"நம்பும வர்க்கெளி தாகி, அன்றிரு வர்க்கரி தான நம்பம ழுப்படை சூலம் .. உடையானே நங்கையி டப்புறம் ஆக, அஞ்சடை யிற்புனல் ஓட நஞ்சுமி டற்றினில் நீல .. மணியாகும்\n"+\
"சம்புவு னைத்தொழு மாணி உய்ந்துயிர் பெற்றிட, வாதை தந்துது ரத்திய கோபம் மிகுகாலன் தண்டனை பெற்றுயிர் கால அங்கவ னைச்செறு கால தண்புற வத்தினில் மேய .. பெருமானே"
    """
    #tp = Sandhapa("முத்தைத்தரு பத்தித் திருநகை அத்திக்கிறை சத்திச் சரவண முத்திக்கொரு வித்துக் குருபர  - எனவோதும்")
    #"""
    #print(utils.get_character_type_counts(tp.text()))
    """
    from yaappu.grammar import Yaappu
    tp = Yaappu(song)
    results,_ = tp.analyze(get_individual_poem_analysis=False)
    for line in results[1:]:
        print(line)
    """
    tp = Vannapa(song)
    tp.asaigaL()
    paa_check, poem_type, paa_str = tp.check_for_vannapaa()
    print(song)
    print(poem_type,"\n", paa_str)
    """
    t1 = ["அடி மோனை", "அடி எதுகை", "அடி இயைபு"]
    t2 = [0,1,-1]
    result = ''
    for t in t2:
        result += "\t\t\t{}".format(t1[t2.index(t)])+"\n"
        result += (tp.adi_thodai_lines(t,'<>'))
    print(result)
    """
    exit()
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
    print(timer()-start,'seconds')    