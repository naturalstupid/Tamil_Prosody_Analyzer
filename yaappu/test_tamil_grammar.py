from grammar import Ezhuthu, Sol, Adi, Yiyarpa, Yaappu
import utils as utils
#from yaappu import Yaappu
char_class_name = 'Ezhuthu'
word_class_name = 'Sol'
line_class_name = 'Adi'
poem_class_name = 'Yiyarpa'
yaappu_class_name = 'Yaappu'
test_input_folder = 'test_input/'

GREEN_CHECK = u'\u2714  '
RED_CROSS = u'\u274C  '
GEQ = u' \u2265 '
STATUS_CHECK = lambda rc : GREEN_CHECK if rc else RED_CROSS

def unit_test(test_name,expected,actual, assert_test=False):
    unit_test.counter +=1
    status = 'Passed'
    if (expected != actual):
        status = 'Failed'
        unit_test.failed += 1
        unit_test.failed_tests += str(unit_test.counter) +';'
    print('Test#:',unit_test.counter,'Test:',STATUS_CHECK(expected == actual)+test_name, \
          "\tExpected Result:",expected, \
          '\tActual Result :',actual, \
           '\tStatus:',status
          )
    if assert_test:
         assert(status)

def class_method_unit_test(class_name, init_value, function_name, expected_result, *args):
    obj = eval(class_name)(init_value)
    test_name = str(class_name) +'-' + function_name + ' ' + init_value +' args: '+' '.join(map(str, args))
    actual_result = getattr(obj,function_name)(*args)
    unit_test(test_name,expected_result,actual_result)

def class_attribute_unit_test(class_name, init_value, attribute_name, expected_result):
    obj = eval(class_name)(init_value)
    test_name = str(class_name) +'-' + attribute_name + ' ' + init_value
    actual_result = getattr(obj,attribute_name)
    unit_test(test_name,expected_result,actual_result)

def run_yaappu_unit_tests():
    run_yaappu_venpa_unit_tests()
    run_yaappu_asiriyapa_unit_tests()
    run_yaappu_kalipa_unit_tests()
    run_yaappu_vanjipa_unit_tests()
    run_yaappu_venpa_subtype_tests()
    run_yaappu_asiriyapa_subtype_tests()
    run_yaappu_kalipa_subtype_tests()
    run_yaappu_vanjipa_subtype_tests()

def run_yaappu_vanjipa_subtype_tests():
    vanjipavinam_map = {"Vanjippavinam_Virutham.txt" : "வஞ்சி விருத்தம் வஞ்சிப்பாவினம்",
    "Vanjippavinam_Thazhisai.txt" : "வஞ்சித் தாழிசை வஞ்சிப்பாவினம்",
    "Vanjippavinam_ThuRai.txt" : "வஞ்சித்  துறை வஞ்சிப்பாவினம்",}
    for poem_file in vanjipavinam_map:
        #print(poem_file, venpa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_vanjipaavinam()
        unit_test(poem_file, vanjipavinam_map.get(poem_file).strip(), paa_check[1].strip())
    
def run_yaappu_kalipa_subtype_tests():
    kalipavinam_map = {"Kalipaavinam_KaliVirutham.txt" : "கலி விருத்தம் கலிப்பாவினம்",
    "Kalipaavinam_ThuRai.txt" : "கலித்துறை கலிப்பாவினம்",
    "Kalipaavinam_Thazhisai.txt" : "கலித் தாழிசை கலிப்பாவினம்",
    "Kalipaavinam_KattaLaiThuRai.txt" : "கட்டளைக் கலித்துறை கலிப்பாவினம்",}
    for poem_file in kalipavinam_map:
        #print(poem_file, venpa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_kalipaavinam()
        unit_test(poem_file, kalipavinam_map.get(poem_file).strip(), paa_check[1].strip())
    
def run_yaappu_asiriyapa_subtype_tests():
    asiriyapavinam_map = {"Asiriyappavinam_ThuRai_Madakkai_1.txt" : "ஆசிரியத் துறை ஆசிரியப்பாவினம்",
    "Asiriyappavinam_AruSeerViruthamtxt.txt" : "ஆசிரிய/வெளி விருத்தம் ஆசிரியப்பாவினம்",
    "Asiriyappavinam_ThuRai.txt" : "ஆசிரியத் துறை ஆசிரியப்பாவினம்",
    "Asiriyappavinam_Thazhisai.txt" : "ஆசிரியத் தாழிசை ஆசிரியப்பாவினம்",
    "Asiriyappavinam_ENSeerViruthamtxt.txt" : "ஆசிரிய/வெளி விருத்தம் ஆசிரியப்பாவினம்",
    "Asiriyappavinam_EzhuSeerViruthamtxt.txt" : "ஆசிரிய/வெளி விருத்தம் ஆசிரியப்பாவினம்",
    "Asiriyappavinam_ThuRai_Madakkai_2.txt" : "ஆசிரியத் துறை ஆசிரியப்பாவினம்",}
    for poem_file in asiriyapavinam_map:
        #print(poem_file, venpa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_asiriyapaavinam()
        unit_test(poem_file, asiriyapavinam_map.get(poem_file).strip(), paa_check[1].strip())
    
def run_yaappu_venpa_subtype_tests():
    venpaavinam_map = {"VenPaavinam_KuraLVeNSendhuRai.txt" : "குறள் துறை வெண்பாவினம்", 
                       "VenPaavinam_VeNThaazhisai.txt" : "வெண் தாழிசை வெண்பாவினம்",
                       "VenPaavinam_KuraLThaazhisai.txt" : "குறள்  தாழிசை வெண்பாவினம்", 
                       "VenPaavinam_VeLiViruttham.txt" : "வெளி விருத்தம் வெண்பாவினம்", 
                       "VenPaavinam_VeNThuRai.txt" : "வெண்டுறை வெண்பாவினம்", }
    for poem_file in venpaavinam_map:
        #print(poem_file, venpa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_venpaavinam()
        unit_test(poem_file, venpaavinam_map.get(poem_file).strip(), paa_check[1].strip())

def run_yaappu_venpa_unit_tests():
    venpa_map = {"VeNPA_oru_vikarpa_naerisai.txt" :  "ஒரு விகற்ப நேரிசை வெண்பா ", 
    "VenPa_pala_vikarpa_innisai.txt" : "இரு விகற்ப நேரிசை வெண்பா ",
    "VenPA_iru_vikarpa_naerisai.txt" : "பல விகற்ப நேரிசை வெண்பா ",
    "VeNPa_oru_vikarpa_kuraL.txt" : "ஒரு விகற்ப குறள் வெண்பா ",
    "VenPa_naerisa_sindhiyal.txt" : "ஒரு விகற்ப சிந்தியல் வெண்பா ",
    "veNPa_pahrodai.txt" : "பல விகற்ப பஃறொடை வெண்பா ",
    "VeNPa_innisai_sindhiyal.txt" : "இரு விகற்ப சிந்தியல் வெண்பா ",
    "VeNPa_oru_vikarpa_innisai.txt" : "ஒரு விகற்ப இன்னிசை வெண்பா ",
    "VeNPa_iru_vikarpa_kuraL.txt" : "ஒரு விகற்ப குறள் வெண்பா ",}
    for poem_file in venpa_map:
        #print(poem_file, venpa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_venpaa()
        unit_test(poem_file, venpa_map.get(poem_file).strip(), paa_check[1].strip())
    
def run_yaappu_asiriyapa_unit_tests():
    asiriyapa_map={"aasiriyappa_naerisai.txt" : "நேரிசை ஆசிரியப்பா",
    "aasiriyappa_iNaiKuRal.txt" : "இணைக்குறள் ஆசிரியப்பா",
    "asiriyappa_nilaimandila.txt":"நிலை மண்டில ஆசிரியப்பா ",}

    for poem_file in asiriyapa_map:
        #print(poem_file, venpa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_asiriyapaa()
        unit_test(poem_file, asiriyapa_map.get(poem_file).strip(), paa_check[1].strip())

def run_yaappu_kalipa_unit_tests():
    kalipa_map = {"kalippaa_veN.txt" : "வெண் கலிப்பா",
                  "kalippa_tharavu_kocchaga.txt" : "தரவு கொச்சகக் கலிப்பா",}
    for poem_file in kalipa_map:
        #print(poem_file, venpa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_kalipaa()
        unit_test(poem_file, kalipa_map.get(poem_file).strip(), paa_check[1].strip())

def run_yaappu_vanjipa_unit_tests():   
    vanjipa_map = {"vanchipa_sindhadi.txt" : "சிந்தடி வஞ்சிப்பா ",
    "vanchipaa_kuRaladi.txt" : "குறளடி வஞ்சிப்பா ",}
    for poem_file in vanjipa_map:
        #print(poem_file, vanjipa_map.get(poem_file))
        poem =  open(test_input_folder+ poem_file, "r", encoding="utf-8").read()
        ty = eval(yaappu_class_name)(poem)
        paa_check = ty.check_for_vanjipaa()
        unit_test(poem_file, vanjipa_map.get(poem_file).strip(), paa_check[1].strip())

def run_poem_unit_tests():
    poem = "சுரையாழ அம்மி மிதப்ப வரையனைய\r\n" + "யானைக்கு நீத்து முயற்கு நிலையென்ப\r\n" + "கானக நாடன் சுனை"
    class_method_unit_test(poem_class_name, poem, 'words', ['சுரையாழ', 'அம்மி', 'மிதப்ப', 'வரையனைய', 'யானைக்கு', 'நீத்து', 'முயற்கு', 'நிலையென்ப', 'கானக', 'நாடன்', 'சுனை'])
    class_method_unit_test(poem_class_name, poem, 'asai_words', ['சுரை/யா/ழ', 'அம்/மி', 'மிதப்/ப', 'வரை/யனை/ய', 'யா/னைக்/கு', 'நீத்/து', 'முயற்/கு', 'நிலை/யென்/ப', 'கா/னக', 'நா/டன்', 'சுனை'])
    class_method_unit_test(poem_class_name, poem, 'asaigaL', ['நிரை/நேர்/நேர்', 'நேர்/நேர்', 'நிரை/நேர்', 'நிரை/நிரை/நேர்', 'நேர்/நேர்/நேர்', 'நேர்/நேர்', 'நிரை/நேர்', 'நிரை/நேர்/நேர்', 'நேர்/நிரை', 'நேர்/நேர்', 'நிரை'])
    class_method_unit_test(poem_class_name, poem, 'seergaL', ['புளிமாங்காய்', 'தேமா', 'புளிமா', 'கருவிளங்காய்', 'தேமாங்காய்', 'தேமா', 'புளிமா', 'புளிமாங்காய்', 'கூவிளம்', 'தேமா', 'மலர்'],True)
    include_sub_type = True
    class_method_unit_test(poem_class_name, poem, 'thaLaigaL', \
       ['வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை'],include_sub_type)
    class_method_unit_test(poem_class_name, poem, 'osaigaL', \
      ['ஏந்திசைச் செப்பலோசை', 'தூங்கிசைச் செப்பலோசை', 'தூங்கிசைச் செப்பலோசை', 'ஏந்திசைச் செப்பலோசை', 'ஏந்திசைச் செப்பலோசை', 'தூங்கிசைச் செப்பலோசை', 'தூங்கிசைச் செப்பலோசை', 'ஏந்திசைச் செப்பலோசை', 'தூங்கிசைச் செப்பலோசை', 'தூங்கிசைச் செப்பலோசை'],include_sub_type)
    include_sub_type = False
    class_method_unit_test(poem_class_name, poem, 'thaLaigaL', \
      ['வெண்டளை', 'வெண்டளை', 'வெண்டளை', 'வெண்டளை', 'வெண்டளை', 'வெண்டளை', 'வெண்டளை', 'வெண்டளை', 'வெண்டளை', 'வெண்டளை'],include_sub_type)
    class_method_unit_test(poem_class_name, poem, 'osaigaL', \
      ['செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை', 'செப்பலோசை'],include_sub_type)

def run_line_unit_tests():
    run_line_linetype_tests()
    class_method_unit_test(line_class_name, "சுரையாழ அம்மி மிதப்ப வரையனைய", 'sandha_ozhungu', ['காய்', 'மா', 'மா', 'காய்'])
    run_line_thodai_tests()

def run_line_thodai_tests():
    line = "துணையில்லாத் துறவுநெறிக் கிறைவனாகி"
    expected_result = ['(து)ணையில்லாத்', '(து)றவுநெறிக்', 'கிறைவனாகி']
    thodai_index = 0
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் மோனை: இணை (1-2)', actual_result)
    
    line = "புணையெனத்"
    expected_result = ['(பு)ணையெனத்']
    thodai_index = 0
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் மோனை: இல்லை', actual_result)

    line = "திருவுறு திருந்தடி திசைதொழ"
    expected_result = ['(தி)ருவுறு', '(தி)ருந்தடி', '(தி)சைதொழ']
    thodai_index = 0
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் மோனை: கூழை (1-2-3)', actual_result)
    
    line = "வெருவுறும் நாற்கதி; வீடுநனி எளிதே"
    expected_result = ['(வெ)ருவுறும்', 'நாற்கதி', '(வீ)டுநனி', 'எளிதே']
    thodai_index = 0
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் மோனை: பொழிப்பு (1-3)', actual_result)

    line = "திருவுறு திருந்தடி திசைதொழ"
    expected_result = ['தி(ரு)வுறு', 'தி(ரு)ந்தடி', 'திசைதொழ']
    thodai_index = 1
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் எதுகை: இணை (1-2)', actual_result)
    
    line = "வெருவுறும் நாற்கதி; வீடுநனி எளிதே"
    expected_result = ['வெ(ரு)வுறும்', 'நாற்கதி', 'வீடுநனி', 'எ(ளி)தே']
    thodai_index = 1
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் எதுகை: ஒருஊ (1-4)', actual_result)
 
    line = "எயினடுவண் இனிதிருந் தெல்லோர்க்கும்"
    expected_result = ['எயினடுவ(ண்)', 'இனிதிரு(ந்)', 'தெல்லோர்க்கு(ம்)']
    thodai_index = -1
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் இயைபு: கூழை (1-2-3)', actual_result)
    
    line = "பயில்படுவினை பத்தியலாற் செப்பியோன்"
    expected_result = ['பயில்படுவினை', 'பத்தியலா(ற்)', 'செப்பியோ(ன்)']
    thodai_index = -1
    class_method_unit_test(line_class_name, line , 'seer_thodai_words', expected_result,thodai_index)
    actual_result = Adi(line).seer_thodai_types[thodai_index]
    unit_test(' '.join(expected_result), 'சீர் இயைபு: இணை (1-2)', actual_result)
    
    poem = "தனந்தரும் கல்வி தருமொரு நாளும் தளர்வறியா\n"+\
"மனந்தரும் தெய்வ வடிவும் தரும்நெஞ்சில் வஞ்சமில்லா"
    thodai_index = 0
    expected_result = 'அடி ' + utils.THODAI_TYPES[thodai_index] + ' இல்லை \n'
    class_method_unit_test(poem_class_name, poem , 'adi_thodai_lines', expected_result,thodai_index)
    thodai_index = 1
    expected_result = 'அடி ' + utils.THODAI_TYPES[thodai_index] + '\n' \
                    + "த(ன)ந்தரும் கல்வி தருமொரு நாளும் தளர்வறியா\nம(ன)ந்தரும் தெய்வ வடிவும் தரும்நெஞ்சில் வஞ்சமில்லா\n\n"
    class_method_unit_test(poem_class_name, poem , 'adi_thodai_lines', expected_result,thodai_index)
    thodai_index = -1
    expected_result = 'அடி ' + utils.THODAI_TYPES[thodai_index] + '\n' \
                    + "தனந்தரும் கல்வி தருமொரு நாளும் தளர்வறி(யா)\nமனந்தரும் தெய்வ வடிவும் தரும்நெஞ்சில் வஞ்சமில்(லா)\n\n"
    class_method_unit_test(poem_class_name, poem , 'adi_thodai_lines', expected_result,thodai_index)


def run_line_linetype_tests():
    for i in range(1,16):
        chk = 11 if i > 11 else i
        class_method_unit_test(line_class_name, ' '.join(["சீர்"] * i ), 'line_type', utils.LINE_TYPES[chk])
             
def run_word_unit_tests():
    class_method_unit_test(word_class_name,'பெண்மைபோல்','asai_word','பெண்/மைபோல்')
    # Seer Type Tests
    for s in range(4):
        keys = utils.SEER_TYPES[s].keys()
        for key in keys:
            seer = utils.SEER_TYPES[s].get(key)
            asai = key.replace(' ','/')
            combined_seer = seer + ' ' + asai
            class_method_unit_test(word_class_name,seer,'asaigaL',asai)
            class_method_unit_test(word_class_name,seer,'seer_type',seer)
            thaLai_exp = utils.get_keys_containing_string(utils.THALAI_TYPES, combined_seer)
            if thaLai_exp:
                thaLai_exp = thaLai_exp[0]
            else:
                thaLai_exp = ''
            class_method_unit_test(word_class_name,seer,'thaLai_type',thaLai_exp,seer)
            osai_exp = utils.OSAI_TYPES.get(thaLai_exp)
            class_method_unit_test(word_class_name,seer,'osai_type',osai_exp,seer)
    
    run_word_venpaa_seer_unit_tests()        
    run_word_thodai_unit_tests()
    run_word_sandha_seer_tests()

def run_word_venpaa_seer_unit_tests():
    class_method_unit_test(word_class_name,'நாள்', 'venpaa_seer','நாள்')
    class_method_unit_test(word_class_name,'மலர்', 'venpaa_seer','மலர்')
    class_method_unit_test(word_class_name,'காசு', 'venpaa_seer','காசு')
    class_method_unit_test(word_class_name,'பிறப்பு', 'venpaa_seer','பிறப்பு')

def run_word_sandha_seer_tests():
    class_method_unit_test(word_class_name,'புளிமா', 'sandha_seer','மா')
    class_method_unit_test(word_class_name,'தேமாங்காய்', 'sandha_seer','காய்')
    class_method_unit_test(word_class_name,'புளிமாங்கனி', 'sandha_seer','கனி')
    class_method_unit_test(word_class_name,'புளிமாநறும்பூ', 'sandha_seer','பூ')
    class_method_unit_test(word_class_name,'கூவிளந்தண்ணிழல்', 'sandha_seer','ணிழல்')
    class_method_unit_test(word_class_name,'கருவிளம்', 'sandha_seer','விளம்')
    
def run_word_thodai_unit_tests():
    class_method_unit_test(word_class_name,'அகல', 'thodai_matches',True,'ஆழ',0)
    class_method_unit_test(word_class_name,'வளர்த்த', 'thodai_matches',True,'மார்பில்',0)
    class_method_unit_test(word_class_name,'இருதலைக்', 'thodai_matches',True,'எறும்பு',0)
    class_method_unit_test(word_class_name,'ஓட்டைச்', 'thodai_matches',True,'ஊத',0)
    class_method_unit_test(word_class_name,'தொட்டிற்', 'thodai_matches',True,'சுடுகாடு',0)
    class_method_unit_test(word_class_name,'நலிந்தோர்க்', 'thodai_matches',True,'ஞாயிறும்',0)
    
    class_method_unit_test(word_class_name,'தட்டு', 'thodai_matches',True,'பட்டு',1)
    class_method_unit_test(word_class_name,'தட்டு', 'thodai_matches',False,'பாட்டு',1)
    class_method_unit_test(word_class_name,'உலகம்', 'thodai_matches',True,'நிலைபெ',1)
    class_method_unit_test(word_class_name,'தூவி', 'thodai_matches',True,'தேவு',1)
    class_method_unit_test(word_class_name,'தக்கார்', 'thodai_matches',True,'எச்சத்தாற்',1)
    class_method_unit_test(word_class_name,'வரவு', 'thodai_matches',True,'செலவு',1)
    class_method_unit_test(word_class_name,'அன்பன்', 'thodai_matches',True,'நண்பன்',1)
    
    class_method_unit_test(word_class_name,'அன்பன்', 'thodai_matches',True,'நண்பன்',-1)
    class_method_unit_test(word_class_name,'சங்கே', 'thodai_matches',True,'அன்பே',-1)
    class_method_unit_test(word_class_name,'கலா', 'thodai_matches',True,'பலா',-1)
    class_method_unit_test(word_class_name,'கலா', 'thodai_matches',False,'காலா',-1)
    class_method_unit_test(word_class_name,'அண்டி', 'thodai_matches',False,'தோண்டி',-1)
    class_method_unit_test(word_class_name,'ஆண்டி', 'thodai_matches',True,'தோண்டி',-1)
    class_method_unit_test(word_class_name,'குரம்பை', 'thodai_matches',True,'பேதை',-1)
    wrd = Sol('வையகத்')
    unit_test(wrd.text() + ' Aikaaram first letter IS_NEDIL TRUE', True, wrd.tamil_char_objects[0].is_nedil())
    wrd = Sol('யானைக்கு')
    unit_test(wrd.text() + ' Aikaaram Middle letter IS_NEDIL FALSE', False, wrd.tamil_char_objects[1].is_nedil())
    wrd = Sol('வெண்டளை')
    unit_test(wrd.text() + ' Aikaaram Lastletter IS_NEDIL FALSE', False, wrd.tamil_char_objects[-1].is_nedil())
        
def run_character_unit_tests():
    class_method_unit_test(char_class_name, '', 'is_kuril', False)
    class_method_unit_test(char_class_name, 'க்ஷை', 'is_kuril', True)
    class_method_unit_test(char_class_name, 'க்ஷை', 'is_vada_ezhuthu', True)
    class_method_unit_test(char_class_name, 'கூ', 'is_nedil', True)
    class_method_unit_test(char_class_name, 'ங்', 'is_otru', True)
    class_method_unit_test(char_class_name, 'க', 'is_vallinam', True)
    class_method_unit_test(char_class_name, 'ங்', 'is_mellinam', True)
    class_method_unit_test(char_class_name, 'வி', 'is_yidaiyinam', True)

def run_all_unit_tests():
  #call unit tests here below "
  run_character_unit_tests()
  run_word_unit_tests()
  run_line_unit_tests()
  run_poem_unit_tests()
  run_yaappu_unit_tests()

if __name__ == '__main__':
    unit_test.counter = 0
    unit_test.failed=0
    unit_test.failed_tests = ''

    run_all_unit_tests()
    #run_line_thodai_tests()
      
    if unit_test.failed > 0:
        print(str(unit_test.failed)+ ' out of ' + str(unit_test.counter) + " tests Failed. Test id's of failed tests:",unit_test.failed_tests)
    else:
        print('All (' + str(unit_test.counter)+') unit tests passed.')
    exit()
    