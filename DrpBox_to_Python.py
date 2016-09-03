# -*- coding: utf-8 -*-
"""
Created on Sat Jan 09 17:12:48 2016

@author: Jigar Mehta
"""
import re
import dropbox
import pandas as pd
import os

# PDF Parsing
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import HTMLConverter
from pyPdf import PdfFileReader

def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 1 #is for all
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def edit(string):
        string= re.sub('<[^>]*>', '', string).replace('\n',' ')
        string=string.replace(id1.strip(),' ')
        string=string.replace(ftr.strip(),' ')
        string=string.replace(hdr.strip(),' ')
        string=string.replace('Page ','')
        string=string.replace('Page ','')
        string=string.replace('  ',' ')
        #string=string.replace("\x9",'')    
        string=string.replace('/span>1','')
        return string

fname = r'H:\GSU\Spring 16 courses\MK8710 - CRM\Harrah_s_Entertainment__Inc.pdf'
#fname=r'C:\Users\Jigar Mehta\Documents\Python Scripts\38.4.08_08_matos.pdf'
#fname= r'C:\Users\Jigar Mehta\Dropbox\Jigar\Data\Paper A&B\24.1.2_schultze.pdf'
o_pth=r'C:\Users\Jigar Mehta\Documents\Python Scripts'
for yr in range(2000,2008):
    path=r'C:\Users\Jigar Mehta\Desktop\gra\F_data'
    #fol=['Issue-35-1 March 2011',	'Issue-35-2 June 2011',	'Issue-35-3 September 2011',	'Issue-35-4 December 2011',	'Issue-36-1 March 2012',	'Issue-36-2 June 2012',	'Issue-36-3 September 2012',	'Issue-36-4 December 2012',	'Issue-37-1 March 2013',	'Issue-37-2 June 2013',	'Issue-37-3 September 2013',	'Issue-37-4 December 2013',	'Issue-38-1 March 2014',	'Issue-38-2 June 2014',	'Issue-38-3 September 2014',	'Issue-38-4 September 2014',	'Issue-39-1 March 2015',	'Issue-39-2 June 2015',	'Issue-39-3 September 2015',	'Issue-39-4 December 2015']
    year=2006
    fol=['March','June','September','December']
    stxt=[]
    for it in range(0,len(fol)):    
        path_n=path+'\\'+fol[it]+' '+str(year)+'\\'+'articles'
        for name in os.listdir(path_n):
            if not name.startswith('._'):
                fname=path_n+'\\'+name
                stxt.append(convert_pdf_to_html(fname))
    
    hdr=ftr=''
    page_cnt,	tbl_no,	fig_no,	cate,	ref_cnt,	titles,	keywords,	key_cnt,\
    	abstract,	p_id,	p_yr,	p_mon,	auth_cnt,intr1,conclu,full=[],	[],	[],	[],	[],	[],\
    	[],	[],	[],	[],	[],	[],	[], [],[],[]
    authors,city,country,eid,snr,auth_new,eid_new,coun,name1=[],[],[],[],[],[],[],[],[]
     
    a,i=0,0
    
    for it in range(0,len(fol)):
        path_n=path+'\\'+fol[it]+' '+str(year)+'\\'+'articles'
        for name in os.listdir(path_n):
            if not name.startswith('._'):
               
               fname=path_n+'\\'+name  
               name1.append(name)
               # -*- coding: utf-8 -*-
               pdf = PdfFileReader(open(fname,'rb'))
               page_cnt.append(pdf.getNumPages())
              
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
               cate.append(cat)
    #         
             
               r0=tit.index('">1')
               title=re.sub('<[^>]*>', '', tit[16:r0])
               title=title[:title.find('span')]
               title= title.replace('\n',' ')
               title=title.replace('\xe2\x80\x9d','')
               title=title.replace('\xe2\x80\x9c','')
               title=title.replace('<','')
               title= title.replace('  ',' ').strip()
               titles.append(title)
               i=i+1

m=o_pth+"\\"+str(year)+"tit_cat.csv"
#n=o_pth+"\\"+str(year)+"y.csv"
ab_ky=pd.DataFrame({'fname':name1,'Category':cate,'Title':titles})
ab_ky.to_csv(m)

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
                   keywords.append(key)
                   key_cnt.append(keyw_cnt)     
               except:
                   key=''
                   keywords.append(key)
                   key_cnt.append(keyw_cnt)    
                                  
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
               abstract.append(abs)
            i=i+1  
        
    m=o_pth+"\\"+str(yr)+"ab_ky.csv"
    n=o_pth+"\\"+str(yr)+"y.csv"
    ab_ky=pd.DataFrame({'fname':name1,'Pages_count':page_cnt,'keywords_count':key_cnt,'Abstract':abstract})
    ab_ky.to_csv(m)
    y=pd.DataFrame({'fname':name1,'keywords':keywords})
    y.to_csv(n)
           
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
               snr.append(asa)
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
           #print ftr
        i=i+1
#           try:
#               
#               intr=stxt[i][stxt[i].index('font-size:18px')+17:]
#               i1=intr.index('font-size:18px')
#           except ValueError:
#               try:
#                   intr=stxt[i][stxt[i].index('font-size:17px')+17:]
#                   i1=intr.index('font-size:17px')
#               except:
#                   intr=stxt[i][stxt[i].index('It has been more than 40 years')]
#           
#              
#               
#           #intr=intr.replace(kaat,'')
#           intr=intr.replace(ftr[2:],'')
#           intr=intr.replace(hdr,'')
#           intrb=intr
#            
#           intr=intr[12:i1+16]
#           intr=edit(intr)
#           
#           intr1.append(intr.strip())
#            
#           if a==0: #old
#               try:
#                   conc=stxt[i][stxt[i].index('font-size:18px">Conclusion'):]
#                   conc=conc[conc.index('font-size')+16:]
#               except:
#                   try:
#                       conc=stxt[i][stxt[i].index('font-size:17px">Conclusion'):]
#                       conc=conc[conc.index('font-size')+16:]
#                   except:
#                       try:
#                          conc=stxt[i][stxt[i].index('Summary and Conclusion'):]
#                          conc=conc[conc.index('font-size')+16:]
#                       except:
#                          try:
#                             conc=stxt[i][stxt[i].index('Concluding Remarks'):]
#                             conc=conc[conc.index('font-size')+16:]
#                          except:
#                              try:
#                                  conc=stxt[i][stxt[i].index('Discusssion and Conclusion'):]
#                                  conc=conc[conc.index('font-size')+16:]
#                              except:
#                                  conc=''
#                
#                
#           else: 
#               try:
#                   cas=intrb.find('font-size:17px">Conclusion')
#                   if cas==-1:
#                       cas=intrb.find('Discussion and Conclusion')
#                       if cas==-1:
#                            cas=intrb.find('font-size:18px">Conclusion')
#                            if cas==-1:
#                                cas=intrb.find('font-size:18px">Discussion and Conclusion')
#                                
#                   conc=intrb[cas:]
#                   #rem_txt=intr[i1+16:cas+16]
#                   conc=conc[conc.index('font-size:13px')+16:]
#                   if conc.find('Acknowledgments')==-1:
#                       if i==14:
#                           l1= conc.find('font-size:13px">References')
#                       else:
#                           l1= conc.find('font-size:15px">References')
#                   else:
#                       l1= conc.find('Acknowledgments')
#                   conc=conc[:l1]
#                            
#               except ValueError:
#                  
#                   well=intrb.find('Limitations and Future')
#                   if well==-1:                            
#                       #rem_txt=intr[i1+16:intrb.index('font-size:15px">References')]
#                       conc=''
#                       print("No Conclusion")
#                       print i
#                   else:
#                       conc=intrb[well:]
#                       #rem_txt=intr[i1+16:well+31]
#                       conc=conc[conc.index('font-size:13px')+16:]
#                       if conc.find('Acknowledgments')==-1:
#                           if i==14:
#                               l1= conc.find('font-size:13px">References')
#                           else:
#                               l1= conc.find('font-size:15px">References')
#                       else:
#                           l1= conc.find('Acknowledgments')
#                                         
#                       conc=conc[:l1]
#               conc=edit(conc)
#               conc=conc.replace(ftr[2:],'')
#               conc=conc.replace(hdr,'')
#               #rem_txt=edit(rem_txt)
#               #full.append(rem_txt)
#               conclu.append(conc.strip())
        i=i+1
print(fname)
len(p_id)      
z=pd.DataFrame({'paper_id' : p_id, 'fname':name1,'Pub_yr' : p_yr,'Pub_mon':p_mon,'category':cate,'title':titles,'Pages_count':page_cnt,'keywords_count':key_cnt,\
'Abstract':abstract,'author_count':auth_cnt,'tables':tbl_no,'figures':fig_no,'references':ref_cnt,'introduction':intr1,'conclusion':conclu})
z.to_csv('z.csv')
y=pd.DataFrame({'fname':name1,'keywords':keywords})
y.to_csv('y.csv')
snr_edit=pd.DataFrame({'paper_id' : p_id,'name':name1,'snr_edtr':snr})
snr_edit.to_csv("snr.csv")



auth=pd.DataFrame({'fname' :name1,'author':auth_new,'email':eid_new,'country':coun})
auth.to_csv('auth.csv')
i=0
text_file = open("Output1.txt", "w")
text_file.write(stxt[i])
text_file.close()
fname
    #print conc

f=open(a,'rb')
f.write(stxt[i])
f.close()

print i5


s='conclusion'
st=s[s.index('con'):]
print st
print intr1[5]

titles[52]