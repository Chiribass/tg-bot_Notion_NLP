from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

import sys

sys.path.insert(0, "./test_add_page")
from pages_request import Pages

commands = ("/start", "/addpage", "/addcontent")


class UserState(StatesGroup):
    command = State()
    content = State()
    search_page = State()
    add_page_name = State()


class NotionBot:
    def __init__(self):
        self.storage = MemoryStorage()
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=self.storage)

    def run(self):
        @self.dp.message_handler(commands=["start"])
        async def start(message: types.Message):
            await self.bot.send_message(message.from_user.id, "начал")

            await UserState.command.set()

        @self.dp.message_handler(commands=["addpage"], state=UserState.command)
        async def start(message: types.Message):
            await self.bot.send_message(message.from_user.id, "введите название новой страницы")

            await UserState.add_page_name.set()

        @self.dp.message_handler(commands=["addcontent"], state=UserState.command)
        async def start(message: types.Message):
            await self.bot.send_message(message.from_user.id, "на какую страницу?")

            await UserState.search_page.set()

        @self.dp.message_handler(state=UserState.add_page_name)
        async def add_page(message: types.Message, state: FSMContext):
            name = message.text

            post = Pages()
            post.add_page(name)

            await self.bot.send_message(
                message.from_user.id,
                "добавлена страница " + str(post.new_page_url),
            )

            await UserState.command.set()

        @self.dp.message_handler(state=UserState.search_page)
        async def search_page(message: types.Message, state: FSMContext):
            if message.text not in commands:
                name = message.text

                post = Pages()
                post.search_in_db()

                searched_pages = {
                    pages["properties"]["Name"]["title"][0]["text"]["content"]: pages["id"]
                    for pages in post.results
                }

                if name in searched_pages:
                    await state.update_data(page_id=searched_pages[name])
                    await self.bot.send_message(
                        message.from_user.id,
                        "что написать на страницу " + name + "?",
                    )

                    await UserState.content.set()
                else:

                    await self.bot.send_message(message.from_user.id, "нет такой страницы")
            else:
                # FIXME: чтобы вернуться к командам, надо два раза ввести команду(чтобы не сработало условие и чтобы сработал декоратор)
                await self.bot.send_message(message.from_user.id, "еще раз")
                await UserState.command.set()

        @self.dp.message_handler(state=UserState.content)
        async def add_content(message: types.Message, state: FSMContext):

            if message.text not in commands:
                page_id = await state.get_data()
                page_id = page_id["page_id"]

                content = message.text

                post = Pages()
                post.add_content(page_id, content)

                await self.bot.send_message(message.from_user.id, "ok")
            else:
                # FIXME: чтобы вернуться к командам, надо два раза ввести команду(чтобы не сработало условие и чтобы сработал декоратор)
                await self.bot.send_message(message.from_user.id, "еще раз")
                await UserState.command.set()

        executor.start_polling(self.dp)
        


if __name__ == "__main__":
    bot = NotionBot()
    bot.run()
