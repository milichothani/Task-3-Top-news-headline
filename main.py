from bs4 import BeautifulSoup
import requests

# response = requests.get("https://indianexpress.com/")
response = requests.get("https://news.ycombinator.com/news")

yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")

articles = soup.find_all("span", class_="titleline")
article_texts = []
article_links = []
article_upvotes =[]

for article_tag in articles:
    article_link_tag = article_tag.find("a")
    
    text = article_link_tag.getText()
    article_texts.append(text)

    link = article_link_tag.get("href")
    article_links.append(link)

upvotes = soup.find_all("span", class_="score")
for upvote_tag in upvotes:
    article_upvotes.append(upvote_tag.getText())
    
while len(article_upvotes) < len(article_texts):
    article_upvotes.append("No upvotes yet")
    
numeric_upvotes = []
for up in article_upvotes:
    if "points" in up:
        numeric_upvotes.append(int(up.split()[0]))
    else:
        numeric_upvotes.append(0)
        
larget_number = max(numeric_upvotes)
largest_index = numeric_upvotes.index(larget_number)

print(article_texts[largest_index])
print(article_links[largest_index])

# print(article_texts)
# print(article_links)
# print(numeric_upvotes)

top_news = list(zip(numeric_upvotes, article_texts, article_links))
top_news.sort(reverse=True, key=lambda x: x[0])

print("Top 10 Tech news headlines\n")
for i,(upvote, title, link) in enumerate(top_news[:10], 1):
    print(f"{i}. {title} ({upvote})")
    print(link)
    print()
    
with open("top_headlines.txt", "w", encoding="utf-8") as file:
    file.write("TOP 10 TECH NEWS HEADLINES\n\n")
    for i, (upvote, title, link) in enumerate(top_news[:10], 1):
        file.write(f"{i}. {title} ({upvote} points)\n")
        file.write(f"{link}\n\n")