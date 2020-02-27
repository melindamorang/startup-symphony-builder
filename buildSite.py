# Builds the Startup Symphony site from component HTML parts
import io
import os

builderdir = os.getcwd()
contentdir = os.path.join(builderdir, "ContentPages")
output_folder = os.path.join(os.path.dirname(builderdir), "startup-symphony")

menu_active = ' class="current"'

def get_html_from_builder_file(file_path, variable_dict={}):
    '''Grab the html code from a partial html file used to construct the final page, and substitute any variables'''
    html_code = []
    with io.open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for var, val in variable_dict.items():
                line = line.replace(var, val)
            html_code.append(line)
    return html_code

def build_page(sections, file_name):
    with io.open(os.path.join(output_folder, file_name), 'w', encoding='utf-8') as f:
        for sec in sections:
            f.writelines(sec)

# Generate all content pages
pages = os.listdir(contentdir)
for p in pages:
    page = os.path.join(contentdir, p)
    page_code = get_html_from_builder_file(page)
    keywords = page_code[0] # First line of file contains keywords for the page
    page_code = page_code[1:] # Rest of file is the actual html code
    vars = {"$PageKeywords": keywords,
            "$HomeMenuItemActive": "",
            "$TopicsMenuItemActive": "",
            "$StepByStepMenuItemActive": "",
            "$ContactMenuItemActive": "",
            "$BannerText": ""}
    top_code = get_html_from_builder_file(os.path.join(builderdir, "top.html"), vars)
    bottom_code = get_html_from_builder_file(os.path.join(builderdir, "bottom.html"))
    build_page([top_code, page_code, bottom_code], p)

# Generate topic index, step-by-step, and contact pages
other_pages = {"topics.html": "$TopicsMenuItemActive", "stepbystep.html": "$StepByStepMenuItemActive", "contact.html": "$ContactMenuItemActive"}
for pagename in other_pages:
    page_code = get_html_from_builder_file(os.path.join(builderdir, pagename))
    vars = {"$PageKeywords": "",
            "$HomeMenuItemActive": "",
            "$TopicsMenuItemActive": "",
            "$StepByStepMenuItemActive": "",
            "$ContactMenuItemActive": "",
            "$BannerText": ""}
    vars[other_pages[pagename]] = menu_active
    top_code = get_html_from_builder_file(os.path.join(builderdir, "top.html"), vars)
    bottom_code = get_html_from_builder_file(os.path.join(builderdir, "bottom.html"))
    build_page([top_code, page_code, bottom_code], pagename)

# Generate homepage
page_code = get_html_from_builder_file(os.path.join(builderdir, "index.html"))
vars = {"$PageKeywords": "",
        "$HomeMenuItemActive": menu_active,
        "$TopicsMenuItemActive": "",
        "$StepByStepMenuItemActive": "",
        "$ContactMenuItemActive": "",
        "$BannerText": '<h1>The Startup Symphony</h1>'}
top_code = get_html_from_builder_file(os.path.join(builderdir, "top.html"), vars)
bottom_code = get_html_from_builder_file(os.path.join(builderdir, "bottom.html"))
build_page([top_code, page_code, bottom_code], 'index.html')
