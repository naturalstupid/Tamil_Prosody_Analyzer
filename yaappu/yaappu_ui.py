# coding=utf8
from PyQt6 import QtTest
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtGui import QFont
from yaappu import Sandhapa, Vannapa
grammar = __import__("grammar")
utils = __import__("utils")
_APP_TITLE = "Tamil Prosody Analyzer"
def _set_text_edit_size_to_rows(text_edit:QTextEdit,n_rows):
    m = QtGui.QFontMetrics(text_edit.font())
    row_height = m.lineSpacing()
    text_edit.setFixedHeight(n_rows*row_height)
class MyAppWidget(QWidget):
    def __init__(self, tamil_poem_file=None):
        super(MyAppWidget,self).__init__()
        self.tamil_poem_file = tamil_poem_file
        self.setWindowTitle(_APP_TITLE)
        window_height = 500
        window_width = 750
        self.setMinimumSize(window_width, window_height)
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        isaipa_label = QLabel("இசைப்பாவை ஆராயவும்:")
        h_layout.addWidget(isaipa_label)
        #button_group = QButtonGroup()
        self._btnSandhapa = QCheckBox("சந்தப்பா") #QRadioButton("சந்தப்பா")
        self._btnSandhapa.clicked.connect(self._isaipaa_selection_changed)
        self._btnSandhapa.setChecked(False)
        #button_group.addButton(self._btnSandhapa)
        h_layout.addWidget(self._btnSandhapa)
        self._btnVannapa = QCheckBox("வண்ணப்பா") # QRadioButton("வண்ணப்பா")
        self._btnVannapa.clicked.connect(self._isaipaa_selection_changed)
        self._btnVannapa.setChecked(False)
        #button_group.addButton(self._btnVannapa)
        h_layout.addWidget(self._btnVannapa)
        self._isaipaa_selected = self._btnSandhapa.isChecked() or self._btnVannapa.isChecked()
        #print('_isaipaa_selected',self._isaipaa_selected)
        h_layout.addStretch()
        layout.addLayout(h_layout)
        self.input_text = QTextEdit()
        #splitter = QSplitter(Qt.Orientation.Vertical)
        #splitter.addWidget(self.input_text)
        #self.input_text.setMaximumHeight(int(0.25*window_height))
        _set_text_edit_size_to_rows(self.input_text,10)
        layout.addWidget(self.input_text)
        self.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        buttonLayout = QHBoxLayout()
        open_button = QPushButton("செய்யுள் கோப்பை திறக்கவும்")
        open_button.clicked.connect(self.display_file_contents)
        buttonLayout.addWidget(open_button)
        analyze_button = QPushButton("யாப்பறி")
        analyze_button.clicked.connect(self.analyze_poem)
        buttonLayout.addWidget(analyze_button)
        reset_button = QPushButton("மீட்டமை ")
        reset_button.clicked.connect(self.clear_all_text)
        buttonLayout.addWidget(reset_button)
        close_button = QPushButton("வெளியேறு")
        close_button.clicked.connect(self.quit)
        buttonLayout.addWidget(close_button)
        #""" Not wotking yet
        save_as_pdf_button = QPushButton("வெளியீட்டை சேமி")
        save_as_pdf_button.clicked.connect(self._save_as_text) #(self._save_as_image)
        buttonLayout.addWidget(save_as_pdf_button)
        #"""
        layout.addLayout(buttonLayout)
        self.tabWidget = QTabWidget()
        self.tabNames = ["எழுத்து", "அசை-சீர்-அடி", "தளை-ஓசை", "சீர்-தொடை", "அடி -தொடை","யாப்பு","ஆய்வு விவரங்கள்","இசைப்பா"]
        self.tabCount = len(self.tabNames)
        self.tabWidget.setTabEnabled(self.tabCount-1,self._isaipaa_selected)
        self.outputText = []
        for t in range(self.tabCount):
            self.outputText.append(QTextEdit(""))
            self.tabWidget.addTab(self.outputText[t],self.tabNames[t])
            self.outputText[t].setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.outputText[t].setLineWrapColumnOrWidth(window_width)
        layout.addWidget(self.tabWidget)
        self.setLayout(layout)
        self._display_file_contents(tamil_poem_file)
    def _isaipaa_selection_changed(self):
        self._isaipaa_selected = self._btnSandhapa.isChecked() or self._btnVannapa.isChecked()
        self.tabWidget.setTabEnabled(self.tabCount-1,self._isaipaa_selected)
        #print('_isaipaa_selected',self._isaipaa_selected)
    def _display_file_contents(self, tamil_poem_file):
        import os
        if tamil_poem_file:
            with open(tamil_poem_file, 'r', encoding='utf-8') as f:
                self.input_text.setPlainText(f.read())
            self.setWindowTitle(_APP_TITLE+"-"+os.path.basename(tamil_poem_file))
            self.analyze_poem()        
    def display_file_contents(self):
        path = QFileDialog.getOpenFileName(self, 'Open a tamil poem unicode text file', './test_input/', 'Text Files (*.txt)')#, '', QFileDialog_Options()
        tamil_poem_file = path[0]
        self._display_file_contents(tamil_poem_file)
    def _save_as_text(self):
        path = QFileDialog.getSaveFileName(self, 'Choose folder and file to save as text file', './output', 'Text files (*.txt)')#)
        output_file = path[0]
        f = open(output_file,"w",encoding='utf-8')
        indent = "\t\t\t\t\t"
        f.write(indent+"செய்யுள்"+"\n"+self.input_text.toPlainText()+"\n\n")
        for t in range(self.tabCount):
            f.write(indent+self.tabNames[t]+"\n")
            f.write(self.outputText[t].toPlainText()+"\n\n")
        f.close()
    def _save_as_image(self):
        """ TODO: To disable scrollbar while grabbing the UI """
        path = QFileDialog.getSaveFileName(self, 'Choose folder and file to save as image file', './output', 'Image files (*.png)')#)
        output_file = path[0]
        for t in range(self.tabCount):
            self.tabWidget.setCurrentIndex(t)
            self.outputText[t].setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            QApplication.processEvents()
            im = self.grab()
            saved_image_file = output_file.replace(".png","_tab_"+str(t)+".png") 
            print("Saved as "+saved_image_file)
            im.save(saved_image_file)
        for t in range(self.tabCount):
            self.outputText[t].setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
    def _save_as_pdf(self):
        """ Not working Yet """
        path = QFileDialog.getSaveFileName(self, 'Choose folder and file to save PDF file', './test/input', 'PDF files (*.pdf)')#)
        pdf_file = path[0]
        print(pdf_file)
        from fpdf import FPDF
        pdf = FPDF()
        font_name =  "Nirmala" # "Arial" #  
        font_file = "C:\\windows\\fonts\\nirmala.ttf"
        print('adding tamil font')
        pdf.add_font(font_name,'',font_file,uni=True)
        pdf.set_font(font_name,'',12)
        print('adding poem page')
        pdf.add_page()
        print('writing poem page')
        pdf.write(12, self.input_text.toPlainText())
        print('finished poem page')
        for t in range(self.tabCount):
            print('writing tab # info',t)
            pdf.add_page()
            tab_text = self.outputText[t].toPlainText()
            for line in tab_text.split("\n"):
                pdf.write(12,line)
                pdf.ln(12)
        print("writing",pdf_file)
        pdf.output(pdf_file)#,"F",True)
        print('finished')
    def clear_all_text(self):
        self.input_text.setPlainText("")
        for t in range(self.tabCount):
            self.outputText[t].setPlainText("")
        self.setWindowTitle(_APP_TITLE)
    def quit(self):
        sleepSecs = 0.5 * 1000  # 1 sec
        QtTest.QTest.qWait(sleepSecs)
        self.close()
    def __get_character_statistics(self, tamil_poem):
        result = ""# "அம்சம் இன்னும் செயல்படுத்தப்படவில்லை"
        for res in utils.get_character_type_counts(tamil_poem.text(),show_by_character_type_keys=False, include_zero_counts=False):
            result += res[0] + " : " +str(res[1]) + "\n"
        return result
    def __get_asai_seer_adi(self, tamil_poem):
        result = '' #"அம்சம் இன்னும் செயல்படுத்தப்படவில்லை"
        word_length = 40
        for line in tamil_poem.line_objects:
            line1, line2, line3, line4 = ['']*4
            for word in line.word_objects:
                line1 += "{:<{wl}}".format(word.asai_word(),wl=word_length)# + " "
                line2 += "{:<{wl}}".format(word.asaigaL(),wl=word_length)# + " "
                line3 += "{:<{wl}}".format(word.seer_type(),wl=word_length)# + " "
                line4 += "{:<{wl}}".format(word.sandha_seer(),wl=word_length)# + " "
            line_type = line.line_type()
            result += '\n'.join([line1, line2, line3, line4, line_type])+"\n\n"
        return result
    def __get_thaLai_Osai(self, tamil_poem):
        result = '' #"அம்சம் இன்னும் செயல்படுத்தப்படவில்லை"
        word_length = 40
        line_count = tamil_poem.line_count()
        lines = tamil_poem.line_objects
        for l in range(line_count):
            word_count = lines[l].word_count()
            for w in range(word_count):
                if (l==line_count-1 and w==word_count-1):
                    continue
                l1=l
                w1=w
                l2=l1
                w2=w1+1
                if (w2 == word_count):
                    w2 =0
                    l2 = l1+1
                word1 = lines[l1].word_objects[w1]
                word1_text = word1.text()
                seer1 = word1.seer_type()
                word2 = lines[l2].word_objects[w2]
                word2_text = word2.text()
                asai2 = word2.asaigaL().strip()
                thaLai_type = word1.thaLai_type(word2_text)
                osai_type = word1.osai_type(word2_text)
                result += "{:<{wl}}".format(str(word1_text+" - "+word2_text),wl=word_length)
                result += "{:<{wl}}".format(str(seer1+" - "+thaLai_type),wl=word_length)
                result += "{:<{wl}}".format(str(osai_type),wl=word_length) + "\n"
        return result
    def __get_seer_thodai(self, tamil_poem):
        result = "" #"அம்சம் இன்னும் செயல்படுத்தப்படவில்லை"
        len_arr = [line.word_count() for line in tamil_poem.line_objects]
        thodai_type_2d = []
        t1 = ["சீர் மோனை", "சீர் எதுகை", "சீர் இயைபு"]
        t2 = [0,1,-1]
        for t in t2:
            result += "\t\t\t{}".format(t1[t2.index(t)])+"\n"
            thodai_type_2d.append(tamil_poem.seer_thodai_words(t))
            for l in range(tamil_poem.line_count()):
                result +=' '.join(thodai_type_2d[t][l])+"\t"
                result += ''.join(tamil_poem.line_objects[l].seer_thodai_types[t])+"\n"
            result += "\n"
        return result
    def __get_adi_thodai(self, tamil_poem):
        result = ""#"அம்சம் இன்னும் செயல்படுத்தப்படவில்லை"
        t1 = ["அடி மோனை", "அடி எதுகை", "அடி இயைபு"]
        t2 = [0,1,-1]
        for t in t2:
            result += "\t\t\t{}".format(t1[t2.index(t)])+"\n"
            result += (tamil_poem.adi_thodai_lines(t,'<>'))
        return result
    def analyze_poem(self):
        poem_text = self.input_text.toPlainText()
        if poem_text.strip() != '':
            tamil_poem = grammar.Yaappu(poem_text)
            line_count = len(poem_text.split("\n"))
            _set_text_edit_size_to_rows(self.input_text,line_count+1)
            paa_check,poem_analysis = tamil_poem.analyze(get_individual_poem_analysis=True)
            self.outputText[0].setPlainText(self.__get_character_statistics(tamil_poem))
            self.outputText[1].setPlainText(self.__get_asai_seer_adi(tamil_poem))
            self.outputText[2].setPlainText(self.__get_thaLai_Osai(tamil_poem))
            self.outputText[3].setPlainText(self.__get_seer_thodai(tamil_poem))
            self.outputText[4].setPlainText(self.__get_adi_thodai(tamil_poem))
            self.outputText[5].setPlainText(paa_check[1] + grammar.RULE_CHECK(paa_check[0])+"\n"+paa_check[2])
            self.outputText[6].setPlainText(poem_analysis)
            if self._isaipaa_selected:
                isaipaa_str = ""
                if (self._btnSandhapa.isChecked()):
                    sandhappaa = Sandhapa.Sandhapa(poem_text)
                    paa_check, poem_type, paa_str = sandhappaa.check_for_sandhapaa();
                    isaipaa_str += str(paa_check) + '\n' + poem_type + '\n' + paa_str
                if (self._btnVannapa.isChecked()):
                    vannappaa = Vannapa.Vannapa(poem_text)
                    paa_check, poem_type, paa_str = vannappaa.check_for_vannapaa();
                    isaipaa_str += str(paa_check) + '\n' + poem_type + '\n' + paa_str
                #print(isaipaa_str)
                self.outputText[7].setPlainText(isaipaa_str)    
            self.tabWidget.setCurrentIndex(5)
        else:
            self.input_text.setPlainText('')
if __name__ == "__main__":
    import sys
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook

    app = QApplication(sys.argv)
    window = MyAppWidget('./test_input/Asiriyappavinam_ThuRai_Madakkai_2.txt')
    window.show()
    sys.exit(app.exec())        
        