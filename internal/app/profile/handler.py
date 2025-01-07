from fastapi import APIRouter, HTTPException, status

from internal.app.profile.usecase import ProfileUseCase, ProfileType


class ProfileHandler:
    def __init__(self, use_case: ProfileUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.router.add_api_route(
            "/{profile_type}/{profile_id}", self.profile, methods=["GET"])

    @staticmethod
    def __str_to_enum(profile_type: str) -> ProfileType:
        if profile_type == "shop":
            return ProfileType.SHOP
        elif profile_type == "user":
            return ProfileType.USER
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="invalid profile type")

    async def profile(self, profile_type: str, profile_id: int, is_public: str = None):
        return self.__use_case.get_profile_json(self.__str_to_enum(profile_type), profile_id, is_public)
