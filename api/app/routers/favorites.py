"""CRUD for favorite (saved) grids."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_user
from ..models import Favorite, User, WordList
from ..schemas import FavoriteCreate, FavoriteRead

router = APIRouter(prefix="/favorites", tags=["favorites"])


async def _get_owned(db: AsyncSession, user: User, fav_id: int) -> Favorite:
    obj = await db.get(Favorite, fav_id)
    if obj is None or obj.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favori introuvable")
    return obj


@router.get("", response_model=list[FavoriteRead])
async def list_favorites(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Favorite]:
    stmt = (
        select(Favorite)
        .where(Favorite.user_id == user.id)
        .order_by(Favorite.created_at.desc())
    )
    return list((await db.execute(stmt)).scalars().all())


@router.post("", response_model=FavoriteRead, status_code=status.HTTP_201_CREATED)
async def create_favorite(
    data: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Favorite:
    # If a list is referenced, make sure it belongs to the user.
    if data.list_id is not None:
        ref = await db.get(WordList, data.list_id)
        if ref is None or ref.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Liste référencée invalide"
            )
    obj = Favorite(user_id=user.id, name=data.name, list_id=data.list_id, grid=data.grid)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{fav_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    fav_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    obj = await _get_owned(db, user, fav_id)
    await db.delete(obj)
    await db.commit()
