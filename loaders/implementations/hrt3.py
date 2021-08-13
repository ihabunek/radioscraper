from loaders.implementations.common import hrt


async def load(session):
    return await hrt.load(session, 'PROGRAM3')
