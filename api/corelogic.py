from ast import Return
import spacy
import re
import string
from spacy.matcher import Matcher
from nltk.corpus import wordnet

import itertools

json={
  "RadioButton": {
    "gender": ["male", "female"],
    "terms condition": ["agree", "disagree"],
    "degree": ["completed", "pursuing"],
    "satisfiedonservice": ["less", "medium", "high"],
    "colors": ["black", "white", "blue"],
    "size": ["small", "medium", "large"],
    "select screen": ["home", "login", "signup", "dashboard"],
    "flavor": ["vanila", "choclate"],
    "choose": ["choose"]
  },
  "TextBoxes": [
    "name",
    "id",
    "password",
    "cell",
    "cnic",
    "zipcode",
    "state",
    "code",
    "phone",
    "username",
    "user id",
    "email",
    "company",
    "webaddress",
    "website",
    "quantity",
    "date",
    "join date",
    "joining",
    "date of join",
    "date of birth",
    "date of marriage",
    "address",
    "mail",
    "cell",
    "number",
    "no",
    "date",
    "days",
    "title",
    "price",
    "description",
    "requirements",
    "message",
    "complain",
    "letter",
    "overview",
    "comments",
    "qty",
    "quantity"
    "price"
  ],

  "CheckBoxes": [
    "subjects",
    "check expertise",
    "php",
    "ship to home",
    "ship",
    "work",
    "bank",
    "payment",
    "cash on deliverly",
    "credit card payment",
    "accept",
    "remember me",
    "keep me login"
  ],
  "ComboBoxes": [
    "select language",
    "languages",
    "select cities",
    "select cities",
    "programs",
    "select",
    "select programs",
    "choose",
    "select",
    "courses",
    "programs",
    "select month",
    "select date",
    "select year",
    "category",
    "options",
    "font",
    "courses",
    "ebooks"
  ]
}
class WordBank:
    def __init__(self,controls):
        self.controls = controls
        self.controlsdic = {

        }
        self.radiolst = []
        self.checklst = []
        self.txtlst = []
        self.combolst = []

        self.controlsname = ["RadioButton","CheckBoxes","ComboBoxes","TextBoxes"]
    def get_key(val):
        for key, value in json:
             if val == value:
                return key
    def get_all_values(self,nested_dictionary,control):
        for key, value in nested_dictionary.items():
            if type(value) is dict:
                self.get_all_values(value,control)
            else:
                for i in range(len(value)):
                    if(value[i] in control.lower()):
                        if(key not in self.controlsname):
                            control = "RadioButton"
                            return control
                        else:
                            control = key
                            return control
                    elif(key in control.lower()):

                        control = "RadioButton"
                        return control
    def get_controls(self):
        for i in range(len(self.controls)):
            self.controlname = self.get_all_values(json,self.controls[i])
            if(self.controlname == "TextBoxes" or self.controlname == None):
                self.txtlst.append(self.controls[i])
            elif(self.controlname =="RadioButton"):
                self.radiolst.append(self.controls[i])
            elif(self.controlname =="ComboBoxes"):
                self.combolst.append(self.controls[i])
            elif(self.controlname =="CheckBoxes"):
                self.checklst.append(self.controls[i])
        if(self.checklst != []):
            self.controlsdic["CheckBoxes"] = self.checklst
        if(self.combolst != []):
            self.controlsdic["ComboBoxes"] = self.combolst
        if(self.radiolst != []):
            self.controlsdic["RadioButton"] = self.radiolst
        if(self.txtlst != []):
            self.controlsdic["TextBoxes"] = self.txtlst
        return self.controlsdic
class ProVision:
    def __init__(self, userstory):
        self.output = {}
        self.nlp = spacy.load("en_core_web_sm")
        self.userstory = userstory
        doc = self.nlp(self.userstory)
        self.list_of_sents = self.find_sents(doc)
        self.errormsg = self.preprocess(self.list_of_sents)
        self.controloutput = {}
        
    def preprocess(self,list_of_sent):
        corrsenbool = []
        for i in range(len(list_of_sent)):
            x = re.search("^As\\sa|an\\s.*\\sI want\\s.*\\sso that\\s.*", str(list_of_sent[i]))
            y = re.search("^As\\sa|an\\s[a-z]*\\sI want\\s[a-z]*\s.*",str(list_of_sent[i]))
            if x or y:
                corrsenbool.append(True)
            else:
                corrsenbool.append(False)
        if(False in corrsenbool):
            print("op")
            return self.Error_Handle_Sent(corrsenbool)
        else:
            print("here")
            return True
    def main(self):
        screentitle = {}
        controlsdic = {}
        buttondic = {}
        titleOfProject = self.find_title_of_project(self.list_of_sents[0])
        print('title:',titleOfProject)
        print()
        screenlist = self.list_of_sents
        screenlist.pop(0)
        print('No of Screens',len(screenlist))
        print()
        for i in range(len(screenlist)):
            print('Screen',int(i+1))
            print()
            lst = self.detectscreentitle(str(screenlist[i]))
            controls,firstsent,lastsent = self.getcontrols(str(screenlist[i]))
            buttonlst = self.buttons_extraction(str(screenlist[i]))
            if(type(buttonlst) == list):
                buttondic['Screen'+str(int(i+1))] = [s.strip() for s in buttonlst]
            controls  = self.detectstopwordsfromlist([s.strip() for s in controls])
            a = WordBank(controls)
            controltitle = a.get_controls()
            self.controloutput['Screen'+str(int(i+1))] = controltitle
            screentitle['Screen'+str(int(i+1))] = [s.strip() for s in lst]
            controlsdic['Screen'+str(int(i+1))] = [s.strip() for s in controls]
            print("title:",[s.strip() for s in lst])
            print("controls",[s.strip() for s in controls])
            print("controls output",self.controloutput)
            print("Expected Buttons:",buttonlst)
            print()
        self.output['TITLE'] = titleOfProject
        self.output['SCREENS'] = screentitle
        self.output['CONTROLS'] = controlsdic
        self.output['BUTTONS'] = buttondic
        self.output['NOOFSCREENS'] = len(screenlist)
        return self.output,self.controloutput
    def detectstopwordsfromlist(self,controls):
        for i in range(len(controls)):
            tempstr  = ""
            nlpstr = self.nlp(controls[i])
            for token in nlpstr:
                if not token.is_stop:
                    tempstr = tempstr + token.text+' '
                if(tempstr != ""):
                    controls[i] = tempstr
            nlpstr = self.nlp(controls[i])
            tempstr  = ""
            for chunk in nlpstr.noun_chunks:
                tempstr = tempstr + chunk.text + ' '
        return controls
    def dstbyfnls(self,firstsent,lastsents):
        fsl = self.detectstopwords(self.nlp(firstsent))
        lsl = self.detectstopwords(self.nlp(lastsents))
        templst = self.nounchunklist(firstsent)
        if(templst != []):
            return templst

    def nounchunklist(self,firstsent):
        chunklst = []
        desc = self.nlp(firstsent)
        for i in desc.noun_chunks:
            chunklst.append(i.text)
        if(chunklst != []):
            return chunklst
    def prprnounpos(self,lst):
        templst = []
        for i in range(len(lst)):
            doc = self.nlp(lst[i])
            for i in doc:
                if i.pos_ == "PROPN":
                    templst.append(i.text)
        for i in range(len(templst)):
            if(templst[i] not in lst):
                lst.append(templst[i])
        return lst

    def detectstopwords(self,string):
        stopwords = []
        if(type(string) == list):
            for i in range(len(string)):
                tempstrnlp = self.nlp(string[i].strip())
                tempstr = ""
                for token in tempstrnlp:
                    if not token.is_stop:
                        tempstr = tempstr + token.text+' '
                if(string !=""):
                    string[i] = tempstr.strip()
                    return string
        else:
    #         print(type(string),"else type")
    #         print("else part")
    #         print("String",string)
            for token in string:
                if not token.is_stop:
                    stopwords.append(token.text)
            return stopwords

    def detectscreentitle(self,screenlist):
        postitle = []
        self.nlp = spacy.load("en_core_web_sm")
        string = screenlist
        lst = string.split(re.findall("^As a .+ I want",string)[0])
        sents = lst[1]
        original = ["details","providing","giving","description","title"]
        #PART ONE: Getting all the words between I want and original sysn
        synlst = self.getsynomynlst(original)
        title = self.nlp(sents)
        stopwords = []
        positions = []
        positiontext= []
        for i in title:
            if(i.lemma_ in synlst or i.text in original):
                positions.append(i.i)
                positiontext.append(i.text) 
        stringtitle = ''
        if(positiontext!= []):
            for i in title[:positions[0]]:
                stringtitle = stringtitle + i.text+' '
        if(stringtitle != ''):
            postitle.append(stringtitle) 
    #     else:
    #         print("elsepart")
    #         postitle.append(sents)
        postitle = self.nounchunkscreentitle(string,postitle)
        postitle = self.detectstopwords(postitle) #remove wordslike 'I', 'which','details'
        return postitle


    def nounchunkscreentitle(self,string,postitle):
        chunklst = []
        doc = self.nlp(string)
        for chunk in doc.noun_chunks:
            chunklst.append(chunk.text)
        if('I' in string):
            index = chunklst.index('I')
            postitle.append(chunklst[index+1])
        elif('as' in chunklst[0]):
            postitle.append(chunklst[1])
        if(postitle != []):
            postitle = self.detectstopwords(postitle)
            postitle = self.prprnounpos(postitle)
            return postitle
    def prprocess(self,list_of_sent):
        corrsenbool = []
        for i in range(len(list_of_sent)):
            x = re.search("^As\\sa|an\\s.*\\sI want\\s.*\\sso that\\s.*", str(list_of_sent[i]))
            y = re.search("^As\\sa|an\\s[a-z]*\\sI want\\s[a-z]*\s.*",str(list_of_sent[i]))
            if x or y:
                corrsenbool.append(True)
            else:
                corrsenbool.append(False)
        if(False in corrsenbool):
            return self.Error_Handle_Sent(corrsenbool)
        else:
            return True

    def Error_Handle_Sent(self,boolist):
            sentenceerror=[]
            for i in range(len(boolist)):
                if(boolist[i] == False):
                    sentenceerror.append(i+1)
            return self.Error_Show(sentenceerror)
    def Error_Show(self,sentenceerror):
        errstr = ''
        if(len(sentenceerror)>1):
            for i in range(len(sentenceerror)):
                errstr = errstr+str(int(i+1))+', '
            errormsg = "Sentence of "+errstr+" position are not user story please correct them!"
            return errormsg
        else:
            errormsg = "Sentence of "+str(sentenceerror[0])+" position is not user story please correct them!"
            return errormsg
    def getsynomynlst(self,lst):
        synlst = list()
        for i in range(len(lst)):
            for synset in wordnet.synsets(lst[i]):
                for lemma in synset.lemmas():
                    synlst.append(lemma.name())    
        return synlst  
    def getcontrols(self,controlindex):
        string = controlindex
        lst = string.split(re.findall("^As a .+ I want",string)[0])
        firstsents, lastsents = '',''
        sents = lst[1]
        string2 = lst[1].strip()
        lst = re.search("((?!so that.*).)*",string2).group().strip()
    #     if('so that' in string):
    #         print(True)
        if(',' in lst):
            comma = lst.split(',')
            firstsents = comma[0].strip().rsplit(' ', 1)[0]
            desc = self.nlp(comma[0])
            comma[0] = desc[len(desc)-1].text
            endsent = comma[len(comma)-1]
            if("and" in endsent):
                endsent = endsent.strip()
                lst = endsent.strip().split("and")
                try:
                    endcont = lst[1].strip().split(' ', 1)[1]
                    lastsents = endcont
                except:
                    pass
                lst[1] = (lst[1].split())[0]
                comma.pop()
                for i in range(len(lst)):
                    comma.append(lst[i].strip())
        else:
            lst = (endsent.strip().split())[0]
            if(lst == ''):
                lastsents = endsent.strip().split(' ', 1)[1]

            comma.append(lst)
        return comma, firstsents, lastsents

    def verbchunk(self,string):
        matcher = Matcher(self.nlp.vocab)
        sentence = self.nlp(string)
        pattern =[
                [{'POS': 'VERB', 'OP': '?'},
                   {'POS': 'ADV', 'OP': '*'},
                   {'POS': 'VERB', 'OP': '+'}]
                     ]
        matcher.add('GRAMMAR', pattern)
        lst = [sentence[start:end] for _, start, end in matcher(sentence)]
        return lst
    def buttons_extraction(self,string):
        if("so that" in string):
            x = re.findall("so that.+",string)
            string   = x[0].replace("so that",'').strip()
            if(',' in string):
                lst = string.split(',')
                if('and' in lst[len(lst)-1] or 'or' in lst[len(lst)-1]):
                    lastindex = lst[len(lst)-1].split('and')
                    lst.pop()
                    for i in range(len(lastindex)):
                        lst.append(lastindex[i].strip())
                    buttonlst = self.verbchunk(string)
                    buttonlst = self.contains_punct(buttonlst)
                    return buttonlst
            else:
                textstr = self.nlp(string)
                lst = self.detectstopwords(textstr) 
                lstverb = self.verbchunk(string)
                lst.extend(lstverb)
                lst = self.contains_punct(lst)
                return lst
        else:
            print("no buttons or wrong placement of buttons in story")
    def contains_punct(self,buttonlst):
        for i in range(len(buttonlst)):
            if(type(buttonlst[i]) != str):
                buttonlst[i] = buttonlst[i].text
        buttonlst = [''.join(c for c in s if c not in string.punctuation) for s in buttonlst]
        buttonlst = [s for s in buttonlst if s]
        return buttonlst

    def find_title_of_project(self,sent):
        # If project title in Quotation Marks then return the title
        title = self.nlp(str(sent))
        matcher = Matcher(self.nlp.vocab)
        pattern = [
            [{'ORTH': '"'},
               {'OP': '*'},
               {'ORTH': '"'}]
        ]
        matcher.add('TEST', pattern)
        lst = [title[start:end] for _, start, end in matcher(title)]#generating the list of all the possible match of "TITLE"
        if(lst != []): #Checking if we find the 
            isquote = True
            finaltitle = re.findall('"([^"]*)"', str(lst[0])) #All words in " " in lst[0]
            if(len(finaltitle) == 1): #checking list must contain only one title
                return finaltitle[0]
        #end Quotation marks

        else:
            #Try to catch Proper Noun 
            lst = []
            tempstr = ''
            concat = False
            propernountitlelst= []
            for ent in title.ents:
                lst.append(ent)
            for postagsent in title.sents:
                for token in postagsent:
                    if(token.pos_ == 'PROPN'):
                        concat = True
                        tempstr = tempstr + str(token) + ' '
                    else:
                        concat = False
                        if(tempstr != ''):
                            propernountitlelst.append(tempstr.strip())
            if(len(lst)==len(propernountitlelst) and (lst !=[] and propernountitlelst !=[])): 
                if(len(lst[0])>len(propernountitlelst[0])): #If sales propernoun and  entties lst matches then return
                    return lst[0]
                else:
                    return propernountitlelst[0]
            elif(propernountitlelst != [] and len(propernountitlelst) == 1): #If dont matches then return propernoun index at 0
                return propernountitlelst[0] #given that there is only one proper noun
            else:
                #If not any proper noun found then work on noun
                chunklst,notstop = [],[] #nounchunklst 
                chunkstr,title = '','' 
                txt = str(sent) 
                desc = self.nlp(txt)
                for chunk in desc.noun_chunks:
                    chunklst.append(chunk.text)  #Generating noun chunk list

                for i in range(len(chunklst)):
                    chunkstr = chunkstr + chunklst[i]+' ' #concating all chunklst noun to get possible title

                desc = self.nlp(chunkstr)
                notstop = self.detectstopwords(desc) #now check 'chunkstr' if there is stopwords or not and get list of notstopwords
                stopstr = '' 
                for i in range(len(notstop)): #concat notstopwords list
                    stopstr = stopstr + notstop[i]+' '
                desc= self.nlp(txt)
                lst = [token.text for token in desc[0].rights] #detecting the stakeholder 'user'
                if(notstop[0] == lst[0]):
                    notstop.pop(0)
                titlewords =["name","title","call","entitle"]
                synlst = self.getsynomynlst(titlewords) #if above lst words in stopwords then pop then concat
                for i in range(len(notstop)):
                    if(len(notstop)>i):
                        if(notstop[i] in synlst):
                            notstop.pop(i)
                for i in range(len(notstop)):
                    title = title + notstop[i]+ ' '
                else:
                    return title



    def find_sents(self,doc):
        sentences = list(doc.sents)
        return sentences


class VisionStatement:
    def __init__(self, lst):
        self.nlp = spacy.load("en_core_web_sm")
        self.lst = self.find_sents(lst)
       
#         self.userstory = userstory
#         self.list_of_sents = self.find_sents(doc)
        self.errormsg = self.preprocess(self.lst)
        self.controloutput = {}
        self.output = {}
    def preprocess(self,lst):
        return True
    def find_sents(self,doc):
        lst= []
        if(type(doc) == str):
            doc = self.nlp(doc)
        sentences = list(doc.sents)
        for i in sentences:
            lst.append(i.text)
        return lst
            
    def main(self):
        screentitle = {}
        controlsdic = {}
        buttondic = {}
       
     
        for i in range(len(self.lst)):
            controlst = list(self.controls(self.lst[i]))
        #     print('Controls: ',controls)
            btnlst = self.buttons_extraction(str(controlst[1]))
        #     print('Buttons: ',btnlst)
            if(type(btnlst) == list):
                buttondic['Screen'+str(int(i+1))] = [s.strip() for s in btnlst]
            screentitle['Screen'+str(int(i+1))] = self.screen_title_detection(self.lst[i])            
            controlsdic['Screen'+str(int(i+1))] = [s.strip() for s in controlst[0]]
            a = WordBank(self.detectstopwordsfromlist([s.strip() for s in controlst[0]]))
            controltitle = a.get_controls()
            self.controloutput['Screen'+str(int(i+1))] = controltitle
        titleOfProject = self.projecttitle(self.lst[0])
        self.output['TITLE'] = titleOfProject
        self.output['SCREENS'] = screentitle
        self.output['CONTROLS'] = controlsdic
        self.output['BUTTONS'] = buttondic
        self.output['NOOFSCREENS'] = len(self.lst)
        print(self.output,self.controloutput)
        return self.output,self.controloutput
    
    def detectstopwordsfromlist(self,controls):
        for i in range(len(controls)):
            tempstr  = ""
            nlpstr = self.nlp(controls[i])
            for token in nlpstr:
                if not token.is_stop:
                    tempstr = tempstr + token.text+' '
                if(tempstr != ""):
                    controls[i] = tempstr
            nlpstr = self.nlp(controls[i])
            tempstr  = ""
            for chunk in nlpstr.noun_chunks:
                tempstr = tempstr + chunk.text + ' '
        return controls
    def getsynomynlst(self,lst):
        synlst = list()
        for i in range(len(lst)):
            for synset in wordnet.synsets(lst[i]):
                for lemma in synset.lemmas():
                    synlst.append(lemma.name())
        return synlst

    def find_title_of_project(self,sent):
          # If project title in Quotation Marks then return the title
            nlp = spacy.load("en_core_web_sm")
            title = self.nlp(str(sent))
            matcher = Matcher(self.nlp.vocab)
            pattern = [
                [{'ORTH': '"'},
                 {'OP': '*'},
                 {'ORTH': '"'}]
            ]
            matcher.add('TEST', pattern)
            lst = [title[start:end] for _, start, end in matcher(title)]  # generating the list of all the possible match of "TITLE"
            if(lst != []):  # Checking if we find the
                isquote = True
                finaltitle = re.findall('"([^"]*)"', str(lst[0]))  # All words in " " in lst[0]
                if(len(finaltitle) == 1):  # checking list must contain only one title
                    return finaltitle[0]
            # end Quotation marks

            else:
                # Try to catch Proper Noun
                lst = []
                tempstr = ''
                concat = False
                propernountitlelst = []
                for ent in title.ents:
                    lst.append(ent)
                for postagsent in title.sents:
                    for token in postagsent:
                        if(token.pos_ == 'PROPN'):
                            concat = True
                            tempstr = tempstr + str(token) + ' '
                        else:
                            concat = False
                            if(tempstr != ''):
                                propernountitlelst.append(tempstr.strip())
                if(len(lst) == len(propernountitlelst) and (lst !=[] and propernountitlelst !=[])): 
                    if(len(lst[0]) > len(propernountitlelst[0])): #If sales propernoun and  entties lst matches then return
                        return lst[0]
                    else:
                        return propernountitlelst[0]
                elif(propernountitlelst != [] and len(propernountitlelst) == 1):  # If dont matches then return propernoun index at 0
                    return propernountitlelst[0]  # given that there is only one proper noun
                else:
                    # If not any proper noun found then work on noun
                    chunklst, notstop = [], [] #nounchunklst 
                    chunkstr, title = '', '' 
                    nlp = spacy.load("en_core_web_sm")
                    txt = str(sent)
                    desc = self.nlp(txt)
                    for chunk in desc.noun_chunks:
                        chunklst.append(chunk.text)  # Generating noun chunk list

                    for i in range(len(chunklst)):
                        chunkstr = chunkstr + chunklst[i]+' '  # concating all chunklst noun to get possible title

                    desc = self.nlp(chunkstr)
                    notstop = self.detectstopwords(desc)  # now check 'chunkstr' if there is stopwords or not and get list of notstopwords

                    stopstr = ''
                    for i in range(len(notstop)):  # concat notstopwords list
                        stopstr = stopstr + notstop[i]+' '
                    desc = self.nlp(txt)
                    titlewords = ["name", "title","call","entitle"]
                    synlst = self.getsynomynlst(titlewords)  # if above lst words in stopwords then pop then concat
                    for i in range(len(notstop)):
                        if(len(notstop) > i):
                            if(notstop[i] in synlst):
                                notstop.pop(i)
                    for i in range(len(notstop)):
                        title = title + notstop[i]
                    else:
                        return title

    def detectstopwords(self,string):
        stopwords = ""
        if(type(string) == list):
            for i in range(len(string)):
                tempstrnlp = self.nlp(string[i].strip())
                tempstr = ""
                for token in tempstrnlp:
                    if not token.is_stop:

                        tempstr = tempstr + token.text+' '
                if(string != ""):
                    string[i] = tempstr.strip()
                    return string
        else:
    
            for token in string:
                if not token.is_stop:
                    stopwords = stopwords + token.text + " "

            return stopwords

    def nounchunklist(self,firstsent):
            chunklst = []
            if(type(firstsent) == str):
                desc = self.nlp(firstsent)
                for i in desc.noun_chunks:

                    chunklst.append(i.text)
                if(chunklst != []):
                    return chunklst
            elif(type(firstsent) == list):
            #             print(firstsent)
                firstsent = firstsent.split(',')

            matcher = Matcher(nlp.vocab)
            sentence = self.nlp(string)
            pattern = [
                [{'POS': 'VERB', 'OP': '?'},
                {'POS': 'ADV', 'OP': '*'},
                {'POS': 'VERB', 'OP': '+'}]
            ]
            matcher.add('GRAMMAR', pattern)
            lst = [sentence[start:end] for _, start, end in matcher(sentence)]
            return lst

    def projecttitle(self,userstory):
        screen_title = self.detectstopwords(self.nlp(self.nounchunklist(re.findall("who need (.*?),", userstory)[0])[0]))
        project_title1 = self.detectstopwords(self.nounchunklist(re.findall(",(.*?)that", userstory)[0]))
        project_title2 = self.find_title_of_project(re.findall(",(.*?)that", userstory)[0])

        try:
            project_title2.index(project_title1[0])
        except ValueError:
            return project_title2
        else:
            return project_title1[0]
    def is_empty_index(self,lst):
        new = []
        for i in lst:
            if(i != ""):
                new.append(i)
        return new

    def token_lst_to_str(self,lst):
        new = []
        for i in lst:
            if(type(i) != str):
                if(i.text != ""):
                    new.append(i.text)
            else:
                new.append(i)
        return new

    def screen_title_detection(self,userstory):
        screen_title = self.detectstopwords(
            self.nlp(self.nounchunklist(re.findall("who need (.*?),", userstory)[0])[0]))
        return screen_title

    def contains_punct(buttonlst):
        print(buttonlst)
        print(type(buttonlst))

        lst = []
        if(', ' in buttonlst):
            pass

    def controls(self,userstory):
        found = False
        string = self.nlp(re.findall("that.*", userstory)[0])
        original =  ["details", "providing", "giving","description","title",'need']
        lstsynomy = self.getsynomynlst(original)
        regexstr = ""

    #     first occurance of any orignial synmony list in the sentance after the 'that' clause
        for item in string:
            for i in lstsynomy:
                if item.lemma_ == i:
                    print(item.lemma_)
                    found = True
                    break
            regexstr = regexstr + item.text + ' '
            if(found == True):
                break
        regexlst = re.findall(('(?<={0}).*so that'.format(str(regexstr))), string.text)
        control_list = self.nounchunklist(regexlst[0])
        buttonregex = re.findall(('(?<={0})(.*)'.format(str(regexlst))), string.text)[0]
        print(self.is_empty_index(self.detectstopwords(control_list)), buttonregex)
        return self.is_empty_index(self.detectstopwords(control_list)), buttonregex

    def onelist(self,lst):
        new = []
        for item in itertools.chain.from_iterable(lst):
            new.append(item)
        return new
    def verbchunk(self,string):
        matcher = Matcher(self.nlp.vocab)
        sentence = self.nlp(string)
        pattern =[
                [{'POS': 'VERB', 'OP': '?'},
                {'POS': 'ADV', 'OP': '*'},
                {'POS': 'VERB', 'OP': '+'}]
                    ]
        matcher.add('GRAMMAR', pattern)
        lst = [sentence[start:end] for _, start, end in matcher(sentence)]
        return lst
    def buttons_extraction(self,string):

        if("so that" in string):
            buttonlist = []
            x = string.split('so that')[1].strip()

            stop = self.detectstopwords(self.nlp(x))

            verb = self.verbchunk(x)
            if(verb != [] or verb != ""):
                buttonlist.append(self.token_lst_to_str(verb))

            title = self.nlp(str(x))
            matcher = Matcher(self.nlp.vocab)
            pattern = [{'POS': 'VERB'},
                       {'POS': 'NOUN'}]
            matcher.add('TEST1', [pattern])
            matcherlst = [title[start:end] for _, start, end in matcher(title)]
            if(matcherlst == []):

                title = self.nlp(str(stop))
                matcher = Matcher(self.nlp.vocab)
                pattern = [{'POS': 'NOUN'},
                           {'POS': 'NOUN'}]
                matcher.add('TEST2', [pattern])
                matcherlst = [title[start:end]
                              for _, start, end in matcher(title)]
                buttonlist.append(self.token_lst_to_str(matcherlst))
            else:
                buttonlist.append(self.token_lst_to_str(matcherlst))

            return self.onelist(buttonlist)

        else:
            print("no buttons or wrong placement of buttons in story")








class WireFrame:
    def __init__(self,screendetails,controlnames):
        self.screendetails = screendetails
        self.controlnames = controlnames
        print(self.screendetails)
        print(self.controlnames)

        

        self.start = """<!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Bootstrap demo</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
        </head>
        <body>
            <div class="container">
            """

    def main(self):
        for screen in self.controlnames:
            content = ""
            screencontrols = self.controlnames[screen]

            for i in screencontrols:

                if(i == 'TextBoxes'):
                    content = content+'<div id="textboxes">'
                    for j in screencontrols["TextBoxes"]:
                        content = content + '<input class="form-control" type="text"  placeholder="'+j+'"> <br>\n'
                    content = content + '</div>'
                if(i == 'ComboBoxes'):
                    content = content+'<div id="combo">'
                    for j in screencontrols["ComboBoxes"]:
                        content = content + '<input class="form-control" tyoe="select" placeholder="'+j+'"> <br>\n'
                    content = content + '</div>'
                if(i == 'RadioButtons'):
                    content = content+'<div id="radio">'
                    for j in screencontrols["RadioButtons"]:
                        content = content + '<input class="form-check-input" type="radio" name=' + \
                            j+' id='+j+'> <label class="form-check-label">'+j+'</label>\n '
                    content = content + '</div>'
                if(i == 'CheckBoxes'):
                    content = content+'<div id="check">'
                    for j in screencontrols["CheckBoxes"]:
                        content = content + '<input class="form-check-input" type="checkbox" value="" id=' + \
                            j+'> <label class="form-check-label" for='+j+'> '+j+' </label>\n '
                    content = content + '</div>'
            print(self.screendetails)
            if(self.screendetails[screen]['buttons'] != None):
                content = content+'<div id="buttons">'
                for j in self.screendetails[screen]['buttons']:
                    content = content + '<button class="btn btn-primary">'+j+'</button>'
                content = content + '</div>\n'
            content = content + """\n </div>\n<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
        </body>
        </html>"""
            file = open(''+screen+'.html',"w")
            file.write(self.start+content)
            file.close()
        return True
   
