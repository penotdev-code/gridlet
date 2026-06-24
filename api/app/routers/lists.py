"""CRUD for word lists. Templates are lists with is_template=True."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_user
from ..models import User, WordList
from ..schemas import WordListCreate, WordListRead, WordListUpdate

router = APIRouter(prefix="/lists", tags=["lists"])


async def _get_owned(db: AsyncSession, user: User, list_id: int) -> WordList:
    obj = await db.get(WordList, list_id)
    if obj is None or obj.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liste introuvable")
    return obj


@router.get("", response_model=list[WordListRead])
async def list_lists(
    template: bool | None = Query(default=None, description="Filtrer modèles / listes"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[WordList]:
    stmt = select(WordList).where(WordList.user_id == user.id)
    if template is not None:
        stmt = stmt.where(WordList.is_template == template)
    stmt = stmt.order_by(WordList.updated_at.desc())
    return list((await db.execute(stmt)).scalars().all())


@router.post("", response_model=WordListRead, status_code=status.HTTP_201_CREATED)
async def create_list(
    data: WordListCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> WordList:
    obj = WordList(
        user_id=user.id,
        name=data.name,
        items=[item.model_dump() for item in data.items],
        gap=data.gap,
        is_template=data.is_template,
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{list_id}", response_model=WordListRead)
async def get_list(
    list_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> WordList:
    return await _get_owned(db, user, list_id)


@router.put("/{list_id}", response_model=WordListRead)
async def update_list(
    list_id: int,
    data: WordListUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> WordList:
    obj = await _get_owned(db, user, list_id)
    patch = data.model_dump(exclude_unset=True)
    if "items" in patch and patch["items"] is not None:
        patch["items"] = [
            item if isinstance(item, dict) else item.model_dump() for item in patch["items"]
        ]
    for key, value in patch.items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(
    list_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    obj = await _get_owned(db, user, list_id)
    await db.delete(obj)
    await db.commit()
