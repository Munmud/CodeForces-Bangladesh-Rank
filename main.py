import codeforces_api
import os
import time


start_time = time.time()

contest_id = None
country = 'Bangladesh'
user_info_api_access_cnt = 0
fineName = None
f = None


try :
    contest_list = codeforces_api.CodeforcesApi().contest_list()
    print('Success getting contest_list')
    
    for x in contest_list:
        if (x.phase == 'FINISHED'):
            contest_id = x.id
            fileName = str(x.id) + ' ' + str(x.name) + '.txt'
            fileName = fileName.replace('#', '')
            if os.path.isfile( 'CF_Bangladesh_Rank/' + fileName ): continue
            else: break
except:
    print('Codeforces contest_list api not working')
    exit()

if (contest_id == None) :
    exit()

def go(ls):
    res = None
    cnt = user_info_api_access_cnt +1
    
    try:
        res = codeforces_api.CodeforcesApi().user_info(handles=ls)
        print('Success getting user_info #' + str(cnt))
        for x in res:
            if( x.country == country ):
                # poss = poss + 1
                # if (str(x.handle) == 'moontasir_ru'):
                #     moontasir_ru = poss
                print (x.handle, file=f)
        
    except Exception as e:
        # print(e)
        strr = str(e)
        strr = strr.removeprefix("('Request returned not OK status', 'FAILED', 'handles: User with handle ")
        strr = strr.removesuffix(" not found')")
        sz = len(ls)
        ls.remove(strr)
        if (sz-1 == len(ls)):
            print('Removed Ghost User ' + strr)
            go(ls)
        else :
            print('Ghost User not found')

r = None
try :
    r = codeforces_api.CodeforcesApi().contest_standings(contest_id=contest_id)
    print('Success getting contest standing')
except :
    print('Standing Api not Working')

try :
    f = open('CF_Bangladesh_Rank/' + fileName, 'w' )
    print('Successfully Created '+ fileName)
except :
    print('Cannot open file')
ls = []
for xx in r['rows']:
    for x in xx.party.members:
        han = str(x.handle)
        if len(ls) == 500 :
            go(ls)
            user_info_api_access_cnt+=1
            ls.clear()
        ls.append(han)

go(ls)
print('100% Ok in ' + fileName)
print("--- %s seconds ---" % (time.time() - start_time))

f.close()

fileName = 'CF_Bangladesh_Rank/' + fileName
print(fileName)
with open( fileName , 'r' ) as fi:
    poss = 0
    found = 0
    while True:
        poss += 1

        # Get next line from fi
        line = fi.readline()
        if not line:
            break
        line = str(line).strip()
        if (line == 'moontasir_ru'):
            print('Your position is ' + str(poss))
            found= 1
    if (found == 0): print("You didn't participated")



# if (moontasir_ru == -1): print("You didn't participated")
# else: print('your position is' + str(moontasir_ru))