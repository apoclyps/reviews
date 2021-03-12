from typing import Optional

from notifypy import Notify

from dexi.notifications.domain import PullRequestNotification
from dexi.notifications.enums import Sound


class NotificationClient:
    """Notifiction Client provides a warpper and convience methods for sending desktop notifications"""

    def __init__(self) -> None:
        self.notification = Notify()

    def _send_notification(
        self,
        application_name: str,
        title: str,
        message: str,
        icon: Optional[str] = None,
        audio: Optional[str] = None,
    ):
        """a generic wrapper around send notification."""
        self.notification.application_name = application_name
        self.notification.title = title
        self.notification.message = message
        self.notification.icon = icon
        self.notification.audio = audio

        self.notification.send(block=False)

    def send_pull_request_review(self, model: PullRequestNotification):
        """sends a notification for a pull request review"""
        self._send_notification(
            application_name="dexi",
            title="Pull request review",
            message=f"New review for {model.name} in {model.org}/{model.repository}",
            icon=model.language.value,
            audio=Sound.SUCCESS.value,
        )

    def send_pull_request_approved(self, model: PullRequestNotification):
        """sends a notification for a pull request approved"""
        self._send_notification(
            application_name="dexi",
            title="Pull request approved",
            message=f"{model.name} has been approved in {model.org}/{model.repository}",
            icon=model.language.value,
            audio=Sound.SUCCESS.value,
        )

    def send_pull_request_merged(self, model: PullRequestNotification):
        """sends a notification for a pull request merged"""
        self._send_notification(
            application_name="dexi",
            title="Pull request merged",
            message=f"{model.name} has been merged in {model.org}/{model.repository}",
            icon=model.language.value,
            audio=Sound.FAILURE.value,
        )
