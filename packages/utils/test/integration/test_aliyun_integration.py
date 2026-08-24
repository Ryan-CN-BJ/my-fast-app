import httpx
from utils.aliyun import generate_upload_params


class TestAliyunUpload:
    async def test_upload(self):
        cred = await generate_upload_params("1.png")
        res = httpx.post(
            cred.host,
            data={
                "success_action_status": "200",
                "policy": cred["policy"],
                "x-oss-signature-version": cred["x-oss-signature-version"],
                "x-oss-signature": cred["signature"],
                "x-oss-credential": cred["x-oss-credential"],
                "x-oss-date": cred["x-oss-date"],
                "key": cred["key"],
                "x-oss-security-token": cred["x-oss-security-token"],
                "content-type": cred["content-type"],
            },
            files={"file": ("1.png", "123", cred.content_type)},
        )
        assert res.status == "200"
