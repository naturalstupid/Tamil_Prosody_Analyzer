# Tamil Prosody Analyzer / தமிழ் இயற்பா செயலி
This provides a python package to analyze Tamil poems and find out the poem types.  
இயற்றமிழ் என்பது நினைத்த கருத்தை உணர்த்துவதையே நோக்கமாகக் கொண்டு நடப்பது, பேச்சும், உரையும் செய்யுளும் இதில் அடங்கும். இயற்றமிழ்ச் செய்யுளை இயற்பா என்பர்.

இசைத்தமிழ் என்பது இசையின்பம் அளித்தலையே முதன்மை நோக்கமாகக் கொண்டு நடப்பது; சொற்பொருள் இன்பங்களையும் கொடுக்கக் கூடியது. இசைத்தமிழ் நூல்கள்; தேவாரம், திருவாசகம், நாலாயிரப் பனுவலில் (நாலாயிர திவ்விய பிரபந்தம்) முதலாயிரம், பெரிய திருமொழி, திருவாய்மொழி ஆகியன; திருப்புகழ் முதலியன.

Tamil poems are of two types namely:

1. இயற்பா  
1.1 வெண்பா மற்றும் வெண்பாவினம்  
1.2 ஆசிரியப்பா மற்றும் வெண்பாவினம்  
1.3 வஞ்சிப்பா மற்றும் வெண்பாவினம்  
1.4 கலிப்பா மற்றும் வெண்பாவினம்  
1.5 மருட்பா (மருள் - மயக்கம்; கலத்தல். வெண்பாவும் ஆசிரியப்பாவும் கலந்து அமைவது) <b>(Not Implemented)</b>  
2. இசைப்பா <b>(Not Implemented)</b>  
2.1 வண்ணப்பா  
2.2 சந்தப்பா  
2.2 சிந்துப்பா  
2.4 உருப்படிகள்  

This package contains five classes namely Ezhuthu, Sol, Adi, Yiyarpaa and Yaappu:
1. Ezhuthu:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil character and analyzes the character types. Provides methods such as is\_nedil(), is\_kuril(), is\_kutriyalugarm() etc.  
2. Sol:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil word (and calls internally Ezhuthu). Provides methods such as asaigaL() **Note: upper case L, thodai\_matches(with\_another\_word\_text) etc.  
3. Adi:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil sentence (and calls internally Sol). Provides methods such as sandha\_ozhungu(), seer\_thodai\_words() etc.  
4. Yiyarpu:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil Poem (and calls internally Adi). Provides methods such as sandha\_seergal(), thaLaigaL(), osaigaL(), vikarpam() etc.  
5. Yaappu:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil Poem (and calls internally Yiyarpu). Provides methods such as check\_for\_venpaa(), check\_for\_venpaavinam(), check\_for\_asiriyapaa() etc.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; In addition it also accepts two optional arguments namely:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;treat\_aaydham\_as\_kuril=False/True and   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;treat\_kutriyaligaram\_as\_otru=False/True    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; It provides a method <b> analyze() </b> with two optional arguments namely:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>poem\_type\_enum</b> and   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>get\_individual\_poem\_analysis=False/True</b>    

##Usage  
Sample code:  

<code>
        tp = Yaappu("மாதவா போதி வரதா வருளமலா \n"+
"பாதமே யோத சுரரைநீ - தீதகல \n"+
"மாயா நெறியளிப்பா யின்றன் பகலாச்சீர்த் \n"+
"தாயே யலகில்லா டாம்")

	
	tp.analyze()  
</code>
	<b> OR </b>  <br>
<code>  	
    paa_check,poem_analysis = tp.analyze(utils.POEM_TYPES.VENPA)
	
    print('============================================')

    print('POEM Results:',paa_check[1] + RULE_CHECK(paa_check[0]))
    
    print('POEM Results:',paa_check[2])
    
    print(tp.thaLaigaL())
    
    print(tp.seergaL(True))
    
    print(tp.asaigaL())
    
    print(tp.asai_words())
    
</code>
	============================================
	
POEM Results: பல விகற்ப நேரிசை வெண்பா	✔  

POEM Results: வெண்பா யாப்பிலக்கண விதிகள்

	✔  சீர் இலக்கணம் - ஈற்றடியின் ஈற்றுச்சீரைத் தவிர்த்து ஈரசைச்சீர்களும் காய்ச்சீர்களும் மட்டுமே பயின்று வருதல் வேண்டும்.( 100%  ≥  99% )
	
	✔  தளை இலக்கணம் - வெண்டளைகள் மட்டுமே பயின்று வருதல் வேண்டும்.( 100%  ≥  99% )
	
	✔  அடி இலக்கணம் - ஈற்றடி மூன்று சீர்களும் ஏனைய அடிகள் நான்கு சீர்களும் கொண்டிருத்தல் வேண்டும்.
	
	✔  ஓசை இலக்கணம் - செப்பலோசை மிகுந்து வரும்.( 100%  ≥  99% )
	
	✔  ஈற்றுச் சீர் இலக்கணம்  - ஈற்றடியின் ஈற்றுச்சீர் நாள், மலர், காசு, பிறப்பு ஆகியவற்றுள் இருத்தல் வேண்டும். (டாம்)
	
	✔  		நேரிசை வெண்பா -இரண்டாவது அடியில் தனிச்சொல் எதுகை அமைவது  (தீதகல)

பல விகற்ப நேரிசை வெண்பா

['இயற்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை', 'இயற்சீர் வெண்டளை', 'வெண்சீர் வெண்டளை']

['கூவிளம்', 'தேமா', 'புளிமா', 'கருவிளங்காய்', 'கூவிளம்', 'தேமா', 'கருவிளம்', 'கூவிளங்காய்', 'தேமா', 'கருவிளங்காய்', 'தேமா', 'புளிமாங்காய்', 'தேமா', 'புளிமாங்காய்', 'நாள்']

['நேர்/நிரை', 'நேர்/நேர்', 'நிரை/நேர்', 'நிரை/நிரை/நேர்', 'நேர்/நிரை', 'நேர்/நேர்', 'நிரை/நிரை', 'நேர்/நிரை/நேர்', 'நேர்/நேர்', 'நிரை/நிரை/நேர்', 'நேர்/நேர்', 'நிரை/நேர்/நேர்', 'நேர்/நேர்', 'நிரை/நேர்/நேர்', 'நேர்']

['மா/தவா', 'போ/தி', 'வர/தா', 'வரு/ளம/லா', 'பா/தமே', 'யோ/த', 'சுர/ரைநீ', 'தீ/தக/ல', 'மா/யா', 'நெறி/யளிப்/பா', 'யின்/றன்', 'பக/லாச்/சீர்த்', 'தா/யே', 'யல/கில்/லா', 'டாம்']

There is a test code provided testing all classes and methods.  
The main function also checks whether all 1330 thirukurals  from <b>thiukural.txt</b> are of type குறள் வெண்பா  







