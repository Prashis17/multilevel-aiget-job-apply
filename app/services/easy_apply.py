from app.playwright.browser import BrowserAutomation
from app.schemas.workflow import JobLead


class EasyApplyService:
    async def apply(self, job: JobLead, answers: dict[str, str]) -> dict[str, str]:
        async with BrowserAutomation() as browser:
            page = await browser.new_page()
            await page.goto(str(job.url))
            if await self._captcha_detected(page):
                screenshot = await browser.screenshot(page, "captcha_pause")
                return {"status": "pending_human_captcha", "screenshot": screenshot}
            screenshot = await browser.screenshot(page, "application_page")
            return {"status": "ready_for_portal_adapter", "screenshot": screenshot}

    async def _captcha_detected(self, page) -> bool:
        content = (await page.content()).lower()
        return "captcha" in content or "verify you are human" in content

