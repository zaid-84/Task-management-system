from app.services.supabase_service import supabase


def sync_user(auth_user):
    user_id = auth_user.id
    email = auth_user.email

    metadata = auth_user.user_metadata or {}

    name = (
        metadata.get("full_name")
        or metadata.get("name")
        or email.split("@")[0]
    )

    avatar_url = (
        metadata.get("avatar_url")
        or metadata.get("picture")
    )

    user_data = {
        "id": user_id,
        "google_id": user_id,
        "name": name,
        "email": email,
        "avatar_url": avatar_url
    }

    response = (
        supabase
        .table("users")
        .upsert(
            user_data,
            on_conflict="id"
        )
        .execute()
    )

    return response.data