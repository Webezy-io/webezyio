from inquirer.themes import Theme, term

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

