#! /usr/bin/python3

from datetime import datetime
import requests
import re

# create header to let imbd know its a browser asking ;-)
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36" }

# list of shows we are interested in. TODO immortality nor working yet
shows = [{ "csi": "tt0247082"}, {"csi:immortality":"tt4688366"}, {"csi:miami": "tt0313043"}, {"csi:new york":"tt0395843"}]

# collect the data
alldata = []

# for each show in the list
for ser in shows:
    # get the title and the imdb code
    title = list(ser)[0]
    tt = ser[title]
    # for each series - up to 17, there isn't one the data returned won't have results we want
    for s in range(1,17):
        print(f"show: {title}, series {s}")
        # grab the data
        data = str(requests.get(f"https://www.imdb.com/title/{tt}/episodes/?season={s}", verify=True, headers=headers).content)
        # find all the episide cells in the html that are like S1.E3.... up to the < - regex could be better!
        eps = list(re.findall(f"S{s}\.E\d+[\\\\w a-zA-Z0-9.\'\-\$:,&;#\?^<]+", data))
        # chop off whaever that is and the ending <
        eps = [e[:-1].replace("\\xe2\\x88\\x99","").replace("&#x27;","'").replace("&amp;","&") for e in eps]
        # get the series and episode numbers as ints and add to the result
        eps = [
		[int(a) for a in re.split("[SE\.]",x.split(" ")[0]) if a]+[x] for x in eps
	]
        # grab all the broadcast dates, these are in span elements with that weird class
        bc = list(re.findall("sc-ccd6e31b-10 dYquTu\">[A-Za-z\s,0-9]*</span>", data))
        bc
        # add the show name, because its not captured other wise in the final results
        eps = [[title]+e for e in eps]
        bc = [b[b.index(">")+1:b.index("<")] for b in bc]
        # convert to a data YYYY/MM/DD so is readable and sortable
        bc2 = [datetime.strptime(b, "%a, %b %d, %Y").strftime("%Y/%m/%d") for b in bc]
        # extend the alldata  list by adding the new episodes at the end
        alldata.extend(list(zip(bc2, eps)))

# split the data into shows, sorted by S*100+E

show = []

for ser in shows:
    title = list(ser)[0]
    sh = sorted([a for a in alldata if a[1][0]==title])
    sh = sorted(sh, key=lambda s:s[1][1]*100+s[1][2])
    show.append(sh)


# alldata sorted 
alldata = sorted(alldata, key=lambda s:s[1][1]*100+s[1][2])

print("where the broadcast dates are out of order according to series order")

outof = []

for ss in range(len(show)):
    for d in range(len(show[ss])):
        if d>0:
            if show[ss][d][0]<show[ss][d-1][0]:
                print((d,show[ss][d-1],show[ss][d]))
                outof.extend(show[ss][d-1])

print()
print([o[3] for o in outof])
print()

def printout():
    print("| Date       | Show | Episode |Warning|")
    print("|-|-|-|-|")
    for e in sorted(alldata):
        print(f"|{e[0]} | {e[1][0]} | {e[1][3]} | {' *sequence*' if e[1][3] in [o[3] for o in outof] else ''}|")


printout()

print("if there are sequence warnings fix and rerun printout")
