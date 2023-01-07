import datetime

from repositories.base import BaseRepository
from db.jobs import jobs
from models.jobs import Job, JobIn


class JobRepository(BaseRepository):

    async def create(self, user_id: int, job_in: JobIn) -> Job:
        dt_now = datetime.datetime.utcnow()
        job = Job(
            id=0,
            user_id=user_id,
            created_at=dt_now,
            updated_at=dt_now,
            title=job_in.title,
            description=job_in.description,
            salary_from=job_in.salary_from,
            salary_to=job_in.salary_to,
            is_active=job_in.is_active,
        )
        values = {**job.dict()}
        values.pop("id", None)
        query = jobs.insert().values(**values)
        job.id = await self.database.execute(query=query)
        return job

    async def update(self, job_id: int, user_id: int, job_in: JobIn):
        dt_now = datetime.datetime.utcnow()
        job = Job(
            id=job_id,
            user_id=user_id,
            created_at=dt_now,
            updated_at=dt_now,
            title=job_in.title,
            description=job_in.description,
            salary_from=job_in.salary_from,
            salary_to=job_in.salary_to,
            is_active=job_in.is_active,
        )
        values = {**job.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        query = jobs.update().where(jobs.c.id == job_id).values(**values)
        await self.database.execute(query=query)
        return job

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Job]:
        query = jobs.select().limit(limit).offset(offset)
        return await self.database.fetch_all(query=query)

    async def delete(self, job_id: int):
        query = jobs.delete().where(jobs.c.id == job_id)
        return await self.database.execute(query)

    async def get_by_id(self, job_id: int) -> Job | None:
        query = jobs.select().where(jobs.c.id == job_id)
        job = await self.database.fetch_one(query=query)
        if not job:
            return None
        return Job.parse_obj(job)

