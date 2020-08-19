from matplotlib.ticker import StrMethodFormatter
from redbot.core import commands
from contextlib import closing
from itertools import cycle
import matplotlib.pyplot as plt
from io import BytesIO
import re
import requests
import csv
import codecs
import discord


class Predictit(commands.Cog):
    """predictit"""

    def get_predictit_graph(self, contract_id, title):
        url = f'https://www.predictit.org/Resource/DownloadMarketChartData?marketid={contract_id}&timespan=90d'
        d = {}
        colors = cycle(
            ["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red",
             "silver", "teal", "yellow"])
        markers = cycle(
            [".", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D",
             "d",
             "|", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.yaxis.tick_right()
        with closing(requests.get(url, stream=True)) as r:
            reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')
            for row in reader:
                d.setdefault(row['ContractName'], [])
                d[row['ContractName']].append(row)
        last_close_dict = {}
        for k in d:
            for list_item in d[k]:
                try:
                    last_close_dict[k] = float(list_item['CloseSharePrice'][1:])
                except ValueError:
                    last_close_dict[k] = 0
        sorted_last_close_dict = sorted(last_close_dict.items(), reverse=True, key=lambda xb: xb[1])
        for name in sorted_last_close_dict:
            x = []
            y = []
            for list_item in d[name[0]]:  # predictit removed a sortable datestring. this is a bandaid to give it back. D:
                date_time_str = list_item['Date']
                date_time_str = str.split(date_time_str, " ")[0]
                date_time_str = str.split(date_time_str, "/")
                n = 0
                for i in date_time_str:
                    if len(i) < 2:
                        date_time_str[n] = "0" + i
                    n += 1
                date_time_str = f"{date_time_str[0]}-{date_time_str[1]}"
                x.append(date_time_str)
                try:
                    y.append(float(list_item['CloseSharePrice'][1:]) * 100)
                except ValueError:
                    y.append(0)
            ax.plot(x, y, label=name[0], color=next(colors), marker=next(markers), markevery=7)
        plt.legend(frameon=False, bbox_to_anchor=(1.04, 1))
        plt.xticks(rotation=20)
        plt.tick_params(axis='both', labelsize=8, labelcolor='gray', pad=-5)
        plt.tick_params(axis='x', pad=-12)
        plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}¢'))  # remove y axis decimals
        every_nth = 7
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        for n, line in enumerate(ax.xaxis.get_ticklines()):
            line.set_visible(False)
        for n, line in enumerate(ax.yaxis.get_ticklines()):
            line.set_visible(False)
        plt.grid(axis="y", color='gray', alpha=.2)
        size = 8
        fig.set_size_inches(size * (1 + 5 ** 0.5) / 2, size)
        plt.title(label=title, loc="center",
                  fontdict={'fontweight': 'bold', 'size': 18, 'verticalalignment': 'baseline'})
        plt.tight_layout()
        graph_buf = BytesIO()
        plt.savefig(graph_buf, format='png')
        graph_buf.seek(0)
        return graph_buf

    @commands.command()
    async def predictit(self, ctx="", contract_ids="", message=""):
        try:
            if message == "":
                message = ctx.message
            await message.add_reaction("🐻")
            await message.channel.trigger_typing()
            make_a_link = True
            if message.content.startswith("!predictit"):
                contract_ids = re.findall(r'(\d+)', message.content)
            else:
                make_a_link = False
                print(type(contract_ids))
            if len(contract_ids) > 0:
                contract_ids = list(dict.fromkeys(contract_ids))
                for contract_id in contract_ids:
                    req = requests.get(f'https://www.predictit.org/api/marketdata/markets/{contract_id}').json()
                    if req is None:
                        await message.channel.send(f"Predictit returned no data for that contract id. You can get a contract's id from the contract's URL: <https://www.predictit.org/markets/detail/**4319**/Will-Donald-Trump-be-impeached-by-year-end-2019>")
                        return
                    message_list = [f"{message.author.mention}:", f"{req['name']}"]
                    if make_a_link:
                        message_list.append(f"<https://www.predictit.org/markets/detail/{req['id']}>")
                    message_list.append("```")
                    header = f"Contract ({req['id']})"
                    header = f"{header}{' ' * (20 - len(header))}LYP (CHANGE) BYP BNP"
                    message_list.append(header)
                    for contract in req['contracts']:
                        if contract['name'] == req['name']:
                            contract['name'] = ""
                        if len(contract['name']) > 19:
                            contract['name'] = f"{contract['name'][:16]}..."
                        contract_string = f"{contract['name']}"
                        if contract['lastTradePrice'] is None:
                            contract['lastTradePrice'] = 0
                        contract_string = f"{contract_string}{' ' * (20 - len(contract_string))}{str(contract['lastTradePrice'] * 100).split('.')[0]}¢"
                        if contract['lastClosePrice'] is None:
                            contract['lastClosePrice'] = 0
                        contract_string = f"{contract_string}{' ' * (25 - len(contract_string))}({str(contract['lastTradePrice'] * 100 - contract['lastClosePrice'] * 100).split('.')[0]}¢)"
                        if contract['bestBuyYesCost'] is None:
                            contract['bestBuyYesCost'] = 0
                        contract_string = f"{contract_string}{' ' * (33 - len(contract_string))}{str(contract['bestBuyYesCost'] * 100).split('.')[0]}¢"
                        if contract['bestBuyNoCost'] is None:
                            contract['bestBuyNoCost'] = 0
                        contract_string = f"{contract_string}{' ' * (37 - len(contract_string))}{str(contract['bestBuyNoCost'] * 100).split('.')[0]}¢"
                        if len("\n".join(message_list) + "\n" + contract_string) < 1996:
                            message_list.append(contract_string)
                        else:
                            message_list.append("```")
                            await message.channel.send("\n".join(message_list))
                            message_list = ['```', contract_string]
                    if message_list != "```":
                        message_list.append("```")
                    graph = self.get_predictit_graph(contract_id, req['name'])
                    temp_file = discord.File(fp=graph, filename=f"{contract_id}.png", spoiler=False)
                    await message.channel.send(content="\n".join(message_list), file=temp_file)
                    graph.close()
            else:
                req = requests.get(f'https://www.predictit.org/api/marketdata/all/').json()
                if req is None:
                    await message.channel.send("Predictit returned no data to search.")
                    return
                search_term = message.content[11:].lower()
                message_list = [f"{message.author.mention}:", f"Search results for `{search_term}`:", "```"]
                header = f"CONTRACT NAME (ID){' ' * 48}(ID)    LYP (CHANGE) BYP BNP"
                message_list.append(header)
                for market in req['markets']:
                    for contract in market['contracts']:
                        if search_term in contract['name'].lower() or search_term in market['name'].lower():
                            if contract['name'] != market['name']:
                                message_list.append(f"{market['name']}")
                            if len(contract['name']) > 65:
                                contract['name'] = f"{contract['name'][:62]}..."
                            if contract['lastTradePrice'] is None:
                                contract['lastTradePrice'] = 0
                            contract_string = f"{contract['name']}{' ' * (65 - len(contract['name']))}({market['id']})"
                            if contract['lastTradePrice'] is None:
                                contract['lastTradePrice'] = 0
                            contract_string = f"{contract_string}{' ' * (74 - len(contract_string))}{str(contract['lastTradePrice'] * 100).split('.')[0]}¢"
                            if contract['lastClosePrice'] is None:
                                contract['lastClosePrice'] = 0
                            contract_string = f"{contract_string}{' ' * (78 - len(contract_string))}({str(contract['lastTradePrice'] * 100 - contract['lastClosePrice'] * 100).split('.')[0]}¢)"
                            if contract['bestBuyYesCost'] is None:
                                contract['bestBuyYesCost'] = 0
                            contract_string = f"{contract_string}{' ' * (87 - len(contract_string))}{str(contract['bestBuyYesCost'] * 100).split('.')[0]}¢"
                            if contract['bestBuyNoCost'] is None:
                                contract['bestBuyNoCost'] = 0
                            contract_string = f"{contract_string}{' ' * (91 - len(contract_string))}{str(contract['bestBuyNoCost'] * 100).split('.')[0]}¢"
                            if len("\n".join(message_list) + "\n" + contract_string) < 1900:
                                message_list.append(contract_string)
                            else:
                                message_list.append("```")
                                await message.channel.send("\n".join(message_list))
                                message_list = ['```', contract_string]
                if message_list != "```":
                    message_list.append("```")
                await message.channel.send("\n".join(message_list))
        except Exception as e:
            print(e)  # need actual error handling
            await message.add_reaction("⚠")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != 565360489991897088:  # need the right way of getting the client user
            contract_ids = re.findall(r'predictit\.org/markets/detail/(\d+)', message.content)
            if len(contract_ids) > 0:
                await self.predictit(message=message, contract_ids=contract_ids)
