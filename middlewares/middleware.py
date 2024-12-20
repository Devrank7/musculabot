import logging
from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from db.sql.service import run_sql, ReadUser, CreateUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        logger.debug(f"user_id: {event.from_user.id}")
        result = await run_sql(ReadUser(event.from_user.id))
        if result is None:
            logger.info("User not found, ok create it")
            result = await run_sql(CreateUser(event.from_user.id))
        data['user'] = result
        logger.info(f"User: {event.from_user.id}")
        return await handler(event, data)


class AuthMiddlewareCallback(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        logger.debug(f"user_id: {event.from_user.id}")
        result = await run_sql(ReadUser(event.from_user.id))
        if result is None:
            logger.info("User not found, ok create it")
            result = await run_sql(CreateUser(event.from_user.id))
        data['user'] = result
        logger.info(f"User: {event.from_user.id}")
        return await handler(event, data)
