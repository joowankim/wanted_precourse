from fastapi import APIRouter, status, Depends

from src.member.application.member_application import MemberApplication, member_service
from src.member.domain.model.member_service import MemberService
from src.member.domain.model.membership_application import MembershipApplication

router = APIRouter(
    prefix="/members",
    tags=["member"]
)


def member_application(service: MemberService = Depends(member_service)):
    return MemberApplication(service=service)


@router.post("", status_code=status.HTTP_201_CREATED)
def register_member(application: MembershipApplication, member_app: MemberApplication = Depends(member_application)):
    member_app.register_member(application)
