from app import app
from app.base_page_render import render_over_base_template


@app.route("/")
def main_page():
    return render_over_base_template("main_page.html")
