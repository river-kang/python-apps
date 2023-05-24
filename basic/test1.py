import os


f = open("memo.txt", "r")

for line in f:
    value = line.replace("\n", "").replace(",", "").replace('"', "").replace(" ", "")

    print(f'"{value}/32" = "external_gcp_datastream_seoul",')