# Packages and modules

import re
import pandas as pd
import os

import subprocess
import os
import uuid

# PDF Parsing
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import HTMLConverter
from pyPdf import PdfFileReader

#################################################################################################################
#################################################################################################################
#################################################################################################################


# function to clean string

def edit(string):
    string= re.sub('<[^>]*>', '', string).replace('\n',' ')
    #string=string.replace(id1.strip(),' ')
    string=string.replace(ftr.strip(),' ')
    string=string.replace(hdr.strip(),' ')
    string=string.replace('Page ','')
    string=string.replace('Page ','')
    string=string.replace('  ',' ')
    string=string.replace("\xe2\x80",'')
    #string=string.replace("\x9",'')    
    string=string.replace('/span>1','')
    return string

# convert pdf to text to html with tags
def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0 # is for all (0: for all pages in pdf, 1=1 page, 2=2 pages, 3=3 pages, etc.)
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

#################################################################################################################
#################################################################################################################


year=2009           # change year
path=r'C:\Users\Jigar Mehta\Desktop\gra\F_data' # store all files and change path accordingly
fol=['March','June','September','December'] # this is fixed

stxt=[] # array to hold the entire html file, each element of stxt holds one complete article

# convert each file in the 2009 year and all 4 quarters 
for it in range(0,len(fol)):    
    path_n=path+'\\'+fol[it]+' '+str(year)+'\\'+'articles'
    for name in os.listdir(path_n):
        if not name.startswith('._'):
            fname=path_n+'\\'+name
            stxt.append(convert_pdf_to_html(fname))


# define  variables to hold metadata
hdr=ftr=''
page_cnt,	tbl_no,	fig_no,	cate,	ref_cnt,	titles,	keywords,	key_cnt,\
	abstract,	p_id,	p_yr,	p_mon,	auth_cnt,intr1,conclu,full=[],	[],	[],	[],	[],	[],\
	[],	[],	[],	[],	[],	[],	[], [],[],[]
authors,city,country,eid,snr,auth_new,eid_new,coun,name1=[],[],[],[],[],[],[],[],[]
 
# counter variable
i=0 # i points to each element of stxt and so, each pdf file in its html converted version

# a is flag variable. a=1 is for old pattern before 2011, a=0 for new pattern 2011 onwards
a=0

#################################################################################################################
#################################################################################################################


# main loop to extract metadata
for it in range(0,len(fol)):
    path_n=path+'\\'+fol[it]+' '+str(year)+'\\'+'articles' # dynamic path
    for name in os.listdir(path_n):
        if not name.startswith('._'): # for actual articles only
           
           fname=path_n+'\\'+name  
           name1.append(name) # attch actual file name in name1 array (file name can be used as primary key)
           pdf = PdfFileReader(open(fname,'rb'))
           page_cnt.append(pdf.getNumPages()) #get page counts and store in page_cnt array
           
           if a==1: # old
               cat=stxt[stxt[i].index('font-size:12px'):]
               c0 =cat.index('font-size:28px')
               tit =stxt[stxt[i].index('font-size:28px'):] 
           else: # new
               cat=stxt[i][stxt[i].find('font-size:12px'):]
               c0= cat.find('font-size:27px')   
               tit =stxt[i][stxt[i].find('font-size:27px'):]
               au=stxt[i][stxt[i].find('font-size:27px'):]
           cat=re.sub('<[^>]*>', '',cat[16:c0])
           cat=cat[:cat.index('<span')].strip()
           cat=cat.replace('Abstract','')
           cate.append(cat) ## store catgory of papers in cate array

#################################################################################################################
#################################################################################################################         
         
           r0=tit.index('">1')
           title=re.sub('<[^>]*>', '', tit[16:r0])
           title=title[:title.find('span')]
           title= title.replace('\n',' ')
           title=title.replace('\xe2\x80\x9d','')
           title=title.replace('\xe2\x80\x9c','')
           title=title.replace('<','')
           title= title.replace('  ',' ').strip()
           titles.append(title) # store title of paper in tit array
           
           # extract keywords and abstract
           r8=au.index('Italic')
           try:
               r1=au.index('Keywords')
               keyw=au[r1:]
               if  a==0: #old
                   keyw=keyw[keyw.index('font-size:13px">')+18:]
               else: #new
                    keyw=keyw[keyw.index('font-size:12px">')+18:]
               keyw=keyw[:keyw.index("</span>")]
               keyw=re.sub('<[^>]*>', '', keyw)
               keyw=keyw.replace('\n',' ')
               keyw=keyw.replace('  ',' ').strip()
               keyw_cnt=len(keyw.split(','))
               key=keyw.split(',')
               keywords.append(key)     # store actual keywords for each artcile in keywords array
               key_cnt.append(keyw_cnt)  # store number of keywords for each artcile in key_cnt array
           except:
               key=''
               keywords.append(key)         # store actual keywords for each artcile in keywords array
               key_cnt.append(keyw_cnt)     # store number of keywords for each artcile in key_cnt array
                              
           if a==0:# new
               r8=au.index('Italic')
               abs_t=au[r8+24:r1]
               abs=re.sub('<[^>]*>', '', abs_t)
           else:  #old
               r8=au.index('Abstract')
               abs_t=au[r8+8:r1]
               abs=re.sub('<[^>]*>', '', abs_t)
           abs= abs.replace('\n',' ')
           abs= str(abs.replace('  ',' ').strip())
           abs=abs.replace("Abstract",'').strip()
           abstract.append(abs) # store abstract for each artcile in abstract array

#################################################################################################################
#################################################################################################################

               
           ## store number of tables and number of figures in the articles in respective arrays: tbl_no, fig_no
           if a==0:   #new 
               tbl_no.append(stxt[i].count('Arial,Bold; font-size:13px">Table'))
               fig_no.append(stxt[i].count('Arial,Bold; font-size:13px">Figure'))
           else: # old
               tbl_no.append(stxt[i].count('Arial-BoldMT; font-size:13px">Table'))#old
               fig_no.append(stxt[i].count('Arial-BoldMT; font-size:13px">Figure'))#old
            
           ## store the number of references of paper in ref array
           try: 
               ref=au[au.index('font-size:15px">References'):au.index('About the Author')]
           except:
              try:
                  ref=au[au.index('font-size:13px">References'):au.index('About the Author')]
              except:
                   
                  ref=au[au.index('font-size:15px">References'):au.index('Author Biographies')]
                 
           if a==1:#new  
               ref_cnt.append(ref.count('left:72px')+ref.count('left:290px')+10)
           else:# new
               ref_cnt.append(ref.count('TimesNewRoman,Italic; font-size:11px')-10)
               
        # extract senior editor name  for special issue

#################################################################################################################
#################################################################################################################

               
           if 'SPEICAL ISSUE' in cate[i]:
               asa='SPECIAL ISSUE'
           else:
           
               asa=au[au.index("font-size:7px"):]
               kaat=asa[:au.index('font-size:13px">')+16]
               asa=asa[asa.index("font-size:10px")+16:]
               asa1=asa.find("senior")
               asa=asa[:asa1].strip()   
               asa=re.sub('<[^>]*>', '', asa)
               asa=asa.replace('\xc3\xa9',' ')
               asa.replace('\n','')
               asa.replace('1','')
               snr.append(asa) # store senior editor name in snr array
               
           ## extract publication year, month, paper_id number
           ## generate composite key --  another primary key; other primary key was actual filename in name1 array
               
           # p_id array contains paper_id, p_mon array contains publication quarter, p_yr array contains publication year
           # id array contains composite id
               
           try: 
               id1=au[au.index('senior'):]
          
               if a==1:
                   t_id=id1.index('Arial-Italic')+2     
               else:
                   t_id=id1.index('Arial,Italic')
               id1=id1[t_id+30:]
               id_b=id1[:2000]
               t_id=id1.index('<br>')
               id1=id1[:t_id]
              
               id=id1[:id1.index('/')].replace('\n',' ')
               id1=id1.replace('  ',' ')
               pub_yr=id1[id1.index('/')+1:]
               pub_mon=pub_yr.split()[0]
               pub_yr=pub_yr.split()[1]
               id_l=id.split('.')
               id="P_MISQ_"+id_l[1].split()[0]+"_"+id_l[2].split(',')[0].strip()+"_"+id_l[3].split('-')[0].strip()+"_"+id_l[3].split('-')[1]
               id=id.replace('p','')
               id=id.replace(' ','')            
               p_id.append(id)
               p_yr.append(pub_yr)
               p_mon.append(pub_mon)
                    
               hdr=id_b[id_b.index('Italic')+26:].strip()
               h2=hdr.index('<br>')
               hdr=hdr[:h2]
               #print hdr
                
               ftr=id+"/"+pub_mon+" "+pub_yr
           except:
               print "No ID"
               p_id.append('')
               p_yr.append('')
               p_mon.append('')
               

#################################################################################################################
#################################################################################################################
        

# This sections contains how to extract intoduction and conclusion
# introduction extraction is mostly accurate, conclusion is bit inaccuarte

           try:
               
               intr=stxt[i][stxt[i].index('font-size:18px')+17:]
               i1=intr.index('font-size:18px')
           except ValueError:
               try:
                   intr=stxt[i][stxt[i].index('font-size:17px')+17:]
                   i1=intr.index('font-size:17px')
               except:
                   intr=stxt[i][stxt[i].index('It has been more than 40 years')]
           
                         
           #intr=intr.replace(kaat,'')
           intr=intr.replace(ftr[2:],'') # replace footer
           intr=intr.replace(hdr,'') #replace header
           intrb=intr
            
           intr=intr[12:i1+16]
           intr=edit(intr)
           
           intr1.append(intr.strip()) # append introduction 
            
            
        ## conclusion extraction sucks !!! I am commenting as of now.
           if a==0: #old
               try:
                   conc=stxt[i][stxt[i].index('font-size:18px">Conclusion'):]
                   conc=conc[conc.index('font-size')+16:]
               except:
                   try:
                       conc=stxt[i][stxt[i].index('font-size:17px">Conclusion'):]
                       conc=conc[conc.index('font-size')+16:]
                   except:
                       try:
                          conc=stxt[i][stxt[i].index('Summary and Conclusion'):]
                          conc=conc[conc.index('font-size')+16:]
                       except:
                          try:
                             conc=stxt[i][stxt[i].index('Concluding Remarks'):]
                             conc=conc[conc.index('font-size')+16:]
                          except:
                              try:
                                  conc=stxt[i][stxt[i].index('Discusssion and Conclusion'):]
                                  conc=conc[conc.index('font-size')+16:]
                              except:
                                  conc=''
                
                
           else: 
               try:
                   cas=intrb.find('font-size:17px">Conclusion')
                   if cas==-1:
                       cas=intrb.find('Discussion and Conclusion')
                       if cas==-1:
                            cas=intrb.find('font-size:18px">Conclusion')
                            if cas==-1:
                                cas=intrb.find('font-size:18px">Discussion and Conclusion')
                                
                   conc=intrb[cas:]
                   #rem_txt=intr[i1+16:cas+16]
                   conc=conc[conc.index('font-size:13px')+16:]
                   if conc.find('Acknowledgments')==-1:
                       if i==14:
                           l1= conc.find('font-size:13px">References')
                       else:
                           l1= conc.find('font-size:15px">References')
                   else:
                       l1= conc.find('Acknowledgments')
                   conc=conc[:l1]
                            
               except ValueError:
                  
                   well=intrb.find('Limitations and Future')
                   if well==-1:                            
                       #rem_txt=intr[i1+16:intrb.index('font-size:15px">References')]
                       conc=''
                       print("No Conclusion")
                       print i
                   else:
                       conc=intrb[well:]
                       #rem_txt=intr[i1+16:well+31]
                       conc=conc[conc.index('font-size:13px')+16:]
                       if conc.find('Acknowledgments')==-1:
                           if i==14:
                               l1= conc.find('font-size:13px">References')
                           else:
                               l1= conc.find('font-size:15px">References')
                       else:
                           l1= conc.find('Acknowledgments')
                                         
                       conc=conc[:l1]
               conc=edit(conc)
               conc=conc.replace(ftr[2:],'')
               conc=conc.replace(hdr,'')
               #rem_txt=edit(rem_txt)
               #full.append(rem_txt)
               conclu.append(conc.strip())
        
#################################################################################################################
#################################################################################################################        
        
         # count of number of authors in pdf
           au_m=stxt[i][stxt[i].index('font-size:27px'):stxt[i].index("Italic")]
           au_cnt= au_m.count('font-size:13px')
           auth_cnt.append(au_cnt) # store number of authors in auth_cnt array
         
         # extract author name, email id, country
         #this piece of code  is not very accurate
         # requires manual work 
         
           txt=au_m
           emm=au_m
           authors,eid,country=[],[],[]
           for j in range(0,au_cnt):
                   
                   txt1=txt[txt.index('font-size:13px')+15:]
                   r3=txt1.index('<br>')
                   authors.append(txt1[1:r3])   
                   #print author1
                   a13=emm.find('{')+1
                   email=emm[a13:]
                   email=email[:email.find('}')]
                   eid.append(email)
                   try: 
                       a11=emm[a13-100:a13-1]
                       a12=a11.find('>')
                       a12=a11[a12+1:].strip()
                       a12=a12.split(' ,')
                       t1=a12[-1].split()[-1]
                       country.append(t1)
                   except IndexError as ieee:
                       t1=''
                       country.append(t1)
                   emm=txt[txt.find('}')+1:]
                   txt=txt1
           
           # attach author name, email id country in arrays
           auth_new.append(authors)
           eid_new.append(eid)
           coun.append(country)        
        
        # incremanet counter to access next article in the folder
        i=i+1


#################################################################################################################
################################################################################################################# 

# extarct to csv, edit the code as per the need: 


z=pd.DataFrame({'paper_id' : p_id, 'fname':name1,'Pub_yr' : p_yr,'Pub_mon':p_mon,'category':cate,'title':titles,'Pages_count':page_cnt,'keywords_count':key_cnt,\
'Abstract':abstract,'author_count':auth_cnt,'tables':tbl_no,'figures':fig_no,'references':ref_cnt,'introduction':intr1,'conclusion':conclu})
z.to_csv('z.csv')
y=pd.DataFrame({'fname':name1,'keywords':keywords})
y.to_csv('y.csv')
snr_edit=pd.DataFrame({'paper_id' : p_id,'name':name1,'snr_edtr':snr})
snr_edit.to_csv("snr.csv")
