
from synapsecord_bot.context.application import SynapseApplicationContext
from synapsecord_bot.context.command import SynapseContext

type SynapseAnyContext = (SynapseContext | SynapseApplicationContext)