from app.core.config import settings

class SNSService:
    def get_google_auth_url(self) -> str:
        # TODO: Use google-auth-oauthlib to generate URL
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = "http://localhost:3000/auth/callback/google"
        scope = "https://www.googleapis.com/auth/youtube.upload"
        return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&access_type=offline"

    async def upload_video_to_youtube(self, video_url: str, title: str, description: str):
        # TODO: Implement upload logic using google-api-python-client
        pass

sns_service = SNSService()
