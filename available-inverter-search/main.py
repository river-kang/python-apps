with open('files/all_device_configs.txt', 'r') as file:
    all_devices = file.read()

target_devices = dict()
target_devices_name = dict()
with open('files/target_devices.txt', 'r') as file:
    line = file.readline()
    while line:
        row = line.split(',')
        target_devices[row[0]] = row[1].replace('\n', '')
        target_devices_name[row[1].replace('\n', '')] = None
        line = file.readline()


print(target_devices_name)
for key, value in target_devices.items():
    if key in all_devices:
        target_devices_name[value] = True
    else:
        target_devices_name[value] = False

with open('files/supporting_inverters.txt', 'r') as file:
    line = file.readline()
    while line:
        row = line.split(',')

        if row[1] == 'N':
            print(f'{row[0]},N')
        elif row[0] not in target_devices_name or target_devices_name[row[0]] == False:
            print(f'{row[0]},I')
        else:
            print(f'{row[0]},Y')

        line = file.readline()
