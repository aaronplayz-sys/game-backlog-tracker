# app.py
# Flask web application for the Game Backlog Tracker

from flask import Flask, render_template, request, redirect, url_for, flash
from database import DatabaseManager
from tracker import BacklogTracker
from media_tracker import MediaTracker

app = Flask(__name__)
app.secret_key = "backlog_tracker_secret"

# --- DB setup ---
db = DatabaseManager()
db.connect()
db.create_tables()
tracker = BacklogTracker(db.get_connection())
media_tracker = MediaTracker(db.get_connection())

# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def index():
    entries = tracker.get_all_entries()
    games   = tracker.get_all_games()
    stats = {"Backlog": 0, "Playing": 0, "Completed": 0, "Dropped": 0}
    for e in entries:
        stats[e["status"]] = stats.get(e["status"], 0) + 1
    return render_template("index.html", entries=entries, games=games, stats=stats)


# =========================================================
# PLATFORM ROUTES
# =========================================================

@app.route("/platforms")
def platforms():
    return render_template("platforms.html",
                           platforms=tracker.get_all_platforms())

@app.route("/platforms/add", methods=["POST"])
def platform_add():
    result = tracker.add_platform(request.form["name"],
                                  request.form["manufacturer"])
    flash("Platform added!" if result else "Platform already exists.", 
          "success" if result else "danger")
    return redirect(url_for("platforms"))

@app.route("/platforms/update/<int:pid>", methods=["POST"])
def platform_update(pid):
    tracker.update_platform(pid, request.form["name"],
                             request.form["manufacturer"])
    flash("Platform updated!", "success")
    return redirect(url_for("platforms"))

@app.route("/platforms/delete/<int:pid>", methods=["POST"])
def platform_delete(pid):
    tracker.delete_platform(pid)
    flash("Platform deleted.", "success")
    return redirect(url_for("platforms"))


# =========================================================
# GAME ROUTES
# =========================================================

@app.route("/games")
def games():
    return render_template("games.html",
                           games=tracker.get_all_games(),
                           platforms=tracker.get_all_platforms())

@app.route("/games/add", methods=["POST"])
def game_add():
    tracker.add_game(request.form["title"], request.form["genre"],
                     int(request.form["platform_id"]),
                     int(request.form["release_year"]))
    flash("Game added!", "success")
    return redirect(url_for("games"))

@app.route("/games/update/<int:gid>", methods=["POST"])
def game_update(gid):
    tracker.update_game(gid, request.form["title"], request.form["genre"],
                        int(request.form["platform_id"]),
                        int(request.form["release_year"]))
    flash("Game updated!", "success")
    return redirect(url_for("games"))

@app.route("/games/delete/<int:gid>", methods=["POST"])
def game_delete(gid):
    tracker.delete_game(gid)
    flash("Game deleted.", "success")
    return redirect(url_for("games"))


# =========================================================
# BACKLOG ROUTES
# =========================================================

@app.route("/backlog/add", methods=["POST"])
def backlog_add():
    rating = request.form.get("personal_rating")
    hours  = request.form.get("hours_played") or 0
    result = tracker.add_entry(
        int(request.form["game_id"]),
        request.form["status"],
        int(rating) if rating else None,
        float(hours),
        request.form.get("notes", "")
    )
    flash("Added to backlog!" if result else "Entry already exists for that game.",
          "success" if result else "danger")
    return redirect(url_for("index"))

@app.route("/backlog/update/<int:eid>", methods=["POST"])
def backlog_update(eid):
    rating = request.form.get("personal_rating")
    hours  = request.form.get("hours_played")
    tracker.update_entry(
        eid,
        request.form.get("status"),
        int(rating) if rating else None,
        float(hours) if hours else None,
        request.form.get("notes")
    )
    flash("Entry updated!", "success")
    return redirect(url_for("index"))

@app.route("/backlog/delete/<int:eid>", methods=["POST"])
def backlog_delete(eid):
    tracker.delete_entry(eid)
    flash("Entry removed from backlog.", "success")
    return redirect(url_for("index"))


# =========================================================
# MEDIA ROUTES (Movies & TV Shows)
# =========================================================

@app.route("/media")
def media():
    media_type = request.args.get("type")  # optional filter: movie / tv
    items = media_tracker.get_all_media(media_type)

    # Attach progress info for TV shows
    items_with_progress = []
    for item in items:
        item_dict = dict(item)
        if item_dict["media_type"] == "tv":
            item_dict["progress"] = media_tracker.get_progress(item_dict["media_id"])
        items_with_progress.append(item_dict)

    return render_template("media.html", items=items_with_progress,
                           active_filter=media_type)


@app.route("/api/tmdb-search")
def tmdb_search():
    """JSON endpoint used by the live search JS on the Media page."""
    query = request.args.get("q", "").strip()
    if len(query) < 2:
        return {"results": []}
    results = media_tracker.search_tmdb(query)
    return {"results": results}


@app.route("/media/add", methods=["POST"])
def media_add():
    result = media_tracker.add_media_item(
        int(request.form["tmdb_id"]),
        request.form["media_type"],
        request.form["title"],
        request.form.get("poster_path"),
        request.form.get("overview", ""),
        request.form.get("release_date")
    )
    flash(f"Added '{request.form['title']}'!" if result else "Already in your tracker.",
          "success" if result else "danger")
    return redirect(url_for("media"))


@app.route("/media/update/<int:media_id>", methods=["POST"])
def media_update(media_id):
    rating = request.form.get("personal_rating")
    media_tracker.update_media_item(
        media_id,
        request.form.get("status"),
        int(rating) if rating else None,
        request.form.get("notes")
    )
    flash("Updated!", "success")
    return redirect(url_for("media"))


@app.route("/media/delete/<int:media_id>", methods=["POST"])
def media_delete(media_id):
    media_tracker.delete_media_item(media_id)
    flash("Removed from tracker.", "success")
    return redirect(url_for("media"))


@app.route("/media/<int:media_id>")
def media_detail(media_id):
    """Show detail page — seasons and episodes for a TV show."""
    item = media_tracker.get_media_by_id(media_id)
    if not item:
        flash("Media item not found.", "danger")
        return redirect(url_for("media"))

    seasons_with_episodes = []
    if item["media_type"] == "tv":
        seasons = media_tracker.get_seasons_for_media(media_id)
        for season in seasons:
            episodes = media_tracker.get_episodes_for_season(season["season_id"])
            seasons_with_episodes.append({
                "season": season,
                "episodes": episodes
            })

    progress = media_tracker.get_progress(media_id) if item["media_type"] == "tv" else None

    return render_template("media_detail.html", item=item,
                           seasons=seasons_with_episodes, progress=progress)


@app.route("/episode/toggle/<int:episode_id>", methods=["POST"])
def episode_toggle(episode_id):
    media_tracker.toggle_episode_watched(episode_id)
    # Redirect back to the referring show page
    return redirect(request.referrer or url_for("media"))


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)