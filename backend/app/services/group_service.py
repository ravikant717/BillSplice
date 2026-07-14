import random 
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User

def generate_invite_code():

    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6,
        )
    )

def create_group(
    name: str,
    current_user: User,
    db: Session,
):

    group = Group(
        name=name,
        invite_code=generate_invite_code(),
        created_by=current_user.id,
    )

    db.add(group)
    db.commit()
    db.refresh(group)

    member = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
    )

    db.add(member)
    db.commit()

    return group

def get_groups(
    current_user: User,
    db: Session,
):

    groups = (
        db.query(Group)
        .join(
            GroupMember,
            Group.id == GroupMember.group_id,
        )
        .filter(
            GroupMember.user_id == current_user.id
        )
        .all()
    )

    return groups

def join_group(
    invite_code: str,
    current_user: User,
    db: Session,
):

    group = (
        db.query(Group)
        .filter(Group.invite_code == invite_code.upper())
        .first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    existing = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group.id,
            GroupMember.user_id == current_user.id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already a member",
        )

    member = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
    )

    db.add(member)
    db.commit()

    return {
        "message": "Joined successfully"
    }

def get_group_details(group_id, db: Session):

    group = (
        db.query(Group)
        .filter(Group.id == group_id)
        .first()
    )

    members = (
        db.query(User)
        .join(
            GroupMember,
            User.id == GroupMember.user_id,
        )
        .filter(
            GroupMember.group_id == group_id
        )
        .all()
    )

    return {
    "id": group.id,
    "name": group.name,
    "invite_code": group.invite_code,
    "members": [m.name for m in members],
}
    

def leave_group(
    group_id,
    current_user: User,
    db: Session,
):

    member = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == current_user.id,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Not a member of this group",
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Left group successfully"
    }