import requests
from bs4 import BeautifulSoup
import csv

def scrape_blog(url, max_posts=100, output_file='blog_content.txt'):
    # Send an HTTP request to the blog URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links to individual blog posts
        post_links = soup.find_all('a', href=True)  # Adjust the 'a' tag and attributes as per the HTML structure

        # Initialize a counter for the number of posts crawled
        posts_crawled = 0

        seen_links = []
        for link in post_links:
            post_url = link['href']
            if post_url.find('www.digikala.com/mag') != -1 and post_url.find('https://www.digikala.com/mag/%d8%b4%d8%b1%d8%a7%db%8c%d8%b7-%d8%a8%d8%a7%d8%b2%d9%86%d8%b4%d8%b1-%d9%85%d8%ad%d8%aa%d9%88%d8%a7/') == -1 and post_url.find('https://www.digikala.com/mag/careers/') == -1 and post_url.find('https://www.digikala.com/mag/%d8%b4%d8%b1%d8%a7%db%8c%d8%b7-%d8%a8%d8%a7%d8%b2%d9%86%d8%b4%d8%b1-%d9%85%d8%ad%d8%aa%d9%88%d8%a7/') == -1 and post_url.find('https://www.digikala.com/mag/disclaimer/') == -1 and post_url not in seen_links:
                seen_links.append(post_url)
                print(post_url)
                post_content = scrape_post_content(post_url)

            # Process or save the post content as needed
                # print(f"Post URL: {post_url}")
                # print("Post Content:")
                # print(post_content)
                # print("=" * 50)
    else:
        print(f"Failed to retrieve the blog page. Status Code: {response.status_code}")



def scrape_post_content(post_url):
    # Send an HTTP request to the individual post URL
    response = requests.get(post_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the post page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and return the text content of the post
        post_content = soup.find('div', class_='post-module__content')
        title_content = soup.find('div', class_='post-module__title')

        # if title_content is None:
        #     post_content = soup.find('div', class_='post')
        #     title_content = soup.find('div', class_='articleType1__info')
        #     print(post_content, title_content)
        if title_content is not None and post_content is not None:
            title = title_content.find('h1').get_text()
            p_tag = post_content.find_all('p')


            content = [p.get_text() for p in p_tag]
            idx = 0
            for i in range(len(content)):
                if content[i].find('منبع'):
                    idx = i
            content = content[0:idx]
            content = '\n'.join(content)
            # with open('/Users/mohammad/Desktop/artificial-intelligence_digiato.csv', 'a', newline='') as file:
            #     writer = csv.writer(file)
            #     writer.writerow([title, content])
            with open('/Users/mohammad/Desktop/game-gajet_mag.txt', 'a') as file:
                file.writelines(title)
                file.write('\n')
                file.writelines(content)
                file.write('\n\n')

        return post_content.get_text(separator='\n') if post_content else "No content found for this post."
    else:
        return f"Failed to retrieve the post content. Status Code: {response.status_code}"

# Example usage

blog_url = 'https://www.digikala.com/mag/category/%d8%a8%d8%a7%d8%b2%db%8c/%da%af%d8%ac%d8%aa/'
scrape_blog(blog_url)

for i in range(2, 39):
    print('page', i)
    scrape_blog(blog_url + f'/page/{i}/')

# # Open a CSV file to store the news
# with open('/Users/mohammad/Desktop/news.txt', 'w', newline='') as file:
#     writer = csv.writer(file)
#     # Write the header
#     writer.writerow(["Title", "Content"])

#     # Loop through the news articles
#     for article in news_articles:
#         # Extract the title and content
#         title = article.find('h2').text
#         content = article.find('p').text

#         # Write the news article to the CSV file
#         writer.writerow([title, content])