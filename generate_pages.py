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
index_ongoing_html_str = directory_template_str + "index_ongoing.html"
index_completed_html_str = directory_template_str + "index_completed.html"
project_entry_html_str = directory_template_str + "project_entry.html" 
template_gallery_html_str = directory_template_str + "gallery.html"
gallery_image_html_str = directory_template_str + "gallery_image.html"
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

class Project:
    def __init__(self, project_title, project_start_date, project_completion_date, index_entry, gallery_images):
        self.project_title = project_title
        self.project_start_date = project_start_date
        self.project_completion_date = project_completion_date
        self.index_entry = index_entry
        self.gallery_images = gallery_images

    def __repr__(self):
        return repr((self.project_title, self.project_start_date, self.project_completion_date))

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
        image_path = "../todo.png"
        if file_name:
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

def GenerateListProjects():
    print("GenerateListProjects:")
    list_projects_ongoing = []
    list_projects_completed = []
    for dir in os.listdir(directory_source_str):
        dir_source = directory_source_str + dir + "/"
        page_link = directory_project_str + dir + ".html"
        project = GenerateProjectEntry(dir_source, page_link)
        if not project.project_completion_date:
            list_projects_ongoing.append(project)
        else:
            list_projects_completed.append(project)

    list_projects_ongoing = sorted(list_projects_ongoing, key=lambda project: project.project_title)
    list_projects_completed = sorted(list_projects_completed, key=lambda project: project.project_completion_date, reverse=True)
    return list_projects_ongoing, list_projects_completed

def GenerateIndex(list_projects_ongoing, list_projects_completed):
    print("GenerateIndex:")
    path_index = "index.html"
    print("path_index:", path_index)
    code = ReadContent(template_index_html_str)

    code_entries = ReadContent(index_ongoing_html_str)
    #for dir in os.listdir(directory_source_str):
    #    dir_source = directory_source_str + dir + "/"
    #    page_link = directory_project_str + dir + ".html"
    #    print("source:", dir_source)
    #    code_entries += GenerateProjectEntry(dir_source, page_link).index_entry
    for project in list_projects_ongoing:
        code_entries += project.index_entry
    code_entries += ReadContent(index_completed_html_str)
    for project in list_projects_completed:
        code_entries += project.index_entry
    code = code.replace("$PROJECT_ENTRIES$", code_entries)

    with open(path_index, "w") as f_out:
        f_out.write(code)

def GenerateProjectEntry(dir_source, page_link):

    index_entry = ReadContent(project_entry_html_str)

    tree = ET.parse(dir_source+"config.xml")
    root = tree.getroot()
    project_title = root.get("project_title")
    project_image = root.get("project_image")

    node_project_status = root.find("status")
    project_start_date = node_project_status.get("project_start_date")
    project_completion_date = node_project_status.get("project_completion_date")

    index_entry = index_entry.replace("$PROJECT_TITLE$", project_title)
    index_entry = index_entry.replace("$PROJECT_LINK$", page_link)
    image_path = "../todo.png"
    if project_image:
        image_path = "../"+dir_source+project_image
    index_entry = index_entry.replace("$PROJECT_IMAGE$", image_path)

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

    if project_completion_date:
        code_authors += "(" + project_start_date + " until " + project_completion_date + ")"

    index_entry = index_entry.replace("$AUTHORS$", code_authors)

    index_entry = Insert(index_entry, "$ABSTRACT_TEXT$", dir_source+"abstract.txt")



    node_images = root.find("images")
    gallery_images = ""
    for image in node_images.findall("image"):
        file_name = image.get("file")
        if file_name:
            image_path = "../"+dir_source+file_name        
            print("image_path", image_path)
            image_code = ReadContent(gallery_image_html_str)
            image_code = image_code.replace("$IMAGE_FULL_PATH$", image_path)
            image_code = image_code.replace("$PROJECT_LINK$", page_link)
            gallery_images += image_code

    project = Project(project_title, project_start_date, project_completion_date, index_entry, gallery_images)
    return project

#########################################################################################
#
#   GALLERY PAGE
#
#########################################################################################

def GenerateGallery(list_projects_ongoing, list_projects_completed):
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
    code_images = ""
    for project in list_projects_ongoing:
        code_images += project.gallery_images
    #code_entries += ReadContent(index_completed_html_str)
    for project in list_projects_completed:
        code_images += project.gallery_images

    code = code.replace("$GALLERY_ENTRIES$", code_images)

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
    list_projects_ongoing, list_projects_completed = GenerateListProjects()
    print("ongoing:", list_projects_ongoing)
    print("completed:", list_projects_completed)
    GenerateIndex(list_projects_ongoing, list_projects_completed)
    GenerateGallery(list_projects_ongoing, list_projects_completed)
    GenerateVideos()