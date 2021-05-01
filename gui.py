import sys
import constant as ct
import PySimpleGUI as ps
import domain as dm
from multiprocessing import Process


theme = ct.THEME
ps.theme(theme)


class RecordAdderComponent:
    def __init__(self, key):
        self._layout = []
        self._element_record_adder = ps.Spin(values=ct.SPIN_RECORD_ADDER_VALUES, initial_value=0,
                                             size=ct.SIZES['xxxs'], key=key+',spin_add_records',
                                             readonly=True)
        self.render_layout(key)

    def layout(self):
        '''
        [  ADD_SPIN, ADD_BTT ]
        '''
        return self._layout

    def add(self):
        return self._element_record_adder.get()

    def render_layout(self, key):
        '''
        [ ADD_SPIN, ADD_BTT ]
        '''
        layout = [
            self._element_record_adder,
            ps.Button(button_text='➕', image_data=ct.IMAGE, font=ct.IMAGE_FONT,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['add'],
                      key=key+',add_records', image_size=ct.BTT_ASCII_IMAGE_SIZE)
        ]
        self._layout = layout


class TraderComponent:
    def __init__(self, key):
        self._key = key
        self._layout = []
        self._element_total_price = ps.Text(text='0000.00', key=key+',total_price',
                                            background_color='White', text_color='Black',
                                            size=ct.TOTAL_PRICE_SIZE, pad=((0, 3), (3, 3)))
        self._element_total_percent = ps.Spin(ct.SPIN_PERCENT_VALUES, initial_value=0, size=ct.SIZES['xxs'],
                                              enable_events=True, readonly=True, k=key+',update_total_percent')
        self.render_layout(key)

    def layout(self):
        '''
        [
            TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%
        ]
        '''
        return self._layout

    def render_layout(self, key):
        '''
        [
            TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%
        ]
        '''
        layout = [
            ps.Button(button_text='X', image_data=ct.IMAGE, image_size=ct.BTT_ASCII_IMAGE_SIZE,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['cancel_commerce'],
                      key=self._key+',cancel_commerce', pad=ct.CART_CANCEL_PAD, font=ct.IMAGE_FONT),
            ps.Button(button_text='$', image_data=ct.IMAGE, key=self._key+',accept_commerce',
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['accept_commerce'],
                      image_size=ct.BTT_ASCII_IMAGE_SIZE, font=ct.IMAGE_FONT),
            ps.Text(text='$', background_color='White', text_color='Black', pad=((3, 0), (3, 3))),
            self._element_total_price,
            self._element_total_percent
        ]
        self._layout = layout


class OptionsComponent:
    def __init__(self, key, list_components, layout):
        self._key = key
        self._list_components = list_components
        self._layout = [[]]
        self._element_export_options = ps.Combo(values=['STOCK', 'VENTAS', 'COMPRAS'], default_value='STOCK',
                                                size=ct.SIZES['s'], key=self._key+',export_option', readonly=True,
                                                pad=ct.FIRST_OPTION_PAD)
        self._element_export_path = ps.Input(default_text=ct.EXPORT_PATH, size=ct.SIZES['xxl'],
                                             readonly=True, key=self._key+',export_path')
        self.render_layout()
        self._funcs = {
            'export': self.export,
            'change_theme': self.change_theme
        }
        self.render_content_on(layout)

    def render_content_on(self, layout):
        '''
            [
                [ COL, COL ],
                [ FRAME ]
            ]
        '''
        options = self._layout
        options[0] += [
            ps.Button(button_text='', image_data=ct.PNG_TABLE, key=self._key+',report_view',
                      image_size=ct.BTT_GENERAL_IMAGE_SIZE, border_width=ct.BTT_BORDER_WIDTH,
                      tooltip=ct.BTT_TOOLTIPS['report_view']),
            ps.Button(button_text='', image_data=ct.PNG_THEME_CHANGE(), key=self._key+',change_theme',
                      image_size=ct.BTT_GENERAL_IMAGE_SIZE, border_width=ct.BTT_BORDER_WIDTH,
                      tooltip=ct.BTT_TOOLTIPS['change_theme']),
            ps.Button(button_text='', image_data=ct.PNG_EXIT, key='exit',
                      image_size=ct.BTT_GENERAL_IMAGE_SIZE, border_width=ct.BTT_BORDER_WIDTH,
                      tooltip=ct.BTT_TOOLTIPS['exit'])
        ]
        options_col = [
            [
                ps.Column(layout=options, size=ct.OPTIONS_COL_SIZE, pad=(0, 0),
                          element_justification='center')
            ]
        ]
        _layout = [
            ps.Frame(title='↓ OPCIONES ↓', title_color=ct.FRAME_TITLE_COLOR[theme],
                     layout=options_col, title_location='n', pad=ct.OPTIONS_FRAME_PAD,
                     element_justification='center')
        ]
        layout.append(_layout)

    def layout(self):
        '''
        [
            [ EXP_COMB, EXP_SAVEAS, EXP_IN, EXP_BTT ]
        ]
        '''
        return self._layout

    def render_layout(self):
        '''
        [
            [ EXP_COMB, EXP_SAVEAS, EXP_IN, EXP_BTT ]
        ]
        '''
        exporter = [
            [
                self._element_export_options,
                ps.FileSaveAs(button_text='', initial_folder=ct.EXPORT_PATH,
                              target=(555666777, +2), tooltip=ct.BTT_TOOLTIPS['folder'],
                              image_data=ct.PNG_FOLDER, image_size=ct.BTT_GENERAL_IMAGE_SIZE,
                              file_types=(('', '.csv'), ), default_extension='.csv'),
                self._element_export_path,
                ps.Button(button_text='', image_data=ct.PNG_EXPORT, key=self._key+',export',
                          border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['export'],
                          image_size=ct.BTT_GENERAL_IMAGE_SIZE)
            ]
        ]
        self._layout = exporter

    def export(self):
        {
            'STOCK': self._list_components[0], 'VENTAS': self._list_components[1], 'COMPRAS': self._list_components[2]
        }[self._element_export_options.get()].export(self._element_export_path.get())

    def change_theme(self):
        ct.__restart__ = True
        theme = 'PapelerAbasto' if ct.THEME == 'Default1' else 'Default1'
        dm.FileManager.save_in_json(theme, 'theme.json')

    def callback(self, func):
        self._funcs[func]()


class SectionComponent:
    def __init__(self, key):
        self._key = key
        self._layout = [[]]
        self._element_input_searcher = ps.Input(default_text='', key=self._key+',searcher',
                                                size=ct.SIZES['l'], pad=ct.SEARCHER_PAD)
        self._element_sort_options = 0
        self._element_clean_options = ps.Combo(values=self._clean_options, default_value=self._clean_options[0],
                                               size=ct.SIZES['+m'], key=self._key+',clean_options', readonly=True)
        self._funcs = {
            'search': self.search,
            'sort_min_max': self.sort_min_max,
            'sort_max_min': self.sort_max_min,
            'export': self.export,
            'apply': self.apply
        }

    def layout(self):
        return self._layout

    def render_apply(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ]
        ]
        '''
        apply = ps.Button(button_text='✓', image_data=ct.IMAGE, pad=ct.APPLY_PAD, font=ct.IMAGE_FONT,
                          border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['apply'],
                          key=self._key+',apply', image_size=ct.BTT_ASCII_IMAGE_SIZE)
        self._layout[-1].append(apply)

    def render_sorter(self, combo_size=ct.SIZES['s'], btt_size=ct.BTT_GENERAL_IMAGE_SIZE,
                      btt_pad=ct.BTT_FIRST_SORT_PAD):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ]
        ]
        '''
        self._element_sort_options = ps.Combo(values=self._sort_options, default_value=self._sort_options[0],
                                              size=combo_size, key=self._key+',sort_options', readonly=True)
        sorter = [
            self._element_sort_options,
            ps.Button(button_text='', image_data=ct.PNG_SORT_MIN_TO_MAX, pad=btt_pad,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['sort_min_max'],
                      key=self._key+',sort_min_max', image_size=btt_size),
            ps.Button(button_text='', image_data=ct.PNG_SORT_MAX_TO_MIN, pad=btt_pad,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['sort_max_min'],
                      key=self._key+',sort_max_min', image_size=btt_size)
        ]
        self._layout[0] += sorter

    def render_layout(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, APPLY_BTT ]
        ]
        '''
        self.render_searcher()
        self.render_first_index()
        self.render_apply()

    def render_searcher(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT ]
        ]
        '''
        searcher = [
            self._element_input_searcher,
            ps.Button(button_text='', image_data=ct.PNG_SEARCH,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['search'],
                      key=self._key+',search', image_size=ct.BTT_GENERAL_IMAGE_SIZE)
        ]
        self._layout[0] += searcher

    def render_first_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN ]
        ]
        '''
        index = [
            ps.Input(default_text='Nombre', size=ct.SIZES['l'],
                     pad=ct.FIRST_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ P/U', size=ct.SIZES['+s'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True)
        ]
        self._layout.append(index)

    def record_col(self, fields):
        name = [
            fields[0]
        ]
        layout = [
            name, fields[1:]
        ]
        return [
            ps.Column(layout=layout)
        ]

    def render_records(self, size):
        records = [
            record.fields() for record in self._list_control.records()
        ]
        records_list = [
            ps.Column(layout=records, size=size, scrollable=True,
                      vertical_scroll_only=True, pad=ct.RECORD_COL_PAD,
                      key=self._key)
        ]
        self._layout.append(records_list)

    def callback(self, func):
        self._funcs[func]()

    def render_record_to_top(self, index):
        record_to_top = self._records[index].report()
        for i in reversed(range(1, index+1)):
            self._records[i].update(self._records[i-1].report())
        self._records[0].update(record_to_top)

    def search(self):
        index = self._list_control.search(self._layout[0][0].get())
        if index:
            self.render_record_to_top(index)

    def sort(self, sorted_report):
        for i, record in enumerate(self._records):
            record.update(sorted_report[i])

    def sort_min_max(self):
        self.sort(self._list_control.sorted_report_min_max(ct.INDEX[self._element_sort_options.get()]))

    def sort_max_min(self):
        self.sort(self._list_control.sorted_report_max_min(ct.INDEX[self._element_sort_options.get()]))

    def update_rendered_records(self):
        '''
        Actualiza el "layout" según los "registros"
        '''
        for i in range(len(self._layout)):
            self._records[i].update()

    def clean_selected(self):
        self._list_control.clean_selected()

    def export(self, path):
        self._list_control.export(path)

    def save(self):
        self._list_control.save()


class StockSectionComponent(SectionComponent):
    def __init__(self, key, layout):
        dm.StockRecord.key(key)
        self._list_control = dm.StockList.instance()
        dm.StockList.key(key)
        self._records = self._list_control.records()
        self._sort_options = [
            'Nombre', '$ P/U', 'Stock', '%'
        ]
        self._clean_options = [
            'Seleccionados', 'Vacíos'
        ]
        super().__init__(key)
        self._record_adder = RecordAdderComponent(self._key)
        funcs = {
            'add_records': self.add_records,
            'clean': self.clean,
            'secure_mode': self.secure_mode
        }
        self._funcs.update(funcs)
        self.render_layout()
        self.render_content_on(layout)

    def render_content_on(self, layout):
        '''
        [
            [ COL ]
        ]
        '''
        col = [
            [
                ps.Column(layout=self._layout, size=ct.STOCK_COL_SIZE, pad=(0, 0))
            ]
        ]
        frame = [
            [
                ps.Frame(title='↓ STOCK ↓', title_color=ct.FRAME_TITLE_COLOR[theme],
                         layout=col, title_location='n', pad=ct.SECTION_FRAME_PAD)
            ]
        ]
        _layout = ps.Column(layout=frame)
        layout[0].append(_layout)

    def render_layout(self):
        '''
        [ 
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT, ADD_SPIN, ADD_BTT ]
        ]
        '''
        super().render_layout()
        self.render_sorter(combo_size=ct.SIZES['+s'], btt_size=(20, 20), btt_pad=None)
        self.render_index()
        self.render_records()
        self.render_cleaner()
        self.render_record_adder()
        self.render_secure_mode()

    def render_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ]
        ]
        '''
        index = ps.Input(default_text='Stock', size=ct.SIZES['xs'],
                         pad=ct.LAST_INDEX_INPUT_PAD, readonly=True)
        self._layout[-1] = self._layout[-1][:2] + [index] + [self._layout[-1][-1]]

    def render_secure_mode(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ]
        ]
        '''
        self._layout[-1].append(ps.Button(button_text='', key=self._key+',secure_mode',
                                          image_data=ct.PNG_SECURE_MODE(), tooltip=ct.BTT_TOOLTIPS['secure_mode'],
                                          image_size=ct.BTT_GENERAL_IMAGE_SIZE, border_width=ct.BTT_BORDER_WIDTH))

    def render_records(self):
        '''
        [ 
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ]
        ]
        '''
        super().render_records(size=ct.STOCK_RCS_LIST_COL_SIZE)

    def render_cleaner(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT ]
        ]
        '''
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='➖', image_data=ct.IMAGE, font=ct.IMAGE_FONT,
                      border_width=ct.BTT_BORDER_WIDTH,  tooltip=ct.BTT_TOOLTIPS['delete'],
                      key=self._key+',clean', image_size=ct.BTT_ASCII_IMAGE_SIZE)
        ]
        self._layout.append(cleaner)

    def render_record_adder(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT, ADD_SPIN, ADD_BTT ]
        ]
        '''
        layout = self._record_adder.layout()
        self._layout[-1] += layout

    def secure_mode(self):
        self._layout[-1][-1].update(image_data=ct.PNG_SECURE_MODE(),
                                    image_size=ct.BTT_GENERAL_IMAGE_SIZE)
        for record in self._records:
            record.secure_mode()

    def add_records(self):
        add = self._record_adder.add()
        if add:
            self._list_control.add_records(add)
            ct.__restart__ = True

    def clean(self):
        if self._element_clean_options.get() == 'Vacíos':
            self._list_control.clean_empty()
        else:
            self._list_control.clean_selected()

    def apply(self):
        self._list_control.apply()

    def buy(self, records):
        self._list_control.buy(records)


class SalesSectionComponent(SectionComponent):
    def __init__(self, key, layout):
        self._instance = self
        dm.SaleRecord.key(key)
        self._list_control = dm.SaleList.instance()
        self._records = self._list_control.records()
        self._sort_options = [
            'Nombre', '$ P/U', 'Stock', 'Cant.', '$ Fin.', '%'
        ]
        self._clean_options = [
            'Seleccionados', 'Todos'
        ]
        super().__init__(key)
        self._trader = TraderComponent(self._key)
        funcs = {
            'accept_commerce': self.sell
        }
        self._funcs.update(funcs)
        self.render_layout()
        self.render_content_on(layout)

    def render_content_on(self, layout):
        '''
            [
                [ FRAME ]
            ]
        '''
        col = [
            [
                ps.Column(layout=self._layout, size=ct.SALES_COL_SIZE, pad=(0, 0))
            ]
        ]
        sales_sc = ps.Frame(title='↓ VENTAS ↓', title_color=ct.FRAME_TITLE_COLOR[theme],
                            layout=col, title_location='n', pad=ct.SECTION_FRAME_PAD)
        layout[0].append(sales_sc)

    def render_layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],  
            [ RCS_LIST_COL ],  
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]  
        ]
        """
        super().render_layout()
        self.render_sorter()
        self.render_index()
        self.render_records()
        self.render_trader()
        self.render_cleaner()

    def render_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ]  
        ]
        '''
        index = [
            ps.Input(default_text='Stock', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='Cant.', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ Fin.', size=ct.SIZES['xs'],
                     pad=ct.LAST_INDEX_INPUT_PAD, readonly=True),
        ]
        self._layout[-1] = self._layout[-1][:2] + index + [self._layout[-1][-1]]

    def render_trader(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        '''
        layout = self._trader.layout()
        self._layout.append(layout)

    def render_cleaner(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]
        ]
        '''
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='➖', image_data=ct.IMAGE, font=ct.IMAGE_FONT,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['delete'],
                      key=self._key+',clean', image_size=ct.BTT_ASCII_IMAGE_SIZE)
        ]
        self._layout[-1] += cleaner

    def render_records(self):
        '''
        [ 
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ]
        ]
        '''
        super().render_records(size=ct.SALES_RCS_LIST_COL_SIZE)

    def apply(self):
        self._layout[-1][3].update(self._list_control.apply(float(self._layout[-1][4].get())))

    def sell(self):
        self._list_control.sell()


class BuysSectionComponent(SectionComponent):
    def __init__(self, key, layout):
        dm.BuyRecord.key(key)
        self._list_control = dm.BuyList.instance()
        self._records = self._list_control.records()
        self._sort_options = [
            'Nombre', '$ P/U', 'Stock', 'Cant.', 'Proveedor', '$ Fin.', '%'
        ]
        self._clean_options = [
            'Seleccionados', 'Todos'
        ]
        super().__init__(key)
        self._trader = TraderComponent(self._key)
        self._record_adder = RecordAdderComponent(self._key)
        funcs = {
            'add_records': self.add_records,
            'collect': self.collect,
            'accept_commerce': self.buy
        }
        self._funcs.update(funcs)
        self.render_layout()
        self.render_content_on(layout)

    def render_content_on(self, layout):
        '''
            [
                [ FRAME ],
                [ FRAME ]
            ]
        '''
        col = [
            [
                ps.Column(layout=self._layout, size=ct.BUYS_COL_SIZE, pad=(0, 0))
            ]
        ]
        buys_sc = [
            ps.Frame(title='↓ COMPRAS ↓', title_color=ct.FRAME_TITLE_COLOR[theme],
                     layout=col, title_location='n', pad=ct.SECTION_FRAME_PAD)
        ]
        _layout = [
            [
                layout[0][1]
            ], buys_sc
        ]
        _layout_col = ps.Column(layout=_layout)
        layout[0][1] = _layout_col

    def render_layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],    
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],  
            [ RCS_LIST_COL ],  
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT, ADD_SPIN, ADD_BTT ]  
        ]
        """
        super().render_layout()
        self.render_sorter()
        self.render_index()
        self.render_records()
        self.render_trader()
        self.render_price_collector()
        self.render_cleaner()
        self.render_record_adder()

    def render_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ]  
        ]
        '''
        index = [
            ps.Input(default_text='Stock', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='Cant.', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ Fin.', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='Proveedor', size=ct.SIZES['s'],
                     pad=ct.LAST_INDEX_INPUT_PAD, readonly=True)
        ]
        self._layout[-1] = self._layout[-1][:2] + index + [self._layout[-1][-1]]

    def render_trader(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        '''
        self._layout.append(self._trader.layout())

    def render_price_collector(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        '''
        price_collector = ps.Button(button_text='⟳', image_data=ct.IMAGE, font=ct.IMAGE_FONT,
                                    border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['refresh'],
                                    key=self._key+',collect', image_size=ct.BTT_ASCII_IMAGE_SIZE)
        self._layout[0].append(price_collector)

    def render_cleaner(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]
        ]
        '''
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='➖', image_data=ct.IMAGE, font=ct.IMAGE_FONT,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['delete'],
                      key=self._key+',clean', image_size=ct.BTT_ASCII_IMAGE_SIZE)
        ]
        self._layout[-1] += cleaner

    def render_record_adder(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT, ADD_SPIN, ADD_BTT ]
        ]
        '''
        layout = self._record_adder.layout()
        self._layout[-1] += layout

    def render_records(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ]
        ]
        '''
        records = super().render_records(size=ct.BUYS_RCS_LIST_COL_SIZE)

    def add_records(self):
        add = self._record_adder.add()
        if add:
            self._list_control.add_records(add)
            ct.__restart__ = True

    def apply(self):
        # actualiza el precio total
        self._layout[-1][3].update(self._list_control.apply(self._layout[-1][4].get()))

    def collect(self):
        self._list_control.collect()

    def buy(self):
        self._list_control.buy()


class Main:
    _window = None

    @classmethod
    def window(cls):
        return cls._window

    @classmethod
    def set_window(cls, window):
        cls._window = window

    def __init__(self, location):
        dm.FileManager.file_control()
        self._layout = [[]]
        self._stock_sc = StockSectionComponent('self._stock_sc', self._layout)
        self._sales_sc = SalesSectionComponent('self._sales_sc', self._layout)
        self._buys_sc = BuysSectionComponent('self._buys_sc', self._layout)
        self._list_components = [
            self._stock_sc, self._sales_sc, self._buys_sc
        ]
        self._options = OptionsComponent('self._options', self._list_components, self._layout)
        window = ps.Window(title='Papelera Abasto', icon=ct.PNG_ICON,
                           layout=self._layout, location=location,
                           font=('Helvetica 14'), finalize=True,
                           margins=(0, 0))
        Main.set_window(window)

    def save(self):
        for list_component in self._list_components:
            list_component.save()

    def close(self, timeout=0):
        self._window.read(timeout=timeout)
        self._window.close()
        exit()

    def restart(self):
        Process(target=dm.FileManager.restart, args=(self._window.current_location(), )).start()
        self.close(2000)

    def run(self):
        while True:
            event, _ = self._window.read()
            if event in (None, 'exit'):
                self.save()
                self.close()
            print(event)
            # try:
            splited_event = event.split(',')
            var, func = splited_event[0], splited_event[1]
            getattr(eval(var), 'callback')(func)
            # except:
            #     ct.__restart__ = False
            # if ct.__restart__:
            #     self.save()
            #     self.restart()


if __name__ == '__main__':
    Main((20, 20)).run()
