from yaappu import utils
_நிறுத்தற்குறிகள் = ['.', ',',':','?',';','-']
_நிலைமொழி_எழுத்துக்கள்_2_1_1 = utils.UYIRGAL + list(utils.YIDAIYINAM[-6:]) + list(utils.MELLINAM[-5:])
_நிலைமொழி_விதிவிலக்குகள் = ['உரிஞ் ','பொருந் ','வெரிந் ','அவ்', 'இவ்', 'உவ்', 'தெவ்']
def _get_uyir_mey(mey, uyir):
    uyir_mey = ''
    uyir_index =  utils.UYIRGAL.index(uyir)
    mey_index =  utils.MEYGAL.index(mey)
    if uyir_index==0:
        uyir_mey = utils.TAMIL_UNICODE_1[mey_index]
    else:
        uyir_mey = utils.TAMIL_UNICODE_1[mey_index]+utils.TAMIL_UNICODE_2[uyir_index-1]
    return uyir_mey

def _split_uyir_mey(uyir_mey):
    uyir_mey_characters = []
    uyir_mey_chars = utils.get_unicode_characters(uyir_mey)
    for um_char in uyir_mey_chars:
        first_morpheme = utils.get_first_morpheme(um_char)
        last_morpheme = utils.get_last_morpheme(um_char)
        if first_morpheme:
            uyir_mey_characters.append(first_morpheme)
        if last_morpheme and (last_morpheme != first_morpheme) : # single mey ezhuthu
            uyir_mey_characters.append(last_morpheme)
        #print(um_char,first_morpheme,last_morpheme)
    return uyir_mey_characters
def _punctuation_check(word1, word2):
    if word1.strip()[-1] in _நிறுத்தற்குறிகள்:
        return word1+' '+ word2
def check_rule_1(word1, word2):
    word1 = word1.strip()
    word2 = word2.strip()
    if word1 =="" or word2 =="":
        return word1+' '+ word2
    corrected_sentence = ''
    yagaram_chars = ["இ","ஈ", "ஐ"]
    vagaram_chars = ["ஓ"]
    combined_word = ''
    word1_last_char = utils.get_last_morpheme( utils.get_unicode_characters(word1)[-1] )
    word2_first_char = utils.get_first_morpheme( utils.get_unicode_characters(word2)[0] )
    print(word1,word1_last_char, word2,word2_first_char)
    if word1_last_char in utils.UYIRGAL:
        print('word1_last_char in utils.UYIRGAL')
        if word1_last_char in yagaram_chars:
            print('word1_last_char in yagaram_chars')
            tmp_char = ""
            ya = "ய";
            if (word2_first_char == "அ"):
                print('word2_first_char is அ')
                tmp_char = ya
            else:
                print('word2_first_char is NOT அ')
                i = utils.get_index(utils.UYIRGAL,word2_first_char)
                if (i>0):
                    tmp_char = ya + utils.TAMIL_UNICODE_2[i-1]
                else:
                    tmp_char=""
                print('tmp_char',tmp_char)
            tmp_str = "" 
            if tmp_char != "": 
                tmp_str = tmp_char + word2[1:]
            else:
                tmp_str = word2
            print('tmp_str',tmp_str)
            combined_word = word1 + tmp_str
        else:
            print('word1_last_char in yagaram_chars')
            tmp_char = ""
            va = "வ"
            if (word2_first_char =="அ"):
                print('word2_last_char is அ')
                tmp_char = va
            else:
                print('word2_last_char is NOT அ')
                i = utils.get_index(utils.UYIRGAL,word2_first_char)
                if (i>0):
                    tmp_char = va + utils.TAMIL_UNICODE_2[i-1]
                else:
                    tmp_char=""
                print('tmp_char',tmp_char)
            tmp_str = "" 
            if tmp_char != "": 
                tmp_str = tmp_char + word2[1:]
            else:
                tmp_str = word2
            print('tmp_str',tmp_str)
        combined_word = word1 + tmp_str
        print('combned_word',combined_word)
        corrected_sentence += combined_word + ' '
        print('corrected_sentence',corrected_sentence)
    return corrected_sentence

        
if __name__ == '__main__':
    word1 = "வர"
    word2 = "இல்லை"
    corrected_words = check_rule_1(word1, word2)
    print(word1,word2,'corrected_words',corrected_words)
    word1 = "மணி"
    word2 = "அடித்தான்"
    corrected_words = check_rule_1(word1, word2)
    print(word1,word2,'corrected_words',corrected_words)
    word1 = "பல"
    word2 = "இடங்கள்"
    corrected_words = check_rule_1(word1, word2)
    print(word1,word2,'corrected_words',corrected_words)
    word1 = "தீ"
    word2 = "அணைப்பு"
    corrected_words = check_rule_1(word1, word2)
    print(word1,word2,'corrected_words',corrected_words)
    word1 = "கை"
    word2 = "குழந்தை"
    corrected_words = check_rule_1(word1, word2)
    print(word1,word2,'corrected_words',corrected_words)
    #exit()
    #uyir_mey = s._get_uyir_mey("வ்", "அ")
    #print(uyir_mey,uyir_mey[0],uyir_mey[-1])
    print(_split_uyir_mey('கைக்குழந்தை'))