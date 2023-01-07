from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from endpoints.depends import get_job_repository, get_user_repository, get_current_user
from models.user import User
from repositories.jobs import JobRepository
from models.jobs import Job, JobIn


router = APIRouter()


@router.get("/", response_model=list[Job])
async def read_jobs(
        jobs: JobRepository = Depends(get_job_repository),
        limit: int = 100,
        offset: int = 0,
):
    return await jobs.get_all(limit=limit, offset=offset)


@router.post("/", response_model=Job)
async def create_job(
        job_in: JobIn,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
):
    return await jobs.create(user_id=current_user.id, job_in=job_in)


@router.put("/", response_model=Job)
async def update_job(
        job_id: int,
        job_in: JobIn,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
):
    job = await jobs.get_by_id(job_id)
    if job is None or job.user_id != current_user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job is not found")
    updated_job = await jobs.update(job_id=job_id, user_id=current_user.id, job_in=job_in)
    return updated_job


@router.delete("/", response_model=Job)
async def delete_job(
        job_id: int,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
):
    job = await jobs.get_by_id(job_id)
    not_found_exception = HTTPException(status.HTTP_404_NOT_FOUND, "Job is not found")
    if job is None or job.user_id != current_user.id:
        raise not_found_exception
    await jobs.delete(job_id)
    return {"status": True}
