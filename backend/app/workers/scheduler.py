from apscheduler.schedulers.asyncio import AsyncIOScheduler


def build_scheduler() -> AsyncIOScheduler:
    """Build scheduler without starting it.

    Jobs should create their own SQLAlchemy Session per execution. Do not share request sessions or
    LangGraph node state across scheduled jobs.
    """

    return AsyncIOScheduler(timezone="Asia/Seoul")
