import os
import xml.etree.ElementTree as ET

directory_template_str = "template/"
directory_source_str = "source/"
directory_project_str = "project/"
template_html_str = directory_template_str + "template.html"
image_html_str = directory_template_str + "image.html"
author_html_str = directory_template_str + "author.html"
link_html_str = directory_template_str + "link.html" 
template_index_html_str = directory_template_str + "index.html"
project_entry_html_str = directory_template_str + "project_entry.html" 
template_gallery_html_str = directory_template_str + "gallery.html"
template_videos_html_str = directory_template_str + "videos.html"

#########################################################################################
#
#   HELPER FUNCTIONS
#
#########################################################################################

def ReadContent(path):
    content = ""
    with open(path) as f:
        content = f.read()
    return content

def Insert(code, marker, path):
    print("Insert:", path)
    content = ""
    with open(path) as f:
        content = f.read()
    code = code.replace(marker, content)
    return code

#########################################################################################
#
#   PROJECT PAGE
#
#########################################################################################

def GeneratePages():
    print("GeneratePages")
    for dir in os.listdir(directory_source_str):
        dir_source = directory_source_str + dir + "/"
        path_out = directory_project_str + dir + ".html"
        GeneratePage(dir, dir_source, path_out)

def GeneratePage(dir, dir_source, path_out):
    print("")
    print("GeneratePage:", dir)
    print("source:", dir_source)
    print("path_out:", path_out)
    code = ReadContent(template_html_str)
    code = InsertFromConfigXML(code, dir_source)

    code = Insert(code, "$ABSTRACT_TEXT$", dir_source+"abstract.txt")
    with open(path_out, "w") as f_out:
        f_out.write(code)

def InsertFromConfigXML(code, dir_source):
    tree = ET.parse(dir_source+"config.xml")
    root = tree.getroot()
    project_title = root.get("project_title")
    code = code.replace("$PROJECT_TITLE$", project_title)

    node_images = root.find("images")
    code_images = ""
    for image in node_images.findall("image"):
        file_name = image.get("file")
        image_path = "../"+dir_source+file_name
        print("image_path", image_path)
        image_code = ReadContent(image_html_str)
        image_code = image_code.replace("$IMAGE_FULL_PATH$", image_path)
        code_images += image_code
    code = code.replace("$IMAGES$", code_images)

    node_links = root.find("links")
    code_links = ""
    for link in node_links.findall("link"):
        name = link.get("name")
        href = link.get("href")
        link_code = ReadContent(link_html_str)
        link_code = link_code.replace("$LINK_HREF$", href)
        link_code = link_code.replace("$LINK_NAME$", name)
        code_links += link_code
    code = code.replace("$LINKS$", code_links)

    node_authors = root.find("authors")
    code_authors = "["
    first_author = True
    for link in node_authors.findall("author"):
        name = link.get("name")
        href = link.get("href")
        if not first_author:
            code_authors += ", "        
        author_code = ReadContent(author_html_str)
        author_code = author_code.replace("$AUTHOR_HREF$", href)
        author_code = author_code.replace("$AUTHOR_NAME$", name)
        code_authors += author_code        
        first_author = False        
    code_authors += "]"
    code = code.replace("$AUTHORS$", code_authors)

    return code

#########################################################################################
#
#   INDEX PAGE
#
#########################################################################################

def GenerateIndex():
    print("GenerateIndex:")
    path_index = "index.html"
    print("path_index:", path_index)
    code = ReadContent(template_index_html_str)

    code_entries = ""
    for dir in os.listdir(directory_source_str):
        dir_source = directory_source_str + dir + "/"
        page_link = directory_project_str + dir + ".html"
        print("source:", dir_source)
        code_entries += GenerateProjectEntry(dir_source, page_link)
    code = code.replace("$PROJECT_ENTRIES$", code_entries)

    with open(path_index, "w") as f_out:
        f_out.write(code)

def GenerateProjectEntry(dir_source, page_link):

    entry = ReadContent(project_entry_html_str)

    tree = ET.parse(dir_source+"config.xml")
    root = tree.getroot()
    project_title = root.get("project_title")
    project_image = root.get("project_image")
    entry = entry.replace("$PROJECT_TITLE$", project_title)
    entry = entry.replace("$PROJECT_LINK$", page_link)
    image_path = "../"+dir_source+project_image
    entry = entry.replace("$PROJECT_IMAGE$", image_path)

    node_authors = root.find("authors")
    code_authors = "["
    first_author = True
    for link in node_authors.findall("author"):
        name = link.get("name")
        href = link.get("href")
        if not first_author:
            code_authors += ", "        
        author_code = ReadContent(author_html_str)
        author_code = author_code.replace("$AUTHOR_HREF$", href)
        author_code = author_code.replace("$AUTHOR_NAME$", name)
        code_authors += author_code        
        first_author = False        
    code_authors += "]"
    entry = entry.replace("$AUTHORS$", code_authors)

    entry = Insert(entry, "$ABSTRACT_TEXT$", dir_source+"abstract.txt")

    return entry

#########################################################################################
#
#   GALLERY PAGE
#
#########################################################################################

def GenerateGallery():
    print("GenerateGallery:")
    path_gallery = "gallery.html"
    print("path_gallery:", path_gallery)
    code = ReadContent(template_gallery_html_str)

    #code_entries = ""
    #for dir in os.listdir(directory_source_str):
    #    dir_source = directory_source_str + dir + "/"
    #    page_link = directory_project_str + dir + ".html"
    #    print("source:", dir_source)
    #    code_entries += GenerateProjectEntry(dir_source, page_link)
    code = code.replace("$GALLERY_ENTRIES$", "")

    with open(path_gallery, "w") as f_out:
        f_out.write(code)

#########################################################################################
#
#   VIDEOS PAGE
#
#########################################################################################

def GenerateVideos():
    print("GenerateVideos:")
    path_videos = "videos.html"
    print("path_videos:", path_videos)
    code = ReadContent(template_videos_html_str)

    #code_entries = ""
    #for dir in os.listdir(directory_source_str):
    #    dir_source = directory_source_str + dir + "/"
    #    page_link = directory_project_str + dir + ".html"
    #    print("source:", dir_source)
    #    code_entries += GenerateProjectEntry(dir_source, page_link)
    code = code.replace("$VIDEO_ENTRIES$", "")

    with open(path_videos, "w") as f_out:
        f_out.write(code)

#########################################################################################
#
#   MAIN
#
#########################################################################################

if __name__ == '__main__':
    GeneratePages()
    GenerateIndex()
    GenerateGallery()
    GenerateVideos()