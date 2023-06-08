import pytesseract
import datetime
import os
import time
import concurrent.futures
from pprint import pprint

#example file names
'0_33_59_880__0_34_00_839_00522.jpeg'
'0_35_00_040__0_35_00_519_00112.jpeg'

# only read images with this extension.
ext = '.jpeg'

# path with images to read.
path = os.getcwd()

# name of the srt file to create
subname = 'Generated subtitles.srt'

# language of the subtitles
sublang = 'chi_sim'
#sublang = 'eng'

# Shows the minimum confidence in the sentence
showMinimumConfidence = True

#example output showMinimumConfidence False
"""1
00:02:04,334 --> 00:02:06,709
I left the village when I was thirteen."""

#example output showMinimumConfidence True
"""1
00:02:04,334 --> 00:02:06,709
(72%)
I left the village when I was thirteen."""

# If you think grammatical characters or spaces are missing from your subs
# check the text_fixer, either modify it to your needs or bypass it.

startTime = 0

def gather_subs_tp(path, showConfidence=True, debug=False):
    global startTime
    startTime = int(time.time())
    op = []
    count = 0
    namelist = []         
    for root, dirs, files in os.walk(path):
        for name in files:
            if ext in name:
                namelist.append(name)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for name, result in zip(namelist, executor.map(vcheck, namelist)):
            if debug >= 1: print('Time Elapsed:',
                                  str(int(time.time())-startTime),
                                  'secs. Image:', count, 'Name:',name,
                                  'minconf:', result['minconf'],
                                  'text:', result['text'])
            try:
                times, start = fn2time(name, debug)
                if result['text'] == '': raise ValueError
                if showConfidence:
                    text = '({1}%)\n{0}'.format(result['text'],
                                                result['minconf'])
                else:
                    text = result['text']
                op.append((start, times, text))
                count+=1
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print(f'Did not run on: {name}')
    return op

def gather_subs_pp(path, debug=False):
    global startTime
    startTime = int(time.time())
    op = []
    count = 0
    namelist = []         
    for root, dirs, files in os.walk(path):
        for name in files:
            if ext in name:
                namelist.append(name)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for name, result in zip(namelist, executor.map(vcheck, namelist)):
            try:
                if debug >= 1: print('Time Elapsed:',
                                      str(int(time.time())-startTime),
                                     'secs. Image:', count, 'Name:',name,
                                     'minconf:', result['minconf'],
                                     'text', result['text'])
                times, start = fn2time(name, debug)
                text = '({1}%)\n{0}'.format(result['text'], result['minconf'])
                op.append((start, times, text))
                count+=1
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print('Did not run on: ', i)
            
    return op

def check(name, lang=sublang, debug=False):
    config = ("-l {} --oem 1 --psm 7".format(lang))
    text = pytesseract.image_to_string(name, config=config)
    return text

def check1(name, lang=sublang, debug=False):
    config = ("-l {} --oem 1 --psm 7".format(lang))
    text = pytesseract.image_to_data(name, config=config).split('\n')
    op = []
    for i in text:
        sp = i.split('\t')
        op.append(sp[-2:])
    return op

def vcheck(name, lang=sublang, debug=False):
    config  = ("-l {} --oem 1 --psm 7".format(lang))
    result  =  pytesseract.image_to_data(name, config=config).split('\n')[1:]
    minconf = 100
    text    = ''
    for i in result:
        sp = i.split('\t')
        t = sp[-1]
        t = text_fixer(t)
        if not t == '':
            conf = int(sp[-2])
            if conf < minconf and not conf == -1:
                minconf = conf
            text = ''.join([text,t])
    return {'text': text, 'minconf': minconf}

def text_fixer(text, debug=False):
    replaceMe = ['\n', '“', '”', '、', '//', ';', '<',
                 '>', '-', '_', '=', '+', '*', '&', '^',
                 '%', '#','@', '$', '.', '.', '~', ' ', '\t']
    stripMe = [',', '，',':']
    for i in replaceMe:
        text = text.replace(i,'')
    for i in stripMe:
        text = text.strip(i)
    text = text.strip()
    return text

def list2str(t):
    return '{}:{}:{},{}'.format(*t)

def fn2time(istr, debug=False):
    pieces = istr.split('_')
    if not len(pieces) == 10:
        raise ValueError('{} Not a set of times, expected 10 elements, got {}'.format(
                         istr, len(pieces)))
    start = list2str(pieces[0:4])
    end   = list2str(pieces[5:9])
    return '{} --> {}'.format(start, end), list2time(pieces[0:4], debug)

def list2time(ilist, debug=False):
    if debug >=2: print(ilist)
    t = (int(i) for i in ilist)
    return datetime.time(*t)

def sort_subs(subs):
    return sorted(subs, key=lambda sub: sub[0])

def build_subs(subs, debug=False):
    op = ''
    for index, subgroup in enumerate(subs):
        if debug: print(index, subgroup, [type(i) for i in subgroup])
        op = '\n'.join([op, str(index+1), *subgroup[1:], ''])
    return op

def write_subs(path, subtext, debug=False):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(subtext)
    print('Finished writing: {}'.format(path))

if __name__ == '__main__':
    #pass
    write_subs(subname, build_subs(sort_subs(gather_subs_tp(path,
                                                            showMinimumConfidence,
                                                             debug=1)),
                                    debug=False))
    print(str(int(time.time())-startTime))
