from fastapi_amis_admin.admin import AdminSite, Settings

site = AdminSite(settings=Settings(database_url_async="postgresql+asyncpg://postgres:postgres@pg_db-2/postgres"))
