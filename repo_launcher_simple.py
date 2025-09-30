#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import subprocess
import os
from pathlib import Path

def find_repos():
    """Find all git repositories"""
    repos = []
    try:
        result = subprocess.run(
            ['find', str(Path.home()), '-type', 'd', '-name', '.git', '-maxdepth', '4'],
            capture_output=True, text=True, timeout=10
        )
        
        for line in result.stdout.strip().split('\n'):
            if line:
                path = line.replace('/.git', '')
                name = os.path.basename(path)
                if name:
                    repos.append((name, path))
    except:
        pass
    
    return sorted(repos, key=lambda x: x[0].lower())

def open_repo(event):
    """Open selected repository in Claude Code"""
    selection = tree.selection()
    if selection:
        path = tree.item(selection[0])['values'][0]
        # Open Terminal.app and run claude in that directory
        script = f'''
        tell application "Terminal"
            activate
            do script "cd '{path}' && claude ."
        end tell
        '''
        subprocess.run(['osascript', '-e', script])

# Create window
root = tk.Tk()
root.title("Repository Launcher")
root.geometry("600x500")

# Search box
search_frame = tk.Frame(root)
search_frame.pack(fill='x', padx=10, pady=10)

tk.Label(search_frame, text="Search:").pack(side='left', padx=5)
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, width=40)
search_entry.pack(side='left')

# Repository list
tree = ttk.Treeview(root, columns=('Path',), show='tree')
tree.pack(fill='both', expand=True, padx=10, pady=10)

tree.column('#0', width=250)
tree.column('Path', width=350)

# Load repositories
all_repos = find_repos()

def display_repos(filter_text=''):
    tree.delete(*tree.get_children())
    for name, path in all_repos:
        if filter_text.lower() in name.lower() or filter_text.lower() in path.lower():
            tree.insert('', 'end', text=name, values=(path,))

# Search functionality
def filter_repos(*args):
    display_repos(search_var.get())

search_var.trace('w', filter_repos)

# Double-click to open
tree.bind('<Double-Button-1>', open_repo)

# Initial display
display_repos()

# Instructions
tk.Label(root, text="Double-click any repository to open in Claude Code", 
         fg='gray').pack(side='bottom', pady=5)

root.mainloop()