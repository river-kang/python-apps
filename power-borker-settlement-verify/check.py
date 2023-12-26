prevTable = dict()
newTable = dict()

# new 의 마지막 row 이후 empty row 있으면 안됨
with open('new.txt', 'r') as file:
    line = file.readline()
    while line:
        row = line.split(',')
        if len(row) > 10:
            newTable[row[2]] = {
                '총액': row[21],  # total_amount 추출
                '발전소명': row[3],
                '검증발전량': row[7]
            }
        line = file.readline()
    file.close()
print(newTable)

# prev 의 마지막 row 이후 empty row 있으면 안됨
with open('prev.txt', 'r') as file:
    line = file.readline()
    while line:
        row = line.split('\t')
        if len(row) > 10:
            prevTable[row[1]] = {
                '총액': row[22].replace('\n', ''),
                '발전소명': row[2],
                '검증발전량': row[6]
            }
        line = file.readline()
    file.close()
print(prevTable)

# 체크 1. 정산에 빠지는 plant 가 있는지 확인
newKeySet = set(newTable.keys())
prevKeySet = set(prevTable.keys())

newKeySetOnly = newKeySet - prevKeySet
prevKeySetOnly = prevKeySet - newKeySet

print(f'기존 정산방식에만 포함된 것: {prevKeySetOnly}')
print(f'신규 어드민 정산에만 포함된 것: {newKeySetOnly}')


def table_format_output():
    print('거래소ID,발전소명,기존검증발전량,신규검증발전량,검증발전량차,기존총액,신규총액,총액차')
    for key, value in prevTable.items():
        if key in newTable:
            newValue = newTable[key]
            print(
                f'{key},{value["발전소명"]},{value["검증발전량"]},{newValue["검증발전량"]},{(int(value["검증발전량"]) - int(newValue["검증발전량"])) / int(newValue["검증발전량"])},{value["총액"]},{newValue["총액"]},{(int(value["총액"]) - int(newValue["총액"])) / int(newValue["총액"])}')
        else:
            print(f'거래소 ID {key} 가 기존 방식에만 있고 신규 어드민 방식에는 없음.')


def string_format_output():
    for key, value in prevTable.items():
        if key in newTable:
            newValue = newTable[key]
            if value == newTable[key]:
                print(f'거래소 ID:{key} 발전소명: {value["발전소명"]} 에 대하여 정산금 총액 {value["총액"]} 로 동일.')
            else:
                print(
                    f'거래소 ID {key} 에 대하여 정산금 총액이 서로 다름. 기존어드민발전량: {value["검증발전량"]} 신규어드민발전량: {newValue["검증발전량"]} 검증발전량차(%): {(int(value["검증발전량"]) - int(newValue["검증발전량"])) / int(newValue["검증발전량"])}, 기존어드민총액: {value["총액"]} 신규어드민총액: {newValue["총액"]} 총액차(%): {(int(value["총액"]) - int(newValue["총액"])) / int(newValue["총액"])}')
        else:
            print(f'거래소 ID {key} 가 기존 방식에만 있고 신규 어드민 방식에는 없음.')


table_format_output()
