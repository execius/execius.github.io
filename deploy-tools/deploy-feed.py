#!/usr/bin/python3
import json
import re
import markdown
import frontmatter
from pathlib import Path
import sys
from os.path import abspath
from pathlib import Path
from datetime import datetime


root_path=abspath("../")+"/"
base_path=root_path

main_directory = Path("../")
rsc_path=root_path + "/rsc/"
jsons_path=rsc_path + "/json/"
htmls_path=rsc_path+"/html"
md_files_path=rsc_path+"/obsidian-md/"
templates_path= htmls_path+ "/templates/"
html_posts_path = htmls_path+"/posts/"
topics_path = htmls_path+"/topics/"

try :
    if sys.argv[1] == "main":
        base_path="/"
except:
    pass
local_link_path=abspath("../../../../../Documents/obsidianvault")
site_link_path="/rsc/html/posts/"

slots = {
        "stdhead" : "<!-- stdhead-slot -->",
        "feed" : "<!-- feed-slot -->",
        "myinfo" :"<!-- myinfo-slot -->",
        "footer" :"<!-- footer-slot -->",
        "navbar" :"<!-- navbar-slot -->",
        "base" :"<!-- base-slot -->",
        "topics" :"<!-- topics-slot -->",
        "description" : "<!-- description-slot -->",
        "title" : "<!-- title-slot -->"}
filler_slots = {
        "stdhead":"<!-- stdhead-slot -->",
        "myinfo" :"<!-- myinfo-slot -->",
        "footer" :"<!-- footer-slot -->",
        "navbar" :"<!-- navbar-slot -->"}

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

import re

def slugify(name):
    name = name.strip().lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "-", name)
    return name

def convert(text):
    def repl(match):
        raw = match.group(1).strip()
        alias = match.group(2)

        # split note and section
        if "#" in raw:
            note_part, section_part = raw.split("#", 1)
            note_slug = slugify(note_part)
            section_slug = slugify(section_part)
            href = f"{note_slug}.html#{section_slug}"
        else:
            note_slug = slugify(raw)
            href = f"{note_slug}.html"

        label = alias.strip() if alias else raw
        return f"[{label}]({href})"

    return re.sub(r"\[\[([^|\]]+)(?:\|([^\]]+))?\]\]", repl, text)
def slugify_md_names():
    for file in Path(md_files_path).iterdir():
        frontmatter_data = frontmatter.load(file)
        new_name = slugify(frontmatter_data['title'])
        new_path = file.with_name(new_name)
        if file.name != new_name:
            print(f"{file.name} -> {new_name}")
            file.rename(new_path)
#loads json items from a file
def load_json_items(posts_file_json):
    items = []
    with open(posts_file_json,"r",encoding="utf-8") as f:
        data = json.load(f)
        f.close()
    for key in data :
        items.append(data[key])
    return items





def get_text(file_path):
    try:
        with open(file_path,"r", encoding="utf-8") as f:
            text = f.read()
            f.close()
            return text
    except:
        print("couldn't read html file:" ,file_path)
        return ""

global_fillers = {
        "myinfo" :get_text(htmls_path+"/global/myinfo.html"),
        "footer" :get_text(htmls_path+"/global/footer.html"),
        "navbar" :get_text(htmls_path+"/global/navbar.html"),
        "stdhead": get_text(htmls_path+"/global/std_head_content.html")
        }

def write_text(file_path,text):
    try:
        with open(file_path,"w", encoding="utf-8") as f:
            f.write(text)
            f.close()
    except Exception as e:
        print(e)
        print("couldn't write to html file:" ,file_path)
        return ""



def replace_slot(template_text,html_text,replaced_text):
    try:
        result = template_text.replace(replaced_text,html_text)
        result = result.replace(slots['base'],base_path)
        for key in filler_slots:
            result = result.replace(filler_slots[key],global_fillers[key])
        return result
    except Exception as e:
        print(e)
        print("error replacing slot")
        return -1
        pass

def make_page_file(template_path,html_text,slot_text,result_path):
    
    template_text = get_text(template_path)
    page_text = replace_slot(template_text,html_text,slot_text)
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
          <a class="feed-item" href="{html_posts_path}/{slugify(item['title'])}.html">\
            <img class="feed-subitem image" src="{item['image']}">\
            <h2 class="feed-subitem title" >{item['title']}</h2>\
            <p class="feed-subitem description">{item['description']}</p>\
            <div class="feed-subitem information">\
              <div class="feed-subitem information author">\
                <i class="fa-solid fa-user fa-2x"></i>\
                <p class="button feed-subitem information author-username">{item['author']}</p>\
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


def mdtopost(item):
    slot_text="<!-- post-slot -->"
    post_template = get_text(templates['post'])
    obsidian_mdtext = item.content
    standard_mdtext = convert(obsidian_mdtext)
    html = markdown.markdown(standard_mdtext,\
            extensions=['fenced_code', 'codehilite','tables'])
    html = html.replace(local_link_path,site_link_path)
    post = replace_slot(post_template,html,slot_text)
    # post = replace_slot(post,item['tags'],slots['tags'])
    post = replace_slot(post,item['title'],slots['title'])
    post = replace_slot(post,item['description'],slots['description'])
    return post


def make_post_files(posts_items):
    for item in posts_items:
        post_filename = slugify(item['title']) +".html"
        post = mdtopost(item)
        path = html_posts_path + '/' +post_filename
        write_text(path,post)

def get_post_items():
    posts_items = []
    for mdfile in Path(md_files_path).iterdir():
        if mdfile.is_file():
            item = frontmatter.load(mdfile)
            posts_items.append(item)
            posts_items.sort(key=lambda p: p["date"],reverse=True)
    return posts_items


def make_topics(topics_items):
    slot_text="<!-- feed-slot -->"
    topic_name_slot = "<!-- topic-name-slot -->" 
    topic_template = templates['topic']
    for topic_item in topics_items:
        topic_posts = []
        topic_name = topic_item['title']
        for item in posts_items:
            post_topics = item['tags']
            if topic_name in post_topics:
                topic_posts.append(item)
        topic_feed_html = generate_feed_html(topic_posts)
        topic_page_file = topics_path+"/"+topic_item['title']+".html"
        make_page_file(topic_template,topic_feed_html,slot_text,topic_page_file)
        make_page_file(topic_page_file,topic_name,topic_name_slot,topic_page_file)
        make_page_file(topic_page_file,topic_item['description'],slots['description'],topic_page_file)
        make_page_file(topic_page_file,topic_item['title'],slots['title'],topic_page_file)


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
    slot_text=slots['topics']
    topics_page = html_pages_files['topics']
    make_page_file(topics_template,topic_feed,slot_text,topics_page)

topics_items = load_json_items(json_files['topics'])
resources_items = load_json_items(json_files['resources'])
posts_items = get_post_items()

slugify_md_names()
make_post_files(posts_items)
# make_post_files(resources_items)
make_topics(topics_items)
build_feed(posts_items)
build_topics_feed(topics_items)
make_page_file(templates['resources'],"","",html_pages_files['resources'])
