with open('GSAF5.csv', 'rb') as f:
    chunk = f.read(1000)
    with open('debug_file.txt', 'w', encoding='utf-8') as f2:
        f2.write(str(chunk))
