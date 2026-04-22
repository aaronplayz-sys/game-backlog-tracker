# main.py
# Entry point — console menu for the Game Backlog Tracker

from database import DatabaseManager
from tracker import BacklogTracker


def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def pause():
    input("\nPress Enter to continue...")


# =========================================================
# PLATFORM MENUS
# =========================================================

def menu_platforms(tracker):
    while True:
        print_header("PLATFORM MANAGEMENT")
        print("  1. View all platforms")
        print("  2. Add a platform")
        print("  3. Update a platform")
        print("  4. Delete a platform")
        print("  0. Back to main menu")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print_header("ALL PLATFORMS")
            platforms = tracker.get_all_platforms()
            if not platforms:
                print("No platforms found.")
            for p in platforms:
                print(p)
            pause()

        elif choice == "2":
            print_header("ADD PLATFORM")
            name = input("Platform name: ").strip()
            manufacturer = input("Manufacturer: ").strip()
            tracker.add_platform(name, manufacturer)
            pause()

        elif choice == "3":
            print_header("UPDATE PLATFORM")
            platforms = tracker.get_all_platforms()
            for p in platforms:
                print(p)
            try:
                pid = int(input("\nEnter platform ID to update: "))
                name = input("New name (leave blank to keep current): ").strip()
                mfr  = input("New manufacturer (leave blank to keep current): ").strip()
                tracker.update_platform(pid,
                                        name if name else None,
                                        mfr  if mfr  else None)
            except ValueError:
                print("Invalid ID.")
            pause()

        elif choice == "4":
            print_header("DELETE PLATFORM")
            platforms = tracker.get_all_platforms()
            for p in platforms:
                print(p)
            try:
                pid = int(input("\nEnter platform ID to delete: "))
                confirm = input("⚠ This will delete all related games and entries. Confirm? (y/n): ")
                if confirm.lower() == "y":
                    tracker.delete_platform(pid)
            except ValueError:
                print("Invalid ID.")
            pause()

        elif choice == "0":
            break


# =========================================================
# GAME MENUS
# =========================================================

def menu_games(tracker):
    while True:
        print_header("GAME MANAGEMENT")
        print("  1. View all games")
        print("  2. Add a game")
        print("  3. Update a game")
        print("  4. Delete a game")
        print("  0. Back to main menu")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print_header("ALL GAMES")
            games = tracker.get_all_games()
            if not games:
                print("No games found.")
            for g in games:
                print(f"[{g['game_id']}] {g['title']} ({g['release_year']}) "
                      f"| {g['genre']} | {g['platform_name']}")
            pause()

        elif choice == "2":
            print_header("ADD GAME")
            platforms = tracker.get_all_platforms()
            if not platforms:
                print("No platforms found. Add a platform first.")
                pause()
                continue
            print("\nAvailable Platforms:")
            valid_ids = []
            for p in platforms:
                print(f"  [{p.platform_id}] {p.name} ({p.manufacturer})")
                valid_ids.append(p.platform_id)
            try:
                title        = input("\nGame title: ").strip()
                genre        = input("Genre: ").strip()
                platform_id  = int(input(f"Platform ID {valid_ids}: "))
                if platform_id not in valid_ids:
                    print(f"Invalid platform ID. Choose from: {valid_ids}")
                    pause()
                    continue
                release_year = int(input("Release year: "))
                tracker.add_game(title, genre, platform_id, release_year)
            except ValueError:
                print("Invalid input.")
            pause()

        elif choice == "3":
            print_header("UPDATE GAME")
            games = tracker.get_all_games()
            for g in games:
                print(f"[{g['game_id']}] {g['title']}")
            try:
                gid   = int(input("\nEnter game ID to update: "))
                title = input("New title (blank to keep): ").strip()
                genre = input("New genre (blank to keep): ").strip()
                year  = input("New release year (blank to keep): ").strip()
                tracker.update_game(gid,
                                    title if title else None,
                                    genre if genre else None,
                                    None,
                                    int(year) if year else None)
            except ValueError:
                print("Invalid input.")
            pause()

        elif choice == "4":
            print_header("DELETE GAME")
            games = tracker.get_all_games()
            for g in games:
                print(f"[{g['game_id']}] {g['title']}")
            try:
                gid = int(input("\nEnter game ID to delete: "))
                confirm = input("⚠ This will also delete its backlog entry. Confirm? (y/n): ")
                if confirm.lower() == "y":
                    tracker.delete_game(gid)
            except ValueError:
                print("Invalid input.")
            pause()

        elif choice == "0":
            break


# =========================================================
# BACKLOG ENTRY MENUS
# =========================================================

def menu_backlog(tracker):
    while True:
        print_header("MY BACKLOG")
        print("  1. View full backlog")
        print("  2. Add game to backlog")
        print("  3. Update an entry")
        print("  4. Delete an entry")
        print("  0. Back to main menu")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print_header("FULL BACKLOG")
            entries = tracker.get_all_entries()
            if not entries:
                print("Your backlog is empty.")
            for e in entries:
                rating = e['personal_rating'] if e['personal_rating'] else "N/A"
                print(f"[{e['entry_id']}] {e['title']} ({e['platform_name']}) "
                      f"| {e['status']} | Rating: {rating}/10 "
                      f"| Hours: {e['hours_played']} | Added: {e['date_added']}")
                if e['notes']:
                    print(f"       Notes: {e['notes']}")
            pause()

        elif choice == "2":
            print_header("ADD TO BACKLOG")
            games = tracker.get_all_games()
            if not games:
                print("No games found. Add a game first.")
                pause()
                continue
            for g in games:
                print(f"[{g['game_id']}] {g['title']}")
            try:
                game_id = int(input("\nGame ID to add: "))
                print("Statuses: Backlog / Playing / Completed / Dropped")
                status  = input("Status (default: Backlog): ").strip() or "Backlog"
                rating  = input("Personal rating 1-10 (blank to skip): ").strip()
                hours   = input("Hours played (default: 0): ").strip()
                notes   = input("Notes (optional): ").strip()
                tracker.add_entry(
                    game_id,
                    status,
                    int(rating) if rating else None,
                    float(hours) if hours else 0.0,
                    notes
                )
            except ValueError:
                print("Invalid input.")
            pause()

        elif choice == "3":
            print_header("UPDATE BACKLOG ENTRY")
            entries = tracker.get_all_entries()
            for e in entries:
                print(f"[{e['entry_id']}] {e['title']} | {e['status']}")
            try:
                eid    = int(input("\nEntry ID to update: "))
                print("Statuses: Backlog / Playing / Completed / Dropped")
                status = input("New status (blank to keep): ").strip()
                rating = input("New rating 1-10 (blank to keep): ").strip()
                hours  = input("New hours played (blank to keep): ").strip()
                notes  = input("New notes (blank to keep): ").strip()
                tracker.update_entry(
                    eid,
                    status if status else None,
                    int(rating) if rating else None,
                    float(hours) if hours else None,
                    notes if notes else None
                )
            except ValueError:
                print("Invalid input.")
            pause()

        elif choice == "4":
            print_header("DELETE BACKLOG ENTRY")
            entries = tracker.get_all_entries()
            for e in entries:
                print(f"[{e['entry_id']}] {e['title']} | {e['status']}")
            try:
                eid = int(input("\nEntry ID to delete: "))
                confirm = input("Confirm delete? (y/n): ")
                if confirm.lower() == "y":
                    tracker.delete_entry(eid)
            except ValueError:
                print("Invalid input.")
            pause()

        elif choice == "0":
            break


# =========================================================
# MAIN ENTRY POINT
# =========================================================

def main():
    print_header("GAME BACKLOG TRACKER")
    print("  Powered by Python + SQLite")

    db = DatabaseManager()
    db.connect()
    db.create_tables()

    tracker = BacklogTracker(db.get_connection())

    while True:
        print_header("MAIN MENU")
        print("  1. Platforms")
        print("  2. Games")
        print("  3. My Backlog")
        print("  0. Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            menu_platforms(tracker)
        elif choice == "2":
            menu_games(tracker)
        elif choice == "3":
            menu_backlog(tracker)
        elif choice == "0":
            db.disconnect()
            print("\nGoodbye! 🎮")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()