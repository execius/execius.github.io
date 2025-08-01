#!/usr/bin/python3
import json
from pathlib import Path
import sys
from os.path import abspath


root_path=abspath("../")+"/"
base_path=root_path
print(root_path)
print(base_path)

main_directory = Path("../")
rsc_path=root_path + "/rsc/"
jsons_path=rsc_path + "/json/"
htmls_path=rsc_path+"/html"
templates_path= htmls_path+ "/templates/"
html_posts_path = htmls_path+"/posts/"
topics_path = htmls_path+"/topics/"
base_slot = "<!-- base-slot -->"

try :
    if sys.argv[1] == "main":
        base_path="/"
except:
    pass
local_link_path=abspath("../../../../../Documents/obsidianvault")
site_link_path="/rsc/html/posts/"


html_pages_files = {
        "home" : root_path + "/index.html",
        "feed" : htmls_path+"/feed"+ "/index.html",
        "topics" : htmls_path+"/topics"+ "/index.html",
        "resources" : htmls_path+"/resources"+ "/index.html",
        }

templates = {
        "home" : templates_path+"/home/template.html",
        "post" : templates_path+"/post/template.html",
        "feed" : templates_path+"/feed/template.html",
        "topics" : templates_path+"/topics/template.html",
        "topic" : templates_path+"/topic/template.html",
        "resources" : templates_path+"/resources/template.html",
        }
json_files = {
        "post" : jsons_path+"/posts/posts.json",
        "topics" : jsons_path+"/topics/topics.json",
        "resources" : jsons_path+"/resources/resources.json",
        }

directories = [main_directory] + list(main_directory.glob("*/"))


#loads json items from a file
def load_json_items(posts_file_json):
    items = []
    with open(posts_file_json,"r",encoding="utf-8") as f:
        data = json.load(f)
        f.close()
    for key in data :
        items.append(data[key])
    return items



posts_items = load_json_items(json_files['post'])
topics_items = load_json_items(json_files['topics'])


def get_text(file_path):
    try:
        with open(file_path,"r", encoding="utf-8") as f:
            text = f.read()
            f.close()
            return text
    except:
        print("couldn't read html file:" ,file_path)
        return ""

def write_text(file_path,text):
    try:
        with open(file_path,"w", encoding="utf-8") as f:
            f.write(text)
            f.close()
    except:
        print("couldn't write to html file:" ,file_path)
        return ""



def make_page_text(template_text,html_text,replaced_text):
    try:
        result = template_text.replace(replaced_text,html_text)
        result = result.replace(base_slot,base_path)
        return result
    except Exception as e:
        print(e)
        print("error making page")
        return -1
        pass
def make_page_file(template_path,html_text,slot_text,result_path):
    
    template_text = get_text(template_path)
    page_text = make_page_text(template_text,html_text,slot_text)
    write_text(result_path,page_text)

def generate_feed_item(item):

    html_posts_path = htmls_path+"/posts/"
    try :
        if sys.argv[1] == "main":
            base_path="/"
        html_posts_path="/rsc/html/posts/"
    except:
        pass
    result = f"""\
          <a class="feed-item" href="{html_posts_path}/{item['title']}.html">\
            <img class="feed-subitem image" src="{item['image']}">\
            <h2 class="feed-subitem title" >{item['title']}</h2>\
            <p class="feed-subitem description">{item['description']}</p>\
            <div class="feed-subitem information">\
              <div class="feed-subitem information author">\
                <i class="fa-solid fa-user fa-2x"></i>\
                <p class="button feed-subitem information author-username">{item['author-username']}</p>\
              </div>\
              <p class="button feed-subitem information posting-date">{item['date']}</p>\

            </div>\
          </a>\
    """
    return result
def generate_feed_html(items_array):
    feed_html = "\n".join(generate_feed_item(item) for item in items_array)
    return feed_html

    return feed_html
def build_feed(feed_items):
    feed_html=generate_feed_html(feed_items)
    feed_template=templates['feed']
    slot_text="<!-- Feed-slot -->"
    feed_page = html_pages_files['feed']
    make_page_file(feed_template,feed_html,slot_text,feed_page)
    make_page_file(templates['home'],feed_html,slot_text,html_pages_files['home'])
    print("Feed built successfully into", feed_page)



def make_posts(posts_items):
    slot_text="<!-- post-slot -->"
    post_template = templates['post']
    for item in posts_items:
        raw_post_file = html_posts_path+"/raw_html/"+item['title']+".html"
        post_page_file = html_posts_path+"/"+item['title']+".html"
        print(post_page_file)
        raw_post_text = get_text(raw_post_file)
        raw_post_text = raw_post_text.replace(local_link_path,site_link_path)
        make_page_file(post_template,raw_post_text,slot_text,post_page_file)


def make_topics(topics_items):
    slot_text="<!-- feed-slot -->"
    topic_name_slot = "<!-- topic-name-slot -->" 
    topic_template = templates['topic']
    for topic_item in topics_items:
        topic_posts = []
        topic_name = topic_item['title']
        for item in posts_items:
            post_topics = item['topics'].split(',')
            if topic_name in post_topics:
                topic_posts.append(item)
        topic_feed_html = generate_feed_html(topic_posts)
        topic_page_file = topics_path+"/"+topic_item['title']+".html"
        make_page_file(topic_template,topic_feed_html,slot_text,topic_page_file)
        make_page_file(topic_page_file,topic_name,topic_name_slot,topic_page_file)


def generate_topics_feed_item(item):
    html_posts_path = htmls_path+"/posts/"
    topics_path =  htmls_path+"/topics/"
    try :
        if sys.argv[1] == "main":
            base_path="/"
        topics_path = "/rsc/html/topics/"
     
    except:
        pass
    result = f"""\
          <a class="feed-item" href="{topics_path}/{item['title']}.html">\
            <img class="feed-subitem image" src="{item['image']}" >\
            <h2 class="feed-subitem title" >{item['title']}</h2>\
            <p class="feed-subitem description">{item['description']}</p>\
          </a>\
    """
    return result

def generate_topics_feed_html(items_array):
    feed_html = "\n".join(generate_topics_feed_item(item) for item in items_array)
    return feed_html
def build_topics_feed(topics_items):
    topic_feed=generate_topics_feed_html(topics_items)
    topics_template=templates['topics']
    slot_text="<!-- topics-slot -->"
    topics_page = html_pages_files['topics']
    make_page_file(topics_template,topic_feed,slot_text,topics_page)

make_posts(posts_items)
make_topics(topics_items)
build_feed(posts_items)
build_topics_feed(topics_items)
make_page_file(templates['resources'],"","",html_pages_files['resources'])
