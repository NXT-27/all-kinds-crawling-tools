import requests 
from lxml import etree

#### requirements: 
##  python: 3.6.5
##  pip install requests=2.23.0
##  pip install lxml==4.5.0

def set_header(url, user_agent):

    headers = {"User-Agent": user_agent}
    try:
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            return req.text.encode('utf8')
        else:
            return ''
    except Exception as e:
        print(e)




def crawl_paper_nips(conference_name, conference_year, keyword, file_path):

    f = open(file_path, 'w')
    print('--------------------')
    print(f'Conference name: {conference_name}')
    print(f'Conference year: {conference_year}')
    print(f'Keyword: {keyword}')
    print(f'Save path: {file_path}')
    print('Start crawling......')
    print('--------------------\n')


    f.write('--------------------\n')
    f.write(f'Conference name: {conference_name}\n')
    f.write(f'Conference year: {conference_year}\n')
    f.write(f'Keyword: {keyword}\n')
    f.write('--------------------\n\n')


    user_agent = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/65.0.3325.181 Safari/537.36'

    url = 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-'+conference_year
    html = set_header(url,user_agent)
    selector = etree.HTML(html)
    name_list = []
    pdf_list = []
    index = 0

    for paper in selector.xpath('//ul/li/a'):
        paper_title = paper.text
        paper_href = paper.get('href')
        if paper_href.find('paper')>0 and paper_title!=None:
            if keyword==None or paper_title.lower().find(keyword.lower())>0:
                index += 1
                print(f'Index: {index} | Title: {paper_title}')
                f.write('==============\n')
                f.write('['+str(index)+']\n')
                f.write('Title: '+paper_title+'\n\n')
                
                paper_href = 'https://papers.nips.cc'+paper_href
                sub_html = set_header(paper_href,user_agent)
                sub_selector = etree.HTML(sub_html)

                try:
                    for paper_abstract in sub_selector.xpath('//p[@class="abstract"]/text()'):
                        f.write('Abstract: '+paper_abstract+'\n\n')
                except Exception as e:
                    f.write('no abstract\n')

                paper_pdfhref = paper_href+'.pdf'
                f.write('PDF Link: '+paper_pdfhref+'\n\n')

    f.write('\n\n\n')




def crawl_paper_cv(conference_name, conference_year, keyword, file_path):

    f = open(file_path, 'w')    
    print('--------------------')
    print(f'Conference name: {conference_name}')
    print(f'Conference year: {conference_year}')
    print(f'Keyword: {keyword}')
    print(f'Save path: {file_path}')
    print('Start crawling......')
    print('--------------------\n')


    f.write('--------------------\n')
    f.write(f'Conference name: {conference_name}\n')
    f.write(f'Conference year: {conference_year}\n')
    f.write(f'Keyword: {keyword}\n')
    f.write('--------------------\n\n')


    user_agent = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/65.0.3325.181 Safari/537.36'
    url = 'http://openaccess.thecvf.com/'+conference_name+conference_year+'.py#'
    html = set_header(url,user_agent)
    selector = etree.HTML(html)
    name_list = []
    pdf_list = []

    index = 0
    for paper in selector.xpath('//dt[@class="ptitle"]/a'):
        paper_title = paper.text


        if keyword==None or paper_title.lower().find(keyword.lower())>0:
            index += 1

            paper_href = "http://openaccess.thecvf.com/"+paper.get('href')
            sub_html = set_header(paper_href,user_agent)
            sub_selector = etree.HTML(sub_html)

            print(f'Index: {index} | Title: {paper_title}')

            f.write('==============\n')
            f.write('['+str(index)+']\n')
            f.write('Title: '+paper_title+'\n\n')

            try:
                for paper_abstract in sub_selector.xpath('//*[@id="abstract"]/text()'):
                    paper_abstract = paper_abstract.replace('\n','')
                    paper_abstract = paper_abstract.replace('\t','')
                    f.write('Abstract: '+paper_abstract+'\n\n')
            except:
                f.write('no abstract\n')

            try:
                i = 0
                for pdf in sub_selector.xpath('//*[@id="content"]/dl/dd/a/@href'):
                    i += 1
                    if i>1:
                        break
                    pdf = pdf[pdf.rfind('/')+1:]
                    if conference_name=='CVPR' and conference_year=='2018':
                        href = "http://openaccess.thecvf.com/content_"+conference_name.lower()+"_"+conference_year+"/papers/"
                    else:
                        href = "http://openaccess.thecvf.com/content_"+conference_name+"_"+conference_year+"/papers/"
                    paper_pdfhref = href+pdf
                    f.write('PDF Link: '+paper_pdfhref+'\n\n')
            except Exception as e:
                f.write('no pdf\n')
            f.write('\n\n\n')



if __name__ == "__main__":

    conference_name='NIPS'
    conference_year='2016'
    keyword = '3d'
    if keyword== None:
        save_name = conference_name+'_'+conference_year+'_nokeyword'
    else:
        save_name= conference_name+'_'+conference_year+'_'+keyword
    file_path = '/root/path/'+save_name+'.txt'

    if conference_name !='NIPS':
        crawl_paper_cv(conference_name, conference_year, keyword, file_path)
    else:
        crawl_paper_nips(conference_name, conference_year, keyword, file_path)

    