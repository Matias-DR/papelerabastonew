from record_list import (RecordList, StockList, SaleList, BuyList, FileManager)
from PySimpleGUI import (
    theme, Window, Column, Frame, Tab, TabGroup, Button, SaveAs, Input, Combo,
    Spin, Radio, Text
)
from constants import (
    FINDER_INPUT_KEY, FINDER_INPUT_SIZE, FINDER_INPUT_PAD, FINDER_BUTTON_KEY,
    FINDER_BUTTON_PAD, FINDER_BUTTON_TEXT, FINDER_BUTTON_TOOLTIP,
    SORTER_BUTTON_UP_KEY, SORTER_BUTTON_DOWN_KEY, SORTER_BUTTON_PAD,
    SORTER_BUTTON_UP_TOOLTIP, SORTER_BUTTON_DOWN_TOOLTIP, CLEANER_COMBO_KEY,
    CLEANER_COMBO_SIZE, CLEANER_COMBO_PAD, CLEANER_BUTTON_KEY,
    CLEANER_BUTTON_PAD, CLEANER_BUTTON_TEXT, CLEANER_BUTTON_TOOLTIP,
    APPLY_BUTTON_KEY, APPLY_BUTTON_PAD, APPLY_BUTTON_TEXT, APPLY_BUTTON_TOOLTIP,
    INDEX_RADIO_SIZE, INDEX_RADIO_PAD, INDEX_COLUMN_PAD, INDEX_INPUT_NAME_SIZE,
    INDEX_INPUT_NAME_PAD, INDEX_INPUT_NAME_TEXT, INDEX_INPUT_UNIT_PRICE_SIZE,
    INDEX_INPUT_UNIT_PRICE_PAD, INDEX_INPUT_UNIT_PRICE_TEXT,
    INDEX_INPUT_STOCK_SIZE, INDEX_INPUT_STOCK_PAD, INDEX_INPUT_STOCK_TEXT,
    INDEX_INPUT_PERCENT_SIZE, INDEX_INPUT_PERCENT_PAD, INDEX_INPUT_PERCENT_TEXT,
    BUTTON_IMAGE, BUTTON_IMAGE_SIZE, STOCK_SECTION_CLEANER_OPTIONS,
    SORTER_BUTTON_UP_TEXT, SORTER_BUTTON_DOWN_TEXT, ADDER_SPIN_KEY,
    ADDER_SPIN_SIZE, ADDER_SPIN_PAD, ADDER_SPIN_VALUES, ADDER_BUTTON_KEY,
    ADDER_BUTTON_PAD, ADDER_BUTTON_TEXT, ADDER_BUTTON_TOOLTIP,
    STOCK_SECTION_CLEANER_OPTIONS, SAVE_AS_BUTTON_KEY, SAVE_AS_BUTTON_PAD,
    SAVE_AS_BUTTON_TEXT, SAVE_AS_BUTTON_TOOLTIP, SAVE_AS_BUTTON_INITIAL_FOLDER,
    SALELIST_S_SIZE, SALELIST_S_PAD, INDEX_INPUT_FINAL_PRICE_SIZE,
    INDEX_INPUT_FINAL_PRICE_PAD, INDEX_INPUT_FINAL_PRICE_TEXT,
    COMMERCE_BUTTON_KEY, COMMERCE_BUTTON_PAD, COMMERCE_BUTTON_TEXT,
    COMMERCE_BUTTON_TOOLTIP, TOTAL_PRICE_KEY, S_TMP_SIZE, S_TMP_PAD,
    PRE_VISULIZATOR_BUTTON_KEY, PRE_VISULIZATOR_BUTTON_PAD,
    PRE_VISULIZATOR_BUTTON_TEXT, PRE_VISULIZATOR_BUTTON_TOOLTIP,
    BUYSECTION_S_SIZE, BUYSECTION_S_PAD, INDEX_INPUT_AMOUNT_SIZE,
    INDEX_INPUT_AMOUNT_PAD, INDEX_INPUT_AMOUNT_TEXT, INDEX_INPUT_SUPPLIER_SIZE,
    INDEX_INPUT_SUPPLIER_PAD, INDEX_INPUT_SUPPLIER_TEXT, STOCKLIST_S_SIZE,
    STOCKLIST_S_PAD, TOTAL_PRICE_SIZE, TOTAL_PRICE_PAD, SORTER_COMBO_KEY,
    SORTER_COMBO_SIZE, SORTER_COMBO_PAD, SORTER_COMBO_TOOLTIP,
    SORTER_COMBO_STOCK_VALUES, SORTER_COMBO_SALES_VALUES,
    SORTER_COMBO_BUYS_VALUES, WINDOWS_SIZE, WINDOWS_LOCATION
)


class Section(Column):
    __key = None

    @classmethod
    def get_key(cls) -> str:
        return cls.__key

    @classmethod
    def key(cls, key):
        cls.__key = key

    def __init__(self, size: tuple, pad: tuple):
        super().__init__(layout=self.render_layout(), size=size, pad=pad)

    def render_finder(self) -> list:
        return [
            Input(
                key=self.__key + FINDER_INPUT_KEY,
                size=FINDER_INPUT_SIZE,
                pad=FINDER_INPUT_PAD
            ),
            Button(
                key=self.__key + FINDER_BUTTON_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=FINDER_BUTTON_PAD,
                button_text=FINDER_BUTTON_TEXT,
                tooltip=FINDER_BUTTON_TOOLTIP
            )
        ]

    def render_sorter(self) -> list:
        sort_values = self.get_sort_values()
        return [
            Combo(
                key=self.__key + SORTER_COMBO_KEY,
                values=sort_values,
                default_value=sort_values[0],
                size=SORTER_COMBO_SIZE,
                pad=SORTER_COMBO_PAD,
                tooltip=SORTER_COMBO_TOOLTIP,
                readonly=True
            ),
            Button(
                key=self.__key + SORTER_BUTTON_UP_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=SORTER_BUTTON_PAD,
                button_text=SORTER_BUTTON_UP_TEXT,
                tooltip=SORTER_BUTTON_UP_TOOLTIP
            ),
            Button(
                key=self.__key + SORTER_BUTTON_DOWN_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=SORTER_BUTTON_PAD,
                button_text=SORTER_BUTTON_DOWN_TEXT,
                tooltip=SORTER_BUTTON_DOWN_TOOLTIP
            ),
        ]

    def render_cleaner(self, values: list) -> list:
        return [
            Combo(
                key=self.__key + CLEANER_COMBO_KEY,
                size=CLEANER_COMBO_SIZE,
                pad=CLEANER_COMBO_PAD,
                values=values,
                default_value=values[0],
                readonly=True
            ),
            Button(
                key=self.__key + CLEANER_BUTTON_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=CLEANER_BUTTON_PAD,
                button_text=CLEANER_BUTTON_TEXT,
                tooltip=CLEANER_BUTTON_TOOLTIP
            )
        ]

    def render_apply(self) -> list:
        return [
            Button(
                key=self.__key + APPLY_BUTTON_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=APPLY_BUTTON_PAD,
                button_text=APPLY_BUTTON_TEXT,
                tooltip=APPLY_BUTTON_TOOLTIP
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
                pad=INDEX_COLUMN_PAD,
                element_justification='center'
            )
        ]

    def render_name_index(self) -> list:
        return self.render_base_index(
            INDEX_INPUT_NAME_SIZE, INDEX_INPUT_NAME_PAD, INDEX_INPUT_NAME_TEXT
        )

    def render_unit_price_index(self) -> list:
        return self.render_base_index(
            INDEX_INPUT_UNIT_PRICE_SIZE, INDEX_INPUT_UNIT_PRICE_PAD,
            INDEX_INPUT_UNIT_PRICE_TEXT
        )

    def render_stock_index(self) -> list:
        return self.render_base_index(
            INDEX_INPUT_STOCK_SIZE, INDEX_INPUT_STOCK_PAD,
            INDEX_INPUT_STOCK_TEXT
        )

    def render_percent_index(self) -> list:
        return self.render_base_index(
            INDEX_INPUT_PERCENT_SIZE, INDEX_INPUT_PERCENT_PAD,
            INDEX_INPUT_PERCENT_TEXT
        )

    def render_index(self) -> list:
        index = self.render_name_index()
        index += self.render_unit_price_index()
        index += self.render_stock_index()
        return index

    def render_record_list(self) -> list:
        return [self.get_record_list().instance()]

    def render_save_as(self) -> list:
        return [
            SaveAs(
                key=self.__key + SAVE_AS_BUTTON_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=SAVE_AS_BUTTON_PAD,
                button_text=SAVE_AS_BUTTON_TEXT,
                tooltip=SAVE_AS_BUTTON_TOOLTIP,
                file_types=(('', '.csv'), ),
                default_extension='.csv',
                initial_folder=SAVE_AS_BUTTON_INITIAL_FOLDER,
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


class StockAndBuySection:
    def render_adder(self) -> list:
        return [
            Spin(
                key=self.get_key() + ADDER_SPIN_KEY,
                size=ADDER_SPIN_SIZE,
                pad=ADDER_SPIN_PAD,
                values=ADDER_SPIN_VALUES,
                initial_value=0,
                readonly=True
            ),
            Button(
                key=self.get_key() + ADDER_BUTTON_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=ADDER_BUTTON_PAD,
                button_text=ADDER_BUTTON_TEXT,
                tooltip=ADDER_BUTTON_TOOLTIP
            )
        ]


class StockSection(Section, StockAndBuySection):
    @classmethod
    def get_sort_values(cls) -> list:
        return SORTER_COMBO_STOCK_VALUES

    def __init__(self):
        Section.__init__(self, STOCKLIST_S_SIZE, STOCKLIST_S_PAD)
        StockAndBuySection.__init__(self)

    def get_record_list(self) -> RecordList:
        return StockList

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_percent_index()
        return index

    def render_list(self) -> list:
        return [StockList.instance()]

    def render_cleaner(self) -> list:
        return super().render_cleaner(STOCK_SECTION_CLEANER_OPTIONS)

    def render_layout(self) -> list:
        layout = super().render_layout()
        layout[0] += self.render_adder()
        layout[0] += self.render_save_as()
        return layout


class CommerceSection(Section):
    @classmethod
    def render_layout_in_tab(cls) -> Tab:
        layout = [[cls()]]
        return Tab(cls.get_tab_title(), layout)

    def __init__(self, size: tuple, pad: tuple):
        super().__init__(size, pad)

    def render_amount_index(self) -> list:
        return super().render_base_index(
            INDEX_INPUT_AMOUNT_SIZE, INDEX_INPUT_AMOUNT_PAD,
            INDEX_INPUT_AMOUNT_TEXT
        )

    def render_final_price_index(self) -> list:
        return self.render_base_index(
            INDEX_INPUT_FINAL_PRICE_SIZE, INDEX_INPUT_FINAL_PRICE_PAD,
            INDEX_INPUT_FINAL_PRICE_TEXT
        )

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_amount_index()
        index += self.render_final_price_index()
        return index

    def render_commerce(self) -> list:
        return [
            Button(
                key=self.get_key() + COMMERCE_BUTTON_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=COMMERCE_BUTTON_PAD,
                button_text=COMMERCE_BUTTON_TEXT,
                tooltip=COMMERCE_BUTTON_TOOLTIP
            )
        ]

    def render_total_price(self) -> list:
        return [
            Text(text='$'),
            Text(
                key=self.get_key() + TOTAL_PRICE_KEY,
                size=TOTAL_PRICE_SIZE,
                pad=TOTAL_PRICE_PAD
            )
        ]

    def render_pre_visualizator(self) -> list:
        return [
            Button(
                key=self.get_key() + PRE_VISULIZATOR_BUTTON_KEY,
                image_data=BUTTON_IMAGE,
                image_size=BUTTON_IMAGE_SIZE,
                pad=PRE_VISULIZATOR_BUTTON_PAD,
                button_text=PRE_VISULIZATOR_BUTTON_TEXT,
                tooltip=PRE_VISULIZATOR_BUTTON_TOOLTIP
            )
        ]

    def render_cleaner(self) -> list:
        return super().render_cleaner(STOCK_SECTION_CLEANER_OPTIONS)

    def render_layout(self) -> list:
        """
        [
            [
                finder, sorter, cleaner, save_as,
                pre_visualizator, total_price, commerce
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
    @classmethod
    def get_sort_values(cls) -> list:
        return SORTER_COMBO_SALES_VALUES

    @classmethod
    def get_tab_title(cls) -> str:
        return 'VENTAS'

    def __init__(self):
        super().__init__(SALELIST_S_SIZE, SALELIST_S_PAD)

    def get_record_list(self) -> RecordList:
        return SaleList

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_percent_index()
        return index


class BuySection(CommerceSection, StockAndBuySection):
    @classmethod
    def get_sort_values(cls) -> list:
        return SORTER_COMBO_BUYS_VALUES

    @classmethod
    def get_tab_title(cls) -> str:
        return 'COMPRAS'

    def __init__(self):
        CommerceSection.__init__(self, BUYSECTION_S_SIZE, BUYSECTION_S_PAD)
        StockAndBuySection.__init__(self)

    def get_record_list(self) -> RecordList:
        return BuyList

    def render_supplier_index(self) -> list:
        return CommerceSection.render_base_index(
            self, INDEX_INPUT_SUPPLIER_SIZE, INDEX_INPUT_SUPPLIER_PAD,
            INDEX_INPUT_SUPPLIER_TEXT
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
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls.new()
        return cls._instance

    def __init__(self):
        FileManager.db_control()
        theme('PapelerAbasto')
        StockSection.key('StockSection.instance()')
        SaleSection.key('SaleSection.instance()')
        BuySection.key('BuySection.instance()')
        super().__init__(
            self.render_layout(),
            font=('Helvetica 16'),
            size=WINDOWS_SIZE,
            location=WINDOWS_LOCATION
        )
        self.run()

    def render_layout(self) -> list[list]:
        tab_group = [
            [
                SaleSection.render_layout_in_tab(),
                BuySection.render_layout_in_tab()
            ]
        ]
        layout = [[StockSection()], [TabGroup(tab_group)]]
        return layout

    def run(self):
        while True:
            e, _ = self.read()
            print(e)
            if e == None:
                self.close()
                break


if __name__ == '__main__':
    Main()
