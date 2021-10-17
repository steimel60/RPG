str = f"I'm not important. This is a really long string that won't fit in the textbox unless we wrap it. So I found a text wrap func and going to try it out with this string."
words = str.split(' ')
for word in words:
    print(word)

word_counter = 20

words = words[word_counter:]

for word in words:
    print(word)
