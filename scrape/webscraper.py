import re, requests, sys, argparse

# create class to find regexp
class RegEx:
    def __init__(self,pattern,desc):
        self.pattern = pattern
        self.desc = desc

# pass patterns and description to class
rgxEmail = RegEx(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+','Emails')
rgxPhone = RegEx(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b','Phone')
rgxIP = RegEx(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b','IP Addresses')
rgxWord = RegEx(r'[a-zA-Z]+','Words')

# method to scrape websites
def scrapeURL(url,rgx):
    try:
        src = requests.get(url.strip())
        for rg in rgx:
            print('[*] Scraping ' + rg.desc + ' from ' + url.strip())
            res = set(re.findall(rg.pattern, src.text, re.I))
            for dat in res:
                print(dat)
    except Exception as err:
        print (str(err))

# method to import from text file
def scrapeFILE(fle,rgx):
    try:
        with open(fle) as fh:
            for url in fh:
                scrapeURL(url, rgx)
    except Exception as err:
        print(str(err))

# main method
def main(args):
    rgx = []
    isFile = True

    if args.input.lower().startswith('http'):
        isFile = False
    if args.scrape.lower() == 'e':
        rgx = [rgxEmail]
    elif args.scrape.lower() == 'p':
        rgx = [rgxPhone]
    elif args.scrape.lower() == 'i':
        rgx = [rgxIP]
    elif args.scrape.lower() == 'w':
        rgx = [rgxWord]
    elif args.scrape.lower() == 'a':
        rgx = [rgxEmail,rgxPhone,rgxIP,rgxWord]

    if isFile:
        scrapeFILE(args.input,rgx)
    else:
        scrapeURL(args.input,rgx)

    print('============================')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input',action='store',type=str,help='The URL or File to scrape')
    parser.add_argument('scrape',action='store',type=str,nargs='?',default='a',
        help='e = email, p = phone, i = ips, w = words, a = all')

    if len(sys.argv[2:])==0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)

