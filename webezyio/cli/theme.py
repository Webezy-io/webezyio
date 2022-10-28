from inquirer.themes import Theme, term

logo_ascii_art_color = """
                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| |\033[96m _\033[0m | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |\033[96m(_)\033[0m|_| \___/ 
                                   |___/              
"""
logo_ascii_art = """
                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| | _ | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |(_)|_| \___/ 
                                   |___/              
"""
class WebezyTheme(Theme):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.cyan
        self.Question.brackets_color = term.cyan
        self.Question.default_color = term.cyan
        self.Checkbox.selection_color = term.bold_black_on_bright_cyan
        self.Checkbox.selection_icon = "❯"
        self.Checkbox.selected_icon = "◉"
        self.Checkbox.selected_color = term.cyan
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "◯"
        self.List.selection_color = term.bold_black_on_bright_cyan
        self.List.selection_cursor = "❯"
        self.List.unselected_color = term.normal

