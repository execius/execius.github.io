
import json
from pathlib import Path

main_directory = Path("../")
directories = [main_directory] + list(main_directory.glob("*/"))
FEED_DIR = Path("../feed/posts/")
TEMPLATE_FILE="index.html"
feed_templates_files_tupple_lst=[(f"{directory}/template.html",f"{directory}/index.html") for directory in directories ]


def load_feed_items():
    items = []
    for json_file in FEED_DIR.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
            items.append(data)
    return items

def generate_feed_html(item):
    return f"""\
          <a class="feed-item" href="#">\
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

def build_page(feed_items,file_template_tuple):
    try :
        with open(file_template_tuple[0], encoding="utf-8") as f:
            html = f.read()

    except:
        print(f"no template file :{file_template_tuple[0]}\nskiping")
        return 0
    feed_html = "\n".join(generate_feed_html(item) for item in feed_items)
    html = html.replace("<!-- Feed-slot -->", feed_html)

    with open(file_template_tuple[1], "w", encoding="utf-8") as f:
        f.write(html)
    print("Feed built successfully into", file_template_tuple[1])

for file_templ_tup in feed_templates_files_tupple_lst:
    feed_items = load_feed_items()
    build_page(feed_items,file_templ_tup)
