# clean_code.py деген файл жасап, ішіне мынаны қойыңыз:
file_path = 'crud.py' # файлдың жолы

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Барлық U+00A0 таңбасын кәдімгі бос орынға ауыстырамыз
clean_content = content.replace('\xa0', ' ')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(clean_content)

print("Файл сәтті тазаланды!")