import datetime

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import List, Tuple

proj_dir = Path.cwd().parent
archive_dir = proj_dir / 'SiteFiles'/ 'archive'
current_html = proj_dir / 'index.html'
templates_dir = Path.cwd() / 'templates'
resume_path = proj_dir / 'SiteFiles' / 'media' / 'AlexCatanzaroResume.txt'

SECTIONS = [
    "SKILLS AND KNOWLEDGE  ",
    "EXPERIENCE  ",
    "EDUCATION  "
]

REFERENCES = "References Available Upon Request "


def clean_resume(resume_content: str) -> str:
    """
    params: resume_content - raw uncleaned resume file contents
    returns: clean_res_content - cleaned file contents
    """
    trans_map = {
    '\t': ' ',
    '\n': ' ',
    '?': ' ',
    ':': ' '
    }
    trans_table = resume_content[0].maketrans(trans_map)

    return [item.translate(trans_table) for item in resume_content]


def build_html_section(section_header:str , res_slots: List[str]) -> str:
    """
    takes resume slots and builds HTML elements for file insertion
    """
    sh =  section_header.strip().lower()
    css_class = sh.lower().replace(' ', '-')
    container = [
        '<div class="resume-section"><ul class="desc-list">',
        f'<h3 class="{css_class}-header">{sh}</h3>',
        '<hr/>'
        ]
    container_bottom = "</ul></div>"
    list_items = [
        f"<li>{res_attr.strip()}</li>" 
        for res_attr
        in res_slots if res_attr not in ('', ' ')
    ]

    list_items.append(container_bottom)
    container.extend(list_items)

    return ''.join(container)


def stitch_resume(
    section_headers: Tuple[str],
     sections : Tuple[List[str]]
     ) -> str:
    skill_builder = ''
    for section_info in zip(section_headers, sections):
        header, info = section_info
        skill_builder += build_html_section(header, info)
    res_container = f'<div id="resume-container" class="resume-container"> {skill_builder} </div>'

    loader = FileSystemLoader(templates_dir)
    j_env = Environment(loader=loader)

    site_template = j_env.get_template('personal.html')
    refs = f"<div class='references'>{REFERENCES}</div>"

    return site_template.render(resume_section=res_container,references=refs)


def create_and_archive_html(new_html: str):
    tag = datetime.datetime.today().strftime('%m%d%Y')
    archive_html = archive_dir / f"index-{tag}.html"

    with open(current_html, 'r') as existing_html:
        current_contents = existing_html.readlines()

    with open(archive_html, 'w') as archived:
        archived.writelines(current_contents)
    
    with open(current_html, 'w') as updated_res:
        updated_res.writelines(new_html)


def extract_ref_line(clean_res_content):
    res_index = clean_res_content.index(REFERENCES)
    clean_res_content.pop(res_index)

if __name__ == "__main__":
    with open(resume_path, "r") as resume:
        resume_content = resume.readlines()
    crc = clean_resume(resume_content)
    extract_ref_line(crc)

    try:
        sk, ex, ed = [crc.index(item) for item in SECTIONS]
        print("Found sections!")
        skill_head, exp_head, edu_head = crc[sk], crc[ex], crc[ed]
        skills, experience, education = crc[sk+1: ex], crc[ex+1:ed], crc[ed+1:]
    except ValueError:
        print("Can't find sections")
        print(crc)

    html_output = stitch_resume(
        (skill_head, exp_head, edu_head),
        (skills, experience, education)
    )

    create_and_archive_html(html_output)

    print(f"All done! 🔮 {current_html}")
    
    
    