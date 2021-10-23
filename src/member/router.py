from fastapi import APIRouter, status, Depends

from src.member.application.member_application import MemberApplication, member_repository
from src.member.domain.model.membership_application import MembershipApplication
from src.member.infra.member_repository import AbstractMemberRepository

router = APIRouter(
    prefix="/members",
    tags=["member"]
)


@router.get("/hello")
def hello():
    return "Hello member"


def member_application(repository: AbstractMemberRepository = Depends(member_repository)):
    return MemberApplication(repository=repository)


@router.post("", status_code=status.HTTP_201_CREATED)
def register_member(application: MembershipApplication, member_app: MemberApplication = Depends(member_application)):
    member_app.register_member(application)
