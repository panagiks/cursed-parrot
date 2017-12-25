import sqlalchemy as sa

from aiopg.sa import create_engine
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


async def init_pg(app):
    settings = app['settings']['db']
    engine = await create_engine(
        **settings
    )
    app['db'] = engine
    # async with app['db'].acquire() as conn:
    #     await conn.execute(sa.schema.CreateTable(users_tbl))
    #     await conn.execute(sa.schema.CreateTable(oauth_providers_tbl))
    #     await conn.execute(sa.schema.DropTable(messages_tbl))
    #     await conn.execute(sa.schema.CreateTable(messages_tbl))


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def create_user(app, values):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            users_tbl.insert()
            .values(**values)
        )


async def update_user(app, old_tocken, values):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            users_tbl.update()
            .where(users_tbl.c.oauth_token == old_tocken)
            .returning(*users_tbl.c)
            .values(**values)
        )
    return (await result.fetchone())


async def complete_auth(app, token):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            users_tbl.delete()
            .where(users_tbl.c.oauth_token == token)
        )


async def get_user(app, username):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            users_tbl.select()
            .where(users_tbl.c.username == username)
        )
    return (await result.fetchone())


async def get_user_by_token(app, token):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            users_tbl.select()
            .where(users_tbl.c.oauth_token == token)
        )
    return (await result.fetchone())


async def create_oauth_provider(app, values):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            oauth_providers_tbl.insert()
            .values(**values)
        )


async def get_oauth_provider(app, name):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            oauth_providers_tbl.select()
            .where(oauth_providers_tbl.c.name == name)
        )
    return (await result.fetchone())


async def create_message(app, values):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            messages_tbl.insert()
            .values(**values)
        )


async def get_message(app, uuid):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            messages_tbl.select()
            .where(messages_tbl.c.uuid == uuid)
        )
    return (await result.fetchone())


async def list_messages(app):
    async with app['db'].acquire() as conn:
        result = await conn.execute(
            messages_tbl.select()
        )
    return (await result.fetchall())


meta = sa.MetaData()


oauth_providers_tbl = sa.Table(
    'oauth_providers_tbl', meta,
    sa.Column('uuid', UUID, nullable=False, primary_key=True),
    sa.Column('name', sa.String(50), nullable=False),
    sa.Column('app_key', sa.String(100), nullable=False),
    sa.Column('app_secret', sa.String(100), nullable=False),

    sa.UniqueConstraint('name')
)

users_tbl = sa.Table(
    'users_tbl', meta,
    sa.Column('uuid', UUID, nullable=False, primary_key=True),
    sa.Column('username', sa.String(50)),
    sa.Column('oauth_token', sa.String(100), nullable=False),
    sa.Column('oauth_token_secret', sa.String(100), nullable=False),
    sa.Column('fullname', sa.String(200)),
    sa.Column(
        'created', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False
    ),
    sa.Column(
        'edited', sa.TIMESTAMP, server_default=sa.func.now(),
        onupdate=sa.func.now(), nullable=False
    )
)


messages_tbl = sa.Table(
    'messages_tbl', meta,
    sa.Column('uuid', UUID, nullable=False, primary_key=True),
    sa.Column('user', UUID, sa.ForeignKey('users_tbl.uuid'), nullable=False),
    sa.Column('private_key', sa.Text, nullable=False),
    sa.Column('ciphertext', sa.Text, nullable=False),
    sa.Column('expires', sa.TIMESTAMP, nullable=False)
)
