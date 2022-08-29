import csv
import os


class Database:
    _DATA_PATH = os.path.abspath(os.curdir) + '/Src/database/data/vegetables.csv'
    _BACKUP_PATH = os.path.abspath(os.curdir) + '/Src/database/data/vegetables.bkp'
    # _DATA_PATH = 'data/vegetables.csv'
    # _BACKUP_PATH = 'data/vegetables.bkp'

    def __init__(self):
        self.item_data = []
        self.read_up()

    def add_item(self, id_v: int, name: str, description: str, count: int) -> int:
        for item in self.item_data:
            if item['id'] == id_v:
                item['count'] += count
                return 1
        self.item_data.append(
            {
                'id': id_v,
                'name': name,
                'description': description,
                'count': count
            }
        )
        return 0

    def get_item(self, item_index):
        status = 'Ok'
        if item_index == 0:
            status = 'low'
        elif item_index == len(self.item_data) - 1:
            status = 'high'
        return status, self.item_data[item_index]

    def pick_up_item(self, item_index: int, amt: int) -> [dict, str]:
        back = 'System fail'
        if self.item_data[item_index]['count'] <= 0:
            return f'Позиция {self.item_data[item_index]["name"]} закончилась.', 0
        elif self.item_data[item_index]['count'] > amt:
            back = self.item_data[item_index].copy()
            back.pop('count')
            self.item_data[item_index]['count'] -= amt
        elif self.item_data[item_index]['count'] <= amt:
            back = self.item_data[item_index].copy()
            amt = back.pop('count')
            self.item_data[item_index]['count'] = 0
        return back, amt

    # == still not in use
    # noinspection GrazieInspection
    def write_down(self, access_mode: str = 'r') -> None:  # USE CAREFULLY! This can rewrite the WHOLE FILE!!!
        """
        Once again: # USE CAREFULLY!!! This can rewrite the WHOLE FILE (at this stage)!!!
        :param access_mode: Access mode
        :return:
        """
        if os.path.exists(self._DATA_PATH):
            print('File exists. Making backup.')
            os.rename(self._DATA_PATH, self._BACKUP_PATH)

        tmp = [['id', 'name', 'description', 'count']]
        for item in self.item_data:
            tmp.append([item['id'], item['name'], item['description'], item['count']])
        with open('data/vegetables.csv', access_mode, encoding='utf-8') as file_out:
            wd_writer = csv.writer(file_out)
            wd_writer.writerows(tmp)

    def read_up(self) -> None:
        """Read local csv base to item_data"""
        try:
            with open(self._DATA_PATH, 'r', encoding='utf-8') as file_in:
                wd_reader = csv.DictReader(file_in)
                for row in wd_reader:
                    self.add_item(int(row['id']), row['name'], row['description'], int(row['count']))
        except FileNotFoundError as exc:
            print(f'No DataBase found! {exc}')

    def get_showcase(self):
        showcase_out = ''
        for item in self.item_data:
            showcase_out += f"{item['name']} {item['description']} {item['count']} шт.\n"
        return showcase_out

    def search_item_by_name(self, line_in: str) -> tuple[int, dict or int]:
        item_index = 0
        for item in self.item_data:
            if line_in.lower() in item['name'].lower():
                return item_index, item
            item_index += 1
        return 0, 0


class BuyerBasket:
    def __init__(self) -> None:
        self.basket = {}

    def new(self, buyer_id: str) -> int:
        if buyer_id not in self.basket.keys():
            print('NNNEEEEEEEWWWWWWWWWw')
            self.basket[buyer_id] = []
            return 0
        else:
            return 1

    def add_item(self, buyer_id, item: dict) -> str:
        for own_item in self.basket[buyer_id]:
            print('KEYS:', item['id'], own_item.keys(), type(item['id']), type(own_item.keys()))
            if item['id'] in own_item.keys():
                own_item['amt'] += item['amt']
                return f'Кол-во позиции {item["name"]} теперь {own_item["amt"]} шт.'
        else:
            self.basket[buyer_id].append(item)
            return f'Добавлена позиция {item["name"]}, {item["amt"]} шт.'

    def show_basket(self, buyer_id: str) -> str:
        out_line = ''
        if self.basket[buyer_id]:
            for item in self.basket[buyer_id]:
                out_line += f'item id: {item["name"]}\namount: {item["amt"]}' \
                            f'\n{"="*40}\n'
        else:
            out_line = 'Ваша корзинка всё ещё пуста. Положите в нее что-нибудь нужное.'

        return out_line

    def show_position(self, buyer_id: str, pos: int):
        if not self.basket[buyer_id]:
            return 'Ваша корзинка всё ещё пуста. Положите в нее что-нибудь нужное.'
        else:
            return self.basket[buyer_id][pos]

    def empty_basket(self, buyer_id: str) -> [list, str]:
        if not self.basket[buyer_id]:
            return 'Ваша корзинка всё ещё пуста. Положите в нее что-нибудь нужное.'
        local_pack = self.basket[buyer_id]
        self.basket[buyer_id] = []
        return local_pack

    def remove_item(self, buyer_id: str, pos: int) -> [list, str]:
        if not self.basket[buyer_id]:
            return 'Ваша корзинка всё ещё пуста. Положите в нее что-нибудь нужное.'
        rmv_item = self.basket[buyer_id].pop(pos)
        return rmv_item

    def __str__(self) -> str:
        return str(self.basket.keys())


if __name__ == '__main__':
    tester = Database()
    print(os.path.abspath(os.curdir))
    print(tester.get_showcase())
