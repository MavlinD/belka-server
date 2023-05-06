from asgiref.sync import sync_to_async
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.log import LogScheme
from src.auth.users.exceptions import LogNotExists
from src.django_space.indicators.models import Indicator, Log


class LogManager:
    def __init__(self) -> None:
        self.objects = Log.objects

    async def create(self, payload: dict, ad: Indicator) -> LogScheme:
        """Вернуть или создать изображение"""
        image, _ = await self.objects.aget_or_create(**payload, ads_id=ad)
        return await sync_to_async(LogScheme.from_orm)(image)

    async def update(self, image: Log, payload: dict) -> Log:
        """update ind"""

        await self.objects.filter(pk=image.pk).aupdate(**payload)
        image: Log = await self.get_one_by_uniq_attr(image_id=image.pk)

        return image

    async def delete(self, ad: Log) -> None:
        """remove ind"""
        await self.objects.filter(pk=ad.pk).adelete()

    async def get_one_by_uniq_attr(self, image_id: int) -> Log | None:
        """get one ind by uniq attr"""
        image_in_db = await self.objects.filter(pk=image_id).afirst()
        if not image_in_db:
            raise LogNotExists(image=image_id)
        return image_in_db
