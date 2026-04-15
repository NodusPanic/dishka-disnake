# Dishka-Disnake Documentation

> **Note:** Before using `dishka-disnake`, it is recommended to familiarize yourself with the principles of **[Dishka](https://github.com/reagento/dishka)**, as this library builds on them while providing a Disnake-like interface.

`dishka-disnake` is a wrapper for Disnake that allows you to use all standard Disnake interactions (slash commands, user commands, message commands, buttons, selects, and modals) with a slightly different import structure and simplified setup.

---

## Installation

```bash
pip install dishka-disnake
```


## Setup
To initialize your bot with Dishka, you need to call `setup_dishka` **before creating your bot instance**. This ensures that all Dishka integrations are properly configured in the asynchronous container:

```py
from dishka import make_async_container, AsyncContainer
from dishka_disnake import setup_dishka
from disnake.ext.commands import Bot

# Create the async container for your bot
container: AsyncContainer = make_async_container(...)

async def main():
    # Setup Dishka integration on the container before creating the bot
    setup_dishka(container)

    # Now you can create your bot instance
    bot = Bot(...)

    # Start your bot
    await bot.start("YOUR_BOT_TOKEN")
```
`setup_dishka(async_container)` prepares your async container so that commands, buttons, selects, and modals work correctly with Dishka.

---

## Commands
`dishka-disnake` supports all standard Disnake command types(only cogs):

---

### Slash Commands
```py
from dishka_disnake.commands import slash_command

class HelloCog(Cog)

    @slash_command(name="hello", description="Say hello")
    async def hello_command(interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```


### UserCommands
```py
from dishka_disnake.commands import user_command

class HelloCog(Cog)

    @user_command(name="hello", description="Say hello")
    async def hello_command(interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```


### MessageCommands
```py
from dishka_disnake.commands import message_command

class HelloCog(Cog)

    @message_command(name="hello", description="Say hello")
    async def hello_command(interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```

---

## Components
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



### Modals
```py
from disnake import ModalInteraction
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

---

## Notes
- The usage of commands, buttons, selects, and modals is identical to Disnake.
- The main difference is the import path (`from dishka_disnake` instead of `from disnake`).
- Make sure to call `setup_dishka` **before initializing your bot**, passing the asynchronous container to properly configure Dishka integration.

---

This documentation should provide a solid starting point for using dishka-disnake while keeping all the familiar patterns from Disnake.
