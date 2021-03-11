from notifypy import Notify
from typing import Optional

from dexi.notifications.domain import PullRequestNotification
from dexi.notifications.enums import Sound, Language

class Notification:

    @staticmethod
    def send_notification(application_name: str, title: str, message: str, icon: Optional[str], audio: Optional[str]):
        notification = Notify()

        notification.application_name = application_name
        notification.title = title
        notification.message = message
        notification.icon = icon if icon else None
        notification.audio = audio if audio else None

        notification.send(block=False)

    @staticmethod
    def send_pull_request_review(pr_info: PullRequestNotification):
        Notification.send_notification(
            application_name="dexi",
            title="Pull request review",
            message=f"New reivew for {pr_info.name} in {pr_info.org}/{pr_info.repository}",
            icon=pr_info.language.value,
            audio=Sound.SUCCESS.value
        )

    @staticmethod
    def send_pull_request_approved(pr_info: PullRequestNotification):
        Notification.send_notification(
            application_name="dexi",
            title="Pull request approved",
            message=f"{pr_info.name} has been approved in {pr_info.org}/{pr_info.repository}",
            icon=pr_info.language.value,
            audio=Sound.SUCCESS.value
        )

    @staticmethod
    def send_pull_request_merged(pr_info: PullRequestNotification):
        Notification.send_notification(
            application_name="dexi",
            title="Pull request merged",
            message=f"{pr_info.name} has been merged in {pr_info.org}/{pr_info.repository}",
            icon=pr_info.language.value,
            audio=Sound.FAILURE.value
        )
