from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.tags.schemas import TagCreate


async def test_get_all_tags(async_client: AsyncClient):
    response = await async_client.get("/tags/all")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_post_tag(
    async_client: AsyncClient,
    test_tag_in_db: TagCreate,
):
    response = await async_client.post(
        "/tags/add",
        json=jsonable_encoder(test_tag_in_db),
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_post_tag_conflict(
    async_client: AsyncClient,
    test_tag_in_db: TagCreate,
):
    response = await async_client.post(
        "/tags/add",
        json=jsonable_encoder(test_tag_in_db),
    )
    assert response.status_code == status.HTTP_201_CREATED


    conflict_response = await async_client.post(
        "/tags/add",
        json=jsonable_encoder(test_tag_in_db),
    )
    assert conflict_response.status_code == status.HTTP_409_CONFLICT



async def test_delete_tag(
    async_client: AsyncClient,
    test_tag_in_db: TagCreate,
):
    create_response = await async_client.post(
        "/tags/add",
        json=jsonable_encoder(test_tag_in_db),
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    tag_id = create_response.json()["tag_id"]

    delete_response = await async_client.delete(f"/tags/{tag_id}")
    assert delete_response.status_code == status.HTTP_200_OK

    get_all_response = await async_client.get("/tags/all")
    if get_all_response.status_code == status.HTTP_200_OK:
        all_ids = [tag["tag_id"] for tag in get_all_response.json()]
        assert tag_id not in all_ids
    else:
        assert get_all_response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_tag_not_found(
    async_client: AsyncClient,
):
    import uuid
    fake_tag_id = uuid.uuid4()
    response = await async_client.delete(f"/tags/{fake_tag_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
