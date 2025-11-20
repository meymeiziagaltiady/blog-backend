from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.src.schema.content_schema import ContentCreate, ContentUpdate, ContentResponse
from app.src.schema.response_schema import ApiResponse
from app.src.db.database import get_db
from app.src.service.content_service import (
    create_content,
    get_all_user_content,
    get_content_by_id,
    update_content,
    delete_content,
)

router = APIRouter(prefix="/content", tags=["Content"])


# create new content
@router.post("/", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_new_content(
    payload: ContentCreate, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user

    content = create_content(db=db, payload=payload, user_id=user.id)

    return ApiResponse.success(
        data=ContentResponse.model_validate(content),
        message="Content created successfully",
        status_code=status.HTTP_201_CREATED,
    )


# get all content owned by logged in user
@router.get("/", response_model=ApiResponse)
def get_contents(request: Request, db: Session = Depends(get_db)):
    user = request.state.user

    contents = get_all_user_content(db=db, user_id=user.id)

    return ApiResponse.success(
        data=[ContentResponse.model_validate(c) for c in contents],
        message="Content list retrieved successfully",
        status_code=status.HTTP_200_OK,
    )


# get a content by id
@router.get("/{content_id}", response_model=ApiResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    content = get_content_by_id(db=db, content_id=content_id)

    return ApiResponse.success(
        data=ContentResponse.model_validate(content),
        message="Content retrieved successfully",
        status_code=status.HTTP_200_OK,
    )


# update a content
@router.put("/{content_id}", response_model=ApiResponse)
def update_one(
    content_id: int,
    payload: ContentUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.state.user

    content = update_content(
        db=db,
        content_id=content_id,
        payload=payload,
        user_id=user.id,
        user_role=user.role,
    )

    return ApiResponse.success(
        data=ContentResponse.model_validate(content),
        message="Content updated successfully",
        status_code=status.HTTP_200_OK,
    )


# delete a content
@router.delete("/{content_id}", response_model=ApiResponse)
def delete_one(content_id: int, request: Request, db: Session = Depends(get_db)):
    user = request.state.user

    deleted = delete_content(
        db=db,
        content_id=content_id,
        user_id=user.id,
        user_role=user.role,
    )

    return ApiResponse.success(
        data=ContentResponse.model_validate(deleted),
        message="Content deleted successfully",
        status_code=status.HTTP_200_OK,
    )
