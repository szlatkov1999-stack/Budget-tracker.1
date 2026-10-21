from kivy.config import Config
# Android'de klavye sorunları yaşamamak için eski uygulamandaki ayarı koruyoruz
Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("kivy", "keyboard_mode", "system")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
import json, os
from datetime import datetime

# --- RENK PALETİ (Eski uygulamandan alındı) ---
BG   = (0.05, 0.07, 0.12, 1)
CARD = (0.11, 0.14, 0.21, 1)
CHI  = (0.16, 0.20, 0.29, 1)
TXT  = (0.96, 0.97, 0.99, 1)
MUT  = (0.55, 0.62, 0.72, 1)
PUR  = (0.55, 0.36, 0.96, 1)
CYN  = (0.02, 0.71, 0.83, 1)
GRN  = (0.06, 0.72, 0.51, 1)
RED  = (0.94, 0.27, 0.42, 1)
YEL  = (0.98, 0.75, 0.14, 1)
DRK  = (0.05, 0.05, 0.10, 1)

Window.clearcolor = BG
DATA_FILE = "butce_veri.json"

# --- VERİ FONKSİYONLARI ---
def veri_yukle():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def veri_kaydet(islemler):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(islemler, f, ensure_ascii=False, indent=2)

# --- ÖZEL TASARIM SINIFLARI (Eski uygulamandan alındı) ---
class Kart(BoxLayout):
    def __init__(self, r=20, bg=CARD, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            self._c = Color(*bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[r])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

class Buton(Button):
    def __init__(self, r=16, bg=PUR, tc=TXT, **kw):
        super().__init__(**kw)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = tc
        self.bold = True
        self.font_size = '18sp'
        with self.canvas.before:
            self._c = Color(*bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[r])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

class In(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.foreground_color = TXT
        self.cursor_color = PUR
        self.font_size = '20sp'
        self.padding = [15, 10, 15, 10]
        self.multiline = False
        with self.canvas.before:
            self._c = Color(*CHI)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[14])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

class CustomSpinner(Spinner):
    def open_dropdown(self, *args):
        if self._dropdown:
            self._dropdown.max_height = Window.height * 0.5
        super().open_dropdown(*args)

# --- ANA UYGULAMA ---
class ButceApp(App):
    def build(self):
        self.title = "Gelir Gider Takip"
        self.islemler = veri_yukle()
        
        ana = BoxLayout(orientation="vertical", padding=[14, 14, 14, 10], spacing=10)
        
        # --- ÜST KART: BAKİYE ---
        u = Kart(r=26, orientation="vertical", size_hint_y=0.18, padding=[15, 15, 15, 15], spacing=2)
        self.bakiye_label = Label(text="", font_size="22sp", markup=True, halign="center")
        u.add_widget(self.bakiye_label)
        ana.add_widget(u)
        
        # --- ORTA KART: EKLEME FORMU ---
        form_kart = Kart(r=20, orientation="vertical", size_hint_y=0.42, padding=[15, 15, 15, 15], spacing=10)
        
        # Gelir/Gider Seçimi
        self.tur_spinner = CustomSpinner(text="Gider", values=("Gelir", "Gider"), background_normal='', background_color=CHI, color=TXT, font_size='18sp')
        
        # Tutar
        self.tutar_input = In(hint_text="Tutar (örn: 150.50)", input_filter="float", font_size='20sp')
        
        # Kategori
        self.kategori_spinner = CustomSpinner(text="Kategori", values=("Market", "Kira", "Fatura", "Ulaşım", "Maaş", "Ek Gelir", "Diğer"), background_normal='', background_color=CHI, color=TXT, font_size='18sp')
        
        # Kaydet Butonu
        btn_kaydet = Buton(text="KAYDET", bg=GRN, tc=DRK, r=20, size_hint_y=0.3, font_size="20sp")
        btn_kaydet.bind(on_press=self.kaydet)
        
        form_kart.add_widget(self.tur_spinner)
        form_kart.add_widget(self.tutar_input)
        form_kart.add_widget(self.kategori_spinner)
        form_kart.add_widget(btn_kaydet)
        ana.add_widget(form_kart)
        
        # --- ALT BÖLÜM: LİSTE ---
        self.scroll = ScrollView(size_hint=(1, 0.4))
        self.liste_kutu = GridLayout(cols=1, size_hint_y=None, spacing=8)
        self.liste_kutu.bind(minimum_height=self.liste_kutu.setter("height"))
        self.scroll.add_widget(self.liste_kutu)
        ana.add_widget(self.scroll)
        
        self.liste_yenile()
        self.bakiye_guncelle()
        return ana

    def kaydet(self, instance):
        try:
            tutar = float(self.tutar_input.text.replace(",", "."))
            if tutar <= 0: raise ValueError
        except ValueError:
            self.bakiye_label.text = "[color=ff6666]Hata: Geçerli bir tutar girin![/color]"
            return

        islem = {
            "tur": self.tur_spinner.text,
            "tutar": tutar,
            "kategori": self.kategori_spinner.text,
            "tarih": datetime.now().strftime("%d-%m-%Y %H:%M")
        }
        self.islemler.append(islem)
        veri_kaydet(self.islemler)
        
        self.tutar_input.text = ""
        self.liste_yenile()
        self.bakiye_guncelle()

    def sil(self, index):
        del self.islemler[index]
        veri_kaydet(self.islemler)
        self.liste_yenile()
        self.bakiye_guncelle()

    def liste_yenile(self):
        self.liste_kutu.clear_widgets()
        for i, islem in enumerate(reversed(self.islemler)):
            gercek_idx = len(self.islemler) - 1 - i
            
            renk = GRN if islem["tur"] == "Gelir" else RED
            isaret = "+" if islem["tur"] == "Gelir" else "-"
            
            # Her satır için özel Kart tasarımı
            satir = Kart(r=15, bg=CARD, orientation="horizontal", size_hint_y=None, height=60, padding=[15, 5, 15, 5], spacing=5)
            
            lbl = Label(text=f"{isaret} {islem['kategori']}\n[color=aaaaaa]{islem['tarih']}[/color]", font_size="14sp", halign="left", valign="middle", markup=True, color=renk)
            lbl.bind(size=lbl.setter("text_size"))
            
            tutar_lbl = Label(text=f"{islem['tutar']:.2f} TL", font_size="16sp", bold=True, color=renk, size_hint_x=0.35)
            
            btn_sil = Buton(text="Sil", bg=RED, r=10, size_hint_x=0.15, font_size="14sp")
            btn_sil.bind(on_press=lambda x, idx=gercek_idx: self.sil(idx))
            
            satir.add_widget(lbl)
            satir.add_widget(tutar_lbl)
            satir.add_widget(btn_sil)
            self.liste_kutu.add_widget(satir)

    def bakiye_guncelle(self):
        gelir = sum(i["tutar"] for i in self.islemler if i["tur"] == "Gelir")
        gider = sum(i["tutar"] for i in self.islemler if i["tur"] == "Gider")
        bakiye = gelir - gider
        renk = "66ff88" if bakiye >= 0 else "ff6666"
        
        self.bakiye_label.text = (
            f"[color=66ff88]Gelir: {gelir:.2f}[/color]  |  "
            f"[color=ff6666]Gider: {gider:.2f}[/color]\n"
            f"[b][color={renk}]Bakiye: {bakiye:.2f} TL[/color][/b]"
        )

if __name__ == "__main__":
    ButceApp().run()
