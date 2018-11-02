
import os



html ='<meta name="viewport" content="width=device-width, initial-scale=1">\n'
file = os.listdir('.')
ext = os.path.splitext(file[-1])
exts = ['.html']
print(file)
for i in file:
    ext = os.path.splitext(i)[-1]
    if ext in exts:
        with open(i, 'r') as f:
            content = f.readlines()
            if '<meta name="viewport"' not in ' '.join(content[:4]):
                content.insert(3, html)
                with open(i, 'w') as ff:
                    ff.write(''.join(content))
                print(i, 'ok')
  
            