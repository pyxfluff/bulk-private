# pyxfluff 2024

import orjson

from time import sleep 
from rich.console import Console
from httpx import HTTPError, get, post

console = Console()

places = {}

cookie = input("Insert your FULL cookie header (read post) > ")
target_id = input("Enter your User ID > ")

with console.status("Fetching places..."):
    try:
        resp = get(
            url = f"https://apis.roblox.com/universes/v1/search?CreatorType=User&CreatorTargetId={target_id}&IsArchived=false&IsPublic=true&PageSize=500&SortParam=LastUpdated&SortOrder=Desc",
            headers = {
                "cookie": cookie,
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64; ArchLinux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Referer": "https://create.roblox.com/",
                "Origin": "https://create.roblox.com",
                "Accept": "application/json"
            },
            timeout = 3
        )

        resp.raise_for_status()
        places = resp.json()["data"]
        correct, index = [], 1

        for place in places:
            correct.append({
                "id": place["id"],
                "name": place["name"],
                "index": index
            })
            index += 1

        places = correct

    except (HTTPError, ValueError) as e:
        print(e)

console.print("""   
[blue]# Roblox bulk privater #[/blue]
[skyblue]pyxfluff 2024[/skyblue]
              
Welcome. Please enter the IDs of games you would like to [green]exclude[/green].
              
[red]This action cannot be undone once completed.[/red] When you are done, type [yellow]done[/yellow] to confirm.
""")

console.print_json(data=places)

while True:
    index

    try:
        index = input("Item to exclude (index number) >> ")
        index = int(index)
    except ValueError:
        if index.lower() == "done":
            break

        console.print("[red]This is not a number.[/red] Please enter a valid number or type [green]done[/green] to finish and confirm.")
        continue

    with console.status("Searching..."):
        for item in places:
            if item["index"] == index:
                console.print(f"[green]✓ {item["name"]} ({item["id"]}) has been removed[/green]")
                places.remove(item)

console.print("""[red]
Just to confirm, you are privating these games:
[/red]""")
console.print_json(data=places)
console.print("[red]You will not be able to undo this action without manually making them all public again. Continue? \[y/n]")

yn = input("> ")

if yn.lower() in ["no", "n"]:
    print("Exiting.")
    exit()
elif yn.lower() not in ["yes", "y"]:
    print("Unknown value, try again")
    exit()

with console.status("Privating games...") as status:
    resp = post(
            url = f"https://develop.roblox.com/v1/universes/{places[0]["id"]}/deactivate",
            headers = {
                "cookie": cookie,
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64; ArchLinux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Referer": "https://create.roblox.com/",
                "Origin": "https://create.roblox.com",
                "Accept": "application/json"
            },
            timeout = 2
        )

    token = resp.headers.get("X-CSRF-TOKEN")
    
    for game in places:
        status.update(f"Privating {game["name"]} ({game["id"]})")
        succeeded = False
        while not succeeded:
            try:
                resp = post(
                    url = f"https://develop.roblox.com/v1/universes/{game["id"]}/deactivate",
                    headers = {
                        "cookie": cookie,
                        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; ArchLinux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                        "Referer": "https://create.roblox.com/",
                        "Origin": "https://create.roblox.com",
                        "Accept": "application/json",
                        "X-CSRF-TOKEN": token
                    },
                    timeout = 2
                )

                resp.raise_for_status()
                token = resp.headers.get("X-CSRF-TOKEN")
                succeeded = True
            except HTTPError as e:
                status.update(f"[yellow]Privating {game["name"]} ({game["id"]}) failed, if you are seeing this a lot make sure you have a valid cookie! Ratelimits usually expire 30 seconds later.[/yellow]")
                print(e)
                sleep(10)
        
console.print("[green]✓ Done! All games are now private.[/green]\n\n These are now your public games:")

resp = get(
    url = f"https://apis.roblox.com/universes/v1/search?CreatorType=User&CreatorTargetId={target_id}&IsArchived=false&IsPublic=true&PageSize=500&SortParam=LastUpdated&SortOrder=Desc",
    headers = {
        "cookie": cookie,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; ArchLinux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Referer": "https://create.roblox.com/",
       "Origin": "https://create.roblox.com",
       "Accept": "application/json"
    },
    timeout = 3
)

console.print_json(data=resp.json()["data"])
