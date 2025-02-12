import tkinter as tk
import asyncio
import aiopylgtv
import os
import json
from wakeonlan import send_magic_packet

TV_IP = "192.168.0.17"
TV_MAC = "60:AB:14:3B:C3:64"
KEY_FILE = "tv_key.json"

# Load TV Key if it exists
TV_KEY = None
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "r") as f:
        tv_data = json.load(f)
        TV_KEY = tv_data.get("TV_KEY")

# Initialize client with the saved key
client = aiopylgtv.WebOsClient(TV_IP)
client.client_key = TV_KEY  # Assign saved key

async def connect_tv():
    """Connect to LG TV and save key if needed."""
    global client, TV_KEY

    try:
        await client.connect()
        print("✅ Connected to TV")

        # If we have a new key, save it
        if client.client_key and client.client_key != TV_KEY:
            TV_KEY = client.client_key  # Update the global variable
            with open(KEY_FILE, "w") as f:
                json.dump({"TV_KEY": TV_KEY}, f)
            print(f"🔑 TV Key Saved: {TV_KEY}")

    except Exception as e:
        print(f"❌ Connection failed: {e}")

async def send_command(cmd):
    """Send a command asynchronously."""
    try:
        await connect_tv()
        await cmd()
    except Exception as e:
        print(f"❌ Command failed: {e}")

def run_async_task(task):
    """Run async task safely from Tkinter without event loop errors."""
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, lambda: asyncio.run(task))

def power_on():
    """Send Wake-on-LAN magic packet to turn on the TV."""
    send_magic_packet(TV_MAC)
    print("📡 Sent Wake-on-LAN packet to TV")

def power_off():
    run_async_task(send_command(client.power_off))

def volume_up():
    run_async_task(send_command(client.volume_up))

def volume_down():
    run_async_task(send_command(client.volume_down))

def move_up():
    run_async_task(send_command(client.input_up))

def move_down():
    run_async_task(send_command(client.input_down))

def move_left():
    run_async_task(send_command(client.input_left))

def move_right():
    run_async_task(send_command(client.input_right))

def enter():
    run_async_task(send_command(client.input_enter))


### IPTV
async def launch_iptv():
    """Try different methods to launch IPTV Smarters Pro."""
    await connect_tv()
    try:
        apps = await client.get_apps()
        
        iptv_app_id = None
        iptv_system_id = None

        for app in apps:
            if "iptvsmarters" in app["id"].lower():
                iptv_app_id = app["launchPointId"]
                iptv_system_id = app["id"]  # Backup method
                break

        if iptv_app_id:
            try:
                await client.launch_app(iptv_app_id)
                print(f"✅ Successfully launched IPTV Smarters Pro with LaunchPoint ID: {iptv_app_id}")
            except:
                print("❌ Standard launch failed, trying alternative method...")
                await client.launch_app(iptv_system_id)  # Try system ID method

        else:
            print("❌ IPTV Smarters Pro app not found on TV!")

    except Exception as e:
        print(f"❌ Failed to launch IPTV Smarters Pro: {e}")


### YouTube

async def launch_youtube():
    await connect_tv()

    try:
        apps = await client.get_apps()

        youtube_app_id = None
        youtube_system_id = None

        for app in apps:
            if "youtube" in app["id"].lower():
                youtube_app_id = app["launchPointId"]
                youtube_system_id = app["id"]
                break
        
        if youtube_app_id:
            try:
                await client.launch_app(youtube_app_id)
                print("Launched")
            
            except Exception as e:
                print(f"Failed: {e}")

                await client.launch_app(youtube_system_id)
        else:
            print("App not found")
    except Exception as e:
        print(f"Failed: {e}")


async def launch_crunchyroll():
    await connect_tv()

    try:
        apps = await client.get_apps()

        crunchyroll_app_id = None
        crunchyroll_system_id = None

        for app in apps:
            if "crunchyroll" in app["id"].lower():
                crunchyroll_app_id = app["launchPointId"]
                crunchyroll_system_id = app["id"]
                break
        if crunchyroll_app_id:
            try:
                await client.launch_app(crunchyroll_app_id)
            except Exception as e:
                print(f"Failed: {e}")

                await client.launch_app(crunchyroll_system_id)
        else:
            print("App not found")
    
    except Exception as e:
        print(f"Failed: {e}")


# Create Tkinter GUI
root = tk.Tk()
root.title("LG TV Remote Control")
root.geometry("400x500")
root.configure(bg="black")

# Power Controls
power_frame = tk.Frame(root)
power_frame.configure(bg="black", padx=10, pady=10)
power_frame.pack(pady=10)


tk.Button(
    power_frame, 
    text="Power ON", 
    command=power_on, 
    width=10, 
    bg="green").pack()

tk.Button(
    power_frame, 
    text="Power OFF", 
    command=power_off,
    width=10, 
    bg="red").pack()

# Volume Controls
volume_frame = tk.Frame(root)
volume_frame.configure(bg="black")
volume_frame.pack(pady=10)
tk.Button(
    volume_frame, 
    text="Volume +",
    command=volume_up, 
    width=10).pack(side=tk.LEFT, padx=5)

tk.Button(
    volume_frame, 
    text="Volume -",
    command=volume_down, 
    width=10).pack(side=tk.RIGHT, padx=5)

# App Launcher
app_frame = tk.Frame(root)
app_frame.pack(pady=20)

tk.Button(
    app_frame, 
    text="YouTube", 
    command=lambda: run_async_task(launch_youtube()), width=10, 
    background="red",
    border=2, 
    padx=5, 
    pady=5).grid(row=0, column=0)

tk.Button(
    app_frame, 
    text="IPTV", 
    command=lambda: run_async_task(launch_iptv()), 
    width=10, 
    background="purple",
    border=2,
    padx=5, 
    pady=5).grid(row=0, column=1)

tk.Button(
    app_frame, 
    text="Crunchyroll", 
    command=lambda: run_async_task(launch_crunchyroll()),
    width=10,
    background="orangered",
    border=2,
    padx=5, 
    pady=5).grid(row=1, column=0)

tk.Button(
    app_frame,
    text="Twitch",
    command=None,
    width=10,
    background="pink",
    padx=5,
    pady=5,
).grid(row=1, column=1)


root.mainloop()
