import csv
import json
from io import StringIO
from json import JSONDecodeError
from typing import Dict, List

import sentry_sdk
from flask import Flask, make_response, redirect, render_template, request, url_for
from pydantic import BaseModel, ValidationError
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(integrations=[FlaskIntegration()], traces_sample_rate=1.0)

app = Flask(__name__)


@app.route("/")
def index():
    error = None
    if request.args.get("error"):
        error = (
            "Huh, something is not right with the JSON input. Are you sure "
            "you copied the right object from the browser console?"
        )
    return render_template("index.html", error=error)


@app.route("/table", methods=["POST"])
def table():
    bookmarks_raw = request.form.get("bookmarks", "")
    try:
        bookmarks_json = json.loads(bookmarks_raw)
        bookmarks = parse_bookmarks(bookmarks_json)
    except (KeyError, TypeError, JSONDecodeError, ValidationError):
        return redirect(url_for("index", error="da"))

    return render_template(
        "table.html",
        bookmarks=bookmarks,
        bookmarks_raw=bookmarks_raw,
    )


@app.route("/export", methods=["POST"])
def export():
    bookmarks_raw = request.form["bookmarks"]
    try:
        bookmarks = parse_bookmarks(json.loads(bookmarks_raw))
        bookmarks_csv = bookmarks_to_csv(bookmarks)
    except (KeyError, TypeError, JSONDecodeError, ValidationError):
        return redirect(url_for("index", error="da"))
    output = make_response(bookmarks_csv)
    output.headers["Content-Disposition"] = "attachment; filename=bookmarks.csv"
    output.headers["Content-type"] = "text/csv"
    return output


class Bookmark(BaseModel):
    created_at: str
    id_str: str
    full_text: str
    user_id_str: str
    retweet_count: int
    favorite_count: int
    reply_count: int
    quote_count: int
    conversation_id_str: str
    lang: str


def parse_bookmarks(obj: Dict) -> List[Bookmark]:
    bookmarks = obj["globalObjects"]["tweets"].values()
    return [Bookmark(**record) for record in bookmarks]


def bookmarks_to_csv(bookmarks: List[Bookmark]) -> str:
    fields = [
        "created_at",
        "id_str",
        "full_text",
        "user_id_str",
        "retweet_count",
        "favorite_count",
        "reply_count",
        "quote_count",
        "conversation_id_str",
        "lang",
    ]
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for bookmark in bookmarks:
        writer.writerow(bookmark.dict())
    return output.getvalue()
