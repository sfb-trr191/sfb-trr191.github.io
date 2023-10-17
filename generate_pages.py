import os
import xml.etree.ElementTree as ET

directory_template_str = "template/"
directory_source_str = "source/"
directory_project_str = "project/"
template_html_str = directory_template_str + "template.html"
image_html_str = directory_template_str + "image.html"
link_html_str = directory_template_str + "link.html" 

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

    return code

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

if __name__ == '__main__':
    GeneratePages()