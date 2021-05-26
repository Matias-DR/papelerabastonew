from record_list import (RecordList, StockList, SaleList, BuyList, FileManager)
from PySimpleGUI import (
    T, theme, Window, Column, Frame, Tab, TabGroup, Button, SaveAs, Input,
    Combo, Spin, Radio, Text
)
import constants as cs
from multiprocessing import Process

MAIN = None


class Section(Column):
    __key = None
    __instance = None

    @classmethod
    def instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def get_index_name_size(cls) -> tuple:
        return cls._INDEX_NAME_SIZE

    @classmethod
    def get_cleaner_options(cls) -> list:
        return cls._CLEANER_OPTIONS

    @classmethod
    def get_key(cls) -> str:
        return cls.__key

    @classmethod
    def key(cls, key):
        cls.__key = key

    def __init__(self, size: tuple, pad: tuple):
        super().__init__(layout=self.render_layout(), size=size, pad=pad)

    def __len__(self) -> int:
        return len(self.get_record_list())

    def render_finder(self) -> list:
        return [
            Input(
                key=self.__key + cs.FINDER_INPUT_KEY,
                size=cs.FINDER_INPUT_SIZE,
                pad=cs.FINDER_INPUT_PAD
            ),
            Button(
                key=self.__key + cs.FINDER_BUTTON_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.FINDER_BUTTON_PAD,
                button_text=cs.FINDER_BUTTON_TEXT,
                tooltip=cs.FINDER_BUTTON_TOOLTIP
            )
        ]

    def render_sorter(self) -> list:
        sort_values = self.get_sort_values()
        return [
            Combo(
                key=self.__key + cs.SORTER_COMBO_KEY,
                values=sort_values,
                default_value=sort_values[0],
                size=cs.SORTER_COMBO_SIZE,
                pad=cs.SORTER_COMBO_PAD,
                tooltip=cs.SORTER_COMBO_TOOLTIP,
                readonly=True
            ),
            Button(
                key=self.__key + cs.SORTER_BUTTON_UP_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.SORTER_BUTTON_PAD,
                button_text=cs.SORTER_BUTTON_UP_TEXT,
                tooltip=cs.SORTER_BUTTON_UP_TOOLTIP
            ),
            Button(
                key=self.__key + cs.SORTER_BUTTON_DOWN_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.SORTER_BUTTON_PAD,
                button_text=cs.SORTER_BUTTON_DOWN_TEXT,
                tooltip=cs.SORTER_BUTTON_DOWN_TOOLTIP
            ),
        ]

    def render_cleaner(self) -> list:
        cleaner_options = self.get_cleaner_options()
        return [
            Combo(
                key=self.__key + cs.CLEANER_COMBO_KEY,
                size=cs.CLEANER_COMBO_SIZE,
                pad=cs.CLEANER_COMBO_PAD,
                values=cleaner_options,
                default_value=cleaner_options[0],
                readonly=True
            ),
            Button(
                key=self.__key + cs.CLEANER_BUTTON_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.CLEANER_BUTTON_PAD,
                button_text=cs.CLEANER_BUTTON_TEXT,
                tooltip=cs.CLEANER_BUTTON_TOOLTIP
            )
        ]

    def render_apply(self) -> list:
        return [
            Button(
                key=self.__key + cs.APPLY_BUTTON_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.APPLY_BUTTON_PAD,
                button_text=cs.APPLY_BUTTON_TEXT,
                tooltip=cs.APPLY_BUTTON_TOOLTIP
            )
        ]

    def render_base_index(
        self, input_size: tuple, input_pad: tuple, default_text: str
    ) -> list:
        index = [
            [
                Input(
                    size=input_size,
                    pad=input_pad,
                    default_text=default_text,
                    readonly=True
                )
            ]
        ]
        return [
            Column(
                layout=index,
                pad=cs.INDEX_COLUMN_PAD,
                element_justification='center'
            )
        ]

    def render_name_index(self) -> list:
        return self.render_base_index(
            self.get_index_name_size(), cs.INDEX_INPUT_NAME_PAD,
            cs.INDEX_INPUT_NAME_TEXT
        )

    def render_unit_price_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_UNIT_PRICE_SIZE, cs.INDEX_INPUT_UNIT_PRICE_PAD,
            cs.INDEX_INPUT_UNIT_PRICE_TEXT
        )

    def render_stock_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_STOCK_SIZE, cs.INDEX_INPUT_STOCK_PAD,
            cs.INDEX_INPUT_STOCK_TEXT
        )

    def render_percent_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_PERCENT_SIZE, cs.INDEX_INPUT_PERCENT_PAD,
            cs.INDEX_INPUT_PERCENT_TEXT
        )

    def render_index(self) -> list:
        index = self.render_name_index()
        index += self.render_unit_price_index()
        index += self.render_stock_index()
        return index

    def render_record_list(self) -> list:
        return [self.get_record_list()]

    def render_save_as(self) -> list:
        return [
            SaveAs(
                key=self.__key + cs.SAVE_AS_BUTTON_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.SAVE_AS_BUTTON_PAD,
                button_text=cs.SAVE_AS_BUTTON_TEXT,
                tooltip=cs.SAVE_AS_BUTTON_TOOLTIP,
                file_types=(('', '.csv'), ),
                default_extension='.csv',
                initial_folder=cs.SAVE_AS_BUTTON_INITIAL_FOLDER,
                target=(555666777, +2),
            )
        ]

    def render_layout(self) -> list:
        """
        [
            [finder, sorter, cleaner, adder, save_as],
            [index, apply],
            [record_list]
        ]
        """
        layout = []
        layout.append(self.render_finder())
        layout[0] += self.render_sorter()
        layout[0] += self.render_cleaner()
        layout.append(self.render_index())
        layout[1] += self.render_apply()
        layout.append(self.render_record_list())
        return layout

    def callback(self, func: str) -> bool:
        if getattr(self, func)():
            return True
        return False


class StockAndBuySection:
    _CLEANER_OPTIONS = cs.STOCK_SECTION_CLEANER_OPTIONS

    def render_adder(self) -> list:
        return [
            Spin(
                key=self.get_key() + cs.ADDER_SPIN_KEY,
                size=cs.ADDER_SPIN_SIZE,
                pad=cs.ADDER_SPIN_PAD,
                values=cs.ADDER_SPIN_VALUES,
                initial_value=0,
                readonly=True
            ),
            Button(
                key=self.get_key() + cs.ADDER_BUTTON_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.ADDER_BUTTON_PAD,
                button_text=cs.ADDER_BUTTON_TEXT,
                tooltip=cs.ADDER_BUTTON_TOOLTIP
            )
        ]

    def add_records(self) -> bool:
        how_many_add = int(MAIN[self.get_key() + ',spin_adder'].get())
        self.get_record_list().add_records(how_many_add)
        if how_many_add > 0:
            return True
        return False


class StockSection(Section, StockAndBuySection):
    _INDEX_NAME_SIZE = cs.INDEX_INPUT_STOCK_NAME_SIZE

    @classmethod
    def get_sort_values(cls) -> list:
        return cs.SORTER_COMBO_STOCK_VALUES

    @classmethod
    def get_record_list(cls) -> StockList:
        return StockList.instance()

    def __init__(self):
        Section.__init__(self, cs.STOCKLIST_S_SIZE, cs.STOCKLIST_S_PAD)
        StockAndBuySection.__init__(self)

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_percent_index()
        return index

    def render_list(self) -> list:
        return [StockList.instance()]

    def render_layout(self) -> list:
        layout = super().render_layout()
        layout[0] += self.render_adder()
        layout[0] += self.render_save_as()
        return layout


class CommerceSection(Section):
    @classmethod
    def render_layout_in_tab(cls) -> Tab:
        layout = [[cls.instance()]]
        return Tab(
            cls.get_tab_title(),
            layout,
            pad=cs.TAB_PAD,
            border_width=cs.TAB_BORDER_WIDTH
        )

    def __init__(self, size: tuple, pad: tuple):
        super().__init__(size, pad)

    def render_amount_index(self) -> list:
        return super().render_base_index(
            cs.INDEX_INPUT_AMOUNT_SIZE, cs.INDEX_INPUT_AMOUNT_PAD,
            cs.INDEX_INPUT_AMOUNT_TEXT
        )

    def render_final_price_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_FINAL_PRICE_SIZE, cs.INDEX_INPUT_FINAL_PRICE_PAD,
            cs.INDEX_INPUT_FINAL_PRICE_TEXT
        )

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_amount_index()
        index += self.render_final_price_index()
        return index

    def render_commerce(self) -> list:
        return [
            Button(
                key=self.get_key() + cs.COMMERCE_BUTTON_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.COMMERCE_BUTTON_PAD,
                button_text=cs.COMMERCE_BUTTON_TEXT,
                tooltip=cs.COMMERCE_BUTTON_TOOLTIP
            )
        ]

    def render_total_price(self) -> list:
        return [
            Text(text='$'),
            Text(
                key=self.get_key() + cs.TOTAL_PRICE_KEY,
                size=cs.TOTAL_PRICE_SIZE,
                pad=cs.TOTAL_PRICE_PAD
            )
        ]

    def render_pre_visualizator(self) -> list:
        return [
            Button(
                key=self.get_key() + cs.PRE_VISULIZATOR_BUTTON_KEY,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.PRE_VISULIZATOR_BUTTON_PAD,
                button_text=cs.PRE_VISULIZATOR_BUTTON_TEXT,
                tooltip=cs.PRE_VISULIZATOR_BUTTON_TOOLTIP
            )
        ]

    def render_layout(self) -> list:
        """
        [
            [
                finder, sorter, cleaner, save_as,
                pre_visualizator, cs.total_price, commerce
            ],
            [index, apply],
            [record_list]
        ]
        """
        layout = super().render_layout()
        layout[0] += self.render_save_as()
        layout[0] += self.render_pre_visualizator()
        layout[0] += self.render_total_price()
        layout[0] += self.render_commerce()
        return layout


class SaleSection(CommerceSection):
    _INDEX_NAME_SIZE = cs.INDEX_INPUT_SALE_NAME_SIZE
    _CLEANER_OPTIONS = cs.SALE_SECTION_CLEANER_OPTIONS

    @classmethod
    def get_sort_values(cls) -> list:
        return cs.SORTER_COMBO_SALES_VALUES

    @classmethod
    def get_tab_title(cls) -> str:
        return 'VENTAS'

    @classmethod
    def get_record_list(self) -> RecordList:
        return SaleList.instance()

    def __init__(self):
        super().__init__(cs.SALELIST_S_SIZE, cs.SALELIST_S_PAD)

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_percent_index()
        return index


class BuySection(CommerceSection, StockAndBuySection):
    _INDEX_NAME_SIZE = cs.INDEX_INPUT_BUY_NAME_SIZE

    @classmethod
    def get_sort_values(cls) -> list:
        return cs.SORTER_COMBO_BUYS_VALUES

    @classmethod
    def get_tab_title(cls) -> str:
        return 'COMPRAS'

    @classmethod
    def get_record_list(cls):
        return BuyList.instance()

    def __init__(self):
        CommerceSection.__init__(
            self, cs.BUYSECTION_S_SIZE, cs.BUYSECTION_S_PAD
        )
        StockAndBuySection.__init__(self)

    def render_supplier_index(self) -> list:
        return CommerceSection.render_base_index(
            self, cs.INDEX_INPUT_SUPPLIER_SIZE, cs.INDEX_INPUT_SUPPLIER_PAD,
            cs.INDEX_INPUT_SUPPLIER_TEXT
        )

    def render_index(self) -> list:
        index = CommerceSection.render_index(self)
        index += self.render_supplier_index()
        index += self.render_percent_index()
        return index

    def render_layout(self) -> list:
        layout = CommerceSection.render_layout(self)
        adder = self.render_adder()
        layout[0].insert(6, adder[-1])
        layout[0].insert(6, adder[0])
        return layout


class Main(Window):
    def __init__(self):
        global MAIN
        MAIN = self
        FileManager.db_control()
        theme('PapelerAbasto')
        StockSection.key('StockSection.instance()')
        SaleSection.key('SaleSection.instance()')
        BuySection.key('BuySection.instance()')
        super().__init__(
            self.render_layout(),
            font=('Helvetica 16'),
            size=cs.WINDOWS_SIZE,
            location=cs.WINDOWS_LOCATION
        )
        self.run()

    def render_layout(self) -> list[list]:
        tab_group = [
            [
                SaleSection.render_layout_in_tab(),
                BuySection.render_layout_in_tab()
            ]
        ]
        layout = [
            [StockSection.instance()],
            [
                TabGroup(
                    tab_group,
                    pad=cs.TAB_GROUP_PAD,
                    border_width=cs.TAB_GROUP_BORDER_WIDTH
                )
            ]
        ]
        return layout

    def close(self, timeout=0):
        self.read(timeout=timeout)
        super().close()
        exit()

    def restart(self):
        Process(target=FileManager.restart).start()
        self.close(2000)

    def run(self):
        while True:
            e, _ = self.read()
            try:
                var, func = e.split(',')
                print('var: ', var, 'func: ,', func)
                if getattr(eval(var), 'callback')(func):
                    print('entrada')
                    self.restart()
            except:
                if e == None:
                    self.close()
                    break


if __name__ == '__main__':
    Main()
