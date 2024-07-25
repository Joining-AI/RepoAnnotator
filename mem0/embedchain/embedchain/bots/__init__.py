# 这里是从一个叫做 "embedchain" 的大盒子里拿出一个小盒子叫 "bots"，
# 然后从小盒子里面再拿出一个更小的盒子叫 "poe"，最后从这个更小的盒子里取出一个玩具叫 "PoeBot"。
# 我们把这个玩具放到我们的游戏空间里，但是因为我们暂时不需要用到它，
# 所以加上了一个特殊的标签 "noqa: F401"，告诉检查游戏规则的人可以忽略这个玩具。
from embedchain.bots.poe import PoeBot  # noqa: F401

# 接下来，我们还是从那个大盒子 "embedchain" 里面找到小盒子 "bots"，
# 再从小盒子里找到盒子 "whatsapp"，然后取出里面的玩具 "WhatsAppBot"。
# 同样地，我们把这个玩具也放在一边，并且用 "noqa: F401" 标签告诉别人先不用管它。
from embedchain.bots.whatsapp import WhatsAppBot  # noqa: F401

# 这一行是我们的计划，我们打算从 "embedchain" 大盒子里找到 "bots" 小盒子，
# 再找到 "discord" 盒子，然后取出里面的 "DiscordBot" 玩具。
# 但是现在我们遇到了一些问题，所以这里写上了 "TODO: fix discord import"，
# 意思是我们需要修复拿到 "DiscordBot" 玩具的方法。
# 由于现在还不能拿到这个玩具，所以我们没有写下具体的拿取方式。
# from embedchain.bots.discord import DiscordBot

