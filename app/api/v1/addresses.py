from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/", response_model=list[AddressResponse])
async def list_addresses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Address).where(Address.user_id == current_user.id))
    return result.scalars().all()


@router.post("/",  response_model=AddressResponse,  status_code=201)
async def create_address(
    data: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.is_default:
        await db.execute(
            Address.__table__.update()
            .where(Address.user_id == current_user.id)
            .values(is_default=False)
        )
    address = Address( 
        full_name = data.full_name,
        phone = data.phone,
        address_line1 = data.address_line1,
        address_line2 = data.address_line2,
        city = data.city,
        state = data.state,
        country = data.country,
        postal_code = data.postal_code,
        is_default = data.is_default,
        user_id = current_user.id
    )
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    data: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Address).where(Address.id == address_id, Address.user_id == current_user.id)
    )
    address = result.scalar_one_or_none()
    if not address:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Address not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}", status_code=204)
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Address).where(Address.id == address_id, Address.user_id == current_user.id)
    )
    address = result.scalar_one_or_none()
    if address:
        await db.delete(address)
