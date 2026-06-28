import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix showWord
content = re.sub(r"speak\(`\$\{title\}-\$\{text\}\`)", "speak(title + '-' + text)", content)

# Fix playHomePoem - try simpler approach
old_play = """async function playHomePoem(){
      for(let i=0;i<poem.length;i++){
        highlightLine(i, 'poem');
        await speak(poem[i].plain);
      }
    }"""

new_play = """async function playHomePoem(){
      for(let i=0;i<poem.length;i++){
        highlightLine(i, 'poem');
        await speak(poem[i].line);
      }
    }"""

content = content.replace(old_play, new_play)

# Fix heart-right segment text to match the HTML text
heart_right_old = """speak('我們學到。有時候找不到人，不一定是壞事。可以學會耐心等待，也可以欣賞路上的風景。')"""
heart_right_new = """speak('我們學到。有時候找不到人，不一定是壞事。可以學會耐心等待，也可以欣賞路上的風景。')"""
content = content.replace(heart_right_old, heart_right_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed")