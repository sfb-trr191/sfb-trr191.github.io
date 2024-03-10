import os
import os.path
import xml.etree.ElementTree as ET

list_keywords_financed_project = ["financed", "Financed"]

directory_template_str = "template/"
directory_source_str = "source/"
directory_project_str = "project/"
template_html_str = directory_template_str + "template.html"
image_html_str = directory_template_str + "image.html"
author_html_str = directory_template_str + "author.html"
link_html_str = directory_template_str + "link.html" 
template_index_html_str = directory_template_str + "index.html"
template_student_projects_html_str = directory_template_str + "student-projects.html"
index_ongoing_html_str = directory_template_str + "index_ongoing.html"
index_completed_html_str = directory_template_str + "index_completed.html"
project_entry_student_html_str = directory_template_str + "project_entry_student.html" 
project_entry_html_str = directory_template_str + "project_entry.html" 
template_gallery_html_str = directory_template_str + "gallery.html"
gallery_image_html_str = directory_template_str + "gallery_image.html"
template_videos_html_str = directory_template_str + "videos.html"
template_random_image_html_str = directory_template_str + "random_image.html"
image_data_js_str = directory_template_str + "image_data.js"
placeholder_todo = "todo_empty_256x128.png"

#########################################################################################
#
#   HELPER FUNCTIONS
#
#########################################################################################

def GetThumbnailPath(path):
    path_thumbnail = path.replace(".jpg", ".thumbnail.jpg") 
    path_thumbnail = path.replace(".png", ".thumbnail.jpg")
    if os.path.isfile(path_thumbnail):
        return path_thumbnail
    return path

def IsProjectFinanced(project_type):
    return project_type in list_keywords_financed_project

def ReadContent(path):
    content = ""
    with open(path, encoding="utf8") as f:
        content = f.read()
    return content

def Insert(code, marker, path):
    print("Insert:", path)
    content = ""
    if os.path.isfile(path):
        with open(path, encoding="utf8") as f:
            content = f.read()
    code = code.replace(marker, content)
    return code

def InsertText(code, marker, content):
    code = code.replace(marker, content)
    return code

def Read(path):
    print("Read:", path)
    content = ""
    if os.path.isfile(path):
        with open(path, encoding="utf8") as f:
            content = f.read()
    return content

class Project:
    def __init__(self, project_type, project_title, project_start_date, project_completion_date, index_entry, gallery_images, list_image_data):
        self.project_type = project_type
        self.project_title = project_title
        self.project_start_date = project_start_date
        self.project_completion_date = project_completion_date
        self.index_entry = index_entry
        self.gallery_images = gallery_images
        self.list_image_data = list_image_data

    def __repr__(self):
        return repr((self.project_type, self.project_title, self.project_start_date, self.project_completion_date))

class ImageData:
    def __init__(self, project_title, image_description, project_link, image_link, thumbnail_link):
        self.project_title = project_title
        self.image_description = image_description
        self.project_link = project_link
        self.image_link = image_link
        self.thumbnail_link = thumbnail_link

    def __repr__(self):
        return repr((self.project_title, self.image_description, self.project_link, self.image_link))

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
    with open(path_out, "w", encoding="utf8") as f_out:
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
        image_path = "../"+placeholder_todo
        thumbnail_path = image_path
        image_description_path = ""
        if file_name:
            image_path = "../"+dir_source+file_name        
            image_description_path = (dir_source+file_name).replace(".png", ".txt") 
            image_description_path = image_description_path.replace(".jpg", ".txt")    
             
            thumbnail_path = GetThumbnailPath(dir_source+file_name)

        print("image_path", image_path)
        image_code = ReadContent(image_html_str)
        image_code = image_code.replace("$IMAGE_FULL_PATH$", image_path)
        image_code = image_code.replace("$THUMBNAIL_FULL_PATH$", "../"+thumbnail_path)
        image_code = Insert(image_code, "$IMAGE_DESCRIPTION$", image_description_path)
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
        author_code = name    
        if href:
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
    list_student_projects_ongoing = []
    list_student_projects_completed = []
    list_image_data = []
    for dir in os.listdir(directory_source_str):
        dir_source = directory_source_str + dir + "/"
        page_link = directory_project_str + dir + ".html"
        project = GenerateProjectEntry(dir_source, page_link)
        for image_data in project.list_image_data:
            list_image_data.append(image_data)
        if IsProjectFinanced(project.project_type):
            if not project.project_completion_date:
                list_projects_ongoing.append(project)
            else:
                list_projects_completed.append(project)
        else:
            if not project.project_completion_date:
                list_student_projects_ongoing.append(project)
            else:
                list_student_projects_completed.append(project)   


    list_projects_ongoing = sorted(list_projects_ongoing, key=lambda project: project.project_title)
    list_projects_completed = sorted(list_projects_completed, key=lambda project: project.project_completion_date, reverse=True)
    list_student_projects_ongoing = sorted(list_student_projects_ongoing, key=lambda project: project.project_title)
    list_student_projects_completed = sorted(list_student_projects_completed, key=lambda project: project.project_completion_date, reverse=True)
    return list_projects_ongoing, list_projects_completed, list_student_projects_ongoing, list_student_projects_completed, list_image_data

def GenerateIndex(path_page, path_template, list_projects_ongoing, list_projects_completed):
    print("GenerateIndex:")
    print("path_page:", path_page)
    code = ReadContent(path_template)

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

    with open(path_page, "w", encoding="utf8") as f_out:
        f_out.write(code)

def GenerateProjectEntry(dir_source, page_link):
    tree = ET.parse(dir_source+"config.xml")
    root = tree.getroot()
    project_title = root.get("project_title")
    project_image = root.get("project_image")
    project_type = root.get("project_type")

    node_project_status = root.find("status")
    project_start_date = node_project_status.get("project_start_date")
    project_completion_date = node_project_status.get("project_completion_date")

    index_entry = ""
    if IsProjectFinanced(project_type):
        index_entry = ReadContent(project_entry_html_str)
    else:
        index_entry = ReadContent(project_entry_student_html_str)

    index_entry = index_entry.replace("$PROJECT_TITLE$", project_title)
    index_entry = index_entry.replace("$PROJECT_LINK$", page_link)
    index_entry = index_entry.replace("$PROJECT_TYPE$", project_type)
    image_path = "../"+placeholder_todo
    thumbnail_path = image_path
    if project_image:
        image_path = "../"+dir_source+project_image
        thumbnail_path = GetThumbnailPath(dir_source+project_image)
    index_entry = index_entry.replace("$PROJECT_THUMBNAIL$", thumbnail_path)

    node_authors = root.find("authors")
    code_authors = "["
    first_author = True
    for link in node_authors.findall("author"):
        name = link.get("name")
        href = link.get("href")
        if not first_author:
            code_authors += ", "
        author_code = name    
        if href:     
            author_code = ReadContent(author_html_str)
            author_code = author_code.replace("$AUTHOR_HREF$", href)
            author_code = author_code.replace("$AUTHOR_NAME$", name)
        code_authors += author_code        
        first_author = False        
    code_authors += "]"

    #if project_completion_date:
    #    if project_start_date:
    #        code_authors += "(" + project_start_date + " until " + project_completion_date + ")"
    #    else:
    #        code_authors += "(completed: " + project_completion_date + ")"

    if project_completion_date:
        code_authors += "(completed: " + project_completion_date + ")"

    index_entry = index_entry.replace("$AUTHORS$", code_authors)

    index_entry = Insert(index_entry, "$ABSTRACT_TEXT$", dir_source+"abstract.txt")



    node_images = root.find("images")
    gallery_images = ""
    list_image_data = []
    for image in node_images.findall("image"):
        file_name = image.get("file")
        if file_name:
            image_path = "../"+dir_source+file_name  
            image_description_path = (dir_source+file_name).replace(".png", ".txt")    
            image_description_path = image_description_path.replace(".jpg", ".txt")    
            thumbnail_path = GetThumbnailPath(dir_source+file_name)

            print("image_path", image_path)
            print("thumbnail_path", thumbnail_path)
            image_code = ReadContent(gallery_image_html_str)
            image_code = image_code.replace("$THUMBNAIL_FULL_PATH$", thumbnail_path)
            image_code = image_code.replace("$PROJECT_LINK$", page_link)
            image_code = image_code.replace("$PROJECT_TITLE$", project_title)
            #image_code = Insert(image_code, "$IMAGE_DESCRIPTION$", image_description_path)
            image_code = InsertText(image_code, "$IMAGE_DESCRIPTION$", "")
            gallery_images += image_code

            #image_description = Read(image_description_path)
            image_description = ""
            list_image_data.append(ImageData(project_title, image_description, page_link, image_path, thumbnail_path))

    project = Project(project_type, project_title, project_start_date, project_completion_date, index_entry, gallery_images, list_image_data)
    return project

#########################################################################################
#
#   GALLERY PAGE
#
#########################################################################################

def GenerateGallery(list_projects_ongoing, list_projects_completed, list_student_projects_ongoing, list_student_projects_completed):
    print("GenerateGallery:")
    path_gallery = "gallery.html"
    print("path_gallery:", path_gallery)
    code = ReadContent(template_gallery_html_str)

    code_images = ""
    for project in list_projects_ongoing:
        code_images += project.gallery_images
    for project in list_projects_completed:
        code_images += project.gallery_images
    for project in list_student_projects_ongoing:
        code_images += project.gallery_images
    for project in list_student_projects_completed:
        code_images += project.gallery_images

    code = code.replace("$GALLERY_ENTRIES$", code_images)

    with open(path_gallery, "w", encoding="utf8") as f_out:
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

    with open(path_videos, "w", encoding="utf8") as f_out:
        f_out.write(code)

#########################################################################################
#
#   RANDOM IMAGE PAGE
#
#########################################################################################

def GenerateRandomImage(list_image_data):
    print("GenerateRandomImage:")
    path_random_image = "random_image.html"
    print("path_random_image:", path_random_image)
    code = ReadContent(template_random_image_html_str)

    code_image_data = ""
    first = True
    for image_data in list_image_data:
        if not first:
            code_image_data += ","
        image_code = ReadContent(image_data_js_str)
        image_code = image_code.replace("$PROJECT_TITLE$", image_data.project_title)
        image_code = image_code.replace("$IMAGE_DESCRIPTION$", image_data.image_description)
        image_code = image_code.replace("$PROJECT_LINK$", image_data.project_link)
        image_code = image_code.replace("$IMAGE_FULL_PATH$", image_data.image_link)
        image_code = image_code.replace("$THUMBNAIL_FULL_PATH$", image_data.thumbnail_link)
        code_image_data += image_code
        first = False

    code = code.replace("$LIST_IMAGE_DATA$", code_image_data)

    print("")
    for image_data in list_image_data:
        print(image_data)

    with open(path_random_image, "w", encoding="utf8") as f_out:
        f_out.write(code)

#########################################################################################
#
#   MAIN
#
#########################################################################################

if __name__ == '__main__':
    GeneratePages()
    list_projects_ongoing, list_projects_completed, list_student_projects_ongoing, list_student_projects_completed, list_image_data = GenerateListProjects()
    print("ongoing:", list_projects_ongoing)
    print("completed:", list_projects_completed)
    print("student ongoing:", list_student_projects_ongoing)
    print("student completed:", list_student_projects_completed)
    GenerateIndex("index.html", template_index_html_str, list_projects_ongoing, list_projects_completed)
    GenerateIndex("student-projects.html", template_student_projects_html_str, list_student_projects_ongoing, list_student_projects_completed)
    GenerateGallery(list_projects_ongoing, list_projects_completed, list_student_projects_ongoing, list_student_projects_completed)
    GenerateVideos()
    GenerateRandomImage(list_image_data)