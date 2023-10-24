# Amazon-ChatBot-HackOn2023
![Amazon](https://img.shields.io/badge/Amazon-AmaziBot-orange?labelColor=grey&style=flat&logo=amazon) ![AWS](https://img.shields.io/badge/AWS-EC2-orange?labelColor=grey&style=flat&logo=aws) ![Flask](https://img.shields.io/badge/Flask-Backend-blue?labelColor=grey&style=flat&logo=flask) ![Intents](https://img.shields.io/badge/Intents-grey?style=flat&logo=target) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) ![Adobe](https://img.shields.io/badge/adobe-%23FF0000.svg?style=for-the-badge&logo=adobe&logoColor=white) ![Stack Overflow](https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white)![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Amazon](https://img.shields.io/badge/Amazon-ORANGE?style=flat&logo=Amazon)

## Problem Statement

Theme 1 - Shopping Experience with Generative Al + AWS
Contextual shopping experience using ChatGPT: We invite you to explore futuristic shopping experience using generative Al for Amazon. Objective is to curate contextual shopping experiences based on individual user's chat session and preferences. AWS can be used for solutioning. E.g. I want to buy best air conditioner for my living room in 30K budget, please suggest me a branded 5 star power rated AC.

## Our Solution

1. Amazon Chatbot: We've developed a specialized chatbot tailored for Amazon's shopping platform which is programmed to greet users, creating a welcoming environment and is capable of understanding and responding to various shopping queries, such as product recommendations.

2. Product Suggestions: Upon receiving a query, the chatbot generates a list of 5 relevant products, complete with essential details like product name, reviews, and ratings which is presented in an interactive card format, making it easy for users to digest information.

3. Add to Cart and Direct Amazon Link: Users have the convenience of adding products directly to their Amazon cart from within the chat interface and clicking on the product card redirects the user to the actual Amazon product page for a more detailed view.

4. Voice-to-Text Integration: To enhance user experience, we've integrated a voice-to-text feature, allowing users to speak their queries instead of typing them.

5. AWS EC2 Hosting: The entire application is hosted on Amazon's EC2, ensuring a scalable and robust solution.

6. Future-Ready: This solution is designed with the future in mind, easily adaptable for more advanced features and integrations. most importantly the virtual try-on feature for clothes , jewelry , furniture and many more.

By combining generative AI, user experience design, and AWS services, we offer a next-level, contextual shopping experience that revolutionizes the way users interact with Amazon.

## Screenshots

![Bot Interface](https://github.com/sidoriginal/Amazon-ChatBot-HackOn2023/blob/main/Screenshots/bot1.png?raw=true)

![Bot Interface](https://github.com/sidoriginal/Amazon-ChatBot-HackOn2023/blob/main/Screenshots/bot2.png?raw=true)

![Scrapy Running](https://github.com/sidoriginal/Amazon-ChatBot-HackOn2023/blob/main/Screenshots/terminal.png?raw=true)


## How To Run

Install the following files

```bash
scrapy
flask
numpy
pandas
requests
```
OR Run 

```bash
pip install -r requirements.txt
```
Make account on [Wit.ai](https://www.wit.ai/) and make new app there, train your chatbot about desired intents and entities. After that in **_main.py** put your own Server Access Token:
```_main.py
# Your Wit.ai access token
access_token = "YOUR_SERVER_ACCESS_TOKEN"

# Base URL for Wit.ai API
base_url = "https://api.wit.ai"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {access_token}"
}
```

Now make account on [ScapperApi](https://www.scraperapi.com/) and create account to get API key, then in **amazon_scraper/amazon_scarper/spiders/amazon.py** put your API key:
```amazon.py
def start_requests(self):
        queries.append(self.search_query)
        for query in queries:
            url = 'https://www.amazon.in/s?' + urllib.parse.urlencode({'k': query})
            API = 'YOUR_API_KEY'
            payload = {'api_key': API, 'url': url, 'country_code': 'in'}
            proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
            yield scrapy.Request(proxy_url, callback=self.parse_keyword_response)
    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')
        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.in/dp/{asin}"
            API = 'YOUR_API_KEY'
            payload = {'api_key': API, 'url': product_url, 'country_code': 'in'}
            proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
            yield scrapy.Request(proxy_url, callback=self.parse_product_page, meta={'asin': asin})
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urllib.parse.urljoin("https://www.amazon.in",next_page)
            API = 'YOUR_API_KEY'
            payload = {'api_key': API, 'url': url, 'country_code': 'in'}
            proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
            yield scrapy.Request(proxy_url, callback=self.parse_keyword_response)
}
```
Now run flask app using:
```bash
python app.py
```

Your ChatBot is running now!!

## Tech-Stack

This project is a sophisticated chatbot designed to enhance the Amazon shopping experience. It employs a range of technologies to deliver a seamless and interactive user interface:

1. Scrapy : Utilized for web scraping, it fetches real-time product information from Amazon, including product details and pricing.
  
2. Wit.ai : Powers the chatbot's natural language understanding. Intents are trained to recognize user queries and respond appropriately, such as suggesting products.

3. HTML, CSS, JavaScript : The frontend is crafted using standard web technologies. Each product suggestion is displayed as a card with options to "Show Product" or "Add to Cart."

4. Flask: Serves as the backend framework, integrating the Scrapy spider and Wit.ai bot with the frontend, and handling user interactions.

5. Amazon EC2 : The entire application is hosted on an Amazon EC2 instance, ensuring scalability and robust performance.

## Future Scope


As we look ahead, there are several exciting directions in which this chatbot can evolve to further enhance the user experience:

1. Virtual Try-On: Integration of Augmented Reality (AR) to allow users to virtually try on attire such as shoes, watches, glasses, and clothes, providing a more interactive shopping experience is being made. Few reference papers on which we are working are as follows:
* Size Does Not Matter : https://openaccess.thecvf.com/content/ICCV2023/papers/Chen_Size_Does_Matter_Size-aware_Virtual_Try-on_via_Clothing-oriented_Transformation_Try-on_ICCV_2023_paper.pdf
* GP-VITON : https://github.com/xiezhy6/GP-VTON

2. Amazon API: When fully integrated with Amazon, the use of Amazon's native API could significantly reduce the time required for search queries, making the bot more efficient.

3. Cart Management: A feature could be added to allow users to view all the items in their Amazon cart directly within the chat interface, streamlining the shopping process.

4. Multilingual Support: To cater to a global audience, the chatbot could be developed to support multiple languages, making it accessible to non-English speakers.


