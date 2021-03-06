#icsファイルによるカレンダーのインポートあり版

import re
import datetime

boshu_start_str = '20180701'
boshu_end_str = '20180731'

boshu_start = datetime.datetime.strptime(boshu_start_str, "%Y%m%d")
boshu_end = datetime.datetime.strptime(boshu_end_str, "%Y%m%d")

file_name1 = 'Kyokosan_copy.ics'
file_name2 = 'Godaisan.ics'

class Ikkokukan():
    def __init__(self):
        self.free_set = set() #暇な日を格納するset
        self.isogashi_set = set() #忙しい日を格納するset
        self.isEnd = False
        
    def schedule_free_add(self,date):
        self.free_set.add(date)

    def schedule_isogashi_add(self,date):
        self.isogashi_set.add(date)

    def schedule_free_show(self):
        print(self.free_set)

    def schedule_isogashi_show(self):
        print(self.isogashi_set)

#インスタンス作成
kyokosan = Ikkokukan()
godaisan = Ikkokukan()
soichirosan = Ikkokukan()
everyone = Ikkokukan()

#フラグ
isMatch = False
inviteEnd = False
marry = False

#ループ変数
day = 1

#icsファイルを開く
path_kyoko = file_name1
path_godai = file_name2


calc_date = boshu_start
while calc_date <= boshu_end:
    soichirosan.schedule_free_add(calc_date)
    calc_date = calc_date + datetime.timedelta(days=1)


#響子さんのカレンダー読み込み
with open(path_kyoko) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]

l_DTSTART = [line for line in lines_strip if 'DTSTART' in line]
l_DTEND = [line for line in lines_strip if 'DTEND' in line]
i=0
while i < len(l_DTSTART):
    #予定開始日
    matchObj_start = re.search(r'[0-9]{8}', l_DTSTART[i])
    #日付型に変換
    date_formatted_start = datetime.datetime.strptime(matchObj_start.group(), "%Y%m%d")
    #print("start: ", end="")
    #print(date_formatted_start.date())

    #予定終了日
    matchObj_end = re.search(r'[0-9]{8}', l_DTEND[i])
    #日付型に変換
    date_formatted_end = datetime.datetime.strptime(matchObj_end.group(), "%Y%m%d")
    #print('end  : ', end="")
    #print(date_formatted_end.date())

    #予定のある日を計算
    calc_date = date_formatted_start
    while calc_date < date_formatted_end:
        kyokosan.schedule_isogashi_add(calc_date)
        calc_date = calc_date + datetime.timedelta(days=1)

    i += 1


#五代さんのカレンダー読み込み
with open(path_godai) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]

l_DTSTART = [line for line in lines_strip if 'DTSTART' in line]
l_DTEND = [line for line in lines_strip if 'DTEND' in line]
i=0
while i < len(l_DTSTART):
    #予定開始日
    matchObj_start = re.search(r'[0-9]{8}', l_DTSTART[i])
    #日付型に変換
    date_formatted_start = datetime.datetime.strptime(matchObj_start.group(), "%Y%m%d")
    #print("start: ", end="")
    #print(date_formatted_start.date())

    #予定終了日
    matchObj_end = re.search(r'[0-9]{8}', l_DTEND[i])
    #日付型に変換
    date_formatted_end = datetime.datetime.strptime(matchObj_end.group(), "%Y%m%d")
    #print('end  : ', end="")
    #print(date_formatted_end.date())

    #予定のある日を計算
    calc_date = date_formatted_start
    while calc_date < date_formatted_end:
        godaisan.schedule_isogashi_add(calc_date)
        calc_date = calc_date + datetime.timedelta(days=1)

    i += 1

#忙しい日リストから暇な日リストを作る
everyone.isogashi_set = kyokosan.isogashi_set | godaisan.isogashi_set
#print(everyone.isogashi_set)
#print(len(everyone.isogashi_set))
everyone.free_set = soichirosan.free_set - everyone.isogashi_set
print(everyone.free_set)

'''
while boshu_start.date() < boshu_end.date():
    tmp = boshu_start
    while tmp.date() < boshu_end.date()
        if tmp.date() not in kyokosan.isogashi_set[0].date():
            kyokosan.free_set.append(boshu_start)
        #todo:五代さんの分も
        tmp = tmp + datetime.timedelta(days=1)
    boshu_start = boshu_start + datetime.timedelta(days=1)
'''

'''
print("響子さんの忙しい日is:")
kyokosan.schedule_isogashi_show()
print("惣一郎さんが暇な日日is:")
soichirosan.schedule_free_show()
print("響子さんの空いてる日is:")
kyokosan.schedule_free_show()
'''

'''
#暇な日print
print("響子さんの空いてる日is:")
kyokosan.schedule_free_show()
print("五代さんの空いてる日is:")
godaisan.schedule_free_show()


#暇な日マッチング
matched_set = set()
for kyoko in kyokosan.free_set:
    for godai in godaisan.free_set:
        if kyoko == godai:
            matched_set.append(kyoko)
            isMatch = True

#マッチする日があった場合
if isMatch:
    sorted_set = set(set(matched_set))
    sorted_set.sort()
    print(" 二人の空いてる日is:")
    print(sorted_set)
    while inviteEnd == False:
        print("招待する日を選択してください:")
        inviteDay = input()
        if int(inviteDay) in sorted_set:
            print(inviteDay + "日に招待を送りました!!!!!!!!")
            inviteEnd = True
        else:
            print(inviteDay + "日は予定があるみたいです...")

#マッチする日がなかった場合
else:
    print("来月は頑張ってください...")
    
'''