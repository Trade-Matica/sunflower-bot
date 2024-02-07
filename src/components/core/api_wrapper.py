from datetime import datetime, timezone
import httpx, time, base64, json
from typing import List


class SessionID:
    def __init__(self, sessionId: str, farmId: int, deviceTrackerId: str) -> None:
        self.sessionId: str = sessionId
        self.farmId: int = farmId
        self.deviceTrackerId: str = deviceTrackerId


class Rest:
    def __init__(self, authorization: str, clientVersion: str) -> None:
        self.clientVersion = clientVersion
        self.client = httpx.Client(
            {
                "accept": "*/*",
                "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
                "authorization": authorization,
                "content-type": "application/json;charset=UTF-8",
                "origin": "https://sunflower-land.com",
                "referer": "https://sunflower-land.com/",
                "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            }
        )
        self.session: SessionID = None

    def __gatherTimestamp(self) -> str:
        return (
            datetime.utcfromtimestamp(
                int(time.time() * 1000) / 1000.0,
            )
            .replace(
                tzinfo=timezone.utc,
            )
            .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            + "Z"
        )

    def __wrapResponse(self, response: httpx.Response) -> dict:
        return (
            response.status_code,
            response.json(),
        )

    def getSession(self) -> dict:
        (code, data) = self.__wrapResponse(
            self.client.post(
                "https://api.sunflower-land.com/session",
                json={
                    "clientVersion": self.clientVersion,
                },
            ),
        )

        self.session = SessionID(
            sessionId=data["sessionId"],
            farmId=data["farmId"],
            deviceTrackerId=data["deviceTrackerId"],
        )

        return (
            code,
            data["farm"],
        )

    def plantCrops(self, crops: List[dict]) -> dict:
        """
        Usage:
            `plantCrops([{'seedName': 'carrot', 'index': '9'}])`

        Args:
            crops (List[dict]): list of crops to plant seeds on

        Returns:
            dict: (status_code, json)
        """

        actions = [].append(
            {
                "type": "seed.planted",
                "item": x["seedName"],
                "index": x["index"],
                "createdAt": self.__gatherTimestamp(),
            }
            for x in crops
        )

        return self.__wrapResponse(
            self.client.post(
                f"https://api.sunflower-land.com/autosave/{self.session.farmId}",
                json={
                    "deviceTrackerId": self.session.deviceTrackerId,
                    "clientVersion": self.clientVersion,
                    "sessionId": self.session.sessionId,
                    "actions": actions,
                    "cachedKey": base64.b64encode(
                        json.dumps(
                            {
                                "loggedInAt": int(time.time() * 1000),
                                "account": None,
                            }
                        ).encode("utf-8")
                    ).decode("utf-8"),
                },
            ),
        )

    def harvestCrops(self, index: list) -> dict:
        """
        Usage:
            `harvestCrops([1, "id", ...])`

        Args:
            index (list): list of crops to harvest

        Returns:
            dict: (status_code, json)
        """
        actions = [].append(
            {
                "type": "crop.harvested",
                "index": x,
                "createdAt": self.__gatherTimestamp(),
            }
            for x in index
        )

        return self.__wrapResponse(
            self.client.post(
                f"https://api.sunflower-land.com/autosave/{self.session.farmId}",
                json={
                    "deviceTrackerId": self.session.deviceTrackerId,
                    "clientVersion": self.clientVersion,
                    "sessionId": self.session.sessionId,
                    "actions": actions,
                    "cachedKey": base64.b64encode(
                        json.dumps(
                            {
                                "loggedInAt": int(time.time() * 1000),
                                "account": None,
                            }
                        ).encode("utf-8")
                    ).decode("utf-8"),
                },
            ),
        )
