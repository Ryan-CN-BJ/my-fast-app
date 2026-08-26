from userservice.service.base import BaseService
from dataclasses import dataclass

from userservice.model.setting_group import SettingGroup
from userservice.model.setting import Setting
from sqlalchemy import select
from sqlalchemy.orm import selectinload


@dataclass(frozen=True)
class SettingDef:
    key: str
    value: str
    display_name: str
    description: str


@dataclass(frozen=True)
class SettingGroupDef:
    key: str
    display_name: str
    description: str
    settings: list[SettingDef]


SETTING_GROUPS: list[SettingGroupDef] = [
    SettingGroupDef(
        key="aliyun_oss_config",
        display_name="阿里云oss配置",
        description="用于静态资源存储",
        settings=[
            SettingDef(
                key="OSS_ENDPOINT",
                value="oss-cn-beijing.aliyuncs.com",
                display_name="OSS_ENDPOINT",
                description="OSS_ENDPOINT",
            ),
            SettingDef(
                key="OSS_REGION_ID",
                value="cn-beijing",
                display_name="OSS_REGION_ID",
                description="OSS_REGION_ID",
            ),
            SettingDef(
                key="OSS_BUCKET_NAME",
                value="test-mrj",
                display_name="OSS_BUCKET_NAME",
                description="OSS_BUCKET_NAME",
            ),
            SettingDef(
                key="OSS_ACCESS_KEY_ID",
                value="***",
                display_name="OSS_ACCESS_KEY_ID",
                description="OSS_ACCESS_KEY_ID",
            ),
            SettingDef(
                key="OSS_ACCESS_KEY_SECRET",
                value="***",
                display_name="OSS_ACCESS_KEY_SECRET",
                description="OSS_ACCESS_KEY_SECRET",
            ),
            SettingDef(
                key="OSS_STS_ROLE_ARN",
                value="***",
                display_name="OSS_STS_ROLE_ARN",
                description="OSS_STS_ROLE_ARN",
            ),
        ],
    )
]


class SettingService(BaseService):
    async def initialize(self):
        result = await self.db.execute(
            select(SettingGroup).options(selectinload(SettingGroup.settings))
        )
        db_groups = list(result.scalars().all())

        # 根据SETTING_GROUPS更新settinggroup表
        for setting_group in SETTING_GROUPS:
            db_group = next(
                (
                    db_group
                    for db_group in db_groups
                    if db_group.key == setting_group.key
                ),
                None,
            )
            if db_group:
                db_group.display_name = setting_group.display_name
                db_group.description = setting_group.description

                to_remove = [
                    s
                    for s in db_group.settings
                    if not any(sg.key == s.key for sg in setting_group.settings)
                ]
                for s in to_remove:
                    db_group.settings.remove(s)

                # for db_setting in db_group.settings:
                #     exist = any(
                #         setting
                #         for setting in setting_group.settings
                #         if setting.key == db_setting.key
                #     )
                #     if not exist:
                #         db_group.settings.remove(db_setting)

                for setting in setting_group.settings:
                    db_setting = next(
                        (
                            db_setting
                            for db_setting in db_group.settings
                            if setting.key == db_setting.key
                        ),
                        None,
                    )
                    if db_setting:
                        db_setting.description = setting.description
                        db_setting.display_name = setting.display_name
                    else:
                        db_group.settings.append(
                            Setting(
                                key=setting.key,
                                value=setting.value,
                                display_name=setting.display_name,
                                description=setting.description,
                            )
                        )

            else:
                db_group = SettingGroup(
                    key=setting_group.key,
                    display_name=setting_group.display_name,
                    description=setting_group.description,
                    settings=[
                        Setting(
                            key=s.key,
                            value=s.value,
                            display_name=s.display_name,
                            description=s.description,
                        )
                        for s in setting_group.settings
                    ],
                )
                self.db.add(db_group)
        await self.db.flush()

        # 删除数据库中存在但是SETTING_GROUPS不存在的
        db_groups_not_in_setting_groups = [
            db_group
            for db_group in db_groups
            if not any(
                db_group.key == setting_group.key for setting_group in SETTING_GROUPS
            )
        ]
        for db_group in db_groups_not_in_setting_groups:
            # for setting in db_group.settings:
            #     await self.db.delete(setting)
            await self.db.delete(db_group)
        await self.db.flush()
