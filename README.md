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

## DishkaCog

`DishkaCog` is a base class for Cogs that automatically injects dependencies from the Dishka container into all supported handlers — no decorators needed.

Supported handler types:
- Slash commands (`@commands.slash_command`)
- User commands (`@commands.user_command`)
- Message commands (`@commands.message_command`)
- Prefix commands (`@commands.command`)
- Events (`@Cog.listener`)

```py
from dishka import FromDishka
from dishka_disnake import DishkaCog
from disnake import AppCmdInter
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

class MyCog(DishkaCog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Slash command — session is injected automatically
    @commands.slash_command(name="hello")
    async def hello(self, interaction: AppCmdInter, session: FromDishka[AsyncSession]):
        await interaction.response.send_message(f"Hello! {session}")

    # Prefix command — session is injected automatically
    @commands.command(name="ping")
    async def ping(self, ctx: Context, session: FromDishka[AsyncSession]):
        await ctx.send(f"Pong! {session}")

    # User command — session is injected automatically
    @commands.user_command(name="info")
    async def info(self, interaction: AppCmdInter, session: FromDishka[AsyncSession]):
        await interaction.response.send_message(f"Info! {session}")

    # Message command — session is injected automatically
    @commands.message_command(name="quote")
    async def quote(self, interaction: AppCmdInter, session: FromDishka[AsyncSession]):
        await interaction.response.send_message(f"Quote! {session}")

    # Listener event — session is injected automatically
    @Cog.listener("on_ready")
    async def on_ready(self, session: FromDishka[AsyncSession]):
        print(f"Ready! {session}")

def setup(bot: Bot):
    bot.add_cog(MyCog(bot))
```

### Subcommands and subcommand groups

`DishkaCog` also works with subcommands and subcommand groups:

```py
class MyCog(DishkaCog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def base(self, interaction: AppCmdInter):
        pass

    @base.sub_command()
    async def sub(self, interaction: AppCmdInter, session: FromDishka[AsyncSession]):
        await interaction.response.send_message(f"Sub! {session}")

    @commands.slash_command()
    async def group(self, _: AppCmdInter):
        pass

    @group.sub_command_group()
    async def subgroup(self, _: AppCmdInter):
        pass

    @subgroup.sub_command()
    async def nested(self, interaction: AppCmdInter, session: FromDishka[AsyncSession]):
        await interaction.response.send_message(f"Nested! {session}")
```

### Difference from `@inject`

If you only need injection on specific methods rather than the entire Cog, use the `@inject` decorator on individual methods in a regular `Cog` instead of inheriting from `DishkaCog`:

```py
from dishka_disnake import inject

class MyCog(Cog):

    @slash_command(name="hello")
    @inject
    async def hello(self, interaction: AppCmdInter, session: FromDishka[AsyncSession]):
        await interaction.response.send_message(f"Hello! {session}")
```

---

## Commands
`dishka-disnake` supports all standard Disnake command types (only cogs):

---

### Slash Commands
```py
from dishka_disnake.commands import slash_command

class HelloCog(Cog):

    @slash_command(name="hello", description="Say hello")
    async def hello_command(self, interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```

### UserCommands
```py
from dishka_disnake.commands import user_command

class HelloCog(Cog):

    @user_command(name="hello", description="Say hello")
    async def hello_command(self, interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
        ...
```

### MessageCommands
```py
from dishka_disnake.commands import message_command

class HelloCog(Cog):

    @message_command(name="hello", description="Say hello")
    async def hello_command(self, interaction: AppCmdInter, usecase: FromDishka[HelloUseCase]):
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
- `DishkaCog` automatically patches Disnake's parameter validation when imported, so no additional setup is required.
