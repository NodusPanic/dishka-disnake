"""
Disnake mini library with Dishka integration

Example:

---

### Slash Commands
```py
from dishka_disnake.commands import slash_command

class HelloCog(Cog)

    @slash_command(name="hello", description="Say hello")
    async def hello_command(interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```

---

### UserCommands
```py
from dishka_disnake.commands import user_command

class HelloCog(Cog)

    @user_command(name="hello", description="Say hello")
    async def hello_command(interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```

---

### MessageCommands
```py
from dishka_disnake.commands import message_command

class HelloCog(Cog)

    @message_command(name="hello", description="Say hello")
    async def hello_command(interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```

---

### Buttons
```py
from disnake import ui, MessageInteraction
from dishka_disnake.ui import Button, button


class MyButton(Button):
    def __init__(self):
        super().__init__(label="My Button", style=ButtonStyle.primary)

    async def callback(self, interaction: MessageInteraction, repo: FromDishka[UserRepo]):
        ...


class MyView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MyButton())

    @button(label="My Button")
    async def my_button_callback(self, interaction: MessageInteraction, repo: FromDishka[UserRepo]):
        ...

```

---

### Selects
```py
from disnake import ui, MessageInteraction, SelectOption
from dishka_disnake.ui import Select, select


class MySelect(Select):
    def __init__(self):
        super().__init__(placeholder="My Select", options=[
            SelectOption(label="Option 1", value="1"),
            SelectOption(label="Option 2", value="2"),
        ])

    async def callback(self, interaction: MessageInteraction, repo: FromDishka[UserRepo]):
        ...


class MyView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MySelect())

    @select(placeholder="My Select")
    async def my_select_callback(self, interaction: MessageInteraction, repo: FromDishka[UserRepo]):
        ...

```
similar with `UserSelect`, `RoleSelect`, `MentionableSelect`, `ChannelSelect` and `StringSelect`

---

### Modals
```py
from disnake import ui, ModalInteraction
from dishka_disnake.ui import Modal, modal


class MyModal(Modal):
    def __init__(self):
        super().__init__(title="My Modal", components=[
            TextInput(label="My Input", style=TextInputStyle.short),
            TextInput(label="My Input Description", style=TextInputStyle.paragraph),
        ])

    async def callback(self, interaction: ModalInteraction, repo: FromDishka[UserRepo]):
        ...
```
"""

__version__ = "0.1.6"
__author__ = "kipoha"


from dishka_disnake.cog import DishkaCog
from dishka_disnake.injector import inject, inject_loose, FromDishka
from dishka_disnake.setup import setup_dishka

__all__ = [
    "inject",
    "inject_loose",
    "setup_dishka",
    "FromDishka",
    "DishkaCog",
]
