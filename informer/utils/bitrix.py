import requests


class BitrixSender:

    def __init__(
        self,
        webhook_url: str,
        user_id: str,
        source_id: str,
        name: str = "",
        phone: str = "",
        email: str = "",
        order_id: str | int = "",
        message_body: str = "",
        extra_data: dict | None = None,
    ):
        self.webhook_url = webhook_url
        self.source_id = source_id
        self.user_id = user_id
        self.title = f"Заявка с сайта №{order_id}"
        self.name = name if name else f"Контакт #{phone}"
        self.phone = phone
        self.email = email
        self.message_body = message_body
        self.extra_data = extra_data if extra_data is not None else {}

    def send_request(self, method: str, data) -> dict:
        response = requests.post(
            f"{self.webhook_url}{method}/",
            headers={"Content-Type": "application/json"},
            json=data,
        )
        return response.json()

    @property
    def extra_utm_data(self) -> dict[str, str]:
        return {
            key: value
            for key, value in {
                "UTM_CAMPAIGN": self.extra_data.get("utm_campaign"),
                "UTM_CONTENT": self.extra_data.get("utm_content"),
                "UTM_MEDIUM": self.extra_data.get("utm_medium"),
                "UTM_SOURCE": self.extra_data.get("utm_source"),
                "UTM_TERM": self.extra_data.get("utm_term"),
                "UF_CRM_YM_UID": self.extra_data.get("ym_uid"),
                "UF_CRM_UBTCUID": self.extra_data.get("ubtcuid"),
            }.items()
            if value
        }

    def send_order(self):
        return self.lead_create()

    def lead_create(self):
        data = {
            "fields": {
                "TITLE": self.title,
                "TYPE_ID": "GOODS",
                "STATUS_ID": "NEW",
                "OPENED": "Y",
                "COMMENTS": self.message_body,
                **self.extra_utm_data,
            },
            "params": {"REGISTER_SONET_EVENT": "Y"},
        }
        if self.phone:
            data["fields"]["PHONE"] = [{"VALUE": self.phone, "VALUE_TYP": "WORK"}]
        if self.email:
            data["fields"]["EMAIL"] = [{"VALUE": self.email}]
        if self.source_id:
            data["fields"]["SOURCE_ID"] = self.source_id
        if self.user_id:
            data["fields"]["ASSIGNED_BY_ID"] = self.user_id
        return self.send_request("crm.lead.add", data)
