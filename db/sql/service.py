import datetime
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, literal_column, update, delete
from sqlalchemy.orm import selectinload, joinedload

from db.sql.connect import AsyncSessionMaker
from db.sql.enums.enums import Lang
from db.sql.model import User, WFPData


class SqlService(ABC):
    @abstractmethod
    async def run(self):
        raise NotImplementedError


class ReadUser(SqlService):

    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == literal_column(str(self.tg_id))).options(selectinload(User.wfp_data)))
            return user


class CreateUser(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            new_user = User(tg_id=self.tg_id)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user


class UpdateUserDate(SqlService):
    def __init__(self, tg_id: int, date_time: Optional[datetime.datetime] = None, debug: bool = False):
        self.tg_id = tg_id
        self.date_time = date_time
        self.debug = debug

    async def run(self):
        async with AsyncSessionMaker() as session:
            date_one_before_kill = self.date_time - (
                datetime.timedelta(minutes=1) if self.debug else datetime.timedelta(days=1))
            date_three_before_kill = self.date_time - (
                datetime.timedelta(minutes=2) if self.debug else datetime.timedelta(days=3))
            date_week_before_kill = self.date_time - (
                datetime.timedelta(minutes=3) if self.debug else datetime.timedelta(days=7))
            stmt = (
                update(User)
                .where(User.tg_id == literal_column(str(self.tg_id)))
                .values(
                    date_of_kill=self.date_time if self.date_time is not None else User.date_of_kill,
                    date_one_before_kill=date_one_before_kill,
                    date_three_before_kill=date_three_before_kill,
                    date_week_before_kill=date_week_before_kill,
                )
            )
            await session.execute(stmt)
            await session.commit()


class UpdateUserLang(SqlService):
    def __init__(self, tg_id: int, lang: Lang):
        self.tg_id = tg_id
        self.lang = lang

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(User)
                .where(User.tg_id == literal_column(str(self.tg_id)))
                .values(
                    lang=self.lang
                )
            )
            await session.execute(stmt)
            await session.commit()


class UpdateUserDateOnNone(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(User)
                .where(User.tg_id == literal_column(str(self.tg_id)))
                .values(
                    date_of_kill=None,
                    date_one_before_kill=None,
                    date_three_before_kill=None,
                    date_week_before_kill=None,
                )
            )
            await session.execute(stmt)
            await session.commit()


class UpdateUserDateBeforeWeekOnNone(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(User)
                .where(User.tg_id == literal_column(str(self.tg_id)))
                .values(
                    date_week_before_kill=None,
                )
            )
            await session.execute(stmt)
            await session.commit()


class UpdateUserDateThreeOnNone(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(User)
                .where(User.tg_id == literal_column(str(self.tg_id)))
                .values(
                    date_three_before_kill=None,
                )
            )
            await session.execute(stmt)
            await session.commit()


class UpdateUserDateOneOnNone(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(User)
                .where(User.tg_id == literal_column(str(self.tg_id)))
                .values(
                    date_one_before_kill=None,
                )
            )
            await session.execute(stmt)
            await session.commit()


class DeleteUser(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = delete(User).where(User.tg_id == literal_column(str(self.tg_id)))
            await session.execute(stmt)
            await session.commit()


class AllUsers(SqlService):
    async def run(self):
        async with AsyncSessionMaker() as session:
            users_scalar = await session.scalars(select(User).options(selectinload(User.wfp_data)))
            return users_scalar.all()


class UsersWithDateOfKill(SqlService):
    async def run(self):
        async with AsyncSessionMaker() as session:
            users_scalar = await session.scalars(
                select(User).where(User.date_of_kill.isnot(None))
            )
            return users_scalar.all()


class AttachWfpDataToUser(SqlService):

    def __init__(self, tg_id: int, order_id: str):
        self.tg_id = tg_id
        self.order_id = order_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == literal_column(str(self.tg_id))).options(selectinload(User.wfp_data)))
            if user.wfp_data:
                return user.wfp_data
            wfp_data = WFPData(order=self.order_id, user_id=user.tg_id)
            session.add(wfp_data)
            user.wfp_data = wfp_data
            await session.commit()
            return wfp_data


class DetachWfpDataFromUser(SqlService):

    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == literal_column(str(self.tg_id))).options(selectinload(User.wfp_data)))
            if user.wfp_data:
                wfp_data = user.wfp_data
                await session.delete(wfp_data)
                user.wfp_data = None
                await session.commit()
                return True
            return False


class CreateAndUpdateFullUser(SqlService):

    def __init__(self, tg_id: int, date_time: Optional[datetime.datetime] = None, debug: bool = False):
        self.tg_id = tg_id
        self.date_time = date_time
        self.debug = debug

    async def run(self):
        async with AsyncSessionMaker() as session:
            date_one_before_kill = self.date_time - (
                datetime.timedelta(minutes=1) if self.debug else datetime.timedelta(days=1))
            date_three_before_kill = self.date_time - (
                datetime.timedelta(minutes=2) if self.debug else datetime.timedelta(days=3))
            date_week_before_kill = self.date_time - (
                datetime.timedelta(minutes=3) if self.debug else datetime.timedelta(days=7))
            result = await session.execute(
                select(User)
                .options(joinedload(User.wfp_data))
                .where(User.tg_id == self.tg_id)
            )
            user = result.scalar_one_or_none()
            if user:
                user.date_one_before_kill = date_one_before_kill
                user.date_three_before_kill = date_three_before_kill
                user.date_week_before_kill = date_week_before_kill
                user.date_of_kill = self.date_time
            else:
                user = User(
                    tg_id=self.tg_id,
                    date_one_before_kill=date_one_before_kill,
                    date_three_before_kill=date_three_before_kill,
                    date_week_before_kill=date_week_before_kill,
                    date_of_kill=self.date_time,
                )
                session.add(user)
            await session.commit()


async def run_sql(runnable: SqlService):
    return await runnable.run()
