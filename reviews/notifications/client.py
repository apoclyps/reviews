from os import path
from pathlib import Path
from typing import Optional, Union

from notifypy import Notify

from reviews import config
from reviews.notifications.models import PullRequestNotification, Sound


class NotificationClient:
    """Notifiction Client provides a warpper and convience methods
    for sending desktop notifications.
    """

    def __init__(self) -> None:
        self.notification = Notify()
        self.application_name = "Code Review Manager"

    @staticmethod
    def _asset_exists(asset: str) -> Union[str, None]:
        """"Checks if an asset exists and returns the path (if it does)"""
        if asset_path := Path(path.join(config.DATA_PATH, asset)):
            if asset_path.exists():
                return str(asset_path)
        return None

    def _send_notification(
        self,
        title: str,
        message: str,
        icon: Optional[str] = None,
        audio: Optional[str] = None,
    ):
        """a generic wrapper around send notification."""
        self.notification.application_name = self.application_name
        self.notification.title = title
        self.notification.message = message
        if icon:
            if file_path := self._asset_exists(asset=icon):
                self.notification.icon = file_path
        if audio:
            if file_path := self._asset_exists(asset=audio):
                self.notification.audio = file_path

        self.notification.send(block=False)

    def send_pull_request_review(self, model: PullRequestNotification) -> bool:
        """sends a notification for a pull request review"""
        return self._send_notification(
            title="Pull request review",
            message=f"New review for {model.name} in {model.org}/{model.repository}",
            audio=Sound.SUCCESS.value,
        )

    def send_pull_request_approved(self, model: PullRequestNotification):
        """sends a notification for a pull request approved"""
        self._send_notification(
            title="Pull request approved",
            message=(
                f"{model.number} has been approved in {model.org}/{model.repository}"
            ),
            audio=Sound.SUCCESS.value,
        )

    def send_pull_request_merged(self, model: PullRequestNotification):
        """sends a notification for a pull request merged"""
        self._send_notification(
            title="Pull request merged",
            message=f"{model.name} has been merged in {model.org}/{model.repository}",
            audio=Sound.FAILURE.value,
        )
