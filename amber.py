
import webbrowser
from utilities.amber_analytics import AmberAnalytics
from kivymd.app import MDApp
from kivy.metrics import dp
from functools import partial
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem


class AmberContent(BoxLayout):
    pass


class AmberApp(MDApp, AmberAnalytics):
    def __init__(self):
        super().__init__()

    def dict_amber(self):
        return {
            'app_background': [54 / 255, 65 / 255, 79 / 255],
            'app_text': [81 / 255, 81 / 255, 81 / 255],
            'app_button_background': {
                'buy': [169 / 255, 199 / 255, 137 / 255],
                'sell': [204 / 255, 135 / 255, 135 / 255]
            },
            'app_button_text': [0, 0, 0],
            'dn_gold': [215 / 255, 163 / 255, 9 / 255],
            'input_box_background': [90 / 255, 101 / 255, 108 / 255],
            'input_box_hint': [158 / 255, 158 / 255, 158 / 255],
            'input_box_foreground': [1, 1, 1],
            'model_type': 'stock investment recommendation',
            'data': self.get_df_available_stocks_data,
            'buy': {
                'hint_text': 'investment dollar amount (default value is $1000)',
                'btn_text': 'buy recommendation',
                'btn_bind': self.show_investment_recommendations
            },
            'sell': {
                'hint_text': 'cash dollar amount (default value is $1000)',
                'btn_text': 'sell recommendation',
                'btn_bind': self.show_cash_recommendations
            }
        }

    def get_amber_buy_sell_widgets(self):
        self.root.ids.screen_manager.current = 'buy_sell_home'
        self.root.ids.buy_sell_box.clear_widgets()
        data = self.dict_amber().get('data')('./data/amber.xlsx')
        tp = TabbedPanel(
            tab_width=Window.width / 3, do_default_tab=False, tab_pos='bottom_mid',
            background_image='', background_color=self.dict_amber().get('app_background')
        )
        amber_layout = BoxLayout(orientation='vertical')
        default_tab = TabbedPanelItem(text='schema', color=self.dict_amber().get('dn_gold'), background_down='')
        default_tab_layout = BoxLayout(orientation='vertical')
        default_tab_title = MDLabel(
            text='Amber ROI: ' + self.dict_amber().get('model_type'), text_color=self.dict_amber().get('dn_gold'),
            size_hint=[1, 0.1], font_style='H5', halign='center', theme_text_color='Custom'
        )
        default_tab_layout.add_widget(default_tab_title)
        default_tab_layout.add_widget(Image(source=f"./assets/db_schema_amber.png", allow_stretch=True))
        default_tab.add_widget(default_tab_layout)
        tp.add_widget(default_tab)
        for action in ['buy', 'sell']:
            tab = TabbedPanelItem(text=action, color=self.dict_amber().get('dn_gold'), background_down='')
            tab_parent_layout = GridLayout(rows=2)
            top_layout = BoxLayout(orientation='horizontal', spacing='10sp', size_hint=[1, 0.15], padding=[10, 10, 10, 5])
            text_input = MDTextFieldRect(
                multiline=False, cursor_color='ffffff', font_size='18sp',
                hint_text=self.dict_amber().get(action).get('hint_text'), background_normal='',
                hint_text_color=self.dict_amber().get('input_box_hint'),
                foreground_color=self.dict_amber().get('input_box_foreground'),
                background_color=self.dict_amber().get('input_box_background')
            )
            given_input = text_input.text
            top_layout.add_widget(text_input)
            section_button = MDFillRoundFlatButton(
                text=self.dict_amber().get(action).get('btn_text'), font_size='20sp',
                size_hint=[0.6, 1], md_bg_color=self.dict_amber().get('app_button_background').get(action)
            )
            tab_result_layout = BoxLayout(orientation='vertical')
            section_button.bind(
                on_press=partial(
                    self.dict_amber().get(action).get('btn_bind'), tab_result_layout, given_input, data
                )
            )
            top_layout.add_widget(section_button)
            tab_parent_layout.add_widget(top_layout)
            tab_parent_layout.add_widget(tab_result_layout)
            tab.add_widget(tab_parent_layout)
            tp.add_widget(tab)
        amber_layout.add_widget(tp)
        self.root.ids.buy_sell_box.add_widget(amber_layout)

# ############################################################## decision -- buy

    def show_investment_recommendations(self, *args):
        result_widget = args[0]
        inv_dollar = args[1]
        df = args[2]
        row_data = []
        if inv_dollar == '':
            inv_dollar = 1000.0
        else:
            inv_dollar = float(inv_dollar)
        buy_list = self.get_investment_recommendations(inv_dollar, df)
        for i in buy_list:
            row_data.append(tuple(i))
        table = MDDataTable(
            use_pagination=True,
            column_data=[
                ('stock', dp(25)),
                ('investing_units', dp(45)),
                ('current_price', dp(45)),
                ('percent_change', dp(35))
            ],
            row_data=row_data
        )
        result_widget.clear_widgets()
        result_widget.add_widget(table)

# ############################################################## decision -- sell

    def show_cash_recommendations(self, *args):
        result_widget = args[0]
        _ = args[1]
        df = args[2]
        row_data = []
        sell_list = self.get_cash_recommendations(df)
        for i in sell_list:
            row_data.append(tuple(i))
        table = MDDataTable(
            use_pagination=True,
            column_data=[
                ('stock', dp(20)),
                ('oldest_price', dp(25)),
                ('oldest_quantity', dp(35)),
                ('current_price', dp(35)),
                ('percent_change', dp(35))
            ],
            row_data=row_data
        )
        result_widget.clear_widgets()
        result_widget.add_widget(table)

# ############################################################## generic

    def selection_dropdown(self, *args):
        parent_button = args[0]
        if args[1] == 'navbar':
            dropdown = DropDown()
            sub_item_list = self.get_sub_item_list().get(parent_button.text).get('sub_item_list')
            for sub_item in sub_item_list:
                btn = self.nav_bar_dropdown_parent(sub_item, parent_button, dropdown)
                dropdown.add_widget(btn)
        else:
            dropdown = args[1]
        dropdown.open(parent_button)

    def nav_bar_dropdown_parent(self, *args):
        sub_item = args[0]
        parent_button = args[1]
        dropdown = args[2]
        btn = Button(text=sub_item, size_hint_y=None, height=60)
        btn.bind(on_release=lambda x: self.selected_sub_item(parent_button, x.text, dropdown))
        return btn

    def selected_sub_item(self, *args):
        parent_button, text, dropdown = args[0], args[1], args[2]
        self.get_sub_item_list().get(parent_button.text).get('action')(text)
        dropdown.dismiss()

    def get_sub_item_list(self):
        return {
            'window size': {
                'sub_item_list': ['default', 'large'],
                'action': self.selected_window_size
            }
        }

    @staticmethod
    def selected_window_size(size):
        if size == 'large':
            Window.size = (1200, 800)
            Window.top = 60
            Window.left = 200
        else:
            Window.size = (800, 600)

    @staticmethod
    def amber_window_ss(img_nm):
        Window.screenshot(name=img_nm)

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    @staticmethod
    def dn_amber_demo():
        webbrowser.open('https://www.datanota.com/amber')

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'amber-data360'
        return AmberContent()


if __name__ == '__main__':
    AmberApp().run()
