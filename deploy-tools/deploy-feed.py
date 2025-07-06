
import json
import pypandoc
import re
from pathlib import Path

main_directory = Path("../")
html_posts_dir = "../html-posts"
post_template_path = html_posts_dir+"/template.html"
directories = [main_directory] + list(main_directory.glob("*/"))
FEED_POSTS_FILE = Path("../feed/posts/posts.json")
TEMPLATE_FILE="index.html"
feed_templates_files_tupple_lst=[(f"{directory}/template.html",f"{directory}/index.html") for directory in directories ]


def load_feed_items(posts_file_json):
    items = []
    with open(posts_file_json,"r",encoding="utf-8") as f:
        data = json.load(f)
        f.close()
    for key in data :
        items.append(data[key])
    return items

def generate_feed_html(item):

    return f"""\
          <a class="feed-item" href="{item['post-page-html-path']}">\
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

def make_post_page(item,post_template_p,html_posts_dir):
    html_post_page_path="../"+item['post-page-html-path']
    post_html_path="../"+item['post-html-path']
    try:

        with open(post_html_path,"r", encoding="utf-8") as f:
            post_html_text = f.read()
        with open(post_template_p,"r", encoding="utf-8") as f:
            template_html = f.read()
            html_post_page = template_html.replace("<!-- post-slot -->",post_html_text)
            f.close()
        with open(html_post_page_path,"w", encoding="utf-8") as f:
            f.write(html_post_page)
            f.close()
        print(f"making post with title {item['title']} done")
    except:
        print(f"error making post page : {markdown_path}")
        return -1
        pass

def build_page(feed_items,file_template_tuple):
    try :
        with open(file_template_tuple[0],"r", encoding="utf-8") as f:
            html = f.read()
            f.close()
    except:
        print(f"no template file :{file_template_tuple[0]}\nskiping")
        return 0
    feed_html = "\n".join(generate_feed_html(item) for item in feed_items)
    html = html.replace("<!-- Feed-slot -->", feed_html)


    with open(file_template_tuple[1], "w", encoding="utf-8") as f:
        f.write(html)
        f.close()
    print("Feed built successfully into", file_template_tuple[1])

feed_items = load_feed_items(FEED_POSTS_FILE) 
for item in feed_items:
    ret = make_post_page(item,post_template_path,html_posts_dir)
    if ret == -1 :
        feed_items.remove(item)
for file_templ_tup in feed_templates_files_tupple_lst:
    build_page(feed_items,file_templ_tup)
