#!/usr/bin/env python3
"""Build the INCF France static site from data_all.json. Output goes to docs/."""

import shutil
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

from parse_data import load_data

OUTPUT_DIR = Path("docs")
TEMPLATE_DIR = Path("site_templates")
STATIC_DIR = Path("static")
MEDIA_DIR = Path("media")

# Set this to your custom domain to write a CNAME file, or leave empty.
CUSTOM_DOMAIN = "www.neuroinfo.fr"


def render_md(text):
    if not text:
        return ""
    return markdown.markdown(text, extensions=["extra"])


def setup_output_dir():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()


def copy_assets():
    shutil.copytree(MEDIA_DIR, OUTPUT_DIR / "media")
    dst_static = OUTPUT_DIR / "static"
    dst_static.mkdir()
    shutil.copy(STATIC_DIR / "site.css", dst_static / "site.css")
    if CUSTOM_DOMAIN:
        (OUTPUT_DIR / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")


def write_page(env, template_name, output_path, **context):
    template = env.get_template(template_name)
    html = template.render(**context)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "index.html").write_text(html, encoding="utf-8")


def build(data):
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html"]),
    )

    for researcher in data["researchers"]:
        researcher["interests_en_html"] = render_md(researcher.get("interests_en", ""))
        researcher["interests_fr_html"] = render_md(researcher.get("interests_fr", ""))

    for project in data["projects"]:
        project["long_description_en_html"] = render_md(project.get("long_description_en", ""))
        project["long_description_fr_html"] = render_md(project.get("long_description_fr", ""))

    write_page(env, "home.html", OUTPUT_DIR)
    write_page(env, "about.html", OUTPUT_DIR / "about")
    write_page(env, "people.html", OUTPUT_DIR / "people", people=data["researchers"])

    for researcher in data["researchers"]:
        write_page(env, "person.html",
                   OUTPUT_DIR / "people" / researcher["id"],
                   person=researcher)

    write_page(env, "projects.html", OUTPUT_DIR / "projects", projects=data["projects"])

    for project in data["projects"]:
        write_page(env, "project.html",
                   OUTPUT_DIR / "projects" / project["id"],
                   project=project)

    write_page(env, "workshops.html", OUTPUT_DIR / "workshops" / "geant2019")

    # Simple 404 page
    template = env.get_template("base.html")
    html = template.render(
        title="Page not found",
        content="<h1>Page not found</h1><p><a href=\"/\">Return to home page</a></p>",
        block_content_is_raw=True,
    )
    # Use a dedicated 404 template instead
    tmpl_404 = env.from_string(
        "{% extends 'base.html' %}{% block content %}"
        "<h1>Page not found</h1><p><a href=\"/\">Return to home page</a></p>"
        "{% endblock %}"
    )
    (OUTPUT_DIR / "404.html").write_text(tmpl_404.render(), encoding="utf-8")


if __name__ == "__main__":
    data = load_data("data_all.json")
    setup_output_dir()
    copy_assets()
    build(data)
    page_count = sum(1 for _ in OUTPUT_DIR.rglob("*.html"))
    print(f"Built {page_count} pages → {OUTPUT_DIR}/")
