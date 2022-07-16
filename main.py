import site
site.addsitedir("micropython")
site.addsitedir("bridge")

from simple_term_menu import TerminalMenu

options = ["badge", "fonts"]
terminal_menu = TerminalMenu(options)

print("Select which example to run:")
menu_entry_index = terminal_menu.show()
selected = options[menu_entry_index]
print("Loading",selected)

print("You can use following key to interact with the system")
print()
print("[Q]         [E]")
print("[A] [S] [D] [F]")
print("  ⬇ Maps to ⬇")
print("[User]      [Up]")
print("[A] [B] [C] [Down]")
print()

__import__(selected)