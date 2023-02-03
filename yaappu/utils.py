# -*- coding: utf-8 -*-
from yaappu import grammar
import string
from itertools import islice
from operator import itemgetter
from collections import Counter
from enum import IntEnum
_TREAT_AAYDHAM_AS_KURIL = False
_TREAT_KUTRIYALIGARAM_AS_OTRU = False    
"""  _CHARACTER_TYPES keys should match is_xxx functions of grammar.Ezhuthu  """
_CHARACTER_TYPES = {'kuril':"குறில்கள்",'nedil':"நெடில்கள்",'uyir_ezhuthu':"உயிர் எழுத்துக்கள்",'mey_ezhuthu':"மெய்யெழுத்துக்கள்",
                    'uyir_mey_ezhuthu':"உயிர்மெய் எழுத்துக்கள்",'vada_ezhuthu':"வட எழுத்துக்கள்", 'vallinam':"வல்லின எழுத்துக்கள்",
                    'yidaiyinam':"இடையின எழுத்துக்கள்",'mellinam':"மெல்லின எழுத்துக்கள்",'aaydham':"ஆய்த எழுத்து",'aikaaram':"ஐகாரம்",
                    'aukaaram':"ஒளகாரம்",'kutriyalugaram':"குற்றியலுகரம்",'kutriyaligaram':"குற்றியலிகரம்",'magarakurukkam':"மகரகுருக்கம்",
                    "uyiralabedai" : "உயிரளபெடை" , "otralabedai" : "ஒற்றளபெடை" }    
AYDHAM = ('ஃ')
UYIRGAL = ["அ","ஆ","இ","ஈ","உ","ஊ","எ","ஏ","ஐ","ஒ","ஓ","ஔ"]
MEYGAL=("க்","ங்","ச்","ஞ்","ட்","ண்","த்","ந்","ன்","ப்","ம்","ய்","ர்","ற்","ல்","ள்","ழ்","வ்","ஜ்","ஷ்","ஸ்","ஹ்","க்ஷ்","ஃ","்",)
AIKAARAM = ("ஐ","கை","ஙை","சை","ஞை","டை","ணை","தை","நை","னை","பை","மை","யை","ரை","றை","லை","ளை","ழை",
            "வை","ஜை","ஷை","ஸை","ஹை","க்ஷை","ை",)
AUKAARAM = ("ஔ","கௌ","ஙௌ","சௌ","ஞௌ","டௌ","ணௌ","தௌ","நௌ","னௌ","பௌ",
    "மௌ","யௌ","ரௌ","றௌ","லௌ","ளௌ","ழௌ","வௌ","ஜௌ","ஷௌ","ஸௌ","ஹௌ","க்ஷௌ","ௌ",)
KURILGAL = ("அ","இ","உ","எ","ஐ","ஒ",  "க","கி","கு","கெ","கை","கொ",
            "ங","ஙி","ஙு","ஙெ","ஙை","ஙொ","ச","சி","சு","செ","சை","சொ","ஞ","ஞி","ஞு","ஞெ","ஞை","ஞொ",
            "ட","டி","டு","டெ","டை","டொ","ண","ணி","ணு","ணெ","ணை","ணொ","த","தி","து","தெ","தை","தொ",
            "ந","நி","நு","நெ","நை","நொ","ன","னி","னு","னெ","னை","னொ","ப","பி","பு","பெ","பை","பொ",
            "ம","மி","மு","மெ","மை","மொ","ய","யி","யு","யெ","யை","யொ","ர","ரி","ரு","ரெ","ரை","ரொ",
            "ற","றி","று","றெ","றை","றொ","ல","லி","லு","லெ","லை","லொ","ள","ளி","ளு","ளெ","ளை","ளொ",
            "ழ","ழி","ழு","ழெ","ழை","ழொ","வ","வி","வு","வெ","வை","வொ","ஜ","ஜி","ஜூ","ஜெ","ஜை","ஜொ",
            "ஷ","ஷி","ஷூ","ஷெ","ஷை","ஷொ", "ஸ","ஸி","ஸூ","ஸெ","ஸை","ஸொ","ஹ","ஹி","ஹூ","ஹெ","ஹை","ஹொ",
            "க்ஷ","க்ஷி","க்ஷூ","க்ஷெ","க்ஷை","க்ஷை","க்ஷொ","ி","ு","ெ","ை","ொ") #,AUKAARAM,AIKAARAM)
NEDILGAL = ("ஆ","ஈ","ஊ","ஏ","ஓ","கா","கீ","கூ","கே","கோ","ஙா","ஙீ","ஙூ","ஙே","ஙோ",
            "சா","சீ","சூ","சே","சோ","ஞா","ஞீ","ஞூ","ஞே","ஞோ","டா","டீ","டூ","டே","டோ","ணா","ணீ","ணூ","ணே","ணோ",
            "தா","தீ","தூ","தே","தோ","நா","நீ","நூ","நே","நோ","னா","னீ","னூ","னே","னோ","பா","பீ","பூ","பே","போ",
            "மா","மீ","மூ","மே","மோ","யா","யீ","யூ","யே","யோ","ரா","ரீ","ரூ","ரே","ரோ","றா","றீ","றூ","றே","றோ",
            "லா","லீ","லூ","லே","லோ","ளா","ளீ","ளூ","ளே","ளோ","ழா","ழீ","ழூ","ழே","ழோ","வா","வீ","வூ","வே","வோ",
            "ஜா","ஜீ","ஜு","ஜே","ஜோ","ஷா","ஷீ","ஷு","ஷே","ஷோ","ஸா","ஸீ","ஸு","ஸே","ஸோ",
            "ஹா","ஹீ","ஹு","ஹே","ஹோ","க்ஷா","க்ஷீ","க்ஷு","க்ஷே","க்ஷோ","ா","ீ","ூ","ே","ோ",)
KUTRIYALUGARAM = ("கு","சு","டு","து","பு","று")
KUTRIYALIGARAM = ("கி","சி","டி","தி","பி","றி","மி",'னி')
VALLINAM = ("க","கா","கி","கீ","கூ","கு","கெ","கே","கை","கொ","கோ","கௌ","ச","சா","சி","சீ","சூ","சு","செ","சே","சை","சொ","சோ","சௌ","ட","டா","டி","டீ","டூ","டு","டெ","டே","டை","டொ","டோ","டௌ","த","தா","தி","தீ","தூ","து","தெ","தே","தை","தொ","தோ","தௌ","ப","பா","பி","பீ","பூ","பு","பெ","பே","பை","பொ","போ","பௌ","ற","றா","றி","றீ","றூ","று","றெ","றே","றை","றொ","றோ","றௌ", "க்","ச்", "ட்", "த்", "ப்", "ற்", )
ZERO_DURATION_SANDHA_OTRUGAL = ("ய்","ர்","ல்","ள்","ழ்","வ்","ண்","ன்",)#"ம்",)
ZERO_DURATION_SANDHA_OTRUGAL_MIDDLE = ("ய்","ர்","ல்","வ்","ழ்","ள்",)#"ம்",)
ZERO_DURATION_SANDHA_OTRUGAL_END = ("ய்","ர்","ண்","ன்",)#"ம்",)
MELLINAM = ("ங","ஙா","ஙி","ஙீ","ஙூ","ஙு","ஙெ","ஙே","ஙை","ஙொ","ஙோ","ஙௌ","ஞ","ஞா","ஞி","ஞீ","ஞூ","ஞு","ஞெ","ஞே","ஞை","ஞொ","ஞோ","ஞௌ","ண","ணா","ணி","ணீ","ணூ","ணு","ணெ","ணே","ணை","ணொ","ணோ","ணௌ","ந","நா","நி","நீ","நூ","நு","நெ","நே","நை","நொ","நோ","நௌ","ம","மா","மி","மீ","மூ","மு","மெ","மே","மை","மொ","மோ","மௌ","ன","னா","னி","னீ","னூ","னு","னெ","னே","னை","னொ","னோ","னௌ","ங்", "ஞ்", "ண்", "ந்", "ன்", "ம்",)
YIDAIYINAM = ("ய","யா","யி","யீ","யூ","யு","யெ","யே","யை","யொ","யோ","யௌ","ர","ரா","ரி","ரீ","ரூ","ரு","ரெ","ரே","ரை","ரொ","ரோ","ரௌ","ல","லா","லி","லீ","லூ","லு","லெ","லே","லை","லொ","லோ","லௌ","வ","வா","வி","வீ","வூ","வு","வெ","வே","வை","வொ","வோ","வௌ","ழ","ழா","ழி","ழீ","ழூ","ழு","ழெ","ழே","ழை","ழொ","ழோ","ழௌ","ள","ளா","ளி","ளீ","ளூ","ளு","ளெ","ளே","ளை","ளொ","ளோ","ளௌ","ய்", "ர்", "ல்", "ள்", "ழ்", "வ்",)
VALLINA_THODAI = ("க", "ச", "ட", "த", "ப", "ற", "கா", "சா", "டா", "தா", "பா", "றா", 
    "கி", "சி", "டி", "தி", "பி", "றி", "கீ", "சீ", "டீ", "தீ", "பீ", "றீ", "கு", "சு", "டு", "து", "பு", "று", "கூ", "சூ", "டூ", "தூ", "பூ", "றூ", 
    "கெ", "செ", "டெ", "தெ", "பெ", "றெ", "கே", "சே", "டே", "தே", "பே", "றே", "கை","சை", "டை", "தை", "பை", "றை", "கொ", "சொ", "டொ", "தொ", "பொ","றொ",  
    "கோ", "சோ", "டோ", "தோ", "போ", "றோ", "கௌ", "சௌ", "டௌ", "தௌ", "பௌ", "றௌ", "க்","ச்", "ட்", "த்", "ப்", "ற்", )
YAGARA_VARISAI = ("ய","யா","யி","யீ","யு","யூ","யெ","யே","யை","யொ","யோ","யௌ",)
VAGARA_VARISAI = {"வ","வா","வி","வீ","வு","வூ","வெ","வே","வை","வொ","வோ","வௌ",}
YIDAIYINA_THODAI = ("ய", "ர", "ல", "ள", "ழ", "வ", "யா", "ரா", "லா", "ளா", "ழா", "வா", "யி", "ரி", "லி", "ளி", "ழி", "வி", 
    "யீ", "ரீ", "லீ", "ளீ", "ழீ", "வீ", "யு", "ரு", "லு", "ளு", "ழு", "வு", "யூ", "ரூ", "லூ", "ளூ", "ழூ", "வூ", "யெ", "ரெ", "லெ", "ளெ", "ழெ", "வெ", 
    "யே", "ரே", "லே", "ளே", "ழே", "வே", "யை", "ரை", "லை", "ளை", "ழை", "வை", "யொ", "ரொ", "லொ", "ளொ", "ழொ", "வொ", 
    "யோ", "ரோ", "லோ", "ளோ", "ழோ", "வோ", "யௌ", "ரௌ", "லௌ", "ளௌ", "ழௌ", "வௌ", "ய்", "ர்", "ல்", "ள்", "ழ்", "வ்", )
MELLINA_THODAI = ("ங", "ஞ", "ண", "ந", "ன", "ம", "ஙா", "ஞா", "ணா", "நா", "னா", "மா", 
    "ஙி", "ஞி", "ணி", "நி", "னி", "மி", "ஙீ", "ஞீ", "ணீ", "நீ", "னீ", "மீ", "ஙூ", "ஞூ", "ணூ", "நூ", "னூ", "மூ", "ஙு", "ஞு", "ணு", "நு", "னு", "மு", 
    "ஙெ", "ஞெ", "ணெ", "நெ", "னெ", "மெ", "ஙே", "ஞே", "ணே", "நே", "னே", "மே", "ஙை", "ஞை", "ணை", "நை", "னை", "மை", 
    "ஙொ", "ஞொ", "ணொ", "நொ", "னொ", "மொ", "ஙோ", "ஞோ", "ணோ", "நோ", "னோ", "மோ", "ஙௌ", "ஞௌ", "ணௌ", "நௌ", "னௌ", "மௌ",  
    "ங்", "ஞ்", "ண்", "ந்", "ன்", "ம்", )
TAMIL_UNICODE_1_TA = ["க","ங","ச","ஞ","ட","ண","த","ந","ன","ப","ம","ய","ர","ற","ல","ள","ழ","வ",]
TAMIL_UNICODE_1_SAN = ["ஜ", "ஷ", "ஸ", "ஹ", "க்ஷ",]
TAMIL_UNICODE_1 = TAMIL_UNICODE_1_TA+TAMIL_UNICODE_1_SAN
TAMIL_UNICODE_2 = ["ா","ி","ீ","ூ","ு","ெ","ே","ை","ொ","ோ","ௌ","்",]
VADA_EZHUTHUKKAL= ("ஜ","ஜா","ஜி","ஜீ","ஜூ","ஜு","ஜெ","ஜே","ஜை","ஜொ","ஜோ","ஜௌ","ஜ்","ஷ","ஷா","ஷி","ஷீ","ஷூ","ஷு","ஷெ","ஷே","ஷை","ஷொ","ஷோ","ஷௌ","ஷ்","ஸ","ஸா","ஸி","ஸீ","ஸூ","ஸு","ஸெ","ஸே","ஸை","ஸொ","ஸோ","ஸௌ","ஸ்","ஹ","ஹா","ஹி","ஹீ","ஹூ","ஹு","ஹெ","ஹே","ஹை","ஹொ","ஹோ","ஹௌ","ஹ்","க்ஷ","க்ஷா","க்ஷி","க்ஷீ","க்ஷூ","க்ஷு","க்ஷெ","க்ஷே","க்ஷை","க்ஷொ","க்ஷோ","க்ஷௌ","க்ஷ்",)
MONAI_THODAI_1= ("அ", "ஆ", "ஐ", "ஔ","க","கா","கை","கௌ","ங","ஙா","ஙை","ஙௌ","ச",
    "சா","சை","சௌ","ஞ","ஞா","ஞை","ஞௌ","ட","டா","டை","டௌ","ண","ணா","ணை","ணௌ","த","தா","தை","தௌ",
    "ந","நா","நை","நௌ","ன","னா","னை","னௌ","ப","பா","பை","பௌ","ம","மா","மை","மௌ","ய","யா","யை","யௌ",
    "ர","ரா","ரை","ரௌ","ற","றா","றை","றௌ","ல","லா","லை","லௌ","ள","ளா","ளை","ளௌ","ழ","ழா","ழை","ழௌ",
    "வ","வா","வை","வௌ","ஜ","ஜா","ஜை","ஜௌ","ஷ","ஷா","ஷை","ஷௌ","ஸ","ஸா","ஸை","ஸௌ",
    "ஹ","ஹா","ஹை","ஹௌ","க்ஷ","க்ஷா","க்ஷை","க்ஷௌ",)
MONAI_THODAI_2= ("இ", "ஈ", "எ", "ஏ","கி","கீ","கெ","கே","ஙி","ஙீ","ஙெ","ஙே","சி","சீ","செ","சே","ஞி",
    "ஞீ","ஞெ","ஞே","டி","டீ","டெ","டே","ணி","ணீ","ணெ","ணே","தி","தீ","தெ","தே","நி","நீ","நெ","நே","னி","னீ","னெ","னே",
    "பி","பீ","பெ","பே","மி","மீ","மெ","மே","யி","யீ","யெ","யே","ரி","ரீ","ரெ","ரே","றி","றீ","றெ","றே","லி","லீ","லெ","லே",
    "ளி","ளீ","ளெ","ளே","ழி","ழீ","ழெ","ழே","வி","வீ","வெ","வே","ஜி","ஜீ","ஜெ","ஜே","ஷி","ஷீ","ஷெ","ஷே",
    "ஸி","ஸீ","ஸெ","ஸே","ஹி","ஹீ","ஹெ","ஹே","க்ஷி","க்ஷீ","க்ஷெ","க்ஷே",)
MONAI_THODAI_3= ("உ", "ஊ", "ஒ", "ஓ","கு","கூ","கொ","கோ","ஙு","ஙூ","ஙொ","ஙோ","சு","சூ","சொ","சோ","ஞு",
    "ஞூ","ஞொ","ஞோ","டு","டூ","டொ","டோ","ணு","ணூ","ணொ","ணோ","து","தூ","தொ","தோ","நு","நூ","நொ","நோ",
    "னு","னூ","னொ","னோ","பு","பூ","பொ","போ","மு","மூ","மொ","மோ","யு","யூ","யொ","யோ","ரு","ரூ","ரொ","ரோ","று","றூ","றொ","றோ",
    "லு","லூ","லொ","லோ","ளு","ளூ","ளொ","ளோ","ழு","ழூ","ழொ","ழோ","வு","வூ","வொ","வோ","ஜூ","ஜு","ஜொ","ஜோ",
    "ஷூ","ஷு","ஷொ","ஷோ","ஸூ","ஸு","ஸொ","ஸோ","ஹூ","ஹு","ஹொ","ஹோ","க்ஷூ","க்ஷு","க்ஷொ","க்ஷோ",)
MONAI_THODAI_4 = ("ச","சா","சை","சௌ","த","தா","தை","தௌ","ஞ","ஞா","ஞை","ஞௌ","ந","நா","நை","நௌ","ம","மா","மை","மௌ","வ","வா","வை","வௌ")
MONAI_THODAI_5 = ("சி","சீ","செ","சே","தி","தீ","தெ","தே","ஞி","ஞீ","ஞெ","ஞே","நி","நீ","நெ","நே",
    "மி","மீ","மெ","மே","வி","வீ","வெ","வே")
MONAI_THODAI_6= ("சு","சூ","சொ","சோ","து","தூ","தொ","தோ","ஞு","ஞூ","ஞொ","ஞோ","நு","நூ","நொ","நோ", "மு","மூ","மொ","மோ","வு","வூ","வொ","வோ")
YIYAIBU_ENDING_LETTERS =("ா","ி","ீ","ு","ூ","ெ","ே","ை","ொ","ோ","ௌ")
VENPA_ALLOWED_SEERS = ("தேமா", "புளிமா", "கூவிளம்", "கருவிளம்", "தேமாங்காய்", "புளிமாங்காய்", "கூவிளங்காய்", "கருவிளங்காய்", "காசு","மலர்","நாள்","பிறப்பு",)
VENPA_ALLOWED_THALAI = ('வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை')
VENPA_EETRU_SEERS = ("காசு","மலர்","நாள்","பிறப்பு",)
ASIRIYAPPA_ALLOWED_SEERS = ("தேமா", "புளிமா", "கூவிளம்", "கருவிளம்",)
ASIRIYAPPA_DISALLOWED_SEERS = ("கருவிளங்கனி","கூவிளங்கனி", )
ASIRIYAPPA_EETRUCHEER_LETTERS = ("ே","ோ","ீ","ை","ாய்",)
NILAIMANDILA_EETRUCHEER_LETTERS= ("னீ","னே","னை","னோ","ம்",)
KALIPPA_EETRUCHEER_LETTERS= ("ே",)
KALIPPA_ALLOWED_SEERS = ("தேமாங்காய்", "புளிமாங்காய்","கூவிளங்காய்", "கருவிளங்காய்",)
KALIPPA_DISALLOWED_SEERS = ("தேமா","புளிமா","கருவிளங்கனி","கூவிளங்கனி", )
VANJPA_ALLOWED_SEERS= ("தேமாங்காய்", "புளிமாங்காய்","கூவிளங்காய்", "கருவிளங்காய்","கருவிளங்கனி","கூவிளங்கனி",)
VANJPA_THANISOL_ALLOWED_SEERS = ("தேமா","புளிமா","கூவிளம்", "கருவிளம்", )
SANDHA_SEERGAL = ("மா", "விளம்", "காய்", "கனி", "பூ", "ணிழல்", 'நிழல்', 'நேர்','நிரை')
UYIR_MEY_LETTERS= ("க","கா","கி","கீ","கூ","கு","கெ","கே","கை","கொ","கோ","கௌ", "ங","ஙா","ஙி","ஙீ","ஙூ","ஙு","ஙெ","ஙே","ஙை","ஙொ","ஙோ","ஙௌ",
    "ச","சா","சி","சீ","சூ","சு","செ","சே","சை","சொ","சோ","சௌ", "ஞ","ஞா","ஞி","ஞீ","ஞூ","ஞு","ஞெ","ஞே","ஞை","ஞொ","ஞோ","ஞௌ",
    "ட","டா","டி","டீ","டூ","டு","டெ","டே","டை","டொ","டோ","டௌ", "ண","ணா","ணி","ணீ","ணூ","ணு","ணெ","ணே","ணை","ணொ","ணோ","ணௌ",
    "த","தா","தி","தீ","தூ","து","தெ","தே","தை","தொ","தோ","தௌ", "ந","நா","நி","நீ","நூ","நு","நெ","நே","நை","நொ","நோ","நௌ",
    "ன","னா","னி","னீ","னூ","னு","னெ","னே","னை","னொ","னோ","னௌ", "ப","பா","பி","பீ","பூ","பு","பெ","பே","பை","பொ","போ","பௌ",
    "ம","மா","மி","மீ","மூ","மு","மெ","மே","மை","மொ","மோ","மௌ", "ய","யா","யி","யீ","யூ","யு","யெ","யே","யை","யொ","யோ","யௌ",
    "ர","ரா","ரி","ரீ","ரூ","ரு","ரெ","ரே","ரை","ரொ","ரோ","ரௌ", "ற","றா","றி","றீ","றூ","று","றெ","றே","றை","றொ","றோ","றௌ",
    "ல","லா","லி","லீ","லூ","லு","லெ","லே","லை","லொ","லோ","லௌ", "ள","ளா","ளி","ளீ","ளூ","ளு","ளெ","ளே","ளை","ளொ","ளோ","ளௌ",
    "ழ","ழா","ழி","ழீ","ழூ","ழு","ழெ","ழே","ழை","ழொ","ழோ","ழௌ","வ","வா","வி","வீ","வூ","வு","வெ","வே","வை","வொ","வோ","வௌ",
    "ஜ","ஜா","ஜி","ஜீ","ஜூ","ஜு","ஜெ","ஜே","ஜை","ஜொ","ஜோ","ஜௌ","ஷ","ஷா","ஷி","ஷீ","ஷூ","ஷு","ஷெ","ஷே","ஷை","ஷொ","ஷோ","ஷௌ",
    "ஸ","ஸா","ஸி","ஸீ","ஸூ","ஸு","ஸெ","ஸே","ஸை","ஸொ","ஸோ","ஸௌ","ஹ","ஹா","ஹி","ஹீ","ஹூ","ஹு","ஹெ","ஹே","ஹை","ஹொ","ஹோ","ஹௌ",
    "க்ஷ","க்ஷா","க்ஷி","க்ஷீ","க்ஷூ","க்ஷு","க்ஷெ","க்ஷே","க்ஷை","க்ஷொ","க்ஷோ","க்ஷௌ",)

SANDHAPAA_DICT = [
{'K': 'ன',  'N': 'னா', "O" : "த்"},
{'KK': 'தன',  'NK': 'தான',  'KN': 'தனா', 'NN': 'தானா', 'KO':'னா', 'NO':'னா'
},
{'NOK': 'தான்ன',  'KOK': 'தன்ன',  'KKO': 'தனன்',  'NOK': 'தான',   'KON': 'தன்னா', 'NKO': 'தான',  'KNO': 'தனா',  'NON': 'தானா', 
},
{ 'KOKO': 'தன்ன', 'NOOK': 'தான்ன',  'NOKO': 'தான',  'KONO': 'தன்னா',  'NONO': 'தானா',  
}, 
{ 'KOOKO': 'தன்ன', 'NOOKO': 'தான்ன',  'NOONO': 'தான்னா',  'KOONO': 'தன்னா', 
},
]
SANDHA_PAA_DURATION = [{"N" : 2.0, "K" : 1.0, ' ' : 0.0, '' : 0.0},
                       {"NO" : 2.0, "KO" : 2.0},
                       {"NOO" : 2.0, "KOO" : 2.0},
                      ]
ASAI_DICT = [{'N':'நேர்', 'K':'நேர்'}, 
             {'NO':'நேர்', 'KO':'நேர்', 'KK':'நிரை', 'KN':'நிரை'}, 
             {'NOO':'நேர்', 'KOO':'நேர்', 'KNO':'நிரை', 'KKO':'நிரை'},
             {'KNOO':'நிரை', 'KKOO':'நிரை'}]
VIKARPAM_LIST = ['ஒரு விகற்ப', "இரு விகற்ப", "பல விகற்ப"]
ASAIGAL = ['நேர்','நிரை']
SEERGAL = ['தேமா',"புளிமா","கூவிளம்","கருவிளம்", "தேமாங்காய்", "தேமாங்கனி", "புளிமாங்காய்", "புளிமாங்கனி", "கருவிளங்காய்", "கருவிளங்கனி", \
           "கூவிளங்காய்", "கூவிளங்கனி", "தேமாந்தண்பூ", "தேமாந்தண்ணிழல்", "தேமாநறும்பூ", "தேமாநறுநிழல்", "புளிமாந்தண்பூ", "புளிமாந்தண்ணிழல்", "புளிமாநறும்பூ", \
                "புளிமாநறுநிழல்", "கூவிளந்தண்பூ", "கூவிளந்தண்ணிழல்", "கூவிளநறும்பூ", "கூவிளநறுநிழல்", "கருவிளந்தண்பூ", "கருவிளந்தண்ணிழல்", "கருவிளநறும்பூ", "கருவிளநறுநிழல்"
          ]
SEER_TYPES = [ {"நேர்":"நேர்", "நிரை":"நிரை"}, \
               {"நேர் நேர்":"தேமா", "நிரை நேர்":"புளிமா", "நேர் நிரை":"கூவிளம்", "நிரை நிரை":"கருவிளம்"}, \
               {"நேர் நேர் நேர்":"தேமாங்காய்", "நேர் நேர் நிரை":"தேமாங்கனி", "நிரை நேர் நேர்":"புளிமாங்காய்", "நிரை நேர் நிரை":"புளிமாங்கனி", \
                "நிரை நிரை நேர்":"கருவிளங்காய்", "நிரை நிரை நிரை":"கருவிளங்கனி", "நேர் நிரை நேர்":"கூவிளங்காய்", "நேர் நிரை நிரை":"கூவிளங்கனி"
               }, \
               {"நேர் நேர் நேர் நேர்":"தேமாந்தண்பூ", "நேர் நேர் நேர் நிரை":"தேமாந்தண்ணிழல்", "நேர் நேர் நிரை நேர்":"தேமாநறும்பூ", "நேர் நேர் நிரை நிரை":"தேமாநறுநிழல்", \
                "நிரை நேர் நேர் நேர்":"புளிமாந்தண்பூ", "நிரை நேர் நேர் நிரை":"புளிமாந்தண்ணிழல்", "நிரை நேர் நிரை நேர்":"புளிமாநறும்பூ", \
                "நிரை நேர் நிரை நிரை":"புளிமாநறுநிழல்", "நேர் நிரை நேர் நேர்":"கூவிளந்தண்பூ", "நேர் நிரை நேர் நிரை":"கூவிளந்தண்ணிழல்", \
                "நேர் நிரை நிரை நேர்":"கூவிளநறும்பூ", "நேர் நிரை நிரை நிரை":"கூவிளநறுநிழல்", "நிரை நிரை நேர் நேர்":"கருவிளந்தண்பூ", \
                "நிரை நிரை நேர் நிரை":"கருவிளந்தண்ணிழல்", "நிரை நிரை நிரை நேர்":"கருவிளநறும்பூ", "நிரை நிரை நிரை நிரை":"கருவிளநறுநிழல்"
               }
            ]
THALAI_TYPES = {"மா நேர்": "நேரொன்றிய ஆசிரியத்தளை", 
        "விளம் நிரை" : "நிரையொன்றிய ஆசிரியத்தளை",
        "விளம் நேர்" : "இயற்சீர் வெண்டளை",
        "மா நிரை" : "இயற்சீர் வெண்டளை",
        "காய் நேர்" : "வெண்சீர் வெண்டளை",
        "காய் நிரை" : "கலித்தளை",
        "கனி நிரை" : "ஒன்றிய வஞ்சித்தளை",
        "கனி நேர்" : "ஒன்றா வஞ்சித்தளை",
        "பூ நேர்" : "வெண்சீர் வெண்டளை",
        "பூ நிரை" : "கலித்தளை",
        "நிழல் நேர்" : "ஒன்றா வஞ்சித்தளை",
        "நிழல் நிரை" : "ஒன்றிய வஞ்சித்தளை",
        "ணிழல் நேர்" : "ஒன்றா வஞ்சித்தளை",
        "ணிழல் நிரை" : "ஒன்றிய வஞ்சித்தளை",
        }
THALAI_TYPES_SHORT = {"மா நேர்": "ஆசிரியத்தளை", 
        "விளம் நிரை" : "ஆசிரியத்தளை",
        "விளம் நேர்" : "வெண்டளை",
        "மா நிரை" : "வெண்டளை",
        "காய் நேர்" : "வெண்டளை",
        "காய் நிரை" : "கலித்தளை",
        "கனி நிரை" : "வஞ்சித்தளை",
        "கனி நேர்" : "வஞ்சித்தளை",
        "பூ நேர்" : "வெண்டளை",
        "பூ நிரை" : "கலித்தளை",
        "நிழல் நேர்" : "வஞ்சித்தளை",
        "நிழல் நிரை" : "வஞ்சித்தளை",
        "ணிழல் நேர்" : "வஞ்சித்தளை",
        "ணிழல் நிரை" : "வஞ்சித்தளை",
        }
OSAI_TYPES = {"நேரொன்றிய ஆசிரியத்தளை" : "ஏந்திசை அகவலோசை",
        "நிரையொன்றிய ஆசிரியத்தளை" : "தூங்கிசை அகவலோசை",
        "இயற்சீர் வெண்டளை" : "தூங்கிசைச் செப்பலோசை",
        "வெண்சீர் வெண்டளை" : "ஏந்திசைச் செப்பலோசை",
        "கலித்தளை" : "ஏந்திசைத் துள்ளலோசை",
        "ஒன்றிய வஞ்சித்தளை" : "ஏந்திசைத் தூங்கலோசை",
        "ஒன்றா வஞ்சித்தளை" : "அகவல் தூங்கலோசை",
        }
OSAI_TYPES_SHORT = {"ஆசிரியத்தளை" : "அகவலோசை",
        "வெண்டளை" : "செப்பலோசை",
        "கலித்தளை" : "துள்ளலோசை",
        "வஞ்சித்தளை" : "தூங்கலோசை",
        }
LINE_TYPES = ('','தனிச்சொல்', 'குறளடி', 'சிந்தடி', 'அளவடி', 'நெடிலடி', 'கழி நெடிலடி', 'கழி நெடிலடி', 'கழி நெடிலடி', 'இடையாகு கழி நெடிலடி', 'இடையாகு கழி நெடிலடி', 'கடையாகு கழி நெடிலடி'  )
THODAI_TYPES = ("மோனை", "எதுகை", "இயைபு")
SEER_THODAI_TYPES = {"":"", "1" : "","1-2" : "இணை", "1-3" : "பொழிப்பு", "1-4" : "ஒருஊ", "1-2-3" : "கூழை", "1-3-4" : "மேற்கதுவாய்", "1-2-4" : "கீழ்க்கதுவாய்", "1-2-3-4" : "முற்று"}
class POEM_TYPES(IntEnum):
    VENPA = 1
    ASIRIYAPA = 2
    KALIPA = 3
    VANJIPA = 4
    VENPAVINAM = 5
    ASIRIYAPAVINAM = 6
    KALIPAVINAM = 7
    VANJIPAVINAM = 8
POEM_CHECK_FUNCTIONS = { 
    POEM_TYPES.VENPA : 'check_for_venpaa', 
    POEM_TYPES.ASIRIYAPA : 'check_for_asiriyapaa',  
    POEM_TYPES.KALIPA : 'check_for_kalipaa', 
    POEM_TYPES.VANJIPA : 'check_for_vanjipaa', 
    POEM_TYPES.VENPAVINAM : 'check_for_venpaavinam', 
    POEM_TYPES.ASIRIYAPAVINAM : 'check_for_asiriyapaavinam', 
    POEM_TYPES.KALIPAVINAM : 'check_for_kalipaavinam', 
    POEM_TYPES.VANJIPAVINAM : 'check_for_vanjipaavinam' 
}
UYIRALABEDAI = ["ஆஅ", "ஆஅஅ", "ஈஇ", "ஊஉ", "ஏஎ", "ஐஇ", "ஓஒ", "ஔஉ"]
OTRALABEDAI = ["ங்ங்","ஞ்ஞ்","ண்ண்","ந்ந்","ன்ன்","ம்ம்","ய்ய்","ல்ல்","ள்ள்","ஃஃ",]

" Check if string has key"
string_has_key = lambda a, d: any(k in a for k in d)

" Flatten a list of lists "
flatten_list = lambda list: [item for sublist in list for item in sublist]
""" Generate VARUKKA EDHUGAI """
VARUKKA_EDHUGAI = list(UYIR_MEY_LETTERS)
VETRUMAI_URUBUGAL = ['','','ஐ','ஆல்','கு','இன்','அது','கண்'] # 0,1,..7
n = 12
i = n
while i < len(VARUKKA_EDHUGAI):
    for j in range(len(MEYGAL)):
        x = MEYGAL[j]
        #print('inserting ',x,' at ', i)
        VARUKKA_EDHUGAI.insert(i,x)
        i += (n+1)

def insert_string_at_index(string, insert_string, index):
    if index == -1:
        index = len(string)-1
        if ' ' in string:
            index = len(string)-2
    if index < len(string):
        result = ''.join(string[:index])+insert_string[0]+string[index]+insert_string[1]+''.join(string[index+1:])
    else:
        result = string
    return result

def get_index(list, element):
    index = -1
    try:
        index = list.index(element)
    except:
        index = -1
    return index
    
def get_keys_containing_string(dict, string):
    return [value for key, value in dict.items() if key.lower() in string.lower()]
            
def get_last_morpheme(word):
    if word.strip()=='':
        return '' 
    last_char = word[-1]
    if last_char == "்":
        last_char = MEYGAL[TAMIL_UNICODE_1.index(word[-2])]
    if (grammar.Ezhuthu(last_char).is_uyir_ezhuthu() or grammar.Ezhuthu(last_char).is_mey_ezhuthu()):
        return last_char
    index = get_index(TAMIL_UNICODE_2,last_char)
    if (index == -1):
        return "அ"
    index = get_index(YIYAIBU_ENDING_LETTERS,last_char)
    if index != -1:
        return UYIRGAL[index+1]
    return last_char

def get_first_morpheme(word):
    if word.strip()=='':
        return '' 
    first_char = word[0]
    if (grammar.Ezhuthu(first_char).is_uyir_ezhuthu() or grammar.Ezhuthu(first_char).is_mey_ezhuthu()):
        return first_char
    index = get_index(TAMIL_UNICODE_1,first_char)
    if (index != -1 ):
        return MEYGAL[index]
    index = get_index(YIYAIBU_ENDING_LETTERS,first_char)
    if index != -1:
        return UYIRGAL[index+1]
    return first_char

def list_has_element(list,element):
    try:
        return element in list
    except:
        return False

def string_has_unicode_character(word, character):
    result = character in get_unicode_characters(word)
    return result

def get_unicode_characters(word):
    import regex
    if (' ' in word):
        return regex.findall('\p{L}\p{M}*|\p{Z}*',word)
    else:
        return regex.findall('\p{L}\p{M}*',word)
    

def get_matching_sublist(char,list,index):
    " To get a subarray of size index at matching element "
    try:
        beg = int(list.index(char)/index)*index
        end = beg + index
        return list[beg:end]
    except ValueError:
        return []
        
def __get_thodai_characters_TODO(thodai_char1, thodai_index=0):
    thodai_characters = []
    temp_list = []
    if (thodai_index == 0 or thodai_index == 1):
        """ Nedil monai/edhugai """
        temp_list = get_matching_sublist(thodai_char1,NEDILGAL,5)
        if temp_list:
            thodai_characters.append(temp_list)
        """ yina monai / edhigai """
        temp_list = get_matching_sublist(thodai_char1,flatten_list([VALLINAM, YIDAIYINAM, MELLINAM]),12)
        if temp_list:
            thodai_characters.append(temp_list)
        """ Varukka monai / edhugai """
        temp_list = get_matching_sublist(thodai_char1,VARUKKA_EDHUGAI,13)
        if temp_list:
            #print(thodai_char1,'found in monia4_5_6')
            thodai_characters.append(temp_list)
    elif (thodai_index == 1):
        temp_list = get_matching_sublist(thodai_char1,VARUKKA_EDHUGAI,13)
        if temp_list:
            #print(thodai_char1,'found in varukka edhugai')
            thodai_characters.append(temp_list)
        temp_list = get_matching_sublist(thodai_char1,flatten_list([VALLINA_THODAI, MELLINA_THODAI, YIDAIYINA_THODAI]),13)
        if temp_list:
            #print(thodai_char1,'found in yina edhugai')
            thodai_characters.append(temp_list)
    thodai_characters = flatten_list(thodai_characters)
    #print(thodai_char1,' in? ',thodai_characters, '???')
    return thodai_characters

def get_thodai_characters(thodai_char1, thodai_index=0):
    thodai_characters = []
    temp_list = []
    if (thodai_index == 0):
        temp_list = get_matching_sublist(thodai_char1,flatten_list([MONAI_THODAI_1, MONAI_THODAI_2, MONAI_THODAI_3]),4)
        if temp_list:
            #print(thodai_char1,'found in monia1_2_3')
            thodai_characters.append(temp_list)
        temp_list = get_matching_sublist(thodai_char1,flatten_list([MONAI_THODAI_4, MONAI_THODAI_5, MONAI_THODAI_6]),8)
        if temp_list:
            #print(thodai_char1,'found in monia4_5_6')
            thodai_characters.append(temp_list)
        temp_list = get_matching_sublist(thodai_char1,VARUKKA_EDHUGAI,13)
        if temp_list:
            #print(thodai_char1,'found in monia4_5_6')
            thodai_characters.append(temp_list)
    elif (thodai_index == 1):
        temp_list = get_matching_sublist(thodai_char1,VARUKKA_EDHUGAI,13)
        if temp_list:
            #print(thodai_char1,'found in varukka edhugai')
            thodai_characters.append(temp_list)
        temp_list = get_matching_sublist(thodai_char1,flatten_list([VALLINA_THODAI, MELLINA_THODAI, YIDAIYINA_THODAI]),13)
        if temp_list:
            #print(thodai_char1,'found in yina edhugai')
            thodai_characters.append(temp_list)
    thodai_characters = flatten_list(thodai_characters)
    #print(thodai_char1,' in? ',thodai_characters, '???')
    return thodai_characters

def frequency_of_occurrence(words, specific_words=None):
    """
    Returns a list of (instance, count) sorted in total order and then from most to least common
    Along with the count/frequency of each of those words as a tuple
    If specific_words list is present then SUM of frequencies of specific_words is returned 
    """
    freq = sorted(sorted(Counter(words).items(), key=itemgetter(0)), key=itemgetter(1), reverse=True)
    if not specific_words or specific_words==None:
        return freq
    else:
        frequencies = 0
        for (inst, count) in freq:
            if inst in specific_words:
                frequencies += count        
        return float(frequencies)
        
def has_required_percentage_of_occurrence(words, specific_words=None,required_percent_of_occurrence=0.99):
    actual_percent_of_occurrence = percentage_of_occurrence(words, specific_words=specific_words)
    percent_check = actual_percent_of_occurrence >= required_percent_of_occurrence
    #print(actual_percent_of_occurrence,required_percent_of_occurrence,percent_check)
    return [percent_check, actual_percent_of_occurrence]

def percentage_of_occurrence(words, specific_words=None):
    """
    Returns a list of (instance, count) sorted in total order and then from most to least common
    Along with the percent of each of those words as a tuple
    If specific_words list is present then SUM of percentages of specific_words is returned 
    """
    frequencies = frequency_of_occurrence(words) # Dont add specific_word as argument here float error happens
    #print('FREQ',frequencies)
    perc = [(instance, count / len(words)) for instance, count in frequencies]
    if not specific_words or specific_words==None:
        return perc
    else:
        percentages = 0
        for (inst, per) in perc:
            if inst in specific_words:
                percentages += per        
        return percentages

def convert_1d_list_to_2d(list_1d_arr, len_arr):
    it = iter(list_1d_arr)
    return [list(islice(it, i)) for i in len_arr]
    
def get_character_type_counts(sentence, results_in_descending_order=True, show_by_character_type_keys=True, include_zero_counts=False):
    stats = {}
    sentence = sentence.replace('\n',' ') #remove line ends
    sentence = sentence.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
    words = sentence.split()
    for word in words:
        if (word.strip() == ''):
            continue
        sol = grammar.Sol(word)
        for tc in sol.tamil_char_objects:
            for char_type in _CHARACTER_TYPES.keys():
                #fun = 'is_'+char_type
                #val = getattr(tc,'is_'+char_type)()
                if char_type in stats:
                    stats[char_type] += getattr(tc,'is_'+char_type)()
                else:
                    stats[char_type] = getattr(tc,'is_'+char_type)()
                #print(tc.text(),char_type,fun,val,stats[char_type])
    results = []
    if show_by_character_type_keys:
        for char_type in _CHARACTER_TYPES.keys():
            if include_zero_counts or stats[char_type] !=0:
                results.append([char_type,stats[char_type]])
    else:
        for char_type in _CHARACTER_TYPES.keys():
            if include_zero_counts or stats[char_type] !=0:
                results.append([_CHARACTER_TYPES.get(char_type),stats[char_type]])
        
    results = sorted(results,key=itemgetter(1),reverse=results_in_descending_order)
    return results       
def get_all_tamil_characters(include_space=True, include_vadamozhi=False):
    all_tamil_chars = []
    if include_space:
        all_tamil_chars = [' ']
    T_U_1 = TAMIL_UNICODE_1_TA
    if include_vadamozhi:
        T_U_1 += TAMIL_UNICODE_1_SAN 
    all_tamil_chars += UYIRGAL+['ஃ']+T_U_1+ [t1+t2 for t1 in T_U_1 for t2 in TAMIL_UNICODE_2]
    return all_tamil_chars
def _get_vannappa_dictionary():
    import itertools
    res = []
    sandham = 'தான'
    a = [['UN','VN','YN','MN'],['UK','VK','MK','YK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['YO'],['UK','VK','MK','YK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['MO'],['UK','VK','MK','YK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தானா'
    a = [['UN','VN','YN','MN'],['UN','VN','MN','YN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['YO'],['UN','VN','MN','YN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['MO'],['UN','VN','MN','YN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தன'
    a = [['UK','VK','YK','MK'],['UK','VK','MK','YK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    
    sandham = 'தனா'
    a = [['UK','VK','YK','MK'],['UN','VN','MN','YN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    
    sandham = 'தத்த'
    a = [['UK','VK','YK','MK'],['VO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UK','VK','YK','MK'],['YOVO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தந்த'
    a = [['UK','VK','YK','MK'],['MO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UK','VK','YK','MK'],['YOMO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    
    sandham = 'தய்ய'
    a = [['UK','VK','YK','MK'],['YO'],['VK','YK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    
    sandham = 'தன்ன'
    a = [['UK','VK','YK','MK'],['MO'],['MK','YK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    
    sandham = 'தத்தா'
    a = [['UK','VK','YK','MK'],['VO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UK','VK','YK','MK'],['YOVO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தந்தா'
    a = [['UK','VK','YK','MK'],['MO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UK','VK','YK','MK'],['YOMO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தய்யா'
    a = [['UK','VK','YK','MK'],['YO'],['VN','YN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    
    sandham = 'தன்னா'
    a = [['UK','VK','YK','MK'],['MO'],['MN','YN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    
    sandham = 'தாத்த'
    a = [['UN','VN','YN','MN'],['VO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['YOVO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தாத்தா'
    a = [['UN','VN','YN','MN'],['VO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['YOVO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தாந்த'
    a = [['UN','VN','YN','MN'],['MO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['YOMO'],['UK','VK','YK','MK']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )

    sandham = 'தாந்தா'
    a = [['UN','VN','YN','MN'],['MO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a = [['UN','VN','YN','MN'],['YOMO'],['UN','VN','YN','MN']]
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    a.append(['YO','MO'])
    res.append( {''.join(tups):sandham for tups in list(itertools.product(*a))} )
    res = {k:v for r in res for k,v in r.items()}
    res1 = sorted(list(res.items()), key = lambda key : len(key[0]))
    res = {ele[0] : ele[1]  for ele in res1}
    #print(VANNAPAA_DICT2)
    return res
VANNAPAA_DICT3 = [
{'UK':'ன','VK':'ன','YK':'ன','MK':'ன','VN':'னா','YN':'னா','MN':'னா',},#'VO':'த்','YO':'த்','MO':'ந்',},
{'YKYO':'ன','MKYO':'ன',},
{'UNUK': 'தான', 'UNVK': 'தான', 'UNMK': 'தான', 'UNYK': 'தான', 'VNUK': 'தான', 'VNVK': 'தான', 'VNMK': 'தான', 'VNYK': 'தான', 'YNUK': 'தான', 'YNVK': 'தான', 'YNMK': 'தான', 'YNYK': 'தான', 'MNUK': 'தான', 'MNVK': 'தான', 'MNMK': 'தான', 'MNYK': 'தான', 'UNUN': 'தானா', 'UNVN': 'தானா', 'UNMN': 'தானா', 'UNYN': 'தானா', 'VNUN': 'தானா', 'VNVN': 'தானா', 'VNMN': 'தானா', 'VNYN': 'தானா', 'YNUN': 'தானா', 'YNVN': 'தானா', 'YNMN': 'தானா', 'YNYN': 'தானா', 'MNUN': 'தானா', 'MNVN': 'தானா', 'MNMN': 'தானா', 'MNYN': 'தானா', 'UKUK': 'தன', 'UKVK': 'தன', 'UKMK': 'தன', 'UKYK': 'தன', 'VKUK': 'தன', 'VKVK': 'தன', 'VKMK': 'தன', 'VKYK': 'தன', 'YKUK': 'தன', 'YKVK': 'தன', 'YKMK': 'தன', 'YKYK': 'தன', 'MKUK': 'தன', 'MKVK': 'தன', 'MKMK': 'தன', 'MKYK': 'தன', 'UKUN': 'தனா', 'UKVN': 'தனா', 'UKMN': 'தனா', 'UKYN': 'தனா', 'VKUN': 'தனா', 'VKVN': 'தனா', 'VKMN': 'தனா', 'VKYN': 'தனா', 'YKUN': 'தனா', 'YKVN': 'தனா', 'YKMN': 'தனா', 'YKYN': 'தனா', 'MKUN': 'தனா', 'MKVN': 'தனா', 'MKMN': 'தனா', 'MKYN': 'தனா', },
{'UNUKYO': 'தான', 'UNUKMO': 'தான', 'UNVKYO': 'தான', 'UNVKMO': 'தான', 'UNMKYO': 'தான', 'UNMKMO': 'தான', 'UNYKYO': 'தான', 'UNYKMO': 'தான', 'VNUKYO': 'தான', 'VNUKMO': 'தான', 'VNVKYO': 'தான', 'VNVKMO': 'தான', 'VNMKYO': 'தான', 'VNMKMO': 'தான', 'VNYKYO': 'தான', 'VNYKMO': 'தான', 'YNUKYO': 'தான', 'YNUKMO': 'தான', 'YNVKYO': 'தான', 'YNVKMO': 'தான', 'YNMKYO': 'தான', 'YNMKMO': 'தான', 'YNYKYO': 'தான', 'YNYKMO': 'தான', 'MNUKYO': 'தான', 'MNUKMO': 'தான', 'MNVKYO': 'தான', 'MNVKMO': 'தான', 'MNMKYO': 'தான', 'MNMKMO': 'தான', 'MNYKYO': 'தான', 'MNYKMO': 'தான', 'UNYOUK': 'தான', 'UNYOVK': 'தான', 'UNYOMK': 'தான', 'UNYOYK': 'தான', 'VNYOUK': 'தான', 'VNYOVK': 'தான', 'VNYOMK': 'தான', 'VNYOYK': 'தான', 'YNYOUK': 'தான', 'YNYOVK': 'தான', 'YNYOMK': 'தான', 'YNYOYK': 'தான', 'MNYOUK': 'தான', 'MNYOVK': 'தான', 'MNYOMK': 'தான', 'MNYOYK': 'தான', 'UNMOUK': 'தாந்த', 'UNMOVK': 'தாந்த', 'UNMOMK': 'தாந்த', 'UNMOYK': 'தாந்த', 'VNMOUK': 'தாந்த', 'VNMOVK': 'தாந்த', 'VNMOMK': 'தாந்த', 'VNMOYK': 'தாந்த', 'YNMOUK': 'தாந்த', 'YNMOVK': 'தாந்த', 'YNMOMK': 'தாந்த', 'YNMOYK': 'தாந்த', 'MNMOUK': 'தாந்த', 'MNMOVK': 'தாந்த', 'MNMOMK': 'தாந்த', 'MNMOYK': 'தாந்த', 'UNUNYO': 'தானா', 'UNUNMO': 'தானா', 'UNVNYO': 'தானா', 'UNVNMO': 'தானா', 'UNMNYO': 'தானா', 'UNMNMO': 'தானா', 'UNYNYO': 'தானா', 'UNYNMO': 'தானா', 'VNUNYO': 'தானா', 'VNUNMO': 'தானா', 'VNVNYO': 'தானா', 'VNVNMO': 'தானா', 'VNMNYO': 'தானா', 'VNMNMO': 'தானா', 'VNYNYO': 'தானா', 'VNYNMO': 'தானா', 'YNUNYO': 'தானா', 'YNUNMO': 'தானா', 'YNVNYO': 'தானா', 'YNVNMO': 'தானா', 'YNMNYO': 'தானா', 'YNMNMO': 'தானா', 'YNYNYO': 'தானா', 'YNYNMO': 'தானா', 'MNUNYO': 'தானா', 'MNUNMO': 'தானா', 'MNVNYO': 'தானா', 'MNVNMO': 'தானா', 'MNMNYO': 'தானா', 'MNMNMO': 'தானா', 'MNYNYO': 'தானா', 'MNYNMO': 'தானா', 'UNYOUN': 'தானா', 'UNYOVN': 'தானா', 'UNYOMN': 'தானா', 'UNYOYN': 'தானா', 'VNYOUN': 'தானா', 'VNYOVN': 'தானா', 'VNYOMN': 'தானா', 'VNYOYN': 'தானா', 'YNYOUN': 'தானா', 'YNYOVN': 'தானா', 'YNYOMN': 'தானா', 'YNYOYN': 'தானா', 'MNYOUN': 'தானா', 'MNYOVN': 'தானா', 'MNYOMN': 'தானா', 'MNYOYN': 'தானா', 'UNMOUN': 'தாந்தா', 'UNMOVN': 'தாந்தா', 'UNMOMN': 'தாந்தா', 'UNMOYN': 'தாந்தா', 'VNMOUN': 'தாந்தா', 'VNMOVN': 'தாந்தா', 'VNMOMN': 'தாந்தா', 'VNMOYN': 'தாந்தா', 'YNMOUN': 'தாந்தா', 'YNMOVN': 'தாந்தா', 'YNMOMN': 'தாந்தா', 'YNMOYN': 'தாந்தா', 'MNMOUN': 'தாந்தா', 'MNMOVN': 'தாந்தா', 'MNMOMN': 'தாந்தா', 'MNMOYN': 'தாந்தா', 'UKUKYO': 'தன', 'UKUKMO': 'தன', 'UKVKYO': 'தன', 'UKVKMO': 'தன', 'UKMKYO': 'தன', 'UKMKMO': 'தன', 'UKYKYO': 'தன', 'UKYKMO': 'தன', 'VKUKYO': 'தன', 'VKUKMO': 'தன', 'VKVKYO': 'தன', 'VKVKMO': 'தன', 'VKMKYO': 'தன', 'VKMKMO': 'தன', 'VKYKYO': 'தன', 'VKYKMO': 'தன', 'YKUKYO': 'தன', 'YKUKMO': 'தன', 'YKVKYO': 'தன', 'YKVKMO': 'தன', 'YKMKYO': 'தன', 'YKMKMO': 'தன', 'YKYKYO': 'தன', 'YKYKMO': 'தன', 'MKUKYO': 'தன', 'MKUKMO': 'தன', 'MKVKYO': 'தன', 'MKVKMO': 'தன', 'MKMKYO': 'தன', 'MKMKMO': 'தன', 'MKYKYO': 'தன', 'MKYKMO': 'தன', 'UKUNYO': 'தனா', 'UKUNMO': 'தனா', 'UKVNYO': 'தனா', 'UKVNMO': 'தனா', 'UKMNYO': 'தனா', 'UKMNMO': 'தனா', 'UKYNYO': 'தனா', 'UKYNMO': 'தனா', 'VKUNYO': 'தனா', 'VKUNMO': 'தனா', 'VKVNYO': 'தனா', 'VKVNMO': 'தனா', 'VKMNYO': 'தனா', 'VKMNMO': 'தனா', 'VKYNYO': 'தனா', 'VKYNMO': 'தனா', 'YKUNYO': 'தனா', 'YKUNMO': 'தனா', 'YKVNYO': 'தனா', 'YKVNMO': 'தனா', 'YKMNYO': 'தனா', 'YKMNMO': 'தனா', 'YKYNYO': 'தனா', 'YKYNMO': 'தனா', 'MKUNYO': 'தனா', 'MKUNMO': 'தனா', 'MKVNYO': 'தனா', 'MKVNMO': 'தனா', 'MKMNYO': 'தனா', 'MKMNMO': 'தனா', 'MKYNYO': 'தனா', 'MKYNMO': 'தனா', 'UKVOUK': 'தத்த', 'UKVOVK': 'தத்த', 'UKVOYK': 'தத்த', 'UKVOMK': 'தத்த', 'VKVOUK': 'தத்த', 'VKVOVK': 'தத்த', 'VKVOYK': 'தத்த', 'VKVOMK': 'தத்த', 'YKVOUK': 'தத்த', 'YKVOVK': 'தத்த', 'YKVOYK': 'தத்த', 'YKVOMK': 'தத்த', 'MKVOUK': 'தத்த', 'MKVOVK': 'தத்த', 'MKVOYK': 'தத்த', 'MKVOMK': 'தத்த', 'UKMOUK': 'தந்த', 'UKMOVK': 'தந்த', 'UKMOYK': 'தன்ன', 'UKMOMK': 'தன்ன', 'VKMOUK': 'தந்த', 'VKMOVK': 'தந்த', 'VKMOYK': 'தன்ன', 'VKMOMK': 'தன்ன', 'YKMOUK': 'தந்த', 'YKMOVK': 'தந்த', 'YKMOYK': 'தன்ன', 'YKMOMK': 'தன்ன', 'MKMOUK': 'தந்த', 'MKMOVK': 'தந்த', 'MKMOYK': 'தன்ன', 'MKMOMK': 'தன்ன', 'UKYOVK': 'தய்ய', 'UKYOYK': 'தய்ய', 'VKYOVK': 'தய்ய', 'VKYOYK': 'தய்ய', 'YKYOVK': 'தய்ய', 'YKYOYK': 'தய்ய', 'MKYOVK': 'தய்ய', 'MKYOYK': 'தய்ய', 'UKVOUN': 'தத்தா', 'UKVOVN': 'தத்தா', 'UKVOYN': 'தத்தா', 'UKVOMN': 'தத்தா', 'VKVOUN': 'தத்தா', 'VKVOVN': 'தத்தா', 'VKVOYN': 'தத்தா', 'VKVOMN': 'தத்தா', 'YKVOUN': 'தத்தா', 'YKVOVN': 'தத்தா', 'YKVOYN': 'தத்தா', 'YKVOMN': 'தத்தா', 'MKVOUN': 'தத்தா', 'MKVOVN': 'தத்தா', 'MKVOYN': 'தத்தா', 'MKVOMN': 'தத்தா', 'UKMOUN': 'தந்தா', 'UKMOVN': 'தந்தா', 'UKMOYN': 'தன்னா', 'UKMOMN': 'தன்னா', 'VKMOUN': 'தந்தா', 'VKMOVN': 'தந்தா', 'VKMOYN': 'தன்னா', 'VKMOMN': 'தன்னா', 'YKMOUN': 'தந்தா', 'YKMOVN': 'தந்தா', 'YKMOYN': 'தன்னா', 'YKMOMN': 'தன்னா', 'MKMOUN': 'தந்தா', 'MKMOVN': 'தந்தா', 'MKMOYN': 'தன்னா', 'MKMOMN': 'தன்னா', 'UKYOVN': 'தய்யா', 'UKYOYN': 'தய்யா', 'VKYOVN': 'தய்யா', 'VKYOYN': 'தய்யா', 'YKYOVN': 'தய்யா', 'YKYOYN': 'தய்யா', 'MKYOVN': 'தய்யா', 'MKYOYN': 'தய்யா', 'UNVOUK': 'தாத்த', 'UNVOVK': 'தாத்த', 'UNVOYK': 'தாத்த', 'UNVOMK': 'தாத்த', 'VNVOUK': 'தாத்த', 'VNVOVK': 'தாத்த', 'VNVOYK': 'தாத்த', 'VNVOMK': 'தாத்த', 'YNVOUK': 'தாத்த', 'YNVOVK': 'தாத்த', 'YNVOYK': 'தாத்த', 'YNVOMK': 'தாத்த', 'MNVOUK': 'தாத்த', 'MNVOVK': 'தாத்த', 'MNVOYK': 'தாத்த', 'MNVOMK': 'தாத்த', 'UNVOUN': 'தாத்தா', 'UNVOVN': 'தாத்தா', 'UNVOYN': 'தாத்தா', 'UNVOMN': 'தாத்தா', 'VNVOUN': 'தாத்தா', 'VNVOVN': 'தாத்தா', 'VNVOYN': 'தாத்தா', 'VNVOMN': 'தாத்தா', 'YNVOUN': 'தாத்தா', 'YNVOVN': 'தாத்தா', 'YNVOYN': 'தாத்தா', 'YNVOMN': 'தாத்தா', 'MNVOUN': 'தாத்தா', 'MNVOVN': 'தாத்தா', 'MNVOYN': 'தாத்தா', 'MNVOMN': 'தாத்தா', },
{'YKMOVOYK':'தந்த','UNYOUKYO': 'தான', 'UNYOUKMO': 'தான', 'UNYOVKYO': 'தான', 'UNYOVKMO': 'தான', 'UNYOMKYO': 'தான', 'UNYOMKMO': 'தான', 'UNYOYKYO': 'தான', 'UNYOYKMO': 'தான', 'VNYOUKYO': 'தான', 'VNYOUKMO': 'தான', 'VNYOVKYO': 'தான', 'VNYOVKMO': 'தான', 'VNYOMKYO': 'தான', 'VNYOMKMO': 'தான', 'VNYOYKYO': 'தான', 'VNYOYKMO': 'தான', 'YNYOUKYO': 'தான', 'YNYOUKMO': 'தான', 'YNYOVKYO': 'தான', 'YNYOVKMO': 'தான', 'YNYOMKYO': 'தான', 'YNYOMKMO': 'தான', 'YNYOYKYO': 'தான', 'YNYOYKMO': 'தான', 'MNYOUKYO': 'தான', 'MNYOUKMO': 'தான', 'MNYOVKYO': 'தான', 'MNYOVKMO': 'தான', 'MNYOMKYO': 'தான', 'MNYOMKMO': 'தான', 'MNYOYKYO': 'தான', 'MNYOYKMO': 'தான', 'UNMOUKYO': 'தாந்த', 'UNMOUKMO': 'தாந்த', 'UNMOVKYO': 'தாந்த', 'UNMOVKMO': 'தாந்த', 'UNMOMKYO': 'தாந்த', 'UNMOMKMO': 'தாந்த', 'UNMOYKYO': 'தாந்த', 'UNMOYKMO': 'தாந்த', 'VNMOUKYO': 'தாந்த', 'VNMOUKMO': 'தாந்த', 'VNMOVKYO': 'தாந்த', 'VNMOVKMO': 'தாந்த', 'VNMOMKYO': 'தாந்த', 'VNMOMKMO': 'தாந்த', 'VNMOYKYO': 'தாந்த', 'VNMOYKMO': 'தாந்த', 'YNMOUKYO': 'தாந்த', 'YNMOUKMO': 'தாந்த', 'YNMOVKYO': 'தாந்த', 'YNMOVKMO': 'தாந்த', 'YNMOMKYO': 'தாந்த', 'YNMOMKMO': 'தாந்த', 'YNMOYKYO': 'தாந்த', 'YNMOYKMO': 'தாந்த', 'MNMOUKYO': 'தாந்த', 'MNMOUKMO': 'தாந்த', 'MNMOVKYO': 'தாந்த', 'MNMOVKMO': 'தாந்த', 'MNMOMKYO': 'தாந்த', 'MNMOMKMO': 'தாந்த', 'MNMOYKYO': 'தாந்த', 'MNMOYKMO': 'தாந்த', 'UNYOUNYO': 'தானா', 'UNYOUNMO': 'தானா', 'UNYOVNYO': 'தானா', 'UNYOVNMO': 'தானா', 'UNYOMNYO': 'தானா', 'UNYOMNMO': 'தானா', 'UNYOYNYO': 'தானா', 'UNYOYNMO': 'தானா', 'VNYOUNYO': 'தானா', 'VNYOUNMO': 'தானா', 'VNYOVNYO': 'தானா', 'VNYOVNMO': 'தானா', 'VNYOMNYO': 'தானா', 'VNYOMNMO': 'தானா', 'VNYOYNYO': 'தானா', 'VNYOYNMO': 'தானா', 'YNYOUNYO': 'தானா', 'YNYOUNMO': 'தானா', 'YNYOVNYO': 'தானா', 'YNYOVNMO': 'தானா', 'YNYOMNYO': 'தானா', 'YNYOMNMO': 'தானா', 'YNYOYNYO': 'தானா', 'YNYOYNMO': 'தானா', 'MNYOUNYO': 'தானா', 'MNYOUNMO': 'தானா', 'MNYOVNYO': 'தானா', 'MNYOVNMO': 'தானா', 'MNYOMNYO': 'தானா', 'MNYOMNMO': 'தானா', 'MNYOYNYO': 'தானா', 'MNYOYNMO': 'தானா', 'UNMOUNYO': 'தாந்தா', 'UNMOUNMO': 'தாந்தா', 'UNMOVNYO': 'தாந்தா', 'UNMOVNMO': 'தாந்தா', 'UNMOMNYO': 'தாந்தா', 'UNMOMNMO': 'தாந்தா', 'UNMOYNYO': 'தாந்தா', 'UNMOYNMO': 'தாந்தா', 'VNMOUNYO': 'தாந்தா', 'VNMOUNMO': 'தாந்தா', 'VNMOVNYO': 'தாந்தா', 'VNMOVNMO': 'தாந்தா', 'VNMOMNYO': 'தாந்தா', 'VNMOMNMO': 'தாந்தா', 'VNMOYNYO': 'தாந்தா', 'VNMOYNMO': 'தாந்தா', 'YNMOUNYO': 'தாந்தா', 'YNMOUNMO': 'தாந்தா', 'YNMOVNYO': 'தாந்தா', 'YNMOVNMO': 'தாந்தா', 'YNMOMNYO': 'தாந்தா', 'YNMOMNMO': 'தாந்தா', 'YNMOYNYO': 'தாந்தா', 'YNMOYNMO': 'தாந்தா', 'MNMOUNYO': 'தாந்தா', 'MNMOUNMO': 'தாந்தா', 'MNMOVNYO': 'தாந்தா', 'MNMOVNMO': 'தாந்தா', 'MNMOMNYO': 'தாந்தா', 'MNMOMNMO': 'தாந்தா', 'MNMOYNYO': 'தாந்தா', 'MNMOYNMO': 'தாந்தா', 'UKVOUKYO': 'தத்த', 'UKVOUKMO': 'தத்த', 'UKVOVKYO': 'தத்த', 'UKVOVKMO': 'தத்த', 'UKVOYKYO': 'தத்த', 'UKVOYKMO': 'தத்த', 'UKVOMKYO': 'தத்த', 'UKVOMKMO': 'தத்த', 'VKVOUKYO': 'தத்த', 'VKVOUKMO': 'தத்த', 'VKVOVKYO': 'தத்த', 'VKVOVKMO': 'தத்த', 'VKVOYKYO': 'தத்த', 'VKVOYKMO': 'தத்த', 'VKVOMKYO': 'தத்த', 'VKVOMKMO': 'தத்த', 'YKVOUKYO': 'தத்த', 'YKVOUKMO': 'தத்த', 'YKVOVKYO': 'தத்த', 'YKVOVKMO': 'தத்த', 'YKVOYKYO': 'தத்த', 'YKVOYKMO': 'தத்த', 'YKVOMKYO': 'தத்த', 'YKVOMKMO': 'தத்த', 'MKVOUKYO': 'தத்த', 'MKVOUKMO': 'தத்த', 'MKVOVKYO': 'தத்த', 'MKVOVKMO': 'தத்த', 'MKVOYKYO': 'தத்த', 'MKVOYKMO': 'தத்த', 'MKVOMKYO': 'தத்த', 'MKVOMKMO': 'தத்த', 'UKYOVOUK': 'தத்த', 'UKYOVOVK': 'தத்த', 'UKYOVOYK': 'தத்த', 'UKYOVOMK': 'தத்த', 'VKYOVOUK': 'தத்த', 'VKYOVOVK': 'தத்த', 'VKYOVOYK': 'தத்த', 'VKYOVOMK': 'தத்த', 'YKYOVOUK': 'தத்த', 'YKYOVOVK': 'தத்த', 'YKYOVOYK': 'தத்த', 'YKYOVOMK': 'தத்த', 'MKYOVOUK': 'தத்த', 'MKYOVOVK': 'தத்த', 'MKYOVOYK': 'தத்த', 'MKYOVOMK': 'தத்த', 'UKMOUKYO': 'தந்த', 'UKMOUKMO': 'தந்த', 'UKMOVKYO': 'தந்த', 'UKMOVKMO': 'தந்த', 'UKMOYKYO': 'தன்ன', 'UKMOYKMO': 'தன்ன', 'UKMOMKYO': 'தன்ன', 'UKMOMKMO': 'தன்ன', 'VKMOUKYO': 'தந்த', 'VKMOUKMO': 'தந்த', 'VKMOVKYO': 'தந்த', 'VKMOVKMO': 'தந்த', 'VKMOYKYO': 'தன்ன', 'VKMOYKMO': 'தன்ன', 'VKMOMKYO': 'தன்ன', 'VKMOMKMO': 'தன்ன', 'YKMOUKYO': 'தந்த', 'YKMOUKMO': 'தந்த', 'YKMOVKYO': 'தந்த', 'YKMOVKMO': 'தந்த', 'YKMOYKYO': 'தன்ன', 'YKMOYKMO': 'தன்ன', 'YKMOMKYO': 'தன்ன', 'YKMOMKMO': 'தன்ன', 'MKMOUKYO': 'தந்த', 'MKMOUKMO': 'தந்த', 'MKMOVKYO': 'தந்த', 'MKMOVKMO': 'தந்த', 'MKMOYKYO': 'தன்ன', 'MKMOYKMO': 'தன்ன', 'MKMOMKYO': 'தன்ன', 'MKMOMKMO': 'தன்ன', 'UKYOMOUK': 'தந்த', 'UKYOMOVK': 'தந்த', 'UKYOMOYK': 'தந்த', 'UKYOMOMK': 'தந்த', 'VKYOMOUK': 'தந்த', 'VKYOMOVK': 'தந்த', 'VKYOMOYK': 'தந்த', 'VKYOMOMK': 'தந்த', 'YKYOMOUK': 'தந்த', 'YKYOMOVK': 'தந்த', 'YKYOMOYK': 'தந்த', 'YKYOMOMK': 'தந்த', 'MKYOMOUK': 'தந்த', 'MKYOMOVK': 'தந்த', 'MKYOMOYK': 'தந்த', 'MKYOMOMK': 'தந்த', 'UKYOVKYO': 'தய்ய', 'UKYOVKMO': 'தய்ய', 'UKYOYKYO': 'தய்ய', 'UKYOYKMO': 'தய்ய', 'VKYOVKYO': 'தய்ய', 'VKYOVKMO': 'தய்ய', 'VKYOYKYO': 'தய்ய', 'VKYOYKMO': 'தய்ய', 'YKYOVKYO': 'தய்ய', 'YKYOVKMO': 'தய்ய', 'YKYOYKYO': 'தய்ய', 'YKYOYKMO': 'தய்ய', 'MKYOVKYO': 'தய்ய', 'MKYOVKMO': 'தய்ய', 'MKYOYKYO': 'தய்ய', 'MKYOYKMO': 'தய்ய', 'UKVOUNYO': 'தத்தா', 'UKVOUNMO': 'தத்தா', 'UKVOVNYO': 'தத்தா', 'UKVOVNMO': 'தத்தா', 'UKVOYNYO': 'தத்தா', 'UKVOYNMO': 'தத்தா', 'UKVOMNYO': 'தத்தா', 'UKVOMNMO': 'தத்தா', 'VKVOUNYO': 'தத்தா', 'VKVOUNMO': 'தத்தா', 'VKVOVNYO': 'தத்தா', 'VKVOVNMO': 'தத்தா', 'VKVOYNYO': 'தத்தா', 'VKVOYNMO': 'தத்தா', 'VKVOMNYO': 'தத்தா', 'VKVOMNMO': 'தத்தா', 'YKVOUNYO': 'தத்தா', 'YKVOUNMO': 'தத்தா', 'YKVOVNYO': 'தத்தா', 'YKVOVNMO': 'தத்தா', 'YKVOYNYO': 'தத்தா', 'YKVOYNMO': 'தத்தா', 'YKVOMNYO': 'தத்தா', 'YKVOMNMO': 'தத்தா', 'MKVOUNYO': 'தத்தா', 'MKVOUNMO': 'தத்தா', 'MKVOVNYO': 'தத்தா', 'MKVOVNMO': 'தத்தா', 'MKVOYNYO': 'தத்தா', 'MKVOYNMO': 'தத்தா', 'MKVOMNYO': 'தத்தா', 'MKVOMNMO': 'தத்தா', 'UKYOVOUN': 'தத்தா', 'UKYOVOVN': 'தத்தா', 'UKYOVOYN': 'தத்தா', 'UKYOVOMN': 'தத்தா', 'VKYOVOUN': 'தத்தா', 'VKYOVOVN': 'தத்தா', 'VKYOVOYN': 'தத்தா', 'VKYOVOMN': 'தத்தா', 'YKYOVOUN': 'தத்தா', 'YKYOVOVN': 'தத்தா', 'YKYOVOYN': 'தத்தா', 'YKYOVOMN': 'தத்தா', 'MKYOVOUN': 'தத்தா', 'MKYOVOVN': 'தத்தா', 'MKYOVOYN': 'தத்தா', 'MKYOVOMN': 'தத்தா', 'UKMOUNYO': 'தந்தா', 'UKMOUNMO': 'தந்தா', 'UKMOVNYO': 'தந்தா', 'UKMOVNMO': 'தந்தா', 'UKMOYNYO': 'தன்னா', 'UKMOYNMO': 'தன்னா', 'UKMOMNYO': 'தன்னா', 'UKMOMNMO': 'தன்னா', 'VKMOUNYO': 'தந்தா', 'VKMOUNMO': 'தந்தா', 'VKMOVNYO': 'தந்தா', 'VKMOVNMO': 'தந்தா', 'VKMOYNYO': 'தன்னா', 'VKMOYNMO': 'தன்னா', 'VKMOMNYO': 'தன்னா', 'VKMOMNMO': 'தன்னா', 'YKMOUNYO': 'தந்தா', 'YKMOUNMO': 'தந்தா', 'YKMOVNYO': 'தந்தா', 'YKMOVNMO': 'தந்தா', 'YKMOYNYO': 'தன்னா', 'YKMOYNMO': 'தன்னா', 'YKMOMNYO': 'தன்னா', 'YKMOMNMO': 'தன்னா', 'MKMOUNYO': 'தந்தா', 'MKMOUNMO': 'தந்தா', 'MKMOVNYO': 'தந்தா', 'MKMOVNMO': 'தந்தா', 'MKMOYNYO': 'தன்னா', 'MKMOYNMO': 'தன்னா', 'MKMOMNYO': 'தன்னா', 'MKMOMNMO': 'தன்னா', 'UKYOMOUN': 'தந்தா', 'UKYOMOVN': 'தந்தா', 'UKYOMOYN': 'தந்தா', 'UKYOMOMN': 'தந்தா', 'VKYOMOUN': 'தந்தா', 'VKYOMOVN': 'தந்தா', 'VKYOMOYN': 'தந்தா', 'VKYOMOMN': 'தந்தா', 'YKYOMOUN': 'தந்தா', 'YKYOMOVN': 'தந்தா', 'YKYOMOYN': 'தந்தா', 'YKYOMOMN': 'தந்தா', 'MKYOMOUN': 'தந்தா', 'MKYOMOVN': 'தந்தா', 'MKYOMOYN': 'தந்தா', 'MKYOMOMN': 'தந்தா', 'UKYOVNYO': 'தய்யா', 'UKYOVNMO': 'தய்யா', 'UKYOYNYO': 'தய்யா', 'UKYOYNMO': 'தய்யா', 'VKYOVNYO': 'தய்யா', 'VKYOVNMO': 'தய்யா', 'VKYOYNYO': 'தய்யா', 'VKYOYNMO': 'தய்யா', 'YKYOVNYO': 'தய்யா', 'YKYOVNMO': 'தய்யா', 'YKYOYNYO': 'தய்யா', 'YKYOYNMO': 'தய்யா', 'MKYOVNYO': 'தய்யா', 'MKYOVNMO': 'தய்யா', 'MKYOYNYO': 'தய்யா', 'MKYOYNMO': 'தய்யா', 'UNVOUKYO': 'தாத்த', 'UNVOUKMO': 'தாத்த', 'UNVOVKYO': 'தாத்த', 'UNVOVKMO': 'தாத்த', 'UNVOYKYO': 'தாத்த', 'UNVOYKMO': 'தாத்த', 'UNVOMKYO': 'தாத்த', 'UNVOMKMO': 'தாத்த', 'VNVOUKYO': 'தாத்த', 'VNVOUKMO': 'தாத்த', 'VNVOVKYO': 'தாத்த', 'VNVOVKMO': 'தாத்த', 'VNVOYKYO': 'தாத்த', 'VNVOYKMO': 'தாத்த', 'VNVOMKYO': 'தாத்த', 'VNVOMKMO': 'தாத்த', 'YNVOUKYO': 'தாத்த', 'YNVOUKMO': 'தாத்த', 'YNVOVKYO': 'தாத்த', 'YNVOVKMO': 'தாத்த', 'YNVOYKYO': 'தாத்த', 'YNVOYKMO': 'தாத்த', 'YNVOMKYO': 'தாத்த', 'YNVOMKMO': 'தாத்த', 'MNVOUKYO': 'தாத்த', 'MNVOUKMO': 'தாத்த', 'MNVOVKYO': 'தாத்த', 'MNVOVKMO': 'தாத்த', 'MNVOYKYO': 'தாத்த', 'MNVOYKMO': 'தாத்த', 'MNVOMKYO': 'தாத்த', 'MNVOMKMO': 'தாத்த', 'UNYOVOUK': 'தாத்த', 'UNYOVOVK': 'தாத்த', 'UNYOVOYK': 'தாத்த', 'UNYOVOMK': 'தாத்த', 'VNYOVOUK': 'தாத்த', 'VNYOVOVK': 'தாத்த', 'VNYOVOYK': 'தாத்த', 'VNYOVOMK': 'தாத்த', 'YNYOVOUK': 'தாத்த', 'YNYOVOVK': 'தாத்த', 'YNYOVOYK': 'தாத்த', 'YNYOVOMK': 'தாத்த', 'MNYOVOUK': 'தாத்த', 'MNYOVOVK': 'தாத்த', 'MNYOVOYK': 'தாத்த', 'MNYOVOMK': 'தாத்த', 'UNVOUNYO': 'தாத்தா', 'UNVOUNMO': 'தாத்தா', 'UNVOVNYO': 'தாத்தா', 'UNVOVNMO': 'தாத்தா', 'UNVOYNYO': 'தாத்தா', 'UNVOYNMO': 'தாத்தா', 'UNVOMNYO': 'தாத்தா', 'UNVOMNMO': 'தாத்தா', 'VNVOUNYO': 'தாத்தா', 'VNVOUNMO': 'தாத்தா', 'VNVOVNYO': 'தாத்தா', 'VNVOVNMO': 'தாத்தா', 'VNVOYNYO': 'தாத்தா', 'VNVOYNMO': 'தாத்தா', 'VNVOMNYO': 'தாத்தா', 'VNVOMNMO': 'தாத்தா', 'YNVOUNYO': 'தாத்தா', 'YNVOUNMO': 'தாத்தா', 'YNVOVNYO': 'தாத்தா', 'YNVOVNMO': 'தாத்தா', 'YNVOYNYO': 'தாத்தா', 'YNVOYNMO': 'தாத்தா', 'YNVOMNYO': 'தாத்தா', 'YNVOMNMO': 'தாத்தா', 'MNVOUNYO': 'தாத்தா', 'MNVOUNMO': 'தாத்தா', 'MNVOVNYO': 'தாத்தா', 'MNVOVNMO': 'தாத்தா', 'MNVOYNYO': 'தாத்தா', 'MNVOYNMO': 'தாத்தா', 'MNVOMNYO': 'தாத்தா', 'MNVOMNMO': 'தாத்தா', 'UNYOVOUN': 'தாத்தா', 'UNYOVOVN': 'தாத்தா', 'UNYOVOYN': 'தாத்தா', 'UNYOVOMN': 'தாத்தா', 'VNYOVOUN': 'தாத்தா', 'VNYOVOVN': 'தாத்தா', 'VNYOVOYN': 'தாத்தா', 'VNYOVOMN': 'தாத்தா', 'YNYOVOUN': 'தாத்தா', 'YNYOVOVN': 'தாத்தா', 'YNYOVOYN': 'தாத்தா', 'YNYOVOMN': 'தாத்தா', 'MNYOVOUN': 'தாத்தா', 'MNYOVOVN': 'தாத்தா', 'MNYOVOYN': 'தாத்தா', 'MNYOVOMN': 'தாத்தா', 'UNYOMOUK': 'தாந்த', 'UNYOMOVK': 'தாந்த', 'UNYOMOYK': 'தாந்த', 'UNYOMOMK': 'தாந்த', 'VNYOMOUK': 'தாந்த', 'VNYOMOVK': 'தாந்த', 'VNYOMOYK': 'தாந்த', 'VNYOMOMK': 'தாந்த', 'YNYOMOUK': 'தாந்த', 'YNYOMOVK': 'தாந்த', 'YNYOMOYK': 'தாந்த', 'YNYOMOMK': 'தாந்த', 'MNYOMOUK': 'தாந்த', 'MNYOMOVK': 'தாந்த', 'MNYOMOYK': 'தாந்த', 'MNYOMOMK': 'தாந்த', 'UNYOMOUN': 'தாந்தா', 'UNYOMOVN': 'தாந்தா', 'UNYOMOYN': 'தாந்தா', 'UNYOMOMN': 'தாந்தா', 'VNYOMOUN': 'தாந்தா', 'VNYOMOVN': 'தாந்தா', 'VNYOMOYN': 'தாந்தா', 'VNYOMOMN': 'தாந்தா', 'YNYOMOUN': 'தாந்தா', 'YNYOMOVN': 'தாந்தா', 'YNYOMOYN': 'தாந்தா', 'YNYOMOMN': 'தாந்தா', 'MNYOMOUN': 'தாந்தா', 'MNYOMOVN': 'தாந்தா', 'MNYOMOYN': 'தாந்தா', 'MNYOMOMN': 'தாந்தா', },
{'UKYOVOUKYO': 'தத்த', 'UKYOVOUKMO': 'தத்த', 'UKYOVOVKYO': 'தத்த', 'UKYOVOVKMO': 'தத்த', 'UKYOVOYKYO': 'தத்த', 'UKYOVOYKMO': 'தத்த', 'UKYOVOMKYO': 'தத்த', 'UKYOVOMKMO': 'தத்த', 'VKYOVOUKYO': 'தத்த', 'VKYOVOUKMO': 'தத்த', 'VKYOVOVKYO': 'தத்த', 'VKYOVOVKMO': 'தத்த', 'VKYOVOYKYO': 'தத்த', 'VKYOVOYKMO': 'தத்த', 'VKYOVOMKYO': 'தத்த', 'VKYOVOMKMO': 'தத்த', 'YKYOVOUKYO': 'தத்த', 'YKYOVOUKMO': 'தத்த', 'YKYOVOVKYO': 'தத்த', 'YKYOVOVKMO': 'தத்த', 'YKYOVOYKYO': 'தத்த', 'YKYOVOYKMO': 'தத்த', 'YKYOVOMKYO': 'தத்த', 'YKYOVOMKMO': 'தத்த', 'MKYOVOUKYO': 'தத்த', 'MKYOVOUKMO': 'தத்த', 'MKYOVOVKYO': 'தத்த', 'MKYOVOVKMO': 'தத்த', 'MKYOVOYKYO': 'தத்த', 'MKYOVOYKMO': 'தத்த', 'MKYOVOMKYO': 'தத்த', 'MKYOVOMKMO': 'தத்த', 'UKYOMOUKYO': 'தந்த', 'UKYOMOUKMO': 'தந்த', 'UKYOMOVKYO': 'தந்த', 'UKYOMOVKMO': 'தந்த', 'UKYOMOYKYO': 'தந்த', 'UKYOMOYKMO': 'தந்த', 'UKYOMOMKYO': 'தந்த', 'UKYOMOMKMO': 'தந்த', 'VKYOMOUKYO': 'தந்த', 'VKYOMOUKMO': 'தந்த', 'VKYOMOVKYO': 'தந்த', 'VKYOMOVKMO': 'தந்த', 'VKYOMOYKYO': 'தந்த', 'VKYOMOYKMO': 'தந்த', 'VKYOMOMKYO': 'தந்த', 'VKYOMOMKMO': 'தந்த', 'YKYOMOUKYO': 'தந்த', 'YKYOMOUKMO': 'தந்த', 'YKYOMOVKYO': 'தந்த', 'YKYOMOVKMO': 'தந்த', 'YKYOMOYKYO': 'தந்த', 'YKYOMOYKMO': 'தந்த', 'YKYOMOMKYO': 'தந்த', 'YKYOMOMKMO': 'தந்த', 'MKYOMOUKYO': 'தந்த', 'MKYOMOUKMO': 'தந்த', 'MKYOMOVKYO': 'தந்த', 'MKYOMOVKMO': 'தந்த', 'MKYOMOYKYO': 'தந்த', 'MKYOMOYKMO': 'தந்த', 'MKYOMOMKYO': 'தந்த', 'MKYOMOMKMO': 'தந்த', 'UKYOVOUNYO': 'தத்தா', 'UKYOVOUNMO': 'தத்தா', 'UKYOVOVNYO': 'தத்தா', 'UKYOVOVNMO': 'தத்தா', 'UKYOVOYNYO': 'தத்தா', 'UKYOVOYNMO': 'தத்தா', 'UKYOVOMNYO': 'தத்தா', 'UKYOVOMNMO': 'தத்தா', 'VKYOVOUNYO': 'தத்தா', 'VKYOVOUNMO': 'தத்தா', 'VKYOVOVNYO': 'தத்தா', 'VKYOVOVNMO': 'தத்தா', 'VKYOVOYNYO': 'தத்தா', 'VKYOVOYNMO': 'தத்தா', 'VKYOVOMNYO': 'தத்தா', 'VKYOVOMNMO': 'தத்தா', 'YKYOVOUNYO': 'தத்தா', 'YKYOVOUNMO': 'தத்தா', 'YKYOVOVNYO': 'தத்தா', 'YKYOVOVNMO': 'தத்தா', 'YKYOVOYNYO': 'தத்தா', 'YKYOVOYNMO': 'தத்தா', 'YKYOVOMNYO': 'தத்தா', 'YKYOVOMNMO': 'தத்தா', 'MKYOVOUNYO': 'தத்தா', 'MKYOVOUNMO': 'தத்தா', 'MKYOVOVNYO': 'தத்தா', 'MKYOVOVNMO': 'தத்தா', 'MKYOVOYNYO': 'தத்தா', 'MKYOVOYNMO': 'தத்தா', 'MKYOVOMNYO': 'தத்தா', 'MKYOVOMNMO': 'தத்தா', 'UKYOMOUNYO': 'தந்தா', 'UKYOMOUNMO': 'தந்தா', 'UKYOMOVNYO': 'தந்தா', 'UKYOMOVNMO': 'தந்தா', 'UKYOMOYNYO': 'தந்தா', 'UKYOMOYNMO': 'தந்தா', 'UKYOMOMNYO': 'தந்தா', 'UKYOMOMNMO': 'தந்தா', 'VKYOMOUNYO': 'தந்தா', 'VKYOMOUNMO': 'தந்தா', 'VKYOMOVNYO': 'தந்தா', 'VKYOMOVNMO': 'தந்தா', 'VKYOMOYNYO': 'தந்தா', 'VKYOMOYNMO': 'தந்தா', 'VKYOMOMNYO': 'தந்தா', 'VKYOMOMNMO': 'தந்தா', 'YKYOMOUNYO': 'தந்தா', 'YKYOMOUNMO': 'தந்தா', 'YKYOMOVNYO': 'தந்தா', 'YKYOMOVNMO': 'தந்தா', 'YKYOMOYNYO': 'தந்தா', 'YKYOMOYNMO': 'தந்தா', 'YKYOMOMNYO': 'தந்தா', 'YKYOMOMNMO': 'தந்தா', 'MKYOMOUNYO': 'தந்தா', 'MKYOMOUNMO': 'தந்தா', 'MKYOMOVNYO': 'தந்தா', 'MKYOMOVNMO': 'தந்தா', 'MKYOMOYNYO': 'தந்தா', 'MKYOMOYNMO': 'தந்தா', 'MKYOMOMNYO': 'தந்தா', 'MKYOMOMNMO': 'தந்தா', 'UNYOVOUKYO': 'தாத்த', 'UNYOVOUKMO': 'தாத்த', 'UNYOVOVKYO': 'தாத்த', 'UNYOVOVKMO': 'தாத்த', 'UNYOVOYKYO': 'தாத்த', 'UNYOVOYKMO': 'தாத்த', 'UNYOVOMKYO': 'தாத்த', 'UNYOVOMKMO': 'தாத்த', 'VNYOVOUKYO': 'தாத்த', 'VNYOVOUKMO': 'தாத்த', 'VNYOVOVKYO': 'தாத்த', 'VNYOVOVKMO': 'தாத்த', 'VNYOVOYKYO': 'தாத்த', 'VNYOVOYKMO': 'தாத்த', 'VNYOVOMKYO': 'தாத்த', 'VNYOVOMKMO': 'தாத்த', 'YNYOVOUKYO': 'தாத்த', 'YNYOVOUKMO': 'தாத்த', 'YNYOVOVKYO': 'தாத்த', 'YNYOVOVKMO': 'தாத்த', 'YNYOVOYKYO': 'தாத்த', 'YNYOVOYKMO': 'தாத்த', 'YNYOVOMKYO': 'தாத்த', 'YNYOVOMKMO': 'தாத்த', 'MNYOVOUKYO': 'தாத்த', 'MNYOVOUKMO': 'தாத்த', 'MNYOVOVKYO': 'தாத்த', 'MNYOVOVKMO': 'தாத்த', 'MNYOVOYKYO': 'தாத்த', 'MNYOVOYKMO': 'தாத்த', 'MNYOVOMKYO': 'தாத்த', 'MNYOVOMKMO': 'தாத்த', 'UNYOVOUNYO': 'தாத்தா', 'UNYOVOUNMO': 'தாத்தா', 'UNYOVOVNYO': 'தாத்தா', 'UNYOVOVNMO': 'தாத்தா', 'UNYOVOYNYO': 'தாத்தா', 'UNYOVOYNMO': 'தாத்தா', 'UNYOVOMNYO': 'தாத்தா', 'UNYOVOMNMO': 'தாத்தா', 'VNYOVOUNYO': 'தாத்தா', 'VNYOVOUNMO': 'தாத்தா', 'VNYOVOVNYO': 'தாத்தா', 'VNYOVOVNMO': 'தாத்தா', 'VNYOVOYNYO': 'தாத்தா', 'VNYOVOYNMO': 'தாத்தா', 'VNYOVOMNYO': 'தாத்தா', 'VNYOVOMNMO': 'தாத்தா', 'YNYOVOUNYO': 'தாத்தா', 'YNYOVOUNMO': 'தாத்தா', 'YNYOVOVNYO': 'தாத்தா', 'YNYOVOVNMO': 'தாத்தா', 'YNYOVOYNYO': 'தாத்தா', 'YNYOVOYNMO': 'தாத்தா', 'YNYOVOMNYO': 'தாத்தா', 'YNYOVOMNMO': 'தாத்தா', 'MNYOVOUNYO': 'தாத்தா', 'MNYOVOUNMO': 'தாத்தா', 'MNYOVOVNYO': 'தாத்தா', 'MNYOVOVNMO': 'தாத்தா', 'MNYOVOYNYO': 'தாத்தா', 'MNYOVOYNMO': 'தாத்தா', 'MNYOVOMNYO': 'தாத்தா', 'MNYOVOMNMO': 'தாத்தா', 'UNYOMOUKYO': 'தாந்த', 'UNYOMOUKMO': 'தாந்த', 'UNYOMOVKYO': 'தாந்த', 'UNYOMOVKMO': 'தாந்த', 'UNYOMOYKYO': 'தாந்த', 'UNYOMOYKMO': 'தாந்த', 'UNYOMOMKYO': 'தாந்த', 'UNYOMOMKMO': 'தாந்த', 'VNYOMOUKYO': 'தாந்த', 'VNYOMOUKMO': 'தாந்த', 'VNYOMOVKYO': 'தாந்த', 'VNYOMOVKMO': 'தாந்த', 'VNYOMOYKYO': 'தாந்த', 'VNYOMOYKMO': 'தாந்த', 'VNYOMOMKYO': 'தாந்த', 'VNYOMOMKMO': 'தாந்த', 'YNYOMOUKYO': 'தாந்த', 'YNYOMOUKMO': 'தாந்த', 'YNYOMOVKYO': 'தாந்த', 'YNYOMOVKMO': 'தாந்த', 'YNYOMOYKYO': 'தாந்த', 'YNYOMOYKMO': 'தாந்த', 'YNYOMOMKYO': 'தாந்த', 'YNYOMOMKMO': 'தாந்த', 'MNYOMOUKYO': 'தாந்த', 'MNYOMOUKMO': 'தாந்த', 'MNYOMOVKYO': 'தாந்த', 'MNYOMOVKMO': 'தாந்த', 'MNYOMOYKYO': 'தாந்த', 'MNYOMOYKMO': 'தாந்த', 'MNYOMOMKYO': 'தாந்த', 'MNYOMOMKMO': 'தாந்த', 'UNYOMOUNYO': 'தாந்தா', 'UNYOMOUNMO': 'தாந்தா', 'UNYOMOVNYO': 'தாந்தா', 'UNYOMOVNMO': 'தாந்தா', 'UNYOMOYNYO': 'தாந்தா', 'UNYOMOYNMO': 'தாந்தா', 'UNYOMOMNYO': 'தாந்தா', 'UNYOMOMNMO': 'தாந்தா', 'VNYOMOUNYO': 'தாந்தா', 'VNYOMOUNMO': 'தாந்தா', 'VNYOMOVNYO': 'தாந்தா', 'VNYOMOVNMO': 'தாந்தா', 'VNYOMOYNYO': 'தாந்தா', 'VNYOMOYNMO': 'தாந்தா', 'VNYOMOMNYO': 'தாந்தா', 'VNYOMOMNMO': 'தாந்தா', 'YNYOMOUNYO': 'தாந்தா', 'YNYOMOUNMO': 'தாந்தா', 'YNYOMOVNYO': 'தாந்தா', 'YNYOMOVNMO': 'தாந்தா', 'YNYOMOYNYO': 'தாந்தா', 'YNYOMOYNMO': 'தாந்தா', 'YNYOMOMNYO': 'தாந்தா', 'YNYOMOMNMO': 'தாந்தா', 'MNYOMOUNYO': 'தாந்தா', 'MNYOMOUNMO': 'தாந்தா', 'MNYOMOVNYO': 'தாந்தா', 'MNYOMOVNMO': 'தாந்தா', 'MNYOMOYNYO': 'தாந்தா', 'MNYOMOYNMO': 'தாந்தா', 'MNYOMOMNYO': 'தாந்தா', 'MNYOMOMNMO': 'தாந்தா'}
]
if __name__ == '__main__':
    """
    VANNAPAA_DICT2 = _get_vannappa_dictionary()
    print(VANNAPAA_DICT2)
    exit()
    """
    #"""
    s = 'அஃதின்றேல்'
    word = grammar.Sol(s)
    print(word.duration('vannapa'))
    nko = word._get_nko_yinam_string('vannapa', last_word=False, middle_word=False)
    sandha_kuzhippu = word.sandha_kuzhippu('vannapa', last_word=False, middle_word=False)
    print(word.text(),nko,sandha_kuzhippu)
    exit()
    #"""
    """
    s = "முத்து, வற்றல், விட்டம், மொய்த்த, மெய்ச்சொல், கர்த்தன்\n"+ \
"அக்கா, முட்டாள், விட்டான், பொய்க்கோ, நெய்க்கோல், மெய்க்கோன்\n"+ \
"பாட்டு, பாட்டன், கூத்தன், வார்ப்பு, தூர்த்தன், வாழ்த்தல்\n"+ \
"தாத்தா, மூச்சால், சாத்தான், வேய்ப்பூ, மாய்த்தோர், வார்த்தோன்\n"+ \
"பந்து, உம்பர், சுண்டல், மொய்ம்பு, மொய்ம்பர், மொய்ம்பன்\n"+ \
"அந்தோ, வந்தார், தந்தேன், மொய்ம்பா, மொய்ம்போர், மொய்ம்போன்\n"+ \
"வேந்து, வேந்தர், பாங்கன், பாய்ந்து, சார்ங்கர், சார்ங்கம்\n"+ \
"சேந்தா, வாங்கார், நான்றான், நேர்ந்தோ, சார்ந்தார், மாய்ந்தான்"#வற்றல் விட்டம்"
    for w in s.split(','):
        word = grammar.Sol(w)
        nko = word._get_nko_yinam_string('vannapa', last_word=False, middle_word=False)
        sandha_kuzhippu = word.sandha_kuzhippu('vannapa', last_word=False, middle_word=False)
        print(word.text(),nko,sandha_kuzhippu)
    exit()
    VANNAPAA_DICT2 = {}
    for key,values in VANNAPAA_DICT1.items():
        for value in values:
            VANNAPAA_DICT2[value]=key
    temp1 = sorted(list(VANNAPAA_DICT2.items()), key = lambda key : len(key[0]))
    VANNAPAA_DICT2 = {ele[0] : ele[1]  for ele in temp1}
    """
    words = 'முத்து,வற்றல்,விட்டம்,மொய்த்த,மெய்ச்சொல்,கர்த்தன்'
    for word in words.split(','):
        word_object = grammar.Sol(word)
        nko = word_object._get_nko_yinam_string('vannappa', last_word=False)
        print(word,nko)
    exit()
    print(print(get_unicode_characters('முத்து, வற்றல்,அரிதினில்')))
    exit()
    print(len(get_all_tamil_characters()))
    exit()
    s = "முத்து, வற்றல், விட்டம், மொய்த்த, மெய்ச்சொல், கர்த்தன்\n"+ \
"அக்கா, முட்டாள், விட்டான், பொய்க்கோ, நெய்க்கோல், மெய்க்கோன்\n"+ \
"பாட்டு, பாட்டன், கூத்தன், வார்ப்பு, தூர்த்தன், வாழ்த்தல்\n"+ \
"தாத்தா, மூச்சால், சாத்தான், வேய்ப்பூ, மாய்த்தோர், வார்த்தோன்\n"+ \
"பந்து, உம்பர், சுண்டல், மொய்ம்பு, மொய்ம்பர், மொய்ம்பன்\n"+ \
"அந்தோ, வந்தார், தந்தேன், மொய்ம்பா, மொய்ம்போர், மொய்ம்போன்\n"+ \
"வேந்து, வேந்தர், பாங்கன், பாய்ந்து, சார்ங்கர், சார்ங்கம்\n"+ \
"சேந்தா, வாங்கார், நான்றான், நேர்ந்தோ, சார்ந்தார், மாய்ந்தான்"#வற்றல் விட்டம்"
    print(s,'\n',get_character_type_counts(s,show_by_character_type_keys=False, include_zero_counts=False))
    exit()
    s = "NOKOKNKO"
    total = sum([SANDHA_PAA_DURATION[k] for k in s])
    print(total)
    exit()
    print('first morpheme',get_first_morpheme("காய்"),'last morpheme',get_last_morpheme("காய்"))
    exit()
    print(insert_string_at_index(get_unicode_characters('தனந்தரும் கல்வி தருமொரு நாளும் தளர்வறியா'),'()',-1))
    exit()
    words = ["மா", "விளம்", "காய்", "கனி", "பூ", "மா", "விளம்", "காய்", "கனி", "பூ"]
    specific_words = ["விளம்"]
    print(frequency_of_occurrence(words))
    print(frequency_of_occurrence(words, specific_words))
    print(percentage_of_occurrence(words))
    print(percentage_of_occurrence(words, specific_words))
    exit()
    print(get_matching_sublist('சை',flatten_list([MONAI_THODAI_4, MONAI_THODAI_5, MONAI_THODAI_6]),8))
    print(get_matching_sublist('வெ',flatten_list([MONAI_THODAI_1, MONAI_THODAI_2, MONAI_THODAI_3]),4))
    exit()
    print(get_keys_containing_string(THALAI_TYPES,'தேமாந்தண்பூ நேர் நேர் நேர் நிரை' ))
    exit()
    print(get_unicode_characters('க்ஷோக்ஷௌஹோ'))
    exit()
    print('கூவிளங்கனி','ங்',string_has_unicode_character('கூவிளங்கனி','ங்'))
    print('கூவிளங்கனி',"ூ",string_has_unicode_character('கூவிளங்கனி',"ூ"))
    exit()
    sol = grammar.Sol('கூவிளங்கனி')
    exit()
    get_unicode_characters(str)
    exit()
    print(str,str[-1])
    print(str, string_has_unicode_character(str, "ூ"))
    tamil_letter = grammar.Ezhuthu('கூ')
    print(tamil_letter.text,tamil_letter.is_nedil,'is kuril',tamil_letter.is_kuril)