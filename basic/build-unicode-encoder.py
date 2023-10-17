import unicodedata

value = "정밀 진단 보고서"

# Cloud Build Trigger 변환

print(value.encode('utf-8'))


url_encoded_value = value.encode().replace("%20", ".").replace("%u", "_")

print(url_encoded_value)